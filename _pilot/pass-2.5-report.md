# Pass 2.5 Report: Three Fixes

**Date:** 2026-05-10

---

## 1. Null-Byte Corruption Diagnosis

### Pattern

Both corrupted files show the same pattern: **contiguous trailing null bytes** appended after valid content. The content before the nulls is intact and identical to the git HEAD version.

| File | Total size | Valid content | Null padding | Content matches HEAD? |
|---|---|---|---|---|
| `mishnah_db.json` | 6,560,768 | 5,099,317 | 1,461,451 (22%) | Yes, byte-identical |
| `hebrew-leviticus-unit-19.html` | 402,896 | 21,117 | 381,779 (95%) | No — 504 bytes larger than HEAD (modified + padded) |

No interleaved corruption. No content damage. The last valid byte in `mishnah_db.json` is `}` (0x7d) — the closing brace of the JSON object. The nulls begin immediately after and run contiguously to EOF.

A scan of all 718 large text files (>100 KB) found only these two affected.

### `_redirects` status

Clean — no null bytes. The corruption we fixed in Phase 2 has not recurred.

### Cause

**This is not a Cowork write bug.** Evidence:

1. `mishnah_db.json` was last modified May 4 (before this session). Its valid content is byte-identical to the git HEAD commit. Cowork in this session never wrote to it.
2. The null padding ratios are inconsistent (1.29× for the JSON, 19× for the HTML), ruling out a fixed block-alignment algorithm.
3. The `hebrew-leviticus-unit-19.html` was modified May 8 — likely by an earlier Cowork session that wrote the file, then the mount/sync layer padded it.

**Most likely cause:** The Cowork sandbox mount layer (which maps Windows NTFS paths to Linux paths via `/sessions/.../mnt/`) pre-allocates or over-allocates file buffers during writes. When the write completes with fewer bytes than the allocated buffer, the remaining bytes stay as nulls. This would explain why only files that were written through the sandbox (or opened read-write through it) are affected, and why the padding amounts are variable.

**Prevention:** Every write to a repo file from the sandbox should be followed by a truncation to the actual content length. Alternatively, files should be written via a temp file + atomic rename, which avoids the buffer pre-allocation issue. For now, the practical mitigation is: **check for and strip trailing nulls when reading any file that may have been written through the sandbox.**

---

## 2. `mishnah_db.json` Cleanup

| Metric | Value |
|---|---|
| Original size | 6,560,768 bytes |
| Cleaned size | 5,099,317 bytes |
| Bytes removed | 1,461,451 |
| JSON valid after cleanup | Yes |
| `_meta` key present | Yes |
| Chapter entries | 524 (unchanged) |
| Re-parse after write | OK |

The file was truncated at the first null byte and rewritten. The cleaned file is byte-identical to the git HEAD version (the working copy had no real edits, only padding).

**Note:** `hebrew-leviticus-unit-19.html` also has null padding but was NOT cleaned in this pass, because its valid content differs from HEAD (it was actually modified). Cleaning it requires reviewing the modification first. This is flagged for a future task.

---

## 3. Space-Loss Diagnosis

### What the docx XML actually contains

The Word document encodes line breaks and inter-word spaces as separate XML elements within runs:

**Line breaks** are `<w:br/>` elements inside `<w:r>` runs. A single run can contain both a `<w:br/>` and a `<w:t>` — for example, the phrase "באחד עשר" in cell 1א is stored as:

```xml
<w:r>
  <w:rPr><w:rtl/></w:rPr>
  <w:br/>                          <!-- line break -->
  <w:t>באחד עשר</w:t>              <!-- text that follows -->
</w:r>
```

**Inter-word spaces** between marker-styled runs are stored as separate plain-text runs containing just a space character with `xml:space="preserve"`:

```xml
<w:r><w:rPr><w:rStyle w:val="Horizontal10"/></w:rPr>
  <w:t>כרכין</w:t>
</w:r>
<w:r><w:rPr><w:rtl/></w:rPr>
  <w:t xml:space="preserve"> </w:t>   <!-- space between markers -->
</w:r>
<w:r><w:rPr><w:rStyle w:val="Horizontal10"/></w:rPr>
  <w:t>המקפין</w:t>
</w:r>
```

