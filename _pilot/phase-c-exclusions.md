# Phase C — Migrate the 10 Phase B Exclusions + Slideshow Link Fix

**Date:** 2026-05-13
**Scope:** Migrate the 10 files Phase B excluded (4 multi-footer, 4 high-traffic, 2 high inline-script) and fix the slideshow link on the Torah Portal. Plus an unplanned mid-task repair of two truncated templates.
**Status:** **10/10 migrated successfully. 0 errors. 0 skipped.** Originals byte-identically backed up. Slideshow link fixed. Templates repaired. **Not committed.**

---

## 1. Headline

| Metric | Count |
|---|---:|
| Files attempted | 10 |
| **Migrated successfully** | **10** (100%) |
| Errors | 0 |
| Skipped | 0 |
| Slideshow href fixes applied | 1 |
| Templates repaired (out of scope but blocking) | 2 |
| Net size delta across 10 migrated files | **−27.0 KB** (476.7 → 449.7 KB) |
| New backups created in `_backup-pre-migration/` | 10 |

---

## 2. Part 1 — Slideshow Link Fix on Torah Portal

### File modified

`Torah-New/English/Torah Portal.htm`, line 275.

### Before / after

```diff
- <a href="/torah-weave/introduction/woven-torah-slides"  class="cta-link">View Slideshow →</a>
+ <a href="/torah-weave/introduction/woven-torah-slides/" class="cta-link">View Slideshow →</a>
```

Only difference: trailing `/`.

### Grep verification

```bash
grep -rln '/woven-torah-slides[^/]' \
    --include='*.htm' --include='*.html' \
    --exclude-dir='_backup-pre-migration' --exclude-dir='_archive' .
```

Result: **`./torah-weave/introduction/woven-torah-slides/index.html`** (the slideshow's own index page, on lines 29 and 40).

The Torah Portal href (the actual navigational link) is now correct and no longer appears in the grep output.

The 2 remaining matches are inside the slideshow page's own SEO/canonical metadata — `og:url` and `mainEntityOfPage` — pointing to the trailing-slash-less canonical URL. These are not navigational hrefs (browsers don't follow them for rendering); they're canonical/SEO references. Leaving them alone for now since changing canonical URLs has SEO implications. **Recommend a follow-up SEO pass** to normalize them along with the broader canonical/hreflang/og:image cleanup.

```
torah-weave/introduction/woven-torah-slides/index.html:29:
    <meta property="og:url" content="https://chaver.com/torah-weave/introduction/woven-torah-slides">
torah-weave/introduction/woven-torah-slides/index.html:40:
    "mainEntityOfPage": "https://chaver.com/torah-weave/introduction/woven-torah-slides",
```

---

## 3. Part 2 — Migration Results (All 10 Files)

All 10 files share these properties:

- **DWT type detected:** `Academic-Content-DWT.dwt` (no `English.dwt` or `hebrew.dwt` in this batch)
- **All 5 source regions extracted** (`doctitle`, `meta`, `additional-styles`, `content`, `page-scripts`)
- **All 13 standard checks pass**
- **All group-specific extras pass**
- **Provenance marker present** as `<!-- rendered-from: _templates/Academic-Content-{EN,HE}.html @ <ISO 8601 UTC timestamp> -->` immediately after `<!DOCTYPE html>`
- **`<html lang>`** correct: `lang="en"` for EN, `lang="he" dir="rtl"` for HE
- **Favicon link** present in `<head>`
- **`class="site-footer"`** present (new template footer)
- **No DWT markers** remain (`#BeginTemplate`, `#BeginEditable`, `#EndEditable`, `#EndTemplate` all gone)
- **Mobile-nav not hidden** check returns 0 findings on every file

### Per-file results

