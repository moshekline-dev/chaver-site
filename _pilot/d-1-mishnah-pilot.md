# Track 2 Phase D-1 — Mishnah Chapter Pilot Render

**Date:** 2026-05-14
**Scope:** Render 6 representative Mishnah chapters from `Mishnah-New/English/mishnah_db.json` into clean RTL Hebrew matrix-table HTML with full SEO/AEO (canonical, og:*, BreadcrumbList, Article schema referencing `#mishnah-collection`).
**Status:** **All 6 rendered cleanly. 0 errors, all defensive checks pass.** Cross-check against `_pilot/megillah_1_extracted.json` shows byte-identical structure. **Not committed.**

---

## 1. Files Rendered

| JSON key | Disk path | Size before | Size after | Δ | Markers in content |
|---|---|---:|---:|---:|---|
| `berakhot_1` | `Mishnah-New/Hebrew/Text/Seder Zeraim/Masechet Brachot/Mesechet Brachot Perek 1.htm` | 23,373 | 22,690 | −683 | horizontal1 ×12 |
| `megillah_1` | `Mishnah-New/Hebrew/Text/Seder Moed/Masechet Megillah/Masechet Megillah Perek 1.htm` | 23,699 | 26,238 | +2,539 | horizontal1 ×36, horizontal2 ×2, horizontal3 ×2, internalparallel ×10 |
| `eduyot_1` | `Mishnah-New/Hebrew/Text/Seder Nezikin/Masechet Eduyot/Masechet Eduyot Perek 1.htm` | 26,563 | 28,428 | +1,865 | horizontal1 ×29, vertical1 ×6, internalparallel ×9 |
| `kinnim_1` | `Mishnah-New/Hebrew/Text/Seder Kodashim/Masechet Kinnim/Masechet Kinnim Perek 1.htm` | 22,208 | 21,753 | −455 | (none — JSON has no markers for this chapter) |
| `sotah_9a` | `Mishnah-New/Hebrew/Text/Seder Nashim/Masechet Sotah/Masechet Sotah Perek 9 A.htm` | 23,007 | 23,953 | +946 | horizontal1 ×10, internalparallel ×11 |
| `shabbat_22` | `Mishnah-New/Hebrew/Text/Seder Moed/Masechet Shabbat/Masechet Shabbat Perek 22.htm` | 21,458 | 22,160 | +702 | horizontal1 ×6 |

**Total size delta: +4,914 bytes** across 6 files (mean ≈ +820 B per file). Sizes mostly grew (more JSON-LD content) but berakhot_1 and kinnim_1 shrunk because the previous Word-export markup was bigger than the new clean rendering.

---

## 2. Sample Rendered Output (berakhot_1)

The simplest pilot. Full `<main>` content shown below — what Moshe should see when visiting the page:

```html
<main class="content-wrapper">
    <article class="mishnah-chapter" dir="rtl">
        <h1 dir="rtl">מסכת ברכות פרק א – המבנה הספרותי</h1>
        <table class="mishnah-table" dir="rtl">
            <tbody>
                <tr class="mishnah-row">
                    <td class="mishnah-cell" colspan="2">
                        <p class="cell-content" dir="rtl">
                            <span class="cell-label">1א</span><br>
                            (א) <span class="horizontal1">מאימתי קורין את שמע</span> בערבית<br>
                            משעה שהכהנים נכנסים לאכול בתרומתן<br>
                            <span class="horizontal1">עד</span> סוף האשמורה הראשונה דברי רבי אליעזר<br>
                            וחכמים אומרים עד חצות<br>
                            …
                        </p>
                    </td>
                    <td class="mishnah-cell" colspan="2">
                        <p class="cell-content" dir="rtl">
                            <span class="cell-label">1ב</span><br>
                            (ב)<span class="horizontal1"> מאימתי קורין את שמע</span> בשחרית<br>
                            …
                        </p>
                    </td>
                </tr>
                <tr class="mishnah-row">
                    <td class="mishnah-cell" colspan="4">
                        <p class="cell-content" dir="rtl">
                            <span class="cell-label">2</span><br>
                            (ג) בית שמאי אומרים<br>
                            בערב כל אדם יטו ויקראו ובבקר יעמדו<br>
                            …
                        </p>
                    </td>
                </tr>
                <tr class="mishnah-row">
                    <td class="mishnah-cell" colspan="2">
                        <p class="cell-content" dir="rtl">
                            <span class="cell-label">3א</span><br>
                            (ד) <span class="horizontal1">בשחר</span> מברך שתים לפניה ואחת לאחריה<br>
                            <span class="horizontal1">ובערב</span> שתים לפניה ושתים לאחריה<br>
                            …
                        </p>
                    </td>
                    <td class="mishnah-cell" colspan="2">
                        <p class="cell-content" dir="rtl">
                            <span class="cell-label">3ב</span><br>
                            (ה) מזכירין יציאת מצרים בלילות<br>
                            …
                        </p>
                    </td>
                </tr>
            </tbody>
        </table>
    </article>
</main>
```