### Why the original extractor dropped them

The Pass 2 extractor collected text only from `<w:t>` elements via:
```python
text = ''.join(t.text or '' for t in run_el.findall(qn('w:t')))
```

This missed `<w:br/>` elements entirely (they have no text attribute — they're self-closing tags that mean "insert a line break here"). The space-only runs WERE captured, but their text was concatenated without the preceding newline, making the output look like `מגלה נקראתבאחד עשר` instead of `מגלה נקראת\nבאחד עשר`.

### Fix applied

The v2 extractor walks ALL children of each `<w:r>` run element:

```python
for child in run_el:
    tag = child.tag.split('}')[-1]
    if tag == 't':
        text_parts.append(child.text or '')
    elif tag == 'br':
        text_parts.append('\n')
    elif tag == 'tab':
        text_parts.append('\t')
    elif tag == 'cr':
        text_parts.append('\n')
```

This captures line breaks, tabs, and carriage returns in document order alongside text content.

---

## 4. Re-Extraction Results

### Cell 1א comparison

**Extracted (v2):**
```
1א
(א) מגלה נקראת
באחד עשר
בשנים עשר
בשלשה עשר
בארבעה עשר
בחמשה עשר
לא פחות ולא יותר
כרכין המקפין חומה מימות יהושע בן נון קורין בחמשה עשר
כפרים ועירות גדולות קורין בארבעה עשר
אלא שהכפרים מקדימין ליום הכניסה
```

**Existing JSON:**
```
מגלה נקראת
באחד עשר
בשנים עשר
...
```

**Result: MATCH** (after stripping the cell label `1א\n` and mishnah number `(א) `).

### Full comparison — all 12 cells

| Cell | Has subdivisions? | Text match (label/number stripped)? | Notes |
|---|---|---|---|
| 1א | No | MATCH | — |
| 1ב | No | MATCH | — |
| 2א | Yes (A, B) | Differs by `A ` / `B ` markers | Content identical; existing strips subdivision letters |
| 2ב | No | MATCH | — |
| 2ג | Yes (A, B) | Differs by `A ` / `B ` markers | Same pattern |
| 3א | Yes (A, B) | Differs by `A ` / `B ` markers | Same pattern |
| 3ב | Yes (A, B) | Differs by `A ` / `B ` markers | Same pattern |
| 4א | No | MATCH | — |
| 4ב | Yes (A, B) | Differs by `A ` / `B ` markers | Same pattern |
| 4ג | No | MATCH | — |
| 5א | Yes (A, B) | Differs by `A ` / `B ` markers | Same pattern |
| 5ב | Yes (A, B) | Differs by `A ` / `B ` markers | Same pattern |

All 5 non-subdivided cells match exactly. All 7 subdivided cells match after removing the inline `A` / `B` markers. The existing JSON stores subdivision content separately and doesn't include the letter markers in the text — the extracted JSON preserves them inline. This is a formatting convention difference, not a content discrepancy.

### Extraction stats (v2)

| Metric | Pass 2 (v1) | Pass 2.5 (v2) |
|---|---|---|
| Total runs processed | 203 | 236 |
| Output file size | 40,132 bytes | 43,292 bytes |
| Markers extracted | 50 | 50 |
| Cells with subdivisions | 7 | 7 |
| Anomalies | 0 | 0 |

The run count increased from 203 to 236 because the v2 extractor captures `<w:br/>`-only runs and space-only runs that v1 skipped.

---

## 5. Additional Finding

The `mishnah_db.json` note about null bytes: the file in the repo had 1,461,451 bytes of null padding but zero content changes from git HEAD. The git diff showed `1 insertion, 1 deletion` purely because the null padding makes git see the single-line JSON as changed. After cleaning, `git diff` should show the file as unmodified.

---

## Files Updated

- `Mishnah-New/English/mishnah_db.json` — cleaned (5,099,317 bytes, was 6,560,768)
- `_pilot/megillah_1_extracted.json` — re-extracted with proper whitespace (43,292 bytes)
- `_pilot/pass-2.5-report.md` — this report
