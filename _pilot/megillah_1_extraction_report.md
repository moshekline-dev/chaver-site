# Extraction Report: Megillah Chapter 1 — Pass 2

**Source:** `The Whole  Structured Mishnah for pdf.docx`, Table #168
**Existing JSON:** `Mishnah-New/English/mishnah_db.json` → key `megillah_1`
**Date:** 2026-05-10

---

## 1. Extraction Summary

| Metric | Value |
|---|---|
| Total runs processed | 203 |
| Total markers extracted | 50 (cell level) |
| Cells with subdivisions | 7 of 12 |
| Anomalies (unrecognized styles) | 0 |

**Markers by type:**

| Type | Count | Cells present |
|---|---|---|
| `horizontal1` | 36 | 1א (6), 1ב (30) |
| `internalparallel` | 10 | 3א (2), 3ב (2), 4ב (2), 5א (2), 5ב (2) |
| `horizontal2` | 2 | 2א (1), 2ב (1) |
| `horizontal3` | 2 | 2ב (1), 2ג (1) |
| `vertical1` | 0 | — |
| `closure` | 0 | — |
| `ciasm1` | 0 | — |
| `ciasm2` | 0 | — |

Four of the eight marker types are unused in this chapter (consistent with Pass 1 findings).

---

## 2. Comparison with Existing JSON

### Metadata fields — all exact match

`tractate_he`, `tractate_en`, `seder_he`, `seder_en`, `chapter_num`, `chapter_he`, `source_url`, `shape` — all identical between existing and extracted.

### Structure — exact match

Both have 5 rows with cell counts [2, 3, 2, 3, 2], matching the shape `[[2,2], [1,2,1], [2,2], [1,2,1], [2,2]]`.

### Labels — all 12 match

Every cell label (1א through 5ב) is identical in both.

### Positions — all match (after fix)

The initial extraction used cell-index column numbering (1, 2, 3) instead of grid-column numbering (accounting for colspans). This was corrected: in a `[2,2]` row, the second cell starts at grid column 3 because the first cell spans columns 1–2. All 12 positions now match.

### Text — minor differences in all 12 cells

Every cell has the same textual content, but with two systematic differences:

1. **Missing inter-run spaces.** The docx stores each phrase as a separate run with no whitespace between runs. The existing JSON has spaces inserted between phrases. This affects all 12 cells. Example from 1א: existing has `מגלה נקראת באחד עשר` while extracted has `מגלה נקראתבאחד עשר`.

2. **Mishnah numbers included.** The extracted text includes the Hebrew mishnah numbers (e.g., `(א)`, `(ב)`) that are in the docx runs. The existing JSON strips these.

Both differences are cosmetic and systematic — they can be handled by a post-processing step. The underlying textual content is identical.

One cell (2ב) has an apparent discrepancy where the existing starts with `אף` while the extracted text appears to start with `ף`. This is a false positive in the comparison: the cell label `2ב` ends with ב, and the next run starts with `אף`. When the label is stripped by regex, the match pattern `2בא` incorrectly consumed the first letter of `אף`. The actual content is identical.

### Markers — new (existing was all zero)

The existing JSON has zero markers in every cell. The extracted JSON now has 50 markers distributed across 10 of 12 cells (cells 4א and 4ג have no markers in the source document).

### Subdivisions — match

| Cell | Existing | Extracted | Labels match? |
|---|---|---|---|
| 2א | 2 subdivisions (A, B) | 2 subdivisions (A, B) | Yes |
| 2ג | 2 subdivisions (A, B) | 2 subdivisions (A, B) | Yes |
| 3א | 2 subdivisions (A, B) | 2 subdivisions (A, B) | Yes |
| 3ב | 2 subdivisions (A, B) | 2 subdivisions (A, B) | Yes |
| 4ב | 2 subdivisions (A, B) | 2 subdivisions (A, B) | Yes |
| 5א | 2 subdivisions (A, B) | 2 subdivisions (A, B) | Yes |
| 5ב | 2 subdivisions (A, B) | 2 subdivisions (A, B) | Yes |

All 7 subdivided cells match. No cell gained or lost subdivisions.

---

## 3. Per-Cell Marker Listings

### Row 1

**Cell 1א** (6 markers — all `horizontal1`):
`כרכין`, `המקפין`, `חומה`, `כפרים`, `ועירות`, `גדולות`

