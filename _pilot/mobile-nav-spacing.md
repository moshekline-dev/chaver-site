# Mobile Nav Spacing Polish

**Date:** 2026-05-12
**File:** `torah-weave/Admin/Assets/CSS/main.css`
**Strategy:** Reduce horizontal padding inside the SITE NAV block so long Hebrew labels (`PDF המשנה`, `קוד הצבעים`) fit on one line on mobile. Add safe wrap behavior in case anything still wraps.
**Status:** CSS-only edits applied. **Not committed.**

---

## 1. The 4 Specific Edits

### Edit 1 — Top-level mobile items get more horizontal room

Inside the `@media (max-width: 768px)` block, line 3987:

```diff
  .nav-menu > li > a,
  .nav-menu > li > button {
      width: 100%;
      text-align: start;
-     padding: 0.85rem 1.25rem;
+     padding: 0.85rem 0.9rem;
  }
```

Saves ~5.6 mm of side padding on a typical mobile viewport (the 0.35rem difference on each side, doubled).

### Edit 2 — Submenu items: less indent, breathing room on the trailing side, safe wrap

Inside the same `@media (max-width: 768px)` block, lines 4001–4007:

```diff
  .submenu li a {
-     padding-inline-start: 2.5rem;
+     padding-inline-start: 2rem;
+     padding-inline-end: 0.9rem;
      white-space: normal;
+     word-break: keep-all;
+     overflow-wrap: normal;
  }
```

The `word-break: keep-all` + `overflow-wrap: normal` pair ensures Hebrew (and any other) text only wraps at whitespace boundaries — never mid-word.

### Edit 3 — `.nav-row` desktop default tightens slightly

Line 3850:

```diff
  .nav-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
-     padding: 0.5rem 1rem;
+     padding: 0.5rem 0.75rem;
      max-width: 1200px;
      margin: 0 auto;
  }
```

Visually imperceptible on a 1200px-wide desktop screen; meaningful on mobile.

### Edit 4 — Mobile-specific `.nav-row` override (full-width, tight padding)

Added inside the `@media (max-width: 768px)` block, lines 4009–4013:

```css
/* Use full mobile viewport for the nav row */
.nav-row {
    max-width: none;
    padding: 0.5rem 0.75rem;
}
```

`max-width: none` cancels the 1200px constraint on small screens so the nav row uses every available pixel. The spec called this optional ("Adding this is safe regardless"); I added it as defense in case the menu's absolute positioning was getting clipped by an ancestor's stacking context. No-op if the absolute positioning was already fine; harmless either way.

---

## 2. Verification — All 8 Programmatic Checks Passed

| # | Check | Result |
|---|---|---|
| 1 | Top-level mobile items have `padding: 0.85rem 0.9rem` (not `1.25rem`) | ✓ line 3987 |
| 2 | Submenu items have `padding-inline-start: 2rem` and `padding-inline-end: 0.9rem` | ✓ lines 4002–4003 |
| 3 | Submenu items have `word-break: keep-all` and `overflow-wrap: normal` declared | ✓ lines 4005–4006 |
| 4 | `.nav-row` has `padding: 0.5rem 0.75rem` (not `1rem`) | ✓ line 3850 |
| 5 | Responsive `.nav-row` rule (per Change 3) is inside the `@media (max-width: 768px)` block | ✓ lines 4010–4012, inside the `@media (max-width: 768px) { ... }` block that closes at line 4014 |
| 6 | No other CSS modified | ✓ all edits inside the SITE NAV block; pre-existing rules outside it (matched on the same patterns at lines 1988 etc.) untouched |
| 7 | No template files modified | ✓ |
| 8 | No JS modified | ✓ |

---

## 3. What This Changes for the User

**Desktop:** essentially identical. The `.nav-row` `1rem` → `0.75rem` change is 4 px less padding on each side — invisible on a 1200 px-wide screen. Hover dropdowns work exactly as before.

**Mobile:**
- Top-level menu items have **~28% more horizontal room** (0.9rem vs. 1.25rem on each side).
- Submenu items are indented **2rem instead of 2.5rem**, with a small `0.9rem` end padding for breathing room.
- The nav row itself uses the **full mobile viewport width** (no 1200 px constraint inheriting from desktop).
- Long Hebrew labels like **PDF המשנה** and **קוד הצבעים** should now fit on one line.
- If anything still wraps (an unusually long item or a very narrow phone), it wraps at **word boundaries** — never mid-word — thanks to `word-break: keep-all` + `overflow-wrap: normal`.

---

## 4. Files Touched

| File | Action |
|---|---|
| `torah-weave/Admin/Assets/CSS/main.css` | 4 edits inside the SITE NAV block: one in the desktop default (`.nav-row` padding), three in the mobile breakpoint (top-level item padding, submenu item padding + wrap rules, new responsive `.nav-row` override). Net +6 lines |
| `_pilot/mobile-nav-spacing.md` | This report |

No template changes. No JS changes. The new nav structure from the previous task is unchanged — this is pure spacing polish.