(Full content in the rendered file — abridged here for readability.)

### Visual structure

- 3 rows: 2+2 colspan / 4 colspan / 2+2 colspan = matrix shape `[[2,2], [4], [2,2]]`
- Each cell wraps in `<p class="cell-content" dir="rtl">` with a `<span class="cell-label">` followed by `<br>` and then the content
- Marker spans use lowercase JSON-native class names (`horizontal1`, `vertical1`, etc.) — main.css supports both lowercase and capitalized forms; visual rendering identical
- Line breaks within cells use `<br>` (preserving the `\n` separators from the JSON `text` field)
- RTL throughout: `dir="rtl"` on `<article>`, `<h1>`, `<table>`, every `<td>`, every `<p>`

---

## 3. Per-Chapter Verification Table

All 6 pilots pass every defensive check:

| Chapter | Shape | Rows | Cells | Runs | Markers in JSON | Marker spans in HTML | Verification |
|---|---|---:|---:|---:|---|---|---|
| `berakhot_1` | `[[2,2], [4], [2,2]]` | 3 | 5 | 133 | horizontal1 | 12 horizontal1 | ✓ all checks |
| `megillah_1` | `[[2,2], [1,2,1], [2,2], [1,2,1], [2,2]]` | 5 | 12 | 236 | 4 types | 50 marker spans (4 types) | ✓ all checks |
| `eduyot_1` | `[[1,1,1] × 4]` | 4 | 12 | 353 | horizontal1, vertical1, internalparallel | 44 marker spans (3 types) | ✓ all checks |
| `kinnim_1` | `[[1,1,1] × 2]` | 2 | 6 | 126 | (none) | 0 marker spans | ✓ all checks |
| `sotah_9a` | `[[2,2] × 4]` | 4 | 8 | 172 | horizontal1, internalparallel | 21 marker spans (2 types) | ✓ all checks |
| `shabbat_22` | `[[2,2] × 3]` | 3 | 6 | 92 | horizontal1 | 6 marker spans (1 type) | ✓ all checks |

### Defensive check matrix

Every file passes:

| Check | berakhot_1 | megillah_1 | eduyot_1 | kinnim_1 | sotah_9a | shabbat_22 |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| File ends with `</html>` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| JSON-LD parses (3 blocks each) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Canonical preserved (from E-2) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| No `\u05XX` Hebrew escapes (raw UTF-8) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| E-1 site-wide stub sentinel present | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| D-1 pilot sentinel present exactly once | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Provenance marker (`rendered-from: ...HE.html`) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Article schema `isPartOf` includes `#mishnah-collection` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| BreadcrumbList uses Hebrew labels (`מסכת`, `סדר`) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Atomic write + post-write byte-size verify | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

### JSON-LD block structure (consistent across all 6)

Each rendered file has 3 JSON-LD blocks in `<head>`:

1. **`@graph` stub** — from E-1, references `#website`, `#organization`, `#moshe-kline` (unchanged by D-1)
2. **`BreadcrumbList`** — 6 items, Home → Mishnah → Hebrew → {Hebrew seder name} → {Hebrew tractate name} → {tractate + chapter}
3. **`Article`** — full schema with `isPartOf: [{"@id": "#website"}, {"@id": "#mishnah-collection"}]`, references canonical Person + Organization @ids

