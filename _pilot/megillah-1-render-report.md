# Render Report: Megillah 1 with Marker Spans (Visual Pilot)

**Date:** 2026-05-10

---

## 1. Source Files

| Input | Path | Size |
|---|---|---|
| Extracted JSON | `_pilot/megillah_1_extracted.json` | 43,292 bytes (v2, with proper spaces) |
| Template | `_templates/Academic-Content-HE.html` | 14,908 bytes |
| Reference structure | `Mishnah-New/Hebrew/Text/Seder Moed/Masechet Megillah/Masechet Megillah Perek 1.htm` | (read-only, for table pattern) |

---

## 2. Rendered Output

| Property | Value |
|---|---|
| Output file | `pilot/megillah-perek-1-marked.html` |
| File size | 22,492 bytes |
| Line count | 438 lines |
| Encoding | UTF-8, LF line endings |

---

## 3. Marker Span Counts

| Marker class | Count | Expected | Match? |
|---|---|---|---|
| `horizontal1` | 36 | 36 | Yes |
| `horizontal2` | 2 | 2 | Yes |
| `horizontal3` | 2 | 2 | Yes |
| `internalparallel` | 10 | 10 | Yes |
| **Total marker spans** | **50** | **50** | **Yes** |

Additional spans:

| Class | Count | Purpose |
|---|---|---|
| `Subunit` | 19 | Cell labels (12) + subdivision markers (7 cells × 1 extra = 7) |

---

## 4. Sanity Check Results

| # | Check | Result |
|---|---|---|
| 1 | `<html lang="he" dir="rtl">` present | PASS |
| 2 | `main.css` path correct | PASS |
| 3 | `horizontal1` spans present (36) | PASS |
| 4 | `horizontal2` spans present (2) | PASS |
| 5 | `horizontal3` spans present (2) | PASS |
| 6 | `internalparallel` spans present (10) | PASS |
| 7 | No DWT markers or `{{ region:` placeholders | PASS |
| 8 | File size 22,492 bytes in [15K, 60K] range | PASS |

**All 8 checks PASSED.**

---

## 5. Structure Verification

The rendered table HTML was verified against the existing chapter page:

- **Table wrapper:** `<div align="right"><table border="0" cellpadding="0" cellspacing="0" dir="rtl" width="100%">` — matches
- **Header row:** 4 cells (Mesechet / logo colspan=2 / Perek) — matches
- **Content rows:** 5 rows with cell counts [2, 3, 2, 3, 2] — matches shape `[[2,2], [1,2,1], [2,2], [1,2,1], [2,2]]`
- **Colspan attributes:** All 12 cells have correct colspan values matching existing page
- **Cell labels:** `<span class="Subunit">LABEL<br/></span>` pattern — matches existing
- **Subdivision labels:** `<span class="Subunit">A </span>` inline pattern — matches existing
- **Combined label+subdivision:** `<span class="Subunit">2א<br/>A </span>` pattern (label and first subdivision in one span) — matches existing
- **Trailing empty row:** `<tr><td></td><td></td><td></td><td></td></tr>` — matches existing
- **Cell content order:** Document order (left-to-right in source, RTL flipped by browser) — matches existing

---

## 6. Rendering Approach

The renderer walks each cell's `runs` array in document order:

1. **Cell label** (first run): Wrapped in `<span class="Subunit">LABEL<br/></span>`
2. **First subdivision letter** (if present): Folded into the label span: `<span class="Subunit">LABEL<br/>A </span>`
3. **Subsequent subdivision letters** (B, C): New span: `<span class="Subunit">B </span>`
4. **Marker runs** (`marker` ≠ null): Wrapped in `<span class="{marker}">TEXT</span>`
5. **Plain runs** (`marker` = null): Emitted as plain text
6. **Newlines** (`\n` in run text): Converted to `<br/>`

This approach reads exclusively from the `runs` array (not the `subdivisions` or `text` fields), preserving exact document order and avoiding any reconstruction logic.

---

## 7. Anomalies

**None.** The rendering completed without errors or unexpected patterns.

**Note:** The file size (22,492 bytes) is slightly larger than the existing plain chapter page's content region because the marker `<span>` tags add markup. The existing page has no marker spans — all text is plain. This pilot adds 50 marker spans, accounting for the difference.

---

## Files Produced

- `pilot/megillah-perek-1-marked.html` — the rendered pilot page with marker spans
- `_pilot/megillah-1-render-report.md` — this report
