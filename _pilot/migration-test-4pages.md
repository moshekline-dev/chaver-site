# Migration Test — 4 Pages from DWT to New Templates

**Date:** 2026-05-13
**Scope:** Pilot migration of 4 representative pages to verify migration logic before bulk-migrating the remaining ~500 DWT-attached pages.
**Status:** All 4 pages migrated. Originals backed up to `_backup-pre-migration/`. All 8 verification checks pass on each file. **Not committed.**

---

## ⚠ One Note Before the Per-File Summaries

Two of the four spec'd paths used `.htm` extensions but the actual files on disk have `.html` extensions. The live URLs work via Cloudflare clean-URL handling (the extensionless URL resolves to the `.html` file; the `.htm` URL 404s). I migrated the actual on-disk files:

| Spec said | Actual on-disk file |
|---|---|
| `/torah-weave/leviticus-19-ark-at-the-center.htm` | `/torah-weave/leviticus-19-ark-at-the-center.html` |
| `/torah-weave/Woven-Torah-Method.htm` | `/torah-weave/Woven-Torah-Method.html` |
| `/Mishnah-New/Hebrew/Articles/MAVO.htm` | (matches — `.htm` is correct here) |
| `/hebrew index.html` | (matches) |

Worth knowing for the bulk migration: extension detection must be case-and-suffix-flexible.

---

## 1. Page 1 — `/torah-weave/leviticus-19-ark-at-the-center.html`

**Detected:** EN, attached to `Academic-Content-DWT.dwt`. Template: `_templates/Academic-Content-EN.html`.

### Extraction summary

| Region | Bytes |
|---|---:|
| `doctitle` | 118 |
| `meta` | 2,911 |
| `additional-styles` | 60 |
| `content` | 9,023 |
| `page-scripts` | 52 |

All 5 source regions found via `<!-- #BeginEditable -->` markers. Direct 1:1 mapping to template placeholders.

### Verification — all checks passed

| Check | Result |
|---|---|
| `class="nav-toggle"` present | ✓ 1 |
| 2 `<button type="button">` for dropdowns | ✓ 2 (Torah, Insights) |
| DWT markers (`#BeginTemplate`, `#BeginEditable`, etc.) removed | ✓ 0 |
| `class="menu-toggle"` old button | ✓ 0 |
| `onclick="toggleMenu()"` | ✓ 0 |
| `<html lang="en">` | ✓ |
| `<title>` preserved | ✓ "Love Your Neighbor Is Not a Standalone Law…" — identical to backup |
| `href` count preserved | ✓ 50 → 50 (exact match) |
| `<a>` / `<p>` / `<h*>` landmark counts | ✓ 49→49 `<a>`, 1→1 `<p>`, 14→14 `<h*>`; `<div>` 16→18 (+2 from new nav wrapper structure) |
| File size | 27,300 → 26,478 bytes (slight shrink from removing the old footer scaffolding) |

---

## 2. Page 2 — `/Mishnah-New/Hebrew/Articles/MAVO.htm`

**Detected:** HE (forced — file said `lang="en"` but path contains `/Hebrew/`, DWT is `hebrew.dwt`). Template: `_templates/Academic-Content-HE.html`.

### Extraction summary

| Source region | Bytes | Maps to template placeholder |
|---|---:|---|
| `doctitle` | 143 | `doctitle` |
| `additional-styles` | 51 | `additional-styles` |
| `start` | 41,917 | **`content`** (per `hebrew.dwt` convention) |
| `page-scripts` | 52 | `page-scripts` |
| *(no `meta` region in `hebrew.dwt`)* | — | `meta` ← empty string |

### Lang correction applied

**Original had `<html lang="en" xml:lang="en">` despite being Hebrew content.** Using the HE template fixes this: migrated file is `<html lang="he" dir="rtl">`. The lang-correction logic detected HE via path (`/Hebrew/`) and DWT (`hebrew.dwt`), overriding the buggy `lang="en"` declaration.

### Verification — all checks passed

