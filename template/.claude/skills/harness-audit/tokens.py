#!/usr/bin/env python3
"""On-demand, read-only token and context report over Claude Code transcripts.

Usage: python3 .claude/skills/harness-audit/tokens.py [--project SUBSTR] [--since YYYY-MM-DD]
       [--until YYYY-MM-DD] [--session ID_PREFIX] [--json]

Writes only to stdout. Prints sizes, tool names and file paths, never message text.
"""
import argparse
import collections
import datetime
import heapq
import json
import os
import re
import sys

ROOT = os.path.join(os.environ.get("CLAUDE_CONFIG_DIR") or os.path.expanduser("~/.claude"), "projects")
# Opus price ratios relative to one uncached input token (same as the ad-hoc usage scripts).
W_CACHE_READ, W_CACHE_WRITE, W_OUTPUT = 0.1, 1.25, 5
REBUILD_THRESHOLD = 20_000
WRITE_TOOLS = ("Edit", "Write", "MultiEdit", "NotebookEdit")


def weight(inp, cr, cw, out):
    return inp + cr * W_CACHE_READ + cw * W_CACHE_WRITE + out * W_OUTPUT


PROJECT_PREFIXES = []
TEMP_PREFIXES = ("-private-var-folders-", "-var-folders-", "-tmp-", "-private-tmp-")


def encode(path):
    return re.sub(r"[^A-Za-z0-9]", "-", path) + "-"


def set_project_prefix(dirnames):
    """Project dirs encode absolute paths. Drop the encoded parent of the current
    directory, else the shared prefix of the scanned projects, else the encoded home, so labels
    are short and carry no username."""
    global PROJECT_PREFIXES
    real = [d for d in dirnames if not d.startswith(TEMP_PREFIXES)]
    common = os.path.commonprefix(real) if len(real) > 1 else ""
    common = common[:common.rfind("-") + 1]
    PROJECT_PREFIXES = [encode(os.path.dirname(os.getcwd()))]
    if len(common) > 1:
        PROJECT_PREFIXES.append(common)
    PROJECT_PREFIXES.append(encode(os.path.expanduser("~")))


def project_label(dirname):
    if dirname.startswith(TEMP_PREFIXES):
        return "(temp dirs)"
    for prefix in PROJECT_PREFIXES:
        if dirname.startswith(prefix):
            return dirname[len(prefix):]
    return dirname


def turn_kind(msg):
    """Classify the line that starts a turn. Tool results and meta lines return None."""
    content = msg.get("message", {}).get("content")
    if msg.get("isCompactSummary"):
        return "other"
    if isinstance(content, str):
        if "<task-notification>" in content:
            return "notification"
        # Meta lines (skill text, reminders) do not start a turn, except a channel message.
        if msg.get("isMeta") and "<channel" not in content:
            return None
        return "human"
    if isinstance(content, list):
        texts = []
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "tool_result":
                return None
            if block.get("type") == "text":
                texts.append(block.get("text", ""))
        joined = "".join(texts)
        if "<task-notification>" in joined:
            return "notification"
        return "human" if joined else "other"
    return "other"


def result_size(content):
    if isinstance(content, str):
        return len(content)
    total = 0
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict):
                total += len(block.get("text", "") or "")
                src = block.get("source")
                if isinstance(src, dict):
                    total += len(src.get("data", "") or "")
    return total


def discover(args):
    since_ts = None
    if args.since:
        since_ts = datetime.datetime.fromisoformat(args.since).replace(tzinfo=datetime.timezone.utc).timestamp()
    files = []
    if not os.path.isdir(ROOT):
        sys.exit(f"no transcripts at {ROOT} (set CLAUDE_CONFIG_DIR if Claude Code keeps its data elsewhere)")
    for proj in sorted(os.listdir(ROOT)):
        pdir = os.path.join(ROOT, proj)
        if not os.path.isdir(pdir) or (args.project and args.project not in proj):
            continue
        for dirpath, _dirs, names in os.walk(pdir):
            for name in names:
                if not name.endswith(".jsonl"):
                    continue
                path = os.path.join(dirpath, name)
                rel = os.path.relpath(path, pdir).split(os.sep)
                sid = rel[0][:-6] if rel[0].endswith(".jsonl") else rel[0]
                if args.session and not sid.startswith(args.session):
                    continue
                try:
                    if since_ts is not None and os.path.getmtime(path) < since_ts:
                        continue
                except OSError:
                    continue
                files.append((proj, sid, os.sep + "subagents" + os.sep in path, path))
    set_project_prefix({f[0] for f in files})
    return files


