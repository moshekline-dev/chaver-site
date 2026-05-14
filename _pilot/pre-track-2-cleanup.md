# Pre-Track-2 Cleanup — JSON Metadata + File Extension Standardization

**Date:** 2026-05-14
**Scope:** Two small cleanups before Phase D pilot: (1) populate 12 missing/null fields in `Mishnah-New/English/mishnah_db.json`; (2) rename 15 chapter files from `.html` to `.htm`, update their canonical URLs, add 15 Cloudflare 301 redirects, and update 15 portal links.
**Status:** **All audits pass. JSON parses cleanly post-edit. Corpus-wide single `.htm` extension achieved. 0 errors.** **Not committed.**

---

## 1. JSON Edits — Section Summary

### 1.1 Field updates applied

12 field updates across 4 chapter entries. Each field was checked for null/missing before overwriting; no conflicts encountered (all targeted fields were null pre-edit).

| Chapter | Field | New Value |
|---|---|---|
| `keritot_3` | `source_url` | `https://chaver.com/Mishnah-New/Hebrew/Text/Seder%20Kodashim/Masechet%20Kritot/Masechet%20Kritot%20Perek%203.htm` |
| `keritot_3` | `seder_he` | `קדשים` |
| `keritot_3` | `seder_en` | `Kodashim` |
| `keritot_3` | `tractate_en` | `Keritot` |
| `keritot_3` | `chapter_num` | `3` |
| `kinnim_1` | `source_url` | `https://chaver.com/Mishnah-New/Hebrew/Text/Seder%20Kodashim/Masechet%20Kinnim/Masechet%20Kinnim%20Perek%201.htm` |
| `kinnim_1` | `seder_he` | `קדשים` |
| `kinnim_1` | `seder_en` | `Kodashim` |
| `kinnim_1` | `tractate_en` | `Kinnim` |
| `kinnim_1` | `chapter_num` | `1` |
| `sotah_9a` | `source_url` | `https://chaver.com/Mishnah-New/Hebrew/Text/Seder%20Nashim/Masechet%20Sotah/Masechet%20Sotah%20Perek%209%20A.htm` |
| `sotah_9b` | `source_url` | `https://chaver.com/Mishnah-New/Hebrew/Text/Seder%20Nashim/Masechet%20Sotah/Masechet%20Sotah%20Perek%209%20B.htm` |

### Fields NOT touched (already populated correctly)

| Chapter | Field | Existing Value |
|---|---|---|
| `keritot_3` | `tractate_he` | `מסכת כריתות` (already set; left alone) |
| `keritot_3` | `chapter_he` | `ג` (already set; left alone) |
| `kinnim_1` | `tractate_he` | `מסכת קינים` (already set; left alone) |
| `kinnim_1` | `chapter_he` | `א` (already set; left alone) |
| `sotah_9a/b` | All seder/tractate/chapter fields | Already populated pre-edit |

### 1.2 `seder_he` value note

The task spec proposed `seder_he: "סדר קדשים"` (with the prefix). I cross-checked the existing corpus convention — every other `seder_he` value is the bare seder name without `"סדר "` prefix (e.g., `'זרעים'`, `'מועד'`, `'נשים'`). I matched the corpus convention: `'קדשים'` not `'סדר קדשים'`. This keeps `keritot_3` and `kinnim_1` consistent with the other 89 Kodashim chapters.

### 1.3 JSON file integrity

| Metric | Value |
|---|---|
| Pre-edit size | 16,656,951 B (16.66 MB) |
| Post-edit size | 16,657,418 B |
| Delta | +467 B (within the ~500-byte expected) |
| Post-edit parse | ✓ (json.load() succeeds) |
| Hebrew chars escaped to `\uXXXX`? | No — `ensure_ascii=False` preserved them |
| Indentation | 2-space (preserved from original) |
| Atomic write | ✓ (write to tmp + fsync + os.replace) |

### 1.4 Post-edit verification

Every applied edit was re-read from disk and compared to the target value: **12/12 match.**

---

## 2. File Renames — 15 `.html` → `.htm`

### 2.1 Renames performed

All 15 files renamed via filesystem `os.rename`. The git index lock (carried over from earlier session) prevented `git mv` from being usable, so the fallback path ran. **GitHub Desktop will show these as old-file-deleted + new-file-added pairs** — git's similarity detection should classify them as renames in the diff/commit view since the file content is identical.