| Check | Result |
|---|---|
| `class="nav-toggle"` present | ✓ 1 |
| 3 `<button type="button">` for dropdowns | ✓ 3 (תורה, משנה, נתונים) |
| DWT markers removed | ✓ 0 |
| Old `menu-toggle` / `toggleMenu` references | ✓ 0 |
| **`<html lang="he" dir="rtl">`** (lang corrected) | ✓ |
| `<title>` preserved | ✓ "מבוא למשנה כדרכה" — identical to backup |
| `href` count | 26 → 27 (+1 — the new Hebrew nav has one more link than the old hebrew.dwt nav) |
| `<a>` / `<p>` / `<h*>` landmark counts | ✓ 26→26 `<a>`, 444→444 `<p>` (significant prose preserved), 30→28 `<h*>` (the old hebrew.dwt had 2 `<h*>` in its own header/footer that the new template doesn't replicate) |
| File size | 81,390 → 77,610 bytes |

### Notes on hebrew.dwt convention (relevant for bulk migration)

- `hebrew.dwt` has only 4 editable regions: `doctitle`, `additional-styles`, `start`, `page-scripts`. **No `meta` region.** For the bulk task, that means HE pages from `hebrew.dwt` will all have empty `<head>` meta sections after migration — fine, but worth knowing that SEO meta tags from those pages were never region-editable (they lived in the DWT itself and are now hardcoded in the new template via the gtag.js etc.).
- `start` → `content` is a stable name remap.

---

## 3. Page 3 — `/torah-weave/Woven-Torah-Method.html`

**Detected:** EN, attached to `Academic-Content-DWT.dwt`. Template: `_templates/Academic-Content-EN.html`.

### Extraction summary

| Region | Bytes |
|---|---:|
| `doctitle` | 107 |
| `meta` | 4,573 |
| `additional-styles` | 5 |
| `content` | 25,572 |
| `page-scripts` | 5 |

All 5 regions found. Direct mapping.

### Verification — all checks passed

| Check | Result |
|---|---|
| `class="nav-toggle"` present | ✓ 1 |
| 2 `<button type="button">` for dropdowns | ✓ 2 (Torah, Insights) |
| DWT markers removed | ✓ 0 |
| Old nav markup | ✓ 0 |
| `<html lang="en">` | ✓ |
| `<title>` preserved | ✓ "The Woven Torah: A Two-Dimensional Reading of the Five Books of Moses" |
| `href` count | ✓ 67 → 67 (exact match) |
| Landmark counts | ✓ 66→66 `<a>`, 2→2 `<p>`, 22→22 `<h*>`; `<div>` 15→17 (+2 nav wrapper) |
| File size | 45,350 → 44,529 bytes |

---

## 4. Page 4 — `/hebrew index.html` (standalone)

**Detected:** HE, standalone (no `<!-- #BeginTemplate -->` marker). Template: `_templates/Academic-Content-HE.html`. **Required special-case extraction.**

### Extraction strategy (for the bulk task — standalone HE pages will need this same approach)

| Region | How extracted |
|---|---|
| `doctitle` | `<title>...</title>` from `<head>` |
| `meta` | All `<head>` content **except** charset/viewport/title/inline-`<style>` |
| `additional-styles` | The inline `<style>` block (entire 456-line block) |
| `content` | `<body>` content **between** `</header>` and `<footer>` |
| `page-scripts` | Empty — old `toggleMenu()` at end of body **discarded** (new template has its own nav JS) |

### Extraction sizes

| Region | Bytes |
|---|---:|
| `doctitle` | 265 |
| `meta` | 6,495 (includes 3 schema.org JSON-LD blocks: WebSite, Book, FAQPage, plus Google Fonts links, OG/Twitter tags, hreflang block) |
| `additional-styles` | 11,672 (the inline page-specific CSS for hero section, gateway, book, credentials, about) |
| `content` | 9,835 (5 `<section>` blocks: hero, gateway, book-section, credentials-section, about-section) |
| `page-scripts` | 0 |

### Verification — all checks passed

| Check | Result |
|---|---|
| `class="nav-toggle"` present | ✓ 1 |
| 3 `<button type="button">` for dropdowns | ✓ 3 |
| DWT markers | ✓ 0 (there were none to begin with) |
| Old nav markup | ✓ 0 (the old `<header>`/`<nav>`/`.menu-toggle` discarded) |
| `<html lang="he" dir="rtl">` | ✓ (original already had this) |
| `<title>` preserved | ✓ "chaver.com \| תורה ומשנה: ארכיטקטורה ספרותית דו-ממדית" |
| `href` count | 32 → 41 (+9 — the new template's nav menu adds Torah/Mishnah/Data dropdowns + their children + Contact + English links that the original homepage's `<nav>` didn't have) |
| Landmark counts | ✓ 25→33 `<a>` (+8 from new nav), 4→4 `<p>`, 10→10 `<h*>` (content preserved), `<div>` 22→25 (+3 nav wrapper) |
| File size | 33,022 → 42,131 bytes (grew because we kept all the page-specific inline `<style>` AND added the new template's full nav/footer scaffolding) |

### Notes on the standalone page

1. **Old inline nav CSS not stripped.** The original's `<style>` block contains `.site-header { ... }`, `.main-nav { ... }`, `.menu-toggle { ... }` rules from when it had its own custom nav. The migrated file keeps these styles. **They don't conflict with the new nav** (which uses `.nav-row`, `.nav-toggle`, `.nav-menu`, `.has-dropdown`, `.submenu` — different selectors), but they're dead code. The new `header.site-header` rule in `main.css` (specificity 0,1,1) wins over the old standalone `.site-header { ... }` (specificity 0,1,0), so the visual outcome is the new gradient. Flagged for optional manual cleanup.

2. **Old `<header>` and `<footer>` in body discarded.** The new template provides both. The old standalone footer at lines 688–729 was structurally similar to the new template footer (same 4 sections), so the swap is essentially seamless — except one Mishnah link in the old footer pointed at `/Mishnah-New/English/Mishnah%20Portal.htm` and the new template's points at `/mishnah/` (the placeholder URL that's consistent with the rest of the site's nav). The new footer also adds **קוד הצבעים** to the Mishnah section.

3. **Old `toggleMenu()` script discarded.** The new template's JS handles the new nav.

4. **The 3 schema.org JSON-LD scripts (WebSite, Book, FAQPage) are preserved in the `meta` region.** Important for SEO — these were the home page's structural data signal.

5. **Hebrew home page–specific styling (the coffee/cream color palette, Crimson Pro & Frank Ruhl Libre fonts, hero gradient, custom section layouts) is fully preserved in `additional-styles`.** The page should still look distinctive.

---

## 5. Original vs. Migrated — Quick Side-by-Side

| File | Lang corrected? | Original bytes | Migrated bytes | `<a>` orig→new | `<p>` orig→new |
|---|---|---:|---:|---:|---:|
| leviticus-19-ark-at-the-center.html | no | 27,300 | 26,478 | 49→49 | 1→1 |
| MAVO.htm | **yes (en→he+rtl)** | 81,390 | 77,610 | 26→26 | 444→444 |
| Woven-Torah-Method.html | no | 45,350 | 44,529 | 66→66 | 2→2 |
| hebrew index.html (standalone) | no | 33,022 | 42,131 | 25→33 (+8 nav) | 4→4 |

`<p>` and content-level `<a>` counts are preserved across the migration for the three DWT pages — content was extracted byte-faithfully from each `content` region (or `start` for hebrew.dwt). The href increases on MAVO (+1) and hebrew-index (+8) come entirely from the new template's enhanced nav (more menu items than the old templates had).

---

## 6. Pages Recommended for Manual Browser Review

All four pages should be tested in Moshe's browser before merging. Specific things to look for:

- **leviticus-19** and **Woven-Torah-Method:** these are content-heavy English articles. Confirm the article body renders identically, internal links work, and the new nav appears at the top with hover dropdowns on desktop / hamburger on mobile.
- **MAVO:** this is the biggest test — Hebrew RTL content (5,072 words from a `start` region), and the lang correction. Confirm Hebrew renders correctly (RTL flow, fonts), all internal links work, and the nav switches to Hebrew labels.
- **hebrew index.html:** the most unusual migration. Confirm the home-page-specific styling (coffee colors, hero gradient, custom fonts) still renders, the content sections (hero, gateway, book, credentials, about) all appear, and the schema.org JSON-LD scripts are still in `<head>` (View Source check).

---

## 7. Rollback Path

If anything breaks, restore from `_backup-pre-migration/`:

```bash
cp _backup-pre-migration/torah-weave/leviticus-19-ark-at-the-center.html torah-weave/leviticus-19-ark-at-the-center.html
cp _backup-pre-migration/Mishnah-New/Hebrew/Articles/MAVO.htm Mishnah-New/Hebrew/Articles/MAVO.htm
cp _backup-pre-migration/torah-weave/Woven-Torah-Method.html torah-weave/Woven-Torah-Method.html
cp "_backup-pre-migration/hebrew index.html" "hebrew index.html"
```

All four backups verified byte-identical to originals before migration.

---

## 8. What's Needed for the Bulk Migration (Notes for the Follow-Up Task)

- **Extension handling:** `.htm` vs `.html` — detection logic must accept both. Cloudflare clean-URL handling resolves either.
- **Language detection rules** (in order of priority): explicit `<html lang="he">` → HE; path contains `/Hebrew/` → HE; path contains `hebrew` (case-insensitive) → HE; DWT is `hebrew.dwt` → HE; otherwise EN. The MAVO case shows we need to **override** the explicit `<html lang>` declaration when path/DWT signal HE.
- **DWT region mapping for `hebrew.dwt`:** `start` → `content`, no `meta` region (defaults to empty).
- **DWT region mapping for `Academic-Content-DWT.dwt`:** direct 1:1 mapping of all 5 regions.
- **Standalone page handling:** these need per-page judgement. The standalone HE home was the only one in this pilot. If there are other standalone HTML files in the corpus, each may need ad-hoc extraction.
- **Backup discipline:** every migrated file should have a byte-identical backup in `_backup-pre-migration/` mirroring the source path. This pilot's backup script (`cp -v` with directory mirroring) is reusable.

---

## Files Touched

| File | Action |
|---|---|
| `torah-weave/leviticus-19-ark-at-the-center.html` | Migrated to new EN template |
| `Mishnah-New/Hebrew/Articles/MAVO.htm` | Migrated to new HE template (with `lang` correction) |
| `torah-weave/Woven-Torah-Method.html` | Migrated to new EN template |
| `hebrew index.html` | Migrated to new HE template (standalone — special handling) |
| `_backup-pre-migration/...` (4 files mirroring source paths) | Original copies, byte-identical to pre-migration state |
| `_pilot/migration-test-4pages.md` | This report |

No template, CSS, or JS changes. No DWT files touched.
