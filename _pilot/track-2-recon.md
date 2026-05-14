# Track 2 — Mishnah JSON Reconnaissance

**Date:** 2026-05-14
**Scope:** Read-only discovery for the upcoming Phase D-1 pilot build. Locate the Mishnah JSON, describe its schema, cross-reference against existing chapter paths, propose a render strategy. **No files modified.**

---

## 1. Search Results

### Candidate JSON files

| Path | Size | Modified | Notes |
|---|---:|---|---|
| `Mishnah-New/English/mishnah_db.json` | **16.66 MB** | 2026-05-11 09:52 UTC | **Primary candidate.** Already deployed in the repo. |
| `_pilot/mishnah_db_reextracted.json` | 16.66 MB | 2026-05-11 09:52 UTC | **Byte-identical to the primary** (same MD5). Working copy left from extraction work. |
| `plan/mishnah_db.json` (outside repo) | 6.56 MB | 2026-05-04 09:34 UTC | **Older, smaller version.** Probably superseded by the May 11 extraction. Different MD5. |
| `_pilot/megillah_1_extracted.json` | 43.3 KB | 2026-05-10 11:40 UTC | Single-chapter sample (Megillah 1) from an earlier extraction test. |
| `_pilot/keritot_3_4_5_kinnim_1_extracted.json` | 119.6 KB | 2026-05-11 05:19 UTC | A few-chapter extraction (Keritot 3/4/5, Kinnim 1). |

### Recommendation

The **`Mishnah-New/English/mishnah_db.json`** (the deployed copy) is the single source of truth. The `_pilot/mishnah_db_reextracted.json` is its byte-identical sibling — keep one or the other, doesn't matter for the build pipeline. The `plan/mishnah_db.json` is older and should be ignored unless you specifically want to compare against an earlier extraction state.

A supporting extractor script is at `_pilot/mishnah_extractor_v2.py` with a test at `_pilot/mishnah_extractor_v2_test.py`. Phase D won't need to re-run extraction (the JSON is complete) but those tools are available if any rebuild is needed.

### Other formats considered

No `.jsonl`, `.ndjson`, `.yaml`, `.yml`, or `.tsv` chapter-data files found. Several CSVs exist in `plan/` (inventory, pdf-inventory, template-registry) but those are operational metadata, not chapter content.

---

## 2. JSON Schema

### Top-level structure

```
dict (525 chapter entries + 1 _meta key) = 526 total keys
```

Each chapter is keyed by a lowercase phonetic identifier like `berakhot_1`, `megillah_3`, `sotah_9a`. The `_meta` key holds extractor metadata.

### `_meta` block highlights

```json
{
  "version": "2026-05-rev9",
  "description": "Mishnah structural database — all 524 chapters with marker annotations",
  "markers_populated_count": 310,
  "total_chapters": 525,
  "total_markers": 10405,
  "extractor_version": "2.1.4",
  "last_extraction_date": "2026-05-11",
  "marker_types": ["horizontal1", "horizontal2", "horizontal3", "vertical1",
                   "internalparallel", "closure", "ciasm1", "ciasm2"],
  "notes": "Re-run of Pass 6 against updated docx. ketubot_14 added (2×3); yadayim_3 corrected from combined ch.3+ch.4 to 3×2; yadayim_4 separated as its own 2×2 table. v2.1.4 extractor unchanged. sotah_9 still split into sotah_9a / sotah_9b. shabbat_22 still ti=110 (defensive override remains in code). zevachim_5 retains palindrome [1,2,3,2,1] shape.",
  "duplicate_table_decisions": {
    "shabbat_22": "ti=110 (earlier, 3×2 with markers) — duplicate eliminated in docx",
    "middot_1": "ti=410 (later, 3×3) — duplicate eliminated in docx",
    "middot_2": "ti=412 (later, 5×2) — duplicate eliminated in docx",
    "kelim_4": "ti=423 (later, 2×3) — duplicate eliminated in docx",
    "zevachim_5": "ti=330 (later, palindrome [1,2,3,2,1]) — duplicate eliminated in docx",
    "sotah_9": "split into sotah_9a and sotah_9b"
  },
  "known_open_issues": {
    "nazir_8_docx_typo": "docx has 'סכת נזיר' instead of 'מסכת נזיר'; v2.1.3+ tolerates via fallback matcher",
    "311_vs_310_marker_count_discrepancy": "Claude in Word reported 311 chapters with colored highlights; deferred for investigation"
  },
  ...
}
```

