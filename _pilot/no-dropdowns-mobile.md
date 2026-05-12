# No Dropdowns on Mobile — Hide Them Entirely

**Date:** 2026-05-12
**Strategy:** Stop trying to make mobile dropdowns work. Hide them on mobile, turn the parent labels into direct links to the section's portal page. Desktop hover unchanged.
**Status:** Applied across both templates, main.css, and the preview. **Not committed.**

---

## ⚠ Spec / Current-State Mismatch — How I Reconciled

The spec was written assuming the templates still have `<details>/<summary>` markup. The prior task converted them to `<a class="dropdown-toggle">/<ul class="dropdown">` with a class-toggle JS handler. The current state on disk doesn't match the spec's "BEFORE" examples.

I delivered the **intent** of the task (desktop hover + mobile hide + parent labels go to portals) on the current markup. Three concrete adaptations from the literal spec:

1. **Spec said** "wrap `<summary>` text in `<a href="parent">`". **I did** change each `.dropdown-toggle`'s `href="#"` to the parent destination directly. End-user behavior identical.
2. **Spec said** "JS stays unchanged" (assuming the older `<details>` JS that was inert on mobile). **I had to** remove the current `.dropdown-toggle` click handler, because it called `e.preventDefault()` and would have blocked navigation on desktop — the opposite of the desired behavior.
3. **Spec's CSS** targeted `<summary>`/`<details>` selectors. **I wrote** equivalent CSS targeting the current `.dropdown-toggle`/`.dropdown` selectors. Same cascade outcome.

End-user behavior is exactly as the spec describes: desktop hover opens dropdowns, click on parent navigates; mobile shows only the top-level items, each a direct link.

---

## 1. HTML Changes — Toggle `href`s Now Point at Parent Destinations

### EN template

```diff
- <a href="#" class="dropdown-toggle">Torah</a>
+ <a href="/Torah-New/English/Torah%20Portal.htm" class="dropdown-toggle">Torah</a>
```

```
  <a href="#" class="dropdown-toggle">Insights</a>          (unchanged — no parent page exists)
```

### HE template

```diff
- <a href="#" class="dropdown-toggle">&#1514;&#1493;&#1512;&#1492;</a>
+ <a href="/Torah-New/Hebrew/Hebrew%20Torah%20Portal.htm" class="dropdown-toggle">&#1514;&#1493;&#1512;&#1492;</a>

- <a href="#" class="dropdown-toggle">&#1502;&#1513;&#1504;&#1492;</a>
+ <a href="/mishnah/" class="dropdown-toggle">&#1502;&#1513;&#1504;&#1492;</a>

- <a href="#" class="dropdown-toggle">&#1504;&#1514;&#1493;&#1504;&#1497;&#1501;</a>
+ <a href="/torah-weave/data/" class="dropdown-toggle">&#1504;&#1514;&#1493;&#1504;&#1497;&#1501;</a>
```

Decoded labels: **תורה** → Hebrew Torah Portal; **משנה** → `/mishnah/` (placeholder until built); **נתונים** → Torah data page.

The dropdown `<ul>` children of each toggle are byte-identical to before — no structural changes outside the toggle's `href`.

---

## 2. JavaScript Changes — Dropdown-Toggle Handler Removed

In both templates and the preview, the class-toggle click handler (~18 lines) was removed. The click-outside handler was simplified back to its original form (it no longer needs to clear `.is-open` because nothing sets that class anymore).

```diff
  if (!menu.contains(event.target) && !toggle.contains(event.target)) {
      menu.classList.remove('show');
-     // Also close any open dropdowns
-     document.querySelectorAll('.has-dropdown.is-open').forEach(function(li) {
-         li.classList.remove('is-open');
-     });
  }
  });

- // Dropdown toggle handler — class-based, works on mobile and desktop
- document.addEventListener('DOMContentLoaded', function() {
-     var toggles = document.querySelectorAll('.has-dropdown .dropdown-toggle');
-     toggles.forEach(function(toggle) {
-         toggle.addEventListener('click', function(e) {
-             e.preventDefault();
-             ...class-toggle logic...
-         });
-     });
- });
+ // Note: dropdown behavior is CSS-only.
+ // Desktop opens .dropdown on .has-dropdown:hover; mobile hides them entirely.
+ // Parent labels (.dropdown-toggle) are direct links to their parent destination.
```

**`toggleMenu()` is unchanged.** It still controls the mobile hamburger.

Why the JS removal was necessary: the prior task's click handler called `e.preventDefault()` on every toggle click. That worked when toggles had `href="#"` (preventDefault stopped the page from jumping). Now toggles have real `href`s pointing at portal pages — `preventDefault` would block the actual navigation we want. Easier to delete the handler than to add a "preventDefault only on desktop after-hover" branch.

---

## 3. CSS Changes — `main.css` Block Rewritten

The previous `NAV DROPDOWN — CLASS-TOGGLE PATTERN` block (~66 lines) replaced with a leaner `NAV DROPDOWN BEHAVIOR — DESKTOP HOVER + MOBILE HIDE` block (~46 lines).

### Removed

- `.has-dropdown.is-open .dropdown { display: flex }` — no longer used (no JS sets `.is-open`)
- The previous `@media (max-width: 768px)` block that styled the mobile dropdown layout (static position, full width, indented children) — irrelevant now that the dropdown is fully hidden on mobile

### Added (the only `.dropdown`/`.dropdown-toggle` rules now in `main.css`)

