# Phase B — Safe-Subset Bulk Migration

**Date:** 2026-05-13
**Scope:** Migrate the 761 DWT-attached pages that match all 7 safe-subset criteria. Edge cases (`English.dwt`, `hebrew.dwt`, orphans, multi-footer, high-traffic exclusions, missing-region skeletons) deferred to future individual tasks.
**Status:** **761 of 761 files migrated successfully. 0 errors. 0 skipped.** Originals byte-identically backed up to `_backup-pre-migration/`. **Not committed.**

---

## 1. Headline Numbers

| Metric | Count |
|---|---:|
| Files attempted | 761 |
| **Migrated successfully** | **761** (100%) |
| Skipped | 0 |
| Errors | 0 |
| Backup-verified files | 768 (incl. 7 from earlier pilot tasks) |
| Backup directory size | 20.6 MB |
| Net size delta of migrated files | **−2.4 MB** (cleaner output: 19.77 MB → 17.34 MB) |
| Wall-clock time | 21 s for the initial 733 + ~5 s for the 28-file retry |

---

## 2. By Language and DWT

| Language | Count |
|---|---:|
| **EN** | 161 |
| **HE** | 600 |

| Source DWT | Count |
|---|---:|
| `Academic-Content-DWT.dwt` | 761 (100%) |

(By design — the safe-subset criteria required exactly `Academic-Content-DWT.dwt`. The 37 `English.dwt` and 16 `hebrew.dwt` files in the survey are out of scope for this task.)

### By top-level directory

| Directory | Count |
|---|---:|
| `Mishnah-New` | 529 |
| `torah-weave` | 224 |
| `Torah-New` | 6 |
| `General` | 2 |

The vast majority of migrations are Hebrew Mishnah chapter pages (`Mishnah-New/Hebrew/Text/Seder*/Masechet*/`).

---

## 3. Skip List

**Empty.** Every file in the target list migrated cleanly after the bug fix described in Section 7 below.

### Initial run skip pattern (resolved)

The first pass skipped 28 files (all Genesis/Leviticus analysis, Genesis units, Exodus unit 9, Deuteronomy unit 8 commentary parts, and `torah-weave/commentary.html`) for failing checks 5 and/or 8 — word-count ratios in the 0.92–0.99 range and 1–5 hrefs reported missing from `<main>`.

**Root cause:** my verification regex `<main[^>]*>(.*?)</main>` is non-greedy. When a source page's `content` editable region contains its OWN `<main>` tag (e.g., the genesis-map page's citation block), the migrated file has two `<main>` elements: the template's `<main class="content-wrapper">` and the inner one from content. Non-greedy match captures from outer-open to inner-close, missing the text and links between inner-close and outer-close (typically the suggested-citation block at the very end of the page).

**Fix:** match the OUTERMOST `<main class="content-wrapper">` by anchoring on the template's specific opening tag and the LAST `</main>` in the document via string `.find()` and `.rfind()`. Re-ran the 28 failures; all passed cleanly.

**The migration itself was always byte-correct** — the bug was in the verification only. No content was lost; the saved migrated files contain the full source content region. The 28 retries didn't need re-extraction; just re-verification with the corrected logic.

---

## 4. `lang_corrected` Events

**600 of 600 Hebrew pages** had their declared `<html lang="en">` overridden to `<html lang="he" dir="rtl">` via path/DWT-based detection. This matches the survey's 709 mismatch count minus the orphan HE pages (90 HE orphans don't appear in Phase B) and the excluded HE pilot files.

These 600 Hebrew pages had been declaring English as their language for years — accessibility tools (screen readers, browser translation prompts) and search engines were treating them as English-language pages. The migration silently fixes this for every reached HE page.

The single biggest correctness improvement of Phase B is probably this one detail — the new HE template's `<html lang="he" dir="rtl">` makes 600 pages correctly self-describe as Hebrew RTL content. The visual change is minimal; the semantic and SEO impact is substantial.

---

## 5. Backup Directory Stats

| Metric | Value |
|---|---|
| File count | 768 |
| Total size | 20.6 MB |
| Location | `_backup-pre-migration/` (mirrors source directory structure) |
| Backup ↔ migrated file count match | **761 migrated** + **7 from earlier pilot tasks** (the 4 original pilots + 3 Phase A pilots) = **768** ✓ |