Plus a `shape_review_decisions` block recording per-chapter shape adjudication notes from the May 10 review pass (Kelim 4, Yevamot 2, Ketubot 11/12, Eduyot 7, Keritot 3, Tahorot 1, Sanhedrin 6, Avot 2, Bekhorot 8 all have explicit decision records).

### Per-chapter structure — sample (Berakhot 1)

Top-level keys per chapter:

```
{
  "tractate_he": "מסכת ברכות",
  "tractate_en": "Berakhot",
  "seder_he": "זרעים",
  "seder_en": "Zeraim",
  "chapter_he": "א",
  "chapter_num": 1,
  "shape": [[2, 2], [4], [2, 2]],
  "source_url": "https://chaver.com/Mishnah-New/Hebrew/Text/Seder%20Zeraim/Masechet%20Brachot/Mesechet%20Brachot%20Perek%201.htm",
  "rows": [ {row_num, cells: [{...}]} × N ]
}
```

`shape` is a list of row-widths. `[[2, 2], [4], [2, 2]]` means three rows: row 1 has two cells of colspan 2, row 2 has one cell of colspan 4, row 3 has two cells of colspan 2. This drives the matrix-table HTML layout.

Each row is `{row_num: int, cells: list}`. Each cell is:

```
{
  "label": "1א",                      // human-readable position label
  "position": {"row": 1, "col": 1, "colspan": 2},
  "text": "1א\n(א) מאימתי קורין את שמע בערבית\nמשעה שהכהנים נכנסים לאכול בתרומתן\n...",
  "runs": [
    {"text": "1א", "marker": null},
    {"text": "\n", "marker": null},
    {"text": "(א) ", "marker": null},
    {"text": "מאימתי קורין את שמע", "marker": "horizontal1"},
    {"text": " בערבית", "marker": null},
    ...
  ],
  "markers": [
    {"type": "horizontal1", "text": "מאימתי קורין את שמע"},
    {"type": "horizontal1", "text": "עד"},
    {"type": "horizontal1", "text": "בניו"}
  ]
}
```

### Per-field purpose

| Field | Role |
|---|---|
| `tractate_he`, `tractate_en` | Display names in HE/EN |
| `seder_he`, `seder_en` | Order name in HE/EN |
| `chapter_he`, `chapter_num` | Chapter ordinal in HE (letter) and Arabic digit |
| `shape` | Matrix layout dimensions; `len(shape)` = number of rows, each entry = list of colspans |
| `source_url` | Target chapter URL (some inconsistency vs. disk paths — see §3) |
| `rows[i].row_num` | 1-indexed row number |
| `rows[i].cells[j].label` | Position label like "1א" or "3ב" — display this in the cell header |
| `rows[i].cells[j].position` | `{row, col, colspan}` for grid placement |
| `rows[i].cells[j].text` | Full plaintext (use as fallback or for og:description extraction) |
| `rows[i].cells[j].runs` | The text broken into spans with optional `marker` for inline highlighting — **this is the render source of truth** |
| `rows[i].cells[j].markers` | High-level summary of markers in the cell (redundant with `runs` for rendering; useful for analysis/reporting) |

### Content type

**Structured data, not pre-rendered HTML.** The Phase D-2 build needs a render function that walks the rows/cells/runs structure and emits matrix-table HTML.

### Hebrew encoding

