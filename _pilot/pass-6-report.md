# Pass 6 Report — Extractor v2.1.4 + Re-extract + Promote

**Date:** 2026-05-11
**Extractor:** `_pilot/mishnah_extractor_v2.py` v2.1.4
**Live dataset:** `Mishnah-New/English/mishnah_db.json`, promoted to `_meta.version: "2026-05-rev8"`
**Status:** Validation passed, promotion completed, live byte-identical to staged.

---

## 1. v2.1.4 Changes Summary

### Fix 1 — `TABLE_OVERRIDES` (per-chapter table pinning)

Module-level constant:

```python
TABLE_OVERRIDES = {
    "shabbat_22": "ti=110",  # earlier of two tables (defensive — duplicate gone in current docx)
}
```

When `build_table_index` encounters a duplicate `(tractate, chap)` key, it consults `TABLE_OVERRIDES` before falling back to last-write-wins. If the override target (`"ti=N"`) matches either the current or prior occurrence, that table is kept. Otherwise the safe fallback (last-write-wins) is preserved.

The new docx no longer has a duplicate for shabbat_22 (the earlier 0-marker table was removed upstream), so the override is effectively defensive in this Pass. It remains in the code so a future docx edit that re-introduces a duplicate would still pick the right table.

### Fix 2 — sotah_9 split

In `build_table_index`, after matching `(eng, chap_num) == ("sotah", 9)`, the matcher inspects `chapter_text` for `חלק א` / `חלק ב`:

- `חלק א` → keyed as `sotah_9a`
- `חלק ב` → keyed as `sotah_9b`
- Neither → key as the unified `sotah_9` (fallback, not expected to fire)

In `extract_all_chapters_from_json`, the live JSON's `sotah_9` key is intentionally skipped (no placeholder emitted). After the main pass, fresh `sotah_9a` and `sotah_9b` entries are appended, inheriting `tractate_he/en`, `seder_he/en`, `chapter_num`, `chapter_he`, and `source_url` from the live `sotah_9` entry, with a new `chapter_part_he` field set to `"חלק א"` or `"חלק ב"` respectively.

### Fix 3 — Version bump

```python
__version__ = "2.1.4"
```

Saved to canonical `_pilot/mishnah_extractor_v2.py`. The bash-runnable runtime copy is at `/sessions/.../outputs/mishnah_ext_214.py` (fresh filename to bypass FUSE mount caching of same-name files).

---

## 2. Verification Results — Eight Key Chapters

All 8 verifications pass against the updated docx.

| Chapter | Expected | v2.1.4 actual | Verdict |
|---|---|---|---|
| `megillah_1` | byte-identical to live (62 markers, no firing) | shape `[[2,2],[1,2,1],[2,2],[1,2,1],[2,2]]`, 62 markers, no header firing | **PASS** |
| `berakhot_1` | rule must NOT fire (mishnah-ג row preserved) | shape `[[2,2],[4],[2,2]]`, wide row 2 has the full mishnah-ג text + 12 horizontal1 markers; no firing | **PASS** |
| `tahorot_1` | rule fires on row 2; header attached | signal=2, row 2 absorbed → header on row 2 (renumbered); shape `[[1,1,1],[1,1,1],[1,1,1]]` | **PASS** |
| `shabbat_22` | match ti=110, 3×2, 10 markers | ti=110, shape `[[2,2],[2,2],[2,2]]`, 10 markers | **PASS** |
| `zevachim_5` | shape `[1,2,3,2,1]` (palindrome cells per row) | shape `[[4],[2,2],[1,2,1],[2,2],[4]]` — palindrome `[1,2,3,2,1]` cells per row | **PASS** |
| `sukkah_3` | must have content, not placeholder | shape `[[1,1,1],[1,1,1],[1,1,1]]`, 18 horizontal1 markers, 9 subdivided cells | **PASS** |
| `sotah_9` | must NOT exist in output | absent from index, absent from results dict | **PASS** |
| `sotah_9a` / `sotah_9b` | present with chapter_part_he | `sotah_9a` shape `[[2,2]]×4`, 36 markers, `chapter_part_he="חלק א"`; `sotah_9b` shape `[[1,1,1]]×4`, 55 markers, `chapter_part_he="חלק ב"` | **PASS** |

