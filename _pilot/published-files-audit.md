# Published-Files Audit — Link-Traversal Crawl

**Date:** 2026-05-13
**Method:** BFS crawl from `/` + `/hebrew index` + every URL in `sitemap.xml` + every nav/footer link in the two templates. Followed all internal `href`/`src`/`action` attributes. Cycle-detected via visited-set.
**Status:** Audit complete. **PAUSED for Moshe's review before Step 6 (archive operations).** No files modified.

---

## ⚠ This Audit Did NOT Move Any Files

Per the task spec, Step 6 (archive operations) requires explicit confirmation. I have not moved anything. The findings below are ready to act on once you've reviewed the orphan list.

---

## 1. Headline Counts

| Category | Count |
|---|---:|
| **Seeds (deduplicated)** | 869 |
| Initial queue after seed resolution | 862 |
| Seed URLs that didn't resolve to a file | 2 |
| **Files visited during crawl** | 1,837 |
| **Files reached** (page + asset) | 1,837 |
| **Published + DWT-attached (Phase B targets)** | **790** |
| **Orphan + DWT-attached** | **140** |
| **Published, NOT DWT-attached** (standalone) | 228 |
| Broken internal links (raw) | 2,683 |
| — false positives (`page_view`, `timing` strings) | 428 |
| — WordPress-export cruft (`./feed/index.html`, `./wp-json/index.html`, etc.) | 1,671 |
| — **Content-link broken targets** | **584** |
| External links seen | 4,737 |
| Unique external hosts | 26 |
| Sitemap URLs total | 820 |
| Sitemap URLs resolved to files | 820 (100%) |
| Sitemap URLs unresolved (would 404 if visited) | **0** ✓ |
| Reached but NOT in sitemap | 201 |
| Sitemap files NOT reached (declared but unlinked) | 0 ✓ |

The previous survey's 930 DWT-attached count is now resolved as **790 Phase B targets + 140 orphans**.

---

## 2. Phase B Migration Scope (Updated)

**790 files** to migrate, down from the survey's 930.

### By language

| Language | Count |
|---|---:|
| EN | 173 |
| HE | 617 |

### By source DWT

| DWT | Count |
|---|---:|
| `Academic-Content-DWT.dwt` | 784 |
| `English.dwt` | 2 |
| `hebrew.dwt` | 4 |

Note how drastically the `English.dwt` and `hebrew.dwt` counts drop once orphans are removed: 37 → 2 and 16 → 4. **Nearly all `English.dwt` and `hebrew.dwt` pages are orphans** (35 of 37, and 12 of 16 respectively). The two surviving `English.dwt` pages are `General/Contact.htm` and possibly `Mishnah-New/English/Articles/TheArt-H.htm` (or similar). The 4 surviving `hebrew.dwt` pages are mostly active Hebrew Mishnah introduction pages.

---

## 3. Orphan List (140 DWT-Attached Files)

Grouped by top-level directory. After Moshe's review, authorized orphans will be moved to `_archive/<original-path>` in Step 6.

### Counts by directory

| Directory | Count |
|---|---:|
| `Mishnah-New` | 81 |
| `Torah-New` | 23 |
| `torah-weave` | 12 |
| `Mishnah` | 10 |
| `torah-commentary-project` | 7 |
| `General` | 5 |
| `(root)` | 1 |
| `Articles` | 1 |
| **Total** | **140** |

### Detail by directory

#### `Mishnah-New` (81 orphans)

Mostly "Pirkei Masechet" tractate-index pages (`Mishnah-New/Hebrew/Text/Seder Kodashim/Masechet Arakhin/Pirkei Masechet Arakhin.htm` etc.) — index pages for individual masechet chapters that aren't linked from the main nav. Two of these are old Hebrew Articles (`CfrHnnia.htm`, `TheWholeStructure.htm`). One is `Mishnah-New/English/mishnah-viewer.html` — a JS viewer prototype.

Sample of 8 (full list in `/tmp/crawl_results.json` → `orphan_dwt`):

