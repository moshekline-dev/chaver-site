# Pass 6 Re-run Report — rev8 → rev9

**Date:** 2026-05-11
**Extractor:** `_pilot/mishnah_extractor_v2.py` v2.1.4 (unchanged)
**Live dataset:** `Mishnah-New/English/mishnah_db.json`, promoted to `_meta.version: "2026-05-rev9"`
**Status:** Validation passed (13/13), promotion completed byte-identical.

This is a re-run of Pass 6 against a freshly updated docx. No extractor changes — only the docx changed.

---

## 1. Docx changes (Moshe-side, since rev8)

Source docx is now read from the Research folder canonical location:
`C:\Users\Moshe\OneDrive\Documents\Research\The Structured Mishnah\ספר על המשנה כדרכה\For KDP\The Whole  Structured Mishnah for pdf.docx` (mtime 2026-05-11 09:30).

| Chapter | Before (rev8) | After (rev9) |
|---|---|---|
| `ketubot_14` | not in docx → placeholder | new 2×3 table, shape `[[1,1,1],[1,1,1]]`, 0 markers |
| `yadayim_3` | 6-row table conflating ch.3 + ch.4, shape `[[2,2],[2,2],[2,2],[1,2,1],[2,2],[2,2]]` | corrected to clean 3×2 table, shape `[[2,2],[2,2],[2,2]]`, 0 markers |
| `yadayim_4` | not in docx (was conflated with ch.3) → placeholder | separated as its own 2×2 table, shape `[[2,2],[2,2]]`, 0 markers |

All three new/corrected tables are structurally populated; none have styled text yet.

---

## 2. Extraction summary

```
extractor_version:        2.1.4 (unchanged)
total_chapters:           525
matched_chapters:         525  (was 523 in rev8)
missing_chapters:         0    (was 2 — ketubot_14, yadayim_4)
markers_populated_count:  310  (unchanged)
total_markers:            10,405 (unchanged — new chapters carry no styled text yet)
duplicates_in_docx:       0
extraction_wall_time:     7.0s
staged_file_size:         16,656,951 bytes
```

---

## 3. Validation results

All 13 checks PASS:

1. JSON parses cleanly
2. Exactly 526 top-level keys (525 chapters + `_meta`)
3. `sotah_9` not present
4. `sotah_9a` (4 rows) and `sotah_9b` (4 rows) both present with content
5. `shabbat_22` has 10 markers
6. `zevachim_5` cells-per-row `[1,2,3,2,1]` (palindrome)
7. `sukkah_3` has content (3 rows, no `_missing_from_docx`)
8. `_meta.version == "2026-05-rev9"`
9. All marker types canonical (8 only)
10. Total markers in 9,500–11,000 range (got 10,405)
11. **`ketubot_14` populated** (rows=2, `_missing_from_docx=False`) ✓
12. **`yadayim_3` populated** (rows=3, `_missing_from_docx=False`) ✓
13. **`yadayim_4` populated** (rows=2, `_missing_from_docx=False`) ✓

---

## 4. Promotion confirmation

- **Pre-promotion:**  live `16,616,285` bytes, sha256 `5844f7a9c5792144…` (rev8)
- **Staged:**         `16,656,951` bytes, sha256 `5500c5e6bd018c96…`
- **Post-promotion:** live `16,656,951` bytes, sha256 `5500c5e6bd018c96…` (rev9, matches staged)
- **Byte-identity:**  confirmed
- **Re-parse after promotion:** OK, 526 top-level keys, `_meta.version == "2026-05-rev9"`
- **Staged file cleanup:** deletion blocked by the FUSE mount (same as Pass 6 first run). The staged file is byte-identical to live and can be safely removed manually via Windows Explorer.

---

## 5. rev8 → rev9 deltas

| Metric | rev8 | rev9 | Δ |
|---|---:|---:|---:|
| Total chapters | 525 | 525 | 0 |
| Matched chapters | 523 | 525 | +2 |
| Missing-from-docx | 2 | 0 | −2 |
| Chapters with markers | 310 | 310 | 0 |
| Total markers | 10,405 | 10,405 | 0 |
| Duplicate-table conflicts | 0 | 0 | 0 |
| Tables in docx | 541 (uploaded copy) | 543 (Research canonical) | +2 (new ketubot_14 + yadayim_4) |

No marker changes because the three new/corrected tables carry no styled text yet — they are structurally populated only.

The `_meta.notes` field was updated to mention the re-run; `_meta.known_open_issues` retains the same two items as rev8 (`nazir_8` docx typo, marker-count discrepancy). `_meta.shape_review_decisions` preserved from prior revisions.

---

## 6. Files modified

| File | Action |
|---|---|
| `Mishnah-New/English/mishnah_db.json` | Promoted to rev9 (525 chapters, 10,405 markers, 0 missing) |
| `_pilot/MIGRATION-STATE.md` | Section 9 appended documenting this re-run |
| `_pilot/pass-6-rerun-report.md` | Created (this file) |
| `_pilot/mishnah_db_reextracted.json` | Staged file left in place (mount-blocked deletion); byte-identical to live |

The v2.1.4 extractor at `_pilot/mishnah_extractor_v2.py` was **not** modified in this run.

---

## 7. Anomalies

1. **Staged file deletion blocked** by the FUSE mount (same as the prior Pass 6 run). The file is byte-identical to the live promoted version, so leaving it is safe.
2. **`_meta.description`** still says "all 524 chapters" — carryover wording; `total_chapters` correctly reports 525.
3. **The three new chapters carry 0 markers each.** ketubot_14, yadayim_3, yadayim_4 are structurally complete but not yet colored in the docx. They will pick up markers automatically on the next re-extraction once styled text is added.

---

## 8. Pending git operations (for Moshe via GitHub Desktop)

Files for review and commit:

- `Mishnah-New/English/mishnah_db.json` (rev9)
- `_pilot/MIGRATION-STATE.md` (Section 9 appended)
- `_pilot/pass-6-rerun-report.md` (new)
- `_pilot/mishnah_db_reextracted.json` (staged copy; can be excluded or deleted manually)

The extractor source `_pilot/mishnah_extractor_v2.py` and Pass 6 first-run reports already in tree are unchanged this round.

No commits made. Cloudflare cache purge applies after deployment.
