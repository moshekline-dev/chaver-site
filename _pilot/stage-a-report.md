# Stage A Report — v2.1.2 Re-Extraction (HALTED AT VERIFICATION)

**Date:** 2026-05-11
**Extractor:** `_pilot/mishnah_extractor_v2.py` v2.1.2
**Status:** **Stopped at Step 2 (verification) per task instructions** — heuristics over-fire and key-name aliasing is incomplete. Full 524-chapter re-extraction was **not** run.

The canonical extractor file on disk has been bumped to v2.1.2 and contains both new behaviors. Because the FUSE mount serving the bash sandbox caches the pre-session content of files in `chaver-site/_pilot/`, a fresh runnable copy was placed at `/sessions/.../mnt/outputs/mishnah_extractor_v2.py` and all verification runs used that copy. The two files are identical content; only the canonical path's bash-side view is stale.

---

## 1. v2.1.2 Changes Summary

### Fix 1 — Header-row classifier (`_classify_special_rows`)

A docx data row containing exactly one cell is reclassified by its position relative to multi-cell ("data") rows in the same table. The classifier only fires when the table has at least one multi-cell row.

| Position | Action |
|---|---|
| TOP (no multi-cell row before it) | Prepend text/runs/markers into the first cell of the next data row, drop the 1-cell row. |
| MIDDLE (multi-cell rows both before and after) | Emit the 1-cell row's text as a `header` property on the next data row, drop the 1-cell row. |
| BOTTOM (no multi-cell row after it) | Append into the last cell of the preceding data row; log as anomaly. |

Each firing is logged to `_classifier_log` on the returned chapter dict (transient field; the caller strips it before persistence).

### Fix 2 — Graceful missing-chapter handling

`extract_all_chapters_from_json(docx_path, live_json_path)`:

- Iterates the keys of the live `mishnah_db.json` (excluding `_meta`).
- For each key, looks up `(tractate_en, chapter_num)` in a pre-built docx table index.
- If matched, runs `extract_chapter()` and merges in metadata (`tractate_en`, `seder_he`, `seder_en`, `chapter_num`, `source_url`) from the live entry.
- If unmatched, emits a placeholder dict preserving the live entry's metadata, with `shape: []`, `rows: []`, `_missing_from_docx: true`.

### New helper — `build_table_index(doc)`

Pre-indexes all docx tables by `(tractate_en, chapter_num)`. Handles both standard-header and reversed-header layouts. Records any duplicate `(tractate_en, chapter_num)` keys to a `duplicates` list (last-write-wins behavior in the index itself).

### New CLI mode — `--from-json`

```
python mishnah_extractor_v2.py <docx> --from-json <live.json> <out.json>
```

Drives full corpus extraction from the JSON. The output payload includes a `_meta` block with summary statistics, the classifier log per chapter, and the duplicates list.

### Version bump

```
__version__ = "2.1.2"
```

---

## 2. Verification Results — Six Known-Good Chapters