### Per-chapter Title + Description (sample)

| Chapter | `<title>` | `<meta name="description">` |
|---|---|---|
| berakhot_1 | מסכת ברכות פרק א – המבנה הספרותי \| Chaver.com | משנה מסכת ברכות פרק א בפריסה מבנית – הטקסט המלא עם הדגשת המבנה הספרותי הדו-ממדי |
| megillah_1 | מסכת מגילה פרק א – המבנה הספרותי \| Chaver.com | משנה מסכת מגילה פרק א בפריסה מבנית – הטקסט המלא עם הדגשת המבנה הספרותי הדו-ממדי |
| eduyot_1 | מסכת עדיות פרק א – המבנה הספרותי \| Chaver.com | משנה מסכת עדיות פרק א בפריסה מבנית – הטקסט המלא עם הדגשת המבנה הספרותי הדו-ממדי |
| kinnim_1 | מסכת קינים פרק א – המבנה הספרותי \| Chaver.com | משנה מסכת קינים פרק א בפריסה מבנית – הטקסט המלא עם הדגשת המבנה הספרותי הדו-ממדי |
| sotah_9a | מסכת סוטה פרק ט – המבנה הספרותי \| Chaver.com | משנה מסכת סוטה פרק ט בפריסה מבנית – הטקסט המלא עם הדגשת המבנה הספרותי הדו-ממדי |
| shabbat_22 | מסכת שבת פרק כב – המבנה הספרותי \| Chaver.com | משנה מסכת שבת פרק כב בפריסה מבנית – הטקסט המלא עם הדגשת המבנה הספרותי הדו-ממדי |

### Per-chapter BreadcrumbList (sample for `megillah_1`)

```
1. Home                       → https://chaver.com/
2. Mishnah                    → https://chaver.com/Mishnah-New/
3. Hebrew                     → https://chaver.com/Mishnah-New/Hebrew/
4. מועד (seder_he)            → https://chaver.com/Mishnah-New/Hebrew/Text/Seder%20Moed/
5. מסכת מגילה (tractate_he)   → https://chaver.com/Mishnah-New/Hebrew/Text/Seder%20Moed/Masechet%20Megillah/
6. מסכת מגילה פרק א          → canonical (.htm)
```

(All 6 pilots follow this same 6-item pattern with Hebrew labels at positions 4-6.)

---

## 4. Megillah Cross-Check

Compared `mishnah_db.json["megillah_1"]` byte-for-byte against `_pilot/megillah_1_extracted.json`:

| Property | mishnah_db | extracted sample | Match |
|---|---|---|:-:|
| Top-level keys | 9 keys (tractate_he/en, seder_he/en, chapter_he/num, shape, source_url, rows) | Same 9 keys | ✓ |
| `shape` | `[[2,2], [1,2,1], [2,2], [1,2,1], [2,2]]` | Same | ✓ |
| Row count | 5 | 5 | ✓ |
| Cells per row | 2/3/2/3/2 | Same | ✓ |
| Runs per cell (24 cells × N runs) | identical | identical | ✓ |
| Markers per cell | identical | identical | ✓ |
| Row 0 Cell 0 text content (full) | identical | identical | ✓ |
| Markers vocabulary | horizontal1, horizontal2, horizontal3, internalparallel | same 4 | ✓ |

**Conclusion: the `mishnah_db.json` extraction is consistent with the standalone sample. The D-1 render pipeline operating on `mishnah_db.json` produces output equivalent to operating on the standalone sample. The render is reproducible and faithful to the source.**

---

## 5. Anomalies and Observations

### 5.1 `kinnim_1` has zero markers

Per the JSON's `_meta.markers_populated_count: 310 chapters`, Kinnim 1 is one of the 215 chapters with no markers populated yet. The chapter renders correctly (matrix structure, cell labels, content text), just no marker highlighting. This is expected per the JSON state and will not block Phase D-2.

### 5.2 Cell-label detection

