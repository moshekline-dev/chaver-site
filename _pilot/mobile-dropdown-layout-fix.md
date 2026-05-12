# Mobile Dropdown Layout Fix — `<details>` Inline vs. Block

**Date:** 2026-05-12
**File:** `torah-weave/Admin/Assets/CSS/main.css`
**Status:** CSS-only edit applied. **Not committed.**

---

## 1. Before / After — The Mobile Dropdown Block

Replaced the existing `MOBILE NAV DROPDOWN VISIBILITY` block with the expanded `MOBILE NAV DROPDOWN — VISIBILITY + LAYOUT` block. Two new rule groups (display/width on `<details>`; position resets on `.dropdown`) precede the existing two visibility rules.

### BEFORE (was at lines 3876–3895)

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

### AFTER (now at lines 3876–3909)

```css
/* ====================================
   MOBILE NAV DROPDOWN — VISIBILITY + LAYOUT
   On mobile, fix two things:
   1. Make <details> display: block (it's display: inline on desktop,
      which causes block-level children to render off-screen on mobile
      where .dropdown is position: static).
   2. Tie .dropdown visibility to the parent <details>[open] attribute.
   ==================================== */

@media (max-width: 768px) {
    /* Make <details> block-level so children flow correctly */
    .has-dropdown details {
        display: block;
        width: 100%;
    }

    /* Ensure the dropdown fills the menu width on mobile */
    .has-dropdown .dropdown {
        width: 100%;
        left: auto;
        right: auto;
        top: auto;
    }

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

The two existing visibility rules are byte-identical to before. The two new rule groups are additive.

---

## 2. Verification — All 5 Checks Passed

| # | Check | Result |
|---|---|---|
| 1 | Single mobile dropdown block (no duplicates) | ✓ — one `MOBILE NAV DROPDOWN — VISIBILITY + LAYOUT` block at line 3877; the old `MOBILE NAV DROPDOWN VISIBILITY` header is fully replaced, not duplicated |
| 2 | All 4 rule groups present in the block | ✓ — `.has-dropdown details {block, 100%}` (3887); `.has-dropdown .dropdown {100%, auto auto auto}` (3893); `details:not([open]) .dropdown {display: none}` (3901); `details[open] .dropdown {display: flex}` (3906) |
| 3 | Position: after `@media (hover: hover)` block, before `END OF MAIN.CSS` banner | ✓ — hover block ends line 3874, mobile block runs 3876–3909, END banner starts 3911 |
| 4 | `@media (hover: hover) and (pointer: fine)` block unchanged | ✓ — lines 3838–3869 untouched (I only edited inside the mobile block) |
| 5 | No other lines in `main.css` modified | ✓ — single targeted `Edit` operation |

---

## 3. What the Fix Does

The desktop CSS in each template's inline `<style>` block contains:

```css
.has-dropdown details {
    display: inline;
}
```

That's correct for desktop where `.dropdown` is `position: absolute` — the absolute-positioned dropdown floats outside the normal flow regardless of its parent's display mode. But on mobile, the existing earlier mobile block in `main.css` resets `.dropdown` to `position: static`. A `static` flex container *inside an inline parent* enters a context where block-level layout doesn't reliably work: browsers either shrink the dropdown to zero width, render it inline-adjacent to the summary, or position it outside the viewport. The exact behavior varies by mobile engine, which is why this only showed up on mobile.

The fix:

- **`.has-dropdown details { display: block; width: 100% }`** — turn `<details>` into a proper block-level container on mobile so block-level children behave normally.
- **`.has-dropdown .dropdown { width: 100%; left: auto; right: auto; top: auto }`** — explicit `width: 100%` ensures the dropdown stretches across the full menu width instead of shrinking; the `auto` resets to `left/right/top` clear out any residual absolute-position offsets that might still be in the cascade even though `position: static` ignores them.

The two visibility rules (`:not([open]) → display: none`, `[open] → display: flex`) are unchanged — they still control show/hide. The new rules only fix the layout context in which "show" happens.

---

## 4. Compatibility Check (No Regressions Expected)

- **Desktop** is untouched because the new block is wrapped in `@media (max-width: 768px)`. On a desktop viewport the rules don't apply; `<details>` stays `display: inline` and `.dropdown` stays `position: absolute`, exactly as before. Hover-to-open still works via the separate `@media (hover: hover) and (pointer: fine)` block at lines 3845–3869.
- **Mobile** gets the new `display: block` on `<details>` plus the layout-reset rules on `.dropdown`. The explicit click handler in the templates sets the `[open]` attribute on tap → the visibility rule shows the dropdown as a full-width `display: flex` block stacked below the summary. No off-screen rendering.

---

## 5. If This Still Doesn't Work

The task spec notes: *"If after this fix mobile dropdowns STILL don't work, the next step is to use the browser's mobile developer tools (or remote inspection) to look at the actual rendered DOM and CSS."*

If that comes up, the most useful evidence is a Chrome DevTools snapshot of the rendered `<details class="has-dropdown" open>` element on a mobile viewport: the computed styles panel for both the `<details>` and the `.dropdown` child, plus the box-model dimensions. That would tell us whether (a) the `[open]` attribute is actually being set by the click handler (i.e., the JS works), (b) the CSS we added is being applied (cascade resolution), and (c) where the dropdown is being placed in the viewport. We've been guessing at the layout context until now; one DevTools screenshot would replace that guessing with ground truth.

---

## 6. Files Touched

| File | Action |
|---|---|
| `torah-weave/Admin/Assets/CSS/main.css` | Mobile dropdown block expanded (lines 3876–3909 — was 3876–3895). Net +14 lines. |
| `_pilot/mobile-dropdown-layout-fix.md` | This report |

No template changes. No JavaScript changes. No preview regeneration needed — the preview links to `main.css` via absolute URL and picks up the new rules automatically at narrow viewport widths.