```
Mishnah-New/English/mishnah-viewer.html
Mishnah-New/Hebrew/Articles/CfrHnnia.htm
Mishnah-New/Hebrew/Articles/TheWholeStructure.htm
Mishnah-New/Hebrew/Text/Seder Kodashim/Masechet Arakhin/Pirkei Masechet Arakhin.htm
Mishnah-New/Hebrew/Text/Seder Kodashim/Masechet Bekhorot/Pirkei Masechet Bekhorot.htm
Mishnah-New/Hebrew/Text/Seder Kodashim/Masechet Chullin/Pirkei Masechet Chullin.htm
Mishnah-New/Hebrew/Text/Seder Kodashim/Masechet Kinnim/Pirkei Masechet Kinnim.htm
Mishnah-New/Hebrew/Text/Seder Kodashim/Masechet Kritot/Pirkei Masechet Kritot.htm
...
```

**Recommend:** these are likely intentional — the "Pirkei Masechet" pages may be obsolete index pages from the old DWT structure. Worth a quick sample check before archiving.

#### `Torah-New` (23 orphans, all in `English/`)

The entire `Torah-New/English/Articles/Leviticus The Ways of Holiness/` directory (8 chapter files + supporting pages) and most of `Torah-New/English/Text/Leviticus/` (15 unit files). These appear to be a complete unpublished chapter set + a unit-by-unit alternate publication.

```
Torah-New/English/Articles/Leviticus The Ways of Holiness/  (8 files)
Torah-New/English/Text/Leviticus/                          (15 files)
```

**Recommend:** the Ways of Holiness directory is likely an unfinished draft series. The Leviticus Unit pages are likely superseded by `torah-weave/Leviticus/leviticus-unit-X/` (which ARE reached). Confirm with Moshe.

#### `torah-weave` (12 orphans)

Mix of admin/test pages and unfinished drafts:

```
torah-weave/Admin/Assets/english-color-code.html               (admin asset)
torah-weave/Admin/Assets/hebrew-color-code.html                (admin asset)
torah-weave/Admin/DWT-test_1.html                              (test page)
torah-weave/Admin/Unit Commentary Template.html                (template/scaffolding)
torah-weave/Commentary/Commentary.html                         (?)
torah-weave/Genesis/genesis-analysis/The Structure of Genesis (short form).html
torah-weave/Genesis/genesis-analysis/The Structure of Genesis from Gemini.html
torah-weave/Genesis/genesis-analysis/The Structure of Genesis.html
torah-weave/Genesis/genesis-analysis/The Structure of Genesis1.html       (numeric suffix = old version?)
torah-weave/Genesis/genesis-unit-9/Akedah divine names essay.html         (draft essay)
torah-weave/Genesis/hebrew-genesis-unit-1/test.html                       (test page)
torah-weave/The-Sixth-Book-of-theTorah.html                               (draft of essay — see _pilot/The-Sixth-Book-of-theTorah.html?)
```

**Recommend:** the `Admin/` files and `test.html` files are clearly orphans. The `Genesis/genesis-analysis/*.html` files (4 of them) look like multiple drafts/versions of the same content — worth Moshe's input. The Akedah essay and Sixth-Book essay may be intentional unpublished drafts that should stay in the repo.

#### `Mishnah` (10 orphans)

All `Mesechet *.htm` files — the OLD Mishnah directory structure (vs. the active `Mishnah-New/`). These are pre-migration relics:

```
Mishnah/Mesechet Bechorot.htm
Mishnah/Mesechet Chalah.htm
Mishnah/Mesechet Damai.htm
Mishnah/Mesechet Kelaim.htm
Mishnah/Mesechet Maaser Sheni.htm
Mishnah/Mesechet Maasrot.htm
Mishnah/Mesechet Orlah.htm
Mishnah/Mesechet Peah.htm
Mishnah/Mesechet Shviit.htm
Mishnah/Mesechet Trumote.htm
```