### Rollback paths (in order of granularity)

**Single file:**
```bash
cp _backup-pre-migration/<rel-path> <rel-path>
```

**All migrated files at once:**
```bash
cp -r _backup-pre-migration/* .
```

**Via git (preferred if committed/pushed):**
```bash
git revert <commit-hash>
```

All three are equally valid. Backups are the safety net for pre-commit state.

---

## 6. Spot-Check Samples

5 random samples per top-level directory for browser verification (desktop AND mobile). On desktop, confirm the page renders with the new nav at top, hover dropdowns work, content is unchanged. On mobile (incognito), confirm hamburger menu opens, no horizontal overflow, tables render correctly via the new `.matrix-table` / `.scripture-table` rules.

### `Mishnah-New` (529 total — 5 random samples)

```
Mishnah-New/Hebrew/Text/Seder Nezikin/Masechet Baba Kama/Masechet Baba Kama Perek 6.htm
Mishnah-New/Hebrew/Text/Seder Nashim/Masechet Yevamot/Masechet Yevamot Perek 5.htm
Mishnah-New/Hebrew/Text/Seder Nashim/Masechet Nedarim/Masechet Nedarim Perek 9.htm
Mishnah-New/Hebrew/Text/Seder Moed/Masechet Shabbat/Masechet Shabbat Perek 14.htm
Mishnah-New/Hebrew/Text/Seder Moed/Masechet Chagigah/Masechet Chagigah Perek 2.htm
```

These are Hebrew Mishnah chapter pages — verify Hebrew text RTL flow + scripture tables shrink correctly on mobile.

### `torah-weave` (224 total — 5 random samples)

```
torah-weave/Deuteronomy/deuteronomy-unit-5/deuteronomy-unit-5.html
torah-weave/Deuteronomy/deuteronomy-unit-4/deuteronomy-unit-4.html
torah-weave/Exodus/exodus-unit-14/exodus-unit-14.html
torah-weave/Genesis/genesis-analysis/overview.html
torah-weave/Genesis/genesis-unit-10/genesis-unit-10.html
```

These are English Torah unit pages — verify matrix-tables render on desktop (full size) and shrink-to-fit on mobile (`font-size: 0.65em` + tight padding).

### `Torah-New` (6 total)

```
Torah-New/English/Torah Portal.htm
Torah-New/English/Articles/The Torah - A Handbook of Prophecy.html
Torah-New/English/Articles/The Creation Weave.htm
Torah-New/English/Articles/The Literary Structure of Leviticus.htm
Torah-New/English/Articles/The Decalogue.html
```

The Torah Portal is a major landing page; deserves special attention.

### `General` (2 total)

```
General/Color Codes/English Color Code.htm
General/Woven Text.htm
```

The color code guide is referenced from the nav and is critical Moshe verifies it renders correctly.

### Recommended 3-URL browser test

For the deploy spot-check, pick one from each:

1. **`/Mishnah-New/Hebrew/Text/Seder Moed/Masechet Megillah/Masechet Megillah Perek 1`** (any HE Mishnah chapter — confirms RTL + lang correction + new Hebrew nav)
2. **`/torah-weave/Genesis/genesis-unit-1/genesis-unit-1`** (EN Torah unit with matrix-table — confirms desktop layout + mobile shrink-to-fit)
3. **`/torah-weave/Genesis/genesis-analysis/the-map-of-genesis`** (one of the formerly-failed pages — confirms the nested-`<main>` content was preserved correctly)

---

## 7. Anomalies and Patterns Encountered

### 7.1 The nested-`<main>` verification bug

Documented in Section 3. Worth highlighting for the migration-logic doc — the check 5 and 8 regex need to be updated to use the outermost-`<main>` extraction so future migrations don't false-positive-fail on pages where the source content includes its own `<main>` tag.

**Recommended migration-logic.md update:** in Section 6 (Verification Checks), the implementation note for checks 5 and 8 should say:

```python
# Extract migrated content correctly even if source has nested <main>
marker = '<main class="content-wrapper">'
start = final.find(marker)
end = final.rfind('</main>')
new_main_html = final[start + len(marker):end] if start >= 0 and end > start else ''
```

