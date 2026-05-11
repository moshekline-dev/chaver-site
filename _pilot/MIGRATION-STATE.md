# Migration State — chaver-site

**Last updated:** 2026-05-10
**Version:** Pre-Pass-3

---

## 1. What This Project Is

Chaver.com is undergoing two parallel infrastructure upgrades. First, the site is migrating off Microsoft Expression Web's Dynamic Web Template (DWT) system — which requires Expression Web to edit pages — to standalone rendered HTML templates that any editor or build system can produce. Second, the site's public Mishnah JSON dataset (`mishnah_db.json`) is being populated with structural markup extracted from a master Word document that contains 40 years of compositional analysis encoded as character-styled color markers.

The two workstreams are independent but share infrastructure: the same HTML templates render both Torah commentary pages and Mishnah chapter pages; the extracted JSON markers feed both the dataset and the rendered chapter HTML; and the same `main.css` file styles all marker spans across both corpora.

---

## 2. Current State — What's Done

- **Cleanup phases 1–3** (committed, deployed): Removed `_vti_cnf` directories, DESKTOP-VT27BJM duplicate files, orphaned PDFs, `_derived` directories, `__ti_cnf` directories, and the "Units without DWT" backup folder. Total: ~1,200 files removed.

- **Redirect repairs** (committed, deployed): Added 301 redirects for the old genesis-unit-1-commentary folder, genesis-unit-12-261-33 folder, and the Before Chapter and Verse PDF. Cleaned the `_redirects` file of null-byte corruption.

- **Leviticus double-dash rename** (committed, deployed): Renamed `leviticus--unit-*` files/directories to `leviticus-unit-*` (single dash). Updated all internal links and added redirects for the old paths.

