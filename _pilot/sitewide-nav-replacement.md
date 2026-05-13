# Site-Wide Nav Replacement — One Coordinated Commit

**Date:** 2026-05-12
**Strategy:** Replace the entire nav layer (HTML markup, JS, CSS, inline `<style>` leftovers) across both templates, main.css, and the preview — using a verified `<button>`-based pattern. Old nav system is deleted wholesale; new system written cleanly.
**Status:** Applied across four files. **Not committed.**

---

## 1. `main.css` — Old Block Out, New Block In

### Removed

The existing `NAV DROPDOWN — CLASS-TOGGLE PATTERN` block (~65 lines, lines 3837–3902 in the prior state) was deleted. Search for those rule patterns now turns up zero hits — there is no remaining `.has-dropdown` or `.dropdown-toggle` rule anywhere else in `main.css`. The earlier history-task blocks (`MOBILE NAV — FLAT LIST APPROACH`, `MOBILE NAV DROPDOWN — VISIBILITY + LAYOUT`, standalone `NAV DROPDOWN HOVER BEHAVIOR`) had already been removed in prior tasks and didn't reappear.

### Added

The new `SITE NAV — chaver.com` block (lines 3837–3979, ~143 lines). The block defines:

- `.nav-row` (flex header layout, 1200px max-width container)
- `.nav-brand` (site name on the left/right of the row)
- `.nav-toggle` (hamburger button: hidden on desktop, shown on mobile)
- `.nav-menu` (top-level horizontal `<ul>`)
- `.nav-menu > li > a` and `.nav-menu > li > button` (top-level item styling — buttons styled to match links)
- `.has-dropdown > button::after` (▾ chevron on dropdown buttons)
- `.submenu` (white absolute-positioned panel with shadow and rounded corners; default `display: none`)
- `@media (hover: hover) and (pointer: fine)` → `.has-dropdown:hover .submenu { display: block }` (desktop hover open)
- `.has-dropdown.is-open > .submenu { display: block }` (JS-driven open)
- `@media (max-width: 768px)` block — converts the nav to mobile: hamburger visible, menu collapses to a vertical dropdown below the header, submenus flow inline below their parent buttons, items full-width and indented

`header.site-header` is unchanged (still has `position: sticky` which provides the positioning context for absolute submenus on desktop).

---

## 2. HE Template Changes (3 sub-changes)

### A — Inline `<style>` cleanup (4 deletions)

| Deleted | Was a rule for |
|---|---|
| `.menu-toggle { display: none; background: none; ... }` block | Old hamburger desktop style |
| `.menu-toggle { display: block }` (inside mobile `@media`) | Old hamburger mobile visibility |
| `.menu-toggle { display: block }` (inside landscape `@media`) | Old hamburger landscape visibility |
| `.menu-toggle` comma entry inside `@media print` rule | Hide old hamburger in print |

The DROPDOWN MENU section (`.has-dropdown`, `.has-dropdown details`, `.has-dropdown summary`, `.dropdown`, etc.) had been removed in a prior task, so the only orphans left were the four `.menu-toggle` references.

After these edits, the inline `<style>` block has zero references to `.has-dropdown`, `.dropdown`, `.dropdown-toggle`, `details`, `summary`, or `.menu-toggle`. The remaining `nav ul {}` / `nav a {}` rules apply to no element in the new structure (since the new markup uses `.nav-menu` and `.nav-row` inside a `<div>`, not a `<nav>`) but are benign — they don't break anything.

### B — `<header>` replacement

The old structure with `<nav class="main-nav">`, `<button class="menu-toggle">`, and `<ul id="nav-menu">` (containing `<a href="#" class="dropdown-toggle">` plus orphan `<ul class="dropdown">`) was replaced with the new structure:

- `<header class="site-header">`
  - `<div class="nav-row">`
    - `<div class="nav-brand">חבר</div>`
    - `<button class="nav-toggle" aria-label="פתח/סגור תפריט" aria-expanded="false">☰</button>`
    - `<ul class="nav-menu" id="primary-menu">`
      - 1 home `<li><a>` (דף הבית)
      - 3 `<li class="has-dropdown">` blocks (תורה / משנה / נתונים), each with `<button type="button">` and `<ul class="submenu">`
      - 2 leaf `<li><a>` (צור קשר, English)

All Hebrew labels and URLs unchanged from prior state.

### C — `<script>` replacement

The 40+ line block (`toggleMenu`, click-outside, class-toggle dropdown handler) is replaced with the new IIFE-wrapped script (~50 lines):

- Captures `.nav-toggle` and `.nav-menu` once
- Hamburger handler: toggles `.is-open-menu` on the menu; updates `aria-expanded` on the toggle
- Dropdown handler: listens on `.has-dropdown > button`; calls `stopPropagation()`; closes all others; opens or closes this one; updates `aria-expanded` on each
- Click-outside: tests `!e.target.closest('.site-header')`; if outside, closes the menu and all dropdowns

The script is wrapped in an IIFE so no global names are introduced. `toggleMenu()` no longer exists in the global scope (and isn't referenced by any HTML anymore — the new hamburger has no `onclick` attribute).

---

## 3. EN Template Changes

Identical structure to HE, with English content. Inline `<style>` cleanup is byte-identical (4 `.menu-toggle` removals). Header replaced with the English version (1 home, 2 dropdowns: Torah/3 items and Insights/10 items, 4 leaf items including עברית as Hebrew toggle). Script is identical to HE's.

---

## 4. Preview Updated

`_pilot/hebrew-nav-render-preview.html` got the same three sub-changes as the HE template: inline `<style>` cleanup, header replacement, script replacement. The preview's other regions (sample content, footer) and references to `/torah-weave/Admin/Assets/CSS/main.css` are unchanged.

---

## 5. Verification — 14 Programmatic Checks, All Passed

### `main.css` (6 checks)

| # | Check | Result |
|---|---|---|
| 1 | New `SITE NAV — chaver.com` block present (single, comment header) | ✓ line 3838 |
| 2 | No `has-dropdown` or `dropdown-toggle` outside the new SITE NAV block | ✓ Grep returned 0 matches for `dropdown-toggle`; `has-dropdown` only appears in the new block |
| 3 | Has `.nav-row`, `.nav-brand`, `.nav-toggle`, `.nav-menu`, `.has-dropdown`, `.submenu` rules | ✓ all present in the new block |
| 4 | Has `@media (hover: hover) and (pointer: fine)` with `.has-dropdown:hover .submenu` rule | ✓ |
| 5 | Has `@media (max-width: 768px)` with `.nav-toggle { display: block }` and `.nav-menu.is-open-menu { display: flex }` rules | ✓ |
| 6 | `header.site-header { background: linear-gradient(...) }` unchanged | ✓ (untouched this task) |

### HE template (4 checks)

| # | Check | Result |
|---|---|---|
| 7 | Inline `<style>` has zero references to `.has-dropdown`, `.dropdown`, `.dropdown-toggle`, `details`, `summary`, `.menu-toggle` | ✓ Grep returns 0 matches in inline CSS region |
| 8 | `<header>` contains `.nav-toggle` button, `<ul class="nav-menu">`, and 3 `<li class="has-dropdown">` | ✓ |
| 9 | Each `.has-dropdown` has `<button type="button">` (not `<a>`) and `<ul class="submenu">` | ✓ buttons at lines 228, 236, 245 — all `<button type="button" aria-haspopup="true" aria-expanded="false">` |
| 10 | Inline `<script>` contains the new IIFE handler with `.has-dropdown > button` selector | ✓ line 331 |

### EN template (3 checks)

| # | Check | Result |
|---|---|---|
| 11 | Same inline `<style>` cleanup as HE | ✓ zero matches for orphan selectors |
| 12 | Same nav HTML structure but with English content + 2 dropdowns | ✓ Torah/3 items and Insights/10 items |
| 13 | Same JS handler | ✓ IIFE with `.has-dropdown > button` selector |

### Preview (1 check)

| # | Check | Result |
|---|---|---|
| 14 | `_pilot/hebrew-nav-render-preview.html` regenerated with the same changes | ✓ all three changes applied |

---

## 6. Unexpected State Encountered

A few of the spec's named blocks didn't exist in `main.css` to delete — they had already been replaced in prior tasks:

- `MOBILE NAV — FLAT LIST APPROACH` — not present (was replaced last task with `NAV DROPDOWN BEHAVIOR — DESKTOP HOVER + MOBILE HIDE`, which itself was then replaced with `NAV DROPDOWN — CLASS-TOGGLE PATTERN`)
- `NAV DROPDOWN BEHAVIOR — DESKTOP HOVER + MOBILE HIDE` — not present (already replaced)
- `MOBILE NAV DROPDOWN — VISIBILITY + LAYOUT` — not present (already replaced)

Only `NAV DROPDOWN — CLASS-TOGGLE PATTERN` was actually in the file. That's the block I replaced. End state in `main.css` is exactly what the spec describes either way: a single new `SITE NAV — chaver.com` block, no other dropdown rules anywhere.

Similarly for the templates: the orphan `.has-dropdown`, `.dropdown`, `details`, `summary` rules had already been removed in the prior "Working Mobile Dropdowns — Coordinated Single Commit" task. The only remaining orphan in the inline `<style>` was the four `.menu-toggle` rules, which this task cleaned up. The result is the same: zero references to any of those orphan selectors after this commit.

---

## 7. Expected Behavior After Deploy

### Desktop (≥768 px, hover-capable)

- Beige gradient header across the top of every page on the new template.
- Brand text on the right (HE, RTL) or left (EN, LTR) of the row.
- Hover over **Torah/Insights/תורה/משנה/נתונים** → white submenu panel appears below the button with shadow and rounded corners.
- Click the dropdown button → also opens (and closes any other open dropdown); `aria-expanded` flips to `true`.
- Move cursor away → submenu closes.
- Click outside the header → all dropdowns close; `aria-expanded` flips back to `false`.

### Mobile (<768 px)

- Header shows brand + ☰ hamburger icon.
- Tap hamburger → menu drops down below the header in the beige gradient color, full-width.
- Tap **תורה** → its children appear indented below, semi-transparent background.
- Tap **משנה** while **תורה** is open → תורה closes, משנה opens.
- Tap a leaf item → navigates.
- Tap outside the header → menu and all dropdowns close.

### Accessibility

- Dropdown toggles are `<button>` elements (semantically correct for "this opens something").
- `aria-haspopup="true"` on each dropdown button.
- `aria-expanded` flips dynamically.
- `aria-label` on the hamburger (Hebrew on HE template, English on EN).

---

## 8. Files Touched

| File | Action |
|---|---|
| `torah-weave/Admin/Assets/CSS/main.css` | Old `NAV DROPDOWN — CLASS-TOGGLE PATTERN` block (~65 lines) replaced with `SITE NAV — chaver.com` block (~143 lines). Net +78 lines |
| `_templates/Academic-Content-HE.html` | 4 `.menu-toggle` deletions in inline `<style>`; `<header>` replaced; `<script>` replaced |
| `_templates/Academic-Content-EN.html` | Same three changes with English content |
| `_pilot/hebrew-nav-render-preview.html` | Mirrors HE template changes |
| `_pilot/sitewide-nav-replacement.md` | This report |

**Out of scope (per task spec):** DWT files in `Dynamic Web Templates/`. Legacy DWT-attached `.htm` pages keep their original nav until you decide to migrate them. The `/mishnah/` 404 is a separate content task.
