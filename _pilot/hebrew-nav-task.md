# Hebrew Navigation Replacement — Task Report

**Date:** 2026-05-11
**Scope:** Replace English-style nav in `_templates/Academic-Content-HE.html` with Hebrew-appropriate nav (5 top-level items, one with dropdown).
**Status:** Template updated. Render preview generated. **Not committed.**

---

## 1. Before / After — Nav Block in `_templates/Academic-Content-HE.html`

The file's nav block (lines 312–350 of the original) was byte-identical to the English template's nav: 8 top-level items including "Home," a Torah dropdown, an Insights dropdown of 10 English insights articles, "Mishnah," "The Method," "Data," "About Moshe Kline," and a single "עברית" toggle to the Hebrew home. This confirmed the diagnosis that Hebrew pages were inheriting English chrome.

### BEFORE (original lines 312–350)

```html
<header class="site-header">
    <nav class="main-nav">
        <button class="menu-toggle" onclick="toggleMenu()" aria-label="Toggle navigation">&#9776;</button>
       <ul id="nav-menu">
<li><a href="/">Home</a></li>
<li class="has-dropdown">
    <details>
        <summary>Torah</summary>
        <ul class="dropdown">
            <li><a href="/Torah-New/English/Torah%20Portal.htm">Torah Portal</a></li>
            <li><a href="/torah-weave/commentary.html">Commentary</a></li>
            <li><a href="/woven-torah/full-torah-map-2/index.html">Full Torah Map</a></li>
        </ul>
    </details>
</li>
<li class="has-dropdown">
    <details>
        <summary>Insights</summary>
        <ul class="dropdown">
            <li><a href="/torah-weave/bible-contradictions-explained.html">Bible Contradictions Explained</a></li>
            <li><a href="/torah-weave/yhwh-and-elohim-two-names.html">YHWH and Elohim: Two Names</a></li>
            <li><a href="/torah-weave/six-days-of-creation-picture.html">The Six Days Are a Picture</a></li>
            <li><a href="/torah-weave/cain-and-abel-two-fathers.html">Why Was Cain's Offering Rejected?</a></li>
            <li><a href="/torah-weave/ten-commandments-two-tablets.html">Why Two Tablets?</a></li>
            <li><a href="/torah-weave/leviticus-19-ark-at-the-center.html">The Ark at the Center</a></li>
            <li><a href="/torah-weave/ten-plagues-creation-in-reverse.html">Plagues: Creation in Reverse</a></li>
            <li><a href="/torah-weave/book-of-numbers-camp-map.html">Numbers: Map of the Camp</a></li>
            <li><a href="/torah-weave/who-wrote-the-bible-theories-compared.html">Who Wrote the Bible?</a></li>
            <li><a href="/torah-weave/documentary-hypothesis-alternative.html">Beyond JEDP</a></li>
        </ul>
    </details>
</li>
<li><a href="/Mishnah/TheMishnah.htm">Mishnah</a></li>
<li><a href="/torah-weave/Woven-Torah-Method.html">The Method</a></li>
<li><a href="/torah-weave/data/">Data</a></li>
<li><a href="/about-Moshe-Kline.html">About Moshe Kline</a></li>
<li><a href="/hebrew%20index.html">&#1506;&#1489;&#1512;&#1497;&#1514;</a></li>
</ul>        </nav>
</header>
```

### AFTER (current lines 312–332)

