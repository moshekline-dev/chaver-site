# Force `<details>` Open on Mobile

**Date:** 2026-05-12
**Strategy:** Bypass native `<details>` hide-when-closed behavior on mobile by programmatically forcing every nav `<details>` to `open = true` at page load. Combined with the existing `pointer-events: none` on `<summary>`, the details can never be closed by user interaction on mobile, so their children stay visible.
**Status:** JS appended to both templates + preview. **Not committed.**

---

## 1. The New JavaScript Block

Appended to the existing `<script>` block in both `_templates/Academic-Content-EN.html` and `_templates/Academic-Content-HE.html`, after the explicit click handler.

```javascript
// On mobile, force all <details> elements always open.
// The flat-list CSS makes them visually inert (no chevron, no tap behavior),
// but native <details> hides non-summary children when closed regardless of
// CSS. Setting open=true bypasses that hide-when-closed behavior.
function forceDetailsOpenOnMobile() {
    if (window.matchMedia('(max-width: 768px)').matches) {
        document.querySelectorAll('.has-dropdown details').forEach(function(d) {
            d.open = true;
        });
    } else {
        // On desktop, restore default (closed) state so hover CSS can control visibility
        document.querySelectorAll('.has-dropdown details').forEach(function(d) {
            d.open = false;
        });
    }
}

// Run on initial load
document.addEventListener('DOMContentLoaded', forceDetailsOpenOnMobile);

// Re-run if viewport changes (e.g., rotation, browser resize crossing 768px)
window.addEventListener('resize', forceDetailsOpenOnMobile);
```

**Behavior on viewport changes** — the resize listener handles three scenarios cleanly: portrait↔landscape rotation on a tablet that crosses the 768 px threshold, browser window resizing on desktop into a mobile-width state for testing, and DevTools device-emulation toggles. Each transition re-runs the function, so the `[open]` state always matches whichever stylesheet branch is active.

---

## 2. Root-Cause Diagnosis Recap

The prior tasks established:

- **CSS-only attempts** (mobile `[open]` selectors, `display: block` on `<details>`, `!important` on layout rules) couldn't fix the mobile nav alone because native `<details>` hides non-summary children whenever the `open` attribute is absent — a *user-agent shadow tree* behavior that CSS `display: flex` (even with `!important`) doesn't override.
- **JS-only attempts** (close-others on `toggle` event, then explicit click handler) didn't help on mobile because `pointer-events: none` (added in the flat-list task) deliberately blocks the click event from reaching summary, so the click handler never fires there.

The clean fix combines both worlds: **the flat-list CSS keeps the dropdown visually inert and bypasses the layout-context problem, and this small JS makes sure the native shadow-tree hiding is also bypassed.**

In incognito with fresh cache, the user observed the chevron correctly gone (CSS working) but the dropdown items still hidden — which is exactly the native shadow-tree behavior that CSS cannot reach. Forcing `open = true` resolves it.

---

## 3. Verification — All 5 Programmatic Checks Passed

| # | Check | EN template | HE template |
|---|---|---|---|
| 1 | New `forceDetailsOpenOnMobile` function present | ✓ line 455 | ✓ line 452 |
| 2 | `DOMContentLoaded` listener for the new function added | ✓ line 469 | ✓ line 466 |
| 3 | `window.addEventListener('resize', ...)` added | ✓ line 472 | ✓ line 469 |
| 4 | Existing `toggleMenu()`, click-outside, explicit click handler unchanged | ✓ (lines 414, 419, 433 intact) | ✓ (lines 411, 416, 430 intact) |
| 5 | Clean tail (`</script>` → `{{ region: page-scripts }}` → `</body>` → `</html>`) | ✓ closing tags at 476/477 | ✓ closing tags at 473/474 |

The preview file `_pilot/hebrew-nav-render-preview.html` was also updated with the same JS block for consistency (`forceDetailsOpenOnMobile` at line 456; resize listener at line 473; closing tags at 477/478).

---

## 4. Why Desktop Behavior Is Unchanged

Three layers cooperate to keep desktop working exactly as before:

1. **Hover CSS** in the `@media (hover: hover) and (pointer: fine)` block doesn't depend on the `[open]` attribute — it uses `:hover` selectors. Hovering over a `.has-dropdown` element with `<details>` closed still shows the dropdown via `display: block` on `:hover`.

2. **`forceDetailsOpenOnMobile()` on desktop** explicitly sets every `<details>.open = false` (the `else` branch). This means hover CSS controls visibility entirely; the `[open]` attribute is dormant and predictable.

3. **The explicit click handler** still works on desktop: when a user clicks a summary, `pointer-events` defaults to `auto` on desktop (no `@media (max-width: 768px)` rules apply), so the click event reaches the handler. The handler toggles `[open]` exactly as it did before.

No conflict: hover CSS doesn't read `[open]`, click handler manages `[open]` on demand, and the new function only enforces "all closed" on desktop initial-state plus "all open" on mobile.

---

## 5. Mobile Behavior After Deploy

The expected final flow on a mobile viewport:

1. Page loads → `DOMContentLoaded` fires → `forceDetailsOpenOnMobile()` runs → every `.has-dropdown details` gets `open = true`.
2. Native shadow-tree hiding is bypassed → all dropdown `<ul>` content is renderable.
3. The flat-list CSS (`@media (max-width: 768px)` with `!important` flags) styles the rendered content: `<details>` collapses to `display: contents`, `<summary>` is non-tappable, the dropdown `<ul>` is full-width and always shown as `display: flex` column.
4. User taps hamburger → `toggleMenu()` adds `.show` to the menu → the entire flat list is visible.
5. User taps any link in the flat list → navigates normally.
6. If the user rotates the device or resizes such that the viewport crosses 768 px, the resize listener re-runs the function and flips every `<details>` to `false` (entering desktop mode) or `true` (entering mobile mode). The CSS picks up the matching breakpoint at the same time, so layout and `[open]` state stay in sync.

---

## 6. Edge Cases Worth Knowing

- **`MediaQueryList.matches`** is well-supported (every browser since IE 10). Safe to use without polyfill.
- **`d.open = true`** vs. `setAttribute('open', '')`: both work in modern browsers and trigger the same internal state flip. Using the property is slightly faster and more idiomatic.
- **Resize listener firing rate**: the function is cheap (a few querySelectorAll + boolean property writes), so debouncing isn't necessary even when resize fires many times per second during a drag.
- **Print stylesheets**: `@media print` is unaffected because `window.matchMedia('(max-width: 768px)')` checks the actual viewport, not the print media. Printing on desktop while the JS is in the closed state is fine.

---

## 7. Files Touched

| File | Action |
|---|---|
| `_templates/Academic-Content-EN.html` | Appended `forceDetailsOpenOnMobile` function + 2 event listeners (lines 455–472) after the existing explicit click handler |
| `_templates/Academic-Content-HE.html` | Same addition (lines 452–469) |
| `_pilot/hebrew-nav-render-preview.html` | Same addition for consistency (lines 456–473) |
| `_pilot/force-details-open-mobile.md` | This report |

No CSS changes. No HTML structure changes. No DWT changes.
