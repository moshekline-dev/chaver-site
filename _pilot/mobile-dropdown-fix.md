# Mobile Dropdown Fix — Tie `.dropdown` Visibility to `<details>[open]`

**Date:** 2026-05-12
**Status:** CSS-only fix added to `main.css`. No template changes. Preview reuses the same `main.css` link and needs no edit. **Not committed.**

---

## 1. The CSS Block Added

Inserted into `torah-weave/Admin/Assets/CSS/main.css` at **lines 3876–3895**, between the existing hover-behavior block (ends line 3874) and the `END OF MAIN.CSS` banner (starts line 3897).

```css
/* ====================================
   MOBILE NAV DROPDOWN VISIBILITY
   On mobile, explicitly tie .dropdown visibility to the
   parent <details> [open] attribute. The inline CSS sets
   .dropdown { display: flex } which overrides the native
   <details> hide-when-closed behavior on some mobile
   browsers. This block restores correct mobile behavior.
   ==================================== */

@media (max-width: 768px) {
    /* Hide dropdown items when parent <details> is closed */
    .has-dropdown details:not([open]) .dropdown {
        display: none;
    }

    /* Show dropdown items when parent <details> is open */
    .has-dropdown details[open] .dropdown {
        display: flex;
    }
}
```

(Verified via Read tool. Line numbers above are accurate as of this commit.)

---

## 2. Diagnosis Recap

The inline `<style>` block in `_templates/Academic-Content-EN.html` and `_templates/Academic-Content-HE.html` sets:

```css
.dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    display: flex;
    flex-direction: column;
    ...
}
```

That `display: flex` is unconditional. On desktop, the prior task's `@media (hover: hover) and (pointer: fine)` block explicitly toggles `display: none` / `display: block` based on `:hover` state, so the dropdown shows/hides correctly regardless of whether the underlying `<details>` element is "open".

On mobile, there is no hover. The dropdown's visibility is supposed to depend on the native `<details>` element's behavior — closed `<details>` hides its non-`<summary>` children. But when CSS explicitly sets `display: flex` on those children, **some mobile browsers (older Chromium-on-Android, some Safari versions) treat the explicit `display` as overriding the native hide-when-closed behavior**, leaving the dropdown items permanently visible (or in some cases permanently invisible).

The fix is to **explicitly couple the dropdown's display to the parent `<details>[open]` attribute** on mobile. When the parent's `<summary>` is tapped, the browser flips the `[open]` attribute, and the new rules pick up the change:

- `<details>` closed → `:not([open])` selector matches → `display: none` wins (specificity 0,3,1 vs. inline's 0,1,0)
- `<details>` open → `[open]` selector matches → `display: flex` wins, dropdown renders

The native `<details>` toggle is doing the work; the new CSS just makes the visual response unambiguous.

---

## 3. Specificity Check

| Selector | Specificity |
|---|---:|
| Inline `.dropdown { display: flex }` | 0,1,0 = 10 |
| New `.has-dropdown details:not([open]) .dropdown` | 0,3,1 = 31 |
| New `.has-dropdown details[open] .dropdown` | 0,3,1 = 31 |

The new rules win the cascade on mobile (where they apply via `@media (max-width: 768px)`).

---

## 4. Desktop / Mobile Mode Separation

| Viewport | Active block | Behavior |
|---|---|---|
| `@media (hover: hover) and (pointer: fine)` — pointer-capable desktop | Existing hover block (lines 3845–3869) | Hover-to-open; ignores `<details>[open]` state |
| `@media (hover: none)` — touch | (empty placeholder block — comment only) | Native `<details>` click behavior |
| `@media (max-width: 768px)` — narrow viewport (mobile/tablet) | **New** block (lines 3885–3895) | Visibility tied to `<details>[open]` attribute |

The `(hover: hover)` and `(max-width: 768px)` selectors are independent dimensions — a narrow viewport with a precise pointer (a small laptop) matches both, and that's intentional: the hover behavior still wins where applicable, and the open-attribute coupling provides a correct fallback if the user happens to tap. On a phone (touch + narrow), only the new block applies, which is exactly the case we're fixing.

---

## 5. Programmatic Checks — All Passed

| Check | Result |
|---|---|
| New `MOBILE NAV DROPDOWN VISIBILITY` block present once | ✓ (line 3877) |
| New block contains `display: none` for `:not([open]) .dropdown` | ✓ (line 3888) |
| New block contains `display: flex` for `[open] .dropdown` | ✓ (line 3893) |
| Position: after `@media (hover: none)` block (line 3871), before `END OF MAIN.CSS` (line 3897) | ✓ |
| Hover block (`@media (hover: hover) and (pointer: fine)`) unchanged | ✓ (lines 3845–3869 untouched) |
| No other lines in `main.css` modified | ✓ |

Note: there are two other `@media (max-width: 768px)` blocks earlier in `main.css` (line 3193 — general mobile nav layout, and line 3486 — portrait-orientation tweaks). The new block is a third mobile block; the rules don't overlap or conflict because each addresses different selectors. Browsers will merge them into a single matched rule set at the correct viewport width.

---

## 6. Preview

The existing `_pilot/hebrew-nav-render-preview.html` already links to `/torah-weave/Admin/Assets/CSS/main.css` via absolute URL — when the preview is served and viewed at narrow viewport width, the new rules apply automatically. No edit to the preview HTML was needed; this task was CSS-only and the preview was last regenerated at the end of the prior (template rebuild) task.

---

## 7. Manual Verification Steps for Moshe

Once the change is committed and deployed (or served from a local web server):

**Desktop regression check (must still work):**

- Hovering over **תורה** in the nav opens the dropdown ✓
- Moving the mouse away closes it ✓
- Hovering over **משנה** closes תורה and opens משנה (the close-others handler from the prior task) ✓

**Mobile fix verification:**

1. Narrow the browser window to under 768 px wide, or open on a phone.
2. Tap the hamburger icon — the 6-item nav drops down.
3. Tap **תורה** in the nav. The 3 dropdown items (שער התורה, מפת התורה, קוד הצבעים) appear, indented below.
4. Tap **תורה** again. The dropdown collapses.
5. With תורה open, tap **משנה**. The close-others handler closes תורה; the 4 משנה items appear.
6. Same for **נתונים** (2 items).

If anything misbehaves, the most likely culprit is browser-specific `<details>` quirks rather than the CSS — the rules are standard and well-supported in current browsers (caniuse: `details/summary` 97%+ support; `:not()` and attribute selectors 98%+).

---

## 8. Files Touched

| File | Action |
|---|---|
| `torah-weave/Admin/Assets/CSS/main.css` | Added one new block (lines 3876–3895), 20 lines including comment + `@media` wrapper + two rules |
| `_pilot/mobile-dropdown-fix.md` | This report |

No template files were modified. No JavaScript changes. CSS-only fix.
