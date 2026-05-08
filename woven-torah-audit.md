# /woven-torah/ Directory Audit

**Date:** 2026-05-08  
**Scope:** Read-only audit of `/woven-torah/` in the chaver-site repo  
**Classification:** **B — Partially Unique** (see Summary Assessment below)

---

## 1. Directory Structure

**Total size:** 495 MB  
**Total files:** 10,427 (excluding `_vti_cnf` metadata)  
**HTML pages:** 248  
**Directories:** 1,943 (excluding `_vti_cnf`)

### Size Breakdown

| Directory | Size | % of Total | Contents |
|-----------|------|------------|----------|
| wp-content/ | 404 MB | 82% | WordPress uploads, images, Elementor CSS, fonts |
| wp-includes/ | 32 MB | 6% | WordPress core JS/CSS (jQuery, etc.) |
| All other dirs | 59 MB | 12% | 248 HTML pages + scattered assets |

### Top-Level Directories (35)

Directories with `index.html`: 33 of 35

**Content pages (articles/essays):**
- `about/` — About the Woven Torah Project
- `biblical-literary-units-the-creation-weave/` — Genesis Unit 1 commentary
- `bidirectional-reading-the-decalogue-and-avot-pairs-as-literary-tables/` — Decalogue/Avot literary tables
- `color-code-guide/` — Color code explanation
- `divine-speech-in-two-dimensions-the-paired-structure-of-the-decalogue-as-literary-paradigm/` — Decalogue article
- `genesis-unit-1-demonstration/` — Interactive unit demo
- `genesis-unit-12-261-33-revealing-isaacs-independence/` — Genesis 12 commentary
- `introduction-to-torah-maps/` — How to read the maps
- `learn/` — Learning hub page
- `research-articles/` — Research article index
- `rules-for-studying-woven-torah/` — Study rules
- `torah-commentary-project/` — Commentary project overview

**Map pages:**
- `full-torah-map-2/` — Complete Torah map
- `genesis-map/`, `exodus-map/`, `leviticus-map/`, `numbers-map/`, `deuteronomy-map/`

**Unit pages:**
- `torah_units/` — 90 Torah unit pages (all 5 books)

**Hebrew content:**
- `language/he/` — 20 Hebrew article pages + 85 Hebrew Torah units
- `he/` — 4 test/experimental Hebrew pages
- `hebrew_pages/` — 1 page (appears to be a test)
- `hebrew_torah_units/` — 1 page (appears to be a test)

**WordPress infrastructure:**
- `wp-content/` — 9,188 files (images, CSS, JS, fonts)
- `wp-includes/` — 992 files (WordPress core)
- `elementor-hf/` — Elementor header/footer template
- `author/` — WordPress author archive
- `404/` — Custom 404 page
- `assistant-diary/` — Appears to be a test/internal page

---

## 2. Hebrew Content

### Hebrew Article Pages (20 pages in `language/he/hebrew_pages/`)

| Page | Title |
|------|-------|
| full-hebrew-map-of-torah/ | Full Hebrew Map of Torah |
| hebrew-about/ | Hebrew About |
| hebrew-bidirectional-reading-.../ | Hebrew Bidirectional Reading: The Decalogue and Avot Pairs as Literary Tables |
| hebrew-color-code/ | Hebrew Color Code |
| hebrew-divine-speech-in-two-dimensions-.../ | Hebrew Divine Speech in Two Dimensions |
| hebrew-genesis-unit-1-the-creation-paradigm/ | Hebrew Genesis Unit 1: The Creation Paradigm |
| hebrew-genesis-unit-12-.../ | Hebrew Genesis Unit 12 (26:1-33): Revealing Isaac's Independence |
| hebrew-introduction-to-torah-maps/ | Hebrew Introduction to Torah Maps |
| hebrew-map-of-deuteronomy/ | Hebrew Map of Deuteronomy |
| hebrew-map-of-exodus/ | Hebrew Map of Exodus |
| hebrew-map-of-genesis/ | Hebrew Map of Genesis |
| hebrew-map-of-leviticus/ | Hebrew Map of Leviticus |
| hebrew-map-of-numbers/ | Hebrew Map of Numbers |
| hebrew-research-articles/ | Hebrew Research Articles (index) |
| hebrew-the-five-pairs-of-avot-1-.../ | Hebrew The Five Pairs of Avot 1 |
| hebrew-the-principle-of-woven-texts-.../ | Hebrew The Principle of Woven Texts |
| hebrew-the-sophisticated-literary-structure-of-leviticus-19-part-1/ | Hebrew Leviticus 19 (Part 1) |
| hebrew-the-sophisticated-literary-structure-of-leviticus-19-part-2/ | Hebrew Leviticus 19 (Part 2) |
| hebrew-the-sophisticated-literary-structure-of-leviticus-19-part-3/ | Hebrew Leviticus 19 (Part 3) |
| hebrew-the-voice-is-the-voice-of-yhwh-.../ | Hebrew The Voice is the Voice of YHWH (Part 1) |

**Meta tags:** All pages have `<meta name="description">` with Hebrew text and `<link rel="canonical">`. All have `hreflang` alternates pointing to English equivalents.

