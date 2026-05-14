# E-3 — Bespoke Schema for Special Pages

**Date:** 2026-05-14
**Scope:** Six HTML files get bespoke schema upgrades that E-1/E-2 intentionally skipped, plus one documentation update capturing the `is_home` detector lesson from E-2.
**Status:** **All 7 files modified successfully. 0 errors. 0 JSON-LD parse failures.** **Not committed.**

---

## 1. Files Modified Summary

| File | Pre-E-3 size | Post-E-3 size | Δ | E-3 change |
|---|---:|---:|---:|---|
| `hebrew index.html` | 39,896 | 39,748 | −148 | Block 1 (WebSite) gained `@id`, lost expanded author; Block 2 (Book) author now references canonical Person `@id`; Block 3 (FAQPage) unchanged |
| `Mishnah/TheMishnah.htm` | 113,283 | 114,256 | +973 | New CollectionPage block with `@id: #mishnah-collection`, 524 items |
| `Mishnah-New/English/Mishnah Portal.htm` | 98,498 | 99,533 | +1,035 | Same — CollectionPage with `#mishnah-collection` |
| `Mishnah-New/Hebrew/Text/Shishah Sidrei Mishnah.htm` | 94,495 | 95,339 | +844 | Same |
| `Torah-New/English/Torah Portal.htm` | 35,331 | 36,343 | +1,012 | New CollectionPage with `@id: #torah-collection`, 86 items |
| `Mishnah-New/Hebrew/Articles/MAVO.htm` | 80,492 | 80,589 | +97 | Article `isPartOf` expanded to array with `#mishnah-collection` |
| `Mishnah-New/English/Articles/Introduction to the Structured Mishnah.htm` | 96,912 | 97,009 | +97 | Same — `isPartOf` array |
| `_pilot/migration-logic.md` | 14,798 | 16,891 | +2,093 | New section 11 documenting `is_home` detector convention |

**Total file size delta across HTML files: +3,910 bytes** (mostly the 4 CollectionPage blocks).

---

## 2. Hebrew Home Schema Consolidation

### Before/after of each JSON-LD block

| Block # | Type | Before | After |
|---|---|---|---|
| 0 | `@graph` (E-1 stub) | `@id`s: `#website`, `#organization`, `#moshe-kline` | unchanged (preserve E-1 stub) |
| 1 | `WebSite` | No `@id`. `author: {"@type": "Person", "name": "Moshe Kline", "url": "https://independent.academia.edu/MosheKline"}` | **`@id: https://chaver.com/#website`** added. `author: {"@id": "https://chaver.com/#moshe-kline"}` |
| 2 | `Book` ("Before Chapter and Verse") | `author: {"@type": "Person", "name": "Moshe Kline"}` | `author: {"@id": "https://chaver.com/#moshe-kline"}` |
| 3 | `FAQPage` (4 Hebrew Q&As) | No top-level Person reference; only Q/A nested objects | unchanged (no Person ref to canonicalize) |

### Why this matters

The WebSite entity now references the canonical `@id` declared by E-0 on the EN home page. JSON-LD's distributed-definition semantics say crawlers will union the properties from both definitions into a single WebSite entity. The Hebrew home's `WebSite` adds the Hebrew-language properties (`inLanguage: "he"`, the Hebrew name and description) to the canonical entity.

The Book entity preserves its page-specific properties (name, ISBN, bookFormat, etc.) but its author field now points to the canonical Person `@id` — so a crawler that resolves Person `#moshe-kline` will find all the canonical Person properties (alumniOf, sameAs links, knowsAbout, etc.) from the About page, plus the relationship "author of this book" inferred from this Book entity. The Hebrew home's Book author no longer "shadows" the canonical Person with a less-complete record.

### Post-edit JSON-LD parse

All 4 blocks parse cleanly. File ends with `</html>` ✓.

---

## 3. Portal CollectionPage Schemas

### Per-portal verification

