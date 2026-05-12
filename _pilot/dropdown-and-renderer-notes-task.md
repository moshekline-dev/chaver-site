# Dropdown Hover Behavior + Subdivision Rendering Note

**Date:** 2026-05-12
**Status:** CSS applied to `main.css`. Close-others JS applied to both templates. HE template separately **repaired** — was truncated. Subdivision design note created. **Not committed.** ⚠ Visual verification on the deployed (or locally-served) site still needed — see "Anomalies" below.

---

## ⚠ Anomaly Found and Repaired — HE Template Was Truncated

While attempting to add the close-others JS to `_templates/Academic-Content-HE.html`, I discovered the file was cut off mid-comment with no `<script>` tag, no `toggleMenu()` function, no `{{ region: page-scripts }}`, no `</body>`, and no `</html>`.

| Snapshot | Bytes | State |
|---|---:|---|
| `_templates/Academic-Content-HE.html` in working tree (before this repair) | 13,900 | Truncated; trailing bytes are NULL (`\x00`) padding |
| Same file at `HEAD` | 13,429 | Truncated (slightly shorter, no NULL padding) — already deployed |
| EN counterpart `_templates/Academic-Content-EN.html` | ~14,800 | Complete (this task's edit added the close-others JS cleanly) |
| HE template after this repair | 15,112 | Complete; matches the EN template's structure |

**What this means in practice:** the HE template has been deployed for a while with no mobile-menu script (the hamburger `toggleMenu()` is missing) and with technically-invalid HTML (no closing tags). Browsers are forgiving so pages still render, but the hamburger menu on Hebrew pages cannot have been opening. Worth a manual test on a real Hebrew page to confirm whether mobile users have been hitting a dead hamburger button.

**Repair done:**

- Stripped the trailing NULL bytes from the working tree copy.
- Truncated the file cleanly at the end of `</footer>` (the last verifiably-intact element).
- Appended the full tail — the mobile-menu script (`toggleMenu`, click-outside), the new close-others handler, `</script>`, `{{ region: page-scripts }}`, `</body>`, `</html>` — matching the EN template structure exactly.
- Preserved CRLF line endings throughout.

Post-repair sanity checks: `file` reports "HTML document", 0 NULL bytes, 1 occurrence each of `function toggleMenu`, the close-others comment, `{{ region: page-scripts }}`, `</body>`, and `</html>`.

---

## 1. CSS Change in `main.css`

Appended at the end of `torah-weave/Admin/Assets/CSS/main.css`, just before the `END OF MAIN.CSS` banner. **Important context:** the existing visual styles for `.has-dropdown` and `.dropdown` are not in `main.css` — they live in each template's inline `<style>` block (the "CRITICAL DWT LAYOUT STYLES" section). The task description assumed they'd be in `main.css`. The new behavior block was added to `main.css` anyway per the task spec; the `:hover` selectors have higher specificity than the inline `.dropdown` selectors, so the cascade works regardless of source order.

```css
/* ====================================
   NAV DROPDOWN HOVER BEHAVIOR
   Applies to both English and Hebrew templates.
   Visual rules for .has-dropdown / .dropdown live in each
   template's inline <style> block (DWT layout styles).
   This file adds open/close BEHAVIOR only.
   ==================================== */

@media (hover: hover) and (pointer: fine) {
    /* Desktop / pointer-capable devices: hover-to-open */

    .has-dropdown summary {
        list-style: none;
        cursor: pointer;
    }
    .has-dropdown summary::-webkit-details-marker {
        display: none;
    }

    /* Force the dropdown visible on hover, regardless of <details> open state */
    .has-dropdown:hover .dropdown {
        display: block;
    }

    /* Hide the dropdown when not hovered, even if <details> was clicked open */
    .has-dropdown:not(:hover) .dropdown {
        display: none;
    }

    .has-dropdown summary {
        pointer-events: auto;
    }
}

@media (hover: none) {
    /* Touch devices keep the native <details> click-to-open/close behavior. */
    /* No additional rules needed — browser default. */
}
```

---

## 2. JS Change in Both Templates

Appended to the existing `<script>` block at the bottom of each template, right after the click-outside handler. Identical JS in both files.

```diff
              menu.classList.remove('show');
          }
      });
+
+        // Close other nav dropdowns when one is opened (accordion behavior)
+        document.addEventListener('DOMContentLoaded', function() {
+            var allDetails = document.querySelectorAll('.has-dropdown details');
+            allDetails.forEach(function(d) {
+                d.addEventListener('toggle', function() {
+                    if (this.open) {
+                        allDetails.forEach(function(other) {
+                            if (other !== d) { other.open = false; }
+                        });
+                    }
+                });
+            });
+        });
      </script>
```

Applied to:
- `_templates/Academic-Content-EN.html` (clean Edit on existing well-formed file).
- `_templates/Academic-Content-HE.html` (included as part of the tail reconstruction described above).

---

## 3. Verification Status

### Programmatic checks — passing

| Check | Result |
|---|---|
| HE template integrity (`file` says HTML, no NULLs) | ✓ |
| `toggleMenu` defined once in HE template | ✓ |
| Close-others handler present once in HE template | ✓ |
| `{{ region: page-scripts }}` placeholder restored | ✓ |
| `</body></html>` closing tags restored | ✓ |
| EN template close-others handler present | ✓ |
| `main.css` ends with `END OF MAIN.CSS` banner after new block | ✓ |
| Preview regenerated, no unresolved `{{ region: ... }}` markers | ✓ |

### Browser behavior — NOT verified by me

The `(hover: hover) and (pointer: fine)` media query and the `:hover` rules require an actual browser test. I have not opened the preview in a real browser yet.

Two caveats Moshe should verify directly:

1. **`<details>` content visibility on closed elements.** When `<details>` is *not* open, browsers natively hide its non-`<summary>` children. Modern Chromium and Firefox respect `display` overrides on those children (so `.has-dropdown:hover .dropdown { display: block }` *should* show the dropdown on hover even if `<details>` is "closed"), but the behavior has historical edge cases. If hover opens visually but the dropdown items are still invisible, the fix is to add a JS handler that sets `details.open = true` on `mouseenter` and `false` on `mouseleave`. I can add that if it turns out to be needed.

2. **Local file:// preview won't load `main.css`.** Opening `_pilot/hebrew-nav-render-preview.html` directly via `file://` will fail to resolve `/torah-weave/Admin/Assets/CSS/main.css` (an absolute path served by Cloudflare Pages in production). The preview is only meaningful when served from a local web server (or when the file is opened from inside a checkout where the relative tree is served). Visual hover verification needs the site running.

The task spec said "If anything doesn't work as expected, STOP and report. Don't push the changes through if hover is breaking in unexpected ways." Per that guidance: I've stopped before claiming the visual behavior works, and the changes are in working-tree state for review.

---

## 4. Subdivision Rendering Note

Created `_pilot/renderer-design-notes.md` with the **Subdivision Rendering** decision section, plus a small "Open Decisions" appendix capturing related questions for when the renderer is built (mishnah-number prefix handling, header-row chapter treatment, sotah_9 URL split, and the unresolved choice between "empty trailing rows" vs `rowspan` for uneven-subdivision rows).

The file is fresh — `_pilot/renderer-design-notes.md` did not previously exist.

---

## 5. Files Touched

| File | Action |
|---|---|
| `torah-weave/Admin/Assets/CSS/main.css` | Appended `@media (hover: hover)` block before the `END OF MAIN.CSS` banner |
| `_templates/Academic-Content-EN.html` | Added close-others JS to the existing `<script>` block (clean Edit) |
| `_templates/Academic-Content-HE.html` | **Repaired truncation** + added close-others JS (rebuilt the file's tail from the `</footer>` closing tag onwards) |
| `_pilot/hebrew-nav-render-preview.html` | Regenerated from the repaired HE template (15,529 bytes; no unresolved regions) |
| `_pilot/renderer-design-notes.md` | New — subdivision rendering decision + open questions |
| `_pilot/dropdown-and-renderer-notes-task.md` | This report |

---

## 6. Suggested Next Step

Have Moshe (a) deploy the repaired HE template to a Cloudflare preview branch (or run a local server) and (b) test the hover behavior on the live nav. If the dropdowns don't visually open on hover despite the CSS being applied, the small JS fallback ("force `details.open` on mouseenter") is the fix and can be added in a 5-minute follow-up.