The JSON's `cell.label` field is sometimes incomplete (e.g., `'1'` for a cell whose visual label is `'1ב'`). The render uses the FIRST LINE of `cell.text` (everything before the first `\n`) as the displayed label rather than `cell.label`. This gives the correct visual label across all 6 pilots.

The implementation walks `cell.runs` and accumulates run text until it matches the first line of `cell.text`, then skips the subsequent `\n` run. This is robust across the 6 pilots — no fallback path was needed.

### 5.3 `chapter_he: 'כב'` for shabbat_22

The Hebrew chapter letter for Shabbat 22 is `כב` (two characters: `כ` + `ב` = 20 + 2). The render handles multi-character chapter labels correctly. Same for `כא` (21), `כג` (23), etc., which will appear in larger tractates.

### 5.4 No marker types found that don't have CSS coverage

The 5 chapters with markers (all except kinnim_1) use only these marker types: `horizontal1`, `horizontal2`, `horizontal3`, `vertical1`, `internalparallel`. main.css supports all 8 known marker types including `closure`, `ciasm1`, `ciasm2`. **0 marker types in any of the 6 pilots are unsupported by main.css.**

### 5.5 No Hebrew rendering issues

All Hebrew text rendered as raw UTF-8 (not `\u05XX` escaped). `ensure_ascii=False` in JSON serialization preserved the Hebrew characters in the JSON-LD blocks. The `<title>`, `<meta>`, and `<h1>` elements all show Hebrew correctly.

### 5.6 Size delta direction varies

Some files grew, some shrunk:
- **Grew**: megillah_1 (+2,539), eduyot_1 (+1,865), sotah_9a (+946), shabbat_22 (+702)
- **Shrunk**: berakhot_1 (−683), kinnim_1 (−455)

The growth is dominated by the new BreadcrumbList JSON-LD (+~900 B) and Article schema (+~700 B) — but these are ADDED to a base that already had E-2's BreadcrumbList + Article. The growth is in fact mostly from the matrix table being larger than the pre-D-1 placeholder content. The shrinkage on berakhot_1 / kinnim_1 reflects that the prior Word-export content for those chapters was unusually verbose.

After Phase D-2 renders all 525 chapters, the total corpus size will be more predictable per the average ≈+820 bytes per chapter we observed here.

---

## 6. Recommendations for Phase D-2

Based on this pilot, Phase D-2 (bulk render of 525 chapters) should be straightforward. Specific recommendations:

### 6.1 Reuse the D-1 render pipeline verbatim

The `/tmp/d1_render.py` script can be promoted to `_pilot/d2_render.py` with two changes:

- Replace the hard-coded `PILOTS` dict with: iterate over all 525 keys in `mishnah_db.json` (excluding `_meta`) and use each entry's `source_url` field to determine the disk path.
- Add idempotency: skip if `<!-- D-1 pilot` or `<!-- D-2 bulk` sentinel already present and the chapter content hash hasn't changed (so re-runs are no-ops on already-rendered files).

### 6.2 Handle the 4 special cases

- `keritot_3`, `kinnim_1`, `sotah_9a`, `sotah_9b` had their `source_url` and metadata populated in the Pre-Track-2 Cleanup task. These now have all required fields and should render fine. Verify before bulk run.

### 6.3 Handle empty markers gracefully

215 chapters have no markers (per `_meta.markers_populated_count: 310`). The render handles this fine (kinnim_1 verified). D-2 should produce valid output for unmarked chapters too.

### 6.4 Atomic-write batch checkpoint