```css
/* Dropdown toggle label — clickable in all viewports */
.has-dropdown .dropdown-toggle {
    cursor: pointer;
    user-select: none;
}

/* Chevron on the toggle (hidden on mobile via the rule below) */
.has-dropdown .dropdown-toggle::after {
    content: ' \25BE';
    font-size: 0.7em;
    margin-inline-start: 0.25em;
}

/* Default: dropdown hidden everywhere */
.has-dropdown .dropdown {
    display: none;
}

/* Desktop only: hover-to-open behavior */
@media (hover: hover) and (pointer: fine) {
    .has-dropdown:hover .dropdown {
        display: flex;
        flex-direction: column;
    }
}

/* Mobile: hide dropdowns entirely. Parent .dropdown-toggle navigates
   to its href as a direct link instead. */
@media (max-width: 768px) {
    .has-dropdown .dropdown {
        display: none !important;
    }
    .has-dropdown .dropdown-toggle::after {
        content: '' !important;
    }
}
```

The cascade is now trivial:
- Default state: `display: none`.
- Desktop only, on hover: `display: flex`.
- Mobile (any state): `display: none !important` — wins over the inline DWT CSS regardless of source order.

---

## 4. Verification — All 8 Programmatic Checks Passed

| # | Spec check (adapted to current markup) | Result |
|---|---|---|
| 1 | `main.css` contains the new consolidated block with both `@media (hover: hover)` and `@media (max-width: 768px)` sections inside the dropdown-behavior comment block | ✓ block starts line 3838; hover at 3865; mobile at 3874 |
| 2 | Previous `MOBILE NAV — FLAT LIST APPROACH` block removed | ✓ (already removed in the prior task) |
| 3 | Standalone `NAV DROPDOWN HOVER BEHAVIOR` block removed/merged | ✓ (merged into the new block; one `@media (hover: hover)` in the file at line 3865) |
| 4 | Flat-list `!important` declarations (`display: contents`, `pointer-events: none`, etc.) removed | ✓ Grep confirms zero matches |
| 5 | HE template's three `.dropdown-toggle` `<a>` elements each point at the parent destination (not `#`) | ✓ Torah Portal, /mishnah/, /torah-weave/data/ |
| 6 | EN template's `.dropdown-toggle` `<a>` elements similarly | ✓ Torah → Torah Portal; Insights → `#` (no parent page; spec-permitted) |
| 7 | No template structure changes outside the toggle `href`/JS-handler updates | ✓ dropdown `<ul>` blocks and footer untouched |
| 8 | JS adapted: the (current) class-toggle click handler is **removed** because it would block desktop navigation; `toggleMenu()` and click-outside remain | ✓ confirmed in both templates |

Spec's check 8 said "JS unchanged". On the current markup that would leave `e.preventDefault()` blocking the new direct-link navigation on desktop — directly opposite to the spec's intent. Removing the handler is the only way to honor both "click on parent navigates" and "JS stays as inert as possible."

---

## 5. Expected Behavior

### Desktop (≥768 px, hover-capable)

| Action | Result |
|---|---|
| Hover **תורה** / Torah / etc. | Dropdown items appear below (CSS `:hover` rule) |
| Move cursor away | Dropdown disappears |
| Click **תורה** (or any parent label) | Navigates to Hebrew Torah Portal directly (NEW — was previously a JS toggle) |
| Click a dropdown child | Navigates to that child's page |

### Mobile (<768 px)

| Action | Result |
|---|---|
| Tap hamburger | Menu drops down |
| See **6 top-level items**: דף הבית, תורה, משנה, נתונים, צור קשר, English | All direct links |
| Tap **תורה** | Navigates to Hebrew Torah Portal |
| Tap **משנה** | Navigates to `/mishnah/` (currently a placeholder 404 — will start working once the portal page is built) |
| Tap **נתונים** | Navigates to the Torah data page |
| Tap **צור קשר** | Goes to the contact page |
| No dropdowns appear, no chevrons, no tap-to-expand, no accordion |

For users on mobile who want to reach a sub-item (e.g., **שער המשנה**, **PDF המשנה**, **מבוא**, **קוד הצבעים**), they tap **משנה** first to land on the Mishnah Portal, then drill down from there. That's the spec's stated intent: "Users navigate to portal pages first, then drill down from there."

**Accessibility note about Insights on mobile:** Insights' 10 articles become unreachable from the EN mobile nav (since `href="#"` doesn't go anywhere). The spec acknowledged this — "if no parent page exists, leave as a non-navigating link or use `href="#"`." Each individual Insights article still has its own URL and can be linked to from elsewhere on the site; the mobile nav just doesn't surface them. If you want them mobile-reachable later, a follow-up could either (a) create an `/insights/` index page and point the toggle there, or (b) flatten Insights into the mobile nav as a separate non-dropdown link list.

---

## 6. Files Touched

| File | Action |
|---|---|
| `_templates/Academic-Content-EN.html` | Torah toggle href changed; Insights stays at `#`; class-toggle JS handler removed; click-outside simplified |
| `_templates/Academic-Content-HE.html` | All three toggle hrefs updated to parent destinations; same JS removal/simplification |
| `torah-weave/Admin/Assets/CSS/main.css` | Nav dropdown block rewritten (~66 lines → ~46 lines). Net −20 lines |
| `_pilot/hebrew-nav-render-preview.html` | Same href + JS changes as HE template |
| `_pilot/no-dropdowns-mobile.md` | This report |

No DWT files touched. No content changes. The 525 Mishnah chapter pages and other out-of-scope items unchanged.