- **Template reverse-engineering** (committed, not deployed as templates — they're infrastructure): Extracted the Academic-Content-DWT into two standalone template files:
  - `_templates/Academic-Content-EN.html` (14,898 bytes)
  - `_templates/Academic-Content-HE.html` (14,908 bytes)
  - Round-trip validated: byte-identical reconstruction from scaffolding + regions.
  - Template uses `{{ region: name }}` placeholders for 5 editable regions: doctitle, meta, additional-styles, content, page-scripts.

- **Template pilot — plain Hebrew page** (committed, deployed at `/pilot/megillah-perek-1-he.html`): Successfully rendered a real Hebrew Mishnah chapter page through the HE template. Confirmed: RTL works, main.css applies, no DWT markers in output.

- **Mishnah JSON null-byte cleanup** (committed): Stripped 1,461,451 bytes of trailing null padding from `mishnah_db.json` (6.56 MB → 5.10 MB). Content byte-identical to git HEAD; corruption was mount-layer artifact.

- **Word → JSON extraction pilot** (in `_pilot/`, not yet merged into dataset): Extracted Megillah Chapter 1 from the master docx. 50 structural markers across 4 types, 7 cells with A/B subdivisions, all verified against existing JSON. Extraction is byte-faithful.

- **Visual rendering pilot** (committed, deployed at `/pilot/megillah-perek-1-marked.html`): Rendered the extracted JSON into HTML with inline `<span class="horizontal1">` etc. All 50 marker spans verified present. Colors render correctly via main.css (validated against the Color Code page).

- **Inventory and audit artifacts** (committed at repo root):
  - `template-registry.csv` — maps all 933 DWT-attached pages to their target templates
  - `legacy-audit.csv` — disposition of 54 non-Academic-Content legacy DWT pages

---

## 3. Verified Mappings and Decisions

### Style → CSS class mapping (authoritative)

| Word character style | CSS class | Color (for reference only) |
|---|---|---|
| `Horizontal10` | `horizontal1` | #3399FF (blue) |
| `Horizontal2` | `horizontal2` | #008080 (teal) |
| `Horizontal3` | `horizontal3` | #008B8B (dark cyan) |
| `Vertical1` | `vertical1` | #8B4513 (brown) |
| `InternalParallel` | `internalparallel` | #C00000 (dark red) |
| `Closure` | `closure` | #77206D (purple) |
| `Ciasm1` | `ciasm1` | #7030A0 (violet) |
| `Ciasm2` | `ciasm2` | #7030A0 (violet, underlined) |

### Why colors don't matter

The docx applies colors via named character styles, not direct run-level formatting. The extraction reads the `w:rStyle` XML element from each run's properties — the style NAME carries all structural information. The actual color hex values are irrelevant to extraction (they only matter for the CSS rendering on the site, which is handled by main.css).

### Source document location

```
C:\Users\Moshe\OneDrive\Documents\Research\The Structured Mishnah\ספר על המשנה כדרכה\For KDP\The Whole  Structured Mishnah for pdf.docx
```

(3.40 MB, 544 tables, 738 paragraphs)

### Mishnah dataset current state

- File: `Mishnah-New/English/mishnah_db.json`
- Version: `2026-05-rev3`
- Total chapters: 524
- Chapters with existing markers (any level): **148**
  - 128 have cell-level markers (`cell.markers` non-empty)
  - 20 have markers only at subdivision level (`cell.subdivisions[*].markers`)
  - 82 of the 128 also have subdivision-level markers (overlap)
- Chapters needing marker population from docx: **376**
- **Pass 3 skip criterion:** Skip a chapter if ANY markers exist at either cell or subdivision level (the "strict/union" definition). This avoids overwriting the 20 subdivision-only chapters.

### Technical decisions

- **Character-style extraction:** Read `w:rStyle` from `<w:rPr>` in each `<w:r>` run. Do NOT use `run.font.color.rgb` (returns None for style-inherited colors).
- **Merged cell handling:** Use `tr._tr.findall(qn('w:tc'))` directly — python-docx's `row.cells` duplicates merged cells.
- **Subdivision detection:** A run with `Subunit` style whose text is a single uppercase Latin letter (`A`, `B`, `C`) is a subdivision marker. Cell labels (like `2א`) also use `Subunit` but start with a digit.
- **Mishnah numbers:** `(א)`, `(ב)`, etc. are preserved in extraction (not stripped). The existing JSON strips them. This is a formatting choice to resolve in Pass 3.
- **Space-loss bug (fixed in v2):** The extractor must walk ALL children of each `<w:r>` element — including `<w:br/>` (line break), `<w:tab/>`, and `<w:cr/>` — not just `<w:t>` text elements. Self-closing `<w:br/>` tags have no text content and are invisible to `findall('w:t')`.

---

## 4. What's Next — Remaining Work

In approximate order of execution:

1. **Pass 3: Full corpus extraction** — Extract markers from all 524 chapters in the docx and merge into `mishnah_db.json`. The 128 chapters with existing markers need comparison/validation; the 396 empty chapters need population. Scope: ~2 hours of extraction time, plus validation.

2. **Hebrew chapter page regeneration** — Re-render all 524 Mishnah chapter pages with inline marker spans (like the pilot). Each page uses the HE template + table structure from the JSON. Scope: batch process, dependent on Pass 3 completion.

3. **Hebrew navigation** — Translate template nav labels, decide link routing for Hebrew pages, add breadcrumb patterns for Mishnah section. Open design question.

4. **88 Hebrew Torah unit pages migration** — Currently on Academic-Content-DWT with `lang="en"` (wrong). Need to re-render through Academic-Content-HE template. Scope: batch process after template validation.

5. **214 English Academic-Content pages migration** — Re-render through Academic-Content-EN template. Largest batch. Scope: batch process.

6. **54 Legacy DWT pages** — Per `legacy-audit.csv`: some keep (Contact, portals), some retire (superseded articles), some migrate to EN template. Requires per-page decisions.

7. **`hebrew-leviticus-unit-19.html` corruption** — 95% null padding, valid content was modified (504 bytes larger than HEAD). Needs content review before cleaning.

8. **Author page with Person schema** — Low-effort, high-value: add schema.org Person markup to the About page for entity building.

---

## 5. Key Files and Locations

| What | Path |
|---|---|
| EN template | `_templates/Academic-Content-EN.html` |
| HE template | `_templates/Academic-Content-HE.html` |
| Template notes | `_templates/REVERSE-ENGINEER-NOTES.md` |
| Template registry | `template-registry.csv` (repo root) |
| Legacy audit | `legacy-audit.csv` (repo root) |
| Mishnah dataset | `Mishnah-New/English/mishnah_db.json` |
| Source docx | (see path in §3 above — local machine, not in repo) |
| v2 extractor | `_pilot/mishnah_extractor_v2.py` |
| Pilot — plain HE | `pilot/megillah-perek-1-he.html` |
| Pilot — with markers | `pilot/megillah-perek-1-marked.html` |
| Color Code reference | `/General/Color%20Codes/English%20Color%20Code.htm` |
| Main CSS | `torah-weave/Admin/Assets/CSS/main.css` |
| Extraction reports | `_pilot/megillah-1-recon-report.md`, `megillah_1_extraction_report.md`, `pass-2.5-report.md` |

---

## 6. How to Extend or Pick Up the Work

A new session should:

1. **Read this document first.** It contains everything needed to avoid re-deriving technical context.

2. **Check the dataset version.** Open `mishnah_db.json` and read `_meta.version` — this tells you what revision is live. If it says `2026-05-rev3`, Pass 3 hasn't run yet.

3. **Use the pilots as reference implementations.** The two files in `pilot/` show the exact HTML patterns any new rendering should match: table structure, class usage, subdivision markers, Subunit spans.

4. **Use the template scaffolding as source of truth.** `_templates/Academic-Content-*.html` defines page structure. Region content goes into the placeholders — no DWT markers, no meta/OG in the template itself.

5. **Run the extractor, don't rewrite it.** `_pilot/mishnah_extractor_v2.py` is verified to produce correct output. Import its functions or invoke it from the command line.

6. **Maintain read-only-by-default discipline.** Report first, modify only after explicit approval from Moshe. Never edit deployed files in place — draft in a working folder, Moshe deploys via Expression Web + GitHub Desktop.

---

## 7. Known Issues / Open Questions

- **`hebrew-leviticus-unit-19.html` corruption:** 21,117 bytes of valid content + 381,779 bytes of null padding (95%). The valid content is 504 bytes larger than git HEAD, meaning it was actually modified before the padding was appended. Needs manual review of the modification before cleaning.

- **Null-byte corruption mechanism:** Diagnosed as a Cowork sandbox mount-layer artifact — occurs when files are written through the Linux→Windows path mapping. Pre-allocated buffers leave trailing nulls when the actual content is shorter. Mitigation: strip trailing nulls after any sandbox write; or use temp-file + atomic rename. Should not recur in normal (non-sandbox) operation.

- **`_redirects` had similar corruption** earlier (cleaned in Phase 2, has not recurred).

- **Academic-Content-EN template untested:** Only the HE variant has been piloted end-to-end. The EN template should be tested before broad migration of the 214 English pages.

- **Hebrew navigation labels:** The template nav currently shows English text. Hebrew pages need translated nav labels — this is an open design decision (separate HE nav, dynamic switching, or accept English nav on Hebrew pages).

- **Mishnah number convention:** The docx includes `(א)`, `(ב)` etc. in cell text. The existing JSON strips them. Pass 3 needs to decide: preserve (for rendering), strip (for backward compatibility), or add as a separate field.

- **54 legacy DWT pages:** The `legacy-audit.csv` has recommendations (keep/retire/migrate) but no action has been taken yet. Low priority.

- **`internalparallel` CSS class:** The Torah HTML pages don't use this class (it's Mishnah-only). Needs verification that main.css has a rule for it — or one needs to be added.

