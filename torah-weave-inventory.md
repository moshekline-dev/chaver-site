# /torah-weave/ Directory Inventory

**Date:** 2026-05-08  
**Scope:** Read-only inventory of `/torah-weave/` in the chaver-site repo  
**Companion document:** `woven-torah-audit.md` (same date)

---

## 1. Directory Structure

**Total size:** 215 MB  
**Total files:** 491 (excluding `_vti_cnf` metadata)  
**HTML pages:** 289  
**Directories:** 212 (excluding `_vti_cnf`)

### Top-Level Directories (10, excluding `_vti_cnf`)

| Directory | Contents |
|-----------|----------|
| Admin/ | CSS (`main.css`, 3,824 lines), images, JS, color-code pages, slide shows |
| Commentary/ | 2 commentary HTML files (Commentary.html, Torah Map Commentary.html) |
| Deuteronomy/ | 13 unit dirs + 13 Hebrew unit dirs + map dir |
| Exodus/ | 19 unit dirs + 19 Hebrew unit dirs + map dir |
| Genesis/ | 19 unit dirs + 19 Hebrew unit dirs + map dir + analysis dir + extras |
| Leviticus/ | 22 unit dirs + 22 Hebrew unit dirs + map dir + analysis dir |
| NotebookLM-Genesis/ | 46 `.txt` files — plain-text exports for NotebookLM ingestion |
| Numbers/ | 13 unit dirs + 13 Hebrew unit dirs + map dir |
| data/ | `torah-units.json`, `torah-units.csv`, `index.html` |
| introduction/ | PDF, slide shows (Woven Torah slides, Decalogue presentation), hidden-matrix page |

### Top-Level HTML Files (16)

| File | Title |
|------|-------|
| `index.html` | Redirect → Torah Portal |
| `overview.html` | Fifty Gates: The Architecture of the Torah |
| `commentary.html` | Torah Weave Commentary |
| `Woven-Torah-Method.html` | The Woven Torah: A Two-Dimensional Reading of the Five Books of Moses |
| `The-Sixth-Book-of-theTorah.html` | The Voice Is the Voice of YHWH, and the Hands Are the Hands of Elohim |
| `bible-contradictions-explained.html` | Bible Contradictions Explained Through Structure |
| `book-of-numbers-camp-map.html` | The Book of Numbers Is a Map of the Camp |
| `cain-and-abel-two-fathers.html` | Why Was Cain's Offering Rejected? |
| `documentary-hypothesis-alternative.html` | Beyond JEDP: A Structural Alternative to the Documentary Hypothesis |
| `leviticus-19-ark-at-the-center.html` | Love Your Neighbor Is Not a Standalone Law: The Hidden Structure of Leviticus 19 |
| `six-days-of-creation-picture.html` | The Six Days of Creation Are a Picture |
| `ten-commandments-two-tablets.html` | The Ten Commandments Were Not a List: Why Two Tablets? |
| `ten-plagues-creation-in-reverse.html` | The Ten Plagues Are Creation in Reverse |
| `who-wrote-the-bible-theories-compared.html` | Who Wrote the Bible? Four Theories of Authorship Compared |
| `why-two-names-for-god.html` | Why Does God Have Two Names in the Bible? |
| `yhwh-and-elohim-two-names.html` | Why Does God Have Two Names in the Bible? (duplicate/variant) |

---

## 2. Technology Stack

All pages use **Expression Web Dynamic Web Templates (DWT)**:
- Template: `Academic-Content-DWT.dwt`
- `<!-- #BeginTemplate -->` / `<!-- #EndTemplate -->` markers
- `<!-- #BeginEditable -->` / `<!-- #EndEditable -->` content regions
- Styling from `Admin/Assets/CSS/main.css` (3,824 lines)
- Clean semantic HTML with structural marker classes (`horizontal1`, `vertical1`, `closure`, `ciasm1`, `ciasm2`)
- Google Analytics via gtag.js

---

## 3. Torah Unit Pages by Book

### Genesis (most developed)