UTF-8. RTL is handled via `direction: rtl;` in main.css (the new template's HE side wraps `<main>` with `dir="rtl"` by template/lang). The text contains expected Hebrew punctuation, niqqud-free Mishnah Hebrew, and the parenthesized verse markers like `(א)`, `(ב)`, etc. (note the non-breaking-space ` ` after parens, preserved from the docx source).

### Cross-references

`source_url` is the only cross-reference field — points to the existing chapter URL. Per-chapter there's no schema for cross-chapter links, citations, or English translations.

### Translations / commentary

None. The JSON is Hebrew-only with marker annotations.

### Timestamps

`_meta.last_extraction_date: "2026-05-11"` (corpus-level). No per-chapter `datePublished` or `dateModified`.

### Sample sizes

For `berakhot_1`:

- JSON entry size: ≈ 11–12 KB (Hebrew UTF-8 expands characters)
- 3 rows, 5 cells total (because two rows have 2 cells, one row has 1 cell)
- 34 runs in the first cell; ~150 runs total in the chapter
- 3 cell-level markers (all horizontal1)

For the full corpus:

- Per-chapter JSON size: **min ~2 KB, median ~25 KB, max ~120 KB**
- Total JSON size on disk: 16.66 MB
- Marker coverage: **310 of 525 chapters have at least one marker** (≈ 59%); 215 have no markers
- Total marker instances across all `runs`: **6,953**
- Unique marker types observed in `runs`: `ciasm1, ciasm2, closure, horizontal1, horizontal2, horizontal3, internalparallel, vertical1` (8 types)

### Chapters by seder

| Seder (EN) | Chapter count |
|---|---:|
| Zeraim | 74 |
| Moed | 88 |
| Nashim | 73 |
| Nezikin | 73 |
| Kodashim | 89 |
| Tohorot | 126 |
| (unspecified) | 2 |
| **Total** | **525** |

The 2 "unspecified" entries are `keritot_3` and `kinnim_1` — both have empty `seder_en` / `seder_he` / `tractate_en` / `chapter_num` fields (Phase D-2 will need to fill those in from key parsing or per-tractate lookup).

### Rendered-HTML size extrapolation

Each existing chapter file on disk averages ≈ 19,000–22,000 bytes (post Phase B + E-1 + E-2). The new render won't be dramatically different in size if it generates clean tables (the existing files have Word-export cruft that bloats them — `MsoNormal` styles, font-family declarations, etc., which a clean render can omit).

**Estimated total post-render disk footprint:** 10–12 MB across 525 chapters. Modest growth over today's footprint.

---

## 3. Cross-Reference JSON ↔ Existing Chapter Paths

### Methodology

Built two lists and compared by **normalized path** (the `.htm`/`.html` extension stripped):

- List A: `source_url` from JSON, URL-decoded, stripped of `https://chaver.com/` and trailing extension
- List B: every `*Perek*.htm` and `*Perek*.html` file under `Mishnah-New/Hebrew/Text/`, excluding `BACKUP_*` folders

### Headline numbers

| Category | Count |
|---|---:|
| JSON entries with `source_url` | 521 |
| JSON entries without `source_url` (special cases) | 4 |
| **Total JSON chapter entries** | **525** |
| Existing chapter files on disk (`.htm` + `.html`) | **525** |
| Match by normalized name (source_url ↔ disk path, ignoring extension) | **521 (100% of those with source_url)** |
| JSON entries without `source_url` that have a corresponding disk file (via tractate-chapter heuristic) | **4 (all of them)** |
| Disk files with no JSON entry | 0 |
| JSON entries with no disk file | 0 |

**Net result: every JSON entry maps to exactly one disk file, and vice versa.** No orphans on either side.

### Two specific mismatches to flag

#### 3.1 Extension mismatch (15 files): `.htm` in JSON vs `.html` on disk

The JSON `source_url` for these chapters ends in `.htm`, but the actual files on disk use `.html`:

| Tractate | Chapters affected |
|---|---|
| Zevachim (Kodashim) | All 14 chapters (Perek 1 through 14) |
| Nedarim (Nashim) | Perek 1 only (Perek 2–11 are `.htm` like the rest of the corpus) |

These 15 files were Phase B-migrated under their `.html` paths and have E-1 + E-2 injected just like the rest. The JSON's `.htm` source_url is what a normalized canonical naming would produce, but it doesn't match reality.

**Implication for Phase D-2:** the render must write to the **actual disk path** (preserving `.html` for these 15 cases), not blindly trust `source_url`. The JSON's `source_url` field is an aspirational canonical hint, not a directive.

This is also a separate URL-correctness issue worth flagging: Cloudflare doesn't strip `.htm`, but does strip `.html`. So:

- `https://chaver.com/Mishnah-New/Hebrew/Text/Seder%20Zeraim/Masechet%20Brachot/Mesechet%20Brachot%20Perek%201.htm` works (matches the `.htm` file)
- `https://chaver.com/Mishnah-New/Hebrew/Text/Seder%20Kodashim/Masechet%20Zevachim/Masechet%20Zevachim%20Perek%201` works (matches the `.html` file with extension stripped)
- `https://chaver.com/Mishnah-New/Hebrew/Text/Seder%20Kodashim/Masechet%20Zevachim/Masechet%20Zevachim%20Perek%201.htm` will **404** (no `.htm` file there)

The links from Shishah Sidrei Mishnah (the portal) to each chapter may have this inconsistency. Worth a future fixup pass: normalize all 15 to `.htm` (rename and update all references) OR keep `.html` and update the portal's outbound links accordingly. Recommend the **rename to .htm** path — it matches the rest of the corpus and matches what the JSON already expects.

#### 3.2 Four JSON entries with no `source_url`

These 4 entries do exist on disk; the JSON just doesn't have the `source_url` field populated for them:

| JSON key | Matching disk file | Notes |
|---|---|---|
| `keritot_3` | `Masechet Kritot Perek 3.htm` (Kodashim) | Has rows + markers; per `_meta.shape_review_decisions`, "Docx structure doesn't match target subdivisions yet" — empty pending docx revision |
| `kinnim_1` | `Masechet Kinnim Perek 1.htm` (Kodashim) | Has rows. (Kinnim is a very small tractate, 3 chapters total.) |
| `sotah_9a` | `Masechet Sotah Perek 9 A.htm` (Nashim) | New split from sotah_9; has rows + markers |
| `sotah_9b` | `Masechet Sotah Perek 9 B.htm` (Nashim) | Companion to 9a |

For Phase D-2, the render function will need to either (a) derive `source_url` from the JSON key + tractate metadata, or (b) accept a manual override map for these 4 cases. A small heuristic should handle them.

Also note: **`keritot_3` and `kinnim_1` both have `null` for `seder_en`, `tractate_en`, and `chapter_num`**. The render function needs to fill these from the JSON key.

### Naming/spelling inconsistencies between JSON keys and disk paths

The JSON keys use scholarly biblical-Hebrew transliteration (lowercase, no spaces). The disk paths use a variant transliteration with title case and "Masechet" prefix. They don't match 1:1 lexically, but the chapter-level mapping is unambiguous:

| JSON key | Disk-path tractate name | Notes |
|---|---|---|
| `berakhot` | `Brachot` | "Berakhot" (academic) vs "Brachot" (Sephardic transliteration) |
| `keritot` | `Kritot` | Similar academic/colloquial distinction |
| `bavakamma` | `Baba Kama` | JSON has no space; disk has space |
| `bavametzia` | `Baba Metzia` | Same |
| `bavabatra` | `Baba Batra` | Same |
| `moed_katan` | `Moed Katan` | Underscore vs space |
| `maaser_sheni` | `Maaser Sheni` | Underscore vs space |
| `tevulyom` | `Tevul Yom` | Concatenated vs spaced |
| `oktzin` | `Uktzim` | Different spellings — "Oktzin" (modern) vs "Uktzim" (traditional) |
| `chullin` | `Chullin` | Match |
| `bekhorot` | `Bekhorot` | Match |
| `middot` | `Midot` | Single 'd' on disk; double 'd' in JSON |

The JSON key naming is internally consistent and matches the academic conventions used in scholarly literature. The disk-path naming is the legacy of the site's history. **The JSON-key form is the better canonical going forward** — but the disk paths are what's deployed and indexed.

### Sotah 9 special case

The JSON splits Sotah Perek 9 into `sotah_9a` and `sotah_9b` (per the `_meta.duplicate_table_decisions` note: "split into sotah_9a and sotah_9b"). The disk has matching split files:

- `Masechet Sotah Perek 9 A.htm`
- `Masechet Sotah Perek 9 B.htm`

So there's no mismatch — the disk already accommodates the split. The breakdown counted Sotah as 10 "chapters" in the JSON (1, 2, 3, 4, 5, 6, 7, 8, 9a, 9b) which matches 10 disk files.

### Net delta vs. 524 expectation

The original task spec referred to "524 chapters." The JSON reports `total_chapters: 525` in `_meta`, and we counted 525 chapter entries (excluding `_meta`). The extra 1 is the Sotah 9 split (which adds one chapter to the 524-chapter standard count — 9a + 9b instead of one combined 9).

**Reconciliation:** 524 canonical chapters + 1 (Sotah 9 split into A/B) = 525.

---

## 4. Render-Feasibility Assessment

### Verdict: render-from-structure required

The JSON is **structured data, not pre-rendered HTML**. Phase D-2 needs a render function that consumes `rows[].cells[]` and emits an RTL Hebrew matrix-table.

The render is straightforward in concept — walk the cells, generate `<table>/<tr>/<td>` with appropriate `colspan` from `position.colspan`, split text into `<span>` runs with marker-typed class names. The complexity is in the details: cell labels, line breaks (the `text` field uses `\n` for visual line breaks within a cell), highlighting (the `runs` field is the source of truth, not `markers`), and producing visually consistent output across all chapters.

### Recommended render pipeline

```
JSON chapter entry
  → derive metadata (canonical URL, breadcrumb, title, description)
  → for each row: emit <tr>
      → for each cell: emit <td colspan="{position.colspan}">
          → emit <p class="cell-content" dir="rtl">
              → emit <span class="cell-label">{label}</span> + <br/>
              → for each run: emit <span class="{marker or 'plain'}">{text}</span>
                  (preserve \n as <br/> in text)
  → wrap in <table class="mishnah-table" dir="rtl">
  → inject into HE template via {{ region: content }}
```

### CSS compatibility

main.css already supports both `.Horizontal1` (capitalized — Word export legacy) and `.horizontal1` (lowercase — JSON-native form), along with `.Vertical1` / `.vertical1`, `.Ciasm1`/`.ciasm1`, `.Closure`/`.closure`, `.InternalParallel`/`.internalparallel`. **Phase D-2 can use the JSON's marker names verbatim as CSS class names.** No case conversion needed.

The existing rendered chapters use the capitalized forms (`Horizontal1`) from the Word-export pipeline. The new render will use lowercase forms (`horizontal1`) from JSON — same visual result.

### Where to write the rendered files

**Recommend: write to the existing disk paths.** This:

1. Preserves all existing inbound nav links from Shishah Sidrei Mishnah portal (which links to specific paths with `.htm`/`.html` extensions per current state)
2. Preserves canonical URLs set by E-2
3. Preserves all SEO/AEO investments (BreadcrumbList, Article schema, E-1 entity references)
4. Means Phase D-2 is an in-place rewrite of `<main>` content while keeping all chrome and metadata

The 15 extension-mismatch cases (Zevachim + Nedarim 1) should be written to the existing `.html` paths to preserve canonical URLs. Their canonical URLs (as set by E-2) already reflect the `.html` extension. If Moshe later wants to rename them to `.htm` for consistency, that's a separate task.

### Per-chapter Title pattern

Recommend (Hebrew, RTL-friendly):

```
{tractate_he} פרק {chapter_he} – המשנה כדרכה | Chaver.com
```

Example: `מסכת ברכות פרק א – המשנה כדרכה | Chaver.com`

Or with the structural-analysis framing:

```
{tractate_he} פרק {chapter_he} – המבנה הספרותי | Chaver.com
```

Per chapter the `<title>` is fully derivable from the JSON.

### Per-chapter Description pattern

```
משנה {tractate_he} פרק {chapter_he} בפריסה מבנית – הטקסט המלא עם הדגשת המבנה הספרותי הדו-ממדי
```

This matches the existing pre-E-2 description pattern observed on the existing Megillah/Brachot/etc. pages. Reusing it gives consistency. The first ~100 chars of `text` from `rows[0].cells[0]` is also available as an alternative if Moshe wants a quote-style description.

### Article schema population (per chapter)

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title}",
  "description": "{description}",
  "url": "{canonical}",
  "mainEntityOfPage": "{canonical}",
  "inLanguage": "he",
  "author": {"@id": "https://chaver.com/#moshe-kline"},
  "publisher": {"@id": "https://chaver.com/#organization"},
  "isPartOf": {"@id": "https://chaver.com/#mishnah-collection"},  ← NEW: from E-3
  "image": {"@type": "ImageObject", "url": "https://chaver.com/torah-weave/Admin/Assets/Images/og-default-1200x630.jpg", "width": 1200, "height": 630}
}
```

The `isPartOf` reference assumes E-3 (Mishnah Portal → CollectionPage) lands first. Phase D-1 pilot doesn't need to wait — can use the existing `#website` reference and update later. Order of operations: **E-3 (CollectionPage on portals) → D-1 (pilot 3-5 chapters) → D-2 (bulk all 525 chapters with full isPartOf)**.