class Session:
    def __init__(self, proj, sid):
        self.proj, self.sid = proj, sid
        self.main = collections.Counter()
        self.sub = collections.Counter()
        self.ctx_sum = 0
        self.ctx_peak = 0
        self.turns = 0
        self.compactions = []
        self.rebuilds = []
        self.reread = collections.Counter()
        self.timeline = []


def scan(files, args):
    since = args.since or ""
    until = args.until or "9999-99-99"
    seen = set()
    sessions = {}
    kinds = collections.defaultdict(collections.Counter)
    results_heap = []
    reread_files = collections.Counter()
    stats = collections.Counter()
    malformed = 0
    unreadable = 0
    # main files first so a message copied into a subagent file keeps its main-session role
    files = sorted(files, key=lambda f: f[2])
    for proj, sid, is_sub_file, path in files:
        sess = sessions.setdefault((proj, sid), Session(proj, sid))
        tool_names = {}
        tool_paths = {}
        last_op = {}
        file_calls = 0
        turn = "other"
        turn_open = False
        cur = None
        try:
            fh = open(path, encoding="utf-8", errors="replace")
        except OSError:
            unreadable += 1
            continue
        with fh:
            for line in fh:
                if not ('"type":"assistant"' in line or '"type":"user"' in line or "compact_boundary" in line):
                    continue
                try:
                    d = json.loads(line)
                except ValueError:
                    malformed += 1
                    continue
                ts = d.get("timestamp", "")
                if ts and (ts < since or ts[:10] > until):
                    continue
                typ = d.get("type")
                stats["bytes_total"] += len(line)
                if typ == "system":
                    if d.get("subtype") == "compact_boundary" and not is_sub_file:
                        meta = d.get("compactMetadata") or {}
                        ev = {"ts": ts, "pre": meta.get("preTokens", 0), "post": meta.get("postTokens", 0),
                              "ms": meta.get("durationMs", 0)}
                        sess.compactions.append(ev)
                        if cur:
                            sess.timeline.append(cur)
                            cur = None
                        sess.timeline.append({"compaction": ev})
                    continue
                msg = d.get("message") or {}
                content = msg.get("content")
                if typ == "user":
                    kind = turn_kind(d)
                    if kind is None:
                        if isinstance(content, list):
                            for block in content:
                                if isinstance(block, dict) and block.get("type") == "tool_result":
                                    size = result_size(block.get("content"))
                                    stats["bytes_results"] += size
                                    name = tool_names.get(block.get("tool_use_id"), "?")
                                    entry = (size, name, tool_paths.get(block.get("tool_use_id"), ""), sid[:8])
                                    if len(results_heap) < 10:
                                        heapq.heappush(results_heap, entry)
                                    elif entry > results_heap[0]:
                                        heapq.heapreplace(results_heap, entry)
                    elif not is_sub_file:
                        turn, turn_open = kind, True
                    continue
                if typ != "assistant":
                    continue
                if isinstance(content, list):
                    for block in content:
                        if not isinstance(block, dict) or block.get("type") != "tool_use":
                            continue
                        tid, name = block.get("id"), block.get("name", "?")
                        tool_names[tid] = name
                        inp = block.get("input") or {}
                        fpath = inp.get("file_path") or inp.get("notebook_path") or ""
                        if fpath:
                            tool_paths[tid] = fpath
                        if name == "Read" and fpath:
                            if last_op.get(fpath) == "read":
                                sess.reread[fpath] += 1
                                reread_files[fpath] += 1
                            last_op[fpath] = "read"
                        elif name in WRITE_TOOLS and fpath:
                            last_op[fpath] = "write"
                usage, mid = msg.get("usage"), msg.get("id")
                if not usage or not mid:
                    continue
                key = (mid, d.get("requestId"))
                if key in seen:
                    continue
                seen.add(key)
                inp_t = usage.get("input_tokens", 0) or 0
                cr = usage.get("cache_read_input_tokens", 0) or 0
                cw = usage.get("cache_creation_input_tokens", 0) or 0
                out = usage.get("output_tokens", 0) or 0
                w = weight(inp_t, cr, cw, out)
                ctx = inp_t + cr + cw
                file_calls += 1
                if file_calls > 1 and cw > REBUILD_THRESHOLD:
                    sess.rebuilds.append({"ts": ts, "cache_creation": cw, "sub": is_sub_file or bool(d.get("isSidechain"))})
                bucket = sess.sub if (is_sub_file or d.get("isSidechain")) else sess.main
                bucket["in"] += inp_t
                bucket["cr"] += cr
                bucket["cw"] += cw
                bucket["out"] += out
                bucket["calls"] += 1
                bucket["w"] += w
                if bucket is sess.sub:
                    kinds["subagent"]["calls"] += 1
                    kinds["subagent"]["w"] += w
                    kinds["subagent"]["ctx"] += ctx
                    continue
                sess.ctx_sum += ctx
                sess.ctx_peak = max(sess.ctx_peak, ctx)
                k = kinds[turn]
                k["calls"] += 1
                k["w"] += w
                k["ctx"] += ctx
                if turn_open:
                    k["turns"] += 1
                    sess.turns += 1
                    turn_open = False
                    if cur:
                        sess.timeline.append(cur)
                    cur = {"ts": ts, "start": turn, "ctx": 0, "cr": 0, "cw": 0, "out": 0, "calls": 0}
                if cur is None:
                    cur = {"ts": ts, "start": turn, "ctx": 0, "cr": 0, "cw": 0, "out": 0, "calls": 0}
                cur["ctx"] = max(cur["ctx"], ctx)
                cur["cr"] += cr
                cur["cw"] += cw
                cur["out"] += out
                cur["calls"] += 1
        if cur:
            sess.timeline.append(cur)
    return sessions, kinds, sorted(results_heap, reverse=True), reread_files, stats, malformed, unreadable


