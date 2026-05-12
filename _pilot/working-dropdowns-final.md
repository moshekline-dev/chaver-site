# Working Mobile Dropdowns — Coordinated Single Commit

**Date:** 2026-05-12
**Strategy:** Remove the orphan `<details>/<summary>` CSS that was silently overriding every fix this session AND restore the class-toggle pattern, all in one commit. After this, mobile users get tap-to-expand dropdowns; desktop users get hover dropdowns; both driven from `main.css` alone.
**Status:** Four coordinated changes applied. **Not committed.**

---

## 1. Orphan CSS Removed from Both Templates' Inline `<style>`

This was the silent root cause throughout the session: the templates' inline `<style>` block still contained a 55-line "DROPDOWN MENU - NATIVE details/summary" section from the original template, plus 2 dropdown-related rules inside the `@media (max-width: 768px)` block. Because the inline `<style>` loads *after* `main.css`, those rules won every cascade tie against anything we put in `main.css`. Every attempted fix was dying here.

### Removed from each template

**A — The DROPDOWN MENU section (~55 lines):**

```diff
-     /* ==========================================
-        DROPDOWN MENU - NATIVE details/summary
-        ========================================== */
-
-     .has-dropdown { position: relative; }
-     .has-dropdown details { display: inline; }
-     .has-dropdown summary {
-         cursor: pointer;
-         list-style: none;
-         padding: 0.25rem 0.75rem;
-         border-radius: 4px;
-         transition: all 0.3s ease;
-     }
-     .has-dropdown summary::-webkit-details-marker { display: none; }
-     .has-dropdown summary::after {
-         content: ' \25BE';
-         font-size: 0.7em;
-     }
-     .dropdown {
-         position: absolute;
-         top: 100%;
-         left: 0;
-         display: flex;
-         flex-direction: column;
-         list-style: none;
-         min-width: 200px;
-         padding: 0.4rem 0;
-         border-radius: 4px;
-         box-shadow: 0 4px 12px rgba(0,0,0,0.15);
-         background: #fff;
-         z-index: 1001;
-         gap: 0;
-     }
-     .dropdown li { width: 100%; }
-     .dropdown a {
-         display: block;
-         padding: 0.5rem 1rem;
-         white-space: nowrap;
-         border-radius: 0;
-     }
```

**B — Mobile `@media (max-width: 768px)` rules cleaned up:**

```diff
-         nav a, .has-dropdown summary {
+         nav a {
              display: block;
              padding: 1rem;
          }

-         /* Mobile dropdown: no flyout, just indent */
-         .dropdown {
-             position: static;
-             box-shadow: none;
-             min-width: 0;
-             padding: 0;
-         }
-
-         .dropdown a {
-             padding-left: 2rem;
-             font-size: 0.95em;
-         }
```

**C — Landscape nested `@media` rule cleaned up:**

```diff
-             nav a, .has-dropdown summary {
+             nav a {
                  display: block;
                  padding: 0.75rem 1rem;
                  border-bottom: 1px solid rgba(61, 47, 31, 0.2);
              }
```

The `nav a` rules survive (they apply to all leaf nav links); only the `.has-dropdown summary` half of the comma list was orphan. After these edits, **no inline `<style>` rule in either template references `details`, `summary`, `.has-dropdown`, `.dropdown`, or `.dropdown-toggle`**. All dropdown CSS lives in `main.css` only.

Same three edits applied identically to `_pilot/hebrew-nav-render-preview.html`.

---

## 2. Class-Toggle JS Handler Restored in Both Templates

In both templates' `<script>` block, the inert "dropdown behavior is CSS-only" comment was replaced with an active class-toggle handler. The click-outside handler was extended to also clear `.is-open` when the user taps outside the menu.

### Added (same code in both templates + preview)

```javascript
// Dropdown toggle handler — class-based, tap-to-expand on mobile
document.addEventListener('DOMContentLoaded', function() {
    var toggles = document.querySelectorAll('.has-dropdown .dropdown-toggle');
    toggles.forEach(function(toggle) {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            var parentLi = toggle.closest('.has-dropdown');
            var wasOpen = parentLi.classList.contains('is-open');

            // Close all dropdowns first
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

### Click-outside also extended

```diff
  if (!menu.contains(event.target) && !toggle.contains(event.target)) {
      menu.classList.remove('show');
+     document.querySelectorAll('.has-dropdown.is-open').forEach(function(li) {
+         li.classList.remove('is-open');
+     });
  }
