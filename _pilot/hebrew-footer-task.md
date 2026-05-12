# Hebrew Footer for HE Template

**Date:** 2026-05-11
**Scope:** Replace the English 4-section footer in `_templates/Academic-Content-HE.html` with the Hebrew 4-section footer (verbatim from `/hebrew index.html`, with two intentional small changes noted below).
**Status:** Template updated. Preview regenerated. Every footer link checked over HTTPS. **Not committed.**

---

## 1. Before / After — Footer Block

### BEFORE (English footer — original lines 362–407)

```html
<footer class="site-footer">
    <div class="footer-container">
        <div class="footer-content">
            <div class="footer-section">
                <h4>Featured Articles</h4>
                <ul>
                    <li><a href="/The%20Esoteric%20Woven%20Torah,…pdf">The Esoteric Woven Torah</a></li>
                    <li><a href="/Torah/Structure%20is%20Theology%20Published%20Version.pdf">Structure is Theology (SBL)</a></li>
                    <li><a href="/Torah-New/English/Articles/The%20Editor%20was%20Nodding.pdf">"The Editor was Nodding"</a></li>
                    <li><a href="/Mishnah-New/English/Articles/Introduction%20to%20the%20Structured%20Mishnah.htm">Introduction to The Structured Mishnah</a></li>
                    <li><a href="/Torah-New/English/Articles/The%20Decalogue.html">The Decalogue</a></li>
                </ul>
            </div>
            <div class="footer-section">
                <h4>Full Texts</h4>
                <ul>
                    <li><a href="/Torah-New/English/Torah%20Portal.htm">Torah Portal</a></li>
                    <li><a href="/Mishnah/TheMishnah.htm">Mishnah Portal</a></li>
                    <li><a href="/Torah-New/English/Text/The%20Structured%20Torah%20(JPS%201917).pdf">Structured Torah (PDF)</a></li>
                    <li><a href="/Torah-New/Hebrew/Text/The%20Structured%20Torah.pdf">התורה כדרכה</a></li>
                    <li><a href="/Mishnah-New/Hebrew/Text/The%20Structured%20Mishnah.pdf">The Structured Mishnah PDF</a></li>
                </ul>
            </div>
            <div class="footer-section">
                <h4>Resources</h4>
                <ul>… 6 items including 3 YouTube links …</ul>
            </div>
            <div class="footer-section">
                <h4>About Moshe Kline</h4>
                <p>Graduate of St. John's College and Yeshiva University…</p>
                <p>The Woven Torah methodology has been independently validated…</p>
                <p><a href="/about-Moshe-Kline.html">Read more &rarr;</a></p>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&#169; 2026 Chaver.com. The Woven Texts Project.</p>
        </div>
    </div>
</footer>
```

### AFTER (Hebrew footer — current lines 362–402)

```html
<footer class="site-footer">
    <div class="footer-container">
        <div class="footer-content">
            <div class="footer-section">
                <h3>מפות תורה</h3>
                <ul>
                    <li><a href="/woven-torah/language/he/hebrew_pages/hebrew-map-of-genesis/">בראשית</a></li>
                    <li><a href="/woven-torah/language/he/hebrew_pages/hebrew-map-of-exodus/">שמות</a></li>
                    <li><a href="/woven-torah/language/he/hebrew_pages/hebrew-map-of-leviticus/">ויקרא</a></li>
                    <li><a href="/woven-torah/language/he/hebrew_pages/hebrew-map-of-numbers/">במדבר</a></li>
                    <li><a href="/woven-torah/language/he/hebrew_pages/hebrew-map-of-deuteronomy/">דברים</a></li>
                </ul>
            </div>
            <div class="footer-section">
                <h3>המשנה כדרכה</h3>
                <ul>
                    <li><a href="/Mishnah-New/Hebrew/Mishnah%20Portal.htm">פורטל המשנה</a></li>
                    <li><a href="/Mishnah-New/Hebrew/Text/The%20Structured%20Mishnah.pdf">PDF של המשנה</a></li>
                </ul>
            </div>
            <div class="footer-section">
                <h3>מחקר</h3>
                <ul>
                    <li><a href="https://independent.academia.edu/MosheKline" target="_blank">Academia.edu</a></li>
                    <li><a href="/Torah/Structure%20is%20Theology%20Published%20Version.pdf">Structure is Theology</a></li>
                    <li><a href="/woven-torah/research-articles/">מאמרים</a></li>
                </ul>
            </div>
            <div class="footer-section">
                <h3>קשר</h3>
                <ul>
                    <li><a href="/General/Contact.htm">צור קשר</a></li>
                    <li><a href="https://independent.academia.edu/MosheKline" target="_blank">Academia.edu (top 1%)</a></li>
                    <li><a href="/">English Site</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2026 Chaver.com. The Woven Texts Project.</p>
        </div>
    </div>
</footer>
```

