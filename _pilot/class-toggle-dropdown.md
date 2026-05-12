# Nav Dropdowns Rewritten — Class-Toggle Pattern

**Date:** 2026-05-12
**Strategy:** Stop fighting `<details>/<summary>`. Use standard `<a>/<ul>` markup with JS-controlled `.is-open` class — the pattern that every working mobile nav uses (Elementor, Bootstrap, every CMS theme).
**Status:** Applied across both templates, main.css, and the preview. **Not committed.**

---

## 1. Why This Replaces the Previous Approach

We tried five mechanical fixes for `<details>/<summary>` on mobile:

1. CSS `[open]` attribute selectors
2. Explicit JS click handler with `e.preventDefault()`
3. `<details> { display: block }` override
4. `!important` flags on layout-critical rules
5. Forcing `<details>.open = true` on mobile

Each fix addressed one symptom and uncovered another. The root cause is that `<details>` carries a *user-agent shadow tree* with its own visibility logic that doesn't compose well with custom CSS layouts. The fix isn't another override — it's swapping out the markup.

`<a href="#" class="dropdown-toggle">` + `<ul class="dropdown">` doesn't have a shadow tree, doesn't auto-toggle, doesn't have native hide-when-closed behavior. Visibility is fully under our control via the `.is-open` class. The pattern is mature, well-supported, and is what the user reported is working today on the woven-torah Elementor pages.

---

## 2. HTML — Before / After

### EN template (2 dropdowns)

```diff
  <li class="has-dropdown">
-     <details>
-         <summary>Torah</summary>
-         <ul class="dropdown">
-             <li><a href="/Torah-New/English/Torah%20Portal.htm">Torah Portal</a></li>
-             <li><a href="/torah-weave/commentary">Commentary</a></li>
-             <li><a href="/woven-torah/full-torah-map-2/">Full Torah Map</a></li>
-         </ul>
-     </details>
+     <a href="#" class="dropdown-toggle">Torah</a>
+     <ul class="dropdown">
+         <li><a href="/Torah-New/English/Torah%20Portal.htm">Torah Portal</a></li>
+         <li><a href="/torah-weave/commentary">Commentary</a></li>
+         <li><a href="/woven-torah/full-torah-map-2/">Full Torah Map</a></li>
+     </ul>
  </li>
```

Same transformation applied to the **Insights** dropdown (10 items, indentation cleaned up).

### HE template (3 dropdowns)

Same shape transformation applied to **תורה** (3 items), **משנה** (4 items), and **נתונים** (2 items). The `<details>` wrappers are gone; each summary becomes `<a href="#" class="dropdown-toggle">` with the same Hebrew label. All leaf `<li><a>` items are byte-identical to before.

### Preview file

Same three HE-style transformations applied to keep the preview aligned with the HE template.

---

## 3. JavaScript — Before / After (identical change in both templates + preview)

### Removed (three blocks gone, ~50 lines)

- The explicit click handler that listened on every `<summary>` inside `.has-dropdown`, called `preventDefault()`, manipulated `<details>.[open]`, etc.
- The `forceDetailsOpenOnMobile()` function (with `matchMedia` check and `d.open = true/false` writes).
- The `window.addEventListener('resize', forceDetailsOpenOnMobile)` listener.

### Added (one block, ~18 lines)

```javascript
// Dropdown toggle handler — class-based, works on mobile and desktop
document.addEventListener('DOMContentLoaded', function() {
    var toggles = document.querySelectorAll('.has-dropdown .dropdown-toggle');
    toggles.forEach(function(toggle) {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            var parentLi = toggle.closest('.has-dropdown');
            var wasOpen = parentLi.classList.contains('is-open');

            // Close all dropdowns
            document.querySelectorAll('.has-dropdown.is-open').forEach(function(li) {
                li.classList.remove('is-open');
            });

            // Open this one if it wasn't already
            if (!wasOpen) {
                parentLi.classList.add('is-open');
            }
        });
    });
});
```

### Modified (click-outside handler — same in both templates)

The existing handler now also closes any `.is-open` dropdowns when the user taps outside:

```diff
  if (!menu.contains(event.target) && !toggle.contains(event.target)) {
      menu.classList.remove('show');
+     // Also close any open dropdowns
+     document.querySelectorAll('.has-dropdown.is-open').forEach(function(li) {
+         li.classList.remove('is-open');
+     });
  }
```

`toggleMenu()` is **unchanged**.

---

## 4. CSS — `main.css` Restructured

Two existing blocks at lines 3837–3934 (~98 lines) were both removed:

- **`NAV DROPDOWN HOVER BEHAVIOR`** — the desktop hover-open block that operated on `.has-dropdown:hover .dropdown` (and the empty `@media (hover: none)` placeholder).
- **`MOBILE NAV — FLAT LIST APPROACH`** — the !important-laden block that used `display: contents` on `<details>` and hid the chevron.

Replaced with a single consolidated **`NAV DROPDOWN — CLASS-TOGGLE PATTERN`** block at lines 3837–3902 (~66 lines):