```

`toggleMenu()` is unchanged.

---

## 3. Toggle `href`s Reverted to `#`

Because the JS handler now intercepts clicks with `e.preventDefault()`, the toggle's `href` can be `#` again — the page won't jump.

### EN template

```diff
- <a href="/Torah-New/English/Torah%20Portal.htm" class="dropdown-toggle">Torah</a>
+ <a href="#" class="dropdown-toggle">Torah</a>
```

Insights was already `href="#"` — no change.

### HE template (and preview)

```diff
- <a href="/Torah-New/Hebrew/Hebrew%20Torah%20Portal.htm" class="dropdown-toggle">תורה</a>
+ <a href="#" class="dropdown-toggle">תורה</a>

- <a href="/mishnah/" class="dropdown-toggle">משנה</a>
+ <a href="#" class="dropdown-toggle">משנה</a>

- <a href="/torah-weave/data/" class="dropdown-toggle">נתונים</a>
+ <a href="#" class="dropdown-toggle">נתונים</a>
```

---

## 4. `main.css` — Block Rewritten with `!important`

The existing `NAV DROPDOWN BEHAVIOR — DESKTOP HOVER + MOBILE HIDE` block was replaced with the new `NAV DROPDOWN — CLASS-TOGGLE PATTERN` block.

### Replaced (was ~46 lines)

The previous block hid dropdowns entirely on mobile (the workaround we shipped while debugging).

### Added (now ~65 lines, lines 3837–3902 in main.css)

```css
/* Dropdown toggle label — clickable in all viewports */
.has-dropdown .dropdown-toggle {
    cursor: pointer;
    user-select: none;
}

/* Chevron on the toggle */
.has-dropdown .dropdown-toggle::after {
    content: ' \25BE';
    font-size: 0.7em;
    margin-inline-start: 0.25em;
}

/* Default: dropdown hidden everywhere */
.has-dropdown .dropdown {
    display: none !important;
}

/* Show dropdown when parent <li> has .is-open class (set by JS on tap) */
.has-dropdown.is-open .dropdown {
    display: flex !important;
    flex-direction: column !important;
}

/* Desktop: also show on hover */
@media (hover: hover) and (pointer: fine) {
    .has-dropdown:hover .dropdown {
        display: flex !important;
        flex-direction: column !important;
    }
}

/* Mobile-specific layout: dropdown flows inline, full width */
@media (max-width: 768px) {
    .has-dropdown .dropdown {
        position: static !important;
        box-shadow: none !important;
        min-width: 0 !important;
        padding: 0 !important;
        width: 100% !important;
        background: transparent !important;
        top: auto !important;
        left: auto !important;
        right: auto !important;
    }

    .has-dropdown .dropdown li a {
        padding-left: 2.5rem;
        padding-right: 2.5rem;
        font-size: 0.95em;
    }
}
```

**Why `!important` everywhere:** the orphan CSS is gone from the *new* templates after this commit, but the **DWT-attached legacy pages** still load their inline `<style>` block with the orphan rules (we explicitly chose not to touch the DWT in this task). On those pages, `main.css` loads first, the DWT inline `<style>` loads second, and `!important` is what wins the cascade against the DWT's `display: inline` on `<details>` and `position: absolute; display: flex` on `.dropdown`.

---

## 5. Verification — All 10 Programmatic Checks Passed