### BreadcrumbList per chapter

```
Home → Mishnah → Hebrew → {seder_he} → {tractate_he} → {tractate_he} פרק {chapter_he}
```

Same pattern E-2 already generates from path segments. The new render shouldn't need to re-author BreadcrumbList — E-2 has put one on every existing chapter file. The render preserves it.

### Optional enhancements (deferred — not D-1/D-2 scope)

- **Cross-chapter navigation links** (prev/next chapter, same tractate) — would require building a chapter-order index
- **Citation widgets** for academic referencing of specific Mishnah passages
- **English translation toggle** — would require new data (not in current JSON)

---

## 5. Open Questions for Moshe

Before Phase D-1 can be drafted in detail, please decide:

### Q1: Extension consistency for the 15 `.html` mismatches

The 14 Zevachim chapters and Nedarim Perek 1 use `.html` extension while the rest of the corpus uses `.htm`. Pick one:

- **(A)** Rename the 15 to `.htm` to match the rest. Update portal links if any explicitly reference `.html`. Pre-Phase-D-2 cleanup.
- **(B)** Keep `.html`. Update the JSON `source_url` field for those 15 entries to match (or just let the disk path win during render).
- **(C)** Leave as-is, render writes to actual disk path. Canonical URLs stay mixed.

**Recommend (A)** — single-extension consistency simplifies future tooling, matches the JSON expectation, and the URL canonical layer in E-2 can be refreshed for just these 15 files.