def build_report(sessions, kinds, top_results, reread_files, stats, malformed, unreadable, nfiles, args):
    per_project = collections.defaultdict(lambda: {"main": collections.Counter(), "sub": collections.Counter()})
    for s in sessions.values():
        per_project[project_label(s.proj)]["main"].update(s.main)
        per_project[project_label(s.proj)]["sub"].update(s.sub)
    total_w = sum(c["w"] for p in per_project.values() for c in p.values())
    sess_rows = []
    for s in sessions.values():
        w = s.main["w"] + s.sub["w"]
        if not w:
            continue
        calls = s.main["calls"]
        sess_rows.append({
            "project": project_label(s.proj), "session": s.sid, "weighted": w,
            "subagent_share": s.sub["w"] / w, "turns": s.turns, "main_calls": calls,
            "avg_context": s.ctx_sum / calls if calls else 0, "peak_context": s.ctx_peak,
            "compactions": len(s.compactions),
        })
    sess_rows.sort(key=lambda r: -r["weighted"])
    kind_rows = {k: dict(v) for k, v in kinds.items()}
    rebuild_rows = sorted(
        ({"project": project_label(s.proj), "session": s.sid, "count": len(s.rebuilds),
          "tokens": sum(r["cache_creation"] for r in s.rebuilds)}
         for s in sessions.values() if s.rebuilds), key=lambda r: -r["tokens"])
    reread_rows = sorted(
        ({"project": project_label(s.proj), "session": s.sid, "count": sum(s.reread.values()),
          "top_files": s.reread.most_common(3)} for s in sessions.values() if s.reread),
        key=lambda r: -r["count"])
    compactions = [dict(c, project=project_label(s.proj), session=s.sid)
                   for s in sessions.values() for c in s.compactions]
    compactions.sort(key=lambda c: c["ts"])
    report = {
        "filters": {"project": args.project, "since": args.since, "until": args.until, "session": args.session},
        "files_scanned": nfiles, "malformed_lines": malformed, "unreadable_files": unreadable,
        "weights": {"input": 1, "cache_read": W_CACHE_READ, "cache_creation": W_CACHE_WRITE, "output": W_OUTPUT},
        "weighted_total": total_w,
        "projects": {p: {"main": dict(v["main"]), "subagents": dict(v["sub"])} for p, v in per_project.items()},
        "top_sessions": sess_rows[:10],
        "turn_starts": kind_rows,
        "waste": {
            "cache_rebuilds_total": sum(r["count"] for r in rebuild_rows),
            "cache_rebuild_tokens_total": sum(r["tokens"] for r in rebuild_rows),
            "cache_rebuilds_top_sessions": rebuild_rows[:10],
            "rereads_total": sum(reread_files.values()),
            "rereads_top_sessions": reread_rows[:10],
            "rereads_top_files": reread_files.most_common(10),
            "tool_result_bytes": stats["bytes_results"], "transcript_bytes": stats["bytes_total"],
            "largest_tool_results": [{"bytes": b, "tool": n, "path": p, "session": s} for b, n, p, s in top_results],
            "compaction_count": len(compactions),
            "compactions": compactions,
        },
    }
    if args.session:
        report["timeline"] = {s.sid: s.timeline for s in sessions.values() if s.timeline}
    return report