| Content Type | Count | File Naming |
|--------------|-------|-------------|
| Unit texts | 19 | `genesis-unit-N/genesis-unit-N.html` |
| Unit commentaries | 19 | `genesis-unit-N/genesis-unit-N-commentary.html` |
| Hebrew units | 19 | `hebrew-genesis-unit-N/index.html` (units 2–19), `hebrew-genesis-unit-1/hebrew-genesis-unit-1.html` (unit 1) |
| Map | 1 | `genesis-map/genesis-map.html` |
| Map commentary | 1 | `genesis-map/genesis-map-commentary.html` |
| Analysis pages | 10 | See Section 4 below |

**Extra Genesis content:**
- `Units without DWT/` — 19 bare unit files (no DWT template attached)
- `genesis-unit-1-commentary/index.html` — standalone commentary directory (separate from in-unit copy)
- `genesis-unit-12-261-33-revealing-isaacs-independence/index.html` — extended Genesis 12 commentary
- `genesis-unit-9/Akedah-divine-names-essay.html` — Akedah divine names essay (also at `Akedah divine names essay.html` with spaces)

### Exodus

| Content Type | Count | File Naming |
|--------------|-------|-------------|
| Unit texts | 19 | `exodus-unit-N/exodus-unit-N.html` |
| Unit commentaries | 0 | — |
| Hebrew units | 19 | `hebrew-exodus-unit-N/index.html` |
| Map | 1 | `exodus-map/index.html` |
| Analysis pages | 0 | No `exodus-analysis/` directory |

### Leviticus

| Content Type | Count | File Naming |
|--------------|-------|-------------|
| Unit texts | 22 | `leviticus-unit-N/leviticus-unit-N.html` |
| Unit commentaries | 4 | Units 1, 2, 3, 22 (double-dash naming: `leviticus--unit-N-commentary.html`) |
| Hebrew units | 22 | `hebrew-leviticus-unit-N/index.html` |
| Map | 1 | `leviticus-map/index.html` |
| Analysis pages | 5 | See Section 4 below |

**Note:** Commentary filenames use a double dash (`leviticus--unit-N-commentary`), unlike Genesis (`genesis-unit-N-commentary`).

### Numbers

| Content Type | Count | File Naming |
|--------------|-------|-------------|
| Unit texts | 13 | `numbers-unit-N/index.html` |
| Unit commentaries | 0 | — |
| Hebrew units | 13 | `hebrew-numbers-unit-N/index.html` |
| Map | 1 | `numbers-map/index.html` |
| Analysis pages | 0 | — |

**Note:** Numbers unit pages use `index.html` naming (not `numbers-unit-N.html`).

### Deuteronomy

| Content Type | Count | File Naming |
|--------------|-------|-------------|
| Unit texts | 12 | `deuteronomy-unit-N/index.html` (units 1–7, 9–13; unit 8 has no text page) |
| Unit commentaries | 8 | All in `deuteronomy-unit-8/` (multi-part Decalogue commentary suite) |
| Hebrew units | 13 | `hebrew-deuteronomy-unit-N/index.html` |
| Map | 1 | `deuteronomy-map/index.html` |
| Analysis pages | 0 | — |

**Note:** Deuteronomy unit pages use `index.html` naming. Unit 8 has no unit text page — the directory contains only the 8-part commentary suite.

### Unit Coverage Summary

| Book | Unit Texts | Commentaries | Hebrew Units | Map | Analysis |
|------|-----------|--------------|--------------|-----|----------|
| Genesis | 19 | 19 | 19 | Yes + commentary | 10 pages |
| Exodus | 19 | 0 | 19 | Yes | 0 |
| Leviticus | 22 | 4 | 22 | Yes | 5 pages |
| Numbers | 13 | 0 | 13 | Yes | 0 |
| Deuteronomy | 12 | 8 (Unit 8 suite) | 13 | Yes | 0 |
| **Total** | **85** | **31** | **86** | **5** | **15** |

---

## 4. Analysis Pages

### Genesis Analysis (`Genesis/genesis-analysis/`)