| Chapter | Task expectation | v2.1.2 actual | Verdict |
|---|---|---|---|
| `megillah_1` | byte-identical to live entry (50 markers, 7 subdivision cells per the task; live entry actually has 62 markers, 7 subdivision cells) | shape `[[2,2],[1,2,1],[2,2],[1,2,1],[2,2]]`, 5 rows, 62 markers, 7 subdivided cells. **No classifier firing.** Matches the existing `_pilot/megillah_1_extracted.json` (v2.1.1 output) structurally. | **PASS** (task's "50 markers" number is stale; correct number is 62 and that matches v2.1.1 output and the live entry) |
| `tahorot_1` | `header` field on row 2 with expected Hebrew | MIDDLE fired on docx row 2 → header attached to docx row 3 (the next data row after the 1-cell row was absorbed). Final shape `[[1,1,1],[1,1,1],[1,1,1]]`, 0 markers. **Note:** v2.1.2 preserves docx `row_num` after drops; the live JSON has rows renumbered 1/2/3 with header on row 2. Renumbering is not part of the spec. | **Heuristic fires correctly** but row numbering differs from live by design |
| `keritot_3` | shape `[[2,2],[2,2]]`, 4 cells with A-D subdivisions, full text | shape `[[2,2],[2,2]]`, 4 cells, 4 subdivided cells, 0 markers | **PASS** |
| `kinnim_1` | shape `[[1,1,1],[1,1,1]]`, 6 cells, 4 with A-B-C subdivisions | shape `[[1,1,1],[1,1,1]]`, 6 cells, 4 subdivided cells, 0 markers | **PASS** |
| `yevamot_2` | 15 horizontal1 markers across 2×5 shape | shape `[[2,2]]×5`, 5 rows × 2 cells, 15 horizontal1 markers | **PASS** |
| `berakhot_1` | match existing JSON entry (live: 5 rows, shape `[[2,2],[1,2,1],[2,2],[1,2,1],[2,2]]`) | shape `[[2,2],[2,2]]`, 2 rows, 12 horizontal1 markers. **Classifier fired MIDDLE on docx row 2** — the row containing mishnah ג ("בית שמאי אומרים…") was reclassified as a header on row 3, dropping its content as a real data row. | **FAIL** — heuristic over-fires |

The berakhot_1 result is the trigger for the Step-2 stop. Mishnah ג is genuine content (a full-width data row in the current docx), not a header — but the position-based heuristic cannot distinguish "title/header text" from "wide-format mishnah".

---

## 3. Survey — Classifier Behavior Across All 520 Indexed Chapters

To understand the scale, I ran the v2.1.2 classifier across every indexed docx table without writing the output. The classifier fires far more often than the task spec anticipated:

| Classification | Task expected (approximate) | v2.1.2 actual (chapters where the firing-type occurs at least once) |
|---|---|---|
| TOP — title-row pattern | 17 (Group E from Pass 3.6) | **69** |
| MIDDLE — header in middle | 1 (tahorot_1) | **49** |
| BOTTOM — rare fallback anomaly | "rare" | **56** |
| Chapters with multiple classifications | — | **59** |

### Group E coverage check

Of the 17 chapters Pass 3.6 documented as "title-row pattern" in `_meta.shape_review_decisions`, **only 10 fire TOP under v2.1.2**:

- Fired TOP: `avot_2`, `bekhorot_8`, `makkot_1`, `makkot_2`, `makkot_3`, `sanhedrin_7`, `sanhedrin_11`, `shevuot_6`, `shevuot_8`, `zevachim_5`
- Did **not** fire TOP: `meilah_1`, `niddah_3`, `sanhedrin_1`, `shevuot_3`, `temurah_7`, `yadayim_3`, `zevachim_6`

Some of the 7 misses fire BOTTOM instead (e.g., `meilah_1`) because the docx structure for those chapters places their 1-cell row at the bottom of the table rather than the top. The heuristic does not recognize them as title rows.

### Sample MIDDLE firings beyond tahorot_1

The MIDDLE classification fires on chapters where a mishnah is laid out as a full-width row — not as a header. Examples (with first ~80 chars of the text that gets re-cast as a header):

- `berakhot_1`: "(ג) בית שמאי אומרים בערב כל אדם יטו ויקראו ובבקר יעמדו…"
- `berakhot_7`: "(ג) כיצד מזמנין בשלשה אומר נברך…"
- `bava_kamma_1`: "(ג) שום כסף ושוה כסף בפני בית דין ועל פי עדים…"
- `eduyot_2`: "(ו) שלשה דברים אמר רבי ישמעאל ולא הודה לו רבי עקיבא…"
- `nedarim_1`: "(ב) האומר לחברו קונם קונח קונס הרי אלו כנויין לקרבן…"
- `pesachim_3`: "בצק החרש אם יש כיוצא בו שהחמיץ הרי זה אסור"
- `sanhedrin_7`: "(ד) אלו הן הנסקלין הבא על האם…"
- `shabbat_7`: "(ב) אבות מלאכות ארבעים חסר אחת"
- `tahorot_3`, `tahorot_8`, `tahorot_9`: numbered mishnayot

Many of these clearly contain mishnah numbering `(ב)`, `(ג)`, `(ד)`, etc. — they are content, not section headers. Treating them as headers loses the content from cell text.

### Sample BOTTOM firings

BOTTOM is supposed to be a "rare" anomaly. It fires 56 times in the current docx. Examples:

- `taanit_1`: "יצא ניסן וירדו גשמים סימן קללה שנאמר…"
- `taanit_4`: "(ח) אמר רבן שמעון בן גמליאל לא היו ימים טובים לישראל…"
- `meilah_1`: "נמצא מעשה דמים בקדשי קדשים להקל ולהחמיר…"
- `niddah_8`: "(ד) עד שהוא נתון תחת הכר ונמצא עליו דם…"

These appear to be summary or coda paragraphs at the bottom of the chapter — distinct content, not a fallback merge candidate. Applying the heuristic appends them to the last cell of the preceding row, where they would render as part of a different mishnah.

---

## 4. Anomaly — 52 Live-JSON Keys Don't Match Indexed Docx Keys

This is independent of the classifier and is a pre-existing extractor issue surfaced by the new from-json driver.

The current `TRACTATE_NAMES` mapping produces snake-case English keys that don't match the live JSON's compressed keys for five tractates:

| Hebrew | Extractor produces | Live JSON uses |
|---|---|---|
| בבא קמא | `bava_kamma` | `bavakamma` |
| בבא מציעא | `bava_metzia` | `bavametzia` |
| בבא בתרא | `bava_batra` | `bavabatra` |
| אהלות | `ohalot` | `oholot` |
| ראש השנה | `rosh_hashana` | `rosh_hashanah` |

This produces **52 false missing-from-docx flags**:

- bava_kamma 1–10 (10) + bavametzia 1–10 (10) + bavabatra 1–10 (10) + oholot 1–18 (18) + rosh_hashanah 1–4 (4) = 52

Combined with the two truly missing chapters from Pass 3 (`ketubot_14`, `yadayim_4`) and two more that turned up here (`nazir_8`, `sukkah_3`), the unmatched-live-JSON-keys total is 56. Stage A as written would mark all 56 as `_missing_from_docx: true` even though docx tables exist for 52 of them.

`nazir_8` and `sukkah_3` warrant separate investigation — they aren't on the Pass 3 missing list and may indicate a docx table that exists but fails matching for some other reason (e.g., header-cell text doesn't follow the standard pattern).

