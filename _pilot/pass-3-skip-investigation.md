# Pass 3 Skip Investigation

**Date:** 2026-05-10
**Scope:** Investigate the 246 chapters that remain without markers after Pass 3

---

## 1. Revised Inventory

Pass 3 left 246 chapters without markers (not 192 as the pass-3-report stated). The discrepancy: 54 chapters were "successfully extracted" but had 0 styled runs in the docx — the table matched, the shape aligned, but there was no colored text to extract. These are effectively "no markers in docx" alongside the other 173.

| Category | Count | Description |
|---|---|---|
| No markers in docx | 173 | Table found, shape OK, no styled text |
| Shape mismatch | 20 | Table found, row/column structure differs |
| Unmatched | 53 | No matching table found |
| **Total** | **246** | |

### Distribution by Seder

| Seder | No markers | Shape mismatch | Unmatched | Total |
|---|---|---|---|---|
| Zeraim | 1 | 0 | 0 | 1 |
| Moed | 6 | 0 | 0 | 6 |
| Nashim | 3 | 2 | 1 | 6 |
| Nezikin | 11 | 11 | 6 | 28 |
| Kodashim | 54 | 4 | 21 | 79 |
| Toharot | 80 | 3 | 25 | 108 |

The pattern is unmistakable: Kodashim and Toharot account for 76% of all empty chapters. These are the last two Sedarim — the structural analysis work simply hasn't reached them yet in full.

---

## 2. Shape Mismatch Analysis (20 chapters)

### All 20 cases

| Chapter | JSON shape | Docx shape | Match method |
|---|---|---|---|
| avot_2 | [1,3,4,4,6,2] | [1,3,4,1,3,1,5,2] | jaccard |
| eduyot_7 | [3,3] | [2,2,2,2,2,2] | jaccard |
| kelim_4 | [3,3] | [2,2] | jaccard |
| keritot_4 | [3,3] | [2,2,3,3,3] | jaccard |
| ketubot_11 | [1,2,1,2,1] | [1,2,1] | jaccard |
| kinnim_1 | [5,4] | [3,3,3] | jaccard |
| makkot_1 | [4,3,3,3] | [1,3,3,3,3] | jaccard |
| makkot_2 | [4,3,3,3] | [1,3,3,3,3] | jaccard |
| makkot_3 | [4,2,2,2,3] | [1,3,2,2,2,3] | jaccard |
| meilah_1 | [2,2,3,1] | [2,2,1,2,1] | jaccard |
| niddah_3 | [3,3,6] | [3,3,3,3] | jaccard |
| sanhedrin_11 | [3,3,3,3,2] | [1,2,3,3,3,2] | jaccard |
| sanhedrin_6 | [4,3,3,3] | [3,3,3,3] | jaccard |
| sanhedrin_7 | [4,4] | [1,3,1,3] | jaccard |
| shevuot_3 | [2,4,2,2,2] | [2,2,2,2,2,2] | jaccard |
| shevuot_6 | [4,3,3,3] | [1,3,3,3,3] | jaccard |
| shevuot_8 | [3,3,2] | [1,2,3,2] | jaccard |
| tahorot_1 | [3,4,3] | [3,1,3,3] | jaccard |
| temurah_7 | [3,3,2] | [2,2,2,2] | jaccard |
| yevamot_2 | [3,3] | [2,2,2,2,2] | header |

### Patterns found

1. **Docx has more rows than JSON in 17/20 cases.** The most common pattern: the docx has a full-width "title" row (colspan = full table width) that introduces the chapter, while the JSON merges this text into the first data row. Examples: makkot_1/2/3, sanhedrin_11, shevuot_6/8.

2. **Only 1 is header-matched; 19 are Jaccard-matched.** This suggests high confidence that the table IS the right one (Jaccard scores 0.47–0.94), but the structural encoding differs between the docx and JSON.

3. **The mismatches represent different structural analyses**, not extraction bugs. The docx was formatted at one time; the JSON was authored (or revised) at another time with different row/column decisions. Example: `yevamot_2` has 2 rows × 3 columns in JSON but 5 rows × 2 columns in docx — a fundamentally different structural reading.

4. **JSON has more rows than docx in only 1 case** (`ketubot_11`: JSON 5 rows, docx 3 rows). This suggests the JSON has a newer/more detailed analysis.

