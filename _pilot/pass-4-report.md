# Pass 4 Report — Extractor v2.1.1 + Targeted Updates

**Date:** 2026-05-11
**Output:** `Mishnah-New/English/mishnah_db.json` (rev7, 7.37 MB)
**Extractor:** `_pilot/mishnah_extractor_v2.py` v2.1.1

---

## 1. Extractor Changes (v2.1 → v2.1.1)

### Cell-order fix

**Problem:** Reversed-header tables (269 of 545, with פרק in first cell) produced cells in visual left-to-right order, which is ג→ב→א for Hebrew RTL tables. This reversed the column labels relative to the JSON convention (א at index 0).

**Fix:** `extract_chapter()` now detects header orientation at the top of the function. For reversed-header tables, `cells_data` is reversed after collection, and position indices are reassigned. Standard-header tables are unchanged.

**Verification:** Four known-good chapters tested:
- megillah_1 (standard header): labels MATCH, markers MATCH (50=50)
- keritot_4 (reversed header): labels MATCH — cell order now correct
- yevamot_2 (standard header): labels MATCH, markers MATCH (15=15)
- berakhot_1 (standard header): pre-existing label quirk (unrelated to v2.1.1)

### New alias

Added `"קינים": "kinnim"` to `TRACTATE_NAMES`. The docx spells the tractate with yod (קינים); the extractor previously only had the defective spelling (קנים).

---

## 2. Chapters Updated

| Chapter | Old state | New state |
|---|---|---|
| keritot_3 | shape `[[1,1],[1,1]]`, empty rows (Group B placeholder) | shape `[[2,2],[2,2]]`, 4 cells with A-D subdivisions, full text |
| kinnim_1 | shape `[[1,1,1,1,1],[1,1,1,1]]`, 9 cells (corrupted, duplicates) | shape `[[1,1,1],[1,1,1]]`, 6 cells, 4 with A-B-C subdivisions |

Neither chapter has colored text in the docx (0 markers each). Both have correct structural content with subdivisions.

---

## 3. Validation

| Check | Result |
|---|---|
| JSON parses cleanly | PASS |
| Total chapters | 524 |
| keritot_3 shape correct | PASS (`[[2,2],[2,2]]`) |
| keritot_3 all cells have A-D subs | PASS (16 subdivisions total) |
| kinnim_1 shape correct | PASS (`[[1,1,1],[1,1,1]]`) |
| kinnim_1 no duplicate cells | PASS (labels: 1א,1ב,1ג,2א,2ב,2ג) |
| megillah_1 unchanged | PASS (50 markers) |
| _meta updated | PASS (rev7, extractor 2.1.1) |

---

## 4. _meta

```json
{
  "version": "2026-05-rev7",
  "markers_populated_count": 297,
  "total_chapters": 524,
  "total_markers": 7020,
  "extractor_version": "2.1.1",
  "last_extraction_date": "2026-05-11"
}
```

Marker counts unchanged — neither keritot_3 nor kinnim_1 have styled text in the docx.

---

## 5. Mount Truncation Note

The sandbox mount truncates Python files with Hebrew content above ~12KB. The v2.1.1 extractor (14KB with Hebrew dictionary) cannot run directly from the mount. Workaround: the script is regenerated in /tmp at runtime. The canonical source remains `_pilot/mishnah_extractor_v2.py` (editable via the file tools, which don't have this limitation).

---

## 6. Files Modified

| File | Action |
|---|---|
| `_pilot/mishnah_extractor_v2.py` | Updated to v2.1.1 (cell-order fix + alias) |
| `Mishnah-New/English/mishnah_db.json` | Updated (rev7): keritot_3 and kinnim_1 replaced |
| `_pilot/pass-4-report.md` | Created (this report) |

---

## 7. Remaining Work

The cell-order fix in v2.1.1 corrects extraction for **future** runs. It does not retroactively fix the ~200+ chapters already in the live JSON that were extracted with v2.0/v2.1 from reversed-header tables. However, because those chapters were extracted by the batch process (Pass 3/3.5) which compared against existing JSON entries and accepted matches, the cell order in the live JSON is already correct for all populated chapters — the batch scripts used the JSON's own ordering as ground truth.

The only chapters that needed correction were:
- **keritot_3:** Was a Group B placeholder (empty cells). Now populated from docx.
- **kinnim_1:** Was corrupted (duplicate rows from pre-fix docx). Now clean.

No further retroactive fixes are needed.