**Recommend:** archive all 10. The active replacements live in `Mishnah-New/Hebrew/Text/Seder.../`.

#### `torah-commentary-project` (7 orphans)

The entire directory appears orphan — confirms the survey's HIGH-risk finding:

```
torah-commentary-project/Commentaries/Deuteronomy/deuteronomy-unit-3.html  ← stub I migrated in Phase A
torah-commentary-project/Commentaries/Deuteronomy/index.html
torah-commentary-project/Commentaries/Deuteronomy/test.html
torah-commentary-project/Commentaries/Genesis/Units/genesis-unit-2.html
torah-commentary-project/Commentaries/index.html
torah-commentary-project/Commentaries/maps with commentary.html
torah-commentary-project/Commentaries/test2.html
```

**Recommend:** archive all 7. This is the entire `torah-commentary-project/` directory — appears to be an abandoned alternate-structure experiment. **The deuteronomy-unit-3 stub I migrated in Phase A is one of these.**

#### `General` (5 orphans)

```
General/Catalog.htm
General/Leviathan.htm
General/Nonlinear Texts.htm
General/The Torah and Mishnah are Visual texts.htm
General/about-page/about-page.html
```

**Recommend:** the about-page is superseded by `/about-Moshe-Kline` (reached). The other 4 are old essay/topic pages — Moshe should decide whether they're worth keeping linked or archiving.

#### `(root)` (1 orphan)

```
404.html
```

**Special case:** this is the Cloudflare Pages 404 handler — served when a URL doesn't match any file. Not linked from anywhere because it's used as a fallback. **Should NOT be archived.** Flag in the script as a known-safe orphan exception.

#### `Articles` (1 orphan)

```
Articles/TenWrd1.html
```

⚠ **This is the Phase A pilot page I just migrated**. It turns out to be orphan — not linked from anywhere reachable. The migration succeeded (all 13 checks passed), but the file isn't actually visible from the live site. **Recommend:** either find/restore the inbound link that should point to it (the page is "The Decalogue" article — likely should be linked from the Insights nav as `Torah-New/English/Articles/The Decalogue` already is, but that's a DIFFERENT file), OR archive it. Moshe's call.

---

## 4. Broken Internal Links

**2,683 raw broken-link reports**, but the actionable content reduces significantly after filtering noise:

| Category | Count | Action |
|---|---:|---|
| **False positives** (`page_view`, `timing` strings — GA event names captured by my regex from inline scripts) | 428 | Ignore — these aren't real `href`/`src` values |
| **WordPress export cruft** (`./feed/index.html`, `./wp-json/index.html`, `./xmlrpc.php?rsd`, `./wp-includes/...`) | 1,671 | These appear ~85× each because the WP-exported pages all repeat them in head metadata. Cosmetic — they won't be visible to users and don't impact rendering. Worth a one-time cleanup but not blocking Phase B. |
| **Real content-link broken targets** | **584** | Worth Moshe's review |

### Top 15 actionable broken targets (non-WP, non-false-positive)

| Count | Target URL |
|---:|---|
| 86 | `./../../research/index.html` |
| 86 | `./../../services/index.html` |
| 86 | `./../../the-voice-is-the-voice-of-yhwh-but-the-hands-are-the-hands-of-elohim/index.html` |
| 85 | `./../../../../he/color-code-guide/index.html` |
| 21 | `./../research/index.html` |
| 21 | `./../services/index.html` |
| 21 | `./../the-voice-is-the-voice-of-yhwh-but-the-hands-are-the-hands-of-elohim/index.html` |
| 14 | `/torah-weave/Deuteronomy/` |
| 14 | `/torah-weave/Deuteronomy/deuteronomy-unit-8/` |
| 11 | `https://chaver.com/Mishnah-New/English/Articles/Five-Pairs%20from-Avot1` |
| 9 | `/torah-weave/Leviticus/leviticus-analysis/the-map-of-leviticus` |
| 8 | `/torah-weave/Genesis//torah-weave/commentary` (double `/torah-weave/` — relative-path bug in source) |
| 6 | `/torah-weave/hebrew-color-code-guide/` (the not-yet-built page) |
| 6 | `/torah-weave/Torah-pdf/torah-pdf` |
| 5 | `/mishnah/` (the not-yet-built Hebrew Mishnah portal) |