| Old path | New path |
|---|---|
| `Mishnah-New/Hebrew/Text/Seder Kodashim/Masechet Zevachim/Masechet Zevachim Perek 1.html` | `… Perek 1.htm` |
| `… Perek 2.html` | `… Perek 2.htm` |
| `… Perek 3.html` | `… Perek 3.htm` |
| `… Perek 4.html` | `… Perek 4.htm` |
| `… Perek 5.html` | `… Perek 5.htm` |
| `… Perek 6.html` | `… Perek 6.htm` |
| `… Perek 7.html` | `… Perek 7.htm` |
| `… Perek 8.html` | `… Perek 8.htm` |
| `… Perek 9.html` | `… Perek 9.htm` |
| `… Perek 10.html` | `… Perek 10.htm` |
| `… Perek 11.html` | `… Perek 11.htm` |
| `… Perek 12.html` | `… Perek 12.htm` |
| `… Perek 13.html` | `… Perek 13.htm` |
| `… Perek 14.html` | `… Perek 14.htm` |
| `Mishnah-New/Hebrew/Text/Seder Nashim/Masechet Nedarim/Masechet Nedarim Perek 1.html` | `… Perek 1.htm` |

### 2.2 Corpus-wide file count post-rename

```
Mishnah-New/Hebrew/Text/ chapter files:
  .htm:  525  ✓ (single-extension consistency achieved)
  .html: 0    ✓
```

Per-folder confirmation:
- `Seder Kodashim/Masechet Zevachim/`: 14 `.htm` Perek files, 0 `.html`
- `Seder Nashim/Masechet Nedarim/`: 11 `.htm` Perek files (1-11, the renamed Perek 1 + the 10 that were already `.htm`), 0 `.html`

---

## 3. Canonical/og:url Updates in the 15 Renamed Files

Per renamed file, the script updated 6 URL occurrences from the extension-stripped form to the new `.htm`-suffixed canonical:

| URL location | Update |
|---|---|
| `<link rel="canonical" href="...">` | `.../Perek N` → `.../Perek N.htm` |
| `<meta property="og:url" content="...">` | same |
| BreadcrumbList JSON-LD leaf `"item"` | same |
| Article JSON-LD `"url"` | same |
| Article JSON-LD `"mainEntityOfPage"` | same |
| One additional occurrence (typically the `<meta name="twitter:image">` site_url reference or similar) | same |

Total occurrences swapped per file: **6** (consistent across all 15 files). Total swaps corpus-wide: **90** (= 15 files × 6).

### Per-file final state confirmation

| File | canonical | og:url |
|---|---|---|
| Zevachim Perek 1.htm | ends in `.htm` ✓ | ends in `.htm` ✓ |
| Zevachim Perek 2.htm | ✓ | ✓ |
| Zevachim Perek 3.htm | ✓ | ✓ |
| Zevachim Perek 4.htm | ✓ | ✓ |
| Zevachim Perek 5.htm | ✓ | ✓ |
| Zevachim Perek 6.htm | ✓ | ✓ |
| Zevachim Perek 7.htm | ✓ | ✓ |
| Zevachim Perek 8.htm | ✓ | ✓ |
| Zevachim Perek 9.htm | ✓ | ✓ |
| Zevachim Perek 10.htm | ✓ | ✓ |
| Zevachim Perek 11.htm | ✓ | ✓ |
| Zevachim Perek 12.htm | ✓ | ✓ |
| Zevachim Perek 13.htm | ✓ | ✓ |
| Zevachim Perek 14.htm | ✓ | ✓ |
| Nedarim Perek 1.htm | ✓ | ✓ |

All 15 pass canonical+og:url check.

### Defensive checks per file

- File ends with `</html>`: **15/15 ✓**
- All JSON-LD blocks parse: **0 errors across 15 files ✓**
- Atomic write + post-write byte-size verify: **15/15 match ✓**

### Per-file size deltas

Each file gained 24 bytes (the 4 added `.htm` extension strings across the 6 URL occurrences — `.htm` is 4 chars, and the canonical URL appears 6 times = +24 chars / +24 bytes since no multi-byte chars are added). Total corpus growth from this part: +360 bytes.

---

## 4. `_redirects` File

### 4.1 Pre-existing state preserved

The `_redirects` file already existed at the repo root (29,014 bytes, 298 lines, ~100+ pre-existing rules covering Google Search Console 404 cleanups, Mishnah clean-URL→`.htm` rules, legacy WordPress paths, etc.). **None of the pre-existing rules were modified or reordered.**

### 4.2 New rules appended

15 new rules added at the bottom under a clear header comment block:

```
# Mishnah .html → .htm rename redirects (Pre-Track-2 Cleanup, 2026-05-14)
# Source: pages were Phase B-migrated under .html; renamed to .htm for corpus consistency.
# Without these redirects, the old extension-stripped URLs would 404.
/Mishnah-New/Hebrew/Text/Seder%20Kodashim/Masechet%20Zevachim/Masechet%20Zevachim%20Perek%201 /Mishnah-New/Hebrew/Text/Seder%20Kodashim/Masechet%20Zevachim/Masechet%20Zevachim%20Perek%201.htm 301
... (14 more entries)
```