| File | `@id` | `numberOfItems` | `inLanguage` | `about.name` | `about.alternateName` |
|---|---|---:|---|---|---|
| `Mishnah/TheMishnah.htm` | `https://chaver.com/#mishnah-collection` | 524 | en | The Mishnah | המשנה |
| `Mishnah-New/English/Mishnah Portal.htm` | `https://chaver.com/#mishnah-collection` | 524 | en | The Mishnah | המשנה |
| `Mishnah-New/Hebrew/Text/Shishah Sidrei Mishnah.htm` | `https://chaver.com/#mishnah-collection` | 524 | he | The Mishnah | המשנה |
| `Torah-New/English/Torah Portal.htm` | `https://chaver.com/#torah-collection` | 86 | en | The Torah | התורה |

The 3 Mishnah portals all share the same `@id`. JSON-LD spec: crawlers union the properties from all 3 page declarations into one canonical `#mishnah-collection` entity. This gives the entity:

- Three `url` properties (one per portal page that declares it) — the Mishnah collection is reachable via 3 URLs
- Three `name` properties (each portal's title) — multilingual / multi-context naming
- One consistent `numberOfItems: 524` (matches across all 3)
- One consistent `author: #moshe-kline`, `publisher: #organization`, `about: The Mishnah`
- One `inLanguage: he` (from Shishah Sidrei) and two `inLanguage: en` (from TheMishnah + Mishnah Portal)

The Torah Portal stands alone with `#torah-collection` (86 Torah units).

### Per-portal name + description (sourced from page meta)

| File | `name` | `description` |
|---|---|---|
| `Mishnah/TheMishnah.htm` | "The Structured Mishnah — Read Online \| All 524 Chapters \| Chaver.com" | "Read the complete Mishnah online — all six orders, 63 tractates, 524 chapters — presented as literary tables…" |
| `Mishnah-New/English/Mishnah Portal.htm` | "The Structured Mishnah: Complete Hebrew Text with Literary Analysis \| Chaver.com" | "המשנה כדרכה — The Structured Mishnah…" |
| `Mishnah-New/Hebrew/Text/Shishah Sidrei Mishnah.htm` | "ששה סדרי משנה" | "ששה סדרי משנה" |
| `Torah-New/English/Torah Portal.htm` | "The Woven Torah \| Torah's Literary Architecture \| Chaver.com" | "The Torah Portal: access all five books of the Torah organized as 86 literary units…" |

Each was read from the existing `<title>` and `<meta name="description">` on the page — not hard-coded.

### Injection location

The CollectionPage block was injected immediately after the `<!-- /E-2 -->` close marker (or `<!-- /E-1 -->` for Shishah Sidrei which doesn't have E-2 sentinel), with a new `<!-- E-3: CollectionPage schema added -->` / `<!-- /E-3 -->` sentinel pair.

### Per-portal sentinel count

| File | E-3 sentinel count | Position relative to E-1/E-2 |
|---|---:|---|
| `Mishnah/TheMishnah.htm` | 1 | Between `<!-- /E-2 -->` and `<!-- E-1: ... -->` |
| `Mishnah-New/English/Mishnah Portal.htm` | 1 | Same |
| `Mishnah-New/Hebrew/Text/Shishah Sidrei Mishnah.htm` | 1 | Between `<!-- /E-1 -->` and the next head element (no E-2 on this file) |
| `Torah-New/English/Torah Portal.htm` | 1 | Between `<!-- /E-2 -->` and `<!-- E-1: ... -->` |

---

## 4. Article `isPartOf` Expansion

### MAVO + Introduction

Both Article schemas (the E-2-injected ones, identified by `author: {"@id": "https://chaver.com/#moshe-kline"}`) had a single `isPartOf: {"@id": "https://chaver.com/#website"}` (from E-2). After E-3:

```json
"isPartOf": [
  {"@id": "https://chaver.com/#website"},
  {"@id": "https://chaver.com/#mishnah-collection"}
]
```

The article is part of BOTH the website AND the Mishnah collection — both relationships are true and schema.org allows the array form.

### Per-file confirmation

| File | E-2 Article block found | `isPartOf` after | Size delta |
|---|---|---|---:|
| `MAVO.htm` | Block #2 (out of 3) | array of 2 `@id` refs | +97 B |
| `Intro to Structured Mishnah.htm` | Block #2 (out of 4) | array of 2 `@id` refs | +97 B |

For Intro, there's a SECOND Article schema at block #3 (pre-existing, authored before E-2). It uses a non-canonical Person and Organization (literal records, not `@id` refs) and was left untouched per the task scope — only the E-2-injected Article block gained the `isPartOf` reference.

---

## 5. `is_home` Detector Documentation (Section 11)

Added a new section 11 to `_pilot/migration-logic.md` (file grew from 14,798 → 16,891 bytes; +2,093 B — somewhat more than the spec's ~600-800 estimate because the section includes the bug-mode context). The section:

- Defines a home page as one of EXACTLY two files: `index.html` and `hebrew index.html` at repo root
- Lists 3 sub-directory `index.html` files that the lax detector mis-classified during E-2
- Provides the correct path-based detector pattern (with `relative_to(REPO_ROOT)`)
- Shows the anti-pattern (matching on filename only) that caused the bug
- Notes that the distinction matters for hreflang, og:type, and BreadcrumbList skip logic
- Documents the E-2 fix (surgical hreflang removal + BreadcrumbList backfill)

The file still parses as well-formed Markdown: 12 top-level (`## `) section headers, content flows correctly under each, no broken links or stray heading levels.

---

## 6. Defensive Check Pass Rates

| Check | Files checked | Pass rate |
|---|---:|---:|
| File ends with `</html>` | 7 HTML files | **7/7 ✓** |
| All JSON-LD blocks parse | 7 HTML files (across 19 JSON-LD blocks total) | **19/19 ✓** |
| E-3 sentinel exactly once per portal | 4 portals | **4/4 ✓** |
| Article `isPartOf` contains `#mishnah-collection` | 2 articles (MAVO + Intro) | **2/2 ✓** |
| `is_home Detector Convention` section header present | 1 doc file | **✓** |
| Atomic write + post-write byte-size verify | 7 files | **7/7 ✓** |

**No errors, no anomalies.**

---

## 7. Anomalies Encountered

### 7.1 No truly unexpected state, but worth noting:

- **Mishnah Portal (EN)** has a pre-existing Article schema (block 3 of 3). This is unusual for an `og:type=website` portal page — Article would normally apply to content pages. The Article was already there pre-E-3 (likely hand-authored) and was left untouched. The new CollectionPage stands alongside it.
- **TheMishnah.htm** and **Torah Portal.htm** both have a pre-existing WebPage schema with the OLD non-canonical Person `@id` (`https://chaver.com/about-Moshe-Kline.html#moshe-kline` — pre-E-0 form). Out of scope for E-3 but worth noting: these references could be canonicalized in a future cleanup pass. For now they don't conflict with the new CollectionPage (different `@type`, different role).
- **Shishah Sidrei Mishnah** had no E-2 sentinel — per the E-2 audit, it was `skip-already-complete` (had all required tags pre-existing). I injected the CollectionPage immediately after `<!-- /E-1 -->` instead of `<!-- /E-2 -->`. Different anchor, same outcome.
- **Hebrew home's Block 3 (FAQPage)** had no Person/Organization refs at the top level — only nested under `mainEntity.Question.acceptedAnswer.Answer.text` (where the answer text is plain prose, not structured). No canonicalization needed.

---

## 8. Files Touched

| File | Action |
|---|---|
| `hebrew index.html` | Block 1 + Block 2 updated to reference canonical `@id`s |
| `Mishnah/TheMishnah.htm` | CollectionPage block added |
| `Mishnah-New/English/Mishnah Portal.htm` | CollectionPage block added |
| `Mishnah-New/Hebrew/Text/Shishah Sidrei Mishnah.htm` | CollectionPage block added |
| `Torah-New/English/Torah Portal.htm` | CollectionPage block added |
| `Mishnah-New/Hebrew/Articles/MAVO.htm` | Article `isPartOf` array expanded |
| `Mishnah-New/English/Articles/Introduction to the Structured Mishnah.htm` | Article `isPartOf` array expanded |
| `_pilot/migration-logic.md` | Section 11 (`is_home` Detector Convention) appended |
| `_pilot/e3-special-pages.md` | This report |

**Total: 8 files modified + 1 report = 9 files in the commit.**

---

## 9. Moshe's Verification

### Spot-check via GitHub Desktop diff view

1. **`hebrew index.html`** — confirm 4 JSON-LD blocks survive; block 1 (WebSite) has `"@id": "https://chaver.com/#website"`; block 2 (Book) has `"author": {"@id": "https://chaver.com/#moshe-kline"}`. Other properties (name, url, inLanguage, isbn, etc.) intact.
2. **4 portal files** — each shows a new CollectionPage JSON-LD block injected between the E-2 (or E-1) close marker and the next head element. Verify the `@id` matches: `#mishnah-collection` on the 3 Mishnah portals; `#torah-collection` on Torah Portal.
3. **MAVO + Intro** — diff shows the Article schema's `isPartOf` field expanded from a single `@id` reference to an array of 2 (now includes `#mishnah-collection`).
4. **`_pilot/migration-logic.md`** — Section 11 appended at the end. Markdown headers consistent.

### Post-deploy validation

- **Schema.org validator** at `validator.schema.org`: paste `https://chaver.com/Mishnah/TheMishnah.htm` and confirm CollectionPage validates without errors.
- **Google Rich Results Test**: any of the 4 portal URLs should report `CollectionPage` as a detected type. The `#mishnah-collection` entity should be unified across the 3 Mishnah portals.
- **Schema graph traversal**: a crawler that processes `MAVO.htm`'s Article schema will follow `isPartOf` → `#mishnah-collection` → the 3 portal pages that declare it → the canonical `WebSite`/`Person`/`Organization` entities. The full entity graph should now be traversable from any chapter or article.

### Cache purge consideration

If you've recently tested any of these pages, Cloudflare may have cached the pre-E-3 responses. Purge cache for the 6 modified URLs (or "Purge Everything") to see the new schema immediately.

---

## 10. What's Next After E-3

Per the task spec's "what's next" section:

1. **Re-run SEO/AEO audit on 6 representative pages** — should now show ✓ across every column, including the new CollectionPage references on portals and `isPartOf` mishnah-collection on MAVO/Intro.
2. **Track 2 Phase D-1 pilot** — render 5-6 sample chapters from `mishnah_db.json` using the now-clean pipeline. The Article schema for each rendered chapter can reference `#mishnah-collection` via `isPartOf`, completing the schema graph.
3. **Track 2 Phase D-2 bulk** — render all 525 chapters.
4. **Track 2 Phase D-3 polish** — populate `CollectionPage.mainEntity.itemListElement` with the 524+ chapter URLs on each portal, completing the discoverable chapter listing.

After Track 2, the schema graph is complete: Home → WebSite → Organization + Person; Person → ProfilePage + scholarly articles; CollectionPages (Mishnah + Torah) → 524 + 86 individual chapter Articles, each cross-referenced by author/publisher/isPartOf. AI systems and search crawlers can traverse the full corpus as a connected scholarly resource.

---

## 11. Out of Scope (per task spec)

- Populating `CollectionPage.mainEntity.itemListElement` (deferred to Track 2 Phase D-3)
- Canonicalizing the OLD Person `@id` (`...#moshe-kline` form) in the pre-existing WebPage schemas on TheMishnah and Torah Portal
- Adding `award` field to Person schema
- JBL/JHS/SBL article standalone-page schema upgrades
- Anything outside the 7 specified files