### 5 detailed samples

**makkot_1** (Nezikin): JSON has 4 rows [4,3,3,3]; docx has 5 rows [1,3,3,3,3]. The docx has an extra full-width opening row `(א) כיצד העדים נעשים זוממין` that JSON includes in row 1 as a 4th cell.

**sanhedrin_11** (Nezikin): JSON has 5 rows [3,3,3,3,2]; docx has 6 rows [1,2,3,3,3,2]. Same pattern — docx has a full-width opening row with the chapter introduction.

**avot_2** (Nezikin): JSON has 6 rows [1,3,4,4,6,2]; docx has 8 rows [1,3,4,1,3,1,5,2]. The docx splits row 4 into a title row + data row, and similarly for row 5. This reflects different editorial decisions about what constitutes a "row."

**yevamot_2** (Nashim): JSON has 2 rows × 3 columns; docx has 5 rows × 2 columns. Genuinely different structural analysis — not a formatting difference but a scholarly disagreement about the chapter's architecture.

**ketubot_11** (Nashim): JSON has 5 rows [1,2,1,2,1]; docx has 3 rows [1,2,1]. The JSON extends beyond what the docx covers — likely a more recent analysis.

---

## 3. Unmatched Chapter Analysis (53 chapters)

### Root causes identified

Two bugs in the extractor's header-matching logic explain 51 of the 53 unmatched chapters:

**Bug 1: Reversed header format (affects 36 chapters)**

The docx has TWO header formats:
- Standard (256 tables): Cell 0 = `מסכת X`, Last Cell = `פרק Y`
- Reversed (269 tables): Cell 0 = `פרק Y`, Last Cell = `מסכת X`

The extractor only checks the standard orientation (`'מסכת' in c0 and 'פרק' in cl`). Adding a reverse check (`'פרק' in c0 and 'מסכת' in cl`) recovers 36 chapters.

**Bug 2: Hebrew numeral conversion (affects 10 chapters)**

The `_hebrew_chapter_num_to_str()` function treats numbers as letter indices (the 11th Hebrew *letter* = כ) rather than Hebrew numerals (the *number* 11 = יא). This means chapters 11+ get wrong Hebrew strings and can't match headers.

| Chapter | Buggy conversion | Correct conversion |
|---|---|---|
| 11 | כ (11th letter) | יא (10+1) |
| 12 | ל (12th letter) | יב (10+2) |
| 14 | נ (14th letter) | יד (10+4) |
| 17 | פ (17th letter) | יז (10+7) |
| 22 | ת (22nd letter) | כב (20+2) |
| 30 | "30" (fallthrough) | ל (30) |

Affected chapters: kelim_17, kelim_18, kelim_22, kelim_30, ketubot_14, negaim_12, negaim_14, parah_12, zevachim_14, yadayim_4.

**Bug 3: Key naming mismatches (affects 7 chapters)**

The JSON uses non-standard English transliterations for 4 tractates:

| JSON key prefix | Extractor produces | Chapters affected |
|---|---|---|
| `oktzin` | `uktzin` | 3 |
| `tevulyom` | `tevul_yom` | 1 |
| `avodazara` | `avodah_zarah` | 1 |
| `tahorot` | `toharot` | 2 |

Some overlap with Bug 2 (chapters with high numbers AND wrong key prefix).

**Residual: 2 genuinely absent chapters**

After all fixes: `ketubot_14` and `yadayim_4` have no matching table in the docx. These chapters may not have been structurally analyzed yet at all.

### Verification with corrected matching

With all three fixes applied:

| Result | Count |
|---|---|
| Recovered (shape matches) | 46 |
| Recovered (shape mismatch) | 5 |
| Still unmatched | 2 |
| **Total** | **53** |

---

## 4. Recommendations

### Category 1: No markers in docx (173 chapters)

**Action: Accept and skip.** These chapters have correct tables in the docx but no colored/styled text — the structural analysis hasn't been done for them yet. This is a data-authoring gap, not an extraction problem. As analysis proceeds (concentrated in Kodashim and Toharot), these will be populated in future extraction passes.

**Recovery potential:** 0 chapters recoverable mechanically. All 173 require scholarly analysis.

### Category 2: Shape mismatches (20 + 5 = 25 chapters)

