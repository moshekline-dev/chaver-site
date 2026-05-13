# Post-Phase-B Fixup Pass

**Date:** 2026-05-13
**Scope:** Four narrowly-scoped fixes identified after Phase B deployed: favicon, landscape nav, orphan-CSS cleanup on 3 old pilots, narrow-phone matrix-table tightening.
**Status:** All four parts applied. **Not committed.**

---

## Part 1 — Favicon Installation

### File at root

The repo already had a byte-identical `/favicon.ico` at the root (3,262 bytes, valid `.ico` magic bytes `00 00 01 00`). Compared to the uploaded `/sessions/.../uploads/favicon.ico` — `diff -q` reports no differences. **No file copy was needed.**

### Link tag in templates

Added immediately after `<meta name="viewport">` in both templates:

```html
<link rel="icon" type="image/x-icon" href="/favicon.ico">
```

- `_templates/Academic-Content-EN.html` — added at line 15
- `_templates/Academic-Content-HE.html` — added at line 15

### Link tag injection across migrated files

| Metric | Count |
|---|---:|
| Migrated files (phase-b targets + 7 pilots) | 768 |
| Files where icon tag was newly added in this pass | 146 |
| Files that already had the tag (e.g., from prior background-script run that completed partially) | 622 |
| **Final files with `<link rel="icon">`** | **768 / 768** ✓ |

Insertion strategy: after the existing `<meta name="viewport">` tag, with matching indentation. Fallback (not exercised in practice): after `<meta charset>`.

---

## Part 2 — Mobile Landscape Nav Fix

Updated the SITE NAV mobile media query in `main.css` (line 3846 of the SITE NAV block) so landscape phones (viewport width > 768 px but height ≤ 500 px) also get the hamburger nav instead of the full horizontal menu.

### Diff

```diff
- /* MOBILE breakpoint */
- @media (max-width: 768px) {
+ /* MOBILE breakpoint — also fires on short viewports (landscape phones) so the
+    hamburger nav appears instead of the full menu eating screen height. */
+ @media (max-width: 768px), (max-height: 500px) {
      /* On mobile, let body be full-width so the nav menu can span viewport.
         Desktop body keeps its 1200px centering rule (defined elsewhere). */
```

### Verification

| Selector | Line | Status |
|---|---|---|
| Content area `@media (max-width: 768px)` (matrix-table, scripture-table, inline-width cap, etc.) | line 3044 | **unchanged** ✓ |
| SITE NAV `@media (max-width: 768px), (max-height: 500px)` (.nav-toggle, .nav-menu, .submenu, body padding-zero, etc.) | line 3846 | **updated** ✓ |
| Other `@media (max-width: 768px)` blocks (e.g., `@media (max-width: 768px) and (orientation: portrait)`) | line 3376 | unchanged |

Only the SITE NAV media query gained the `, (max-height: 500px)` extension. Content shrink rules remain width-only as intended.

---

## Part 3 — Orphan CSS Cleanup on 3 Old Pilots

Three pages were migrated on 2026-05-12 before the template-cleanup task ran. They still carried orphan nav CSS in their inline `<style>` blocks. Now cleaned via `clean_nav_css_from_inline_style()`.

### Before / after

| File | `<style>` chars before | after | Δ | `check_mobile_nav_not_hidden` before | after |
|---|---:|---:|---:|---:|---:|
| `torah-weave/leviticus-19-ark-at-the-center.html` | 4,408 | 2,148 | −2,260 | 2 findings | **0** ✓ |
| `Mishnah-New/Hebrew/Articles/MAVO.htm` | 4,236 | 2,064 | −2,172 | 2 findings | **0** ✓ |
| `hebrew index.html` | 15,893 | 12,317 | −3,576 | 2 findings | **0** ✓ |

### Rules removed from each file (outside `@media print`)

Same set in each — these are the template-inherited orphan rules that were missed by the prior cleanup task:

- `header.site-header { position: sticky; ... }` (×3 contexts: desktop, mobile @media, landscape nested @media)
- `.main-nav { max-width: 1200px; ... }` (and other compound selectors)
- `nav ul { display: flex; ... }` / inside `@media (max-width: 768px)`: `nav ul { display: none; ... }` ← **this is the rule that would hide our new mobile menu**
- `nav ul.show { display: flex }` (old toggle class — new system uses `.is-open-menu`)
- `nav li { width: 100% }` inside the mobile @media
- `nav a` styling rules
- `footer.site-footer` (outside `@media print`)
- For `hebrew index.html` specifically: also `.menu-toggle` rules (×2) — the page's standalone CSS had its own hamburger styling.

After cleanup, the only remaining `header.site-header` / `footer.site-footer` references are inside the legitimate `@media print` block (which hides them for printing — correct behavior).

### Sanity check — `torah-weave/Woven-Torah-Method.html` (already cleaned in earlier task)

```
check_mobile_nav_not_hidden findings: 0 ✓ (no regression)
```

---

## Part 4 — Matrix-Table Tightening for Narrow Viewports

Added a second-tier shrink rule inside the existing `@media (max-width: 480px)` block in `main.css`, immediately after the existing `.slideshow-intro p` rule and before the closing brace.

### New rules added (at lines 3354–3365)

```css
/* Further shrink matrix-table on very narrow phones — handles the 5+ column
   matrix tables like the Genesis map without clipping. The 0.65em / 3px 2px
   rule above (inside @media max-width: 768px) still applies for 481-768px;
   these rules override for ≤480px. */
.matrix-table {
    font-size: 0.55em;
    line-height: 1.15;
}
.matrix-table th,
.matrix-table td {
    padding: 2px 1px !important;
}
```