### Q2: Spelling/transliteration standard

Disk paths use one transliteration scheme ("Brachot", "Kritot", "Baba Kama") and JSON keys use another ("berakhot", "keritot", "bavakamma"). Pick one:

- **(A)** Keep disk paths as-is for backward compatibility. Render maps JSON-key → disk-path via a hard-coded lookup table.
- **(B)** Migrate disk paths to match JSON's academic spelling. Big lift: rename 525 files, update Shishah Sidrei portal links, add Cloudflare 301 redirects for old URLs.
- **(C)** Establish a canonical academic spelling but keep current paths as 301 redirects to the new ones.

**Recommend (A)** for Phase D — minimal disruption. Add a `JSON_KEY_TO_TRACTATE_NAME` lookup in the render code. Defer (B)/(C) as a separate URL-cleanup task.

### Q3: Render style — match existing or modernize

The existing chapter pages have Word-export cruft (`MsoNormal` classes, inline `style="border: medium none;"`, nested `<span lang="he">` wrappers). A clean render would emit lean HTML.

- **(A)** Replicate the existing visual exactly, including the Word-export markup. Lower risk of visual drift.
- **(B)** Emit clean modern HTML using main.css's matrix-table styles. Smaller file sizes, easier to maintain.

**Recommend (B)**. The 525 chapters are about to be rewritten anyway; do it once, cleanly. Estimated size savings: 30-40% per chapter, plus easier ongoing maintenance.

