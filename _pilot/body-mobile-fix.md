# Body Width Constraint Fix + Stale Nav Rule Cleanup

**Date:** 2026-05-12
**File:** `torah-weave/Admin/Assets/CSS/main.css`
**Strategy:** Override the body's `max-width: 1200px; padding: 40px 20px` on mobile so the new full-width nav menu actually gets the full viewport. Also remove the stale `.main-nav` / `.menu-toggle` rules that the previous nav-replacement cleanup missed.
**Status:** Applied. **Not committed.**

---

## 1. Stale `.main-nav` and `.menu-toggle` Rules Removed

### Before / after counts

| Selector substring | Lines matching BEFORE | Lines matching AFTER |
|---|---:|---:|
| `.main-nav` | 9 | **0** |
| `.menu-toggle` | 6 | **0** |

### Rules deleted from desktop area (lines 207–275 before)

Six rules removed wholesale:
- `.main-nav { max-width: 1200px; margin: 0 auto; padding: 0.75rem 20px; position: relative; min-height: 44px }`
- `.menu-toggle { display: none; ... width: 28px; height: 24px; ... }`
- `.menu-toggle::before { content: ''; ... box-shadow: 0 8px 0 #3d2f1f, 0 16px 0 #3d2f1f }`
- `header.site-header nav ul, .main-nav > ul { list-style: none; display: flex; ... gap: 2.5rem }`
- `header.site-header nav a, .main-nav a { color: #3d2f1f; font-weight: 500; ... }`
- `header.site-header nav a:hover, .main-nav a:hover { color: #8b4513; background-color: rgba(...) }`

The `header.site-header nav ...` halves of those comma lists were also dead (the new header has no `<nav>` element, just `<div class="nav-row">`), so deleting the whole rule was correct.

### Rules deleted from `@media (max-width: 1024px)` block

Seven more rules removed wholesale:
- `.main-nav { padding: 0; min-height: auto }`
- `.menu-toggle { display: block !important; ... width: 44px; height: 40px }` (the 44px hamburger)
- `.menu-toggle::before { top: 10px; left: 8px }`
- `header.site-header nav ul, .main-nav > ul { ... position: fixed !important; ... width: 200px; ... }` — **this was the 200 px hardcoded width** the task description called out
- `header.site-header nav ul.show, .main-nav > ul.show, #nav-menu.show { visibility: visible !important; ... }`
- `header.site-header nav ul li, .main-nav > ul li { display: block !important; width: 100% }`
- `header.site-header nav a, .main-nav a { display: block; padding: 1rem; ... }`
- `header.site-header nav ul li:last-child a, .main-nav > ul li:last-child a { border-bottom: none }`

(The `#nav-menu` selector in that `.show` rule is also obsolete — the new menu uses `id="primary-menu"`.)

### Surgical edit in the print rule

```diff
      .mobile-notice,
-     .menu-toggle,
      .hero,
```

The print rule's other entries (`.unit-navigation`, `.hero`, `.back-to-top`, etc.) were preserved.

### What was left untouched

The `@media (max-width: 1024px)` block still contains a `header.site-header { background: transparent !important; position: fixed !important; top: 10px; right: 10px; width: auto; ... }` override (lines ~3025–3036 after this commit). That rule is **also stale** — it was paired with the old floating-hamburger nav design and turns the header into a small corner widget on tablet/mobile. **It will fight the new full-width sticky header on devices between 769 px and 1024 px wide** (tablets in portrait, narrow laptops in window-resize tests).

Per the spec's explicit scope ("delete every rule whose selector contains `.main-nav` or `.menu-toggle`"), I didn't touch this — its selector is `header.site-header`, not `.main-nav` or `.menu-toggle`. **Flagging for a follow-up cleanup task.** Recommended fix: delete that `header.site-header { ... }` override inside the 1024 px block, since the new SITE NAV uses a single mobile breakpoint at 768 px and the base desktop `header.site-header { position: sticky; top: 0 }` rule is what should win at tablet widths.

---

## 2. Mobile Body Override Added

Inside the SITE NAV block's `@media (max-width: 768px)` section, at the top (before `.nav-toggle`):

