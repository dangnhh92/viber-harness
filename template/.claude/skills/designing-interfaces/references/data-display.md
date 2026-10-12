# Data display rules

Load when a screen shows numbers, charts, tables, KPIs, status or alerts: admin consoles, dashboards, reports, in-app stats.
This file decides what to show and how it reads. If a charting skill with its own palette validator is installed, it owns chart marks and colour.
Values marked `[default]` have no published source; a project may override them.

## Contents
- Source keys
- 1. Does it earn a place (D1 to D9)
- 2. Aggregation honesty (G1 to G6)
- 3. Layout and levels (L1 to L5)
- 4. Colour and alerting (H1 to H12)
- 5. Chart choice by question (C1 to C8)
- 6. Numbers and labels (N1 to N8)
- 7. Accessibility for data (A1 to A3)

## Source keys

- **FEW-IDD**: Stephen Few, Information Dashboard Design, 2nd ed. 2013, ch. 3 "Thirteen common mistakes". Read via summaries, not the book.
- **FEW-BG**: Stephen Few, Bullet Graph Design Specification, perceptualedge.com. Read via summaries.
- **TUFTE**: Edward Tufte, The Visual Display of Quantitative Information, 2nd ed. 2001, ch. 2 (graphical integrity, lie factor), ch. 4 (data-ink). Read via summaries.
- **COWAN**: Nelson Cowan, "The magical number 4 in short-term memory", Behavioral and Brain Sciences 24(1), 2001.
- **CM84**: Cleveland and McGill, "Graphical Perception", JASA 79(387), 1984.
- **IBCS**: International Business Communication Standards, ibcs.com, CC BY-SA 4.0 (now ISO 24896). Read via IBCS FAQ and working-group notes.
- **HPHMI**: Hollifield et al., The High Performance HMI Handbook (PAS), and ISA-101.01 as summarised by ISA and trade press. Standard text not read.
- **ALARM**: ISA-18.2 / IEC 62682 and EEMUA 191 figures, via exida, Emerson and ABB summaries. Standard text not read.
- **NUREG**: NUREG-0700 Rev. 2 (2002), Human-System Interface Design Review Guidelines, US NRC, public domain. Read in full text; guideline numbers below are Rev. 2. Rev. 3 (2020) is current and may renumber.
- **ISO**: ISO 9241-110:2020 (interaction principles), 9241-112 (presentation of information; 2017, new edition 2025). Paywalled; principle names from secondary sources.
- **WCAG**: WCAG 2.2, W3C Recommendation.

## 1. Does it earn a place (decide before layout)

