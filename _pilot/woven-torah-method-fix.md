# Woven-Torah-Method Fix + Migration Cleanup Utility

**Date:** 2026-05-13
**Status:** `torah-weave/Woven-Torah-Method.html` cleaned. New utility `_pilot/nav_css_cleanup.py` added (importable for the bulk migration). **Not committed.**

---

## ⚠ Diagnosis Correction Before the Rest of the Report

The task spec attributed the orphan nav CSS to "the page's editable regions (especially the `meta` region)". When I inspected the actual content, that turned out not to be the case here:

- The original `meta` region in the source DWT file (4,573 chars) contains **zero `<style>` blocks** — it's all `<meta>`, `<link>`, schema.org JSON-LD, etc.
- The orphan nav CSS in the migrated file is in the inline `<style>` block that came from the **template's** "CRITICAL DWT LAYOUT STYLES ONLY" section.
- Specifically, lines 43–206 of `_templates/Academic-Content-EN.html` still contain rules like `header.site-header { position: sticky }`, `nav ul { display: none }` (inside `@media (max-width: 768px)`), `.main-nav`, etc. These were template scaffolding that was missed by earlier orphan-CSS cleanup tasks.

This means **every page migrated from these templates** (including the other three pilot pages: leviticus, MAVO, hebrew-index) will inherit the same orphan rules. The per-page cleanup utility below is the right immediate response, but the long-term fix is to strip those rules from the **template** so the cleanup pass becomes optional.

I'm flagging this rather than touching the template in this task because (a) the spec scoped this to a per-page fix and (b) template edits are high blast-radius. Recommended follow-up: run `clean_nav_css_from_inline_style()` on both `Academic-Content-EN.html` and `Academic-Content-HE.html` themselves.

---

## 1. Woven-Torah-Method — What Was Removed and What Stayed

### Removed (CSS rules deleted from the inline `<style>` block)

Outside any `@media print`:

- `header.site-header { position: sticky; top: 0; z-index: 1000 }`
- `.main-nav { max-width: 1200px; margin: 0 auto; padding: 0.3rem 20px }`
- `nav ul { list-style: none; display: flex; ... gap: 2.5rem }`
- `nav a { text-decoration: none; padding: 0.25rem 0.75rem; ... }`
- `footer.site-footer { margin-top: 80px; padding: 40px 20px 20px }`

Inside `@media (max-width: 768px)` (the outer mobile block):

- `header.site-header { position: relative }`
- `nav ul { display: none; flex-direction: column; ... }` ← the rule that the verification check correctly flagged
- `nav ul.show { display: flex }` ← old class name (new system uses `.is-open-menu`)
- `nav li { width: 100% }`
- `nav a { display: block; padding: 1rem }`

Inside nested `@media (max-height: 500px) and (orientation: landscape)`:

- All `nav ul`, `nav ul.show`, `nav li`, `nav a` rules (same set as the outer mobile block)

### Kept (still in the inline `<style>` block)

- `* { margin: 0; padding: 0; box-sizing: border-box }` (reset)
- `main.content-wrapper { ... }` (desktop content layout)
- `main.content-wrapper { padding: 30px 15px }` (mobile content padding)
- `main.content-wrapper { padding: 15px 10px }` (landscape phone content padding)
- `main.content-wrapper { padding: 20px 15px }` (smaller mobile)
- `.footer-container`, `.footer-content`, `.footer-section ul`, `.footer-bottom`
- `.footer-content { grid-template-columns: 1fr; gap: 30px }` (mobile footer stack)
- The entire `@media print { header.site-header, footer.site-footer { display: none } main.content-wrapper { padding: 0 } }` block — preserved verbatim per spec

### Verification — pass

| Check | Before | After |
|---|---:|---:|
| `header.site-header` occurrences in inline `<style>` | 3 | 1 (inside `@media print` only) |
| `footer.site-footer` | 2 | 1 (inside `@media print` only) |
| `nav ul` | 5 | 0 |
| `nav li` | 2 | 0 |
| `nav a` | 2 | 0 |
| `.main-nav` | 1 | 0 |
| `.menu-toggle`, `.has-dropdown`, `.dropdown`, `.site-banner` | 0/0/0/0 | 0/0/0/0 |
| `check_mobile_nav_not_hidden()` findings | **2** (`nav ul { display: none }` × 2, in outer mobile and nested landscape) | **0** ✓ |
| Content-specific CSS preserved (`main.content-wrapper`, footer-related, reset) | — | All ✓ (5/5 `main.content-wrapper` occurrences kept; all 4 footer-* tokens kept; reset rule kept) |
| File size | 44,378 bytes | 42,265 bytes (−2,113) |

---

## 2. The Utility Functions (saved to `_pilot/nav_css_cleanup.py`)

Two utilities for the bulk migration to import:

### `clean_nav_css_from_inline_style(html: str) → str`

Strips nav-targeting rules from every inline `<style>...</style>` block in the input HTML and returns the cleaned HTML. Preserves comments and whitespace around kept rules.

**Rules removed** (selector patterns, OUTSIDE `@media print`):

