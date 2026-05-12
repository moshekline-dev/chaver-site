# Mobile Flat-List Nav — `!important` for DWT Cascade Win

**Date:** 2026-05-12
**File:** `torah-weave/Admin/Assets/CSS/main.css`
**Status:** `!important` flags added to layout-critical rules in the flat-list block. **Not committed.**

---

## 1. Before / After — The Flat-List Block

### BEFORE (no `!important` on layout rules)

```css
@media (max-width: 768px) {
    .has-dropdown details {
        display: contents;
    }
    .has-dropdown summary {
        cursor: default;
        list-style: none;
        pointer-events: none;
    }
    /* ... */
    .has-dropdown .dropdown {
        display: flex !important;       /* only flag — but inline CSS still won other rules */
        flex-direction: column;
        position: static;
        width: 100%;
        /* ... */
    }
    /* visual polish at the bottom */
}
```

### AFTER (`!important` on every layout-critical declaration)

```css
@media (max-width: 768px) {
    .has-dropdown details {
        display: contents !important;
    }

    .has-dropdown summary {
        cursor: default !important;
        list-style: none !important;
        pointer-events: none !important;
    }
    .has-dropdown summary::-webkit-details-marker {
        display: none !important;
    }
    .has-dropdown summary::after {
        content: '' !important;
    }

    .has-dropdown .dropdown {
        display: flex !important;
        flex-direction: column !important;
        position: static !important;
        width: 100% !important;
        box-shadow: none !important;
        min-width: 0 !important;
        padding: 0 !important;
        background: transparent !important;
    }

    /* visual polish — no !important needed */
    .has-dropdown .dropdown li a {
        padding-left: 2.5rem;
        padding-right: 2.5rem;
        font-size: 0.95em;
        opacity: 0.92;
    }
}
```

The indentation/opacity rules at the bottom are left without `!important` — they're visual polish, not layout-critical. If something in the DWT overrides them, the user sees slightly different indentation, not a broken nav.

---

## 2. Verification — All Programmatic Checks Passed

| Declaration | Required? | Line |
|---|---|---|
| `display: contents !important` (on `.has-dropdown details`) | ✓ | 3895 |
| `pointer-events: none !important` (on `.has-dropdown summary`) | ✓ | 3903 |
| `display: flex !important` (on `.has-dropdown .dropdown`) | ✓ | 3914 |
| `flex-direction: column !important` | ✓ | 3915 |
| `position: static !important` | ✓ | 3916 |
| `width: 100% !important` | ✓ | 3917 |

Other checks:
- `@media (hover: hover) and (pointer: fine)` block at line 3845 — **unchanged** ✓
- `END OF MAIN.CSS` banner at line 3937 — **intact** ✓ (was 3927; +10 lines from the expanded block)
- No CSS outside the flat-list block was modified ✓

---

## 3. Bonus Check — DWT Cascade Situation Confirmed

Fetched the live DWT page `https://chaver.com/Torah-New/English/Torah%20Portal.htm` (HTTP 200, 35,796 bytes) to verify the diagnosis.

**Both CSS sources present on the same page:**

| Source | Status |
|---|---|
| `<link rel="stylesheet" href="/torah-weave/Admin/Assets/CSS/main.css">` | Present in the head |
| One inline `<style>` block (the DWT's CSS) | Present in the head, after the main.css link |

**The exact conflicting rules in the inline `<style>` block** (the ones that were beating us):

```css
.has-dropdown details {
    display: inline;
}

.has-dropdown summary {
    cursor: pointer;
    list-style: none;
    padding: 0.25rem 0.75rem;
    border-radius: 4px;
    transition: all 0.3s ease;
}

.dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    display: flex;
    flex-direction: column;
    list-style: none;
    min-width: 200px;
    padding: 0.4rem 0;
    border-radius: 4px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    background: #fff;
    z-index: 1001;
    gap: 0;
}
```

All three rules are equal-specificity to ours (0,2,1 for `.has-dropdown details`, 0,1,0 for `.dropdown`). Without `!important`, source order decides — and since the inline block loads after `main.css`, the inline wins. With `!important` flags on our flat-list rules, we win regardless.

(The page also has 2 `<details>` elements and the `has-dropdown` markup, confirming the dropdown UI is in the rendered page — what we're styling is real.)

---

## 4. Files Touched

| File | Action |
|---|---|
| `torah-weave/Admin/Assets/CSS/main.css` | Flat-list block expanded with `!important` flags (lines 3876–3924). Same structure; same behavior; just guaranteed cascade win. |
| `_pilot/mobile-flat-nav-important.md` | This report |

No template changes. No JavaScript changes. The preview file `_pilot/hebrew-nav-render-preview.html` is unchanged — it links to `main.css` via absolute URL and picks up the new rules automatically.

---

## 5. What's Different Now on Deployed Pages

On any page that loads `main.css` (which is all of them):

- **Desktop** (≥768 px viewport): no change. The `@media (hover: hover) and (pointer: fine)` block (line 3845, unchanged) drives hover dropdowns exactly as before.
- **Mobile** (<768 px viewport): the flat-list rules now beat the DWT-inline CSS even though the DWT-inline CSS is later in source order. `<details>` collapses to `display: contents`, summary becomes non-tappable, the `<ul.dropdown>` is always visible and full-width with indented items. Same flat-list layout as on new-template pages.

This is the same behavioral pivot as the previous task; this commit just makes it actually take effect on DWT-attached pages.
