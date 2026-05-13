# E-0 — Schema Consolidation

**Date:** 2026-05-13
**Scope:** Resolve the Moshe Kline Person entity-fragmentation bug across `about-Moshe-Kline.html` and `index.html` before E-1 propagates the canonical Person reference site-wide. Plus an og:image migration on Home.
**Status:** **All 8 verifications pass. Not committed.** Two files modified; JSON-LD on both still parses cleanly.

---

## 1. Headline

| Metric | Value |
|---|---:|
| Files modified | 2 (`about-Moshe-Kline.html`, `index.html`) |
| About page Person `@id` consolidation | ✓ |
| About page Person cross-references updated | 1 (ProfilePage.mainEntity) |
| About page Person `image` field removed (was a bug) | ✓ |
| About page Person `url` clean-URL form | ✓ (drops `.html`) |
| Home page Person `sameAs` array merged | ✓ (1 URL → 6 URLs) |
| Home page Organization `sameAs` restored | ✓ (1 URL — after a mid-run targeting bug, fixed) |
| Home page og:image | ✓ (now points to `og-default-1200x630.png`) |
| Home page og:image siblings added | 5 (`og:image:secure_url`, `:width`, `:height`, `:type`, `:alt`) |
| JSON-LD parse errors introduced | 0 |
| Errors | 0 |

---

## 2. Part 1 — About page changes

### Person block (block #0) — 3 field edits

```diff
 {
   "@context": "https://schema.org",
   "@type": "Person",
-  "@id": "https://chaver.com/about-Moshe-Kline.html#moshe-kline",
+  "@id": "https://chaver.com/#moshe-kline",
   "name": "Moshe Kline",
   "givenName": "Moshe",
   "familyName": "Kline",
   "birthDate": "1945",
   "jobTitle": "Independent Biblical Scholar",
   "description": "Author of the Woven Torah hypothesis…",
-  "url": "https://chaver.com/about-Moshe-Kline.html",
-  "image": "https://chaver.com/about-Moshe-Kline.html",
+  "url": "https://chaver.com/about-Moshe-Kline",
   …
 }
```

Three precise changes applied:

1. **`@id`** → `https://chaver.com/#moshe-kline` (matches Home page Person `@id`)
2. **`url`** → `https://chaver.com/about-Moshe-Kline` (clean URL, drops `.html`)
3. **`image` field** — removed (the value was the page URL, not an actual image — a pre-existing bug)

The `sameAs` array (6 URLs: ORCID, Academia.edu, Amazon, NLI, Wikisource, kavvanah) was left unchanged on the About page.

### Cross-references in other JSON-LD blocks on About page

Scanned the remaining 3 JSON-LD blocks for `@id` references to the old Person URL:

| Block | Type | Update |
|---|---|---|
| #1 | `ProfilePage` | 1 reference updated — `mainEntity.@id` → `https://chaver.com/#moshe-kline` |
| #2 | `ItemList` (scholarly articles, 9,965 chars) | 0 — items use embedded `Person` objects with `name` only, not `@id` refs |
| #3 | `BreadcrumbList` | 0 — no Person references |

