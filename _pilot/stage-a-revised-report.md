# Stage A Revised Report — v2.1.3 Full Re-Extraction

**Date:** 2026-05-11
**Extractor:** `_pilot/mishnah_extractor_v2.py` v2.1.3
**Staged output:** `_pilot/mishnah_db_reextracted.json` (16.5 MB, 524 chapters)
**Status:** Full extraction completed. No live data modified.

This run replaces the halted v2.1.2 attempt. The precise two-condition header rule fired 13 times across 9 unique chapters (vs v2.1.2's 174 firings); the new tractate aliases resolved the 52 false-missing entries from the previous Stage A; and `nazir_8`'s docx typo is now tolerated. The remaining three missing-from-docx chapters (`ketubot_14`, `sukkah_3`, `yadayim_4`) match the Pass 3 investigation plus my own check that the docx sukkah series skips from chapter 2 to chapter 4.

---

## 1. v2.1.3 Changes Summary

### Fix 1 — Precise header-row rule (replaces v2.1.2's heuristic)

A 1-cell row is reclassified as a `header` on the next data row **iff both conditions hold**:

1. The wide row's cell label is a standalone row-number signal: an Arabic digit ≥ 2 (e.g. `"2"`, `"3"`, `"12"`) or a Hebrew-letter numeral representing ≥ 2 (e.g. `"ב"`, `"ג"`, `"טו"`). Explicitly excluded: `"1"`, `"א"`, anything with a column suffix like `"2א"`, anything not a clean numeric.
2. The next data row's cell labels all begin with that same row-number prefix.

If either fails, the wide row is preserved as a regular single-cell data row.

Implementation: `_classify_special_rows` in the extractor uses two helpers — `_parse_subunit_signal(label)` for condition 1 and `_parse_cell_label_row(label)` for condition 2 — both of which handle Arabic digits and Hebrew-letter numerals (1–49 covered).

### Fix 2 — Sequential row renumbering after header absorption

When the header rule fires, the wide row is dropped from `rows_data`, and remaining rows are renumbered 1, 2, 3, … to match the live JSON's convention. Cell `position.row` values are updated in lockstep with `row_num`.

### Fix 3 — Five new tractate aliases

`TRACTATE_NAMES` updated to produce the live JSON's compressed keys:

| Hebrew | v2.1.2 produced | v2.1.3 produces (matches live) |
|---|---|---|
| בבא קמא | bava_kamma | **bavakamma** |
| בבא מציעא | bava_metzia | **bavametzia** |
| בבא בתרא | bava_batra | **bavabatra** |
| אהלות | ohalot | **oholot** |
| ראש השנה | rosh_hashana | **rosh_hashanah** |

Also added: `אהילות` → `oholot` (alt spelling, defensive).

### Fix 4 — Tolerant header matching (covers nazir_8 docx typo)

The `build_table_index` matcher previously required `"מסכת"` in one header cell and `"פרק"` in the other. The docx's `nazir_8` table has `"סכת נזיר"` in c0 (missing the leading `מ`) which failed both standard and reversed matching. v2.1.3 falls back to: if one cell has `"פרק"` and the opposite cell contains a known tractate name, use that as the tractate cell. nazir_8 is now indexed correctly.

### Fix 5 — Enriched duplicate-table reporting

When `build_table_index` encounters two tables resolving to the same `(tractate_en, chapter_num)`, the `duplicates` list now records the table index, shape, cell count, and marker count for **both** the prior and the new occurrences, instead of only the new table's metadata.

### Version

`__version__ = "2.1.3"`. Canonical source at `_pilot/mishnah_extractor_v2.py`; a fresh-filename runtime copy at `/sessions/.../outputs/mishnah_ext_213.py` is used for bash execution because the FUSE mount caches the same-name file's pre-session content (a known sandbox quirk; the canonical file is the authoritative reference, visible via the file tools).

---

## 2. Verification Results — Five Known-Good Chapters

| Chapter | Expected behavior | v2.1.3 result | Verdict |
|---|---|---|---|
| `megillah_1` | byte-identical content to `_pilot/megillah_1_extracted.json` (62 markers, 7 subdivision cells) | shape `[[2,2],[1,2,1],[2,2],[1,2,1],[2,2]]`, 5 rows, 12 cells, 62 markers, 7 subdivided cells. **No header rule fired.** | **PASS** |
| `tahorot_1` | Header rule fires on docx row 2; resulting structure has 3 data rows with a `header` on row 2 (renumbered) | Header rule fired: signal=2, docx row 2 absorbed into docx row 3 (renumbered to logical row 2). Final shape `[[1,1,1],[1,1,1],[1,1,1]]`, 3 rows, 9 cells. Row 2 has `header: "2\n(ה) האכל שנטמא באב הטמאה ושנטמא בולד הטמאה\nמצטרפין זה עם זה לטמא כקל שבשניהן כיצד"`. | **PASS** |
| `berakhot_1` | Header rule must **NOT** fire (the wide mishnah-ג row contains content prefix `(ג)`, not a header signal); mishnah ג preserved as a real data row | No header rule fired. Wide single-cell row preserved as docx row 2 → renumbered to row 2 in output. Final shape `[[2,2],[4],[2,2]]`, 3 rows, 5 cells, 12 horizontal1 markers. Row 2's cell `label="2"`, `text` begins `"2\n(ג)\xa0בית שמאי אומרים בערב כל אדם יטו ויקראו ובבקר יעמדו…"` (full mishnah preserved). **The critical regression from v2.1.2 is fixed.** | **PASS** |
| `keritot_3` | Pass 4 v2.1.1 output: 2 rows, shape `[[2,2],[2,2]]`, 4 cells with A-D subdivisions | shape `[[2,2],[2,2]]`, 2 rows, 4 cells, 4 subdivided cells, 0 markers. No header rule fired. | **PASS** |
| `yevamot_2` | 15 horizontal1 markers across 5×2 shape | shape `[[2,2]]×5`, 5 rows, 10 cells, 15 horizontal1 markers, 2 subdivided cells. No header rule fired. | **PASS** |

**Berakhot_1 deep-dive (the critical confirmation).** The previous Stage A halted because v2.1.2's MIDDLE classifier silently re-cast mishnah ג as a header, dropping it as cell content. Under v2.1.3:

- Wide row 2's cell has `label="2"` (the Subunit row-number signal).
- The next data row (docx row 3) has cell labels `["3א", "3ב"]`.
- `_parse_cell_label_row("3א") = 3`, which ≠ signal `2` → **condition 2 fails → rule does not fire**.
- The wide row is preserved as the second data row in the output, with the full mishnah-ג text and all `horizontal1` markers intact.

A divergence note: v2.1.3 produces 3 rows for berakhot_1, while the live JSON entry has 5 rows (shape `[[2,2],[1,2,1],[2,2],[1,2,1],[2,2]]`). The docx in its current form has only 3 data rows for berakhot_1; the live JSON's 5-row structure comes from an earlier extraction pass over a different docx state (or manual editing). Per MIGRATION-STATE.md the docx is the authoritative source, so the 3-row output is structurally correct. The fact that the wide mishnah-ג row remains a wide single-cell row (with colspan 4) — rather than being silently absorbed — is what the verification was meant to confirm.

---

## 3. Full Extraction Statistics

| Metric | Value |
|---|---|
| Total chapters in output | 524 |
| Matched chapters | 521 |
| Missing-from-docx (placeholders) | 3 (`ketubot_14`, `sukkah_3`, `yadayim_4`) |
| Chapters with markers | 307 |
| Total markers | 10,341 |
| Cells with subdivisions | 1,588 |
| Chapters with a `header` field on any row | 9 (13 total firings — `avot_1` has 5) |
| Duplicate-table chapter keys | 6 |
| Output file size | 16,529,972 bytes |
| Extraction wall time | 6.1 seconds |

### Marker-type breakdown

| Type | Live (rev7) | Staged (rev2.1.3) | Delta |
|---|---:|---:|---:|
| horizontal1 | 3,439 | 5,137 | +1,698 |
| internalparallel | 1,793 | 2,455 | +662 |
| vertical1 | 869 | 1,373 | +504 |
| horizontal2 | 364 | 541 | +177 |
| horizontal3 | 340 | 523 | +183 |
| closure | 140 | 157 | +17 |
| ciasm1 | 40 | 83 | +43 |
| ciasm2 | 35 | 72 | +37 |
| **Total** | **7,020** | **10,341** | **+3,321** |

### Headline deltas vs live rev7

| Metric | Live (rev7) | Staged | Delta |
|---|---:|---:|---:|
| Chapters with markers | 297 | 307 | +10 |
| Total markers | 7,020 | 10,341 | **+3,321 (+47%)** |
| Chapters with a `header` field | 1 (tahorot_1) | 9 | +8 |
| Chapters marked missing-from-docx | 0 | 3 | +3 |
| Duplicate-table chapter keys (in docx) | 6 (known) | 6 | (same six) |

### Per-chapter marker deltas

| Bucket | Count |
|---|---:|
| Marker count unchanged | 354 |
| Marker count changed | 170 |
| → Gained markers (staged > live) | 168 chapters, **+3,343** markers cumulative |
| → Lost markers (staged < live) | 2 chapters, **−22** markers cumulative |

**Top gainers (>50 net markers each):**

| Chapter | Live | Staged | Δ |
|---|---:|---:|---:|
| orlah_2 | 19 | 110 | +91 |
| eruvin_10 | 51 | 124 | +73 |
| ketubot_2 | 54 | 123 | +69 |
| bavabatra_10 | 42 | 102 | +60 |
| bavametzia_9 | 26 | 82 | +56 |
| makkot_1 | 0 | 56 | +56 |
| sanhedrin_1 | 0 | 56 | +56 |
| terumot_8 | 10 | 64 | +54 |
| shevuot_3 | 0 | 53 | +53 |
| makkot_3 | 0 | 50 | +50 |
| sanhedrin_10 | 3 | 51 | +48 |
| bavabatra_2 | 32 | 79 | +47 |
| maaser_sheni_1 | 11 | 58 | +47 |
| sanhedrin_7 | 0 | 47 | +47 |

**The two losers:**

| Chapter | Live | Staged | Δ | Note |
|---|---:|---:|---:|---|
| sukkah_3 | 12 | 0 | −12 | Genuinely missing from the current docx (docx skips from sukkah ch.2 to ch.4) — staged is a placeholder. The 12 live markers are at risk if we promote without preservation. |
| shabbat_22 | 10 | 0 | −10 | Two duplicate tables in docx: ti=110 (10 markers) and ti=111 (0 markers). `build_table_index` keeps the later one (ti=111). The live JSON's 10 markers came from ti=110. Stage B decision: pick which docx table is canonical. |

The Group E chapters (the 17 the Pass 3.6 review labelled "title-row pattern") are no longer left empty — v2.1.3 extracts them from the docx, and most now have substantial markers (makkot_1: 56, sanhedrin_1: 56, sanhedrin_7: 47, shevuot_3: 53, makkot_3: 50, etc.).

---

## 4. Header-Rule Firing Log

The precise rule fired 13 times across 9 unique chapters. Each firing shows: chapter, table index, signal (the row-number on the wide row), absorbed-into row in the output, and a preview of the header text.

| Chapter | ti | Signal | Wide row | Target row | Header preview |
|---|---:|---:|---:|---:|---|
| `avot_1` | 316 | 2 | 2 | 3 | `2 (ד) יוסי בן יועזר איש צרדה ויוסי בן יוחנן איש ירושלים קבלו מהם` |
| `avot_1` | 316 | 3 | 4 | 5 | `3 (ו) יהושע בן פרחיה ונתאי הארבלי קבלו מהם` |
| `avot_1` | 316 | 4 | 6 | 7 | `4 (ח) יהודה בן טבאי ושמעון בן שטח קבלו מהם` |
| `avot_1` | 316 | 5 | 8 | 9 | `5 (י) שמעיה ואבטליון קבלו מהם` |
| `avot_1` | 316 | 6 | 10 | 11 | `6 (יב) הלל ושמאי קבלו מהם` |
| `avot_2` | 317 | 4 | 4 | 5 | `4 (ח) רבן יוחנן בן זכאי קבל מהלל ומשמאי הוא היה אומר אם למדת תורה הרבה` |
| `beitzah_5` | 159 | 2 | 2 | 3 | `2 (ב) כל שחיבין עליו משום שבות משום רשות משום מצוה בשבת חיבין עליו ביו` |
| `kilayim_1` | 39 | 3 | 3 | 4 | `3 (ז) אין מביאין אילן באילן ירק בירק ולא אילן בירק ולא ירק באילן רבי י` |
| `meilah_1` | 396 | 3 | 3 | 4 | `3 (ד) מעשה דמים בקדשי קדשים להקל ולהחמיר ובקדשים קלים כלו להחמיר כיצד` |
| `middot_5` | 415 | 2 | 3 | 4 | `2 (ג) שש לשכות היו בעזרה שלש בצפון ושלש בדרום` |
| `sanhedrin_7` | 287 | 2 | 3 | 4 | `2 (ד) אלו הן הנסקלין הבא על האם ועל אשת האב ועל הכלה ועל הזכור ועל הבה` |
| `shabbat_7` | 95 | 2 | 2 | 3 | `2 (ב) אבות מלאכות ארבעים חסר אחת` |
| `tahorot_1` | 494 | 2 | 2 | 3 | `2 (ה) האכל שנטמא באב הטמאה ושנטמא בולד הטמאה מצטרפין זה עם זה לטמא כקל` |

Every firing has the wide row's Subunit text matching the next data row's cell-label prefix. The 5 firings in `avot_1` reflect the chain-of-tradition structure (Pirkei Avot 1 has alternating header/content pairs for each generation), and they are exactly what one would expect for that chapter. The other 8 firings are individual section-headers introducing the next row of structured material.

---

## 5. nazir_8 and sukkah_3 Investigation

### nazir_8 — resolved

The docx table at index 226 has `c0 = "סכת נזיר"` (missing the leading `מ` in `מסכת`) and `cl = "פרק ח"`. The strict v2.1.2 matcher rejected this because neither standard nor reversed matching matched. v2.1.3's tolerant matcher checks: if `"פרק"` is present in one header cell and `_match_tractate` returns a known tractate name from the opposite cell, use that. `_match_tractate("סכת נזיר")` returns `"nazir"` (the substring `"נזיר"` matches the TRACTATE_NAMES dict). nazir_8 is now indexed correctly and extracted with 0 markers (the chapter has no styled text in the current docx).

The typo is in the docx itself. Suggested separate task: fix the typo in the docx so the strict matcher would also find it.

### sukkah_3 — genuinely missing

The docx contains sukkah tables for chapters 1 (ti=151), 2 (ti=152), 4 (ti=153), and 5 (ti=154). Chapter 3 is **absent** from the docx — the docx skips directly from chapter 2 to chapter 4. v2.1.3 correctly emits a placeholder with `_missing_from_docx: true`. The live JSON entry for `sukkah_3` (12 markers) was populated from a prior docx version or other source. If the current docx is the authoritative source, the live entry's content needs to be moved into the docx before any future re-extraction; if the live entry is correct, sukkah_3 is a "Group F: extractor can't match" case (analogous to `ketubot_14` and `yadayim_4` from Pass 3).

---

## 6. Duplicate-Table Confirmation

All 6 known duplicates from the previous Stage A are present, with enriched metadata for review:

| Key | Prior (ti) shape / cells / markers | New (ti) shape / cells / markers | Notes |
|---|---|---|---|
| `shabbat_22` | ti=110: `[[2,2],[2,2],[2,2]]`, 6 cells, 10 markers | ti=111: `[[2,2],[2,2],[2,2],[2,2]]`, 8 cells, 0 markers | ti=110 carries the markers; ti=111 has an extra row but no styling. |
| `sotah_9` | ti=236 (`פרק ט חלק א`): `[[2,2]]×4`, 8 cells, 36 markers | ti=237 (`פרק ט חלק ב`): `[[1,1,1]]×4`, 12 cells, 55 markers | The docx splits sotah ch.9 into two halves (`חלק א` / `חלק ב`); the matcher conflates them. Should arguably be `sotah_9a` and `sotah_9b`, or merged into a 20-cell `sotah_9`. |
| `zevachim_5` | ti=329: `[[1,2,1],[2,2],[1,2,1]]`, 8 cells, 0 markers | ti=330: `[[4],[2,2],[1,2,1],[2,2],[4]]`, 9 cells, 0 markers | Two structurally different layouts; both no markers. |
| `middot_1` | ti=409: `[[1,2,1],[4],[2,2],[4],[1,2,1]]`, 10 cells, 18 markers | ti=410: `[[1,1,1]]×3`, 9 cells, 16 markers | Both have content — different chapter layouts. |
| `middot_2` | ti=411: `[[1,2,1],[4],[2,2],[4],[1,2,1]]`, 10 cells, 14 markers | ti=412: `[[2,2]]×5`, 10 cells, 57 markers | Significant divergence in marker count; ti=412 has nearly 6× the markers and a different shape. |
| `kelim_4` | ti=422: `[[2,2],[2,2]]`, 4 cells, 0 markers | ti=423: `[[1,1,1],[1,1,1]]`, 6 cells, 0 markers | Both empty. |

Last-write-wins behavior unchanged: the new (later) table is kept in the index. Stage B/C should decide per-key which docx table is canonical, or whether some pairs (e.g., sotah_9) should be split into two JSON keys.

### v2.1.2 ↔ v2.1.3 reconciliation

Previous Stage A reported `shape` of ti=329 zevachim_5 as `[[1,2,1],[2,2],[1,2,1]]` and ti=330 as `[[2,2],[1,2,1],[2,2]]`. v2.1.3 reports ti=330 as `[[4],[2,2],[1,2,1],[2,2],[4]]`. The difference: v2.1.2's classifier was absorbing two wide rows in ti=330 (TOP and BOTTOM firings), which v2.1.3 correctly leaves in place because their Subunit signals don't match the adjacent rows' cell-label prefixes. The 5-row structure with two wide `[4]` rows is the true docx shape for ti=330.

---

## 7. Anomalies

1. **Significant marker increase (+47%) over the live JSON.** 168 chapters gained markers, totalling +3,343. This is consistent with the dataset's known provenance issues (the live JSON accumulated through multiple passes over different docx states). The docx in its current form contains substantially more highlighted text than what was previously extracted. Stage B should reconcile per chapter.

2. **shabbat_22 marker loss.** The duplicate-table policy (last-write-wins) caused the 10-marker version (ti=110) to be replaced by the 0-marker version (ti=111). If this is undesirable, change the policy to first-write-wins or pick by marker count.

3. **sukkah_3 marker loss.** Genuinely missing from the current docx; the 12 live markers will be lost on promotion unless preserved.

4. **Group E chapters now populated.** The 17 chapters that Pass 3.6 left as empty (`_meta.shape_review_decisions`) all now have proper extraction (most with non-zero markers). Stage B should decide whether the new shapes match the Pass 3.6 intent or whether the original "JSON current" decisions should be reapplied.

5. **avot_1 has 5 header firings.** Pirkei Avot chapter 1 follows a clear chain-of-tradition pattern: a header introduces each pair of sages, followed by their saying as a structured row. The rule correctly identifies each header. avot_1's `chapters_with_header_row` count contributes 5 to the global 13.

6. **Cell labels appearing as `"6"` (just digit, no column suffix).** In avot_2 row 8, both cells in a multi-cell row have label `"6"`. The label gets the Subunit text from the first run. Not an extractor bug — just a quirk of the docx's label scheme. Stage B should decide whether to normalise these.

---

## 8. Files Touched

| File | Action |
|---|---|
| `_pilot/mishnah_extractor_v2.py` | Updated to v2.1.3. Canonical save location. (Bash sees a stale cached version due to a known FUSE-mount caching quirk; the canonical content is reachable via the file tools or via the runtime copy.) |
| `_pilot/mishnah_db_reextracted.json` | Created (16.5 MB, 524 chapter entries + `_meta`). The staged candidate dataset for Stage B's diff. |
| `_pilot/stage-a-revised-report.md` | Created (this file). |

**Not modified:**
- `Mishnah-New/English/mishnah_db.json` (live, untouched per task spec).
- `_pilot/stage-a-report.md` (the previous halted Stage A's report; kept as historical record).

---

## 9. Next Steps

Per the task spec, Stage B (comprehensive diff against live JSON) and Stage C (per-category apply decisions) are the next phases. The 170 chapters with marker-count changes are the diff hot-spots. Open per-chapter questions for Stage B/C:

- For the 168 marker-gainers: do we promote the staged content, or did the live entries reflect intentional pre-extraction edits that should be preserved?
- For the 2 marker-losers: keep the live entries (sukkah_3, shabbat_22) or accept the docx outcome?
- For the 6 duplicate-table keys: pick one docx table as canonical per key, or split into multiple JSON keys (sotah_9)?
- For the 17 Group E chapters now populated: accept the v2.1.3 extraction, or restore the Pass 3.6 "JSON current" / placeholder treatment?
- For nazir_8: fix the docx typo upstream so the strict matcher would also pick it up?
- For tahorot_1's header text: live JSON starts the header with `"2\n"`; v2.1.3 also starts with `"2\n"` because that's the Subunit row-number text. Should the leading row-number be stripped from the header in a follow-up clean-up?

Awaiting Moshe's review.