### Critical regression check — berakhot_1

The previous Stage A halted because v2.1.2 was misclassifying berakhot_1's wide mishnah-ג row as a header. v2.1.4 preserves the v2.1.3 fix: wide row 2's cell label is `"2"` (signal=2) but the next data row's cells are labelled `"3א"`, `"3ב"` (row-prefix 3) — mismatch, rule does not fire, content preserved. The cell `text` begins `"2\n(ג)\xa0בית שמאי אומרים\nבערב כל אדם יטו ויקראו ובבקר יעמדו…"` and carries all 12 `horizontal1` markers.

---

## 3. Full Extraction Statistics

```
total_chapters:           525  (524 + sotah_9a/b − sotah_9)
matched_chapters:         523
missing_chapters:         2    (ketubot_14, yadayim_4)
markers_populated_count:  310
total_markers:            10,405
cells_with_subdivisions:  1,599
chapters_with_header_row: 13 firings across 9 unique chapters
extractor_version:        2.1.4
extraction_wall_time:     5.4s
staged_file_size:         16,616,285 bytes
```

### Marker counts by type

| Type | Count |
|---|---:|
| horizontal1 | 5,179 |
| internalparallel | 2,477 |
| vertical1 | 1,373 |
| horizontal2 | 541 |
| horizontal3 | 523 |
| closure | 157 |
| ciasm1 | 83 |
| ciasm2 | 72 |
| **Total** | **10,405** |

---

## 4. Rev7 → Rev8 Deltas

| Metric | rev7 (live before) | rev8 (live now) | Δ |
|---|---:|---:|---:|
| Total chapters | 524 | 525 | +1 (sotah split) |
| Chapters with markers | 297 | 310 | +13 |
| Total markers | 7,020 | 10,405 | **+3,385** |
| Chapters with `header` field | 1 (tahorot_1) | 9 | +8 |
| Missing-from-docx | 0 in `_meta`; 3 in practice (ketubot_14, sukkah_3, yadayim_4) | 2 explicitly (ketubot_14, yadayim_4) | sukkah_3 restored |
| Duplicate-table chapters | 6 (acknowledged) | 0 (all upstream-fixed) | −6 |

### Marker-type deltas

| Type | rev7 | rev8 | Δ |
|---|---:|---:|---:|
| horizontal1 | 3,439 | 5,179 | +1,740 |
| internalparallel | 1,793 | 2,477 | +684 |
| vertical1 | 869 | 1,373 | +504 |
| horizontal2 | 364 | 541 | +177 |
| horizontal3 | 340 | 523 | +183 |
| closure | 140 | 157 | +17 |
| ciasm1 | 40 | 83 | +43 |
| ciasm2 | 35 | 72 | +37 |
| **Total** | **7,020** | **10,405** | **+3,385** |

Mostly horizontal1, internalparallel, and vertical1 — consistent with the docx having gained large numbers of standard structural markers across many chapters since rev7's source state.

---

## 5. Validation Results

All 10 checklist items PASS:

1. **JSON parses cleanly** — OK
2. **Exactly 526 top-level keys** — got 526 (525 chapters + `_meta`)
3. **`sotah_9` NOT present** — absent
4. **`sotah_9a` and `sotah_9b` present with content** — both have 4 rows
5. **`shabbat_22` has 10 markers** — got 10
6. **`zevachim_5` shape `[1,2,3,2,1]`** (cells per row) — got `[1,2,3,2,1]`, full shape `[[4],[2,2],[1,2,1],[2,2],[4]]`
7. **`sukkah_3` has content, not placeholder** — 3 rows, no `_missing_from_docx` flag
8. **`_meta.version == "2026-05-rev8"`** — confirmed
9. **All marker types are the 8 canonical** — no `internal_parallel`/`chiastic1`/`chiastic2` found
10. **Total marker count reasonable** (within 9,500–11,000 envelope around v2.1.3's 10,341 baseline) — got 10,405

---

## 6. Promotion Confirmation

- **Pre-promotion:** live size 7,373,272 bytes, sha256 `af6ddae188d19d1c…`
- **Staged:** size 16,616,285 bytes, sha256 `5844f7a9c5792144…`
- **Post-promotion:** live size 16,616,285 bytes, sha256 `5844f7a9c5792144…`
- **Byte-identity:** confirmed (sha256 matches exactly)
- **Re-parse after promotion:** OK, 526 top-level keys, `_meta.version == "2026-05-rev8"`
- **Staged file cleanup:** `_pilot/mishnah_db_reextracted.json` deletion attempted but rejected by the FUSE mount (permissions). The staged file is byte-identical to the live and can be safely deleted manually via Windows Explorer.

---

## 7. Files Modified

| File | Action |
|---|---|
| `_pilot/mishnah_extractor_v2.py` | Updated to v2.1.4 (canonical). Note: the bash mount caches the pre-session content; the canonical content is reachable via the file tools or the runtime copy at `/sessions/.../outputs/mishnah_ext_214.py`. |
| `Mishnah-New/English/mishnah_db.json` | Promoted to rev8 (525 chapters, 10,405 markers). |
| `_pilot/MIGRATION-STATE.md` | Section 8 (Pass 6) appended documenting the changes, decisions, and known open issues. |
| `_pilot/pass-6-report.md` | Created (this file). |
| `_pilot/stage-a-revised-report.md` | Pre-existing — confirmed in tree from the prior Pass 5 / Stage A revised work. |
| `_pilot/stage-a-report.md` | Pre-existing historical record of the halted v2.1.2 attempt. |
| `_pilot/mishnah_db_reextracted.json` | Staged file left in place (mount rejected deletion). Identical to live; safe to delete manually. |

---

## 8. Anomalies

1. **`_meta.description` mentions "524 chapters"** — carried forward from rev7's description; now superseded by 525 entries after the sotah split. Minor wording — `total_chapters` in `_meta` correctly reports 525.

2. **Staged file cleanup blocked.** `os.remove(...)` from the bash sandbox failed with `Operation not permitted`. The file is byte-identical to the live, so leaving it is safe; Moshe can delete via Windows Explorer.

3. **Three "Group E from Pass 3.6" chapters still empty.** `bekhorot_8`, `niddah_3`, `temurah_7`, `yadayim_3`, `zevachim_5`, `zevachim_6` — these have docx structure but no styled text in the current docx, so they extract with 0 markers. Their `shape_review_decisions` entries are preserved in `_meta` as historical context.

4. **`sotah_9a` source_url and `sotah_9b` source_url** both inherit from the original `sotah_9` entry. If Moshe wants distinct URLs for the two halves later, they'll need a manual update in the JSON.

5. **`311 vs 297` marker-count discrepancy** noted in `_meta.known_open_issues`. The rev8 dataset has 310 chapters with markers — closer to the 311 Claude-in-Word figure but still off by 1. Deferred for separate investigation.

6. **`nazir_8` docx typo (`סכת נזיר`)** noted in `_meta.known_open_issues`. The tolerant matcher introduced in v2.1.3 handles it via fallback (the cell contains a known tractate name even without the `מסכת` prefix). Should be fixed upstream in the docx when convenient.

---

## 9. Pending git operations (for Moshe via GitHub Desktop)

Files staged for review and commit:

- `_pilot/mishnah_extractor_v2.py` (v2.1.4)
- `Mishnah-New/English/mishnah_db.json` (rev8)
- `_pilot/MIGRATION-STATE.md` (Section 8 appended)
- `_pilot/pass-6-report.md` (new)
- `_pilot/stage-a-revised-report.md` (already in tree)
- `_pilot/stage-a-report.md` (already in tree)
- `_pilot/mishnah_db_reextracted.json` (staged copy; can be excluded from commit or deleted manually)

No commits made. Cloudflare cache will need a purge after deployment.