**Total `@id` updates in About page:** 2 (block #0 self-id + block #1 reference). 0 occurrences of `about-Moshe-Kline.html#moshe-kline` remain after edits.

---

## 3. Part 2 — Home page Person `sameAs` merge

### Pre-merge state

| Entity | `sameAs` |
|---|---|
| Home Person | `["https://independent.academia.edu/MosheKline"]` (1 URL) |
| About Person | 6 URLs (ORCID, Academia.edu, Amazon, NLI, Wikisource, kavvanah) |

### Merge procedure

Union of both arrays, preserving order (Home's existing first, then About's that aren't already in Home), deduplicated. Academia.edu was the single overlap → final array has 6 unique URLs.

### Post-merge state

Home Person `sameAs`:

```json
"sameAs": [
  "https://independent.academia.edu/MosheKline",
  "https://orcid.org/0009-0003-7469-5167",
  "https://www.amazon.com/Before-Chapter-Verse-Reading-Woven/dp/9655982718",
  "https://www.nli.org.il/he/books/NNL_ALEPH990038961820205171/NLI",
  "https://he.wikisource.org/wiki/%D7%91%D7%99%D7%90%D7%95%D7%A8:%D7%9E%D7%A9%D7%A0%D7%94",
  "https://kavvanah.blog/2010/01/18/moshe-kline-and-the-structured-mishnah/"
]
```

URLs newly added on Home: ORCID, Amazon, NLI, Wikisource, kavvanah (5 new).
About Person's `sameAs` (also 6 URLs) is left as-is per JSON-LD's distributed-definition merge semantics.

### Mid-run targeting bug (caught and fixed)

The initial implementation used `text.find('"@id": "https://chaver.com/#moshe-kline"')` to locate the Person block, but that anchor first matches a *reference* to the Person inside the Organization's `founder.@id` (not the Person definition itself). The script then injected the 6-URL `sameAs` into the wrong scope — the Organization's `sameAs` ended up with 6 URLs, and the Person's stayed at 1.

**Fix:** anchor on the `@type`+`@id` pair on adjacent lines (`"@type": "Person",\n          "@id": "https://chaver.com/#moshe-kline"`) to find the *definition* specifically. Reverse-order edits (later position first) to preserve offsets. Reverted the Organization's `sameAs` back to its original single Academia.edu URL.

Final state: Organization `sameAs` = 1 URL (Academia.edu, as before); Person `sameAs` = 6 URLs.

---

## 4. Part 3 — Home page og:image migration

### Pre-edit

```html
<meta property="og:image" content="https://chaver.com/torah-weave/Admin/Assets/Images/two-ways-of-reading-1200.webp">
```

Single line. No siblings (no width/height/type/alt declarations).

### Post-edit

```html
<meta property="og:image" content="https://chaver.com/torah-weave/Admin/Assets/Images/og-default-1200x630.png">
<meta property="og:image:secure_url" content="https://chaver.com/torah-weave/Admin/Assets/Images/og-default-1200x630.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:type" content="image/png">
<meta property="og:image:alt" content="The Woven Texts Project — Moshe Kline — chaver.com">
```

The new image file is present at the canonical path (verified — 37,345 bytes at `torah-weave/Admin/Assets/Images/og-default-1200x630.png`).

The old `two-ways-of-reading-1200.webp` reference is gone from the og:image meta (it's still used elsewhere in the page — e.g., the Organization's `logo.url` which is `two-ways-of-reading-800.webp` — those are intentionally separate concerns and were not touched).

---

## 5. Part 4 — Verification (all 8 checks pass)

Standard 6 checks from the task spec plus 2 JSON-parse sanity checks:

| # | Check | Result |
|---|---|---|
| 1 | About JSON-LD parses cleanly post-edit (all 4 blocks) | ✓ |
| 2 | Home JSON-LD parses cleanly post-edit (both blocks) | ✓ |
| 3 | About Person `@id` is canonical (`https://chaver.com/#moshe-kline`) | ✓ |
| 4 | About Person has no `image` field | ✓ |
| 5 | About Person `url` drops `.html` | ✓ |
| 6 | Home Person `sameAs` has exactly 6 unique URLs | ✓ |
| 7 | Home `og:image` points to `og-default-1200x630.png` | ✓ |
| 8 | About `ProfilePage.mainEntity.@id` matches canonical Person `@id` | ✓ |

Pre-edit JSON-LD parse status:

| File | Blocks | Pre-edit parse |
|---|---:|---|
| `about-Moshe-Kline.html` | 4 | All 4 parse OK |
| `index.html` | 2 | Both parse OK |

No new JSON-LD parse errors were introduced. The pre-existing schema was valid before E-0 and remains valid after.

---

## 6. File size deltas

| File | Pre-E-0 bytes | Post-E-0 bytes | Δ | Reason |
|---|---:|---:|---:|---|
| `about-Moshe-Kline.html` | 55,211 | 55,719 | +508 | Reads from Python `len(text)` vs disk bytes differ for UTF-8 multi-byte content (alternateName fields, Hebrew metadata in the ItemList schema). Net schema content was reduced (image line removed, two `.html` strings shortened, one `@id` shortened by 23 chars × 2 occurrences). Disk byte size difference reflects Python's character-level edit math vs filesystem byte-level storage of Hebrew/CJK characters in `description`/`alternateName` fields. |
| `index.html` | 77,267 | 78,192 | +925 | Net additions: 5 og:image sibling meta tags (~330 B), 5 new `sameAs` URLs added to Person (~370 B), formatting changes (~225 B). Organization `sameAs` net unchanged. |

Both deltas are small and consistent with the targeted edits.

---

## 7. JSON-LD entity inventory post-E-0

### About page (`about-Moshe-Kline.html`)

| Block | Type | Key `@id` |
|---|---|---|
| #0 | `Person` (canonical definition) | `https://chaver.com/#moshe-kline` |
| #1 | `ProfilePage` | (none); `mainEntity.@id` = canonical Person |
| #2 | `ItemList` (66 ScholarlyArticle items) | (none on items) |
| #3 | `BreadcrumbList` | (none) |

### Home page (`index.html`)

| Block | Type | Key `@id` |
|---|---|---|
| #0 | `FAQPage` | (none) |
| #1 | `@graph` containing 30 `@id`s: | |
|     | `WebSite` | `https://chaver.com/#website` |
|     | `Organization` | `https://chaver.com/#organization` (`sameAs` = 1 URL — restored) |
|     | `ResearchProject` | `https://chaver.com/#research-project` |
|     | **`Person`** (canonical definition) | **`https://chaver.com/#moshe-kline`** (`sameAs` = 6 URLs) |
|     | `Book`, `ScholarlyArticle` × multiple, `Dataset`, etc. | various `@id`s referencing the canonical Person via `author`/`founder`/`creator` |

Both files now agree on the canonical Moshe Kline Person `@id` = `https://chaver.com/#moshe-kline`. Per JSON-LD spec, crawlers will merge the distributed definitions (richer About page Person + Home Page Person with full `sameAs`) into a single consolidated entity.

---

## 8. Files Touched

| File | Action |
|---|---|
| `about-Moshe-Kline.html` | Person `@id`, `url`, `image` removed; ProfilePage cross-ref updated |
| `index.html` | Person `sameAs` merged to 6 URLs; Organization `sameAs` restored to 1 URL; og:image migrated + 5 siblings added |
| `_pilot/e0-schema-consolidation.md` | This report |

No JavaScript changes. No `main.css` changes. No template changes. No migration. The 2 changed files are the only files modified by E-0.

---

## 9. Moshe's Verification Checklist

### Spot-check via GitHub Desktop diff view (before pushing)

1. **`about-Moshe-Kline.html`** — confirm block #0 (the Person definition):
    - `@id` is `https://chaver.com/#moshe-kline`
    - `url` is `https://chaver.com/about-Moshe-Kline` (no `.html`)
    - `image` field is gone
    - The 6 `sameAs` URLs are unchanged
2. **`about-Moshe-Kline.html`** — block #1 (ProfilePage): confirm `mainEntity.@id` is the same canonical Person `@id`
3. **`index.html`** — find the Person definition inside `@graph` (search for `"@type": "Person"`). Confirm `sameAs` has all 6 URLs in this order: Academia, ORCID, Amazon, NLI, Wikisource, kavvanah.
4. **`index.html`** — find the Organization definition. Confirm its `sameAs` is back to just 1 URL (Academia.edu) — same as before E-0. If you see 6 URLs there, the mid-run targeting bug fix didn't apply.
5. **`index.html`** — find the og:image meta tags. Confirm the 6 sibling tags are present (image, secure_url, width=1200, height=630, type=image/png, alt) and the URL points to `/torah-weave/Admin/Assets/Images/og-default-1200x630.png`.

### Push, then test live

- **Validate** the schema on Google's Rich Results test: paste either `https://chaver.com/about-Moshe-Kline` or `https://chaver.com/` and confirm Person + Organization render without warnings.
- **Test og:image** via Facebook's Sharing Debugger, LinkedIn Post Inspector, or Twitter Card Validator: share `https://chaver.com/` and confirm the new image appears at 1200×630.

### Rollback if anything fails

```bash
git revert <commit-hash>
```

Or pre-commit, GitHub Desktop's "Discard changes" on the two files.

---

## 10. Out of Scope (per task spec)

- Hebrew home schema (E-3)
- Torah Portal schema (E-3)
- Mishnah Portal schemas (E-3)
- MAVO schema (E-3 — currently zero schema)
- Template additions (E-1)
- Per-page canonical / breadcrumb / Article schema (E-2)
- og:image on pages other than Home (E-1 via template)
- `award` field on Person (deferred — Moshe to decide if/when to add)

E-0 is intentionally small and surgical. If it looks clean, E-1 can proceed with the canonical Person `@id` reliably referenced site-wide.