### Q4: How to handle the 4 entries without `source_url`

For `keritot_3`, `kinnim_1`, `sotah_9a`, `sotah_9b`:

- Derive `source_url` from JSON-key parsing + a tractate→disk-path lookup
- OR hard-code these 4 in the render code as an override map
- OR populate `source_url` in the JSON directly (one-time edit)

**Recommend** the third — fix it once in JSON, then everything downstream just works. (`source_url` is data, not derivation logic; populate it.)

### Q5: How to handle the 2 entries with `null` seder/tractate/chapter_num

`keritot_3` and `kinnim_1` have `null` values for `seder_en`, `tractate_en`, `chapter_num`. The render needs these for breadcrumb, schema, title. Same recommendation: **fix in JSON** — fill in `seder_he: סדר קדשים`, `seder_en: Kodashim`, `tractate_en: Keritot` (or `Kritot`), `chapter_num: 3` and similar for `kinnim_1`.

### Q6: Pilot chapter selection for Phase D-1

Recommend testing 5 chapters that exercise different shapes:

- `berakhot_1` — small (3 rows, 3 shape) — basic sanity
- `megillah_1` — already has an `_pilot` extraction sample; cross-check
- `eduyot_1` — large/complex
- `kinnim_1` — small tractate, missing source_url + null metadata (validates the fallback path)
- `sotah_9a` — split chapter (validates the suffix handling)
- A heavily-marked chapter (find one with all 8 marker types — perhaps `shabbat_22` per `_meta`)