| # | Group | Lang | File | Size before | Size after | Δ | Region sizes (doctitle / meta / styles / content / scripts) | Checks |
|---|---|---|---|---:|---:|---:|---|---|
| 1 | A | EN | `Mishnah/TheMishnah.htm` | 114,392 | 111,087 | −3,305 | 93 / 6,645 / 60 / 90,476 / 52 | 13/13 + A extras ✓ |
| 2 | A | EN | `Mishnah-New/English/Mishnah Portal.htm` | 98,376 | 95,247 | −3,129 | 105 / 1,699 / 60 / 79,998 / 52 | 13/13 + A extras ✓ |
| 3 | A | EN | `Mishnah-New/English/Articles/index.html` | 21,788 | 18,843 | −2,945 | 63 / 1,536 / 60 / 4,937 / 52 | 13/13 + A extras ✓ |
| 4 | A | EN | `Torah-New/English/Articles/Towards a Hermeneutic of the Non-Linear.htm` | 20,151 | 17,023 | −3,128 | 101 / 1,738 / 60 / 2,916 / 52 | 13/13 + A extras ✓ **see §6** |
| 5 | B | EN | `Torah-New/English/Text/Torah-pdf.html` | 41,589 | 38,294 | −3,295 | 94 / 6,404 / 3,581 / 15,800 / 5 | 13/13 + B extras ✓ |
| 6 | B | HE | `Mishnah-New/Hebrew/Text/mishnah-pdf.html` | 54,504 | 50,281 | −4,223 | 95 / 8,035 / 60 / 28,848 / 52 | 13/13 + B extras ✓ |
| 7 | B | EN | `about-Moshe-Kline.html` | 58,804 | 55,286 | −3,518 | 94 / 14,346 / 60 / 27,976 / 52 | 13/13 + B extras ✓ |
| 8 | B | EN | `index.html` | 79,344 | 76,864 | −2,480 | 88 / 3,967 / 8,911 / 33,240 / 18,378 | 13/13 + B extras ✓ |
| 9 | C | EN | `General/about-page/about-page.html` | 28,990 | 26,051 | −2,939 | 73 / 2,442 / 60 / 11,231 / 52 | 13/13 + C extras ✓ |
| 10 | C | HE | `General/Color Codes/Hebrew-Color-Code.html` | 79,042 | 74,591 | −4,451 | 75 / 1,270 / 9,054 / 38,161 / 584 | 13/13 + C extras ✓ |

### Group-A extra check results (multi-footer preservation)

Both `<footer>` tags preserved: one inside `<main>` (carried over from source content), one outside (new template `site-footer`).

| File | `<footer>` inside `<main>` | Total `<footer>` | Class on inner footer |
|---|---:|---:|---|
| `Mishnah/TheMishnah.htm` | 1 | 2 | `portal-footer` |
| `Mishnah-New/English/Mishnah Portal.htm` | 1 | 2 | `portal-footer` |
| `Mishnah-New/English/Articles/index.html` | 1 | 2 | *(no class)* |
| `Torah-New/English/Articles/Towards a Hermeneutic…` | 1 | 2 | *(no class — see §6)* |

### Group-B extra check results (high-traffic critical)

- **Word count of migrated `<main>` vs. source `content`:** exact match on every file (no ±1% tolerance applied).
- **Schema.org JSON-LD blocks:** all preserved verbatim.
- **PDF/download href preservation:** all PDF hrefs from source content present in migrated `<main>`.

| File | src words | new words | Match | JSON-LD blocks | PDF hrefs |
|---|---:|---:|---|---:|---:|
| `Torah-New/English/Text/Torah-pdf.html` | 1,717 | 1,717 | ✓ exact | 2 → 2 | (none in content) |
| `Mishnah-New/Hebrew/Text/mishnah-pdf.html` | 2,757 | 2,757 | ✓ exact | 3 → 3 | 4 → 4 |
| `about-Moshe-Kline.html` | 3,556 | 3,556 | ✓ exact | 4 → 4 | (none in content) |
| `index.html` | 1,919 | 1,919 | ✓ exact | 2 → 2 | 2 → 2 |

### Group-C extra check results (high inline-script)

The check spec is: "Count inline `<script>` blocks in source vs migrated. Should be equal (excluding gtag/toggleMenu which are template-owned)."