The top 4 (`research/`, `services/`, `the-voice.../`, `he/color-code-guide/`) account for ~340 of the ~584 actionable broken links — these are all from the WP-exported `woven-torah/...` pages that link to pages that existed on the old WordPress site but didn't make it into the static export.

The top 10 broken-source files (which page emits the most broken links):

```
23× Mishnah-New/Hebrew/Text/Shishah Sidrei Mishnah.htm
15× woven-torah/the-principle-of-woven-texts-understanding-the-literary-paradigm/index.html
15× woven-torah/full-torah-map-2/index.html
15× woven-torah/torah_units/genesis-unit-1/index.html
14× woven-torah/the-sophisticated-literary-structure-of-leviticus-19-part-3/index.html
14× woven-torah/the-sophisticated-literary-structure-of-leviticus-19-part-2/index.html
14× woven-torah/research-articles/index.html
14× woven-torah/the-voice-is-the-voice-of-yhwh-but-the-hands-are-the-hands-of-elohim-part-1/index.html
14× woven-torah/genesis-map/index.html
14× woven-torah/the-sophisticated-literary-structure-of-leviticus-19-part-1/index.html
```

The `woven-torah/...` pages are all WP-exports linking to WP infrastructure paths that no longer exist. **For Phase B these are content-review items**, not blockers. The pages themselves are reached and will be migrated; their broken links inside the content are a separate cleanup pass.

---

## 5. Sitemap Discrepancies

### Sitemap URLs without a backing file: **0 ✓**

Every URL in `sitemap.xml` resolves to an actual file. Good — visitors landing on any sitemapped URL will see content, not a 404.

### Sitemap files NOT reached by crawl: **0 ✓**

Every file declared in the sitemap was also reached via internal links. Good — no "ghost" sitemap entries that no internal page links to.

### Reached but NOT in sitemap: **201 files**

These are published (linked from somewhere reachable) but not declared in the sitemap. Recommendations:

- **Worth adding to sitemap:** any content page that's reachable through the site's navigation but happens to be missing from the sitemap (probably an oversight from the last sitemap regeneration).
- **Worth removing from inbound links:** any page that's reached only by happenstance and isn't intended to be a public destination.

The list is large. Sample inspection of a few would help decide which subset is worth adding to sitemap. Examples (from the `reached_not_in_sitemap` list in `/tmp/crawl_results.json`):

- Many `woven-torah/torah_units/...` pages (the WordPress-style unit pages) — some are linked but not in sitemap.
- Several `Mishnah-New/Hebrew/Text/...` chapter pages.
- A few admin/asset paths that shouldn't be in sitemap anyway.

**Recommend:** review this list after Phase B is complete and regenerate sitemap from the post-migration file set.

---

## 6. Comparison to the Previous Survey + Spot Checks

### Headline shift

| Metric | Pre-crawl (survey) | Post-crawl (this audit) | Delta |
|---|---:|---:|---:|
| DWT-attached files in repo | 930 | 930 | 0 |
| Phase B migration target | ~906 (after subtracting 24 manual-review) | **790** | −116 net |
| Orphan files (per-page identification) | not measured | **140** | (new info) |

The audit finds **15% of the DWT-attached corpus is orphan** — substantial enough that running Phase B against the survey's 906-file list would have migrated 116 pages no user can reach. Those would have polluted the new template system with empty stubs (deuteronomy-unit-3 pattern) and stale alternate-version pages.

### Spot-checks (all confirmed)