- **D1** Each panel's title or subtitle names the question it answers ("Are refunds rising?", not "Refunds"). A reviewer can read the question off the screen. (FEW-IDD mistake "choosing inappropriate measures"; ISO 9241-110 suitability for the user's tasks)
- **D2** For each metric, someone can name the action taken when it is high and when it is low. A metric with no action is removed or moved to a detail level. (FEW-IDD; HPHMI "information is data in context made useful")
- **D3** Every headline number sits next to a comparison: target, previous period, or normal range, with the basis named ("vs last 7 days"). A bare number fails. (FEW-IDD mistake "inadequate context"; HPHMI "where am I compared with where I should be")
- **D4** Every number shows its unit, in the value or in its column or axis header. (NUREG 1.2.2-4, 1.3.6-6)
- **D5** Every panel shows the period it covers and when the data was last refreshed, as an absolute time with timezone ("Updated 14:05 UTC"). (NUREG 1.4-7 time delay)
- **D6** Data older than twice its expected refresh interval shows a visible stale marker (icon plus text, e.g. "Stale: last update 3 h ago"), and the number greys out. `[default]` (NUREG 1.4-9, 1.4-10: invalid and unvalidated data must be indicated)
- **D7** Missing data reads "No data" (or the source's error), never `0`. A real zero shows `0`. (NUREG 1.4-9)
- **D8** Manually entered or overridden values are marked distinct from measured or imported values. (NUREG 1.4-11)
- **D9** Forecast, plan and projected values look different from actuals: actual solid, plan outlined, forecast hatched or dashed, previous period grey. (IBCS notation; NUREG 1.2.5-11)

## 2. Aggregation honesty

- **G1** A percentage or rate shows its base on the same screen or on hover ("12% of 340 orders"). (TUFTE graphical integrity: clear labelling to defeat distortion)
- **G2** An average shows n, and states mean or median. Skewed money or duration data defaults to median. `[default]` (TUFTE graphical integrity)
- **G3** Money compared across more than 12 months states nominal or inflation-adjusted. `[default]` (TUFTE: deflated and standardised units are nearly always better for money over time)
- **G4** Values in different units or currencies are never summed or stacked together. (NUREG 1.3.6-13, 1.3.6-14: one scale per axis, index to a common base)
- **G5** A partial current period (this week so far) is labelled partial or excluded from trend comparisons against full periods. `[default]` (TUFTE: do not quote data out of context)
- **G6** Totals equal the sum of the rows shown, or the gap is labelled ("Other", "Filtered out"). `[default]`

## 3. Layout and levels

- **L1** The at-a-glance set fits one viewport (1440x900 desktop, 390x844 phone) without scrolling. `[default]` (FEW-IDD mistake "exceeding the boundaries of a single screen")
- **L2** Every screen belongs to one level and says so in its structure: Level 1 overview (status only, no controls), Level 2 working view (normal work happens here), Level 3 detail of one entity, Level 4 diagnostics (raw logs, events). Normal operation needs no visit below Level 2. (HPHMI, ISA-101 display hierarchy)
- **L3** The most important metric sits top-left (top for a phone). The same metric holds the same position on every screen that shows it. (FEW-IDD mistake "arranging the data poorly"; NUREG 4.2.7.1-7 consistent ordering)
- **L4** Status that needs no action (a sync finished, a job ran) is not shown in the alert list. (NUREG 4.1.2-5)
- **L5** The overview leads with at most 4 headline numbers; everything else sits below or a level down. `[default]` (COWAN: working memory of about 4 chunks; this cap is tighter than Few, who allows a full single screen, so a project may raise it)

## 4. Colour and alerting (high-performance HMI)

- **H1** In normal state the data area is neutral: no red, amber or saturated colour anywhere a value is shown. Colour appears when something needs attention. (HPHMI, ISA-101 grey base; NUREG 4.1.1-4 darkboard)
- **H2** Alert colours (red, amber, and any status hue) are used for nothing else: not for brand, buttons, links, chart series or decoration. (HPHMI "alarm colors should never be used for anything else"; NUREG 1.3.8-8)
- **H3** Every alert state is coded twice: colour plus shape or icon plus text. (NUREG 4.2.6.2-2; HPHMI redundant coding; WCAG 1.4.1)
- **H4** At most 3 alert priorities. Of alerts actually shown over a month, high priority is 5% or less; medium about 15%; low about 80%. More high-priority alerts than that means priorities are wrong, not that the product is in crisis. (ALARM: EEMUA 191 distribution)
- **H5** In steady state an operator gets at most 1 new actionable alert per 10 minutes. More than 10 in 10 minutes is a flood: the UI groups them by cause and shows the count. (ALARM: ISA-18.2 flood definition, EEMUA 191 rate)
- **H6** Unacknowledged, acknowledged and cleared alerts each look different. (NUREG 4.2.3-1, 4.2.3-4)
- **H7** Each alert line shows source, priority, current value, the limit it crossed, and the action or a link to it. (NUREG 4.2.5-4 to 4.2.5-8)
- **H8** Alert lists sort by priority, then time, newest first within a priority. (NUREG 4.2.7.2-1)
- **H9** Flashing only for an unacknowledged urgent alert. The marker beside the text flashes, never the text. One flash rate, 2 to 3 Hz, stopping on acknowledge, on an area small enough to stay under the WCAG flash threshold. (NUREG 1.3.10-9, 1.3.10-10, 1.3.10-12, 1.3.10-13; WCAG 2.2 SC 2.3.1)
- **H10** A key live value is drawn against its normal range (a range bar or bullet graph with the normal band and the limit), not as a bare number. (HPHMI moving analog indicator; FEW-BG)
- **H11** A key live value has its recent trend next to it (sparkline of the last window, window stated). (HPHMI embedded trends)
- **H12** A value people must read updates at most once per second. An update never shifts layout (tabular numerals, fixed width). (NUREG 1.4-3; Vercel WIG tabular-nums)

## 5. Chart choice by question

| The reader asks | Use | Not |
|---|---|---|
| How much now, against target? | number + delta + target, or bullet graph | gauge, dial, donut |
| How did it change over time? | line, time on the horizontal axis, left to right | bars for more than 12 periods `[default]` |
| Which is biggest? | horizontal bar, sorted | pie, unsorted bars |
| What makes up the total? | stacked bar, 6 parts or fewer | pie with more than 3 slices `[default]` |
| How far from plan or last year? | diverging bar with zero in the centre | two separate bars to compare by eye |
| How are values spread, any outliers? | histogram, dot plot, box plot | average alone |
| Do two measures move together? | scatter | dual-axis line |
| Same metric across many entities? | small multiples, shared scale | one chart with 9+ series |
| What is the exact value? | table | chart with labels on every point |

Sources: FEW-IDD (gauges, "inappropriate display media"); FEW-BG; IBCS (time horizontal, structure vertical, variance charts); NUREG 1.2.4-6 (zero centred on deviation bars); TUFTE (small multiples).

- **C1** Bars and areas start at zero. A line axis that does not start at zero says so on the axis. (NUREG 1.3.6-11; TUFTE lie factor)
- **C2** One scale per axis. No dual axis. Two measures of different units become two charts or an index to a common base. (NUREG 1.3.6-13, 1.3.6-14)
- **C3** Lie factor between 0.95 and 1.05: the visual change is proportional to the data change. Area or radius encoding a linear value fails. (TUFTE; the 0.95 to 1.05 band is a later convention, not Tufte's wording)
- **C4** The comparison that matters is encoded by position on a common scale or by length, not by angle, area or colour. (CM84 accuracy ranking: position, length, angle, area, colour)
- **C5** Charts meant to be compared share the same scale. (NUREG 1.3.6-11; TUFTE small multiples)
- **C6** No 3D, no shadow, no decoration on marks; gridlines lighter than data. (TUFTE data-ink; FEW-IDD "useless decoration")
- **C7** At most 9 tick marks between labelled numbers. (NUREG 1.3.6-2)
- **C8** Every series colour reaches 3:1 against the chart background, in light and dark, and adjacent series are distinguishable without colour vision (A3). (WCAG 2.2 SC 1.4.11)

## 6. Numbers and labels

- **N1** Number columns right-align, or align on the decimal point. (NUREG 1.2.2-10)
- **N2** Precision is what the decision needs, and constant within a column. KPI tiles show 3 significant digits or fewer unless an exact amount is the point (money owed, stock count). `[default]` (NUREG 1.3.5-3; FEW-IDD "excessive detail or precision")
- **N3** Decimals below 1 keep the leading zero (0.43); whole numbers have no leading zeros (28, not 0028). (NUREG 1.3.5-2)
- **N4** Abbreviated units (K, M, B, or the locale's equivalents) are the same within one view; the full value is on hover or tap. `[default]` (IBCS "Unify")
- **N5** A delta shows sign, unit and basis: "+12% vs last week". Its colour follows good or bad for that metric, not the sign (costs up is bad). (IBCS variance notation)
- **N6** One locale per screen for separators and dates; the admin's locale, not the server's. (Vercel WIG, Locale and i18n)
- **N7** Labels are plain words. No internal field names, enum keys or codes (`order_status_3`). Abbreviations are defined on the screen or avoided. (NUREG 1.3.2-1, 1.2.1-7; ISO 9241-110 self-descriptiveness)
- **N8** Relative times ("5 min ago") show the absolute time on hover or tap. `[default]`

## 7. Accessibility for data

- **A1** Text and numbers 4.5:1; chart marks, gridlines that carry meaning, and range bands 3:1 against their background. (WCAG 2.2 SC 1.4.3, 1.4.11)
- **A2** Every chart has a table view or an accessible text equivalent of the values. (WCAG 2.2 SC 1.1.1)
- **A3** Series identity never relies on colour alone: legend plus direct labels, or texture. (WCAG 2.2 SC 1.4.1)