**Cell 1ב** (30 markers — all `horizontal1`):
Repeating pattern of `כפרים`, `ועירות`, `גדולות`, `ומקפות`, `חומה` — 6 cycles, marking the same five-term list that recurs across the six different day-of-reading scenarios in mishnah 1ב.

### Row 2

**Cell 2א** (1 marker):
`horizontal2`: `אמרו מקדימין ולא מאחרין` (in subdivision B)

**Cell 2ב** (2 markers):
`horizontal2`: `שאמרו מקדימין ולא מאחרין`
`horizontal3`: `ומתנות לאביונים`

**Cell 2ג** (1 marker):
`horizontal3`: `ומתנות לאביונים` (in subdivision B)

### Row 3

**Cell 3א** (2 markers — `internalparallel`):
Subdivision A: `לשבת` / Subdivision B: `שבת`

**Cell 3ב** (2 markers — `internalparallel`):
Subdivision A: `המדר` / Subdivision B: `נדרים`

### Row 4

**Cell 4א** — no markers
**Cell 4ב** (2 markers — `internalparallel`):
Subdivision A: `מצרע` / Subdivision B: `טהור`

**Cell 4ג** — no markers

### Row 5

**Cell 5א** (2 markers — `internalparallel`):
Subdivision A: `כהן` / Subdivision B: `כהן`

**Cell 5ב** (2 markers — `internalparallel`):
Subdivision A: `במה` / Subdivision B: `שילה`

---

## 4. Anomalies

**None.** All 203 runs had either no character style, a `Subunit` style (labels/subdivisions), or one of the four marker styles. No unknown styles were encountered.

**Note on `mishnah_db.json` file integrity:** The local copy has null-byte corruption after byte 3,541,936 (same pattern seen previously in `_redirects`). The JSON was parsed by reading only up to the first top-level closing brace. The content portion is intact.

---

## 5. Sample Markers by Type

### `horizontal1` (blue, #3399FF) — 36 runs

| Cell | Text |
|---|---|
| 1א | כרכין |
| 1א | המקפין |
| 1א | חומה |

These mark the repeated five-term list (כרכין / המקפין חומה / כפרים / ועירות גדולות / ומקפות חומה) that defines the reading-day categories. The terms repeat identically across 1א and 1ב.

### `horizontal2` (teal, #008080) — 2 runs

| Cell | Text |
|---|---|
| 2א (sub B) | אמרו מקדימין ולא מאחרין |
| 2ב | שאמרו מקדימין ולא מאחרין |

Horizontal parallel connecting 2א and 2ב: the rule about advancing (not delaying) Megillah reading.

### `horizontal3` (dark cyan, #008B8B) — 2 runs

| Cell | Text |
|---|---|
| 2ב | ומתנות לאביונים |
| 2ג (sub B) | ומתנות לאביונים |

Horizontal parallel connecting 2ב and 2ג: gifts to the poor.

### `internalparallel` (dark red, #C00000) — 10 runs

| Cell | Text |
|---|---|
| 3א sub A / sub B | לשבת / שבת |
| 3ב sub A / sub B | המדר / נדרים |
| 4ב sub A / sub B | מצרע / טהור |

Internal parallels connecting the A and B subdivisions within a cell — the "אין בין... ל..." (what's the difference between X and Y) pattern that runs through rows 3–5.

---

## Files Created

- `_pilot/megillah_1_extracted.json` — the candidate chapter entry (40 KB)
- `_pilot/megillah_1_extraction_report.md` — this report

---

## Known Issues for Pass 3

1. **Inter-run spaces.** The docx runs don't include inter-word spaces. A post-processing step should insert spaces at run boundaries where the previous run doesn't end with a space and the next doesn't start with one. (Hebrew is space-delimited, so this is straightforward.)

2. **Mishnah numbers in text.** The docx includes `(א)`, `(ב)`, etc. at the start of each mishnah. The existing JSON strips these. The extraction should either strip them or preserve them with a flag.

3. **Marker duplication.** Markers appear at both cell level and subdivision level for subdivided cells. This is intentional (cell-level gives a quick overview; subdivision-level shows placement), but the JSON consumer needs to know not to double-count.

4. **No `html` field.** The extracted JSON omits the `html` field. A renderer will generate HTML with `<span class="horizontal1">` etc. in a later step.