```
header.site-header        # the bare class on header
footer.site-footer        # the bare class on footer
nav, nav ul, nav li, nav a # generic nav element selectors
.main-nav                  # old wrapper class
.menu-toggle               # old hamburger class
.has-dropdown              # old dropdown wrapper class
.dropdown, .dropdown-toggle  # old dropdown classes
.site-banner               # new template owns this
```

**Rules preserved:**

- Any `@media print { ... }` block — kept verbatim (rules hiding chrome for print are correct).
- Any non-matching selector (`*`, `main.content-wrapper`, `.unit-header-section`, `.structure-box`, `.footer-container`, `.footer-content`, `.footer-section ul`, `.footer-bottom`, custom page-specific classes, etc.).
- Empty `@media (max-width: 768px)` blocks (or other non-print at-rules) after filtering are dropped entirely; non-empty are kept with the cleaned inner contents.
- Recurses through nested `@media` blocks (e.g., `@media (max-width: 768px) { @media (max-height: 500px) and (orientation: landscape) { ... } }`).

The parser uses a brace-balanced top-level rule walker (not regex on rules), so it correctly handles comments inside selectors, nested at-rules, and arbitrary whitespace.

### `check_mobile_nav_not_hidden(html: str) → list[str]`

Scans inline `<style>` blocks for rules that — at mobile widths (any `@media (max-width: ≤768px)`) — set `display: none` on a selector that would hit the new nav:

```
nav ul          # generic descendant of <nav>
.nav-menu       # our new top-level menu class
header.site-header  # would hide entire header
header > nav        # would hide a direct nav child
```

Returns a list of strings describing each offending rule (empty list ⇒ pass). Recurses through nested `@media` and only flags rules in a mobile context.

### Usage in the bulk migration script

```python
import sys
sys.path.insert(0, '_pilot')  # or wherever the helper lives
from nav_css_cleanup import (
    clean_nav_css_from_inline_style,
    check_mobile_nav_not_hidden,
)

# After substituting region content into the template:
migrated_html = render(template, regions)
migrated_html = clean_nav_css_from_inline_style(migrated_html)

# Verification:
findings = check_mobile_nav_not_hidden(migrated_html)
if findings:
    # FAIL — flag this file for manual review, do NOT save
    print(f"Mobile-nav-hidden check FAILED: {findings}")
    skip_this_file()
else:
    # Pass — save the migrated file
    save(migrated_html)
```

The cleanup pass should run **after** template substitution (so it catches both template-inherited orphan rules and any orphan rules that might be in source page regions). The check should run on the cleaned output, immediately before saving.

---

## 3. Migration Logic Document

Also writing `_pilot/migration-logic.md` (companion document) that captures:

- The full extraction algorithm (DWT regions, name remapping for `hebrew.dwt`, standalone-page handling)
- Language detection rules (path-based override of bogus `lang="en"`)
- The CSS cleanup utility
- The mobile-nav-hidden verification check
- The 8 standard verification checks from the pilot task

That doc is the spec for the bulk migration script.

---

## 4. Expected Behavior on Deploy

`https://chaver.com/torah-weave/Woven-Torah-Method`:

**Desktop:** article body, headings, structure boxes render unchanged. Hover dropdowns work on the new nav at the top of the page.

**Mobile:** hamburger ☰ visible (now FIXED — previously the inline `nav ul { display: none }` rule was hiding any `<ul>` inside any `<nav>` element; the new nav's `<ul class="nav-menu">` isn't inside a `<nav>` so it actually wasn't being hit, but other pages with content-area `<nav>` containers would have been). Tap hamburger → menu drops down → tap parent → submenu expands → tap leaf → navigates. Article body renders below the header unaffected.

---

## 5. Note on the Other 3 Pilot Pages

The same template-inherited orphan rules are present in:

- `torah-weave/leviticus-19-ark-at-the-center.html`
- `Mishnah-New/Hebrew/Articles/MAVO.htm`
- `hebrew index.html`

Moshe confirmed mobile verification passed for those three. That's because the specific structural collision in Woven-Torah-Method (a content-area `<nav class="unit-navigation">` interacting with the orphan `nav ul` rule) doesn't exist on those three. But the orphan rules are still there, dead code, slightly increasing file size and creating cascade risk on future content additions.

**Recommended follow-up before the bulk migration:** run `clean_nav_css_from_inline_style()` on each of those three migrated pages too, and on both `_templates/*.html` source templates. That makes the orphan rules disappear globally and the per-page cleanup pass becomes a belt-and-suspenders check rather than a load-bearing fix.

---

## 6. Files Touched

| File | Action |
|---|---|
| `torah-weave/Woven-Torah-Method.html` | Inline `<style>` block cleaned: 4,261 → 2,148 chars (−2,113); file 44,378 → 42,265 bytes |
| `_pilot/nav_css_cleanup.py` | **New** — reusable utility with `clean_nav_css_from_inline_style()` + `check_mobile_nav_not_hidden()` |
| `_pilot/migration-logic.md` | **New** — bulk-migration spec document referencing the utility |
| `_pilot/woven-torah-method-fix.md` | This report |

No template changes. No JS changes. No `main.css` changes. No DWT files touched.
