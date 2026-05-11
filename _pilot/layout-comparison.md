# Layout Comparison — keritot_3, keritot_4, keritot_5, kinnim_1

**Date:** 2026-05-11
**Source docx:** The Whole Structured Mishnah for pdf.docx (uploaded, 545 tables)
**Source JSON:** Mishnah-New/English/mishnah_db.json (rev6)

---

## keritot_3

### Shape

- **JSON (live):** `[[1,1], [1,1]]` — 2×2 (Group B target shape, updated in Pass 3.6)
- **Docx (current):** `[[2,2], [2,2]]` — 2×2 (each cell colspan 2)
- **Cells/row match:** YES (both `[2, 2]`)

### Subdivisions

- **JSON:** 16 subdivisions (4 per cell × 4 cells) — all empty (shape-only update in Pass 3.6)
- **Docx:** 16 subdivisions (A, B, C, D in each of 4 cells) — **with text content**
- **Group B target fulfilled:** YES — the docx now has the A-D subdivisions Moshe planned

### Cells

| Position | JSON label | JSON text (first 50c) | Docx label | Docx text (first 50c) |
|---|---|---|---|---|
| R1C1 | 1א | (empty) | 1ב | אכל חלב וחלב בהעלם אחד אינו חיב אלא חטאת אחת |
| R1C2 | 1ב | (empty) | 1א | אמרו לו אכלת חלב מביא חטאת |
| R2C1 | 2א | (empty) | 2ב | אמר רבי עקיבא שאלתי את רבן גמליאל |
| R2C2 | 2ב | (empty) | 2א | יש אוכל אכילה אחת וחיב עליה ארבע חטאות |

Note: Column ordering is reversed (RTL). JSON has 1א in C1 position; docx has 1ב in C1 position. This is the RTL column-order convention: the extractor reads cells left-to-right in the docx, but the Hebrew table's visual right-to-left means column B (ב) appears first in extraction order.

### Markers

- **JSON:** 0 markers
- **Docx:** 0 markers (no styled text in either)

### Decision needed

**Docx is ready for full population.** The docx now has the 2×2 shape with A-D subdivisions that was the Group B target. The JSON entry should be replaced with the docx extraction. The only consideration: cell ordering (RTL) — the extractor produces cells in left-to-right document order, which reverses the Hebrew column labels. This is consistent with how all other chapters are stored.

---

## keritot_4

### Shape

- **JSON (live):** `[[1,1,1], [1,1,1]]` — 2×3
- **Docx (current):** `[[1,1,1], [1,1,1]]` — 2×3
- **Cells/row match:** YES (both `[3, 3]`)

### Cells

| Position | JSON label | JSON text (first 50c) | Docx label | Docx text (first 50c) |
|---|---|---|---|---|
| R1C1 | 1א | ספק אכל חלב ספק לא אכל ואפלו אכל | 1ג | כשם שאם אכל חלב ודם נותר ופגול |
| R1C2 | 1ב | כשם שאם אכל חלב וחלב בהעלם אחד אינו חיב | 1ב | כשם שאם אכל חלב וחלב בהעלם אחד אינו חיב |
| R1C3 | 1ג | כשם שאם אכל חלב ודם נותר ופגול בהעלם | 1א | ספק אכל חלב ספק לא אכל ואפלו אכל |
| R2C1 | 2א | חלב ונותר לפניו אכל אחד מהם ואין ידוע | 2ג | רבי שמעון שזורי ורבי שמעון אומרים |
| R2C2 | 2ב | אמר רבי יוסף לא נחלקו | 2ב | אמר רבי יוסף לא נחלקו |
| R2C3 | 2ג | רבי שמעון שזורי ורבי שמעון אומרים | 2א | חלב ונותר לפניו אכל אחד מהם ואין ידוע |

### Analysis

The content is identical between JSON and docx — same text in all 6 cells. The only difference is **column ordering** (RTL reversal). JSON has 1א→1ב→1ג left-to-right; docx extraction produces 1ג→1ב→1א. R1C2 (1ב) matches because it's the middle cell.

**No content contamination from the keritot_3/4 merger.** The ספק אכל חלב opening is correctly in keritot_4 (not displaced to keritot_3). The separation was clean.

### Markers

- **JSON:** 0 markers
- **Docx:** 0 markers

### Decision needed

**Content is correct.** The JSON entry contains the same text as the docx; only the column order differs (RTL convention). The JSON can be replaced with the docx extraction to get consistent ordering with other chapters — or left as-is since the content matches. No urgent action needed.

---

## keritot_5

### Shape

- **JSON (live):** `[[1,1,1], [1,1,1]]` — 2×3
- **Docx (current):** `[[1,1,1], [1,1,1]]` — 2×3
- **Cells/row match:** YES (both `[3, 3]`)

### Cells

| Position | JSON label | JSON text (first 50c) | Docx label | Docx text (first 50c) |
|---|---|---|---|---|
| R1C1 | 1א | דם שחיטה בבהמה בחיה ובעופות | 1ג | האשה שהביאה חטאת העוף ספק |
| R1C2 | 1ב | רבי עקיבא מחיב על ספק מעילות | 1ב | רבי עקיבא מחיב על ספק מעילות |
| R1C3 | 1ג | האשה שהביאה חטאת העוף ספק | 1א | דם שחיטה בבהמה בחיה ובעופות |
| R2C1 | 2א | (empty) | 2ג | חתיכה שלחלב וחתיכה שלחלב קדש |
| R2C2 | 2ב | חתיכה שלחלב וחתיכה שלקדש | 2ב | חתיכה שלחלב וחתיכה שלקדש |
| R2C3 | 2ג | (empty) | 2א | חתיכה שלחלין וחתיכה שלקדש |

