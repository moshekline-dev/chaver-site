# Mobile Nav — Flat List Approach

**Date:** 2026-05-12
**File:** `torah-weave/Admin/Assets/CSS/main.css`
**Strategy:** Eliminate dropdown UI on mobile entirely. All destinations visible at once, dropdown children indented to show hierarchy. Desktop hover behavior unchanged.
**Status:** Applied. **Not committed.**

---

## 1. Before / After — The Mobile Block

Replaced the entire previous `MOBILE NAV DROPDOWN — VISIBILITY + LAYOUT` block (lines 3876–3909 in the prior state) with the new flat-list block (lines 3876–3924 now). No `MOBILE HAMBURGER CENTERING` block existed in the file; nothing to remove there.

### REMOVED — the visibility/layout approach

```css
/* MOBILE NAV DROPDOWN — VISIBILITY + LAYOUT */
@media (max-width: 768px) {
    .has-dropdown details { display: block; width: 100%; }
    .has-dropdown .dropdown { width: 100%; left: auto; right: auto; top: auto; }
    .has-dropdown details:not([open]) .dropdown { display: none; }
    .has-dropdown details[open] .dropdown { display: flex; }
}
```

That approach assumed: (a) the explicit click handler reliably toggles `[open]` on mobile, and (b) the `[open]`-keyed display rules then make the dropdown visible. Three sessions of debugging never confirmed both holding at once on the target mobile browsers — without device inspection we couldn't tell which assumption was breaking. So we're abandoning the toggle-on-mobile model.

### ADDED — flat-list approach

```css
/* MOBILE NAV — FLAT LIST APPROACH */
@media (max-width: 768px) {
    .has-dropdown details { display: contents; }

    .has-dropdown summary {
        cursor: default;
        list-style: none;
        pointer-events: none;
    }
    .has-dropdown summary::-webkit-details-marker { display: none; }
    .has-dropdown summary::after { content: ''; }

    .has-dropdown .dropdown {
        display: flex !important;
        flex-direction: column;
        position: static;
        width: 100%;
        box-shadow: none;
        min-width: 0;
        padding: 0;
        background: transparent;
    }

    .has-dropdown .dropdown li a {
        padding-left: 2.5rem;
        padding-right: 2.5rem;
        font-size: 0.95em;
        opacity: 0.92;
    }
}
```

### What each rule group does

| Rule | Purpose |
|---|---|
| `details { display: contents }` | The `<details>` wrapper disappears from the layout tree on mobile. Its children (`<summary>`, `<ul.dropdown>`) flow as direct children of `<li.has-dropdown>`. No more inline-vs-block parent confusion that was breaking the layout. |
| `summary { pointer-events: none }` | Taps on the summary do nothing. It just shows the category label (e.g., "תורה"). No JS event fires, no native toggle attempts — every browser quirk we were fighting is bypassed because user input never reaches the element. |
| `summary::after { content: '' }` | Removes the ▾ chevron — there's no dropdown to indicate. |
| `.dropdown { display: flex !important; flex-direction: column; position: static; width: 100% }` | The dropdown items are always visible on mobile. `!important` defeats any leftover `display: none` rule that might still be in the cascade. `position: static` removes desktop's absolute positioning. `flex-direction: column` stacks the items vertically. |
| `.dropdown li a { padding-left: 2.5rem; ... opacity: 0.92 }` | Visual hierarchy — children are indented and slightly subdued so the eye can tell them apart from top-level items. |

---

## 2. Verification — All 8 Programmatic Checks Passed

| # | Check | Result |
|---|---|---|
| 1 | New `MOBILE NAV — FLAT LIST APPROACH` block present exactly once | ✓ line 3877 |
| 2 | All 5 rule groups present | ✓ `details {contents}` 3889; `summary {pointer-events: none}` 3896; `summary::after` 3901; `.dropdown {display: flex !important}` 3907; `.dropdown li a {padding-left: 2.5rem}` 3919 |
| 3 | Previous `MOBILE NAV DROPDOWN VISIBILITY` block fully removed | ✓ (Grep returned 0 matches for that header) |
| 4 | Previous `MOBILE HAMBURGER CENTERING` block removed | ✓ (no such block existed in the file — nothing to remove) |
| 5 | `@media (hover: hover) and (pointer: fine)` block unchanged | ✓ still at line 3845, body unchanged |
| 6 | File ends with `END OF MAIN.CSS` banner | ✓ line 3927 |
| 7 | No template files (EN or HE) modified | ✓ (only `main.css` edited this task) |
| 8 | No script changes | ✓ |

The preview file `_pilot/hebrew-nav-render-preview.html` is already aligned with the current template/JS state from the prior task and links to `main.css` via absolute URL, so it picks up the new flat-list rules automatically when viewed at narrow viewport widths. No HTML edit to the preview was needed.

---

## 3. Behavior Change Note

**This is a mobile UX change, not just a bug fix.** The dropdown UI on mobile is gone. Mobile users now see a flat list with all 12 destinations:

```
דף הבית
תורה            (label — not tappable)
    שער התורה
    מפת התורה
    קוד הצבעים
משנה            (label — not tappable)
    שער המשנה
    מבוא
    PDF המשנה
    קוד הצבעים  (same destination as above)
נתונים          (label — not tappable)
    התורה
    המשנה
צור קשר
English
```

Trade-offs:

- **+** All destinations reachable in one tap. No "open this dropdown first" step. No browser quirks to fight.
- **+** Pattern matches the dominant mobile nav UX on modern news/content sites — familiar.
- **–** Slightly more vertical scroll inside the menu (the items used to be hidden behind summaries).
- **–** קוד הצבעים appears twice (under תורה and under משנה) — that's already how the desktop dropdowns are structured; mobile just makes both copies visible. Both point at the same destination, so it's not broken, just slightly redundant.

Desktop is unchanged. The hover-to-open behavior on pointer-capable devices keeps the dropdown UI exactly as it was.

---

## 4. What Stays In Place

| Item | State |
|---|---|
| HTML `<details>` / `<summary>` markup in both templates | Unchanged — semantic HTML preserved for accessibility |
| Explicit click handler JS (`summary.addEventListener('click', ...)`) | Stays. On mobile, `pointer-events: none` prevents it from firing. On desktop, it still fires on click and toggles `[open]`. No conflict. |
| `@media (hover: hover) and (pointer: fine)` block in main.css | Unchanged — drives desktop hover behavior |
| Templates (EN and HE) | Unchanged |
| Footer, scripts, content regions | Unchanged |

---

## 5. Files Touched

| File | Action |
|---|---|
| `torah-weave/Admin/Assets/CSS/main.css` | Mobile block replaced (lines 3876–3924). Old block was 33 lines; new block is 48 lines. Net +15 lines. |
| `_pilot/mobile-flat-nav.md` | This report |

No template changes. No JavaScript changes. No preview HTML change needed.
