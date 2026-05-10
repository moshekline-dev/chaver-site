# Reconnaissance Report: Megillah Chapter 1 — Word Document Inspection

**Source:** `The Whole  Structured Mishnah for pdf.docx` (3.40 MB)
**Date:** 2026-05-10
**Status:** Read-only inspection. Nothing was modified.

---

## 1. Document Parse Summary

| Property | Value |
|---|---|
| File size | 3.40 MB |
| Parser | python-docx (successfully parsed, no errors) |
| Total paragraphs | 738 |
| Total tables | 544 |
| Total sections | 16 |
| Page count | Not available via python-docx (Word-only metadata) |

The 544 tables are consistent with the expected ~524 Mishnah chapters plus front-matter tables.

---

## 2. Megillah Chapter 1 — Location and Shape

**Location:** Body element #522, Table #168 (0-indexed).
Preceded by paragraph #53 containing `מסכת מגילה175` (likely a TOC entry or section heading).

**Table structure:** 6 rows total.

| Row | Purpose | Cell spans | Cell labels |
|---|---|---|---|
| 0 | Header | [1, 2, 1] | מסכת מגילה / המשנה כדרכה / פרק א |
| 1 | Content | [2, 2] | 1א, 1ב |
| 2 | Content | [1, 2, 1] | 2א, 2ב, 2ג |
| 3 | Content | [2, 2] | 3א, 3ב |
| 4 | Content | [1, 2, 1] | 4א, 4ב, 4ג |
| 5 | Content | [2, 2] | 5א, 5ב |

**Content shape (rows 1–5):** `[[2,2], [1,2,1], [2,2], [1,2,1], [2,2]]`
**Expected shape from JSON:** `[[2,2], [1,2,1], [2,2], [1,2,1], [2,2]]`
**Result: MATCH**

---

## 3. Color / Marker Formatting

### Critical Finding: No Direct Run Colors

The initial scan found **zero** `w:color` elements applied directly to runs. All color formatting is applied via **character styles** — named styles whose *definitions* contain color values. The python-docx `run.font.color.rgb` API returns `None` for these runs because it doesn't resolve inherited style properties.

**Extraction approach must resolve styles to their defined colors, not check run-level color directly.**

### Table A — Distinct Marker Styles in Megillah 1

| Style ID | Display Name | Color (hex) | Extra formatting | Runs | Chars | Sample text |
|---|---|---|---|---|---|---|
| `Horizontal10` | Horizontal1 | #3399FF (blue) | — | 36 | 194 | כרכין, המקפין, חומה |
| `InternalParallel` | InternalParallel | #C00000 (dark red) | — | 10 | 37 | לשבת, שבת, המדר |
| `Horizontal2` | Horizontal2 | #008080 (teal) | — | 2 | 47 | אמרו מקדימין ולא מאחרין |
| `Horizontal3` | Horizontal3 | #008B8B (dark cyan) | underline (words) | 2 | 30 | ומתנות לאביונים |
| `Subunit` | Subunit | none (bold) | bold, FrankRuehl font | 40 | — | 1א, A, B |

### Table B — Per-Cell Marker Breakdown

| Cell | Base text (chars) | Marker styles used |
|---|---|---|
| 1א | 162 | Horizontal10 (6 runs, 32 chars) |
| 1ב | 323 | Horizontal10 (30 runs, 162 chars) |
| 2א | 126 | Horizontal2 (1 run, 23 chars) |
| 2ב | 136 | Horizontal2 (1 run, 24 chars), Horizontal3 (1 run, 15 chars) |
| 2ג | 104 | Horizontal3 (1 run, 15 chars) |
| 3א | 94 | InternalParallel (2 runs, 7 chars) |
| 3ב | 145 | InternalParallel (2 runs, 9 chars) |
| 4א | 47 | none |
| 4ב | 90 | InternalParallel (2 runs, 8 chars) |
| 4ג | 155 | none |
| 5א | 116 | InternalParallel (2 runs, 6 chars) |
| 5ב | 292 | InternalParallel (2 runs, 7 chars) |

### Full Style Catalog (Document-Wide)

Eight structural marker styles are defined and used across all 544 tables:

| Style ID | Color | Tables using it | Total runs | In Megillah 1? |
|---|---|---|---|---|
| `Horizontal10` | #3399FF (blue) | 284 | 3,751 | Yes |
| `Vertical1` | #8B4513 (brown) | 107 | 1,134 | No |
| `InternalParallel` | #C00000 (dark red) | 98 | 1,333 | Yes |
| `Horizontal2` | #008080 (teal) | 87 | 428 | Yes |
| `Horizontal3` | #008B8B (dark cyan) | 86 | 417 | Yes |
| `Closure` | #77206D (purple) | 38 | 147 | No |
| `Ciasm1` | #7030A0 (violet) | 20 | 64 | No |
| `Ciasm2` | #7030A0 (violet, underlined) | 15 | 53 | No |