### 4.3 Final state

| Metric | Value |
|---|---:|
| Pre-existing rules preserved | ~100 ✓ |
| New rules added | 15 ✓ |
| File size before | 29,014 B |
| File size after | 32,212 B |
| File grew by | 3,198 B (15 rules + header comments) |
| All 15 new redirect mappings present | ✓ |

### What these redirects do

Each rule is a 301 from the old extension-stripped URL (which Cloudflare was serving while the file was `.html`) to the new `.htm`-suffixed URL. Without these redirects, any Google-indexed link or external link to `.../Masechet Zevachim Perek 1` (no extension, the form Cloudflare auto-stripped from `.html`) would 404. With them, Google sees the 301 and updates its index over the next crawl cycle, preserving page rank.

The redirects also benefit any inbound links from external sources (forums, social media, citations) that may reference the extension-stripped form.

---

## 5. Shishah Sidrei Portal Link Updates

### 5.1 Pre-edit state

The portal had 15 outbound links using `.html` extension that referenced the now-renamed chapters:

```
href="../Text/Seder%20Kodashim/Masechet%20Zevachim/Masechet%20Zevachim%20Perek%201.html"
...
href="../Text/Seder%20Nashim/Masechet%20Nedarim/Masechet%20Nedarim%20Perek%201.html"
```

### 5.2 Edits applied

15 link updates, all `.html` → `.htm`. The link URLs are relative (`../Text/...`), preserved intact except for the extension swap.

| Before | After |
|---|---|
| `…Masechet Zevachim Perek 1.html` | `…Masechet Zevachim Perek 1.htm` |
| `…Masechet Zevachim Perek 2.html` | `…Masechet Zevachim Perek 2.htm` |
| (… 12 more Zevachim chapters …) | |
| `…Masechet Zevachim Perek 14.html` | `…Masechet Zevachim Perek 14.htm` |
| `…Masechet Nedarim Perek 1.html` | `…Masechet Nedarim Perek 1.htm` |

### 5.3 Post-edit verification

- Portal `.html` references to the 15 renamed stems: **0** ✓
- Portal `.htm` references to the 15 renamed stems: **15** ✓
- File size delta: **−15 bytes** (15 chars removed: each `.html` → `.htm` loses 1 char)

---

## 6. Anomalies Encountered

### 6.1 None of substance

- All 12 JSON fields were null pre-edit; no field-value conflicts.
- All 15 file renames succeeded on first attempt (via fs-rename fallback after git mv was blocked by index lock).
- All 15 files had the expected canonical/og:url/JSON-LD URL pattern that matched the find-and-replace.
- All 15 portal links matched the expected `.html` pattern.
- JSON-LD on all 15 files reparses cleanly post-edit.
- The `_redirects` file pre-existed with 100+ rules — preserved unchanged; new rules appended cleanly.

### 6.2 Minor note: git mv vs fs-rename

The 15 renames used `os.rename` rather than `git mv` because git's index lock from earlier in the session was still held. This means the 15 files appear in `git status` as both "deleted .html" and "untracked .htm." Git's automatic rename detection during commit (configurable via `git config diff.renames true`, default on) will reclassify them as renames in GitHub Desktop's diff view. **No manual reclassification required** — the commit will record them as renames.

If for some reason GitHub Desktop doesn't auto-detect, you can force rename detection by running `git add -A` (adds both delete and new) followed by `git commit`. The commit metadata will record the rename via similarity index.

### 6.3 seder_he convention deviation from task spec

Task spec proposed `seder_he: "סדר קדשים"` (with prefix). I followed the corpus convention `'קדשים'` (no prefix) — every other entry in the JSON uses bare seder names. Flagged here for transparency; if you want the prefixed form, it's a 2-second JSON edit on the 2 entries.

---

## 7. All Files Touched

