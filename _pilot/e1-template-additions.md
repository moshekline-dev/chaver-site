# E-1 — Template Additions + Site-Wide Injection

**Date:** 2026-05-13
**Scope:** Add site-wide SEO/AEO boilerplate (og:image default, og:site_name, og:locale, twitter:card, meta author, and a 3-stub JSON-LD entity reference block) to the 2 templates AND to all 779 already-migrated files.

**Status:** **All 779 migrated files + 2 templates successfully E-1-injected. 0 errors.** Pre-existing tags on 40 files were replaced with E-1 values; the WebSite/Organization/Person @id stubs were added on top of existing JSON-LD on the 759 files that already had schema. Two truncation issues were discovered (pre-existing damage from Track 1 Part 3's OneDrive write race) and recovered in-line. **Not committed.**

---

## 1. Headline

| Metric | Value |
|---|---:|
| Templates updated | 2 (EN + HE), each with E-1 sentinel exactly once |
| Migrated files scanned | 779 (174 EN + 605 HE) |
| **Migrated files successfully E-1-injected** | **779 (100%)** |
| Files where conflicting tags were replaced | 40 |
| Files truncated pre-E-1 (recovered in-line) | 2 |
| JSON-LD parse errors introduced | 0 |
| Files with E-1 sentinel exactly once (post-edit) | 779 / 779 ✓ |
| Files ending with `</html>` (post-edit) | 779 / 779 ✓ |
| Files with `og:locale` matching lang | 779 / 779 ✓ (en_US for EN, he_IL for HE) |
| Files with `og:image` pointing to og-default-1200x630.png | 779 / 779 ✓ |
| Files with `meta name="author" content="Moshe Kline"` | 779 / 779 ✓ |
| Mean size delta per file | +1,378 bytes |
| Total corpus byte growth | +1.07 MB across 779 files (size-on-disk) |

---

## 2. Templates Updated

| Template | Pre-E-1 size | Post-E-1 size | Δ | Sentinels | Region placeholders preserved |
|---|---:|---:|---:|---|---:|
| `_templates/Academic-Content-EN.html` | 14,978 | 16,364 | +1,386 | 1 open + 1 close | 5/5 (doctitle, meta, additional-styles, content, page-scripts) |
| `_templates/Academic-Content-HE.html` | 13,661 | 15,047 | +1,386 | 1 open + 1 close | 5/5 (same) |

The E-1 block is inserted between `<meta name="viewport">` and `<link rel="icon">` on line 15 of each template. The 22-line block lives inside `<head>` and references the canonical entity `@id`s established in E-0:

- WebSite: `https://chaver.com/#website`
- Organization: `https://chaver.com/#organization`
- Person: `https://chaver.com/#moshe-kline`

EN template: `og:locale` = `en_US`. HE template: `og:locale` = `he_IL`. All other content identical between EN and HE templates.

---

## 3. Bulk Injection Results

### Per-language breakdown

| Language | Files scanned | Injected successfully | Errors |
|---|---:|---:|---:|
| EN | 174 | 174 (after recovery — see §5) | 0 |
| HE | 605 | 605 | 0 |
| **Total** | **779** | **779** | **0** |

### File size deltas

| Statistic | Bytes |
|---|---:|
| Mean delta per file | +1,378 |
| Min delta | +723 (files with many pre-existing tags being replaced — net add was smaller) |
| Max delta | +1,386 (files with no pre-existing tags — full block added) |

---

## 4. Conflict Detection and Resolution

E-1 detected pre-existing conflicting tags on 40 files. Per the task spec, the implementation **replaces** these with E-1 values to standardize the boilerplate site-wide.

### Replaced tag frequency

| Tag | Files where replaced |
|---|---:|
| `og:site_name` | 35 |
| `twitter:card` | 32 |
| `meta name="author"` | 15 |
| `og:locale` | 4 |
| `og:image` | 2 (index.html + hebrew index.html) |
| `og:image:secure_url` | 1 (index.html) |
| `og:image:width` | 1 (index.html) |
| `og:image:height` | 1 (index.html) |
| `og:image:type` | 1 (index.html) |
| `og:image:alt` | 1 (index.html) |

The most common conflict was `og:site_name` (35 files) — likely from manual SEO authoring on key pages. The 2 files with conflicting `og:image` were `index.html` (already correct post-E-0 — same URL just re-injected with E-1 indent) and `hebrew index.html` (had pointed to an old `two-ways-of-reading-1200.webp` — now updated to `og-default-1200x630.png`).

### JSON-LD stub block added

The E-1 block adds a 4th element: a `<script type="application/ld+json">` containing a 3-entity `@graph` declaring `{"@type": "WebSite", "@id": "..."}`, `{"@type": "Organization", "@id": "..."}`, `{"@type": "Person", "@id": "..."}`.

This is additive — existing JSON-LD blocks on each page are preserved. Per JSON-LD's distributed-definition semantics, a stub `@id` reference here resolves to the full entity definition on the Home page. Crawlers will union the properties.

Files that gained the stub block:

| Pre-existing JSON-LD blocks | Files | New JSON-LD count after E-1 |
|---|---:|---:|
| 0 blocks | 20 | 1 (E-1 stub only) |
| 1 block | 36 | 2 |
| 2 blocks | many | 3 |
| 3 blocks | a few | 4 |
| 4 blocks | 1 (about-Moshe-Kline.html) | 5 |

All JSON-LD blocks (existing + new stub) parse cleanly post-edit. 0 parse errors introduced.

---

## 5. Truncation Recovery

Two EN files were found to be **already truncated** before E-1 ran (they didn't end with `</html>`). These were not caused by E-1 — they were pre-existing damage, almost certainly from Track 1 Part 3's OneDrive write race on the bulk EN-nav-dropdown edit. E-1's verification check correctly refused to write these files when the injection result wouldn't end with `</html>`. They were then recovered in-line.

### `Torah-New/English/Torah Portal.htm` — minor truncation

| | Before recovery | After recovery |
|---|---:|---:|
| File size | 33,640 B | 34,929 B |
| `</html>` close | mid-tag `</html` (missing trailing `>`) | ✓ |
| E-1 sentinel | 0 | 1 |

Recovery: appended `>\n` to close `</html>`, then ran the E-1 injection. Only 1 byte was lost in the original truncation; all content (Track 1 Mishnah dropdown, slideshow link fix, etc.) was intact.

### `torah-weave/Genesis/genesis-analysis/the-hidden-warp.html` — severe truncation

| | Before recovery | After recovery |
|---|---:|---:|
| File size | 8,730 B | 52,343 B |
| `</html>` close | none (file ended mid-paragraph at `<figure style="margin: 2em 0; text-align: ce`) | ✓ |
| `</body>` close | missing | ✓ |
| `class="site-footer"` | missing | ✓ |
| `</main>` close | missing | ✓ |
| E-1 sentinel | 0 | 1 |

About **44 KB** of content was lost during Track 1 Part 3. Recovery: re-ran the Phase B migration logic from `_backup-pre-migration/torah-weave/Genesis/genesis-analysis/the-hidden-warp.html` (53,359 B DWT-attached source) using the current EN template (which already has E-1 + Mishnah dropdown + favicon + all post-Phase-B updates baked in). The re-rendered file is byte-for-byte equivalent to what a fresh Phase B run would have produced.

Region extraction sizes for the re-migration:

| Region | Size |
|---|---:|
| `doctitle` | 82 B |
| `meta` | 60 B |
| `additional-styles` | 60 B |
| `content` | 37,310 B |
| `page-scripts` | 52 B |

Final file size 52,343 B is consistent with other migrated EN files of similar source size.

### Truncation audit across the full corpus

After recovery, **all 779 files end with `</html>`**. An additional sanity audit checked for `</body>`, `</main>`, and `class="site-footer"` markers — every file has all three. Apart from these 2 known cases, no other truncated migrated files exist.

---

## 6. Per-Page Verification — All Checks Pass

Across all 779 migrated files:

| Check | Result |
|---|---:|
| E-1 open sentinel (`<!-- E-1: Site-wide SEO/AEO boilerplate`) appears exactly once | 779 / 779 ✓ |
| E-1 close sentinel (`<!-- /E-1 -->`) appears exactly once | 779 / 779 ✓ |
| File ends with `</html>` | 779 / 779 ✓ |
| `<meta name="viewport">` count is exactly 1 (no duplicates introduced) | 779 / 779 ✓ |
| `og:image` content includes `og-default-1200x630.png` | 779 / 779 ✓ |
| `<meta name="author" content="Moshe Kline">` present | 779 / 779 ✓ |
| `og:locale` matches detected language (en_US for EN; he_IL for HE) | 779 / 779 ✓ |
| All `<script type="application/ld+json">` blocks parse without error | 779 / 779 ✓ |
| Templates well-formed | 2 / 2 ✓ |

---

## 7. Special-Handling Pages — Specific Confirmation

Per the task spec's Part 3 list (the 6 pages with notable pre-existing schema):

| Page | Pre-E-1 JSON-LD blocks | Post-E-1 JSON-LD blocks | og:locale | Pre-existing tags replaced | Notes |
|---|---:|---:|---|---|---|
| `index.html` (Home, EN) | 2 (FAQPage + `@graph`) | 3 (added E-1 stub) | en_US | og:site_name, og:locale, og:image (+ 5 sibling tags), twitter:card, meta author — all match E-0 / E-1 canonical values | E-1 stub is redundant with full `@graph` definition; JSON-LD merge semantics handle this correctly. |
| `about-Moshe-Kline.html` (About, EN) | 4 (Person + ProfilePage + ItemList + BreadcrumbList) | 5 (added E-1 stub) | en_US | meta author replaced | The canonical Person entity defined here now also gets a `@id` stub reference at the top of head — both definitions union via shared `@id`. |
| `hebrew index.html` (Home HE) | 3 (WebSite + Book + FAQPage) | 4 (added E-1 stub) | he_IL | og:site_name, og:locale, og:image, twitter:card, meta author replaced. Old og:image (`two-ways-of-reading-1200.webp`) replaced with og-default. | Hebrew home @id consolidation deferred to E-3. |
| `Torah-New/English/Torah Portal.htm` | 1 (WebPage) | 2 (added E-1 stub) | en_US | og:site_name replaced. (Recovered from truncation — see §5.) | |
| `Mishnah/TheMishnah.htm` | 2 | 3 (added E-1 stub) | en_US | og:site_name, twitter:card, meta author replaced | |
| `Mishnah-New/Hebrew/Articles/MAVO.htm` | **0** (zero schema before) | **1** (E-1 stub only) | he_IL | none (had no pre-existing tags to conflict with) | **MAVO has now gained its first JSON-LD ever.** |

---

## 8. Sample Spot-Checks (5 Random Pages, First ~38 Lines)

(Full samples in Verification log; abbreviated here.)

| Page | E-1 location | og:locale | Total `<head>` lines |
|---|---:|---|---:|
| `torah-weave/Numbers/numbers-unit-11/numbers-unit-11.html` | line 13–36 | en_US | 171 |
| `torah-weave/leviticus-19-ark-at-the-center.html` | line 13–36 | en_US | 202 |
| `Mishnah/TheMishnah.htm` | line 13–36 | en_US | 252 |
| `Mishnah-New/Hebrew/Text/Seder Nezikin/Masechet Baba Kama/Masechet Baba Kama Perek 3.htm` | line 13–36 | he_IL | 182 |
| `Mishnah-New/Hebrew/Text/Seder Nashim/Masechet Yevamot/Masechet Yevamot Perek 2.htm` | line 13–36 | he_IL | 182 |

Identical structure across all 5 samples — E-1 block at lines 13–36, immediately after `<meta name="viewport">`, immediately before `<link rel="icon">`. Per-page existing metadata (title, description, page-specific og: tags) follows.

---

## 9. Anomalies and Decisions

### 9.1 Track 1 Part 3 caused two file truncations

The post-edit audit revealed that 2 of the 174 EN files entered E-1 already truncated. Both files were edited by Track 1 Part 3 (the EN nav Mishnah-dropdown conversion). Almost certainly a OneDrive write race — the script wrote correctly but the OneDrive sync left partial bytes for these two files.

**Implication:** The robust pattern is to verify file integrity after every bulk operation. E-1's per-file `endswith('</html>')` check correctly refused to corrupt these files further. The recovery used the `_backup-pre-migration/` source as a clean base.

**Recommendation for future bulk-write tasks:** add a post-write byte-count check (compare written bytes to expected length) and re-write if mismatch. This catches OneDrive truncation at write time.

### 9.2 The E-1 stub on already-schema-rich pages is redundant but harmless

`index.html` and `about-Moshe-Kline.html` each get a 3-stub `@graph` block on top of their full entity definitions. Per JSON-LD spec, this is fine — crawlers union the properties of each `@id`. The stub provides no new information for these pages but makes the boilerplate identical across the entire corpus, which simplifies E-2 reasoning.

### 9.3 No idempotency skips in this run

This was a clean first-run — 0 files had the E-1 sentinel pre-existing. Re-running the script would now skip all 779 (idempotency by sentinel check).

### 9.4 og:title / og:description per-page already exists on many pages

The conflict detection didn't include `og:title` or `og:description` because those are intentionally per-page values (E-2 handles them). E-1's job is the chrome that's identical for every page: image, locale, site_name, twitter, author, entity stubs. The 32 files with existing `twitter:card` got their value overridden to `summary_large_image` (the new standard), but per-page descriptions remained intact.

---

## 10. All Files Touched

| Category | Count |
|---|---:|
| Templates updated (EN + HE) | 2 |
| Migrated EN files updated | 174 |
| Migrated HE files updated | 605 |
| Files recovered from pre-existing truncation | 2 (subset of the 174 EN) |
| `_pilot/e1-template-additions.md` (this report) | 1 |
| `_backup-pre-migration/` entries created | 0 (per task spec — git is the rollback target for E-1) |
| `main.css` changes | 0 |
| JavaScript changes | 0 |

**Total file touches: 781 unique files** (2 templates + 779 migrated pages).

---

## 11. Moshe's Verification Checklist

### Spot-check via GitHub Desktop diff view (before pushing)

1. **`_templates/Academic-Content-EN.html`** and **`_templates/Academic-Content-HE.html`** — confirm the E-1 block appears between viewport meta and favicon link. Verify 5 region placeholders are still present and the templates still end with `</html>`. Confirm EN template uses `og:locale=en_US` and HE uses `og:locale=he_IL`.

2. **Random EN migrated page** (e.g., `index.html` or `torah-weave/Genesis/genesis-unit-1/genesis-unit-1.html`) — find the E-1 block. Confirm 12 meta tags + JSON-LD stub. Confirm rest of file untouched.

3. **Random HE migrated page** (e.g., `Mishnah-New/Hebrew/Text/Seder Moed/Masechet Megillah/Masechet Megillah Perek 1.htm`) — same check, but `og:locale=he_IL`.

4. **MAVO specifically** (`Mishnah-New/Hebrew/Articles/MAVO.htm`) — this page had ZERO schema before. Confirm it now has exactly 1 JSON-LD block (the E-1 stub with the 3 `@id` references).

5. **Torah Portal** (`Torah-New/English/Torah Portal.htm`) — was truncated; recovered in-line. Confirm it ends with `</html>` and has full content including the Track 1 Mishnah dropdown.

6. **the-hidden-warp** (`torah-weave/Genesis/genesis-analysis/the-hidden-warp.html`) — was severely truncated (44 KB lost); fully re-migrated from backup. Confirm content matches the pre-truncation expectation: title "Part C: The Three Rows | Genesis Commentary | Torah Weave", full essay content.

### Push, then test live

- **Google Rich Results Test** on `https://chaver.com/`, `https://chaver.com/about-Moshe-Kline`, and one Mishnah chapter page → should validate without warnings. Each should report Person + Organization + WebSite entity references.
- **Twitter Card Validator** on any 3 pages → should show the og-default-1200x630.png as the card image.
- **Facebook Sharing Debugger** on the same pages → same.

### Rollback if needed

Git is the rollback target for E-1. Once committed:

```bash
git revert <e1-commit-hash>
```

Pre-commit: GitHub Desktop's "Discard changes" works per-file.

---

## 12. What's Next

E-1 has propagated the canonical Person, Organization, and WebSite `@id`s across the entire corpus. Every page now declares the same author entity, the same publisher entity, the same site identity, and the same default OG image.

The corpus is now ready for **E-2 — per-page generation** of:
- `<link rel="canonical">` (path-derived per-page URL)
- `<meta property="og:url">` (matches canonical)
- `<meta property="og:title">` (from existing `<title>`)
- `<meta property="og:description">` (from existing meta description, or smart-extracted from first `<p>` in `<main>` if missing)
- `<meta property="og:type">` (`article` for content pages, `website`/`profile` for portals/about)
- `Article` schema (per-page, with `author`/`publisher` references to canonical `@id`s — which now exist)
- `BreadcrumbList` schema (from URL path + an override map for special segments)

E-2 will run on the same 779-file set with the same surgical-injection pattern.

---

## 13. Out of Scope (per task spec)

- Per-page canonical URLs (E-2)
- Per-page og:url, og:title, og:description (E-2)
- Per-page BreadcrumbList (E-2)
- Per-page Article schema (E-2)
- Per-page og:type override (E-2)
- hreflang (E-2 — for the EN↔HE home pair)
- Bespoke schema on hebrew home, Torah Portal, Mishnah portals, MAVO, JBL article (E-3)
- `award` field on Person (deferred — Moshe to decide)
- WordPress orphan cleanup (separate task)
- DWT cleanup (separate task)
