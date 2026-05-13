# Matrix Table — Horizontal Scroll on Mobile

**Date:** 2026-05-13
**File:** `torah-weave/Admin/Assets/CSS/main.css`
**Strategy:** On mobile, wide `.matrix-table` elements become scrollable blocks instead of expanding the page width past the viewport.
**Status:** Added. **Not committed.**

---

## 1. Where the Rule Was Placed

Inserted at **lines 3093–3102** of `main.css`, inside the existing content-focused `@media (max-width: 768px)` block (which spans lines 3044–3285).

The new rule sits **immediately before** the existing `.torah-map-container .matrix-table { font-size: 0.75em }` rule — natural neighbor (matrix-table-related) and the right cascade order (general rule first, then the more-specific scoped variant).

```css
/* Wide tables (e.g., matrix-table with 8 columns) scroll horizontally
   inside their own area rather than expanding the page width.
   Page stays at viewport width — hamburger stays visible. */
.matrix-table {
    display: block;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    white-space: nowrap;
    max-width: 100%;
}
```

### What each declaration does

- **`display: block`** — turns the `<table>` from `display: table` to `display: block`. `<table>` elements normally ignore `overflow`; switching to `block` makes them respect it.
- **`overflow-x: auto`** — horizontal scrollbar appears when content is wider than the block.
- **`-webkit-overflow-scrolling: touch`** — momentum scroll on iOS Safari (smoother UX inside the scroll region).
- **`white-space: nowrap`** — cell contents don't wrap; the table grows horizontally and scrolls instead of repacking into multi-line cells.
- **`max-width: 100%`** — explicit guarantee the table block itself never exceeds the viewport, regardless of how much content it contains.

---

## 2. Verification — All 6 Programmatic Checks Passed

| # | Check | Result |
|---|---|---|
| 1 | New `.matrix-table` rule with all 5 declarations present in `main.css` | ✓ lines 3096–3102: `display: block`, `overflow-x: auto`, `-webkit-overflow-scrolling: touch`, `white-space: nowrap`, `max-width: 100%` |
| 2 | Rule is inside a `@media (max-width: 768px)` block | ✓ inside the block that opens at line 3044 and closes at line 3285 |
| 3 | Rule is NOT inside the SITE NAV block | ✓ SITE NAV block opens at line 3688 (~600 lines after the rule); separation of concerns preserved |
| 4 | No other CSS modified | ✓ single targeted Edit operation; pre-existing `.torah-map-container .matrix-table` rule at line 3104 (just after the new rule) untouched |
| 5 | No templates or JS modified | ✓ |
| 6 | No HTML pages modified | ✓ |

---

## 3. Expected Behavior

### Desktop (≥768 px viewport)

**No change.** The rule is scoped to `@media (max-width: 768px)` and doesn't apply outside that breakpoint. Matrix tables continue to render as regular `<table>` elements, fitting within the content column with all columns visible at once.

### Mobile (<768 px viewport)

- Page width stays at viewport width — the hamburger ☰ button stays visible at its expected position (no longer pushed off-screen by an oversized table).
- Each `.matrix-table` becomes a scrollable region within the article. The user swipes horizontally inside the table area to see hidden columns.
- A browser-default horizontal scrollbar may appear at the bottom of the table area (varies by browser; iOS Safari hides it until scrolling starts; Chromium-on-Android shows it briefly).
- All other article content (paragraphs, headings, structure boxes, prose blocks) renders normally without horizontal overflow.

---

## 4. Pages Affected

Any page that uses `<table class="matrix-table">` automatically inherits the new mobile behavior. The class is broad: per `grep` of `main.css`, it's defined at line 693 (base styles) and referenced by scoped variants for `.genesis-map`, `.exodus-map`, `.leviticus-map`, `.numbers-map`, `.deuteronomy-map`, and `.torah-map-container`. The Map of Genesis page, all four other book maps, and the Woven Torah Method page are the obvious candidates; unit commentary pages may use it too.

Desktop appearance is unchanged on all of those pages. Worth a quick mobile spot-check on one or two beyond Woven-Torah-Method to confirm the scroll behavior reads correctly on the more elaborate scoped variants (the `.torah-map-container .matrix-table { font-size: 0.75em }` rule still applies and shrinks the cells; the new scroll rule complements it).

---

## 5. Files Touched

| File | Action |
|---|---|
| `torah-weave/Admin/Assets/CSS/main.css` | Added one 8-line rule (lines 3093–3102) inside the existing content-area `@media (max-width: 768px)` block. Net +10 lines (including comment and blank line) |
| `_pilot/matrix-table-scroll.md` | This report |

No templates, JS, individual HTML pages, or DWT files touched. Pure mobile-presentation polish.