| File | Description |
|------|-------------|
| `units-of-genesis.html` | Part A: Units of Genesis |
| `the-map-of-genesis.html` | Part B: The Map of Genesis |
| `the-three-rows.html` | Part C: The Three Rows |
| `architecture-and-meaning-in-genesis.html` | Part D: Architecture and Meaning in Genesis |
| `overview.html` | Genesis series overview |
| `the-hidden-warp.html` | The Hidden Warp |
| `The Structure of Genesis.html` | Full structure essay |
| `The Structure of Genesis1.html` | Variant/copy |
| `The Structure of Genesis (short form).html` | Short-form version |
| `The Structure of Genesis from Gemini.html` | Gemini-generated version |

### Leviticus Analysis (`Leviticus/leviticus-analysis/`)

| File | Description |
|------|-------------|
| `units-of-leviticus.html` | Part A: Units of Leviticus |
| `leviticus-map.html` | Part B: The Map (serves as Leviticus map page) |
| `the-three-rows.html` | Part C: The Three Rows |
| `architecture-and-meaning-in-leviticus.html` | Part D: Architecture and Meaning |
| `overview.html` | Leviticus series overview |

---

## 5. Insights Articles (Top-Level)

These are SEO-targeted "Insights" articles at the top level of `/torah-weave/`:

| File | Topic |
|------|-------|
| `bible-contradictions-explained.html` | Bible contradictions as structural features |
| `book-of-numbers-camp-map.html` | Numbers as a camp map |
| `cain-and-abel-two-fathers.html` | Cain's offering rejection |
| `documentary-hypothesis-alternative.html` | Alternative to JEDP |
| `leviticus-19-ark-at-the-center.html` | Leviticus 19 structure |
| `six-days-of-creation-picture.html` | Creation days as a table |
| `ten-commandments-two-tablets.html` | Decalogue structure |
| `ten-plagues-creation-in-reverse.html` | Plagues as reverse creation |
| `who-wrote-the-bible-theories-compared.html` | Bible authorship theories |
| `why-two-names-for-god.html` | Two divine names |
| `yhwh-and-elohim-two-names.html` | Two divine names (variant) |

**Note:** `why-two-names-for-god.html` and `yhwh-and-elohim-two-names.html` share the same title. One may be a redirect or variant.

---

## 6. Hebrew Content

**86 Hebrew unit directories** across all five books (matching the 86 Torah units exactly):

| Book | Hebrew Dirs | File Naming |
|------|-------------|-------------|
| Genesis | 19 | `hebrew-genesis-unit-N/` |
| Exodus | 19 | `hebrew-exodus-unit-N/` |
| Leviticus | 22 | `hebrew-leviticus-unit-N/` |
| Numbers | 13 | `hebrew-numbers-unit-N/` |
| Deuteronomy | 13 | `hebrew-deuteronomy-unit-N/` |

Hebrew units use RTL markup (`dir="rtl"`, `lang="he-IL"`) and DWT templates. No Hebrew analysis pages or commentaries exist at `/torah-weave/`.

---

## 7. Supporting Assets

### Admin Directory

| Path | Contents |
|------|----------|
| `Admin/Assets/CSS/main.css` | Master stylesheet (3,824 lines) |
| `Admin/Assets/JS/torah-weave-slideshow.js` | Slideshow script |
| `Admin/Assets/Images/` | 7 images (site branding, reading diagrams, book cover) |
| `Admin/Assets/english-color-code.html` | English color-code reference |
| `Admin/Assets/hebrew-color-code.html` | Hebrew color-code reference |
| `Admin/Assets/Slide-Shows/` | 3 slide show directories (beautiful-weave, decalogue, genesis-matrix), 51 total files |

### Data Directory

| File | Description |
|------|-------------|
| `data/torah-units.json` | Machine-readable Torah unit data |
| `data/torah-units.csv` | Spreadsheet-compatible Torah unit data |
| `data/index.html` | Data landing page |

### Introduction Directory

| Path | Contents |
|------|----------|
| `introduction/The_Woven_Torah.pdf` | Introductory PDF |
| `introduction/hidden-matrix.html` | Hidden matrix interactive page |
| `introduction/woven-torah-slides/` | 15 JPG slide images + `index.html` |
| `introduction/decalogue-presentation/` | 15 slide images (PNG + WebP) + `decalogue-woven-code.html` |

### Commentary Directory

| File | Description |
|------|-------------|
| `Commentary/Commentary.html` | Commentary page |
| `Commentary/Torah Map Commentary.html` | Torah Map commentary |