Not a regex; use string `.find()` / `.rfind()` to avoid the non-greedy regex trap.

### 7.2 Size shrinkage is universal

Net delta of −2.4 MB across 761 files (avg ≈3 KB shrinkage per file, ~12% reduction). The pre-migration files carried the full DWT-baked nav + footer scaffolding in their body. The migrated files reference the new template's `<main>` content only; the nav/footer are template scaffolding that doesn't bloat individual page sizes. This is purely additive — the saving applies once per page, repeated 761 times.

### 7.3 `lang_corrected` rate is essentially universal for HE pages

All 600 HE pages had `lang="en"` in their original `<html>` tag. The path-based override fixed 100% of them. Worth noting: this means the historic Hebrew corpus has been mis-labeled at the document level for as long as it's existed. Phase B silently fixes this. No HE pages had `lang="he"` correctly declared in the source.

### 7.4 No `English.dwt` or `hebrew.dwt` files migrated

By design — those are outside the safe subset. The 2 published `English.dwt` files (`General/Contact.htm` is one) and 4 published `hebrew.dwt` files are deferred to future individual tasks. They continue to work fine on the old DWT until that work is done.

### 7.5 Heavy concentration in `Mishnah-New/`

529 of 761 files (70%) are in `Mishnah-New/Hebrew/Text/Seder*/Masechet*/`. These are Mishnah chapter pages from the Torah/Mishnah scholarship corpus. The migration of these will be the most visible change post-deploy — every Hebrew Mishnah chapter is now on the new template with the new Hebrew nav and lang correction.

---

## 8. What's Left for Later (Not in This Task)

Per the task spec's "What's left for later" list — these are still pending:

- 2 published `English.dwt` files (separate small task)
- 4 published `hebrew.dwt` files (separate small task)
- High-traffic exclusions: `Torah-New/English/Text/Torah-pdf.html`, `Mishnah-New/Hebrew/Text/mishnah-pdf.html`, `about-Moshe-Kline.html`, `index.html` — migrate individually with careful before/after comparison
- 4 multi-footer files — individual review
- 13 published-but-content-empty skeleton pages (the Deuteronomy/Numbers units that lack `content` regions) — fill content first, then migrate
- 140 orphans — Moshe-triaged at his pace (the audit report `_pilot/published-files-audit.md` has the list)
- DWT cleanup — archive `Dynamic Web Templates/*.dwt` once nothing references them
- Stale CSS cleanup — remove `.menu-toggle` and `.main-nav` rules from `main.css` after all migrations complete

None of these blocks deploying the safe-subset.

---

## 9. Files Touched

| Category | Count |
|---|---|
| Migrated source files (in working tree) | 761 |
| Backups created in `_backup-pre-migration/` | 761 (plus 7 retained from earlier pilots = 768 total in backup dir) |
| Reports written | 2 (`_pilot/phase-b-safe-targets.txt`, `_pilot/phase-b-progress.md`, `_pilot/phase-b-safe-subset.md`) |
| Templates modified | 0 |
| `main.css` modified | 0 |
| JS modified | 0 |
| Commits | 0 (Moshe pushes when ready) |

---

## 10. Moshe's Deploy Checklist

Per the task spec's Step 5:

1. **Review this report.** Skim Sections 5 (backups), 3 (skip list — empty ✓), 7 (anomalies).
2. **Spot-check 5–10 files via GitHub Desktop's diff view.** Pick from Section 6 samples. Confirm content preserved, new chrome correct, provenance marker present immediately after `<!DOCTYPE html>`.
3. **Test 3 sample URLs** locally if possible (the 3-URL list in Section 6). Desktop + mobile in incognito.
4. **If everything looks good: push via GitHub Desktop.** Cloudflare auto-deploys.
5. **After deploy: re-test the same 3 URLs live**, incognito, desktop + mobile.
6. **If anything's wrong after deploy:** `git revert` (cleanest) or restore from `_backup-pre-migration/` (per-file granularity).

The .git/index.lock issue from the earlier task may recur if Cowork operations have run since the last commit. If so: close GitHub Desktop, delete `.git/index.lock`, reopen.