One additional style (`StyleVertical17ptLightOrange1`, #FF0000) appears in exactly 1 table with 1 run — likely a one-off or error.

---

## 4. Non-Color Formatting

**Bold:** Used exclusively by the `Subunit` character style for cell labels (1א, 2ב, etc.) and A/B subdivision markers. No bold runs exist outside `Subunit`. Bold carries no independent structural meaning.

**Italic:** Zero italic runs in Megillah 1. Zero `w:i` or `w:iCs` elements in the table XML.

**Underline:** Used only as part of `Horizontal3` (underline type: "words") and `Ciasm2` (underline type: "words"). Underline is not independent — it's bundled into the style definition and distinguishes subtypes within a color family.

**Highlight:** None.

**Conclusion:** Formatting dimensions are fully captured by the character style name. There is no need to extract bold/italic/underline independently — they're redundant with the style. The style name IS the marker type.

---

## 5. A/B Subdivision Markers

Subdivision markers appear in 7 of the 12 content cells:

| Cell | Markers | Formatting |
|---|---|---|
| 2א | A, B | Subunit style (bold, no color) |
| 2ג | A, B | Subunit style |
| 3א | A, B | Subunit style |
| 3ב | A, B | Subunit style |
| 4ב | A, B | Subunit style |
| 5א | A, B | Subunit style |
| 5ב | A, B | Subunit style |

**Pattern:** A/B markers are their own runs, styled with `Subunit`, appearing inline in the cell text. They use Latin A/B (not Hebrew א/ב). No C markers appear in this chapter (though they may in others).

**Detection approach:** Scan for runs with `Subunit` style whose text matches `^[A-Z]\s*$`. The cell label (e.g., "2א") is also `Subunit`-styled but is distinguishable because it starts with a digit + Hebrew letter.

---

## 6. Open Questions for Human Review

### Q1: Style name → CSS class mapping

The docx uses character style names. The HTML pages on chaver.com use CSS classes. The likely mapping is:

| Docx style | Probable CSS class | Evidence |
|---|---|---|
| `Horizontal10` | `horizontal1` | Style's display name is "Horizontal1"; #3399FF matches the site's blue |
| `Horizontal2` | `horizontal2` | Direct name match |
| `Horizontal3` | `horizontal3` | Direct name match |
| `Vertical1` | `vertical1` | Direct name match |
| `Closure` | `closure` | Direct name match |
| `Ciasm1` | `ciasm1` | Direct name match |
| `Ciasm2` | `ciasm2` | Direct name match |
| `InternalParallel` | ??? | No obvious CSS class counterpart on the Torah pages |

**Moshe:** Is this mapping correct? Specifically:

- Does `Horizontal10` map to CSS class `horizontal1`? (The style *ID* is "Horizontal10" but the display *name* is "Horizontal1" — this looks like a Word quirk where the style was renamed but the ID kept the old value.)
- What CSS class does `InternalParallel` map to? The Torah HTML pages don't seem to have an `internalparallel` class. Does this marker type appear in the Mishnah HTML pages at all, or is it print-only?
- The one-off `StyleVertical17ptLightOrange1` (#FF0000) — is this a real marker type or an editing artifact?

### Q2: Color values — docx vs. CSS

The colors in the style definitions don't need to match CSS exactly (CSS controls rendering on the site), but confirming the mapping by cross-referencing a few chapters against their HTML pages would validate the extraction. Should we do that as part of Pass 2?

### Q3: Subunit style double duty

`Subunit` is used for both cell labels ("1א") and A/B markers ("A", "B"). The extraction needs to distinguish these. The proposed heuristic: if the run text is a single Latin uppercase letter, it's a subdivision marker; otherwise it's a cell label. Is there any case where this heuristic would fail?

### Q4: Missing marker types in Megillah 1

Megillah 1 uses only 4 of the 8 marker styles (no Vertical1, Closure, Ciasm1, Ciasm2). The extraction code should handle all 8. Should we also run this reconnaissance on a chapter that uses all 8 (or at least the missing 4) to verify they work the same way?

### Q5: Cells with no markers

Cells 4א and 4ג have zero marker styles — all text is plain. Is this expected for these mishnayot, or could it indicate that markers were lost in this version of the document?

---

## Summary: Can We Proceed to Pass 2?

| Question | Answer |
|---|---|
| Can python-docx read the document? | Yes, cleanly |
| Does the table shape match the JSON? | Yes, exact match |
| How many colors / how are they encoded? | 8 marker styles via character styles (not direct colors) |
| Are A/B subdivisions detectable? | Yes — `Subunit`-styled single-letter Latin runs |
| Any formatting we'd miss with color-only extraction? | No — but we'd miss everything if we only checked run-level colors. Must resolve character styles. |

**The extraction approach for Pass 2:** Read the `w:rStyle` value from each run's `rPr`, map it to the known marker-type table, and emit the corresponding JSON marker. Colors are irrelevant at extraction time — the style name carries all the information.
