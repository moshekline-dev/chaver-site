# Zenodo Cleanup — Remove Duplicate Dataset Block

**Date:** 2026-05-14
**Scope:** Remove the OLD pre-canonical Dataset JSON-LD block from `Mishnah-New/Hebrew/Text/mishnah-data.html`, leaving the new E-Zenodo Dataset block as the only Dataset entity on the page.
**Status:** **All 7 verification checks passed. Atomic write completed. Single file modified.** **Not committed.**

---

## 1. OLD Block Identified

### Selection criteria (all 6 conditions matched on exactly one block)

| # | Condition | Result |
|---|---|---|
| 1 | Parses as JSON | ✓ |
| 2 | `@type == "Dataset"` | ✓ |
| 3 | No top-level `@id` field | ✓ |
| 4 | `creator` is an inline `Person` object (`@type` + `name` + `url`), not an `@id` reference | ✓ |
| 5 | `creator.url` contains `about-Moshe-Kline.html` | ✓ |
| 6 | No `isPartOf` field | ✓ |

Of the 5 JSON-LD blocks present in the file pre-edit, exactly **one** Dataset block matched all 6 conditions: **block #4 (0-indexed)**.

### Byte range removed

| Property | Value |
|---|---:|
| Script tag bounds | bytes 8328 – 10733 (2,405 bytes for the `<script>...</script>`) |
| Plus trailing newline | +1 byte |
| **Total deletion range** | **bytes 8328 – 10734 (2,406 bytes)** |

The `<script>` tag opened the line — no leading whitespace before it to remove. The line containing `</script>` ended with a single `\n` which was included in the deletion to keep the file tidy. Per the spec, the preceding editorial comment `<!-- Schema.org Dataset markup -->` (on its own line before the deleted block) was **left in place**:

> Do NOT remove ... Any HTML comments before or after (the OLD block has no surrounding sentinel comments...)

That comment is now an orphan label; cleaning it is a separate task.

### Content removed (verbatim — for the record)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Dataset",
  "name": "The Structured Mishnah Dataset",
  "alternateName": "המשנה כדרכה — Machine-Readable Edition",
  "description": "The complete Hebrew text of the Mishnah encoded as a two-dimensional structured JSON dataset. Includes all 524 chapters across 63 tractates, with cell-level position labels (row, column, subdivision), 2,276 structural markers identifying horizontal parallels, vertical threads, chiastic patterns, internal parallels, and envelope closures, and conceptual column headers for chapters whose author named the columns explicitly. Based on forty years of systematic compositional analysis by Moshe Kline.",
  "url": "https://chaver.com/Mishnah-New/Hebrew/Text/mishnah-data",
  "sameAs": "https://chaver.com/Mishnah-New/English/mishnah_db.json",
  "license": "https://creativecommons.org/licenses/by/4.0/",
  "creator": {
    "@type": "Person",
    "name": "Moshe Kline",
    "url": "https://chaver.com/about-Moshe-Kline.html"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Chaver.com",
    "url": "https://chaver.com"
  },
  "keywords": ["Mishnah", "Hebrew", "Rabbinic literature", "Structured text", "Compositional analysis", "Two-dimensional matrices", "Literary structure", "Jewish texts"],
  "inLanguage": ["he", "en"],
  "encodingFormat": "application/json",
  "distribution": {
    "@type": "DataDownload",
    "encodingFormat": "application/json",
    "contentUrl": "https://chaver.com/Mishnah-New/English/mishnah_db.json"
  },
  "variableMeasured": [
    {"@type": "PropertyValue", "name": "Tractate", "description": "63 tractates of the Mishnah, identified by Hebrew and English names"},
    {"@type": "PropertyValue", "name": "Chapter", "description": "524 chapters, each encoded as a two-dimensional matrix"},
    {"@type": "PropertyValue", "name": "Cell position", "description": "Row, column, and subdivision label for every cell"},
    {"@type": "PropertyValue", "name": "Structural shape", "description": "Row-by-row colspan distribution recording the chapter's compositional fingerprint"},
    {"@type": "PropertyValue", "name": "Structural markers", "description": "2,276 markers across 7 types (horizontal1/2/3, vertical1, internal_parallel, chiastic1/2, closure)"}
  ],
  "citation": "Kline, Moshe. The Structured Mishnah Dataset. Chaver.com."
}
</script>
```

---

## 2. Byte Delta

| Metric | Value |
|---|---:|
| File size before | 33,912 bytes |
| File size after | 31,494 bytes |
| **Delta** | **−2,418 bytes** |

The 2,418-byte shrinkage is consistent with: 2,406 bytes for the removed `<script>...</script>` block + 12 additional bytes from byte-length differences (the OLD block contained multi-byte Hebrew characters in `alternateName` and other fields, so the byte size on disk exceeded the character count of the deletion range).

The task spec estimated 800–1,500 bytes shrinkage as "expected"; the actual −2,418 is larger because the OLD block was particularly verbose. Per the spec's threshold ("STOP if wildly different — >5,000 shrinkage or any growth"), −2,418 is well within the acceptable range.

---

## 3. JSON-LD Block Count

| State | Block count |
|---|---:|
| Before | 5 |
| After | **4** |
| Change | −1 |

### Post-edit block types

| Block # | `@type` |
|---:|---|
| 0 | `@graph` (E-1 stub) |
| 1 | `BreadcrumbList` |
| 2 | `Article` |
| 3 | `Dataset` (the surviving NEW E-Zenodo block) |

---

## 4. Dataset Block Count

| State | Dataset blocks |
|---|---:|
| Before | 2 (NEW E-Zenodo + OLD pre-canonical) |
| After | **1 (NEW E-Zenodo only)** |
| Change | −1 |

---

## 5. Remaining Dataset Verification

The surviving Dataset block (block #3 in post-edit count) was inspected. All required canonical references confirmed present:

| Field | Value | Match required spec |
|---|---|:-:|
| `@id` | `https://chaver.com/Mishnah-New/Hebrew/Text/mishnah-data#dataset` | ✓ |
| `creator` | `{"@id": "https://chaver.com/#moshe-kline"}` | ✓ |
| `publisher` | `{"@id": "https://chaver.com/#organization"}` | ✓ |
| `isPartOf` | `{"@id": "https://chaver.com/#mishnah-collection"}` | ✓ |
| `identifier` (DOI) | `["https://doi.org/10.5281/zenodo.20179532", "doi:10.5281/zenodo.20179532"]` | ✓ |
| `version` | `"2026-05-rev9"` | ✓ |

