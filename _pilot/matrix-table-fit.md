# Matrix Table — Shrink-to-Fit on Mobile (Replaces Earlier Scroll Approach)

**Date:** 2026-05-13
**File:** `torah-weave/Admin/Assets/CSS/main.css`
**Strategy:** Keep `<table class="matrix-table">` as a real table (display: table) on mobile; just shrink its text and cell padding so the whole table fits within the viewport.
**Status:** Old rule replaced. **Not committed.**

---

## 1. Diff — What Was Removed, What Was Added

The previous rule (from the immediately prior task) was breaking the table layout: `display: block` removed the table's automatic column alignment, `overflow-x: auto` + `white-space: nowrap` tried to make a scrollable region but in practice the cells collapsed and the whole map area appeared blank on mobile.

### Removed

```css
@media (max-width: 768px) {
    .matrix-table {
        display: block;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        white-space: nowrap;
        max-width: 100%;
    }
    ...
}
```

### Added (in the same `@media (max-width: 768px)` block, same location)

```css
@media (max-width: 768px) {
    /* Wide matrix tables: shrink down via font-size + tight cell padding so
       the whole table fits within the viewport.
       Tables retain their normal display: table layout so rows align correctly. */
    .matrix-table {
        font-size: 0.65em;
        line-height: 1.2;
    }

    .matrix-table th,
    .matrix-table td {
        padding: 3px 2px !important;
        word-break: break-word;
    }

    .matrix-table thead th small,
    .matrix-table .cell-label,
    .matrix-table td small {
        font-size: 0.85em;
    }
    ...
}
```

The pre-existing `.torah-map-container .matrix-table { font-size: 0.75em }` rule that sits directly after the new block is unchanged — it'll cascade on top of the new general 0.65em for torah-map containers specifically, slightly increasing readability where the layout has more breathing room.

### What each declaration does

- **`font-size: 0.65em`** — shrinks the table content to ~65% of normal text size, so 8 columns fit within typical mobile widths (~380–430 px usable).
- **`line-height: 1.2`** — tightens line height so multi-line cells don't bloat vertically.
- **`padding: 3px 2px !important`** — replaces the desktop default of `12px` cell padding (set in the base `.matrix-table th, .matrix-table td` rule at line ~701 of main.css). `!important` is required because the base rule is equal-specificity and the cascade alone wouldn't beat it cleanly on every browser.
- **`word-break: break-word`** — character-level wrap if a long label (e.g., "Abr. Cov.", unit links) would otherwise force a single cell to push the table wider than viewport.
- **`font-size: 0.85em`** on `small`, `.cell-label`, `td small` — chevron labels and small annotations stay proportionally smaller than the main cell text within the already-shrunk table.

---

## 2. Verification — All 6 Programmatic Checks Passed

| # | Check | Result |
|---|---|---|
| 1 | Old mobile rule (`display: block; overflow-x: auto; white-space: nowrap; max-width: 100%`) for `.matrix-table` is gone | ✓ — confirmed via Grep on the file region around line 3093; the rule was replaced wholesale |
| 2 | New `.matrix-table { font-size: 0.65em; line-height: 1.2 }` rule present inside `@media (max-width: 768px)` | ✓ lines 3096–3099, inside the existing content-area mobile block (3044–3286) |
| 3 | New `.matrix-table th, .matrix-table td { padding: 3px 2px !important; word-break: break-word }` rule present in same `@media` | ✓ lines 3101–3105 |
| 4 | Desktop `.matrix-table` base rules (default font-size, 12px padding at line ~701) unchanged | ✓ — base rule outside any media query, untouched |
| 5 | No other CSS modified | ✓ — single targeted Edit operation; pre-existing `.torah-map-container .matrix-table { font-size: 0.75em }` at line 3113 intact |
| 6 | No templates, JS, or HTML pages modified | ✓ |

---

## 3. Expected Behavior

### Desktop (≥768 px viewport)

**Zero change.** The new rules are scoped to `@media (max-width: 768px)`; they don't apply outside that breakpoint. Matrix tables render with their normal font-size (inherited from the page) and 12px cell padding, exactly as before.

### Mobile (<768 px viewport)

- Matrix table renders as a real table — `display: table` (the default), rows aligned, sticky thead works if defined.
- Text is roughly 65% of normal size — small but readable; tight cell padding (3 px vertical, 2 px horizontal) maximizes column fit.
- All 8 columns visible at once — no horizontal scroll, no whitespace gap where the table should be.
- The hamburger ☰ button stays visible at the top-right; the page width matches the viewport.
- Long cell labels (e.g., "Abr. Cov.", unit links) wrap mid-word if necessary rather than forcing the table wider.

### Other pages with `.matrix-table`

All pages using `<table class="matrix-table">` (Genesis/Exodus/Leviticus/Numbers/Deuteronomy maps, the Torah Map container, the Woven Torah Method page, and any unit commentary pages) inherit the same mobile shrink-to-fit behavior. Desktop appearance is unchanged on all of them.

The `.torah-map-container .matrix-table { font-size: 0.75em }` rule cascades on top of the new `0.65em` general rule for that specific scoped variant — within a torah-map container, the table will be slightly less aggressive in its shrink (0.75 instead of 0.65), since those pages already have a more focused layout with less competing content.

### If 0.65em is too small to read

The number is a trade-off between readability and column fit. If real-phone testing shows it's too small, increase to `0.7em` or `0.75em` and see if the 8 columns still fit. Reducing further (to `0.6em`) is also possible if extra room is needed for very long labels — but readability suffers below ~`0.6em`.

---

## 4. Why the Previous Approach Failed

For the record, in case a similar fix is attempted in the future:

| Previous declaration | What went wrong |
|---|---|
| `display: block` | Removed the table's automatic column alignment. Cells stopped sharing column widths across rows — each row's cells laid out independently, producing a broken visual structure. |
| `overflow-x: auto` | Was supposed to create a scroll region within the (now block) table. But because the inner `<tr>` and `<td>` elements still had table-display semantics inherited from defaults, the layout couldn't actually overflow horizontally — it just collapsed. |
| `white-space: nowrap` | Worked as intended, but on a `display: block` table with broken layout, it forced cells to grow rather than wrap, exacerbating the collapse. |
| `max-width: 100%` | No effect once `display: block` had already broken the table. |

The fundamental issue: `<table>` rendering depends on `display: table`, `display: table-row`, `display: table-cell`. Setting `display: block` on the parent breaks the whole layout chain because the children still expect their parent to be a table. To make this work, you'd also need `display: block` (or `display: flex`/`grid`) on every `<tr>`/`<td>`, which would require redesigning the layout from scratch.

The new approach is much simpler: keep the table as a table, just make everything inside it smaller.

---

## 5. Files Touched

| File | Action |
|---|---|
| `torah-weave/Admin/Assets/CSS/main.css` | Replaced one rule (5 declarations) with three rules (8 declarations) inside the existing content-area `@media (max-width: 768px)` block. Net +9 lines |
| `_pilot/matrix-table-fit.md` | This report |

No template changes. No JS changes. No HTML page changes. No DWT changes.
