# Pre-Migration Survey of DWT-Attached Pages

**Date:** 2026-05-13
**Scope:** Read-only structural analysis of every DWT-attached page in the repo, to identify risks and edge cases before bulk-migrating to the new templates.
**Method:** Python script (`/tmp/survey.py`, kept at `_pilot/nav_css_cleanup.py`'s neighbor) walked the repo, parsed each file, recorded structural signals. No file modified.

---

## 1. Inventory Totals

**930 DWT-attached pages** (substantially more than the spec's expected ~500 — the corpus is larger than briefed). Walked 1,330 `.htm`/`.html` files outside `_*` directories; 930 had `<!-- #BeginTemplate`.

### By extension

| Extension | Count |
|---|---:|
| `.htm` | 630 |
| `.html` | 300 |
| **Total** | **930** |

### By detected language

| Language | Count |
|---|---:|
| HE | 709 (76%) |
| EN | 221 (24%) |

### By source DWT

| DWT | Count | Note |
|---|---:|---|
| `Academic-Content-DWT.dwt` | 877 | Main DWT, 5 regions, handled by current migration logic |
| `English.dwt` | **37** | **Not in current migration logic — needs handling** |
| `hebrew.dwt` | 16 | 4 regions including `start`→`content`; handled by current logic |

### By top-level directory × language

| Directory | EN | HE | Total |
|---|---:|---:|---:|
| `Mishnah-New` | 9 | **607** | 616 |
| `torah-weave` | 161 | 88 | 249 |
| `Torah-New` | 31 | 2 | 33 |
| `Mishnah` | 1 | 11 | 12 |
| `General` | 8 | 1 | 9 |
| `torah-commentary-project` | 7 | 0 | 7 |
| `(root)` | 3 | 0 | 3 |
| `Articles` | 1 | 0 | 1 |

### Language × DWT cross-tab

| Lang | DWT | Count |
|---|---|---:|
| EN | Academic-Content-DWT.dwt | 184 |
| EN | English.dwt | 37 |
| HE | Academic-Content-DWT.dwt | **693** |
| HE | hebrew.dwt | 16 |

The HE files predominantly use `Academic-Content-DWT.dwt`, not `hebrew.dwt`. The DWT is technically EN-style with 5 regions, but content/path indicate HE — confirming the MAVO pattern is the dominant case, not an exception.

---

## 2. Aggregate Findings By Risk Level

### HIGH risk (manual review needed before bulk migration) — 28 unique files

| Risk | Count | Notes |
|---|---:|---|
| Files using `English.dwt` (not in current migration logic) | 37 | Region set matches Academic-Content for 31 of these; 6 use a non-standard `writehere` region |
| Files with editable-region names outside the expected set (`writehere`) | 6 | All in `torah-commentary-project/Commentaries/` |
| Files missing the `content` region | 13 | Academic-Content-DWT pages where `content` editable region is absent — these are skeleton/test pages |
| Files missing `additional-styles` + `page-scripts` regions | 3 | hebrew.dwt pages (`Mishnah/Mesechet Peah.htm`, `Mishnah/Mesechet Shviit.htm`, `Mishnah/Mesechet Trumote.htm`) — only doctitle+start present |
| Files with no `<main>` tag | 9 | Heavy overlap with the missing-content-region set |
| Files with multiple `<footer>` tags in body | 4 | Listed individually below |
| Files with inline `style="width: Npx"` where N > 400 | 20 | Risk of mobile horizontal overflow |
| Files with `non_trivial_js_count ≥ 2` (custom JS beyond gtag/toggleMenu) | 24 | Likely schema.org JSON-LD + custom click handlers |

The 28-file deduplicated HIGH-risk count: every file fitting one or more of the above.

**Zero finding** for: `<iframe>` elements (0), `<img width="≥800">` attributes (0), `#InstanceBegin` markers (0). The corpus is consistent on these dimensions.

### MEDIUM risk (likely handled by existing migration logic but worth confirming on samples)

| Risk | Count | Notes |
|---|---:|---|
| `lang_mismatch` (declared lang ≠ detected lang) | **709** | Nearly all HE pages declare `lang="en"`. Migration logic correctly overrides via path/DWT detection; using HE template fixes this implicitly. |
| Files where `check_mobile_nav_not_hidden()` would FAIL before cleanup | **927** | Effectively every page has the orphan `nav ul { display: none }` rule. The cleanup utility from `_pilot/nav_css_cleanup.py` is **mandatory** for the bulk run. |
| Files with `<table class="matrix-table">` | 47 | Already covered by the new `.matrix-table` shrink-to-fit rule in `main.css` |
| Files with `<table class="scripture-table">` | 99 | NOT yet covered by a mobile rule — may overflow on mobile viewports (see recommendations) |
| Files with inline `<style>` block > 5 KB | 897 | Almost all pages have the full DWT-baked inline `<style>` (~13 KB). The cleanup utility will strip the orphan nav-targeting bits; the rest is content-specific styling that needs to be preserved verbatim. |
| Files with multiple inline `<style>` blocks | 25 | Rare; bulk script should handle by iterating all `<style>` blocks (the cleanup utility already does) |
| Files with `<header class="unit-header-section">` (content-area header) | 90 | Expected; these survive intact through migration |
| Files with `<nav class="unit-navigation">` (content-area nav) | 78 | Same — content-area landmarks are preserved |
| Files with multiple `<header>` tags in body | 110 | Almost always DWT-baked `<header class="site-header">` PLUS content's `<header class="unit-header-section">`. Both legitimate; not a real risk. |
| Files using `English.dwt` with standard regions | 31 | Same 5 regions as Academic-Content-DWT.dwt — should migrate identically once the DWT name is allowed in the migration script's whitelist |

### LOW risk (standard migration path) — ~870 files

The remainder: standard DWT-attached pages with all expected regions present, content-area landmarks preserved, no unusual JS, no oversized images, no iframes. These should migrate cleanly with the existing logic + the CSS cleanup pass.

---

## 3. HIGH Risk — Per-File Detail

### 3a. `English.dwt` pages with `writehere` region (6 files)

These have regions `{additional-styles, doctitle, page-scripts, writehere}` — no `content` or `meta`. The `writehere` region is the body content equivalent.

```
torah-commentary-project/Commentaries/index.html
torah-commentary-project/Commentaries/maps with commentary.html
torah-commentary-project/Commentaries/test2.html
torah-commentary-project/Commentaries/Deuteronomy/deuteronomy-unit-3.html
torah-commentary-project/Commentaries/Deuteronomy/index.html
torah-commentary-project/Commentaries/Deuteronomy/test.html
```

**Recommended handling:** migration script must add a new DWT type for `English.dwt`. For these 6 files, map `writehere` → `content` (similar to how `start` → `content` for hebrew.dwt). Note that `meta` will need to default to empty string (no `meta` region in this variant). The two `test*.html` files look like scratch/test pages — confirm with Moshe whether they should migrate or just be deleted.

### 3b. Academic-Content-DWT.dwt files missing `content` region (13 files)

These are skeleton/empty pages — they have the DWT scaffolding (`additional-styles`, `doctitle`, `meta`) but no `content` or `page-scripts` regions. Sizes range from 12 KB to 42 KB (the size is the DWT scaffolding, not page content).

```
torah-weave/Deuteronomy/deuteronomy-unit-2/deuteronomy-unit-2.html         13,001
torah-weave/Deuteronomy/hebrew-deuteronomy-unit-1/hebrew-deuteronomy-unit-1.html  19,861
torah-weave/Deuteronomy/hebrew-deuteronomy-unit-2/hebrew-deuteronomy-unit-2.html  13,467
torah-weave/Deuteronomy/hebrew-deuteronomy-unit-4/hebrew-deuteronomy-unit-4.html  17,077
torah-weave/Deuteronomy/hebrew-deuteronomy-unit-5/hebrew-deuteronomy-unit-5.html  12,268
torah-weave/Deuteronomy/hebrew-deuteronomy-unit-7/hebrew-deuteronomy-unit-7.html  42,453
torah-weave/Deuteronomy/hebrew-deuteronomy-unit-8/hebrew-deuteronomy-unit-8.html  20,461
torah-weave/Deuteronomy/hebrew-deuteronomy-unit-9/hebrew-deuteronomy-unit-9.html  15,070
torah-weave/Deuteronomy/hebrew-deuteronomy-unit-10/hebrew-deuteronomy-unit-10.html  18,834
torah-weave/Deuteronomy/hebrew-deuteronomy-unit-11/hebrew-deuteronomy-unit-11.html  13,336
torah-weave/Deuteronomy/hebrew-deuteronomy-unit-12/hebrew-deuteronomy-unit-12.html  15,702
torah-weave/Deuteronomy/hebrew-deuteronomy-unit-13/hebrew-deuteronomy-unit-13.html  12,798
torah-weave/Numbers/numbers-unit-1/numbers-unit-1.html                     33,117
```

**Recommended handling:** these look like in-progress/placeholder pages where someone created the DWT scaffolding but never filled in content. The migration should either skip them (leave alone with original DWT) or migrate with empty `content` region (the page will render as empty within the new template chrome). **Recommend skipping in bulk and reviewing manually.** Also worth asking Moshe whether these should be deleted entirely.

### 3c. `hebrew.dwt` files missing `additional-styles` + `page-scripts` (3 files)

```
Mishnah/Mesechet Peah.htm
Mishnah/Mesechet Shviit.htm
Mishnah/Mesechet Trumote.htm
```

These have only `doctitle` and `start` regions. The other 13 hebrew.dwt files have all 4 standard regions. These three are presumably older/incomplete. **Recommended handling:** migrate normally; missing regions default to empty string in the new template.

### 3d. Files with multiple `<footer>` tags in body (4 files)

```
Mishnah/TheMishnah.htm
Mishnah-New/English/Mishnah Portal.htm
Mishnah-New/English/Articles/index.html
Torah-New/English/Articles/Towards a Hermeneutic of the Non-Linear.htm
```

Likely the DWT footer plus a content-area footer (a citation block, copyright, etc.). After migration the new template's footer remains; any content-area footer inside the `content` region is preserved. Worth a spot-check that the migrated output is sensible.

### 3e. Files with inline `style="width: Npx"` where N > 400 (20 files)

Top examples (`width: 900px` is the most common offender):

```
General/about-page/about-page.html              widths=[800]
Mishnah/Mesechet Bechorot.htm                   widths=[900]
Mishnah/Mesechet Brachot.htm                    widths=[900]
Mishnah/Mesechet Chalah.htm                     widths=[900]
Mishnah/Mesechet Damai.htm                      widths=[900]
Mishnah/Mesechet Kelaim.htm                     widths=[900]
Mishnah/Mesechet Maaser Sheni.htm               widths=[900]
Mishnah/Mesechet Maasrot.htm                    widths=[900]
Mishnah/Mesechet Orlah.htm                      widths=[900]
Mishnah-New/Hebrew/Articles/CfrHnnia.htm        widths=[900]
```

These pages have inline-styled elements (probably wrapper divs or images) at 900 px width that will overflow mobile viewports. **Recommended fix:** add a global mobile rule that caps inline-style absolute widths within `<main>`, e.g.:

```css
@media (max-width: 768px) {
    main [style*="width:"] {
        max-width: 100% !important;
    }
}
```

This is a single rule that covers all 20 files without per-page edits.

### 3f. Files with `non_trivial_js_count ≥ 2` (24 files)

These have 2+ inline scripts beyond gtag/toggleMenu/dataLayer. Most are probably schema.org JSON-LD `<script type="application/ld+json">` blocks (would be preserved in the `meta` region during migration), but some may have custom click handlers or other page-specific JS. Manual review recommended.

Top examples:

```
about-Moshe-Kline.html                          count=4 n_scripts=6
index.html                                      count=3 n_scripts=5
Articles/TenWrd1.html                           count=2 n_scripts=3
General/about-page/about-page.html              count=2 n_scripts=4
General/Color Codes/Hebrew-Color-Code.html      count=2 n_scripts=4
Mishnah/TheMishnah.htm                          count=2 n_scripts=4
Mishnah-New/Hebrew/Text/mishnah-pdf.html        count=3 n_scripts=5
Torah-New/English/Text/Torah-pdf.html           count=2 n_scripts=4
```

For each, open and check what the scripts do. If they're all schema.org JSON-LD, no special handling needed. If any is custom interactive JS (e.g., `mishnah-pdf.html`'s PDF viewer), the migration needs to preserve it intact.

---

## 4. MEDIUM Risk Sample Paths

### 4a. `lang_mismatch` (709 files) — too many to list

The bulk script's existing logic (path/DWT-based detection overriding declared `lang`) correctly handles this. Sample of how the override resolves the mismatch:

- `Mishnah-New/Hebrew/Articles/MAVO.htm`: declared `lang="en" xml:lang="en"`, path `/Hebrew/` → migration uses HE template → migrated file has `lang="he" dir="rtl"`.
- Same pattern repeats across 607 Mishnah-New HE pages + 88 torah-weave HE pages + 11 Mishnah HE pages + 2 Torah-New HE pages + 1 General HE page.

### 4b. `scripture-table` pages (99 files) — sample

```
index.html
Mishnah-New/English/Articles/avot-chapter-4.html         (32 scripture tables!)
Mishnah-New/English/Articles/five-pairs-avot-1.html      (10)
Mishnah-New/English/Articles/men-of-kfar-hananya.html    (11)
Mishnah-New/English/Articles/index.html
```

Some Avot pages have many scripture-tables. Need a mobile rule like the `.matrix-table` shrink-to-fit so these don't overflow either.

### 4c. `matrix-table` pages (47 files) — covered by recent CSS rule

Already handled by the `font-size: 0.65em` + tight-padding rule added in the previous task. No special migration handling needed.

### 4d. `English.dwt` with standard regions (31 files) — sample

```
Articles/TenWrd1.html
General/Contact.htm
General/Leviathan.htm
General/Nonlinear Texts.htm
General/The Torah and Mishnah are Visual texts.htm
Mishnah-New/English/Articles/TheArt-H.htm
Torah-New/English/Articles/...   (many)
```

Same region set as Academic-Content-DWT.dwt (`doctitle, meta, additional-styles, content, page-scripts`). The migration script needs to accept `English.dwt` as a synonym for Academic-Content-DWT extraction logic.

---

## 5. Recommendations

### 5.1 Migration logic updates

The current `_pilot/migration-logic.md` needs these additions before the bulk run:

1. **Add `English.dwt` as a recognized DWT type.** Treat it identically to `Academic-Content-DWT.dwt` (same 5-region mapping) for the 31 files with standard regions.
2. **Add `writehere` → `content` remap** for the 6 `torah-commentary-project/Commentaries/...` files using `English.dwt` with non-standard regions. Same pattern as `start` → `content` for hebrew.dwt.
3. **Default missing regions to empty string** when the source DWT didn't define them (already documented for hebrew.dwt's missing `meta`; extend to any region that's documented as missing).
4. **Skip files with missing `content` region by default** — the 13 Academic-Content-DWT skeleton files plus the 6 `writehere` files (after remap, content equivalent IS present in those, so they're fine; only the 13 Academic-Content-DWT ones are truly content-empty). Flag them for manual review.
5. **Detect `English.dwt`** via the DWT filename in the `#BeginTemplate` reference, same way as the other two.

### 5.2 New verification checks

In addition to the 9 checks already in the migration spec, add:

10. **No content outside `<main>` lost.** Some pages have content directly in `<body>` outside any `<main>` tag (9 such pages). Migration's standalone-page heuristic needs to handle this case; for DWT pages it's normally inside the `content` region (which IS wrapped in `<main>` by the template). For the 9 outliers, manual review.
11. **Inline scripts > 200 chars preserved or audited.** For each migrated file, verify that any non-gtag/non-toggleMenu inline script from the source is either (a) preserved in the appropriate region or (b) explicitly listed in the migration log as discarded with reason.
12. **`width: Npx` audit.** Flag any inline-style absolute width > 400 px after migration — should be caught by the global mobile CSS rule (see 5.4) but worth confirming.

### 5.3 Files to handle outside the bulk run (manual one-by-one)

These should be excluded from the bulk pass and migrated individually after careful inspection:

1. **6 `writehere` files** in `torah-commentary-project/Commentaries/` — non-standard region; possibly some are test pages to delete entirely.
2. **13 missing-content Academic-Content-DWT files** in `torah-weave/Deuteronomy/` and `torah-weave/Numbers/` — skeleton pages that need either filling or deletion.
3. **3 minimal `hebrew.dwt` Mishnah files** (Peah, Shviit, Trumote) — missing `additional-styles` and `page-scripts`, just to confirm the empty-default handling produces sensible output.
4. **`about-Moshe-Kline.html`, `index.html`, `mishnah-pdf.html`, `Torah-pdf.html`** — high inline script counts; verify the schema.org JSON-LD blocks are preserved correctly.
5. **`Mishnah/TheMishnah.htm`** — multiple `<footer>` tags, plus already-noted high script count.

That's ~24 files for manual migration. The remaining ~906 should be safe for the bulk run with the cleanup pass.

### 5.4 CSS additions to `main.css` before the bulk run

Three rules would smooth the migration:

```css
/* Within @media (max-width: 768px) — already-existing content block */
@media (max-width: 768px) {
    /* Cap any inline-styled absolute width at viewport.
       Catches the ~20 pages with style="width: 800/900px" overflow risks. */
    main [style*="width:"] {
        max-width: 100% !important;
        height: auto;
    }

    /* Scripture-table shrink-to-fit (same approach as .matrix-table) for the
       99 pages that use this class. */
    .scripture-table {
        font-size: 0.75em;
        line-height: 1.3;
    }
    .scripture-table th,
    .scripture-table td {
        padding: 4px 3px !important;
        word-break: break-word;
    }
}
```

(The exact font-size/padding values are estimates; refine based on real-phone testing of one Avot scripture-table page like `Mishnah-New/English/Articles/avot-chapter-4.html` after the migration.)

### 5.5 Recommended additional pilot pages before the bulk run

The 4-page pilot covered: Academic-Content-DWT EN, hebrew.dwt HE (with lang correction), large Academic-Content-DWT EN with matrix-table, standalone HE home. Three additional edge cases worth piloting next:

1. **`Articles/TenWrd1.html`** — exercises the `English.dwt` standard-regions case (the 31-file population). Validates that adding `English.dwt` to the migration script's DWT whitelist works.
2. **`torah-commentary-project/Commentaries/Deuteronomy/deuteronomy-unit-3.html`** — exercises the `writehere` remap on `English.dwt`. Validates the new region remap logic.
3. **`Mishnah-New/English/Articles/avot-chapter-4.html`** — exercises a page with 32 `scripture-table` elements + significant inline schema.org JSON-LD. Validates both the script-preservation logic and the new `.scripture-table` mobile rule.

If those 3 pass, the bulk migration of the ~906 LOW-risk files should be safe to run.

---

## 6. Appendix: Useful Counts at a Glance

| Metric | Count |
|---|---:|
| Total DWT-attached pages | 930 |
| Pages with `.htm` extension | 630 |
| Pages with `.html` extension | 300 |
| Detected as Hebrew (path/DWT/lang) | 709 |
| Detected as English | 221 |
| Using `Academic-Content-DWT.dwt` | 877 |
| Using `English.dwt` | 37 |
| Using `hebrew.dwt` | 16 |
| Pages whose declared `lang` ≠ detected lang | 709 |
| Pages whose `check_mobile_nav_not_hidden` would fail PRE-cleanup | 927 |
| Pages with `toggleMenu` in inline JS | 914 |
| Pages with gtag/dataLayer in inline JS | 890 |
| Pages with `non_trivial_js_count ≥ 2` | 24 |
| Pages with multiple inline `<style>` blocks | 25 |
| Pages with inline `<style>` total > 5 KB | 897 |
| Pages with `<iframe>` element | 0 |
| Pages with `<img width="≥800">` attribute | 0 |
| Pages with inline `style="width: >400px"` | 20 |
| Pages with `<table>` of any class | 817 |
| Pages with `<table class="matrix-table">` | 47 |
| Pages with `<table class="scripture-table">` | 99 |
| Pages with `<header class="unit-header-section">` | 90 |
| Pages with `<nav class="unit-navigation">` | 78 |
| Pages with multiple `<header>` tags in body | 110 |
| Pages with multiple `<footer>` tags in body | 4 |
| Pages with no `<main>` tag | 9 |
| Pages with editable-region names outside expected set (`writehere`) | 6 |
| Pages missing one or more expected regions | 22 |
| Pages with `<!-- #InstanceBegin` instead of/in addition to `#BeginTemplate` | 0 |

---

## Files Produced By This Survey

| File | Role |
|---|---|
| `/tmp/survey.py` | The analysis script (kept for reproducibility) |
| `/tmp/survey_results.json` | Per-file structural data, ~3 MB |
| `_pilot/pre-migration-survey.md` | This report |

Nothing in the repo was modified. The bulk migration task can proceed once the recommendations in Section 5 are addressed (English.dwt support in the migration script, `writehere` → `content` remap, the 3 additional pilot pages, and the 2 mobile CSS rule additions).