D-2 will write 525 files. Add a progress log every ~50 files (similar to E-2's pattern). Each file uses the same atomic write + post-write byte verify so a mid-batch failure doesn't corrupt files.

### 6.5 Per-chapter verification budget

The 13-check budget from Phase B may not apply directly — adapt to: ends-with-html, JSON-LD parses, canonical preserved, sentinel exactly once, no `\u` escapes. Same as D-1 verification.

### 6.6 Handle the 15 `.htm` chapters (formerly `.html`) carefully

Per the Pre-Track-2 Cleanup task, 15 Zevachim + Nedarim Perek 1 files were renamed `.html` → `.htm`. Their canonical URLs include `.htm`. The render pipeline picks up canonical from the file (E-2 set it correctly) so D-2 just needs to render and preserve. No special handling needed beyond confirming the source_url in the JSON also has `.htm`.

### 6.7 No surprises from cell-label heuristic

The first-line-of-cell.text approach for label detection worked cleanly on all 6 pilots. It should generalize. If any chapter has unusual cell.text shapes (e.g., no `\n` at all), the renderer falls back to "emit all runs as-is" — graceful degradation.

### 6.8 Coverage expectation

After D-2 + D-3:
- 525 chapter pages, each with full SEO/AEO, Article schema, BreadcrumbList, canonical Person/Org/Website references
- 4 portal CollectionPages referencing those 525 articles via the `#mishnah-collection` `@id`
- Schema graph traversable from any chapter → CollectionPage → Person/Org

---

## 7. Files Touched

| File | Action |
|---|---|
| `Mishnah-New/Hebrew/Text/Seder Zeraim/Masechet Brachot/Mesechet Brachot Perek 1.htm` | Re-rendered from `mishnah_db.json[berakhot_1]` |
| `Mishnah-New/Hebrew/Text/Seder Moed/Masechet Megillah/Masechet Megillah Perek 1.htm` | Re-rendered from `mishnah_db.json[megillah_1]` |
| `Mishnah-New/Hebrew/Text/Seder Nezikin/Masechet Eduyot/Masechet Eduyot Perek 1.htm` | Re-rendered from `mishnah_db.json[eduyot_1]` |
| `Mishnah-New/Hebrew/Text/Seder Kodashim/Masechet Kinnim/Masechet Kinnim Perek 1.htm` | Re-rendered from `mishnah_db.json[kinnim_1]` |
| `Mishnah-New/Hebrew/Text/Seder Nashim/Masechet Sotah/Masechet Sotah Perek 9 A.htm` | Re-rendered from `mishnah_db.json[sotah_9a]` |
| `Mishnah-New/Hebrew/Text/Seder Moed/Masechet Shabbat/Masechet Shabbat Perek 22.htm` | Re-rendered from `mishnah_db.json[shabbat_22]` |
| `_pilot/d-1-mishnah-pilot.md` | This report |

No other files modified. The render pipeline lives at `/tmp/d1_render.py` (working copy) — to be promoted to `_pilot/d2_render.py` for Phase D-2.

---

## 8. Moshe's Verification Checklist

### Spot-check via GitHub Desktop diff view

For each of the 6 pilot files, the diff should show:

- Old content (Phase B-migrated Word-export `<table>` with `MsoNormal` cruft) replaced by clean modern HTML matrix table
- `<title>` updated to the new Hebrew format
- `<meta name="description">` updated to the new Hebrew template
- BreadcrumbList JSON-LD: 6 items with Hebrew labels at positions 4-6
- Article JSON-LD: `isPartOf` is an array containing both `#website` and `#mishnah-collection`
- `<!-- D-1 pilot: rendered from mishnah_db.json @ ... -->` sentinel inside `<head>`
- Provenance marker `<!-- rendered-from: _templates/Academic-Content-HE.html @ ... -->` immediately after `<!DOCTYPE html>` (refreshed timestamp)
- E-1 site-wide boilerplate block + E-2 per-page metadata block both preserved unchanged

### Browser verification (after push)

Visit each of the 6 URLs in incognito (no browser cache):

```
https://chaver.com/Mishnah-New/Hebrew/Text/Seder%20Zeraim/Masechet%20Brachot/Mesechet%20Brachot%20Perek%201.htm
https://chaver.com/Mishnah-New/Hebrew/Text/Seder%20Moed/Masechet%20Megillah/Masechet%20Megillah%20Perek%201.htm
https://chaver.com/Mishnah-New/Hebrew/Text/Seder%20Nezikin/Masechet%20Eduyot/Masechet%20Eduyot%20Perek%201.htm
https://chaver.com/Mishnah-New/Hebrew/Text/Seder%20Kodashim/Masechet%20Kinnim/Masechet%20Kinnim%20Perek%201.htm
https://chaver.com/Mishnah-New/Hebrew/Text/Seder%20Nashim/Masechet%20Sotah/Masechet%20Sotah%20Perek%209%20A.htm
https://chaver.com/Mishnah-New/Hebrew/Text/Seder%20Moed/Masechet%20Shabbat/Masechet%20Shabbat%20Perek%2022.htm
```

For each:

- [ ] `<title>` renders correctly in browser tab (Hebrew right-to-left)
- [ ] Matrix table layout looks right: RTL flow, cells aligned, colspan correctly applied
- [ ] Cell labels (`1א`, `1ב`, `2`, `3א`, `3ב`, etc.) visible at top of each cell
- [ ] Marker highlighting visible: colored backgrounds/borders on horizontal1, horizontal2, etc. spans
- [ ] HE nav chrome intact: דף הבית, תורה, משנה dropdown, etc.
- [ ] HE footer intact
- [ ] No JavaScript errors in browser console (F12 → Console)
- [ ] Mobile view (resize to ~400px wide) — table should be readable; matrix-table CSS should shrink-to-fit

### Schema validation

Pick one chapter (say `berakhot_1`) and paste its URL into:

- **Google Rich Results Test** (https://search.google.com/test/rich-results)
  - Should detect Article + BreadcrumbList
  - Should report 0 errors and 0 warnings on those types
- **Schema.org validator** (https://validator.schema.org)
  - Should parse all 3 JSON-LD blocks without error
  - The `isPartOf` array should be recognized as referring to both `#website` and `#mishnah-collection`

### Compare to a non-pilot chapter

To check visual consistency, open a still-Phase-B-migrated chapter (e.g., `Masechet Megillah Perek 2.htm` — not in the pilot) alongside the newly-rendered `Masechet Megillah Perek 1.htm`. Differences are expected:

- Perek 1 (new): clean modern HTML, cleaner styling
- Perek 2 (old): Word-export `MsoNormal` markup, but should look visually similar in the browser (same matrix layout, same marker highlighting from main.css)

The new render should look **at least as good** as the old, with cleaner DOM and faster rendering.

### Authorize Phase D-2

If all 6 pilots look good visually and validate without schema errors:

→ **Authorize Phase D-2** — bulk render all 525 chapters using the same pipeline.

If anything looks off:

→ Flag specific issues. Common ones to watch for:

- Cell labels duplicated (would mean the label-detection heuristic missed)
- Markers not rendering colored (would mean CSS class name mismatch)
- Layout broken (table cells stacking instead of side-by-side) — possible CSS issue with `.mishnah-table` / `.mishnah-cell`

---

## 9. Out of Scope

- Rendering chapters other than the 6 pilots
- Modifying `mishnah_db.json` content
- Touching the portal pages (E-3 already handled CollectionPage schema)
- Populating `CollectionPage.mainEntity.itemListElement` (Phase D-3)
- Cross-chapter prev/next navigation (Phase D-3)
- English translation or commentary (the JSON is Hebrew-only)
- `main.css` changes — none needed (lowercase marker classes already supported)
- Adding new CSS classes (`.mishnah-table` / `.mishnah-cell` / `.cell-content` / `.cell-label` get default browser styling for now; can be polished in D-3)

---

## 10. What's Next After Moshe Approves

1. **Promote `d1_render.py` to `_pilot/d2_render.py`** with bulk-iteration logic
2. **Phase D-2** — render all 525 chapters (one Cowork run, similar pattern to Phase B's bulk run)
3. **Phase D-3** — portal polish:
   - Populate `CollectionPage.mainEntity.itemListElement` on the 3 Mishnah portals with the 524 chapter URLs
   - Add chapter-to-chapter prev/next nav within each tractate
   - Optionally: add `.mishnah-table` / `.mishnah-cell` CSS rules to main.css for polish
4. **Post-D-3 verification** — re-run SEO audit; the full schema graph (525 chapter Articles → CollectionPage → canonical Person/Org/Website) should be traversable