### Q7: hreflang for chapter pages

The 525 chapters are HE-only. No English version exists. Recommend **no hreflang** on chapter pages (current E-2 state — hreflang only on home pair).

### Q8: When to integrate `isPartOf: #mishnah-collection`

The new Article schema references `https://chaver.com/#mishnah-collection`. This `@id` doesn't exist yet — E-3 should create it as the Mishnah Portal CollectionPage's `@id`. Decision:

- **(A)** Run E-3 first (creates `#mishnah-collection`), then D-1 / D-2 reference it
- **(B)** Run D-1 / D-2 first with a placeholder `isPartOf` (or omit), then back-fill after E-3
- **(C)** Run E-3 and D-1 in parallel since they touch different files

**Recommend (A)** — clean dependency order, no back-fill needed. E-3 is small (touches ~4 portal pages) and shouldn't slow Track 2 meaningfully.

---

## 6. Suggested Order of Operations Going Forward

1. **Moshe answers Q1–Q8** (most can be quick decisions)
2. **Optional fixup**: rename 15 `.html` → `.htm` (Q1); populate 4 missing source_urls + 2 missing metadata (Q4/Q5) — small JSON edit
3. **E-3**: Mishnah Portal → CollectionPage with `@id: #mishnah-collection` (4 portal pages)
4. **Phase D-1**: pilot render of 5-6 chapters; verify visual output, marker rendering, file structure
5. **Phase D-2**: bulk render all 525 chapters in one Cowork run (with defensive verification: size match, `</html>` end, JSON-LD parse)
6. **Phase D-3**: portal page enhancements (update Shishah Sidrei Mishnah with linked chapter list from JSON; same for TheMishnah and English Mishnah Portal)
7. **Verification pass**: re-run SEO audit; confirm all 525 chapters pass

Total estimated Cowork work: 3-4 runs (one for E-3, one for D-1 pilot, one for D-2 bulk, optionally one for D-3 polish).

---

## 7. Files Touched

| Path | Purpose |
|---|---|
| `_pilot/track-2-recon.md` | This report |

Nothing else modified. Read-only reconnaissance complete.