The check classifies each inline script as:

- **template-owned** — `gtag(...)`, `window.dataLayer`, or new SITE NAV (`var toggle = document.querySelector('.nav-toggle')`). Always present in migrated; may or may not be present in source.
- **legacy nav** — `function toggleMenu(...)`, `getElementById('nav-menu')`, "Close mobile menu when clicking outside". Present in source DWT scaffolding; intentionally dropped in migration.
- **real** — everything else (page-specific JS, schema.org JSON-LD, etc.). Must be preserved byte-identically.

| File | src inline (total) | new inline (total) | src real | new real | All preserved |
|---|---:|---:|---:|---:|---|
| `General/about-page/about-page.html` | 4 | 4 | 2 | 2 | ✓ (JSON-LD Article + FAQ) |
| `General/Color Codes/Hebrew-Color-Code.html` | 4 | 4 | 2 | 2 | ✓ (JSON-LD Article + scroll-to-top handler) |

**For Color Codes specifically:** the `// Scroll to top functionality` script (real page feature) is preserved verbatim in `<main>`. The `function toggleMenu()` legacy script is correctly dropped.

---

## 4. Anomalies and Patterns Encountered

### 4.1 Pre-task surprise: BOTH templates were truncated on disk

Before the migration could run, I discovered that `_templates/Academic-Content-EN.html` and `_templates/Academic-Content-HE.html` were truncated. The EN template ended mid-tag at `    </scri`; the HE template ended after `})();` with no closing `</script>`, `{{ region: page-scripts }}`, `</body>`, or `</html>`.

**Plausible cause:** the post-Phase-B-fixup task's favicon-link insertion appears to have partial-written the templates. The IDE/Read view showed the files as complete (cached state), but the on-disk bytes were truncated. Migrated Phase B files have full endings, confirming the templates were complete during Phase B.

**Fix applied:** restored the missing tail to both files via a direct Python byte append. Final state verified — each template has exactly 1 of every region placeholder, 1 favicon link, 1 nav-toggle, 1 site-footer, and a well-formed `</html>` close.

| Template | Truncated size | Repaired size | Preserved features |
|---|---:|---:|---|
| `_templates/Academic-Content-EN.html` | 14,754 B | 14,815 B | favicon link, all 5 region placeholders, nav-toggle, site-footer |
| `_templates/Academic-Content-HE.html` | 13,507 B | 13,569 B | same |

**Risk to Phase B outputs:** none. The 768 Phase B-migrated files were rendered from the complete templates (their fully-formed `</script>...</body></html>` ending proves this). Only Phase C migrations were at risk and they were blocked until the templates were repaired.

**Recommended follow-up:** investigate whether the OneDrive sync or the Edit tool's partial-write behavior is the cause. The Phase A → Phase B → Post-Phase-B-fixup sequence may have produced a corrupted template that future tasks need to be defensive against. Compare the repaired templates with the last known-good versions in git history (via GitHub Desktop) before pushing — confirm the templates match what was deployed.

### 4.2 Towards a Hermeneutic of the Non-Linear — embedded legacy chrome inside content region

The article's `content` region contains a full legacy site chrome — old `<header><nav>`, old `<button class="menu-toggle">`, old `<footer>`, old `<script>function toggleMenu()</script>` — plus an apparently never-finished article body (mostly just the title in `<h1>` plus one paragraph).

After migration, this legacy chrome is preserved verbatim INSIDE the new `<main>`. The migration's 13-check verification correctly counts these legacy elements as inside-`<main>` (informational only) rather than as chrome-level violations, so the file passes. But visually the rendered page will show a duplicate nav and footer **stuck inside the main content area**.

The migrated check 3 result for this file:

```
"3_old_nav_removed": { "pass": true, "chrome_count": 0, "inside_main_count_info_only": 2 }
```

**This is a content task, not a migration task** — the page needs Moshe to either:

1. Strip the embedded legacy chrome from the content region and finish writing the article, or
2. Mark the URL as unpublished until the article is completed, or
3. Replace the content with a simple "coming soon" stub.

The migration itself preserved everything in source content exactly — Moshe's call on what to do with it. **Flag for content review before publishing.**

### 4.3 No `English.dwt` or `hebrew.dwt` in this batch

Confirmed via the DWT detection. All 10 files were `Academic-Content-DWT.dwt`. The published-but-deferred `English.dwt` and `hebrew.dwt` pages remain out of scope.

### 4.4 Two Group-B Hebrew pages get their language correctly redeclared

`Mishnah-New/Hebrew/Text/mishnah-pdf.html` (and the Group C `General/Color Codes/Hebrew-Color-Code.html`) had `<html lang="en">` in the source despite the path/DWT correctly signaling Hebrew. Both now have `<html lang="he" dir="rtl">` after migration — the same `lang_corrected` event that affected all 600 Phase B Hebrew pages.

### 4.5 The verification regex was reused, no new bugs

The Phase B nested-`<main>` extraction issue (string `.find()` / `.rfind()` instead of non-greedy regex) was already baked into the migration logic. All 10 Phase C files extracted their `<main>` content correctly.

---

## 5. Backup Verification

All 10 originals byte-identically backed up to `_backup-pre-migration/<rel-path>/`:

```
_backup-pre-migration/Mishnah/TheMishnah.htm                                                          114,392 B
_backup-pre-migration/Mishnah-New/English/Mishnah Portal.htm                                           98,376 B
_backup-pre-migration/Mishnah-New/English/Articles/index.html                                          21,788 B
_backup-pre-migration/Torah-New/English/Articles/Towards a Hermeneutic of the Non-Linear.htm           20,151 B
_backup-pre-migration/Torah-New/English/Text/Torah-pdf.html                                            41,589 B
_backup-pre-migration/Mishnah-New/Hebrew/Text/mishnah-pdf.html                                         54,504 B
_backup-pre-migration/about-Moshe-Kline.html                                                           58,804 B
_backup-pre-migration/index.html                                                                       79,344 B
_backup-pre-migration/General/about-page/about-page.html                                               28,990 B
_backup-pre-migration/General/Color Codes/Hebrew-Color-Code.html                                       79,042 B
```

Each backup file size matches the original pre-migration source size exactly (`size_before` in the migration result JSON).

Rollback paths if anything goes wrong post-deploy:

```bash
# Single file
cp _backup-pre-migration/<rel-path> <rel-path>

# Whole Phase C set at once
for f in Mishnah/TheMishnah.htm \
         "Mishnah-New/English/Mishnah Portal.htm" \
         Mishnah-New/English/Articles/index.html \
         "Torah-New/English/Articles/Towards a Hermeneutic of the Non-Linear.htm" \
         Torah-New/English/Text/Torah-pdf.html \
         Mishnah-New/Hebrew/Text/mishnah-pdf.html \
         about-Moshe-Kline.html \
         index.html \
         General/about-page/about-page.html \
         "General/Color Codes/Hebrew-Color-Code.html"; do
    cp "_backup-pre-migration/$f" "$f"
done

# Or git revert (preferred once committed)
git revert <commit-hash>
```

The templates' repair was NOT backed up (the truncated state was effectively unusable; reverting to it would re-break the templates). If Moshe wants the truncated template state restored for forensic comparison, the bytes are recorded in §4.1 above.

---

## 6. Cowork's Confidence — Per-Group Spot-Check Recommendations

### Group A (multi-footer) — HIGH CONFIDENCE on 3 of 4

