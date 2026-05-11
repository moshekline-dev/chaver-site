# Cell-Order Spot-Check Report

**Date:** 2026-05-11
**Purpose:** Verify whether reversed-header chapters in the live JSON have correct cell order after Pass 4's extractor fix.

---

## 1. Candidate Identification

### Cross-referencing three sets:

| Set | Count |
|---|---|
| Reversed-header tables in docx | 266 |
| Chapters with markers in live JSON | 297 |
| **Intersection** (reversed-header + markers) | **43** |

### Key finding: population source

All 43 candidates are from the **original 148** chapters (pre-Pass 3). They have `html` format cells, not the `text/runs` format produced by Pass 3/3.5.

**Zero** Pass 3/3.5-populated chapters have both reversed headers AND markers. The reason: Pass 3/3.5 recovered chapters primarily in Kodashim and Toharot, where the docx tables have structure but no colored text (0 markers).

---

## 2. Label-Order Check

Scanned all 266 reversed-header chapters in the live JSON for descending label order (the signature of the cell-order bug):

| Category | Count | Notes |
|---|---|---|
| Correct order (ascending: א→ב→ג) | 224 | No issue |
| **Reversed order (descending: ג→ב→א)** | **15** | Bug confirmed |
| No multi-cell rows / no Hebrew labels | 27 | Cannot determine |

### The 15 affected chapters:

| Chapter | Markers | Row 1 labels | Shape decision |
|---|---|---|---|
| sanhedrin_2 | 21 | [1ג, 1ב, 1א] | — |
| sanhedrin_3 | 25 | [1ג, 1ב, 1א] | — |
| sanhedrin_4 | 15 | [1ג, 1ב, 1א] | — |
| sanhedrin_5 | 34 | [1ג, 1ב, 1א] | — |
| sanhedrin_9 | 33 | [1ג, 1ב, 1א] | — |
| sanhedrin_10 | 3 | [1ג, 1ב, 1א] | — |
| shevuot_1 | 40 | [2ב, 2א] (Row 2) | — |
| kelim_4 | 0 | [1ב, 1א] | docx_current |
| makkot_2 | 0 | [1, 1ג, 1ב, 1א] | title_row_pattern |
| makkot_3 | 0 | [1, 1ג, 1ב, 1א] | title_row_pattern |
| sanhedrin_1 | 0 | [1ג, 1ב, 1א] | title_row_pattern |
| sanhedrin_6 | 0 | [1, 1ג, 1ב, 1א] | json_current |
| sanhedrin_7 | 0 | [1, 1ג, 1ב, 1א] | title_row_pattern |
| sanhedrin_11 | 0 | [1, 1ב, 1א] | title_row_pattern |
| tahorot_1 | 0 | [1ג, 1ב, 1א] | docx_current_with_header |

**With markers (need correction):** 7 chapters (171 markers total)
**Without markers (structural only):** 8 chapters

---

## 3. Spot-Check: Text-Content Verification

For 5 chapters from the top-10 list, extracted with v2.1.1 and compared cell text order against the live JSON:

### eduyot_4 (141 markers) — CORRECT ORDER
- v2.1.1 and JSON produce same text in same positions
- Row 1: "אלו דברים מקלי בית שמאי" in C1 in both
- Labels differ (v2.1.1 detects '1' not '1א') but content matches

### eduyot_3 (81 markers) — CORRECT ORDER
- Same text order in corresponding rows
- Row 2 has structural differences (different row grouping) but not reversed

### shevuot_4 (71 markers) — CORRECT ORDER
- All 5 rows match text order between JSON and v2.1.1

### eduyot_1 (55 markers) — CORRECT ORDER
- Rows 1-3 perfect text match; Row 4 has grouping difference

### avodazara_5 (75 markers) — CORRECT ORDER (different row count)
- JSON has 5 rows, v2.1.1 has 7 (structural interpretation differs)
- Where rows align, text order is consistent

**All 5 spot-checked chapters have correct cell order.** The high-marker chapters are fine.

---

## 4. Root Cause Analysis

The 15 reversed-label chapters share a pattern:

1. All are from the **original 148** (populated before Pass 3)
2. All are from **Sanhedrin** (10), **Makkot** (2), **Shevuot** (1), **Kelim** (1), **Tahorot** (1) — all Nezikin/Toharot sedarim
3. The original extraction (v1.0/v2.0) produced these entries with reversed labels
4. Pass 3/3.5 **preserved** these entries unchanged (they were in the "skip" list)

The 43 reversed-header chapters that DO have correct order (like eduyot_4, shevuot_4) were also from the original 148 but were apparently extracted correctly at that time. The difference may be:
- Different extraction logic in the original pass
- Manual correction at some point
- These 15 chapters may have been extracted separately or by a different code path

---

## 5. Verdict

### Pass 4's claim is PARTIALLY correct:

> "No retroactive fixes are needed [for Pass 3/3.5 chapters]"

**TRUE** — zero Pass 3/3.5 chapters have the cell-order bug.

But the claim missed a separate issue: **15 chapters from the original 148 have reversed cell labels**, of which **7 have markers** (171 markers positioned in reversed cells).

### Impact assessment:

For the 7 chapters with markers (sanhedrin_2-5, 9, 10; shevuot_1):
- Cell labels are reversed (1ג before 1א)
- Marker text content is correct (markers are within the cell text regardless of order)
- The HTML renderer reads markers from within each cell — so the site currently displays correctly within each cell
- But the label ordering means the structural position metadata is wrong: a marker labeled as being in column ג is actually in column א's position

**Risk:** Low for current site display (markers render within their cell). Higher if any future tool uses label/position metadata to determine column placement.

---

## 6. Recommendation

**Fix the 7 chapters with markers** by reversing their cell arrays and reassigning position indices. This is a mechanical operation — no re-extraction needed, just reverse each row's `cells` array and update the `position.col` values.

**Defer the 8 chapters without markers** — they have reversed labels but no marker content that could be mispositioned. They can be corrected during a future full re-extraction.

**Estimated effort:** A simple script, ~5 minutes of work. Should be a separate task with Moshe's approval.

---

## Files

| File | Action |
|---|---|
| `_pilot/cell-order-spot-check.md` | Created (this report) |
