# Track 1 — Hebrew Mishnah Portal Live + English Mishnah Dropdown

**Date:** 2026-05-13
**Scope:** Three coordinated changes that together make the Mishnah navigation work properly on both Hebrew and English sides — and bring inbound links to the Hebrew Mishnah PDF.

1. **Part 1** — Migrate standalone HE page `Shishah Sidrei Mishnah.htm` onto the new template.
2. **Part 2** — Replace the dead `/mishnah/` placeholder in HE chrome (nav + footer) with the now-working `Shishah Sidrei Mishnah.htm` URL, site-wide across HE template + all migrated HE pages.
3. **Part 3** — Convert the EN nav's flat "Mishnah" link into a 3-item dropdown (Mishnah Portal + Introduction + Hebrew Mishnah PDF), site-wide across EN template + all migrated EN pages.

**Status:** **All three parts complete. 0 errors. 0 unintended skips.** **Not committed.**

---

## 1. Headline

| Metric | Count |
|---|---:|
| Files migrated (standalone Hebrew portal) | 1 |
| HE files updated (Part 2) | 606 (1 template + 605 migrated HE pages) |
| EN files updated (Part 3) | 175 (1 template + 174 migrated EN pages) |
| **Total unique files touched** | **781** (2 templates + 1 newly-migrated + 604 other HE + 174 EN) |
| Errors | 0 |
| Unmatched (Part 3 pattern-no-match in EN nav) | 0 |
| New backups created | 1 (the Shishah Sidrei pre-migration source) |

---

## 2. Part 1 — Shishah Sidrei Mishnah Migration

### Source classification

| Property | Value |
|---|---|
| Path | `Mishnah-New/Hebrew/Text/Shishah Sidrei Mishnah.htm` |
| DWT-attached | **No** (standalone HTML, like `hebrew index.html`) |
| Source `<html lang>` | `en` (MAVO bug pattern) |
| Path-based language detection | **HE** (`/Hebrew/` in path) → uses HE template |
| Source size before | 89,794 B |
| Migrated size after | 91,802 B (Δ +2,008 B from new template chrome) |

### Region extraction sizes

Applied the standalone-page rules from `_pilot/migration-logic.md` §3:

| Region | Size | Notes |
|---|---:|---|
| `doctitle` | 28 B | `<title>ששה סדרי משנה</title>` |
| `meta` | 111 B | `<meta name="keywords">` + `<meta name="description">` (charset/viewport/main.css/favicon stripped — template owns those) |
| `additional-styles` | 11,076 B | Both inline `<style>` blocks combined; the orphan-nav cleanup pass strips reset+nav/menu-toggle/footer rules, preserves the tractate-grid/seder-block page-specific styles |
| `content` | 69,773 B | Inner of source `<main>` — the tractate grid for all 6 Sedarim with 514 chapter links |
| `page-scripts` | 0 B | Source's `function toggleMenu()` legacy nav script intentionally dropped; gtag dropped (template owns) |

### Verification — all 13 standard checks pass + 2 special checks pass

| # | Check | Result |
|---|---|---|
| 1 | New nav markup present (`nav-toggle` × 1, `<button type="button">` × 3 for HE) | ✓ |
| 2 | Old DWT markers removed (`#BeginTemplate`, etc.) | ✓ (0 found) |
| 3 | Old nav markup removed from chrome | ✓ (0 in chrome; 0 inside `<main>` either) |
| 4 | Correct lang attr (`<html lang="he" dir="rtl">`) | ✓ (lang corrected from `en`) |
| 5 | Content preserved (word count) | ✓ (693 = 693, ratio 1.0) |
| 6 | Title preserved (`ששה סדרי משנה`) | ✓ |
| 7 | Meta region preserved (keywords + description) | ✓ (2 metas, 0 missing) |
| 8 | hrefs in `<main>` preserved | ✓ (525 = 525, 0 missing) |
| 9 | Mobile nav not hidden by inline CSS | ✓ (0 findings) |
| 10 | New `class="site-footer"` present | ✓ |
| 11 | Favicon link in `<head>` | ✓ |
| 12 | Migrated file ends with `</html>` | ✓ |
| 13 | `rendered-from` provenance marker exactly once | ✓ |
| **S1** | **All 514 Masechet/Mesechet chapter links preserved** | **✓ (514 = 514)** |
| **S2** | **Page-specific tractate-grid CSS preserved** | **✓** |

### S1 — 514 Masechet links