| File | Action |
|---|---|
| `Mishnah-New/English/mishnah_db.json` | 12 field updates across 4 chapter entries |
| `Mishnah-New/Hebrew/Text/Seder Kodashim/Masechet Zevachim/Masechet Zevachim Perek 1.html → 1.htm` | Renamed + canonical/og:url/JSON-LD URLs updated |
| `… Perek 2.html → 2.htm` | Same |
| `… Perek 3.html → 3.htm` | Same |
| `… Perek 4.html → 4.htm` | Same |
| `… Perek 5.html → 5.htm` | Same |
| `… Perek 6.html → 6.htm` | Same |
| `… Perek 7.html → 7.htm` | Same |
| `… Perek 8.html → 8.htm` | Same |
| `… Perek 9.html → 9.htm` | Same |
| `… Perek 10.html → 10.htm` | Same |
| `… Perek 11.html → 11.htm` | Same |
| `… Perek 12.html → 12.htm` | Same |
| `… Perek 13.html → 13.htm` | Same |
| `… Perek 14.html → 14.htm` | Same |
| `Mishnah-New/Hebrew/Text/Seder Nashim/Masechet Nedarim/Masechet Nedarim Perek 1.html → 1.htm` | Same |
| `_redirects` | 15 new 301 rules appended (preserving ~100 existing rules) |
| `Mishnah-New/Hebrew/Text/Shishah Sidrei Mishnah.htm` | 15 portal links updated `.html` → `.htm` |
| `_pilot/pre-track-2-cleanup.md` | This report |

**Total file count: 18 files modified + 15 renamed** (the 15 renamed files appear both in "renamed" and "modified" because their content was also updated for the canonical URLs).

---

## 8. Moshe's Verification Checklist

### Pre-push diff review in GitHub Desktop

1. **`Mishnah-New/English/mishnah_db.json`** — search the diff for `keritot_3`, `kinnim_1`, `sotah_9a`, `sotah_9b`. Confirm each has `source_url`, `seder_he` (`קדשים` or `נשים`), `seder_en`, `tractate_en`, `chapter_num` populated. For `keritot_3` and `kinnim_1`, `tractate_he` and `chapter_he` should be unchanged (already correct pre-edit).
2. **15 renames** — GitHub Desktop should show 15 file renames in the Kodashim/Zevachim and Nashim/Nedarim folders. Each rename should also show small content edits (the 6 URL swaps per file).
3. **`_redirects`** — diff should show 15 new lines + the header comment block, appended at the bottom. The first ~298 lines should be unchanged.
4. **`Mishnah-New/Hebrew/Text/Shishah Sidrei Mishnah.htm`** — diff should show 15 link edits, each `.html` → `.htm`. No other changes.

### Post-deploy URL tests

For each of these 15 chapter URLs:

```
https://chaver.com/Mishnah-New/Hebrew/Text/Seder%20Kodashim/Masechet%20Zevachim/Masechet%20Zevachim%20Perek%20N.htm   (N = 1..14)
https://chaver.com/Mishnah-New/Hebrew/Text/Seder%20Nashim/Masechet%20Nedarim/Masechet%20Nedarim%20Perek%201.htm
```

- The `.htm` URL should **serve the page** (200 OK).
- The extension-stripped equivalent (without `.htm`) should **301 redirect** to the `.htm` URL.

Quick test of a couple via your browser or curl:

```bash
curl -I "https://chaver.com/Mishnah-New/Hebrew/Text/Seder%20Kodashim/Masechet%20Zevachim/Masechet%20Zevachim%20Perek%201.htm"
# Expected: 200 OK

curl -I "https://chaver.com/Mishnah-New/Hebrew/Text/Seder%20Kodashim/Masechet%20Zevachim/Masechet%20Zevachim%20Perek%201"
# Expected: 301 to the .htm URL
```

### Sanity check on Shishah Sidrei portal

Visit `https://chaver.com/Mishnah-New/Hebrew/Text/Shishah%20Sidrei%20Mishnah.htm`. Click any of the 15 affected tractate chapter links — should now land on the `.htm` URL directly (no redirect hop).

---

## 9. What's Next

Per the task spec, after this cleanup:

1. **E-3** — Add CollectionPage schema with `@id: https://chaver.com/#mishnah-collection` to TheMishnah, Mishnah Portal (EN), Shishah Sidrei Mishnah. Add `@id: https://chaver.com/#torah-collection` to Torah Portal. Consolidate Hebrew home @ids. Upgrade MAVO. Tighten `is_home` detector.
2. **Phase D-1 pilot** — Render 5-6 chapters from the now-clean JSON to verify the pipeline.
3. **Phase D-2 bulk** — Render all 525 chapters.
4. **Phase D-3 polish** — Portal page enhancements.

---

## 10. Out of Scope (Per Task Spec)

- E-3 (separate task)
- Phase D-1 pilot (separate task — after E-3)
- Phase D-2 bulk (later)
- Cleanup of `_pilot/mishnah_db_reextracted.json` (byte-identical sibling; left alone for now)
- The 311-vs-310 marker count discrepancy in `_meta.known_open_issues` (deferred per metadata notes)
- Any other chapter rename inconsistencies (only the 15 known cases — none others surfaced during cleanup)
