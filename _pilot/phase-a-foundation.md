# Phase A — Foundation Before Bulk Migration

**Date:** 2026-05-13
**Scope:** Prerequisite work before Phase B (bulk migration of ~906 files). Four parts: mobile CSS rules, migration-logic updates, provenance markers on the 4 pilot pages, three new pilot migrations.
**Status:** All four parts complete. 3 new pilot pages migrated and verified (13/13 checks each). **Not committed.**

---

## Part 1 — Two Mobile CSS Rules Added to `main.css`

Inserted into the existing content-area `@media (max-width: 768px)` block, adjacent to the recent `.matrix-table` shrink-to-fit rule (lines 3107–3132 of `main.css`).

### Rule 1: Cap inline absolute-width elements

```diff
+ /* Cap any inline-styled absolute width at viewport on mobile.
+    Catches the ~20 pages with style="width: 800/900px" overflow risks. */
+ main [style*="width:"] {
+     max-width: 100% !important;
+     height: auto;
+ }
```

Targets the 20 files identified in the pre-migration survey (mostly older Mishnah pages with `style="width: 900px"` on wrapper divs/images). Caps each at viewport on mobile only; desktop unchanged.

### Rule 2: Scripture-table shrink-to-fit

```diff
+ /* Scripture tables (99 pages, especially Avot chapter pages with many tables).
+    Same shrink-to-fit approach as .matrix-table. */
+ .scripture-table {
+     font-size: 0.75em;
+     line-height: 1.3;
+ }
+ .scripture-table th,
+ .scripture-table td {
+     padding: 4px 3px !important;
+     word-break: break-word;
+ }
```

Mirrors the `.matrix-table` approach but with slightly larger numbers (0.75em vs 0.65em, 4px/3px vs 3px/2px) — scripture-tables typically have fewer columns than matrix-tables, so don't need to shrink as aggressively. Validated on `avot-chapter-4.html` which has 32 scripture-tables (the densest case in the corpus).

---

## Part 2 — Migration-Logic Updates (`_pilot/migration-logic.md`)

Three additions to the existing migration logic document:

### 2.1 New "For `English.dwt`-attached pages" section

Added after the existing `hebrew.dwt` section. Covers two variants:

- **Variant A (31 files):** standard 5-region set, same direct mapping as `Academic-Content-DWT.dwt`.
- **Variant B (6 files in `torah-commentary-project/Commentaries/`):** 4 regions, with `writehere` → `content` rename and no `meta` region (defaults to empty).

Includes a `map_english_dwt_regions(raw)` reference function that selects the variant at runtime based on whether `writehere` is in the region set.

### 2.2 New Section 5b: `rendered-from` Provenance Marker (REQUIRED)

After CSS cleanup, every migrated file gets a comment marker injected immediately after `<!DOCTYPE html>`:

```html
<!DOCTYPE html>
<!-- rendered-from: _templates/Academic-Content-EN.html @ 2026-05-13T07:42:00Z -->
<html lang="en">
```

Records template path + ISO 8601 UTC timestamp. Makes "which template owns this page" explicit and greppable. Re-renders update the timestamp on the existing marker rather than appending a second one (idempotent via `insert_or_update_provenance()`).

### 2.3 New verification check 13

Added to Section 6 (Verification Checks):

> **Check 13: `rendered-from` provenance marker present.** Migrated file has exactly one `<!-- rendered-from: <template> @ <ISO-8601-timestamp> -->` comment matching the template path used. Zero or multiple markers ⇒ fail.

---

## Part 3 — Provenance Markers Backfilled on 4 Pilot Pages

The 4-page pilot ran 2026-05-12; used that as the backfill timestamp.

| File | Marker added |
|---|---|
| `torah-weave/leviticus-19-ark-at-the-center.html` | `<!-- rendered-from: _templates/Academic-Content-EN.html @ 2026-05-12T12:00:00Z -->` |
| `torah-weave/Woven-Torah-Method.html` | `<!-- rendered-from: _templates/Academic-Content-EN.html @ 2026-05-12T12:00:00Z -->` |
| `Mishnah-New/Hebrew/Articles/MAVO.htm` | `<!-- rendered-from: _templates/Academic-Content-HE.html @ 2026-05-12T12:00:00Z -->` |
| `hebrew index.html` | `<!-- rendered-from: _templates/Academic-Content-HE.html @ 2026-05-12T12:00:00Z -->` |

All 4 verified: marker is the first line after `<!DOCTYPE html>`, exactly one occurrence, file size +83 bytes each.

---

## Part 4 — Three New Pilot Migrations

### Per-file results — all three passed all 13 checks