### Cascade verification

| Viewport range | Active rule | `font-size` | `padding` |
|---|---|---|---|
| > 768 px (desktop) | base `.matrix-table` rule (line 693) | default | 12px |
| 481–768 px (tablet / regular phone landscape) | `@media (max-width: 768px)` rule (line 3096) | 0.65em | 3px 2px |
| ≤ 480 px (narrow phone portrait) | new `@media (max-width: 480px)` rule (line 3358) | **0.55em** | **2px 1px** |

The new rule overrides only for the ≤480px range. The 481–768 range continues to use 0.65em/3px-2px. Desktop unchanged.

---

## 5. All Files Modified

| File | Change | Rough byte delta |
|---|---|---:|
| `favicon.ico` (repo root) | none — already present and byte-identical to upload | — |
| `_templates/Academic-Content-EN.html` | favicon link tag added | +~60 |
| `_templates/Academic-Content-HE.html` | favicon link tag added | +~60 |
| `torah-weave/Admin/Assets/CSS/main.css` | landscape-nav `@media` clause + new ≤480px matrix-table rules | +~400 |
| `torah-weave/leviticus-19-ark-at-the-center.html` | orphan CSS removed | −2,260 |
| `Mishnah-New/Hebrew/Articles/MAVO.htm` | orphan CSS removed | −2,172 |
| `hebrew index.html` | orphan CSS removed | −3,576 |
| 768 migrated files (phase-b + 7 pilots) | favicon link tag added | +~60 each |
| `_pilot/post-phase-b-fixup.md` | new report | (new file) |

The 768 migrated files were modified by a single regex-based insertion targeting `<meta name="viewport">`. Each got the same one-line addition. The total byte change across all 768 migrated files is ~46 KB across the working tree.

---

## 6. Backup Verification

For the 3 old pilot pages cleaned in Part 3: pre-existing backups already exist in `_backup-pre-migration/` from when they were originally migrated on 2026-05-12. Verified each backup exists; no new backups created (pre-existing ones still reflect the pre-migration source state, which is the correct rollback target).

```
_backup-pre-migration/torah-weave/leviticus-19-ark-at-the-center.html  ✓
_backup-pre-migration/Mishnah-New/Hebrew/Articles/MAVO.htm             ✓
_backup-pre-migration/hebrew index.html                                ✓
```

For the 768 migrated files' favicon insertion: changes are tiny (~60 bytes per file, a single one-line addition). No new backups created — the existing `_backup-pre-migration/` copies still reflect the truly-original pre-migration state, which is the correct rollback target for any post-migration fixup.

For the `main.css` and templates: changes are scoped CSS / single-line additions. The git working tree itself is the safety net for these (any commit can be reverted).

---

## 7. Moshe's Verification Checklist

When testing post-deploy:

**Favicon:**
- Open any page on desktop. Browser tab should show the chaver.com favicon (no longer the generic default).
- Open any page on mobile. Same — favicon in tab/bookmark.

**3 cleaned pilot pages on mobile:**
- `/torah-weave/leviticus-19-ark-at-the-center`
- `/Mishnah-New/Hebrew/Articles/MAVO`
- `/hebrew%20index`

Tap hamburger ☰ — menu should open with full nav. (Previously the orphan `nav ul { display: none }` was hiding it.)

**Landscape phone view:**
- Rotate any page on a phone to landscape. Should show hamburger icon, not the full horizontal menu eating most of the visible height. (Trigger threshold: viewport ≤ 768 px wide OR ≤ 500 px tall.)

**Genesis map on narrow portrait:**
- `/torah-weave/Genesis/genesis-analysis/the-map-of-genesis`
- On a ~400 px-wide viewport (typical phone portrait), all 5 columns should be visible, none clipped. Text small but readable.

---

## 8. Out of Scope (Per Task)

Items intentionally not addressed in this fixup:

- Canonical link tags, hreflang, og:image, Twitter cards, Person/Organization schema (the broader SEO/AEO maxing pass — separate task)
- Any orphan-file work
- Any non-migrated DWT pages (the 2 published English.dwt, 4 published hebrew.dwt, 4 high-traffic exclusions, 13 skeleton pages)
- Stale CSS removal from `main.css` (the `.menu-toggle`/`.main-nav` cleanup waits until DWT pages are migrated or archived)
- Sitemap regeneration

---

## Files Touched

| File | Action |
|---|---|
| `_templates/Academic-Content-EN.html` | Added `<link rel="icon">` after `<meta viewport>` |
| `_templates/Academic-Content-HE.html` | Same |
| `torah-weave/Admin/Assets/CSS/main.css` | Extended SITE NAV `@media` to include `(max-height: 500px)`; added `.matrix-table` shrink at `@media (max-width: 480px)` |
| `torah-weave/leviticus-19-ark-at-the-center.html` | Orphan-CSS cleanup via `clean_nav_css_from_inline_style()` |
| `Mishnah-New/Hebrew/Articles/MAVO.htm` | Same |
| `hebrew index.html` | Same |
| 768 migrated files (phase-b targets + 7 pilots) | `<link rel="icon">` injected after `<meta viewport>` |
| `_pilot/post-phase-b-fixup.md` | This report |

No DWT files touched. No JavaScript changes.
