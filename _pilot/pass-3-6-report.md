# Pass 3.6 Report — Shape Decision Application

**Date:** 2026-05-10
**Output:** `_pilot/mishnah_db_staged.json` (rev6, 7.34 MB)
**Extractor:** v2.1 (unchanged)

---

## 1. Group A — Docx Current, Re-extracted (4 chapters)

| Chapter | Old shape | New shape | Markers | Breakdown |
|---|---|---|---|---|
| kelim_4 | [3, 3] | [2, 2] | 0 | No styled text in docx |
| yevamot_2 | [3, 3] | [2, 2, 2, 2, 2] | 15 | horizontal1: 15 |
| ketubot_11 | [1, 2, 1, 2, 1] | [1, 2, 1] | 44 | internalparallel: 42, closure: 2 |
| ketubot_12 | [1, 2, 1] | [3, 3] | 7 | horizontal1: 7 |

All 4 chapters successfully extracted using docx structure. `kelim_4` has correct structure but no colored text yet (Toharot seder, analysis incomplete).

---

## 2. Group B — Subdivision Chapters (2 chapters)

| Chapter | Old shape | New shape | Status |
|---|---|---|---|
| eduyot_7 | [3, 3] | [2, 2] | Shape updated only |
| keritot_3 | [2, 2] | [2, 2] | Shape updated only |

**Result:** Both chapters' docx tables have structures that don't match Moshe's target:

- **eduyot_7:** Docx has `[2, 2, 2, 2, 2, 2]` (6 rows × 2 cells). Target is `[2, 2]` with A-E subdivisions per cell. The docx hasn't been reformatted to reflect the new analysis.
- **keritot_3:** Docx has `[2, 2, 3, 3, 3]` (5 rows). Target is `[2, 2]` with A-D subdivisions. Same situation — docx not yet updated.

For both: JSON `shape` field updated to target. Rows/cells left empty. Markers will populate after the docx is reformatted.

---

## 3. Group C — tahorot_1 with Header Property

| Field | Value |
|---|---|
| Old shape | [3, 4, 3] |
| New shape | [3, 3, 3] |
| Docx shape | [3, 1, 3, 3] |
| Header text | `(ה) האכל שנטמא באב הטמאה ושנטמא בולד הטמאה מצטרפין זה עם זה לטמא כקל שבשניהן כיצד` |
| Markers | 0 (no styled text in docx) |

**New schema element:** Row 2 of `tahorot_1` now has a `header` field:

```json
{
  "row_num": 2,
  "header": "(ה) האכל שנטמא באב הטמאה...",
  "cells": [...]
}
```

The docx's full-width middle row (the single cell in position 2 of the `[3, 1, 3, 3]` structure) becomes a row-level header property. The remaining 3 data rows of the docx map to the JSON's 3 rows of 3 cells.

---

## 4. Groups D + E + F — Documented, Left Empty (20 chapters)

### Group D — JSON Current (1 chapter)

| Chapter | JSON shape | Docx shape | Reason |
|---|---|---|---|
| sanhedrin_6 | [4, 3, 3, 3] | [3, 3, 3, 3] | JSON has correct first-row cell count; docx needs revision |

### Group E — Title-Row Pattern (17 chapters)

These chapters have docx tables with an extra full-width "title" row at the top. Moshe's decision: the JSON view (folding title into row 1) is current; docx view is outdated.

| Tractate | Chapters |
|---|---|
| Avot | avot_2 |
| Bekhorot | bekhorot_8 |
| Makkot | makkot_1, makkot_2, makkot_3 |
| Meilah | meilah_1 |
| Niddah | niddah_3 |
| Sanhedrin | sanhedrin_1, sanhedrin_7, sanhedrin_11 |
| Shevuot | shevuot_3, shevuot_6, shevuot_8 |
| Temurah | temurah_7 |
| Yadayim | yadayim_3 |
| Zevachim | zevachim_5, zevachim_6 |

### Group F — Extractor Can't Match (2 chapters)

| Chapter | Reason |
|---|---|
| keritot_4 | v2.1 strict header matching fails; Jaccard fuzzy matching previously found it |
| kinnim_1 | Same |

All 20 chapters documented in `_meta.shape_review_decisions` with decision reasons.

---

## 5. Validation Results

| Check | Result |
|---|---|
| JSON parses cleanly | PASS |
| Total keys (524 + _meta) | PASS |
| Originally-populated chapters unchanged | PASS (all changes accounted for by pass 3.5 normalization + pass 3.6 Group A/B/C) |
| Groups A+B+C updated | PASS (3 with markers, 4 shape-only) |
| Groups D+E+F empty | PASS (all 20 empty) |
| shape_review_decisions | PASS (27 entries) |
| No invalid marker types | PASS |

---

## 6. Final Marker Totals

| Type | Count | Change vs Pass 3.5 |
|---|---|---|
| horizontal1 | 3,439 | +22 |
| internalparallel | 1,793 | +42 |
| vertical1 | 869 | — |
| horizontal2 | 364 | — |
| horizontal3 | 340 | — |
| closure | 140 | +2 |
| ciasm1 | 40 | — |
| ciasm2 | 35 | — |
| **Total** | **7,020** | **+66** |

The 66 new markers come from: yevamot_2 (15), ketubot_11 (44), ketubot_12 (7).

---

## 7. Final Staged JSON State

| Category | Count |
|---|---|
| Chapters with markers | 297 |
| Chapters without markers | 227 |
| **Total** | **524** |

### Breakdown of 227 chapters without markers

| Reason | Count |
|---|---|
| No styled text in docx (analysis not done) | ~200 |
| Shape decision: title-row pattern (Group E) | 17 |
| Shape decision: JSON current (Group D) | 1 |
| Shape decision: extractor can't match (Group F) | 2 |
| Shape decision: docx not ready for subdivisions (Group B) | 2 |
| Shape decision: re-extracted but no styled text (kelim_4, tahorot_1) | 2 |
| Genuinely absent from docx (ketubot_14, yadayim_4) | 2 |

---

## 8. Anomalies

1. **eduyot_7 and keritot_3:** Docx structure doesn't match Moshe's target. These chapters await docx reformatting before markers can be extracted. Shape field updated but rows remain empty.

2. **kelim_4 and tahorot_1:** Successfully re-extracted with correct shapes, but yield 0 markers because the docx tables have no colored/styled text. The structural cells are populated but all `markers: []` arrays are empty.

3. **Pass 3.5 report said "6 new shape mismatches" but actual count is 7.** The 7th (one of the zevachim chapters) was miscounted in the earlier session. All 7 are now documented in shape-review.md and in `_meta.shape_review_decisions`.

4. **tahorot_1 header property** is the first use of a row-level `header` field in the schema. Future consumers of `mishnah_db.json` should check for this field. It currently applies only to this one chapter.

---

## 9. Comparison: Pass 3.5 → Pass 3.6

| Metric | Pass 3.5 | Pass 3.6 | Change |
|---|---|---|---|
| Version | rev5 | rev6 | — |
| Chapters with markers | 294 | 297 | +3 |
| Total markers | 6,954 | 7,020 | +66 |
| Shape mismatches documented | 0 | 27 | +27 |
| File size | 7.25 MB | 7.34 MB | +0.09 MB |

---

## Files Modified

| File | Action |
|---|---|
| `_pilot/mishnah_db_staged.json` | Updated (rev6) |
| `_pilot/pass-3-6-report.md` | Created (this report) |

**Status:** Ready for Moshe's review before promotion to live.