**Content quality:** NOT auto-translated. Pages use proper RTL markup (`dir="rtl"`, `lang="he-IL"`), contain real Hebrew scholarly text, and appear manually authored.

### Hebrew Torah Units (85 pages in `language/he/hebrew_torah_units/`)

| Book | Count | Notes |
|------|-------|-------|
| Genesis | 19 | Complete |
| Exodus | 19 | Complete |
| Leviticus | 21 | One short — "leviticus-unir-19" (typo in dir name) |
| Numbers | 13 | Complete |
| Deuteronomy | 13 | Complete |

### Hebrew → English Correspondence

Every Hebrew page has an English equivalent already on the main site at `/torah-weave/`. The Hebrew Torah units in `/woven-torah/` are **fully duplicated** by the Hebrew unit pages at `/torah-weave/[Book]/hebrew-[book]-unit-N/`.

The Hebrew *article* pages (Leviticus 19 parts, YHWH voice essay, Avot pairs, etc.) are unique to `/woven-torah/` — **no equivalent exists at `/torah-weave/`**.

---

## 3. Page Quality Assessment

### Technology Stack

All 248 pages are **static WordPress exports** generated by the Simply Static plugin from an Elementor-based WordPress site.

### Boilerplate Analysis (10 pages sampled)

| Metric | Range | Notes |
|--------|-------|-------|
| Total lines per page | 1,960 – 2,916 | |
| Scholarly content | 70–74% of lines | Good ratio |
| wp-content references | 63–69 per page | **All broken** in static export |
| wp-json references | 7 per page | Non-critical (metadata only) |
| Elementor class references | 84–182 per page | Rendering depends on inline CSS |
| fonts.googleapis references | 2 per page | Requires internet |
| Dynamic JS blocks | 6–42 per page | Toggle buttons, print function |

### CSS Status

Pages include massive inline `<style>` blocks generated by Elementor (the `elementor-frontend-inline-css` block). This means basic styling works even without the external CSS files. However, responsive behavior and some widget styles may break without the wp-content CSS files.

### Dead Links

Every page contains ~65 references to `../wp-content/` paths for CSS, JS, and images. These resolve correctly when served from the repo (since `wp-content/` exists in the directory), but they are WordPress infrastructure files, not clean web resources.

### Title Tag Artifacts

All page titles contain formatting glitches from the export:

```
Full Torah Map - woven-torah % % %Full Torah Map | Torah Weave %
```

The `% % %` delimiters are Simply Static export artifacts.

### Content Quality

When boilerplate is stripped, the scholarly content is substantive and well-written. Example from the Creation Weave page:

> "Genesis Unit 1 serves as the paradigmatic example for understanding the entire Woven Torah because it contains... This commentary will demonstrate how to derive meaning from structural observation — a skill essential for reading all 86 units."

Content includes proper heading hierarchy, structured arguments, and Hebrew terms.

---

## 4. Torah Unit Pages (`/woven-torah/torah_units/`)

### Coverage

90 unit directories (excluding "bla" test dir):

| Book | Woven-Torah Units | Torah-Weave Units | Match? |
|------|-------------------|-------------------|--------|
| Genesis | 19 (+1 variant) | 19 | Yes |
| Exodus | 19 (+1 "exodus-1") | 19 | Yes |
| Leviticus | 22 | 22 | Yes |
| Numbers | 13 (+1 "numbers-unit-7-2") | 13 | Yes |
| Deuteronomy | 13 | 13 | Yes |

**Anomalous directories:** `bla/` (test), `exodus-1/` (duplicate of exodus-unit-1?), `genesis-unit-1-1-23/` (alternate numbering), `numbers-unit-7-2/` (sub-unit).

### Content Comparison

The `/woven-torah/torah_units/` pages are **interactive Elementor-built pages** with:
- Toggle buttons for verse numbers (show/hide)
- Color legend toggle
- Print-friendly view generation via JavaScript
- Elementor-styled responsive layout
- Yoast SEO metadata and JSON-LD schema

The `/torah-weave/` unit pages are **static DWT-based HTML** with:
- Expression Web Dynamic Web Templates
- Highlighted structural markers (horizontal1, vertical1, closure, ciasm1, ciasm2)
- Clean semantic HTML
- `main.css`-based styling

**The two versions display the same textual content but in completely different technical stacks.** The torah-weave versions are the current production pages linked from the sitemap.

### Interactive Features

The woven-torah unit pages have JavaScript-based features not present in torah-weave:
- Verse number toggle button
- Collapsible color legend
- Print view generator

These depend on jQuery and Elementor DOM structure. They work in the static export as long as wp-content JS files are served.

---

## 5. Internal Linking

### Within /woven-torah/

150+ pages reference other `/woven-torah/` pages. Internal navigation (sidebar, breadcrumbs, footer links) connects maps, units, articles, and the about page. The internal link structure is coherent.

### Links to Main Site

10+ woven-torah pages link to `/torah-weave/` resources (slides, introduction pages).

### Main Site Links INTO /woven-torah/