### NotebookLM-Genesis Directory

46 `.txt` files — plain-text exports of Genesis units, commentaries, and analysis pages for NotebookLM AI ingestion. Includes `main.txt.txt` (CSS export).

### File Type Breakdown

| Type | Count |
|------|-------|
| HTML | 289 |
| WebP | 92 |
| TXT | 45 |
| PNG | 35 |
| JPG | 16 |
| PDF | 6 |
| CSS | 2 |
| Other (JS, JSON, CSV, XLSX, MD, BAT) | 6 |

---

## 8. Sitemap Coverage

**122 `/torah-weave/` URLs** in `sitemap.xml`:

| Category | Count | Notes |
|----------|-------|-------|
| Insights articles | 11 | All top-level article pages |
| Structural pages | 5 | commentary, overview, architecture-of-the-torah, Woven-Torah-Method, data/ |
| Introduction pages | 3 | decalogue presentation, hidden-matrix, woven-torah-slides |
| Genesis unit texts | 19 | All 19 |
| Genesis commentaries | 19 | All 19 |
| Genesis analysis | 6 | overview, units, map, three-rows, architecture, hidden-warp |
| Akedah essay | 1 | `Genesis/genesis-unit-9/Akedah-divine-names-essay` |
| Exodus unit texts | 19 | All 19 |
| Leviticus unit texts | 13 | Units 1–13 (not 14–22) |
| Leviticus commentaries | 4 | Units 1, 2, 3, 22 |
| Leviticus analysis | 5 | All 5 |
| Deuteronomy commentaries | 8 | Unit 8 suite (all 8 pages) |
| **Total** | **122** | |

**Not in sitemap:** Numbers unit texts (13), Deuteronomy unit texts (12), Leviticus units 14–22 (9), all 86 Hebrew units, all 5 map pages, NotebookLM files, Admin assets.

---

## 9. Anomalies and Notes

1. **Duplicate divine-names articles:** `why-two-names-for-god.html` and `yhwh-and-elohim-two-names.html` share the same title. Both are in the sitemap.

2. **Leviticus commentary double-dash naming:** Files use `leviticus--unit-N-commentary.html` (double dash) instead of the `leviticus-unit-N-commentary.html` pattern used by Genesis.

3. **Numbers/Deuteronomy use `index.html` naming:** These books use `unit-N/index.html` rather than `unit-N/book-unit-N.html`. This means clean URLs work naturally but naming is inconsistent with Genesis/Exodus/Leviticus.

4. **Deuteronomy Unit 8 has no text page:** Only commentary pages exist in the directory (8 files). No `deuteronomy-unit-8.html` or `index.html` for the unit text itself.

5. **Genesis "Units without DWT" directory:** Contains 19 bare unit HTML files without DWT attachment — likely working copies or pre-template originals.

6. **Genesis Unit 12 extended commentary directory:** `genesis-unit-12-261-33-revealing-isaacs-independence/` exists at the Genesis level alongside the standard `genesis-unit-12/` directory.

7. **Genesis Unit 9 has two Akedah essay copies:** One with spaces in the filename (`Akedah divine names essay.html`), one with dashes (`Akedah-divine-names-essay.html`). Only the dashed version is in the sitemap.

8. **`architecture-of-the-torah` in sitemap but no file by that name:** The sitemap references `/torah-weave/architecture-of-the-torah` but no file with that exact name exists. Likely resolves to `overview.html` (titled "Fifty Gates: The Architecture of the Torah") via a redirect or Cloudflare rule.

9. **NotebookLM exports are development artifacts:** 46 plain-text files for AI ingestion, not public-facing content.

---

## 10. Comparison: /torah-weave/ vs /woven-torah/

