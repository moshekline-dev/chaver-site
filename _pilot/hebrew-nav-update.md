# Hebrew Nav Update — נתונים → Dropdown

**Date:** 2026-05-11
**Scope:** Convert the single **נתונים** link in `_templates/Academic-Content-HE.html` to a two-item dropdown (**התורה** / **המשנה**). Mirrors the existing **משנה** dropdown pattern.
**Status:** Template updated. Preview regenerated. **Not committed.**

---

## 1. Before / After — `נתונים` Block Only

### BEFORE (single item)

```html
<li><a href="/torah-weave/data/">&#1504;&#1514;&#1493;&#1504;&#1497;&#1501;</a></li>
```

### AFTER (dropdown with two items)

```html
<li class="has-dropdown">
    <details>
        <summary>&#1504;&#1514;&#1493;&#1504;&#1497;&#1501;</summary>
        <ul class="dropdown">
            <li><a href="/torah-weave/data/">&#1492;&#1514;&#1493;&#1512;&#1492;</a></li>
            <li><a href="/Mishnah-New/Hebrew/Text/mishnah-data">&#1492;&#1502;&#1513;&#1504;&#1492;</a></li>
        </ul>
    </details>
</li>
```

### Label decoding

| Code | Decoded | Meaning |
|---|---|---|
| `&#1504;&#1514;&#1493;&#1504;&#1497;&#1501;` | נתונים | Data |
| `&#1492;&#1514;&#1493;&#1512;&#1492;` | התורה | (the) Torah |
| `&#1492;&#1502;&#1513;&#1504;&#1492;` | המשנה | (the) Mishnah |

### Destination check

| Path | Filesystem |
|---|---|
| `/torah-weave/data/` | `torah-weave/data/index.html` ✓ |
| `/Mishnah-New/Hebrew/Text/mishnah-data` | `Mishnah-New/Hebrew/Text/mishnah-data.html` ✓ (clean URL resolves via Cloudflare Pages, same pattern as the existing `mishnah-pdf` link in the משנה dropdown) |

---

## 2. Preview Regenerated

`_pilot/hebrew-nav-render-preview.html` rebuilt from the updated template (14,183 bytes, no unresolved `{{ region: ... }}` markers).

Programmatic shape check on the regenerated preview:

- Top-level nav items: **5** (בית, משנה ▾, מפת התורה, נתונים ▾, English)
- `has-dropdown` markers: **2** (משנה, נתונים)
- Total `<li>` inside `#nav-menu`: 10 (5 top-level + 3 משנה sub-items + 2 נתונים sub-items)
- `<html lang="he" dir="rtl">` still on line 2
- `toggleMenu()` script unchanged
- No new CSS classes; reuses `has-dropdown`, `dropdown`, `details`, `summary` already in main.css

To verify visually, open `_pilot/hebrew-nav-render-preview.html` and confirm: both **משנה** and **נתונים** open dropdowns; the נתונים dropdown shows התורה and המשנה (in RTL order, with התורה appearing first on the right).

---

## 3. Note

This change is strictly the נתונים line replacement. No other nav items were modified. The 5-item top-level structure from the previous task is preserved; only the data link gained a child menu.

The Mishnah data page (`/Mishnah-New/Hebrew/Text/mishnah-data`) is now reachable from the Hebrew nav for the first time.

---

## Out of Scope (deferred)

- Updating the Mishnah data page's content (e.g., the "524 chapters / 2,276 markers" → "525 / 10,405" stats update for rev9) — separate task.
- Fixing the `<html lang="en">` on either data page — separate task.
- Building the שער המשנה portal page — still pending from prior task.

---

## Files Touched

| File | Action |
|---|---|
| `_templates/Academic-Content-HE.html` | נתונים `<li>` replaced with `has-dropdown` block (now lines 328–336) |
| `_pilot/hebrew-nav-render-preview.html` | Regenerated from updated template |
| `_pilot/hebrew-nav-update.md` | This report |
