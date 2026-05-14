# Zenodo Dataset DOI Integration

**Date:** 2026-05-14
**Scope:** Add Dataset schema JSON-LD + visible citation box to `mishnah-data` landing page; add cross-link from `mishnah-pdf` landing page.
**Status:** **2 files modified cleanly. 0 errors, all defensive checks pass.** **Not committed.**

DOI: `10.5281/zenodo.20179532`
Citation: Kline, Moshe (2026). *The Structured Mishnah Dataset: 525 Chapters in Two-Dimensional Literary Format (JSON)* [Data set]. Zenodo.

---

## 1. Files Modified

| File | Size before | Size after | Δ |
|---|---:|---:|---:|
| `Mishnah-New/Hebrew/Text/mishnah-data.html` | 30,355 | 33,912 | +3,557 |
| `Mishnah-New/Hebrew/Text/mishnah-pdf.html` | 52,906 | 53,219 | +313 |
| `_pilot/zenodo-doi-integration.md` | 0 | (this report) | (new) |

Both files exist at `.html` (extension stripped by Cloudflare for clean URLs `/mishnah-data` and `/mishnah-pdf`).

---

## 2. Insertion Locations

### `mishnah-data.html`

| Insertion | Line | Anchor |
|---|---:|---|
| `<!-- E-Zenodo: Dataset schema added -->` + Dataset JSON-LD `<script>` + `<!-- /E-Zenodo -->` | 101 | Immediately after `<!-- /E-2 -->` (existing E-2 sentinel close) |
| `<p>` with `<a class="cta-link">View on Zenodo (DOI…)</a>` | 414 | Just below the existing JSON download button (in its own `<p>` to avoid inline styles) |
| `<aside class="citation-box">` block | 417 | Immediately after the Zenodo link `<p>` |

### `mishnah-pdf.html`

| Insertion | Line | Anchor |
|---|---:|---|
| `<p class="related-resources">` with cross-link to `mishnah-data` + DOI | 398 | Immediately after the existing PDF download button `<p>` |

No JSON-LD changes on `mishnah-pdf.html` — the Dataset schema lives only on its primary landing page (`mishnah-data`), which is correct per schema.org conventions.

---

## 3. CSS Class Strategy

**`.citation-box` already exists in main.css** at line 1025–1037:

```css
.citation-box {
    background: linear-gradient(to right, #e8f4fd 0%, #d6ebfa 100%);
    border-left: 4px solid #5d87a1;
    padding: 1.25rem 1.5rem;
    margin: 2.5rem 0;
    border-radius: 6px;
    font-size: 0.95rem;
    box-shadow: 0 2px 6px rgba(93, 135, 161, 0.12);
}

.citation-box strong {
    color: #3d5770;
    font-weight: 600;
}
```

The new aside uses this existing class directly — **no inline styles needed for the citation box**. Visual style is the soft-blue gradient panel with a left accent bar that already appears elsewhere on the site.

### Other classes used

| Class | Existing in main.css | Used where |
|---|---|---|
| `.citation-box` | ✓ (line 1025) | The new `<aside>` on mishnah-data |
| `.cta-link` | ✓ | The "View on Zenodo" link |
| `.download-button-large` | ✓ (used by existing JSON download button) | unchanged — original button kept |
| `.related-resources` | ✗ (no rule defined) | The new `<p>` on mishnah-pdf — uses default `<p>` styling |

**No new CSS rules added to main.css** — per project convention. The `.related-resources` class on the mishnah-pdf paragraph is a semantic hook for any future styling but currently relies on default `<p>` margins.

### Inline-style policy

**0 inline styles introduced.** Initially the script added `style="margin-left: 1em;"` to the Zenodo link and `style="margin-top: 1.5em;"` to the related-resources paragraph, but both were removed in a follow-up pass:

- **Zenodo link**: instead of `margin-left`, placed in its own `<p>` element so natural paragraph margins separate it from the JSON download button
- **Related paragraph**: removed inline `margin-top`, relies on default `<p>` margin (typically ~1em browser default)

Post-edit grep for `style="margin..."` introduced by this task: **0 in both files**.

---

## 4. Visible Citation Box (rendered on the page)

This is what visitors will see in `<main>` content on `https://chaver.com/Mishnah-New/Hebrew/Text/mishnah-data`:

```html
<aside class="citation-box">
  <h3>Cite this dataset</h3>
  <p><strong>DOI:</strong> <a href="https://doi.org/10.5281/zenodo.20179532">10.5281/zenodo.20179532</a></p>
  <p><strong>Version:</strong> 2026-05-rev9</p>
  <p><strong>License:</strong> <a href="https://creativecommons.org/licenses/by/4.0/">CC-BY 4.0</a></p>
  <details>
    <summary><strong>Citation</strong></summary>
    <p>Kline, Moshe (2026). <em>The Structured Mishnah Dataset: 525 Chapters in Two-Dimensional Literary Format (JSON)</em> [Data set]. Zenodo. <a href="https://doi.org/10.5281/zenodo.20179532">https://doi.org/10.5281/zenodo.20179532</a></p>
  </details>
</aside>
```