| File | Expected | Found |
|---|---|---|
| `torah-commentary-project/Commentaries/Deuteronomy/deuteronomy-unit-3.html` | ORPHAN | ✓ ORPHAN |
| `torah-weave/Deuteronomy/deuteronomy-unit-3/deuteronomy-unit-3.html` | reached (real page) | ✓ REACHED |
| `Mishnah-New/Hebrew/Articles/MAVO.htm` | reached | ✓ REACHED |
| `hebrew index.html` | reached (home) | ✓ REACHED |
| `torah-weave/Woven-Torah-Method.html` | reached | ✓ REACHED |
| `Mishnah-New/English/Articles/avot-chapter-4.html` | reached | ✓ REACHED |
| `Articles/TenWrd1.html` | ⚠ unsure | **ORPHAN** — and I migrated this in Phase A! |

### The 13 Deuteronomy/Numbers skeleton pages (survey 3b)

All 13 are **REACHED** (they are linked from somewhere — probably from `torah-weave/Deuteronomy/` index pages or from the Torah Map). They are still problematic for Phase B because their source has no `content` editable region, but the migration would produce empty `<main>` content (template chrome only). Not a blocker; flag as content-empty post-migration and let Moshe fill them in over time.

---

## 7. PAUSE — Awaiting Moshe's Review Before Step 6

Per the task spec: **I have stopped here and will not run Step 6 (archive operations) without explicit confirmation.**

### What Moshe needs to review

1. **The 140-file orphan list** (Section 3 above):
   - Which orphans to archive (move to `_archive/`)?
   - Are any misidentified — actually live pages I should migrate instead?
   - The `404.html` should NOT be archived (it's Cloudflare's 404 handler).
   - `Articles/TenWrd1.html` — I already migrated it in Phase A; should I revert from backup and archive, or find an inbound link that should exist and confirm "published"?

2. **The 584 actionable broken internal links** (Section 4):
   - Most are in the WP-exported `woven-torah/...` pages linking to dead WP paths. Worth a separate content-cleanup task; not blocking Phase B.
   - A few (`/mishnah/`, `/torah-weave/hebrew-color-code-guide/`) are intentional placeholders for not-yet-built pages.

3. **The 201 reached-but-not-in-sitemap pages** (Section 5):
   - Mostly an artifact of stale sitemap regeneration. Not blocking; review post-Phase-B.

### What I'll do once confirmed

- **Step 6:** for each orphan in Moshe's confirmed-archive list, move it to `_archive/<original-path>` (preserving directory structure). Use `git mv` to keep history.
- **Step 7:** regenerate `_pilot/phase-b-targets.txt` from the post-archive repo state. This becomes the authoritative Phase B file list (will be ~790 minus whatever Moshe defers + plus any orphans confirmed to be real published files).

### Quick decision shortcut

If you want to batch-approve the obvious orphan categories, the no-brainers are:

- **All 7 `torah-commentary-project/Commentaries/`** — abandoned experimental directory
- **All 10 `Mishnah/Mesechet *.htm`** — superseded by `Mishnah-New/` structure
- **All 4 `torah-weave/Admin/`** orphans — admin/test scaffolding
- **The 4 duplicate Genesis-analysis drafts** in `torah-weave/Genesis/genesis-analysis/` (3 versions of "The Structure of Genesis" + one numbered variant)
- **`torah-weave/Genesis/hebrew-genesis-unit-1/test.html`** — test page

That's 26 of 140. The remaining 114 are largely:
- `Mishnah-New/Hebrew/Text/.../Pirkei Masechet *.htm` (chapter-index pages, may have intentional purpose)
- `Torah-New/English/.../Leviticus...` files (alternate Leviticus publication series — may be content Moshe wants to preserve)
- A few `General/` essay pages

These last 114 deserve a closer look — they may be intentional content that just lost its inbound links over time.

---

## 8. Files Produced

| File | Role |
|---|---|
| `/tmp/crawl.py` | The crawler script |
| `/tmp/crawl_results.json` | Full structured results (reached, orphan, broken, sitemap diffs) |
| `_pilot/published-files-audit.md` | This report |

No repo files modified. No archive operations performed. Awaiting confirmation.