```css
/* Dropdown toggle label — styled like a regular nav link */
.has-dropdown .dropdown-toggle {
    cursor: pointer;
    user-select: none;
}

/* Show a chevron on the toggle */
.has-dropdown .dropdown-toggle::after {
    content: ' \25BE';
    font-size: 0.7em;
    margin-inline-start: 0.25em;
}

/* By default, dropdown is hidden */
.has-dropdown .dropdown {
    display: none;
}

/* Show dropdown when parent <li> has .is-open class (tap/click toggle) */
.has-dropdown.is-open .dropdown {
    display: flex;
    flex-direction: column;
}

/* Desktop only: hover-to-open behavior */
@media (hover: hover) and (pointer: fine) {
    .has-dropdown:hover .dropdown {
        display: flex;
        flex-direction: column;
    }
}

/* Mobile-specific layout adjustments */
@media (max-width: 768px) {
    .has-dropdown .dropdown {
        position: static;
        box-shadow: none;
        min-width: 0;
        padding: 0;
        width: 100%;
        background: transparent;
    }
    .has-dropdown .dropdown li a {
        padding-left: 2.5rem;
        padding-right: 2.5rem;
        font-size: 0.95em;
    }
}
```

The cascade is now simple:
- Default state: dropdown hidden (`display: none`).
- `.has-dropdown.is-open .dropdown` → visible (JS toggles this on tap/click at any viewport).
- `.has-dropdown:hover .dropdown` → visible (CSS only, on hover-capable devices).
- On mobile (`max-width: 768px`), the dropdown is also restyled to flow inline below the toggle (static positioning, full width, indented children).

No `!important` needed anywhere because the selectors don't collide with the DWT's inline `<style>` block — the DWT styles `.dropdown` for the now-removed `<details>` context, and our new rules target the same `.dropdown` class but in a context the DWT doesn't have rules for (`.has-dropdown.is-open .dropdown`, `.has-dropdown:hover .dropdown` are both higher specificity than the inline `.dropdown {}` rule).

---

## 5. Verification — All 8 Programmatic Checks Passed

| # | Check | Result |
|---|---|---|
| 1 | Neither template has any `<details>` or `<summary>` tags in nav HTML | ✓ Grep returned 0 matches for both elements in both templates |
| 2 | Each template has the new `<a href="#" class="dropdown-toggle">` markup | ✓ EN: 2 dropdowns (lines 318, 326); HE: 3 dropdowns (lines 318, 326, 335) |
| 3 | Both templates have the new class-based click handler | ✓ EN line 431; HE line 426 |
| 4 | Old handlers fully removed from both templates | ✓ No `summaries`, `forceDetailsOpenOnMobile`, or `addEventListener('toggle'` in either file |
| 5 | `main.css` has the new `CLASS-TOGGLE PATTERN` block | ✓ line 3838 |
| 6 | `main.css` has the old `MOBILE NAV — FLAT LIST APPROACH` and standalone hover-open blocks removed | ✓ both gone (Grep returned 0 matches for those headers) |
| 7 | Both templates' click-outside handler now also closes `.is-open` dropdowns | ✓ EN lines 423–424; HE lines 418–419 |
| 8 | Both templates end cleanly with `</script>` → `{{ region: page-scripts }}` → `</body>` → `</html>` | ✓ EN: 450/452/453/454; HE: closing tags at 448/449 |

---

## 6. Expected Behavior After Deploy

### Desktop

| Action | Result |
|---|---|
| Hover over **תורה** | Dropdown shows (CSS `:hover` rule) |
| Move cursor away | Dropdown hides |
| Click on **תורה** | Dropdown opens via `.is-open` (JS); stays open until another action closes it |
| Click another toggle while one is open | Previous closes, new one opens (close-all-then-open logic in handler) |
| Click outside menu | All dropdowns close (click-outside handler) |

### Mobile

| Action | Result |
|---|---|
| Tap hamburger | Menu drops down (existing `toggleMenu()` unchanged) |
| Tap **תורה** | 3 indented items appear below; chevron flips conceptually (chevron is part of the toggle's `::after`) |
| Tap **תורה** again | Items hide |
| Tap **משנה** while **תורה** is open | **תורה** closes, **משנה** opens with its 4 items |
| Tap a leaf item (e.g., **שער התורה**) | Navigates to that page (default `<a>` behavior, no preventDefault on leaf items) |
| Tap outside menu | Entire menu closes, including any open dropdown |

---

## 7. DWT Pages Out of Scope (Per Task Spec)

Legacy DWT-attached pages (the ~500 `.htm` files) still have `<details>/<summary>` markup baked into their HTML body — that's what the DWT propagated. Those pages will keep using the old markup and will keep having the mobile dropdown bug, but they'll continue to work fine on desktop.

If/when you decide this new approach is stable on the new-template pages, a follow-up task can bulk-edit the DWT files (or the body-baked nav in legacy pages) to switch them to the same `<a>/<ul>` pattern. That's a meaningful undertaking — affects every old `.htm` page — and the spec wisely kept it out of scope here.

---

## 8. Files Touched

| File | Action |
|---|---|
| `_templates/Academic-Content-EN.html` | Nav HTML: 2 dropdowns converted. JS: explicit click handler + `forceDetailsOpenOnMobile` removed; class-toggle handler added; click-outside updated |
| `_templates/Academic-Content-HE.html` | Nav HTML: 3 dropdowns converted. JS: same swap |
| `torah-weave/Admin/Assets/CSS/main.css` | Two old blocks removed (~98 lines), one consolidated block added (~66 lines). Net −32 lines |
| `_pilot/hebrew-nav-render-preview.html` | Same HTML + JS swap as HE template |
| `_pilot/class-toggle-dropdown.md` | This report |

No DWT files touched.
