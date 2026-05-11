# Hebrew Nav Refinement — Three Focused Changes

**Date:** 2026-05-11
**Scope:** `_templates/Academic-Content-HE.html` — three label/structure refinements derived from studying the legacy `hebrew.dwt` conventions.
**Status:** Template updated. Preview regenerated. All link destinations checked over HTTPS. **Not committed.**

---

## 1. The Three Changes (Diff)

### Change A — בית → דף הבית

```diff
- <li><a href="/hebrew%20index.html">&#1489;&#1497;&#1514;</a></li>
+ <li><a href="/hebrew%20index.html">&#1491;&#1507; &#1492;&#1489;&#1497;&#1514;</a></li>
```

Destination unchanged. Label moves to the formal Hebrew convention used in `Dynamic Web Templates/hebrew.dwt`.

### Change B — flat מפת התורה → תורה dropdown

```diff
- <li><a href="/torah-weave/hebrew-full-torah-map/">&#1502;&#1508;&#1514; &#1492;&#1514;&#1493;&#1512;&#1492;</a></li>
+ <li class="has-dropdown">
+     <details>
+         <summary>&#1514;&#1493;&#1512;&#1492;</summary>
+         <ul class="dropdown">
+             <li><a href="/Torah-New/Hebrew/Hebrew%20Torah%20Portal.htm">&#1513;&#1506;&#1512; &#1492;&#1514;&#1493;&#1512;&#1492;</a></li>
+             <li><a href="/torah-weave/hebrew-full-torah-map/">&#1502;&#1508;&#1514; &#1492;&#1514;&#1493;&#1512;&#1492;</a></li>
+         </ul>
+     </details>
+ </li>
```

The תורה dropdown now exposes both the Torah Portal (newly surfaced) and the Torah Map. The portal page was missed in the original inventory because the filename includes "Hebrew" (`Hebrew Torah Portal.htm`), not just "Torah Portal".

Note on placement: the תורה dropdown is positioned **before משנה** so the Hebrew nav reads, in RTL order from right to left: home → Torah → Mishnah → Data → Contact → English — same conceptual order as the English nav and the legacy `hebrew.dwt`.

### Change C — add צור קשר before English

```diff
+ <li><a href="/General/Contact.htm">&#1510;&#1493;&#1512; &#1511;&#1513;&#1512;</a></li>
  <li><a href="/">English</a></li>
```

Reuses the existing English `/General/Contact.htm` (no separate Hebrew Contact page; the page itself contains both languages).

---

## 2. Final Nav Shape

Programmatic shape check on `_pilot/hebrew-nav-render-preview.html` (regenerated, 14,088 bytes, no unresolved `{{ region: ... }}` markers):

- **Top-level `<li>`: 6** ✓ (דף הבית, תורה ▾, משנה ▾, נתונים ▾, צור קשר, English)
- **`has-dropdown` markers: 3** ✓ (תורה, משנה, נתונים)
- **Total `<li>` inside `#nav-menu`: 13** (6 top-level + 2 + 3 + 2 dropdown items)
- **Total `<a href=>`: 10** (3 top-level non-dropdown links + 7 dropdown items)

RTL: `<html lang="he" dir="rtl">` is still on line 2 of the template, and the CSS classes (`site-header`, `main-nav`, `menu-toggle`, `nav-menu`, `has-dropdown`, `dropdown`) are all preserved from main.css. No CSS changes needed.

---

## 3. HTTP Status of Every Link

Checked over HTTPS against `https://chaver.com/` on 2026-05-11. The 6 top-level items split into 3 dropdown summaries (not links) plus 3 direct links; the 3 dropdowns add 7 destination links — 10 actual destinations total.

| # | Label | Destination | Status |
|---|---|---|---|
| 1 | דף הבית | `/hebrew%20index.html` | **200** |
| — | תורה (dropdown summary, no link) | — | — |
| 2 | ↳ שער התורה | `/Torah-New/Hebrew/Hebrew%20Torah%20Portal.htm` | **200** |
| 3 | ↳ מפת התורה | `/torah-weave/hebrew-full-torah-map/` | **200** |
| — | משנה (dropdown summary, no link) | — | — |
| 4 | ↳ שער המשנה | `/Mishnah-New/Hebrew/Mishnah%20Portal.htm` | **404** *(expected — placeholder)* |
| 5 | ↳ מבוא | `/Mishnah-New/Hebrew/Articles/MAVO.htm` | **200** |
| 6 | ↳ PDF המשנה | `/Mishnah-New/Hebrew/Text/mishnah-pdf` | **200** |
| — | נתונים (dropdown summary, no link) | — | — |
| 7 | ↳ התורה | `/torah-weave/data/` | **200** |
| 8 | ↳ המשנה | `/Mishnah-New/Hebrew/Text/mishnah-data` | **200** |
| 9 | צור קשר | `/General/Contact.htm` | **200** |
| 10 | English | `/` | **200** |

The שער המשנה 404 is the same placeholder noted in the first task — the Hebrew Mishnah Portal page itself is a separate follow-up.

(The task spec mentions "11 nav links" — counting all clickable elements including the 3 `<summary>` dropdown openers gives 13; counting only the destination URLs gives 10. I've listed all 10 destinations above.)

---

## 4. Visual Verification

Open `_pilot/hebrew-nav-render-preview.html` in a browser. Expected:

- 6 top-level items flow right-to-left: דף הבית on the right edge, English on the left.
- Three items show a small ▾ arrow (תורה, משנה, נתונים) and open dropdowns when clicked.
- Hebrew labels render as Hebrew text (not numeric entities, not mojibake).
- Resize to narrow width → hamburger button appears and toggles the nav.

---

## 5. Other Notes

- Hebrew labels remain encoded as numeric HTML entities for consistency with the rest of the template (same convention as the original "עברית" link encoding).
- No other content of the template was modified — head, body wrappers, footer, `toggleMenu()` script, and CSS block are all unchanged.
- The legacy hebrew.dwt-bound pages (e.g., MAVO) will not pick up this nav until they're migrated to `Academic-Content-HE` — out of scope here.

---

## Files Touched

| File | Action |
|---|---|
| `_templates/Academic-Content-HE.html` | Nav block refined (now lines 312–344 of current file) |
| `_pilot/hebrew-nav-render-preview.html` | Regenerated from updated template |
| `_pilot/hebrew-nav-refinement.md` | This report |