```html
<header class="site-header">
    <nav class="main-nav">
        <button class="menu-toggle" onclick="toggleMenu()" aria-label="&#1508;&#1514;&#1497;&#1495;&#1514; &#1514;&#1508;&#1512;&#1497;&#1496;">&#9776;</button>
        <ul id="nav-menu">
            <li><a href="/hebrew%20index.html">&#1489;&#1497;&#1514;</a></li>
            <li class="has-dropdown">
                <details>
                    <summary>&#1502;&#1513;&#1504;&#1492;</summary>
                    <ul class="dropdown">
                        <li><a href="/Mishnah-New/Hebrew/Mishnah%20Portal.htm">&#1513;&#1506;&#1512; &#1492;&#1502;&#1513;&#1504;&#1492;</a></li>
                        <li><a href="/Mishnah-New/Hebrew/Articles/MAVO.htm">&#1502;&#1489;&#1493;&#1488;</a></li>
                        <li><a href="/Mishnah-New/Hebrew/Text/mishnah-pdf">PDF &#1492;&#1502;&#1513;&#1504;&#1492;</a></li>
                    </ul>
                </details>
            </li>
            <li><a href="/torah-weave/hebrew-full-torah-map/">&#1502;&#1508;&#1514; &#1492;&#1514;&#1493;&#1512;&#1492;</a></li>
            <li><a href="/torah-weave/data/">&#1504;&#1514;&#1493;&#1504;&#1497;&#1501;</a></li>
            <li><a href="/">English</a></li>
        </ul>
    </nav>
</header>
```

### Notes on encoding choice

- The Hebrew labels were encoded as numeric HTML entities (e.g., `&#1489;&#1497;&#1514;` for **בית**) to match the existing convention in the same file (the original "עברית" link was `&#1506;&#1489;&#1512;&#1497;&#1514;`). Functionally identical to literal UTF-8 Hebrew under `<meta charset="UTF-8">`, but more robust through any editor that might normalize encodings.
- `toggleMenu()` and the dropdown CSS classes are untouched — same script block at the bottom of the template handles the hamburger.
- `aria-label` translated to **פתיחת תפריט**.
- The rest of the template (head, GA, footer, script block) is unmodified.

### Verification of decoded labels

| Code | Decoded | Meaning |
|---|---|---|
| `&#1489;&#1497;&#1514;` | בית | Home |
| `&#1502;&#1513;&#1504;&#1492;` | משנה | Mishnah |
| `&#1513;&#1506;&#1512; &#1492;&#1502;&#1513;&#1504;&#1492;` | שער המשנה | Mishnah Portal |
| `&#1502;&#1489;&#1493;&#1488;` | מבוא | Introduction |
| `&#1492;&#1502;&#1513;&#1504;&#1492;` | המשנה | (the) Mishnah |
| `&#1502;&#1508;&#1514; &#1492;&#1514;&#1493;&#1512;&#1492;` | מפת התורה | Map of the Torah |
| `&#1504;&#1514;&#1493;&#1504;&#1497;&#1501;` | נתונים | Data |
| `&#1508;&#1514;&#1497;&#1495;&#1514; &#1514;&#1508;&#1512;&#1497;&#1496;` | פתיחת תפריט | Open menu |

---

## 2. Pages Using the Hebrew Template (blast radius)

### Exact match: `<html lang="he" dir="rtl">`

**Total: 5 files** (1 is the template itself; **4 deployed pages** would pick up the new nav).

```
_templates/Academic-Content-HE.html        ← the template (just edited)
hebrew index.html                          ← Hebrew home page (out of scope per task)
Mishnah-New/Hebrew/Text/Mishnah_Index.html
pilot/megillah-perek-1-he.html
pilot/megillah-perek-1-marked.html
```

### Caveat: the legacy Hebrew corpus is larger but does not match the template signature

A looser grep for `lang="he"` anywhere in the file finds **362 files**. The 357 files with `lang="he"` somewhere but **not** `<html lang="he" dir="rtl">` fall into two categories:

1. Pages whose root `<html>` declares `lang="en"` despite serving Hebrew content (legacy DWT artifacts — most of `Mishnah-New/Hebrew/Text/Seder.../*.htm` and most `woven-torah/language/he/...`).
2. English pages with inline `lang="he"` on isolated Hebrew quotation spans.

These pages have the English nav baked directly into their HTML body (not pulled from the template at render time), so the new Hebrew nav will not reach them until either (a) a build pipeline re-renders them from the template, or (b) each page is re-attached to the new template in Expression Web.

### Sample of 20 paths from the 357-file legacy set (first 5, middle 10, last 5)

