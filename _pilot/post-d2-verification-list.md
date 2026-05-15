# Post-D-2 Manual Verification List

Chapters that need manual visual comparison against their legacy/existing site pages after the D-2 bulk render is complete. These could not be fully verified programmatically (either no existing page to diff against, slightly lower content ratio than expected, or known data anomalies).

## No existing page on site (cannot diff — these are new renders)

1. `bavametzia_2`
2. `beitzah_5`
3. `middot_5`
4. `shevuot_6`
5. `shevuot_8`
6. `makkot_1` — existing page has trailing space in filename; may need rename + redirect

## Lower content ratio (92–93% vs source — may be fine but worth checking)

1. `meilah_1` (93%)
2. `sanhedrin_7` (92%)

## All Avot chapters (non-standard structures, word labels, 4–5 cell rows)

1. `avot_1`
2. `avot_2`
3. `avot_3`
4. `avot_5`

Note: `avot_4` was repaired on 2026-05-14 (see `_pilot/cowork-diary.md` entry "avot_4 repair") — JSON went from 5 rows to 8 rows, missing rows 6/7/8 + row 5 B subdivisions extracted from the legacy HTML.

## Chapters with special label types

Chapters using Hebrew word labels (not the standard `Nא`/`Nב`/`Nג` Hebrew-letter labels) or non-standard row labeling:

1. `gittin_3` — labels: `נפש`, `עולם`, `שנה`
2. `ketubot_2` — labels: `אשה`, `עדות עצמית`, `עדות`
3. `chagigah_2` — empty labels with thematic Hebrew words as content
4. `eduyot_7` — empty labels, rows labeled `B` / `C` / `D` / `E`

The renderer's `normalize_label()` function preserves Hebrew word labels as-is (no Hebrew→Latin conversion for multi-character words), but visual confirmation is needed because these are the cases most likely to surface label-handling edge cases.

## Verification procedure

For each chapter above, after the D-2 bulk render lands on Cloudflare:

1. Open both URLs side by side in incognito tabs:
   - Live rendered URL: `https://chaver.com/Mishnah-New/Hebrew/Text/[Seder]/[Tractate]/[chapter file].htm`
   - Reference (if exists): the legacy page or the printed Mishnah text
2. Compare:
   - Cell labels match expected (Latin column letters, Hebrew word labels intact)
   - All mishnayot present (count `(X)` references)
   - Marker spans render with correct colors
   - 3-column rows: headers fit on one line (the v5-alt fix)
   - Subdivisions align across columns where applicable
3. If divergence found → log into `_pilot/cowork-diary.md` and decide whether to:
   - Patch JSON (data issue)
   - Patch renderer (logic issue)
   - Patch main.css (style issue)

## Source for this list

Drafted from the D-1 v5-alt task spec on 2026-05-14 (when the canonical render became `d1_v5alt_render.py`). The list anticipates D-2 bulk rendering of all 525 chapters using that script.