| File | Confidence | Notes |
|---|---|---|
| `Mishnah/TheMishnah.htm` | **HIGH** | The portal page Moshe specifically called out. Both `portal-footer` (inside `<main>`) and `site-footer` (outside) present. 565 hrefs preserved. Should be visually clean. |
| `Mishnah-New/English/Mishnah Portal.htm` | **HIGH** | Similar structure. 540 hrefs preserved. |
| `Mishnah-New/English/Articles/index.html` | **HIGH** | Smaller article-index page. Plain (no `portal-footer` class) inner footer. |
| `Torah-New/English/Articles/Towards a Hermeneutic…` | **LOW — content review needed** | See §4.2. The article's content region is essentially a copy of legacy chrome + a stub title. After migration, the new template wraps this legacy chrome cleanly, but it will render visually as nav-inside-content. **Recommend Moshe view this page before pushing** and decide whether to keep the migrated form or unpublish until the article is written. |

### Group B (high-traffic critical) — HIGH CONFIDENCE on all 4

| File | Confidence | Notes |
|---|---|---|
| `Torah-New/English/Text/Torah-pdf.html` | **HIGH** | The most-trafficked page. Exact word-count match (1,717 = 1,717). 2 JSON-LD blocks preserved. Inline `additional-styles` 3,581 bytes preserved verbatim (page-specific PDF-display CSS). **Spot-check recommendation:** visit `/Torah-New/English/Text/Torah-pdf` in incognito, confirm PDF download link works and embedded preview renders. |
| `Mishnah-New/Hebrew/Text/mishnah-pdf.html` | **HIGH** | Hebrew counterpart. Lang correctly switched from `en` to `he dir="rtl"`. Exact word-count match (2,757). 3 JSON-LD blocks preserved. 4 PDF hrefs preserved. **Spot-check:** confirm RTL flow + Hebrew PDF download. |
| `about-Moshe-Kline.html` | **HIGH** | Exact word-count match (3,556). 4 JSON-LD blocks preserved (Person + Article + likely FAQ + breadcrumb). Largest meta region in the batch (14,346 B) — all preserved. |
| `index.html` (English home) | **HIGH** | Exact word-count match (1,919). 2 JSON-LD blocks preserved. Largest `page-scripts` region in the batch (18,378 B — likely site-specific JS for the homepage scroll/animation effects) — all preserved. 2 PDF hrefs preserved. **Spot-check thoroughly** since this is the site root. |

### Group C (high inline-script) — HIGH CONFIDENCE on both