The `<details>` element keeps the full bibliographic citation collapsed by default — visitors see the DOI/version/license as a 3-line summary, and click "Citation" to expand the formal reference for paper citations. This matches the soft-blue gradient panel styling already in main.css.

### "View on Zenodo" link (visible on the page)

In a `<p>` immediately below the existing JSON download button:

```html
<p>
    <a href="https://doi.org/10.5281/zenodo.20179532" class="cta-link">View on Zenodo (DOI: 10.5281/zenodo.20179532)</a>
</p>
```

Uses the same `.cta-link` class as other call-to-action links on the page for visual consistency.

### Related-resources paragraph (in mishnah-pdf)

In `<main>` content on `https://chaver.com/Mishnah-New/Hebrew/Text/mishnah-pdf`, immediately after the "Download Free PDF" button:

```html
<p class="related-resources"><strong>Related:</strong> Researchers and developers can also access the <a href="/Mishnah-New/Hebrew/Text/mishnah-data">structured JSON dataset</a> with literary-marker annotations (DOI: <a href="https://doi.org/10.5281/zenodo.20179532">10.5281/zenodo.20179532</a>).</p>
```

Small, contextual, with two outbound links: to the dataset landing page and to the Zenodo DOI. No layout disruption.

---

## 5. Dataset JSON-LD (full block as injected)

The new `<script type="application/ld+json">` on `mishnah-data.html` (line 101–148):

```json
{
  "@context": "https://schema.org",
  "@type": "Dataset",
  "@id": "https://chaver.com/Mishnah-New/Hebrew/Text/mishnah-data#dataset",
  "name": "The Structured Mishnah Dataset: 525 Chapters in Two-Dimensional Literary Format (JSON)",
  "alternateName": "מאגר המשנה המובנית",
  "description": "The complete Hebrew text of the Mishnah — all six orders, 63 tractates, and 525 chapters — encoded as a structured JSON dataset with cell-level position labels, mishnah verse numbers, and structural markers identifying horizontal parallels, vertical threads, internal parallels, chiastic patterns, and envelope closures.",
  "url": "https://chaver.com/Mishnah-New/Hebrew/Text/mishnah-data",
  "identifier": ["https://doi.org/10.5281/zenodo.20179532", "doi:10.5281/zenodo.20179532"],
  "sameAs": "https://doi.org/10.5281/zenodo.20179532",
  "license": "https://creativecommons.org/licenses/by/4.0/",
  "datePublished": "2026-05-14",
  "version": "2026-05-rev9",
  "inLanguage": ["he", "en"],
  "keywords": ["Mishnah", "Structured Mishnah", "rabbinic literature", "literary structure", "two-dimensional composition", "digital humanities", "Hebrew text", "JSON", "computational analysis"],
  "creator": {"@id": "https://chaver.com/#moshe-kline"},
  "publisher": {"@id": "https://chaver.com/#organization"},
  "isPartOf": {"@id": "https://chaver.com/#mishnah-collection"},
  "variableMeasured": [
    {"@type": "PropertyValue", "name": "chapters", "value": 525},
    {"@type": "PropertyValue", "name": "tractates", "value": 63},
    {"@type": "PropertyValue", "name": "cells", "value": 4467},
    {"@type": "PropertyValue", "name": "structural markers", "value": 6953},
    {"@type": "PropertyValue", "name": "palindromic chapters", "value": 505}
  ],
  "distribution": {
    "@type": "DataDownload",
    "encodingFormat": "application/json",
    "contentUrl": "https://chaver.com/Mishnah-New/English/mishnah_db.json",
    "name": "mishnah_db.json"
  },
  "citation": "Kline, Moshe (2026). The Structured Mishnah Dataset: 525 Chapters in Two-Dimensional Literary Format (JSON) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.20179532"
}
```

### Schema graph integration

The Dataset entity now connects to the canonical schema graph established by E-0 / E-1 / E-3:

- `creator` → `#moshe-kline` (Person, defined on About page)
- `publisher` → `#organization` (Organization, defined on Home page)
- `isPartOf` → `#mishnah-collection` (CollectionPage, defined on the 3 Mishnah portals)

So a crawler that finds the Dataset can traverse:
- Dataset → CollectionPage (3 portals) → 525 chapter Article entries (post Phase D-2)
- Dataset → creator → Person → ProfilePage (about-Moshe-Kline.html) → ItemList of scholarly articles
- Dataset → publisher → Organization → Home page WebSite

The full scholarship graph is now traversable starting from the Zenodo DOI.

---

## 6. JSON-LD Parse Confirmation