```
Articles/Hebrew Articles.htm
Articles/Introduction to the Structured Mishnah.htm
Mishnah-New/Hebrew/Articles/TheWholeStructureDW.htm
Mishnah-New/Hebrew/Text/Seder Nezikin/Masechet Baba Kama/Masechet Baba Kama Perek 1.htm
Mishnah-New/Hebrew/Text/Seder Nezikin/Masechet Sanhedrin/Masechet Sanhedrin Perek 8.htm
woven-torah/language/he/hebrew_torah_units/exodus-unit-11/index.html
woven-torah/language/he/hebrew_torah_units/exodus-unit-12/index.html
woven-torah/language/he/hebrew_torah_units/exodus-unit-13/index.html
woven-torah/language/he/hebrew_torah_units/exodus-unit-14/index.html
woven-torah/language/he/hebrew_torah_units/exodus-unit-15/index.html
woven-torah/language/he/hebrew_torah_units/exodus-unit-16/index.html
woven-torah/language/he/hebrew_torah_units/exodus-unit-17/index.html
woven-torah/language/he/hebrew_torah_units/exodus-unit-18/index.html
woven-torah/language/he/hebrew_torah_units/exodus-unit-19/index.html
woven-torah/language/he/hebrew_torah_units/exodus-unit-2/index.html
woven-torah/torah_units/numbers-unit-6/index.html
woven-torah/torah_units/numbers-unit-7-2/index.html
woven-torah/torah_units/numbers-unit-7/index.html
woven-torah/torah_units/numbers-unit-8/index.html
woven-torah/torah_units/numbers-unit-9/index.html
```

(Migrating these to the HE template is a separate, larger task — well out of scope here.)

---

## 3. Rendering Confirmation

I generated a full render preview by substituting sample regions into the updated template scaffolding. The output is at:

`_pilot/hebrew-nav-render-preview.html` (14,063 bytes, no unresolved `{{ region: ... }}` markers)

Inline checks:

- `<html lang="he" dir="rtl">` present on line 2 (intact).
- All 5 top-level nav items render as `<li>` children of `#nav-menu`.
- `<details>`/`<summary>` dropdown structure under **משנה** contains the 3 expected items.
- `aria-label` on the hamburger is the Hebrew **פתיחת תפריט**.
- All existing CSS classes (`site-header`, `main-nav`, `menu-toggle`, `nav-menu`, `has-dropdown`, `dropdown`) preserved; no new classes introduced.
- `toggleMenu()` script unchanged at the bottom of the template.

**To verify visually:** open `_pilot/hebrew-nav-render-preview.html` in a browser. Expected behavior:

- Top nav flows right-to-left (בית at the right edge, English link at the left).
- Clicking **משנה** opens a dropdown with 3 items.
- On a narrow viewport, the hamburger button appears and toggles the nav.

---

## 4. Outstanding Follow-Up

The **שער המשנה** link points to `/Mishnah-New/Hebrew/Mishnah%20Portal.htm`, which **does not exist yet** in the repo:

```
/Mishnah-New/Hebrew/Mishnah Portal.htm  ← target (does not exist)
/Mishnah-New/English/Mishnah Portal.htm ← exists
```

This is expected per the task spec ("link can be added now, page built in follow-up"). Until the Hebrew Mishnah Portal page is created, this nav link will 404. Flagged as a separate task.

---

## 5. What Was Not Done (Out of Scope)

- No Hebrew Mishnah Portal page created.
- No legacy Hebrew pages migrated to the new template.
- No changes to `_templates/Academic-Content-EN.html` (English template).
- No changes to `hebrew index.html` (Hebrew home has its own layout).
- No git commit. No push. Moshe reviews the diff in GitHub Desktop before deploying.

---

## Files Touched

| File | Action |
|---|---|
| `_templates/Academic-Content-HE.html` | Nav block replaced (lines 312–332 of current file) |
| `_pilot/hebrew-nav-render-preview.html` | New — browser preview, not for deploy |
| `_pilot/hebrew-nav-task.md` | This report |