def m(x):
    return f"{x / 1e6:.1f}M"


def k(x):
    return f"{x / 1e3:.0f}k"


def pct(a, b):
    return f"{100 * a / b:.1f}%" if b else "0.0%"


def render_text(r, args):
    out = []
    p = out.append
    tw = r["weighted_total"]
    p(f"files {r['files_scanned']}  malformed lines {r['malformed_lines']}  unreadable files {r['unreadable_files']}")
    p(f"weighted = input + {W_CACHE_READ} x cache read + {W_CACHE_WRITE} x cache creation + {W_OUTPUT} x output (Opus ratios, all models)")
    p("")
    p(f"1. TOTALS  weighted {m(tw)}")
    p(f"{'project':32} {'role':9} {'calls':>7} {'input':>8} {'c.read':>9} {'c.write':>9} {'output':>8} {'weighted':>9} {'share':>6}")
    for proj, v in sorted(r["projects"].items(), key=lambda x: -(x[1]["main"].get("w", 0) + x[1]["subagents"].get("w", 0))):
        for role, c in (("main", v["main"]), ("subagents", v["subagents"])):
            if not c.get("calls"):
                continue
            p(f"{proj[:32]:32} {role:9} {c['calls']:7} {m(c['in']):>8} {m(c['cr']):>9} {m(c['cw']):>9} {m(c['out']):>8} {m(c['w']):>9} {pct(c['w'], tw):>6}")
    main_w = sum(v["main"].get("w", 0) for v in r["projects"].values())
    sub_w = sum(v["subagents"].get("w", 0) for v in r["projects"].values())
    p(f"all projects: main {pct(main_w, tw)}  subagents {pct(sub_w, tw)}")
    p("")
    p("2. TOP 10 SESSIONS by weighted cost (context = input + cache read + cache creation, main calls)")
    p(f"{'session':9} {'project':24} {'weighted':>9} {'sub%':>5} {'turns':>6} {'calls':>6} {'avg ctx':>8} {'peak ctx':>9} {'compact':>8}")
    for s in r["top_sessions"]:
        p(f"{s['session'][:8]:9} {s['project'][:24]:24} {m(s['weighted']):>9} {100 * s['subagent_share']:4.0f}% {s['turns']:6} {s['main_calls']:6} {k(s['avg_context']):>8} {k(s['peak_context']):>9} {s['compactions']:8}")
    p("")
    p("3. WHAT STARTS A MAIN-SESSION TURN (human includes prompts sent by other tools or channels; subagents shown for scale)")
    p(f"{'start':13} {'turns':>6} {'calls':>7} {'share':>6} {'avg ctx/call':>13} {'calls/turn':>11}")
    for name, v in sorted(r["turn_starts"].items(), key=lambda x: -x[1].get("w", 0)):
        turns = v.get("turns", 0)
        calls = v.get("calls", 0)
        tt = f"{turns:6}" if name != "subagent" else f"{'-':>6}"
        cpt = f"{calls / turns:11.1f}" if turns else f"{'-':>11}"
        p(f"{name:13} {tt} {calls:7} {pct(v.get('w', 0), tw):>6} {k(v.get('ctx', 0) / calls if calls else 0):>13} {cpt}")
    p("")
    w = r["waste"]
    p("4. WASTE SIGNALS")
    p(f"cache rebuilds (cache creation over {REBUILD_THRESHOLD // 1000}k after a file's first call): {w['cache_rebuilds_total']} calls, {m(w['cache_rebuild_tokens_total'])} tokens")
    for s in w["cache_rebuilds_top_sessions"][:5]:
        p(f"  {s['session'][:8]} {s['project'][:24]:24} {s['count']:4} rebuilds {m(s['tokens']):>8}")
    p(f"re-reads (same path Read again, no Edit or Write between): {w['rereads_total']}")
    for s in w["rereads_top_sessions"][:5]:
        files = ", ".join(f"{path} x{n}" for path, n in s["top_files"])
        p(f"  {s['session'][:8]} {s['count']:4}  {files}")
    if w["rereads_top_files"]:
        p("  top files overall:")
        for path, n in w["rereads_top_files"]:
            p(f"    {n:4} {path}")
    p(f"tool_result bytes: {m(w['tool_result_bytes'])} of {m(w['transcript_bytes'])} transcript bytes read ({pct(w['tool_result_bytes'], w['transcript_bytes'])})")
    p("  10 largest tool results:")
    for t in w["largest_tool_results"]:
        p(f"    {k(t['bytes']):>7} {t['tool']:14} {t['session']} {t['path']}")
    comps = w["compactions"]
    if comps:
        avg_pre = sum(c["pre"] for c in comps) / len(comps)
        avg_post = sum(c["post"] for c in comps) / len(comps)
        p(f"compactions: {len(comps)}  avg preTokens {k(avg_pre)}  avg postTokens {k(avg_post)}")
        for c in sorted(comps, key=lambda c: -c["pre"])[:10]:
            p(f"    {c['ts'][:16]} {c['session'][:8]} pre {k(c['pre'])} post {k(c['post'])} {c['ms'] / 1000:.0f}s")
    else:
        p("compactions: 0")
    if args.session:
        p("")
        p("5. TIMELINE (one row per turn; ctx is the peak call in the turn; times are UTC)")
        for sid, rows in r.get("timeline", {}).items():
            p(f"session {sid}")
            p(f"{'time':11} {'start':13} {'calls':>5} {'ctx':>7} {'c.read':>8} {'c.write':>8} {'output':>7}")
            for row in rows:
                if "compaction" in row:
                    c = row["compaction"]
                    p(f"{c['ts'][5:16].replace('T', ' '):11} COMPACTION preTokens {c['pre']} postTokens {c['post']} {c['ms'] / 1000:.0f}s")
                else:
                    p(f"{row['ts'][5:16].replace('T', ' '):11} {row['start']:13} {row['calls']:5} {k(row['ctx']):>7} {k(row['cr']):>8} {k(row['cw']):>8} {k(row['out']):>7}")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="Read-only token and context report over Claude Code transcripts.")
    ap.add_argument("--project", help="substring of the project directory name (default: all)")
    ap.add_argument("--since", help="YYYY-MM-DD")
    ap.add_argument("--until", help="YYYY-MM-DD, inclusive")
    ap.add_argument("--session", help="session id prefix; adds a per-turn timeline")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    for label in ("since", "until"):
        value = getattr(args, label)
        if value:
            try:
                datetime.date.fromisoformat(value)
            except ValueError:
                ap.error(f"--{label} must be YYYY-MM-DD")
    files = discover(args)
    scanned = scan(files, args)
    report = build_report(*scanned, len(files), args)
    if args.json:
        json.dump(report, sys.stdout, indent=1)
        print()
    else:
        print(render_text(report, args))


if __name__ == "__main__":
    main()
