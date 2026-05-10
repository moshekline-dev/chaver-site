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
