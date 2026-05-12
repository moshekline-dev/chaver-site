# Hebrew Chrome — קוד הצבעים Links Added

**Date:** 2026-05-11
**Scope:** Add the `קוד הצבעים` (Color Code) link in three places in `_templates/Academic-Content-HE.html` — the תורה nav dropdown, the משנה nav dropdown, and the המשנה כדרכה footer section. All three point at the same destination: `/torah-weave/hebrew-color-code-guide/` (placeholder until Moshe transfers the guide).
**Status:** Template updated. Preview regenerated. Full chrome link statuses re-checked. **Not committed.**

---

## 1. Three Additive Diffs

### Diff A — תורה dropdown (was 2 items → now 3)

```diff
  <li class="has-dropdown">
      <details>
          <summary>&#1514;&#1493;&#1512;&#1492;</summary>
          <ul class="dropdown">
              <li><a href="/Torah-New/Hebrew/Hebrew%20Torah%20Portal.htm">&#1513;&#1506;&#1512; &#1492;&#1514;&#1493;&#1512;&#1492;</a></li>
              <li><a href="/torah-weave/hebrew-full-torah-map/">&#1502;&#1508;&#1514; &#1492;&#1514;&#1493;&#1512;&#1492;</a></li>
+             <li><a href="/torah-weave/hebrew-color-code-guide/">&#1511;&#1493;&#1491; &#1492;&#1510;&#1489;&#1506;&#1497;&#1501;</a></li>
          </ul>
      </details>
  </li>
```

### Diff B — משנה dropdown (was 3 items → now 4)

```diff
  <li class="has-dropdown">
      <details>
          <summary>&#1502;&#1513;&#1504;&#1492;</summary>
          <ul class="dropdown">
              <li><a href="/Mishnah-New/Hebrew/Mishnah%20Portal.htm">&#1513;&#1506;&#1512; &#1492;&#1502;&#1513;&#1504;&#1492;</a></li>
              <li><a href="/Mishnah-New/Hebrew/Articles/MAVO.htm">&#1502;&#1489;&#1493;&#1488;</a></li>
              <li><a href="/Mishnah-New/Hebrew/Text/mishnah-pdf">PDF &#1492;&#1502;&#1513;&#1504;&#1492;</a></li>
+             <li><a href="/torah-weave/hebrew-color-code-guide/">&#1511;&#1493;&#1491; &#1492;&#1510;&#1489;&#1506;&#1497;&#1501;</a></li>
          </ul>
      </details>
  </li>
```

### Diff C — footer המשנה כדרכה section (was 2 items → now 3)

```diff
  <div class="footer-section">
      <h3>&#1492;&#1502;&#1513;&#1504;&#1492; &#1499;&#1491;&#1512;&#1499;&#1492;</h3>
      <ul>
          <li><a href="/Mishnah-New/Hebrew/Mishnah%20Portal.htm">&#1508;&#1493;&#1512;&#1496;&#1500; &#1492;&#1502;&#1513;&#1504;&#1492;</a></li>
          <li><a href="/Mishnah-New/Hebrew/Text/The%20Structured%20Mishnah.pdf">PDF &#1513;&#1500; &#1492;&#1502;&#1513;&#1504;&#1492;</a></li>
+         <li><a href="/torah-weave/hebrew-color-code-guide/">&#1511;&#1493;&#1491; &#1492;&#1510;&#1489;&#1506;&#1497;&#1501;</a></li>
      </ul>
  </div>
```

All three new items use the exact same destination URL and the exact same Hebrew-entity-encoded label (`קוד הצבעים`). Same convention as the rest of the file.

---

## 2. Shape After the Changes

Programmatic counts from the regenerated preview (`_pilot/hebrew-nav-render-preview.html`, 14,352 bytes, no unresolved `{{ region: ... }}`):

**Nav**

| Dropdown | Items | Counts color-code? |
|---|---|---|
| תורה | **3** | ✓ |
| משנה | **4** | ✓ |
| נתונים | **2** | – |

Top-level nav items unchanged at **6** (דף הבית, תורה ▾, משנה ▾, נתונים ▾, צור קשר, English).

**Footer**

| Section | Items | Counts color-code? |
|---|---|---|
| מפות תורה | 5 | – |
| המשנה כדרכה | **3** | ✓ |
| מחקר | 3 | – |
| קשר | 3 | – |

`<html lang="he" dir="rtl">` still on line 2. No other parts of the template touched.

**Color-code URL count across chrome:** `2` in nav + `1` in footer = **3 total**, all pointing at `/torah-weave/hebrew-color-code-guide/`.

---

## 3. HTTP Status — Every Hebrew Chrome Link

Checked over HTTPS against `https://chaver.com/` on 2026-05-11.

### Nav (10 destinations)