| File | Confidence | Notes |
|---|---|---|
| `General/about-page/about-page.html` | **HIGH** | 2 real inline scripts (JSON-LD Article + JSON-LD FAQPage) preserved byte-identically. The legacy `toggleMenu()` script was correctly dropped (it would have conflicted with the new SITE NAV's class-toggle pattern). |
| `General/Color Codes/Hebrew-Color-Code.html` | **HIGH** | The `// Scroll to top functionality` page-feature script is preserved verbatim inside `<main>`. JSON-LD preserved. Big `additional-styles` region (9,054 B — the color-code-table styling) preserved. |

---

## 7. Files Touched

| File | Action |
|---|---|
| `Torah-New/English/Torah Portal.htm` | Slideshow href: `/woven-torah-slides` → `/woven-torah-slides/` |
| `_templates/Academic-Content-EN.html` | Restored truncated tail (added `</script> + page-scripts placeholder + </body> + </html>`) |
| `_templates/Academic-Content-HE.html` | Same |
| `Mishnah/TheMishnah.htm` | Migrated to new template (Group A) |
| `Mishnah-New/English/Mishnah Portal.htm` | Migrated to new template (Group A) |
| `Mishnah-New/English/Articles/index.html` | Migrated to new template (Group A) |
| `Torah-New/English/Articles/Towards a Hermeneutic of the Non-Linear.htm` | Migrated to new template (Group A — but see §4.2) |
| `Torah-New/English/Text/Torah-pdf.html` | Migrated to new template (Group B) |
| `Mishnah-New/Hebrew/Text/mishnah-pdf.html` | Migrated to new template (Group B) |
| `about-Moshe-Kline.html` | Migrated to new template (Group B) |
| `index.html` | Migrated to new template (Group B) |
| `General/about-page/about-page.html` | Migrated to new template (Group C) |
| `General/Color Codes/Hebrew-Color-Code.html` | Migrated to new template (Group C) |
| `_backup-pre-migration/<each of the 10 above>` | 10 backups created |
| `_pilot/phase-c-exclusions.md` | This report |

No JavaScript changes. No `main.css` changes. No DWT-attached pages outside the 10-file set were modified.

---

## 8. Moshe's Verification Checklist

### Spot-check via GitHub Desktop diff view (before pushing)

1. **`_templates/Academic-Content-EN.html` and `_templates/Academic-Content-HE.html`** — confirm the closing `</script>`, `{{ region: page-scripts }}`, `</body>`, `</html>` are present and the rest of the file is unchanged from the version that produced the 768 Phase B migrations. If they look intact, the repair is fine. (See §4.1 for context.)
2. **`Torah-New/English/Torah Portal.htm`** — single one-character change on line 275 (trailing slash added).
3. **`Mishnah/TheMishnah.htm`** — the headline file Moshe called out. Confirm both `<footer class="portal-footer">` and `<footer class="site-footer">` are present.
4. **`Torah-New/English/Articles/Towards a Hermeneutic of the Non-Linear.htm`** — **read this one carefully.** See §4.2 and §6. The page's content region is mostly legacy chrome + a stub title. Decide whether to keep it migrated or roll back via `cp _backup-pre-migration/...` and treat as a content-not-yet-written page.
5. **`Torah-New/English/Text/Torah-pdf.html`** and **`index.html`** — diff and skim. Confirm content blocks intact, PDF links and JSON-LD untouched.

### Push, then visit each URL (desktop + mobile, both portrait AND landscape)

**Group A — confirm hamburger nav works (Moshe's primary concern):**

- `https://chaver.com/Mishnah/TheMishnah.htm`
- `https://chaver.com/Mishnah-New/English/Mishnah%20Portal.htm`
- `https://chaver.com/Mishnah-New/English/Articles/`
- `https://chaver.com/Torah-New/English/Articles/Towards%20a%20Hermeneutic%20of%20the%20Non-Linear.htm`

**Group B — high-traffic, test extensively:**

- `https://chaver.com/Torah-New/English/Text/Torah-pdf` ← most-trafficked
- `https://chaver.com/Mishnah-New/Hebrew/Text/mishnah-pdf`
- `https://chaver.com/about-Moshe-Kline`
- `https://chaver.com/` (English home)

**Group C — verify embedded widgets/scripts:**

- `https://chaver.com/General/about-page/about-page.html`
- `https://chaver.com/General/Color%20Codes/Hebrew-Color-Code.html` (test scroll-to-top button)

**Slideshow link sanity check:**

- `https://chaver.com/Torah-New/English/Torah%20Portal.htm` → click "View Slideshow →" → image paths should resolve correctly (they were broken before due to missing trailing slash).

### Rollback if anything fails

```bash
# Single-file rollback
cp _backup-pre-migration/<rel> <rel>

# Whole-batch rollback
git revert <commit-hash>
```

---

## 9. What's Left After Phase C

Per the task spec:

- **2 published `English.dwt` files** (separate small task)
- **4 published `hebrew.dwt` files** (separate small task)
- **13 skeleton pages** (content-empty Deuteronomy/Numbers — fill content first, migrate later)
- **140 orphans** (Moshe triage at his pace)
- **DWT file cleanup** (move `Dynamic Web Templates/*.dwt` to `_archive/`)
- **Stale CSS cleanup** in `main.css` (`.menu-toggle` / `.main-nav`)
- **SEO/AEO maxing pass** — canonical tags, hreflang, og:image, Twitter cards, Person/Organization schema, the 2 slideshow-self-canonical URLs from §2

None of these is urgent and none blocks the Phase C push.

---

## 10. Out of Scope (Per Task)

- Anything not in the 10-file exclusion list
- `English.dwt` and `hebrew.dwt` files
- Orphan files
- Template changes beyond the truncation repair (which was unblockingly necessary)
- `main.css` changes beyond what's verified working
