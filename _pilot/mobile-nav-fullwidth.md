# Mobile Nav — Force Full Viewport Width

**Date:** 2026-05-12
**File:** `torah-weave/Admin/Assets/CSS/main.css`
**Strategy:** Switch the mobile menu from `position: absolute` (which inherits any parent width constraint) to `position: fixed` with `width: 100vw`, so the menu is anchored to the viewport directly.
**Status:** CSS-only edit applied. **Not committed.**

---

## 1. The Diff Applied

In the SITE NAV block's `@media (max-width: 768px)` section, the `.nav-menu` rule (lines 3961–3975) was rewritten:

```diff
  .nav-menu {
      display: none;
-     position: absolute;
-     inset-inline-start: 0;
-     inset-inline-end: 0;
-     top: 100%;
+     position: fixed;
+     inset-inline-start: 0;
+     top: var(--site-header-height, 60px);
+     width: 100vw;
+     max-width: 100vw;
+     max-height: calc(100vh - var(--site-header-height, 60px));
+     overflow-y: auto;
      flex-direction: column;
      background: linear-gradient(135deg, #c9b899 0%, #b39f7d 100%);
      padding: 0.5rem 0;
      z-index: 999;
      box-shadow: 0 4px 8px rgba(0,0,0,0.15);
  }
```

### What each change does

- **`position: fixed`** instead of `absolute` — fixed positions relative to the viewport, not relative to any ancestor with a positioning context. Bypasses every parent's `max-width`, `padding`, `transform`, etc.
- **`width: 100vw; max-width: 100vw`** — exactly viewport width, no narrower no wider, regardless of what any parent says.
- **`top: var(--site-header-height, 60px)`** — positions the menu just below the header. The CSS variable falls back to 60 px if undefined; you can override it site-wide later with `:root { --site-header-height: ... }` once you measure the actual header height across viewports.
- **`max-height: calc(100vh - var(--site-header-height, 60px))`** + **`overflow-y: auto`** — caps the menu's height at the visible viewport minus the header, and adds an internal scrollbar if content exceeds that height. Matters most on the English nav (Insights has 10 items, which on a short phone screen would otherwise spill past the bottom of the viewport).
- **Removed `top: 100%` and `inset-inline-end: 0`** — `100vw` width plus `inset-inline-start: 0` is sufficient to place the menu correctly; the removed properties were redundant once we switched to `fixed`.

---

## 2. Verification — All 7 Programmatic Checks Passed

| # | Check | Result |
|---|---|---|
| 1 | Mobile `.nav-menu` rule uses `position: fixed` (not `absolute`) | ✓ line 3963 |
| 2 | Mobile `.nav-menu` rule has `width: 100vw` and `max-width: 100vw` | ✓ lines 3966, 3967 |
| 3 | Mobile `.nav-menu` rule has `top: var(--site-header-height, 60px)` | ✓ line 3965 |
| 4 | Mobile `.nav-menu` rule has `max-height: calc(100vh - ...)` and `overflow-y: auto` | ✓ lines 3968, 3969 |
| 5 | Desktop `.nav-menu` rule untouched | ✓ (only the rule inside `@media (max-width: 768px)` was edited) |
| 6 | No template or JS changes | ✓ |
| 7 | No other CSS changes | ✓ (single targeted Edit) |

---

## 3. Diagnosis Note

Previous mobile-spacing edits (smaller padding, full-width nav-row override) helped with internal layout, but they couldn't fix a menu being clipped by a parent's positioning context. The chain that was likely constraining the menu width on the deployed page:

- `<header class="site-header">` is `position: sticky` → creates a positioning context for absolute children.
- The `.nav-row` inside the header is the only block child of the header, and it has `max-width: 1200px; margin: 0 auto` on desktop (we already overrode this on mobile in the prior task).
- The `.nav-menu` `position: absolute` rule positioned the menu relative to its nearest positioned ancestor — depending on how the browser resolved that, the menu could end up sized against the `.nav-row` or against the `.site-header`. Either was potentially narrower than the actual viewport if anything was constraining the chain.

Switching to `position: fixed` removes the menu from that chain entirely. The menu now positions itself against the **viewport**, so `width: 100vw` is exactly the full visible screen width, no matter what any parent is doing.

If the menu's vertical position looks slightly off (because the assumed 60 px header height doesn't match reality on some viewport size), the fix is one line: set `:root { --site-header-height: Npx; }` somewhere in `main.css` with the measured value. The `var(--site-header-height, 60px)` syntax already handles the fallback.

---

## 4. Files Touched

| File | Action |
|---|---|
| `torah-weave/Admin/Assets/CSS/main.css` | One Edit: rewrote the mobile `.nav-menu` rule (lines 3961–3975). Net +3 lines |
| `_pilot/mobile-nav-fullwidth.md` | This report |

No template changes. No JS changes. The SITE NAV block's other rules (desktop hover, top-level item padding, submenu styling, hamburger toggle visibility, etc.) are all unchanged.