| # | Where | Label | Destination | Status |
|---|---|---|---|---|
| 1 | top | דף הבית | `/hebrew%20index.html` | **200** |
| 2 | תורה ▾ | שער התורה | `/Torah-New/Hebrew/Hebrew%20Torah%20Portal.htm` | **200** |
| 3 | תורה ▾ | מפת התורה | `/torah-weave/hebrew-full-torah-map/` | **200** |
| 4 | תורה ▾ | **קוד הצבעים** | `/torah-weave/hebrew-color-code-guide/` | **404** ⚠ *(new placeholder)* |
| 5 | משנה ▾ | שער המשנה | `/Mishnah-New/Hebrew/Mishnah%20Portal.htm` | **404** ⚠ *(existing placeholder)* |
| 6 | משנה ▾ | מבוא | `/Mishnah-New/Hebrew/Articles/MAVO.htm` | **200** |
| 7 | משנה ▾ | PDF המשנה | `/Mishnah-New/Hebrew/Text/mishnah-pdf` | **200** |
| 8 | משנה ▾ | **קוד הצבעים** | `/torah-weave/hebrew-color-code-guide/` | **404** ⚠ *(same as #4)* |
| 9 | נתונים ▾ | התורה | `/torah-weave/data/` | **200** |
| 10 | נתונים ▾ | המשנה | `/Mishnah-New/Hebrew/Text/mishnah-data` | **200** |
| 11 | top | צור קשר | `/General/Contact.htm` | **200** |
| 12 | top | English | `/` | **200** |

(12 destinations after counting the second קוד הצבעים reference. The 3 dropdown `<summary>` openers aren't links.)

### Footer (13 destinations)

| Section | Label | Destination | Status |
|---|---|---|---|
| מפות תורה | בראשית | `/woven-torah/language/he/hebrew_pages/hebrew-map-of-genesis/` | **200** |
| מפות תורה | שמות | `/woven-torah/language/he/hebrew_pages/hebrew-map-of-exodus/` | **200** |
| מפות תורה | ויקרא | `/woven-torah/language/he/hebrew_pages/hebrew-map-of-leviticus/` | **200** |
| מפות תורה | במדבר | `/woven-torah/language/he/hebrew_pages/hebrew-map-of-numbers/` | **200** |
| מפות תורה | דברים | `/woven-torah/language/he/hebrew_pages/hebrew-map-of-deuteronomy/` | **200** |
| המשנה כדרכה | פורטל המשנה | `/Mishnah-New/Hebrew/Mishnah%20Portal.htm` | **404** ⚠ *(same placeholder as nav #5)* |
| המשנה כדרכה | PDF של המשנה | `/Mishnah-New/Hebrew/Text/The%20Structured%20Mishnah.pdf` | **200** |
| המשנה כדרכה | **קוד הצבעים** | `/torah-weave/hebrew-color-code-guide/` | **404** ⚠ *(same placeholder as nav #4/#8)* |
| מחקר | Academia.edu | `https://independent.academia.edu/MosheKline` | 403 *(anti-bot; works in browsers)* |
| מחקר | Structure is Theology | `/Torah/Structure%20is%20Theology%20Published%20Version.pdf` | **200** |
| מחקר | מאמרים | `/woven-torah/research-articles/` | **200** |
| קשר | צור קשר | `/General/Contact.htm` | **200** |
| קשר | Academia.edu (top 1%) | `https://independent.academia.edu/MosheKline` | 403 *(same URL as Section מחקר)* |
| קשר | English Site | `/` | **200** |

### Real broken-link picture (deduped)

Two distinct destinations are unbuilt placeholders, and they account for all of the 404s in the chrome. Each will resolve multiple chrome links the moment the page exists:

| Placeholder URL | Affects |
|---|---|
| `/torah-weave/hebrew-color-code-guide/` | 3 chrome links (תורה nav, משנה nav, footer המשנה כדרכה) |
| `/Mishnah-New/Hebrew/Mishnah%20Portal.htm` | 2 chrome links (משנה nav, footer המשנה כדרכה) |

Everything else on chaver.com returns 200. Academia's 403 is anti-scraping, not a broken link.

---

## 4. Visual Verification

Open `_pilot/hebrew-nav-render-preview.html` in a browser. Expected:

- **תורה** dropdown opens to **3** items (שער התורה, מפת התורה, קוד הצבעים).
- **משנה** dropdown opens to **4** items (שער המשנה, מבוא, PDF המשנה, קוד הצבעים).
- **נתונים** dropdown remains at **2** items.
- Scrolling to the footer, the **המשנה כדרכה** section shows **3** items (פורטל המשנה, PDF של המשנה, קוד הצבעים).
- Hebrew text renders as Hebrew letters in RTL flow throughout.

---

## Files Touched

| File | Action |
|---|---|
| `_templates/Academic-Content-HE.html` | Three additive edits: one new `<li>` in each of the תורה dropdown, משנה dropdown, and footer המשנה כדרכה section. No other lines changed. |
| `_pilot/hebrew-nav-render-preview.html` | Regenerated from updated template (14,352 bytes) |
| `_pilot/hebrew-color-code-links.md` | This report |