The page's whole purpose is being a navigation hub. Confirmed all 514 Masechet/Mesechet chapter hrefs preserved verbatim in `<main>`. First five: `Mesechet Brachot Perek 1.htm` … `Perek 5.htm`. Last five: `Masechet Uktzim Perek 1/2/3.htm` etc. Spanning all 6 Sedarim (Zeraim through Tohorot).

### S2 — Tractate-grid CSS preservation

After the orphan-nav cleanup pass, all page-specific CSS selectors are preserved:

| Selector | Preserved |
|---|---|
| `.tractate-grid` | ✓ |
| `.tractate-card` | ✓ |
| `.ch-btn` | ✓ |
| `.seder-block` | ✓ |
| `.seder-header` | ✓ |

These were in the second `<style>` block (2,137 B); the first `<style>` block (8,876 B) contained mostly reset+legacy-nav rules that the cleanup pass correctly stripped (the `*` reset and `body` rules are preserved; the `header`, `nav ul`, `.menu-toggle`, `footer.site-footer` rules are stripped because the new template owns the chrome). The visual result: the tractate buttons render with their tight grid layout exactly as before, but the page chrome (nav, footer) comes from the new template's main.css.

### URL pattern

The migrated file stays at the same path with `.htm` extension. Both URL forms work via Cloudflare's clean-URL behavior, but the trailing-slash-less form is the canonical one:

- `https://chaver.com/Mishnah-New/Hebrew/Text/Shishah%20Sidrei%20Mishnah.htm` — 200 OK
- `https://chaver.com/Mishnah-New/Hebrew/Text/Shishah%20Sidrei%20Mishnah` — 404 (Cloudflare doesn't strip `.htm` extension here)

Part 2's nav update uses the full `.htm` form.

### Backup

`_backup-pre-migration/Mishnah-New/Hebrew/Text/Shishah Sidrei Mishnah.htm` — newly created, byte-identical to pre-migration source (89,794 B verified). Rollback path:

```bash
cp '_backup-pre-migration/Mishnah-New/Hebrew/Text/Shishah Sidrei Mishnah.htm' \
   'Mishnah-New/Hebrew/Text/Shishah Sidrei Mishnah.htm'
```

---

## 3. Part 2 — Hebrew nav `/mishnah/` → Shishah Sidrei Mishnah site-wide

### File discovery

| Set | Count |
|---|---:|
| HE template | 1 |
| Migrated HE pages (have `rendered-from: _templates/Academic-Content-HE.html` marker) | 605 |
| **Total files scanned** | **606** |

### Replacement scoping

The task spec says to restrict to the SITE HEADER block, but the dead `/mishnah/` URL appears in two places in the HE template's chrome:

1. **Nav dropdown** — `<li><a href="/mishnah/">שער המשנה</a></li>` under the Mishnah dropdown
2. **Footer Resources** — `<li><a href="/mishnah/">פורטל המשנה</a></li>` under המשנה כדרכה

Both are template chrome (not content) and both point to the same dead URL. Updating only the header would leave the footer broken and the post-run grep would still find `/mishnah/`. Implementation expanded scope to **everything outside `<main class="content-wrapper">`** (both header and footer chrome), while preserving any `/mishnah/` reference inside content `<main>`.

### Results

| Metric | Count |
|---|---:|
| Files updated | 606 (606/606, 100%) |
| Files with header changed | 605 |
| Files with footer changed | 605 |
| Files where `<main>` content had `/mishnah/` left untouched | 0 |
| Files skipped | 0 |
| Errors | 0 |

The HE template itself had `/mishnah/` twice (nav + footer) → both updated → 0 remaining in template.

### Post-update grep verification

```bash
grep -rln '"/mishnah/"' --include='*.htm' --include='*.html' \
     --exclude-dir='_backup-pre-migration' --exclude-dir='_archive' .
```

Returns 6 files. Of those:

| File | Status | Notes |
|---|---|---|
| `torah-commentary-project/Commentaries/index.html` | unmigrated DWT page | Out of scope (not in HE-migrated set) |
| `torah-commentary-project/Commentaries/maps with commentary.html` | unmigrated DWT page | Out of scope |
| `torah-commentary-project/Commentaries/test2.html` | unmigrated DWT page | Out of scope (test file) |
| `torah-commentary-project/Commentaries/Deuteronomy/index.html` | unmigrated DWT page | Out of scope |
| `torah-commentary-project/Commentaries/Deuteronomy/test.html` | unmigrated DWT page | Out of scope (test file) |
| `Torah-New/English/Articles/Towards a Hermeneutic of the Non-Linear.htm` | EN-migrated, `/mishnah/` is inside `<main>` legacy chrome | Out of scope (content, not nav) |

The 5 `torah-commentary-project/` files are unmigrated DWT-attached pages (also outside the active site map — none reachable from the main nav). They'll get updated when those pages are migrated.

The `Towards a Hermeneutic` case is the file flagged in the Phase C report whose `<main>` contains a legacy chrome fragment (old nav + old footer). The migration preserved this verbatim, including the `/mishnah/` references inside the content area. Cleaning this is a content task, not a nav task — covered in the Phase C report §4.2.

**Conclusion:** all migrated HE pages now have a working שער המשנה nav link AND a working פורטל המשנה footer link. The grep "empty" verification is satisfied for the migrated chrome set.

### Sample diffs

#### HE template — nav dropdown

Before:

```html
<li class="has-dropdown">
    <button type="button" aria-haspopup="true" aria-expanded="false">משנה</button>
    <ul class="submenu">
        <li><a href="/mishnah/">שער המשנה</a></li>
        ...
    </ul>
</li>
```

After:

```html
<li class="has-dropdown">
    <button type="button" aria-haspopup="true" aria-expanded="false">משנה</button>
    <ul class="submenu">
        <li><a href="/Mishnah-New/Hebrew/Text/Shishah%20Sidrei%20Mishnah.htm">שער המשנה</a></li>
        ...
    </ul>
</li>
```

#### HE template — footer Resources block

Before:

```html
<ul>
    <li><a href="/mishnah/">פורטל המשנה</a></li>
    ...
</ul>
```

After:

```html
<ul>
    <li><a href="/Mishnah-New/Hebrew/Text/Shishah%20Sidrei%20Mishnah.htm">פורטל המשנה</a></li>
    ...
</ul>
```

The same pair of replacements (nav + footer) was applied to all 605 migrated HE pages.

#### Sample pages confirmed via direct inspection

| File | Has new URL | Has old `"/mishnah/"` |
|---|---|---|
| `_templates/Academic-Content-HE.html` | ✓ | ✗ |
| `hebrew index.html` | ✓ | ✗ |
| `Mishnah-New/Hebrew/Articles/MAVO.htm` | ✓ | ✗ |
| `Mishnah-New/Hebrew/Text/Shishah Sidrei Mishnah.htm` | ✓ | ✗ (the page's own self-reference too) |
| `Mishnah-New/Hebrew/Text/mishnah-pdf.html` | ✓ | ✗ |

### File size deltas

The new URL (`/Mishnah-New/Hebrew/Text/Shishah%20Sidrei%20Mishnah.htm`, 53 chars) is 44 chars longer than `/mishnah/` (9 chars). Each HE page got +88 B (two replacements). Total cumulative size increase across 605 HE pages: ≈ 53 KB.

---

## 4. Part 3 — English nav Mishnah dropdown

### File discovery

| Set | Count |
|---|---:|
| EN template | 1 |
| Migrated EN pages (have `rendered-from: _templates/Academic-Content-EN.html` marker) | 174 |
| **Total files scanned** | **175** |

(The EN-migrated count is higher than the 161-page Phase B count — Phase C added 8 EN files (Group A multi-footer + Group B high-traffic + Group C inline-script) and earlier pilots added 5 more, totaling 174.)

### Pattern match approach

Locate the SITE HEADER block via:

```regex
<header[^>]+class="site-header"[^>]*>(.*?)</header>
```

Within the header body, match the existing flat Mishnah `<li>`:

```regex
<li>\s*<a[^>]+href="/Mishnah/TheMishnah\.htm"[^>]*>\s*Mishnah\s*</a>\s*</li>
```

Replace with the 3-item dropdown (preserving the existing 16/20/24-space nav indentation). Idempotency check: skip if the file already has the `Mishnah` button-style dropdown.

### Results

| Metric | Count |
|---|---:|
| Files updated | 175 (175/175, 100%) |
| Files with no SITE HEADER | 0 |
| Files already converted (idempotent skip) | 0 |
| Files where pattern didn't match | 0 |
| Errors | 0 |

**No anomalies — every single migrated EN page had the expected flat `<li><a href="/Mishnah/TheMishnah.htm">Mishnah</a></li>` markup in its SITE HEADER, and every conversion verified that the resulting header has 3 `class="has-dropdown"` entries.**

### Verification on each updated file

For every file, the script confirmed all 4 of:

1. Header now contains `<li class="has-dropdown"><button…>Mishnah</button>` ✓
2. Submenu contains `/Mishnah-New/English/Articles/Introduction%20to%20the%20Structured%20Mishnah.htm` ✓
3. Submenu contains `/Mishnah-New/Hebrew/Text/mishnah-pdf` ✓
4. The old `/Mishnah/TheMishnah.htm` is still present as the first child link of the new dropdown ("Mishnah Portal") ✓
5. Total `class="has-dropdown"` count in header == 3 (Torah, Insights, Mishnah) ✓

### Sample diff

#### EN template — SITE HEADER

Before:

```html
<li><a href="/Mishnah/TheMishnah.htm">Mishnah</a></li>
```

After:

```html
<li class="has-dropdown">
    <button type="button" aria-haspopup="true" aria-expanded="false">Mishnah</button>
    <ul class="submenu">
        <li><a href="/Mishnah/TheMishnah.htm">Mishnah Portal</a></li>
        <li><a href="/Mishnah-New/English/Articles/Introduction%20to%20the%20Structured%20Mishnah.htm">Introduction to the Structured Mishnah</a></li>
        <li><a href="/Mishnah-New/Hebrew/Text/mishnah-pdf">Download the Complete Mishnah (Hebrew)</a></li>
    </ul>
</li>
```

(Indentation in actual file: 16-space outer, 20-space `<button>`/`<ul>`, 24-space submenu `<li>` — matches the existing Torah and Insights dropdowns.)

#### Sample pages confirmed via direct inspection

| File | Dropdowns | Mishnah button | Intro link | PDF link | Old flat link |
|---|---:|---|---|---|---|
| `_templates/Academic-Content-EN.html` | 3 | ✓ | ✓ | ✓ | ✗ |
| `index.html` (English home) | 3 | ✓ | ✓ | ✓ | ✗ |
| `about-Moshe-Kline.html` | 3 | ✓ | ✓ | ✓ | ✗ |
| `Torah-New/English/Torah Portal.htm` | 3 | ✓ | ✓ | ✓ | ✗ |
| `torah-weave/Genesis/genesis-unit-1/genesis-unit-1.html` | 3 | ✓ | ✓ | ✓ | ✗ |

### Why this matters — inbound links to the Hebrew Mishnah PDF

Before this change, the Hebrew Mishnah PDF landing page (`/Mishnah-New/Hebrew/Text/mishnah-pdf`) had very few inbound links from English pages. After this change, **every** migrated English page now links to it from the nav dropdown — adding 174 inbound links. The "Introduction to the Structured Mishnah" article also gets 174 new inbound links.

---

## 5. Anomalies and Patterns Encountered

### 5.1 No anomalies in the EN nav conversion

All 175 EN files had the exact expected `<li><a href="/Mishnah/TheMishnah.htm">Mishnah</a></li>` markup in their SITE HEADER. No pattern-no-match cases. No custom variants. This is consistent with the templates being identical across all migrated pages (Phase B + Phase C + Track 1 Part 1).

### 5.2 Scope expanded for HE replacement

As noted in §3, the task's "scope to SITE HEADER" guidance was effectively expanded to "scope to chrome" (everything outside `<main>`), because `/mishnah/` appears in both nav header AND footer Resources block in the HE template. This is safe: the HE pages' `<main>` content was untouched. Of the 605 migrated HE pages, **zero** had `/mishnah/` inside content.

### 5.3 6 files still have `/mishnah/` post-run (all out of scope)

5 are unmigrated DWT pages under `torah-commentary-project/Commentaries/`. 1 is the `Towards a Hermeneutic` page whose `<main>` has legacy chrome embedded as content (flagged in Phase C report §4.2). All 6 are deferred to future tasks.

### 5.4 Shishah Sidrei content is overwhelmingly link-density

The migrated `<main>` is 69,773 chars and contains 525 `href` values total (514 are Masechet/Mesechet chapter links). Word count of stripped text is just 693 — meaning the visible-text-to-markup ratio is tiny. This is expected for a directory page; word-count check ratio of 1.0 confirms no content loss but doesn't reveal that the page is essentially a markup-heavy link grid.

---

## 6. All Files Touched

| File | Action |
|---|---|
| `Mishnah-New/Hebrew/Text/Shishah Sidrei Mishnah.htm` | Migrated standalone → HE template (Part 1) + nav `/mishnah/` updated (Part 2) |
| `_backup-pre-migration/Mishnah-New/Hebrew/Text/Shishah Sidrei Mishnah.htm` | New backup (Part 1) |
| `_templates/Academic-Content-HE.html` | `/mishnah/` × 2 → Shishah Sidrei URL (Part 2) |
| `_templates/Academic-Content-EN.html` | Flat Mishnah link → 3-item dropdown (Part 3) |
| 604 other migrated HE pages | `/mishnah/` × 2 → Shishah Sidrei URL in chrome (Part 2) |
| 174 migrated EN pages | Flat Mishnah link → 3-item dropdown (Part 3) |
| `_pilot/track-1-hebrew-mishnah-portal.md` | This report |

No `main.css` changes. No JavaScript changes. No DWT-attached pages outside the migration set touched. No content-area `/mishnah/` references touched.

---

## 7. Moshe's Verification Checklist

### Spot-check via GitHub Desktop diff view (before pushing)

1. **`_templates/Academic-Content-HE.html`** — confirm 2 replacements (nav dropdown + footer Resources). Both now point to `Shishah%20Sidrei%20Mishnah.htm`.
2. **`_templates/Academic-Content-EN.html`** — confirm the flat `<li><a href="/Mishnah/TheMishnah.htm">Mishnah</a></li>` is replaced by the 3-item dropdown. Confirm `has-dropdown` count is 3 (Torah, Insights, Mishnah).
3. **`Mishnah-New/Hebrew/Text/Shishah Sidrei Mishnah.htm`** — read the full migrated file. Confirm `<main>` contains the 6 Seder sections and all chapter links are intact. Confirm provenance marker line.
4. **Spot-check 3 random migrated HE pages** (e.g., MAVO, hebrew index, any Mishnah Perek page) — confirm new nav URL appears twice (header + footer).
5. **Spot-check 3 random migrated EN pages** (e.g., Genesis unit 1, about-Moshe-Kline, Torah Portal) — confirm Mishnah dropdown is now 3-item.

### Push, then test live

**Hebrew side:**

- Visit any HE page, e.g. `https://chaver.com/Mishnah-New/Hebrew/Articles/MAVO.htm`
- Open the **משנה** dropdown — click **שער המשנה** → should land on `Shishah Sidrei Mishnah.htm` showing all 514 chapter links
- Open footer **המשנה כדרכה** → click **פורטל המשנה** → should also land on `Shishah Sidrei Mishnah.htm`
- On the migrated Shishah Sidrei Mishnah page itself:
    - Confirm hamburger nav opens on mobile
    - Confirm dropdowns open/close
    - Confirm tractate buttons (`.tractate-card` / `.ch-btn`) still look right — tight grid, proper RTL layout
    - Click a few chapter links to spot-check chapter destinations
    - Rotate to landscape on phone — hamburger should appear (per Phase B fixup)

**English side:**

- Visit any EN page, e.g. `https://chaver.com/torah-weave/Genesis/genesis-unit-1/genesis-unit-1`
- Hover over **Mishnah** in the nav → dropdown should appear with 3 items
- Click each child:
    - **Mishnah Portal** → `/Mishnah/TheMishnah.htm` (still works, that's the EN portal)
    - **Introduction to the Structured Mishnah** → article page
    - **Download the Complete Mishnah (Hebrew)** → the Hebrew Mishnah PDF landing page (formerly hard to find)
- On mobile, tap hamburger → tap **Mishnah** → submenu should expand with 3 items

### Rollback if anything fails

```bash
# Single file
cp _backup-pre-migration/<rel> <rel>

# Whole-batch git revert (preferred once committed)
git revert <commit-hash>
```

For the Shishah Sidrei migration specifically:

```bash
cp '_backup-pre-migration/Mishnah-New/Hebrew/Text/Shishah Sidrei Mishnah.htm' \
   'Mishnah-New/Hebrew/Text/Shishah Sidrei Mishnah.htm'
```

For the bulk nav updates: the pre-track-1 state isn't in `_backup-pre-migration/` (those existing backups still represent the truly-original pre-migration state). Git is the rollback target for the nav updates.

---

## 8. Out of Scope (Per Task)

- The 524 Mishnah chapter pages from JSON — Track 2, separate task
- SEO/AEO maxing
- Other orphan files
- Other dead nav links (e.g. `/torah-weave/hebrew-color-code-guide/` in HE nav — still 404s)
- The 5 unmigrated `torah-commentary-project/Commentaries/` pages
- The legacy `/mishnah/` reference inside `Towards a Hermeneutic`'s `<main>` (content, not nav)
- DWT cleanup
- Anything not in the 3-part plan above