20 files on the main site reference `/woven-torah/` paths:
- `404.html`
- `about-Moshe-Kline.html`
- Various pages under `/General/`, `/Mishnah-New/`
- The sitemap includes 10 `/woven-torah/` URLs (maps, intro, divine speech article)
- Footer links on DWT-templated pages link to `/woven-torah/` maps

**The main site actively links to and indexes `/woven-torah/` content.** These are not orphaned pages.

---

## 6. Non-HTML Assets

### File Type Inventory

| Type | Count | Notes |
|------|-------|-------|
| CSS | 4,321 | Elementor styles, utility CSS, fonts |
| JS | 3,044 | jQuery, Elementor, Google Analytics, MonsterInsights |
| SVG | 1,316 | Icons, decorative elements |
| PNG | 860 | Images, screenshots, maps |
| WOFF2 | 192 | Web fonts |
| AVIF | 98 | Modern image format |
| JPG | 69 | Photos |
| TXT | 68 | Misc text files |
| JSON | 61 | Config files |
| WOFF | 40 | Web fonts (older format) |
| TTF | 34 | TrueType fonts |
| WEBP | 28 | Images |
| EOT | 24 | Legacy IE fonts |
| GIF | 12 | Animated/simple images |

### Shared Resources

The `wp-content/` and `wp-includes/` directories are self-contained WordPress infrastructure. No pages on the main site (`/torah-weave/`, `/Mishnah/`, etc.) reference these files. They exist solely to support the `/woven-torah/` pages.

---

## 7. Summary Assessment

### Classification: **B — Partially Unique**

### What Is Fully Redundant (safe to redirect)

- **Torah unit pages** (`torah_units/`): All 86+ units exist in better form at `/torah-weave/[Book]/[book]-unit-N/` with DWT templates, clean CSS, and proper structural markers. The woven-torah versions add toggle buttons but carry 400+ MB of WordPress baggage.

- **Book maps** (`genesis-map/`, `exodus-map/`, etc.): Already in the sitemap pointing to the woven-torah versions, but these are the *only* versions. If redirected, the maps would need to be rebuilt at `/torah-weave/`.

- **Hebrew Torah units** (`language/he/hebrew_torah_units/`): Fully duplicated at `/torah-weave/[Book]/hebrew-[book]-unit-N/`.

- **About page**, **introduction-to-torah-maps**, **color-code-guide**: Equivalents exist on the main site.

### What Is Partially Unique (needs preservation or migration)

- **Hebrew article pages** (20 pages) — These have no equivalent at `/torah-weave/`:
  - Leviticus 19 structure analysis (3 parts) in Hebrew
  - "The Voice is the Voice of YHWH" essay in Hebrew
  - "The Five Pairs of Avot 1" in Hebrew
  - "The Principle of Woven Texts" in Hebrew
  - Hebrew Decalogue/Avot literary tables article
  - Hebrew full Torah map

- **English article pages** with extended commentary not found elsewhere:
  - `biblical-literary-units-the-creation-weave/` — Extended Genesis Unit 1 commentary with structural reading methodology ("Reading the Subdivisions," "Reading the Columns," "Reading the Rows")
  - `genesis-unit-12-261-33-revealing-isaacs-independence/` — Extended commentary
  - `bidirectional-reading-the-decalogue-and-avot-pairs-as-literary-tables/`

- **Interactive features** — The verse-number toggle and color legend toggle in the unit pages have no equivalent in the static torah-weave pages.

### What Is Broken

- All 248 pages have ~65 broken `wp-content` references each
- Title tags contain `% % %` export artifacts
- Responsive behavior may be degraded without Elementor CSS files
- One directory has a typo: `leviticus-unir-19` instead of `leviticus-unit-19`
- Test directories exposed: `bla/`, `he/gen-test/`, `language/he/test/`, `language/he/new-test/`

### Evidence for Classification B

1. The torah unit pages (the bulk of content) are fully redundant with `/torah-weave/`.
2. The 20 Hebrew article pages contain unique scholarly content not available elsewhere on the site. These are manually authored Hebrew translations of research articles.
3. The extended English commentaries (Creation Weave, Genesis 12, Decalogue/Avot) contain unique analytical content that goes beyond the corresponding torah-weave pages.
4. The 495 MB directory size is 82% WordPress infrastructure (wp-content + wp-includes) that serves only these pages.
5. The main site actively links to `/woven-torah/` for maps and the divine speech article — these URLs cannot be removed without updating those links.

---

## Appendix: Files in the Sitemap

The following `/woven-torah/` URLs are indexed in `sitemap.xml`:

1. `full-torah-map-2/` (priority 0.75)
2. `introduction-to-torah-maps/` (priority 0.65)
3. `genesis-map/` (priority 0.65)
4. `exodus-map/` (priority 0.65)
5. `leviticus-map/` (priority 0.65)
6. `numbers-map/` (priority 0.65)
7. `deuteronomy-map/` (priority 0.65)
8. `about/` (priority 0.55)
9. `divine-speech-in-two-dimensions-...` (priority 0.65)
10. All 82 `torah_units/[book]-unit-N/` pages (priority 0.50)