**Action: Manual case-by-case review.** The mismatches represent genuine structural disagreements between the docx and JSON. The most common pattern (extra full-width title row in docx) could theoretically be handled by a "flexible shape comparison" that ignores 1-cell rows, but this risks masking real structural differences.

**Recommended sub-actions:**
1. For the "title row" pattern (makkot_1/2/3, sanhedrin_11, shevuot_6/8, etc.): Consider whether the JSON or docx better represents the intended structure. If the docx is authoritative, update the JSON shapes.
2. For genuine structural disagreements (yevamot_2, eduyot_7): These need scholarly decision about which analysis is current.

**Recovery potential:** ~12 chapters could be extracted if the extractor learned to ignore single-cell title rows (an optional mode). The other ~13 are genuinely different structures.

### Category 3: Unmatched (53 chapters)

**Action: Fix the extractor.** Three code changes recover 51 of 53:

1. **Add reversed header matching** — check both `(מסכת in c0, פרק in cl)` and `(פרק in c0, מסכת in cl)`. One line of code.
2. **Fix `hebrew_num` function** — replace letter-index lookup with proper gematria conversion. ~10 lines.
3. **Add key aliases** — map `oktzin→uktzin`, `tevulyom→tevul_yom`, `avodazara→avodah_zarah`, `tahorot→toharot` during matching. 4 lines.

**Recovery potential:**
- 46 chapters become matchable with correct shapes → ready for extraction
- Of those 46, most likely have no markers (they're in Kodashim/Toharot where analysis is sparse) — so the practical marker yield is probably low
- 5 more become matchable but have shape mismatches → join the manual review set
- 2 remain genuinely absent

---

## 5. Summary and Recovery Estimate

| Category | Chapters | Recoverable by code fix | Needs scholarly work |
|---|---|---|---|
| No markers in docx | 173 | 0 | 173 (analysis needed) |
| Shape mismatch | 20 | ~12 (title-row tolerance) | ~8 (structural disagreement) |
| Unmatched | 53 | 51 (3 bugs fixed) | 2 (genuinely absent) |
| **Total** | **246** | **~63** | **~183** |

**Bottom line:** The 246-chapter skip is primarily a **data-authoring gap** (70%), not a technical limitation. The structural analysis work in the docx is concentrated in the first four Sedarim (Zeraim through Nezikin) and thins out dramatically in Kodashim and Toharot.

The extractor has three fixable bugs that together recover 51 chapters from the "unmatched" category into "matchable." However, most of those 51 will likely yield 0 markers (no styled text) — the fix improves coverage tracking but won't add much actual structural data.

The 20 shape-mismatch chapters are the most interesting for future work: they represent places where the docx and JSON encode different scholarly judgments. Resolving those requires Moshe's decision about which structural analysis is current.

---

## 6. Extractor Bugs to Fix (for Pass 4)

### Bug 1: Reversed header orientation

```python
# Current (only checks one orientation):
if 'מסכת' in c0 and 'פרק' in cl:

# Fixed (checks both):
if 'מסכת' in c0 and 'פרק' in cl:
    tractate_text, chapter_text = c0, cl
elif 'פרק' in c0 and 'מסכת' in cl:
    tractate_text, chapter_text = cl, c0
```

### Bug 2: Hebrew numeral conversion

```python
# Current (WRONG — treats numbers as letter indices):
def _hebrew_chapter_num_to_str(num):
    if 1 <= num <= 22:
        return HEBREW_LETTERS[num - 1]  # BUG: 11th letter ≠ number 11

# Fixed (proper gematria):
def _hebrew_chapter_num_to_str(num):
    ones = ['', 'א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט']
    tens = ['', 'י', 'כ', 'ל']
    if num == 15: return 'טו'
    if num == 16: return 'טז'
    result = tens[num // 10] + ones[num % 10]
    return result
```

### Bug 3: Key aliases

```python
KEY_ALIASES = {
    'avodazara': 'avodah_zarah',
    'oktzin': 'uktzin',
    'tevulyom': 'tevul_yom',
    'tahorot': 'toharot',
}
# Apply reverse aliases when looking up JSON keys from extractor-produced keys
```

---

## Files Created

- `_pilot/pass-3-skip-investigation.md` — this report
- `_pilot/skipped-chapters.csv` — full inventory (246 rows)