| File | JSON-LD blocks total | Parse errors | New block (Dataset) parses |
|---|---:|---:|:-:|
| `mishnah-data.html` | 5 (was 4 + Dataset = 5) | 0 | ✓ |
| `mishnah-pdf.html` | 5 (unchanged) | 0 | n/a (no JSON-LD added here) |

The Dataset block parses cleanly with `ensure_ascii=False` — the Hebrew alternateName (`"מאגר המשנה המובנית"`) is preserved as raw UTF-8, not `\uXXXX` escaped.

---

## 7. Defensive Checks — All Pass

| Check | mishnah-data.html | mishnah-pdf.html |
|---|:-:|:-:|
| File ends with `</html>` | ✓ | ✓ |
| All JSON-LD blocks parse without error | ✓ (5/5) | ✓ (5/5) |
| E-Zenodo sentinel count == 1 (mishnah-data only) | ✓ | n/a |
| No new inline styles introduced | ✓ (0 `style="margin..."` from this task) | ✓ (0) |
| Existing E-1 / E-2 sentinels preserved | ✓ | ✓ |
| Canonical URL preserved (no change) | ✓ | ✓ |
| Atomic write + post-write byte-size verify | ✓ | ✓ |

### Link sanity (the URLs added)

| URL | Type | Expected |
|---|---|---|
| `https://doi.org/10.5281/zenodo.20179532` | Outbound | 302 → Zenodo's page for the dataset |
| `https://chaver.com/Mishnah-New/English/mishnah_db.json` | Outbound (in JSON-LD distribution.contentUrl) | 200 OK (file exists at this path — confirmed via earlier inspections) |
| `https://creativecommons.org/licenses/by/4.0/` | Outbound | 200 OK |
| `https://chaver.com/Mishnah-New/Hebrew/Text/mishnah-data` | Internal cross-link from mishnah-pdf | 200 OK (E-2 canonical) |

I haven't fetched the DOI to verify the 302 since web_fetch only works on URLs in the provenance set. Worth a manual check by Moshe before pushing.

---

## 8. Files Touched

| File | Action |
|---|---|
| `Mishnah-New/Hebrew/Text/mishnah-data.html` | Dataset JSON-LD added; citation box added; "View on Zenodo" link added |
| `Mishnah-New/Hebrew/Text/mishnah-pdf.html` | Related-resources paragraph added with cross-link to mishnah-data + DOI |
| `_pilot/zenodo-doi-integration.md` | This report |

No `main.css` changes. No template changes. No other content files.

---

## 9. Moshe's Verification

### Pre-push diff review in GitHub Desktop

1. **`mishnah-data.html`** — check 3 things:
   - New Dataset JSON-LD block bracketed by `<!-- E-Zenodo: ... -->` / `<!-- /E-Zenodo -->`, right after the E-2 close marker
   - New `<aside class="citation-box">` inside `<main>` content, just below the JSON download button
   - New `<p><a class="cta-link">View on Zenodo (DOI…)</a></p>` between the download button and the citation box
2. **`mishnah-pdf.html`** — confirm a single `<p class="related-resources">` paragraph added immediately after the existing "Download Free PDF" button. Nothing else changed.

### Post-deploy (after push)

1. **Visit `https://chaver.com/Mishnah-New/Hebrew/Text/mishnah-data`** — citation box visible below the download button in the soft-blue gradient style. The Citation `<details>` is collapsed by default; clicking reveals the full bibliographic reference.
2. **Visit `https://chaver.com/Mishnah-New/Hebrew/Text/mishnah-pdf`** — Related paragraph visible just below the PDF download.
3. **Google Rich Results Test** on the mishnah-data URL — should detect Dataset schema with no errors. The 5 numerical `variableMeasured` properties (chapters, tractates, cells, markers, palindromes) should all appear as PropertyValue objects.
4. **Schema.org validator** at validator.schema.org — paste mishnah-data URL; all 5 JSON-LD blocks should parse with zero errors and zero warnings.
5. **Click the "View on Zenodo" link** — should redirect to Zenodo's page for the dataset.

### Cloudflare cache

The deploy will refresh the page server-side. If the URL has been previously cached, do a Purge URL for `https://chaver.com/Mishnah-New/Hebrew/Text/mishnah-data` and `…/mishnah-pdf` to ensure visitors see the new content immediately.

### Manual follow-up tasks (out of scope for Cowork)

Per the task spec, after deploy:

- **ORCID** (https://orcid.org/0009-0003-7469-5167) — check Works section; Zenodo may have already auto-pushed
- **ResearchGate** — add the dataset using DOI `10.5281/zenodo.20179532`
- **Academia.edu** — add a link in your profile referencing the dataset DOI

---

## 10. Out of Scope

- Updating ResearchGate / Academia.edu / ORCID (manual)
- Modifying the JSON dataset itself
- Creating new CSS classes in `main.css`
- Track 2 Phase D-1 push verification (separate task)
- Anything beyond the 2 specified pages