---

## 5. Anomaly — Six Duplicate-Key Docx Tables

The docx contains two tables that the matcher resolves to the same `(tractate_en, chapter_num)` key:

| Key | Tables | Notes |
|---|---|---|
| `shabbat_22` | ti=110 (10 markers, [[2,2],[2,2],[2,2]]) vs ti=111 (0 markers, [[2,2],[2,2],[2,2],[2,2]]) | Two variants with different row counts; ti=110 has content, ti=111 doesn't. |
| `sotah_9` | ti=236 ("פרק ט חלק א") vs ti=237 ("פרק ט חלק ב") | The docx splits sotah ch. 9 into "part 1" and "part 2". The current matcher only matches "פרק ט" and treats them as duplicates. They are conceptually distinct halves. |
| `zevachim_5` | ti=329 vs ti=330 | Different shapes; both 0 markers in the current docx. |
| `middot_1` | ti=409 (15 markers, [[1,2,1],[2,2],[1,2,1]]) vs ti=410 (16 markers, [[1,1,1],[1,1,1],[1,1,1]]) | Two structurally different versions, both with content. |
| `middot_2` | ti=411 (11 markers, [[1,2,1],[2,2],[1,2,1]]) vs ti=412 (57 markers, [[2,2],[2,2],[2,2],[2,2],[2,2]]) | Significantly different — ti=412 has nearly 6× the markers and a 5-row shape. |
| `kelim_4` | ti=422 vs ti=423 | Both 0 markers, different shapes. |

`build_table_index` currently keeps the last-seen table. Without intervention, Stage A would silently take ti=111 for shabbat_22, ti=237 for sotah_9, ti=412 for middot_2, etc., losing the prior tables entirely.

---

## 6. Files Touched

| File | Action |
|---|---|
| `_pilot/mishnah_extractor_v2.py` | Updated to v2.1.2 (header-row classifier, missing-chapter handling, `build_table_index`, `extract_all_chapters_from_json`, `--from-json` CLI). **Note:** the bash mount may show stale pre-session content for this file — the canonical content can be read via the file tools or from `/sessions/.../mnt/outputs/mishnah_extractor_v2.py`. |
| `_pilot/stage-a-report.md` | Created (this file). |

**Not written:**
- `_pilot/mishnah_db_reextracted.json` — Stage A's intended deliverable. Not produced because verification halted on a substantive divergence (`berakhot_1`) before the Step-3 full pass.

---

## 7. Decision Needed Before Continuing

The task spec at Step 2 says: "If any chapter diverges from expected, STOP and report — the new heuristics may be over-firing." Berakhot_1 diverges (the classifier reduces a 5-row live entry to a 2-row staged entry that loses mishnah ג as content), and the survey shows the same pattern repeating across dozens of chapters. Continuing to Step 3 without direction would produce a candidate dataset where ~110 chapters have content reshuffled by the heuristic, ~50 falsely missing because of name aliasing, and 6 chapters silently overwritten by the duplicate-table handling.

Three plausible directions, ordered roughly by amount of upstream re-work:

1. **Tighten the classifier before running.** Add disambiguation so the heuristic only fires when a 1-cell row is structurally a header — e.g., (a) only fire MIDDLE if the row's text does not start with a mishnah-number marker like `(ג)`; (b) only fire TOP if there is exactly one 1-cell row at the start; (c) only fire BOTTOM when the row's text is very short relative to surrounding rows. The TOP-classifier should cover all 17 Group E chapters, not just 10. The MIDDLE-classifier should cover tahorot_1 and few others, not 49. The BOTTOM-classifier may need to be disabled or made opt-in pending Moshe's review of the 56 cases.

2. **Add the missing name aliases to `TRACTATE_NAMES`.** Either change the mapping to produce live-JSON keys (`bavakamma`, `bavametzia`, `bavabatra`, `oholot`, `rosh_hashanah`) or add a name-normalization step in `extract_all_chapters_from_json` that maps between forms. Investigate `nazir_8` and `sukkah_3` to see why they fail to match.

3. **Decide the duplicate-table policy.** Sotah_9 should arguably be two keys (`sotah_9a`, `sotah_9b`) or merged. For shabbat_22, middot_1, middot_2, etc., one of the two tables is the authoritative version — Moshe needs to flag which.

If you'd rather see the staged output before making any of these decisions, I can run the full extraction as-is (no aliasing, current over-firing heuristic, last-write-wins on duplicates) and write `_pilot/mishnah_db_reextracted.json` with the anomalies recorded. Stage B's diff would then highlight every place a heuristic fired, and you could decide per-category.

Tell me which path to take.