(In the actual file, all Hebrew is encoded as numeric HTML entities — same convention as the rest of the template. Decoded labels are shown above for readability.)

---

## 2. Structural Notes

- **4 `<div class="footer-section">`** ✓
- **Heading level: `<h3>`** (the English footer used `<h4>`). This change comes from the verbatim source — `/hebrew index.html` uses `<h3>` for footer section headers. Confirm in the preview that the larger heading still looks right under main.css; if it doesn't, that's a styling tweak rather than a content fix.
- **13 `<a href=>` in the footer** (5 + 2 + 3 + 3).
- **Two intentional deviations from the home-page source**, both noted in the task spec:
  1. Copyright `&copy; 2026` (the home page footer shows 2025).
  2. פורטל המשנה points at `/Mishnah-New/Hebrew/Mishnah%20Portal.htm` (matching the nav's שער המשנה destination, currently a placeholder). The home page footer points the same label at the English portal.
- **No other parts of the template were touched.** Head, nav, body wrappers, `toggleMenu()` script, and the entire DWT region scaffolding (`{{ region: ... }}`) are unchanged.

---

## 3. Preview Regenerated

`_pilot/hebrew-nav-render-preview.html` rebuilt from the updated template (14,318 bytes; no unresolved `{{ region: ... }}` markers). The preview now exercises the full Hebrew chrome — nav at the top, footer at the bottom — over a Hebrew-language sample content block.

Programmatic shape checks pass:

- 6 top-level nav `<li>`, 3 dropdowns (תורה, משנה, נתונים) — unchanged from the previous task.
- 4 footer sections, 4 `<h3>`, 0 `<h4>`.
- Section headers decode to: **מפות תורה**, **המשנה כדרכה**, **מחקר**, **קשר**.
- `<html lang="he" dir="rtl">` still on line 2.

To verify visually, open `_pilot/hebrew-nav-render-preview.html` in a browser and scroll. Expected: Hebrew nav across the top, Hebrew chapter labels (בראשית, שמות, ויקרא, במדבר, דברים) flowing right-to-left in the first footer column, and English copyright line at the bottom.

---

## 4. HTTP Status of Every Footer Link

Checked over HTTPS against `https://chaver.com/` (and Academia for external) on 2026-05-11.

### Section 1 — מפות תורה

| Label | Destination | Status |
|---|---|---|
| בראשית | `/woven-torah/language/he/hebrew_pages/hebrew-map-of-genesis/` | **200** |
| שמות | `/woven-torah/language/he/hebrew_pages/hebrew-map-of-exodus/` | **200** |
| ויקרא | `/woven-torah/language/he/hebrew_pages/hebrew-map-of-leviticus/` | **200** |
| במדבר | `/woven-torah/language/he/hebrew_pages/hebrew-map-of-numbers/` | **200** |
| דברים | `/woven-torah/language/he/hebrew_pages/hebrew-map-of-deuteronomy/` | **200** |

### Section 2 — המשנה כדרכה

| Label | Destination | Status |
|---|---|---|
| פורטל המשנה | `/Mishnah-New/Hebrew/Mishnah%20Portal.htm` | **404** *(placeholder — same page as the שער המשנה link in the nav)* |
| PDF של המשנה | `/Mishnah-New/Hebrew/Text/The%20Structured%20Mishnah.pdf` | **200** |

### Section 3 — מחקר

| Label | Destination | Status |
|---|---|---|
| Academia.edu | `https://independent.academia.edu/MosheKline` | 403 *(see note)* |
| Structure is Theology | `/Torah/Structure%20is%20Theology%20Published%20Version.pdf` | **200** |
| מאמרים | `/woven-torah/research-articles/` | **200** |

### Section 4 — קשר

| Label | Destination | Status |
|---|---|---|
| צור קשר | `/General/Contact.htm` | **200** |
| Academia.edu (top 1%) | `https://independent.academia.edu/MosheKline` | 403 *(same URL as Section 3 — see note)* |
| English Site | `/` | **200** |

**Note on the Academia.edu 403:** Academia.edu rejects HEAD/curl requests regardless of User-Agent (anti-scraping). The URL itself is well-formed and is the same one already in production on `/hebrew index.html`'s footer. Real browsers visit it fine; the 403 in this check is an artifact of the verification method, not a broken link.

---

## 5. The One Real 404

Same as before: `/Mishnah-New/Hebrew/Mishnah%20Portal.htm` 404s because the Hebrew Mishnah Portal page hasn't been built yet. Both the nav's **שער המשנה** and the footer's **פורטל המשנה** point at this single not-yet-existent page, so building it once will resolve both 404s with no template changes.

---

## Files Touched

| File | Action |
|---|---|
| `_templates/Academic-Content-HE.html` | Footer block replaced (now lines 362–402) |
| `_pilot/hebrew-nav-render-preview.html` | Regenerated; now exercises both nav and footer |
| `_pilot/hebrew-footer-task.md` | This report |