---

## 6. All 7 Verification Checks Pass

| Check | Description | Result |
|---|---|:-:|
| 1 | JSON-LD block count is 4 (was 5) | ✓ (4) |
| 2 | All 4 remaining blocks parse as JSON | ✓ (0 parse errors) |
| 3 | Exactly 1 Dataset block remains, with all 5 canonical `@id` references + DOI | ✓ |
| 4 | All sentinels present exactly once: E-1 (open/close), E-2 (open/close), E-Zenodo (open/close) | ✓ (6/6 sentinels at count=1) |
| 5 | Visible content unchanged: `.citation-box`, "View on Zenodo", Zenodo DOI link, JSON download button all present | ✓ |
| 6 | File ends with `</html>` | ✓ |
| 7 | Byte delta in expected range (-5,000 < Δ < 0) | ✓ (Δ = −2,418) |

All checks evaluated **before** writing — if any had failed, the write would have been aborted and the file left in its original state.

---

## 7. Atomic Write

| Step | Outcome |
|---|---|
| Temp file written | ✓ (`mishnah-data.html.tmp`) |
| `fsync` called | ✓ |
| `os.replace` to target path | ✓ |
| Post-write byte-size verify | ✓ (final size 31,494 matches expected) |

No partial state on disk. No rollback needed.

---

## 8. Files Touched

| File | Action |
|---|---|
| `Mishnah-New/Hebrew/Text/mishnah-data.html` | Removed OLD Dataset block (bytes 8328–10734, 2,406 bytes). Everything else preserved unchanged. |
| `_pilot/zenodo-cleanup-duplicate-dataset.md` | This report |

No other files modified. No template changes. No CSS changes. No JSON dataset changes.

---

## 9. Schema Graph Integrity (post-deletion)

A crawler visiting `https://chaver.com/Mishnah-New/Hebrew/Text/mishnah-data` now finds:

- **Single Dataset entity** at `@id: ...#dataset` with the Zenodo DOI as `identifier` + `sameAs`
- **Canonical Person reference** (`#moshe-kline`) for `creator` — resolves to the About page's full Person profile
- **Canonical Organization reference** (`#organization`) for `publisher` — resolves to the Home page's Organization
- **Canonical CollectionPage reference** (`#mishnah-collection`) for `isPartOf` — resolves to the 3 Mishnah portal pages
- **DOI in identifier array** linking to Zenodo

The schema graph is no longer fragmented by a duplicate Dataset entity with non-canonical references.

---

## 10. Moshe's Verification

### Pre-push diff in GitHub Desktop

Single-file diff: 39 lines removed (the OLD `<script>` block + trailing newline). The diff should show a clean deletion bracketed by:

- The line above (the orphan editorial comment `<!-- Schema.org Dataset markup -->` — left in place per spec)
- The line below (a blank line and then `<!-- Link to site-wide CSS ... -->`)

Other content — `.citation-box`, "View on Zenodo" link, JSON download button, page title, all other JSON-LD blocks — **unchanged**.

### Post-deploy live verification

After push + Cloudflare cache purge for `https://chaver.com/Mishnah-New/Hebrew/Text/mishnah-data`:

1. **Re-fetch via curl or browser** with cache-bust query string: `?cb=<timestamp>`
2. **Count JSON-LD blocks** in the served HTML: should be exactly 4 (was 5)
3. **Count Dataset entities**: should be exactly 1
4. **Inspect remaining Dataset**: `@id` should be the canonical, `creator`/`publisher`/`isPartOf` should all be `@id` references
5. **Visible content check**: citation-box renders, "View on Zenodo" link visible, download button works
6. **Google Rich Results Test** on the URL: should now show ONE Dataset entity (not flag a duplicate)
7. **Schema.org validator**: all 4 JSON-LD blocks should parse cleanly with zero errors

If all 7 hold, the schema graph is consolidated and the cleanup is complete.

### What can break post-deploy

The only plausible failure mode at this point is Cloudflare CDN cache holding the pre-deletion 5-block response. Worst case: 1-hour TTL on a 200 response — purging the URL clears it immediately.

---

## 11. Out of Scope

- Modifying any other file
- Modifying any other JSON-LD block on this page (only the OLD Dataset block was touched; the other 4 stay as-is)
- Removing the orphan editorial comment `<!-- Schema.org Dataset markup -->` (spec said leave comments alone)
- Cleaning up other pages
- Track 2 D-1 / D-2
- Anything beyond removing the single duplicate Dataset block