| # | Check | Result |
|---|---|---|
| 1 | Both templates have ZERO occurrences of `details`, `summary`, `.has-dropdown summary`, `.has-dropdown details` in inline `<style>` | ✓ Grep returned no matches in either |
| 2 | Both templates have ZERO `.dropdown {` rules in inline `<style>` (only `main.css` has dropdown CSS) | ✓ |
| 3 | Both templates have the class-toggle JS handler (`toggles.forEach`) | ✓ EN line 362; HE line 357 |
| 4 | Both templates' click-outside handler closes `.is-open` dropdowns | ✓ EN lines 353–354; HE lines 348–349 |
| 5 | All `.dropdown-toggle` hrefs are `#` | ✓ EN: 2 (Torah 249, Insights 257); HE: 3 (תורה 249, משנה 257, נתונים 266) |
| 6 | `main.css` has the new `CLASS-TOGGLE PATTERN` block with `!important` flags | ✓ line 3838 |
| 7 | `main.css` has NO other dropdown-related blocks | ✓ this is the only one |
| 8 | `_pilot/hebrew-nav-render-preview.html` regenerated from the updated HE template | ✓ same edits applied |
| 9 | Preview also has the orphan CSS removed AND the class-toggle JS | ✓ Grep confirms no orphan CSS; `toggles.forEach` at line 361 |
| 10 | Both templates end cleanly (`</script>` → `{{ region: page-scripts }}` → `</body>` → `</html>`) | ✓ EN: `</body>` 383, `</html>` 384; HE: `</body>` 378, `</html>` 379 |

---

## 6. Root Cause — Documented for the Audit Trail

For the record, here's why the previous five fixes silently failed:

| Fix attempt | What we tried | Why it failed |
|---|---|---|
| 1. `[open]` attribute selectors | Tie dropdown visibility to `<details>[open]` via CSS in `main.css` | The inline `<style>` had `.dropdown { display: flex }` unconditionally → won the cascade |
| 2. Explicit JS click handler | Manage `<details>[open]` manually in response to clicks | CSS visibility was still being driven by the inline `<style>`, not by `[open]` |
| 3. `display: block` on `<details>` on mobile | Override the desktop `display: inline` | The inline `<style>` had it set with equal specificity and *later* source order — inline won |
| 4. `!important` on layout rules | Force our cascade wins | The orphan `.dropdown { display: flex }` in inline `<style>` was already `display: flex` — adding `!important` to our own `display: flex !important` didn't help because the visible-state contradiction was elsewhere (native `<details>` shadow tree) |
| 5. Force `<details>.open = true` on mobile | Programmatically bypass shadow-tree hiding | Worked technically, but the inline `<style>`'s `.dropdown` positioning (`position: absolute`) put the now-visible items off-screen |

All five failed because we never cleaned up the inline `<style>`. **This commit finally does** — for the new templates. The DWT-attached legacy pages still have the orphan CSS, but the `!important` flags in `main.css` win on those pages too (the orphan CSS doesn't use `!important`, so any non-`!important` declaration loses to ours regardless of source order).

---

## 7. Expected Behavior After Deploy

**Desktop (≥768 px, hover-capable):**
- Hover **תורה** / Torah / etc. → dropdown opens (CSS `:hover` rule)
- Click on `.dropdown-toggle` → also opens (via JS `.is-open` class)
- Click a child item → navigates
- Move cursor away → dropdown hides
- Click outside menu → all dropdowns close

**Mobile (<768 px):**
- Tap hamburger → menu drops down full-width
- Tap **תורה** → dropdown expands below, indented children (שער התורה, מפת התורה, קוד הצבעים)
- Tap **תורה** again → collapse
- Tap **משנה** while **תורה** is open → תורה closes, משנה opens with its 4 children
- Tap a leaf item → navigates
- Tap outside menu → menu + all dropdowns close

This is the Elementor-style tap-to-expand pattern. With the orphan CSS finally gone, there's nothing fighting it.

---

## 8. Files Touched

| File | Action |
|---|---|
| `_templates/Academic-Content-EN.html` | Inline `<style>` cleaned (3 edits, ~60 lines removed); JS handler restored; Torah toggle href reverted to `#` |
| `_templates/Academic-Content-HE.html` | Same inline `<style>` cleanup; same JS restore; all 3 toggle hrefs reverted to `#` |
| `torah-weave/Admin/Assets/CSS/main.css` | Existing block replaced with the `!important`-flagged `CLASS-TOGGLE PATTERN` version (~65 lines) |
| `_pilot/hebrew-nav-render-preview.html` | Same three changes as HE template (inline CSS cleanup + JS restore + href revert) |
| `_pilot/working-dropdowns-final.md` | This report |

**Out of scope (per task spec):** DWT files in `Dynamic Web Templates/`. Legacy DWT-attached pages still have the orphan CSS, but `main.css`'s `!important` flags win the cascade on those pages anyway. A follow-up bulk-edit task can clean up the DWT if/when you want to make the cascade no longer rely on `!important`.