```css
@media (max-width: 768px) {
    /* On mobile, let body be full-width so the nav menu can span viewport.
       Desktop body keeps its 1200px centering rule (defined elsewhere). */
    body {
        max-width: none;
        padding-left: 0;
        padding-right: 0;
    }

    .nav-toggle {
        display: block;
    }
    ...
}
```

`overflow-x: hidden` on the desktop body rule (line 55) is preserved — not overridden — so horizontal scroll is still prevented if anything accidentally extends past the viewport.

### Desktop body rule (UNCHANGED)

```css
body {
    font-family: 'Palatino Linotype', 'Book Antiqua', Palatino, Georgia, serif;
    line-height: 1.8;
    color: #2c3e50;
    background-color: #fdfcf8;
    max-width: 1200px;          /* still here on desktop */
    margin: 0 auto;             /* still here */
    padding: 40px 20px;         /* still here */
    overflow-x: hidden;         /* still here */
}
```

Lines 47–56 of `main.css`. Untouched by this commit.

---

## 3. Verification — All 7 Programmatic Checks Passed

| # | Check | Result |
|---|---|---|
| 1 | `grep -c "\.main-nav" main.css` → 0 | ✓ Grep returned "No matches found" |
| 2 | `grep -c "\.menu-toggle" main.css` → 0 | ✓ Grep returned "No matches found" |
| 3 | Mobile `@media (max-width: 768px)` block contains `body { max-width: none; padding-left: 0; padding-right: 0; }` | ✓ lines 3810–3812 (inside the SITE NAV mobile block at line 3806) |
| 4 | Desktop body rule (`max-width: 1200px`, `padding: 40px 20px`) UNCHANGED | ✓ lines 47–56 untouched |
| 5 | Mobile `.nav-menu` rule still has `position: fixed` and `width: 100vw` | ✓ lines 3821 (`position: fixed`) and 3824 (`width: 100vw`) |
| 6 | No template files or JS modified | ✓ (only `main.css` edited) |
| 7 | No other CSS changes outside the listed edits | ✓ (three Edit operations all targeted the documented rules) |

---

## 4. Note on Mobile Body Content

Now that `body { padding-left: 0; padding-right: 0 }` on mobile, page content inside the body (article paragraphs, scripture tables, etc.) goes edge-to-edge unless an inner wrapper provides its own side padding. The site already has `main.content-wrapper { padding: 30px 15px }` (line ~3060 in the existing mobile @media block) and `.content-wrapper { padding: 40px 20px }` at desktop scale, so content should still have reasonable margins. If any specific page looks bad edge-to-edge after deploy, the fix is targeted — add side padding to that page's content wrapper, don't restore body padding.

---

## 5. Expected Behavior After Deploy

**Desktop (≥1025 px):** completely unchanged. Body is still the centered 1200 px column with 40/20 px padding. New nav still has the same look.

**Tablet (769–1024 px):** the `@media (max-width: 1024px)` block still has the **header.site-header override** I flagged in Section 1, so the header will misbehave at these widths until that override is removed. The mobile body fix doesn't reach this range — it's gated on `max-width: 768px`. Recommend deferring deploy testing on tablet widths until the follow-up cleanup.

**Mobile (≤768 px):**
- Body gets `max-width: none; padding-left: 0; padding-right: 0` — content uses the full viewport width.
- Header stretches edge-to-edge (sticky, gradient background).
- Hamburger menu opens `position: fixed; width: 100vw` — exactly the visible screen width.
- All nav items have full horizontal room; long Hebrew labels fit on one line.

---

## 6. Files Touched

| File | Action |
|---|---|
| `torah-weave/Admin/Assets/CSS/main.css` | Three Edits: delete 6 desktop nav rules (~70 lines), delete 8 mobile-1024px-block nav rules (~80 lines), remove 1 print-rule entry, add 1 new mobile body override (5 lines). Net −145 lines |
| `_pilot/body-mobile-fix.md` | This report |

No template changes. No JS changes. No DWT changes.

---

## 7. Recommended Follow-Up

A small follow-up task should delete the `header.site-header { ... }` override at the top of the `@media (max-width: 1024px)` block — it makes the header `position: fixed` in the top-right corner with `width: auto`, which was correct for the old floating-hamburger nav design and is wrong for the new full-width sticky bar. Without that follow-up, tablet-width viewports (769–1024 px) will render the header in the corner instead of across the top.