---

## 8. Pass 6 — Full Re-extraction with v2.1.4 (2026-05-11)

### What changed

Full corpus re-extraction with extractor v2.1.4 against a freshly updated source docx. The live `Mishnah-New/English/mishnah_db.json` was promoted from `2026-05-rev7` to `2026-05-rev8`. Total markers increased by **+3,385** (7,020 → 10,405). Chapters with markers increased by **+13** (297 → 310). The dataset now has **525 keys** (524 chapters with `sotah_9` split into `sotah_9a` and `sotah_9b`).

### Extractor changes (v2.1.3 → v2.1.4)

- `TABLE_OVERRIDES` constant pins specific docx tables when duplicate `(tractate, chap)` resolution would otherwise pick the wrong one. Currently contains a single entry: `shabbat_22 → ti=110`. (The duplicate for shabbat_22 has since been eliminated in the docx itself, so the override is now defensive.)
- `sotah_9` split: `build_table_index` keys tables whose `chapter_text` contains `חלק א` / `חלק ב` as `sotah_9a` / `sotah_9b` respectively. The unified `sotah_9` key is not produced. `extract_all_chapters_from_json` suppresses the live `sotah_9` key (no placeholder) and emits fresh `sotah_9a` / `sotah_9b` entries inheriting metadata from the live `sotah_9` entry, with a new `chapter_part_he` field on each half.

### Scholarly review — six duplicate-table decisions

| Chapter | Decision | How v2.1.4 handles it |
|---|---|---|
| `middot_1` | Use later table (3×3) | Last-write-wins; docx update eliminated the duplicate |
| `middot_2` | Use later table (5×2) | Last-write-wins; docx update eliminated the duplicate |
| `kelim_4` | Use later table (2×3) | Last-write-wins; docx update eliminated the duplicate |
| `shabbat_22` | Use EARLIER table (ti=110, 3×2, 10 markers) | `TABLE_OVERRIDES` (defensive — docx update also eliminated the duplicate) |
| `zevachim_5` | Palindrome `[1,2,3,2,1]` cells per row | Moshe relabelled mislabelled `5ג` → `5` in docx; duplicate eliminated, single table now extracts the palindrome shape |
| `sotah_9` | Split into two scholarly chapters | New `sotah_9` split logic; emits `sotah_9a` (36 markers, חלק א) and `sotah_9b` (55 markers, חלק ב) |

### Dataset state — Pass 6