### Specific check

- **First cell (R1C3 in docx / R1C1 in JSON):** Contains "דם שחיטה בבהמה בחיה ובעופות" — the canonical opening of Keritot 5. **CONFIRMED.**
- **No displaced content** from keritot_3 or keritot_4.

### Subdivisions

- JSON: 4 subdivisions (in R2C1 and R2C3)
- Docx: 4 subdivisions (A,B in R2C1 and R2C3) — same structure

### Markers

- **JSON:** 0 markers
- **Docx:** 0 markers

### Decision needed

**No action needed.** Content is correct; same RTL column-order difference as keritot_4. No contamination from the adjacent chapter split.

---

## kinnim_1

### Matching

The v2.1 extractor **could not match** this chapter. Root cause: the docx spells the tractate as **מסכת קינים** (with yod: קינים) but the extractor's `TRACTATE_NAMES` dictionary only has **קנים** (without yod). This is a **Bug 4** — a missing alternate Hebrew spelling.

Extraction was performed manually from table #416.

### Shape

- **JSON (live):** `[[1,1,1,1,1], [1,1,1,1]]` — row 1 has 5 cells, row 2 has 4 cells (9 total)
- **Docx (current):** `[[1,1,1], [1,1,1]]` — 2×3 (6 total)
- **Cells/row match:** NO

### Cells

| Position | JSON | Docx |
|---|---|---|
| R1C1 | 1א (empty) | 1ג: איזהו נדר האומר הרי עלי עולה... [subs A,B,C] |
| R1C2 | 1ב: סדר קנים כך הוא החובה... | 1ב: סדר קנים כך הוא החובה... |
| R1C3 | 1ג (empty) | 1א: חטאת העוף נעשית למטה... [subs A,B,C] |
| R1C4 | **1ב: סדר קנים... (DUPLICATE)** | — |
| R1C5 | **1ג (empty, DUPLICATE)** | — |
| R2C1 | 2א (empty) | 2ג: כיצד משם אחד לדה ולדה... [subs A,B,C] |
| R2C2 | 2א (empty, **DUPLICATE LABEL**) | 2ב: במה דברים אמורים בחובה... |
| R2C3 | 2ב: במה דברים אמורים... | 2א: חטאת שנתערבה בעולה... [subs A,B,C] |
| R2C4 | 2ג (empty) | — |

### Analysis

The JSON entry is clearly corrupted:
- **Row 1:** 5 cells instead of 3 — cells 1ב and 1ג are duplicated (cells 4-5 repeat cells 2-3)
- **Row 2:** 4 cells instead of 3 — label 2א appears twice
- **Total:** 9 cells vs correct 6

The docx extraction is clean:
- 2×3 shape, 6 cells, no duplicates
- Labels: 1ג, 1ב, 1א / 2ג, 2ב, 2א (RTL order)
- 4 cells have A,B,C subdivisions (12 total)
- 0 markers (no styled text)

### Decision needed

**JSON entry must be replaced.** The current JSON has duplicate rows from the pre-fix docx. The clean docx extraction should replace it entirely. Note: the extractor needs a new alias (`"קינים": "kinnim"`) added to `TRACTATE_NAMES` before automated extraction will work.

---

# Summary

## Match status

| Chapter | Matched by v2.1? | Table # | Notes |
|---|---|---|---|
| keritot_3 | YES | #392 | Reversed header (פרק first) |
| keritot_4 | YES | #393 | Reversed header |
| keritot_5 | YES | #394 | Reversed header |
| kinnim_1 | **NO** | #416 (manual) | Missing Hebrew spelling alias: קינים |

## Shape agreement

| Chapter | JSON shape | Docx shape | Match? |
|---|---|---|---|
| keritot_3 | [2, 2] | [2, 2] | YES |
| keritot_4 | [3, 3] | [3, 3] | YES |
| keritot_5 | [3, 3] | [3, 3] | YES |
| kinnim_1 | [5, 4] | [3, 3] | **NO** (JSON corrupted) |

## Text content

- **keritot_3:** JSON cells are empty (Group B shape-only); docx has full text with A-D subdivisions. No contamination.
- **keritot_4:** Same content in JSON and docx; column order reversed (RTL). ספק אכל חלב confirmed in correct chapter. Separation was clean.
- **keritot_5:** Same content; column order reversed. דם שחיטה confirmed in correct chapter. No displaced content.
- **kinnim_1:** JSON has 9 cells with duplicates; docx has clean 6 cells. JSON is corrupted.

## Recommendations

| Chapter | Recommendation |
|---|---|
| keritot_3 | **Replace JSON with docx extraction.** Group B target shape is fulfilled — docx has 2×2 with A-D subdivisions. |
| keritot_4 | **Optional: replace JSON with docx extraction** to normalize column ordering. Content is identical. |
| keritot_5 | **No action.** Content correct, no anomalies. |
| kinnim_1 | **Replace JSON with docx extraction.** Current JSON is corrupted (duplicate rows). Also: add `"קינים": "kinnim"` alias to extractor. |

## Extractor fix needed

Add to `TRACTATE_NAMES` in `mishnah_extractor_v2.py`:

```python
"קינים": "kinnim",
```

This is the same class of bug as the alternate spellings fixed in v2.1 (עדיות, נידה, etc.). Bump to v2.1.1 or note for next version.