| Content Type | /torah-weave/ | /woven-torah/ | Status |
|--------------|---------------|---------------|--------|
| **Technology** | DWT + main.css | Static WordPress/Elementor export | torah-weave is production |
| **Total size** | 215 MB | 495 MB | woven-torah 82% WordPress baggage |
| **Total HTML pages** | 289 | 248 | — |
| | | | |
| **Genesis unit texts** | 19 | 19 | Redundant — torah-weave is canonical |
| **Exodus unit texts** | 19 | 19 | Redundant — torah-weave is canonical |
| **Leviticus unit texts** | 22 | 22 | Redundant — torah-weave is canonical |
| **Numbers unit texts** | 13 | 13 | Redundant — torah-weave is canonical |
| **Deuteronomy unit texts** | 12 | 13 | Redundant — torah-weave is canonical |
| | | | |
| **Genesis commentaries** | 19 | 0 | torah-weave only |
| **Leviticus commentaries** | 4 | 0 | torah-weave only |
| **Deut Unit 8 commentary suite** | 8 | 0 | torah-weave only |
| **Akedah divine names essay** | 1 | 0 | torah-weave only |
| **Genesis map commentary** | 1 | 0 | torah-weave only |
| | | | |
| **Genesis analysis (Parts A–D + extras)** | 10 | 0 | torah-weave only |
| **Leviticus analysis (Parts A–D + overview)** | 5 | 0 | torah-weave only |
| | | | |
| **Insights articles** | 11 | 0 | torah-weave only |
| **"Sixth Book of Torah" essay** | 1 | 0 | torah-weave only |
| **Woven-Torah-Method article** | 1 | 0 | torah-weave only |
| **overview / commentary / data pages** | 3 | 0 | torah-weave only |
| | | | |
| **Hebrew unit texts** | 86 | 85 | Redundant — both copies exist |
| **Hebrew article pages** | 0 | 20 | **ONLY COPY — do not redirect** |
| | | | |
| **Book maps** | 5 (Gen has named file; others use index.html) | 5 (all in sitemap pointing to woven-torah) | Both exist; sitemap currently points to woven-torah maps |
| | | | |
| **Extended English commentaries** | 0 at top level | 3 (Creation Weave, Genesis 12, Decalogue/Avot) | **ONLY COPY — do not redirect** |
| | | | |
| **Interactive features (verse toggle, color legend)** | No | Yes (jQuery-based) | **ONLY COPY — do not redirect** |
| | | | |
| **Introduction / slides** | 3 presentations + PDF | 0 | torah-weave only |
| **Data files (JSON, CSV)** | Yes | 0 | torah-weave only |
| **NotebookLM exports** | 46 .txt files | 0 | torah-weave only |
| **Admin (CSS, JS, images)** | main.css + assets | WordPress infrastructure (404 MB) | Completely different stacks |
| | | | |
| **WordPress infrastructure** | None | wp-content (404 MB), wp-includes (32 MB) | woven-torah only |
| **About page** | No | Yes | Equivalent exists on main site |
| **Color code guide** | In Admin/Assets/ | Yes (standalone page) | Equivalent exists |
| **Intro to Torah maps** | In introduction/ | Yes | Overlapping content |
| **Learn / Rules pages** | No | Yes | woven-torah only |
| **Research articles index** | No | Yes | woven-torah only |

### Key Findings

1. **torah-weave is the canonical production directory.** All sitemap URLs, DWT templates, and `main.css` styling originate here. The woven-torah directory is a legacy WordPress export.

2. **Unit texts are fully redundant.** All 86 unit texts exist in both directories. The torah-weave versions are canonical (clean HTML, DWT, structural markers).

3. **Commentaries, analysis, and insights exist only at torah-weave.** The 31 commentaries, 15 analysis pages, and 11 insights articles have no woven-torah equivalent.

4. **20 Hebrew article pages exist only at woven-torah.** These are manually authored Hebrew translations of research articles (Leviticus 19 in 3 parts, YHWH voice essay, Avot pairs, Decalogue study, full Torah map, etc.). No equivalent exists at torah-weave.

5. **3 extended English commentaries exist only at woven-torah.** The Creation Weave methodology essay (`biblical-literary-units-the-creation-weave/`), extended Genesis 12 commentary, and Decalogue/Avot literary tables article have no torah-weave equivalent.

6. **Interactive features (verse number toggle, color legend toggle) exist only at woven-torah.** These jQuery-based features have no equivalent in the static torah-weave pages.

7. **Book maps exist in both directories.** The sitemap currently indexes the woven-torah map URLs, even though torah-weave map pages also exist. If woven-torah maps are redirected, the sitemap must be updated to point to torah-weave maps.
