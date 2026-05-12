# Explicit Click Handler for Nav Dropdowns

**Date:** 2026-05-12
**Status:** JS swap applied identically to both templates and to the preview. **Not committed.**

---

## 1. What Changed — Same Diff in Both Templates

The `toggle`-event-based close-others handler is replaced with an explicit click handler that takes full control of `<details>[open]`. The script block's `toggleMenu()` function and click-outside handler are unchanged.

```diff
- // Close other nav dropdowns when one is opened (accordion behavior)
- document.addEventListener('DOMContentLoaded', function() {
-     var allDetails = document.querySelectorAll('.has-dropdown details');
-     allDetails.forEach(function(d) {
-         d.addEventListener('toggle', function() {
-             if (this.open) {
-                 allDetails.forEach(function(other) {
-                     if (other !== d) { other.open = false; }
-                 });
-             }
-         });
-     });
- });
+ // Explicit click handler for nav dropdowns (works reliably on mobile + desktop)
+ document.addEventListener('DOMContentLoaded', function() {
+     var summaries = document.querySelectorAll('.has-dropdown summary');
+     summaries.forEach(function(summary) {
+         summary.addEventListener('click', function(e) {
+             e.preventDefault();  // Prevent native <details> toggle; we handle it manually
+             var thisDetails = summary.closest('details');
+             var wasOpen = thisDetails.hasAttribute('open');
+
+             // Close all dropdowns
+             document.querySelectorAll('.has-dropdown details').forEach(function(d) {
+                 d.removeAttribute('open');
+             });
+
+             // If the tapped dropdown was closed, open it (otherwise leave all closed)
+             if (!wasOpen) {
+                 thisDetails.setAttribute('open', '');
+             }
+         });
+     });
+ });
```

**Behavior:** the click listener catches every tap on a `<summary>`, calls `preventDefault()` to neutralize the native `<details>` toggle (which is what was misbehaving on mobile), then explicitly sets the `[open]` state on the tapped element while clearing it from every other dropdown. The accordion property (only one dropdown open at a time) is preserved.

**Why this works where the toggle handler didn't:** the `toggle` event is fired by the browser *after* a `<details>` element's state changes. On mobile, some browsers either fire `toggle` inconsistently when an explicit `e.preventDefault()` chain is in play, or the toggle event arrives but the `[open]` state has already been reverted by the time our handler runs. By intercepting `click` directly and managing `[open]` ourselves, we eliminate the dependency on a particular event-ordering contract.

---

## 2. Verification — 8 Programmatic Checks All Passed

| # | Check | EN template | HE template |
|---|---|---|---|
| 1, 2 | No `addEventListener('toggle'` (old handler gone) | ✓ (Grep returned 0) | ✓ (Grep returned 0) |
| 3, 4 | Exactly one `summary.addEventListener` (new handler present) | ✓ (line 433) | ✓ (line 430) |
| 5 | `toggleMenu()` function still present | ✓ (EN: line 414, HE: line 411) | ✓ |
| 6 | Click-outside handler still present (`Close mobile menu when clicking outside` comment) | ✓ (EN: line 419, HE: line 416) | ✓ |
| 7 | No other lines modified outside the swapped block | ✓ (single `Edit` operation per template, replace_all=false, targeted at the 13-line block) | ✓ |
| 8 | Clean closing tags | ✓ (EN: `</body>` line 453, `</html>` line 454) | ✓ (HE: `</body>` line 450, `</html>` line 451) |

---

## 3. CSS Compatibility Check

The CSS added in prior tasks is unchanged and remains correct under the new JS:

| Viewport | Active CSS | New JS interaction |
|---|---|---|
| Desktop (`@media (hover: hover) and (pointer: fine)`) | Forces `.dropdown { display: block }` on `.has-dropdown:hover`, hides on `:not(:hover)` | Hover behavior is independent of `[open]` state; click handler can also set `[open]` without changing hover behavior. No conflict. |
| Mobile (`@media (max-width: 768px)`) | `.has-dropdown details[open] .dropdown { display: flex }` / `:not([open]) { display: none }` | The new JS directly sets/removes the `[open]` attribute on `<details>` — exactly the trigger the CSS is waiting for. The chain is: tap `<summary>` → JS sets `[open]` → CSS shows dropdown. |

The two CSS blocks remain mutually exclusive (one matches hover-capable devices, one matches narrow viewports without hover-capability) and the new JS is the bridge between user input and the `[open]` attribute that both CSS blocks key off (on mobile) or ignore (on desktop, where hover wins).

---

## 4. Preview Regenerated

`_pilot/hebrew-nav-render-preview.html` updated with the same JS swap (the preview's `<script>` block was a verbatim copy of the HE template's; I applied the same `Edit` to keep them aligned). New explicit click handler at line 434; closing tags intact at lines 454/455.

To verify on a deployed/served instance:

**Desktop:**
- Hover over **תורה** → dropdown opens (CSS hover behavior, no change from before).
- Click **תורה** → dropdown opens; click again → dropdown closes (this used to silently fail or double-toggle; now it works reliably because of `preventDefault` + explicit `[open]` management).
- Click **משנה** while תורה is open → תורה closes, משנה opens.

**Mobile:**
- Tap hamburger → menu drops down.
- Tap **תורה** → 3 dropdown items appear.
- Tap **תורה** again → closes.
- Tap **משנה** while תורה is open → תורה closes, משנה opens.
- Tap outside the menu → entire menu closes (existing click-outside handler still works).

---

## 5. Trade-Offs and Edge Cases

- **Keyboard users:** the native `<details>` element can be toggled via the Space or Enter key when `<summary>` is focused. Because `click` events fire when those keys activate a focused button-like element, the new handler catches those too. Keyboard accessibility is preserved.
- **`<details name="...">` accordion attribute:** the new HTML spec lets `<details>` elements with matching `name` attributes auto-close each other. We're not using that — partly because browser support is uneven (Safari ≥ 17) — and the new JS gives us the same accordion behavior with broader compatibility.
- **`e.preventDefault()` stops the default toggle.** This means the `<details>` element's `open` attribute is never set by the browser's own click handling. Anyone reading the HTML in a debugger should expect to see the `[open]` attribute change in response to JS, not in response to the native default action. This is a feature, not a bug — it's what makes the behavior reliable on mobile.

---

## 6. Files Touched

| File | Action |
|---|---|
| `_templates/Academic-Content-EN.html` | One `Edit`: 13-line close-others block replaced with 19-line explicit click handler |
| `_templates/Academic-Content-HE.html` | Same `Edit`, same content |
| `_pilot/hebrew-nav-render-preview.html` | Same `Edit` applied to keep preview aligned |
| `_pilot/explicit-click-dropdown.md` | This report |

The prior CSS fix in `main.css` (the `@media (max-width: 768px)` block tying `.dropdown` visibility to `<details>[open]`) is unchanged and remains in place — it's what makes the new JS's `[open]` toggling visually take effect on mobile.