- **Live JSON:** `Mishnah-New/English/mishnah_db.json`, version `2026-05-rev8`
- **Total keys:** 526 (525 chapter entries + `_meta`)
- **Sotah split:** 524 original chapters minus 1 (`sotah_9`) plus 2 (`sotah_9a`, `sotah_9b`) = 525
- **Chapters with markers:** 310 (vs rev7's 297, delta +13)
- **Total markers:** 10,405 (vs rev7's 7,020, delta +3,385)
- **Missing-from-docx:** 2 — `ketubot_14`, `yadayim_4` (down from rev7's investigation that flagged ketubot_14, yadayim_4, sukkah_3; sukkah_3 was restored in the docx for Pass 6)
- **Marker types:** 8 canonical only (no `internal_parallel` / `chiastic1` / `chiastic2`)
- **Header rule firings:** 13 firings across 9 unique chapters (avot_1 has 5 — chain-of-tradition pattern)
- **No duplicate `(tractate, chap)` clashes** in the new docx (all upstream-fixed)

### Known open issues (after Pass 6)

- `nazir_8` docx typo: header cell reads `סכת נזיר` (missing the leading `מ`). v2.1.3+'s tolerant matcher handles this via fallback. Should be fixed in the docx upstream eventually.
- 311 vs 297 marker-count discrepancy: Claude in Word reported 311 chapters with colored highlights in the docx; the new dataset has 310. Close, but not byte-identical. Deferred for investigation.
- `_meta.description` still says "all 524 chapters" — superseded by 525 entries after the sotah split. Minor wording; can be updated when convenient.

### Files touched (Pass 6)

- `_pilot/mishnah_extractor_v2.py` — v2.1.4
- `Mishnah-New/English/mishnah_db.json` — promoted from rev7 to rev8 (byte-identical to staged before promotion)
- `_pilot/MIGRATION-STATE.md` — this update
- `_pilot/pass-6-report.md` — new
- `_pilot/stage-a-revised-report.md` — created during the prior session (v2.1.3 extraction)
- `_pilot/stage-a-report.md` — historical record of the halted v2.1.2 attempt
- `_pilot/mishnah_db_reextracted.json` — staged file left in place (the bash mount rejected the deletion); safe to delete manually

### What's next

- Stage B (planned but not started): comprehensive diff of the dataset against any external sources of truth (e.g., the 311 vs 310 reconciliation).
- Hebrew chapter page regeneration with marker spans (now unblocked — Pass 3's prerequisite met).

---

## 9. Pass 6 re-run — rev8 → rev9 (2026-05-11)

Re-run of Pass 6 against an updated docx (May 11 09:30, sourced from the Research folder rather than the upload, so the canonical KDP location is now the build input). The docx fixes targeted the two remaining missing chapters and a layout error:

- **ketubot_14 added** as a 2×3 table (`[[1,1,1],[1,1,1]]`); 0 markers (structurally populated, no styled text yet).
- **yadayim_3 corrected** from a 6-row table that conflated ch.3 and ch.4 to a clean 3×2 table (`[[2,2],[2,2],[2,2]]`); 0 markers.
- **yadayim_4 separated** as its own 2×2 table (`[[2,2],[2,2]]`); 0 markers.

The v2.1.4 extractor was unchanged — no code edits this round. Just a clean re-extraction against the corrected docx, byte-identical promotion to live.

### Headline numbers — rev8 → rev9

| Metric | rev8 | rev9 | Δ |
|---|---:|---:|---:|
| Total chapters | 525 | 525 | 0 |
| Matched chapters | 523 | **525** | +2 |
| Missing-from-docx | 2 (ketubot_14, yadayim_4) | **0** | −2 |
| Chapters with markers | 310 | 310 | 0 (three new chapters have no styled text yet) |
| Total markers | 10,405 | 10,405 | 0 |
| Duplicate-table conflicts | 0 | 0 | 0 |

`yadayim_3` is no longer 6 rows; it is now the intended 3 rows of 2 cells each. `yadayim_4` exists as its own entry. `ketubot_14` exists as its own entry. All three are populated and free of `_missing_from_docx`.

### Files touched (this re-run)

- `Mishnah-New/English/mishnah_db.json` — rev8 → rev9 (byte-identical to staged before promotion). sha256 `5500c5e6bd018c96…`.
- `_pilot/MIGRATION-STATE.md` — this section.
- `_pilot/pass-6-rerun-report.md` — new short report.
- `_pilot/mishnah_db_reextracted.json` — staged file left in place (mount rejected deletion); byte-identical to live, safe to delete manually.

### Known open issues (still)

- `nazir_8` docx typo (`סכת נזיר`) — handled by v2.1.3+ fallback; should be fixed upstream eventually.
- 311 vs 310 marker-chapter-count discrepancy — deferred.
- `_meta.description` still says "all 524 chapters" — wording carryover; `total_chapters` correctly reports 525.