| Page | DWT | Template | Test purpose | Orig → New | Status |
|---|---|---|---|---|---|
| `Articles/TenWrd1.html` | `English.dwt` (5-region) | `_templates/Academic-Content-EN.html` | `English.dwt` standard-regions case (the 31-file population) | 99,259 → 101,716 B (+2,457) | **ALL 13 PASS, SAVED** |
| `torah-commentary-project/Commentaries/Deuteronomy/deuteronomy-unit-3.html` | `English.dwt` (writehere) | `_templates/Academic-Content-EN.html` | `English.dwt` with `writehere` region remap | 61,725 → 43,938 B (−17,787) | **ALL 13 PASS, SAVED** |
| `Mishnah-New/English/Articles/avot-chapter-4.html` | `Academic-Content-DWT.dwt` | `_templates/Academic-Content-EN.html` | Page with 32 `scripture-table` + schema.org JSON-LD | 173,139 → 170,574 B (−2,565) | **ALL 13 PASS, SAVED** |

(Sizes reported are post-cleanup. The `deuteronomy-unit-3` shrinks substantially because the source's body was largely a stale custom nav/footer that gets replaced by the new template — and its `writehere` region was actually empty in the original.)

### Verification — all 13 checks per file

The same 13 checks (incl. the new check 13 `rendered-from` marker) passed on every page. Selected highlights:

**Articles/TenWrd1.html:**
- Content word count: 6,975 → 6,975 (ratio 1.000)
- Title: `"The Decalogue"` preserved
- 4 OG tags + 2 schema.org JSON-LD blocks preserved
- 1 content-area href preserved (0 lost from `<main>`)
- 1 inline `<style>` orphan rule remaining (inside `@media print`, kept intentionally)

**deuteronomy-unit-3.html (`writehere` variant):**
- `writehere` region was empty in source → migrated to empty `<main>` (content word count 0 → 0, ratio skipped)
- Title `"Home"` preserved
- 0 hrefs/og/schema.org in source (none lost)
- Confirms the `writehere` → `content` remap works correctly

**avot-chapter-4.html (large scripture-table page):**
- Content word count: 18,880 → 18,880 (ratio 1.000)
- Title: `"Avot Chapter 4: What Did Shmuel HaKatan Say?"` preserved
- 4 OG tags + 1 schema.org JSON-LD preserved
- Content `<a>` set: 0 lost
- 32 `<table class="scripture-table">` preserved unchanged; new `.scripture-table` mobile CSS will apply on phones

### One nontrivial finding — `<main>`-scoped href check correction

My first script run used a whole-document URL-set diff for check #8 ("internal refs preserved"), which **false-positively failed on 2 of 3 pages** because the new template's nav/footer has different URLs than the old DWT-baked nav/footer (e.g., `English.dwt` had `/Mishnah-New/English/Mishnah%20Portal.htm` in its nav; the new template has `/Mishnah/TheMishnah.htm`).

Fix: scope the href check to the source's `content` region vs. the migrated file's `<main>` content only. This isolates content-level links from nav/footer chrome that legitimately changes via the template swap.

After the fix, all three pages passed cleanly. The bulk migration script's check 8 should use the same `<main>`-scoped comparison.

### Critical safety bug found during Part 4 — idempotency required

During the first migration run, I made a mistake that the bulk migration script must guard against:

1. Run 1: `avot-chapter-4.html` migrated successfully and got saved (file size went from 174,216 → 170,574 bytes, with `rendered-from` marker added).
2. Run 2 (refined check 8 logic): re-read the now-migrated file, tried to extract DWT regions — but the file no longer has `#BeginTemplate` markers because it's already migrated. Extracted empty regions. Rendered the template with empty placeholders, producing a 12,086-byte stub. Saved the stub over the previously-good migrated file.

I restored from `_backup-pre-migration/` and re-ran with an **idempotency check** added at the start of the script:

```python
if '#BeginTemplate' not in orig:
    # Already migrated — skip.
    return {'status': 'skipped_already_migrated'}
```

After this guard, re-running the migration script is now safe — already-migrated pages are skipped, only DWT-attached source files get re-rendered. **The bulk migration script MUST include this guard** to avoid the same data-loss pattern at scale.

Documenting this in the migration logic: see the new "Idempotency" subsection in Section 5b, plus the idempotency-guard recommendation in the bulk script outline.

---

## 5. Recommendations for Phase B (Bulk Migration)

Based on what was learned during Phase A, the bulk migration logic needs these refinements before the bulk run:

### 5.1 Idempotency guard (MANDATORY)

Skip files that have already been migrated (no `#BeginTemplate` present). Without this, re-running the bulk script for any reason — for example, after fixing a bug mid-run, or after a partial failure — will overwrite valid migrated files with broken stubs.

```python
if '#BeginTemplate' not in source:
    return {'status': 'skipped_already_migrated'}
```

Place this check at the very top of the per-file processing function. The same guard is now also documented in `_pilot/migration-logic.md` Section 5b.

### 5.2 `<main>`-scoped href check (MANDATORY)

Update check #8 to scope the href set comparison to the source's `content` region vs. the migrated file's `<main>` element. Don't compare whole-document URL sets — the template nav/footer URLs legitimately differ, and that's not a regression.

### 5.3 Already covered by Part 2 of this task

These were addressed by the migration-logic updates:

- ✓ `English.dwt` as a recognized DWT type (5-region variant + `writehere` variant)
- ✓ `writehere` → `content` remap
- ✓ `rendered-from` provenance marker injection (with idempotent insert-or-update)
- ✓ Check 13 (provenance marker present)

### 5.4 Don't forget the existing requirements

From the 4-page pilot's recommendations and the survey:

- Run `clean_nav_css_from_inline_style()` after template substitution (catches the template-inherited orphan nav CSS).
- Backup to `_backup-pre-migration/<path>` before overwriting.
- Path/DWT-based language detection (handles the 709 `lang="en"`-but-actually-Hebrew files).
- Skip-list the 24 manual-review files from the survey rather than auto-migrating them.

### 5.5 Smaller observations from Part 4

- **Size shrinkage on `writehere` pages is expected.** `deuteronomy-unit-3` went from 61.7 KB to 43.9 KB — most of the original was custom-baked nav/footer chrome that the new template replaces. The content `writehere` region was empty (the page exists as a stub). Worth confirming this is intentional for the other 5 `writehere` pages.
- **Schema.org JSON-LD preservation worked.** Both `avot-chapter-4.html` (1 schema.org block) and `TenWrd1.html` (2 schema.org blocks) had their inline JSON-LD scripts preserved exactly in the migrated `meta` region. No special handling needed.
- **`English.dwt` page sizes can grow.** `TenWrd1.html` grew from 99 KB to 101 KB after migration. The new template scaffolding (nav + footer + main.css link) is heavier than the old `English.dwt` scaffolding. Normal.
- **OneDrive sync delays.** During Phase A I encountered the same bash-mount-staleness issue from earlier tasks — `cp` operations sometimes need 2-3 seconds to be visible to subsequent reads. The bulk script should add a small `time.sleep(0.05)` after writes if it depends on re-reading the just-written file, OR keep an in-memory copy of what was just written. Not critical but a robustness improvement.

---

## 6. Files Touched

| File | Action |
|---|---|
| `torah-weave/Admin/Assets/CSS/main.css` | 2 new rule groups inside `@media (max-width: 768px)`: inline-width cap + `.scripture-table` shrink-to-fit (10 new lines) |
| `_pilot/migration-logic.md` | Section 3 expanded with `English.dwt` handling + `writehere` remap; new Section 5b on `rendered-from` provenance marker (incl. idempotent injection function); new check 13 added to Section 6 |
| `torah-weave/leviticus-19-ark-at-the-center.html` | `<!-- rendered-from: ... -->` marker added |
| `torah-weave/Woven-Torah-Method.html` | same |
| `Mishnah-New/Hebrew/Articles/MAVO.htm` | same |
| `hebrew index.html` | same (manually re-ordered by the user/linter afterwards; preserved) |
| `Articles/TenWrd1.html` | **Migrated** (all 13 checks pass); backup in `_backup-pre-migration/Articles/TenWrd1.html` |
| `torah-commentary-project/Commentaries/Deuteronomy/deuteronomy-unit-3.html` | **Migrated** (all 13 checks pass); backup in `_backup-pre-migration/...` |
| `Mishnah-New/English/Articles/avot-chapter-4.html` | **Migrated** (all 13 checks pass); backup in `_backup-pre-migration/...` |
| `_pilot/phase-a-foundation.md` | This report |

---

## 7. What Moshe Tests Before Phase B

For each of the 3 new pilot pages (and a spot-check of the 4 original ones):

**Desktop:**
- Page loads
- Hover over nav dropdowns
- Internal links work
- Content renders identically to before migration (for content-only pages — nav/footer chrome is intentionally new)
- Footer is the new 4-section design

**Mobile (incognito):**
- Hamburger icon visible at the top-right (NOT off-screen)
- Tap hamburger → menu opens with all top-level items
- Tap dropdown buttons → submenus expand inline
- Tap leaf items → navigation works
- Tap outside → menu closes
- Content fits viewport — no horizontal scroll on the page itself
- On `avot-chapter-4.html`: the 32 scripture-tables should each be small but readable (the new `.scripture-table` mobile rule shrinks them)
- On `TenWrd1.html`: any inline-styled wide elements should be capped at viewport (new `main [style*="width:"]` rule)
- On `deuteronomy-unit-3.html`: the page is essentially empty content (the `writehere` region was empty); should render the new template chrome with no body content

**Spot-check non-migrated DWT pages** to confirm they still work — the new mobile CSS rules don't break them (the rules target `.matrix-table`, `.scripture-table`, and `main [style*="width:"]` — none of which clash with the old `.menu-toggle`/`.main-nav` rules still in those legacy pages).

If all checks pass on the 3 new pages + the spot-check of a few legacy DWT pages, Phase B is ready to run.
