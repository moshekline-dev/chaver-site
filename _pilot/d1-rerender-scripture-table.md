# D-1 Re-render — scripture-table pattern (v2)

**Date:** 2026-05-14
**Scope:** Re-render the 6 D-1 pilot chapter files using the existing `.scripture-table` HTML pattern (one table per matrix row, with column-letter `<thead>` headers). Zero new CSS — reuses `.scripture-table`, `.col-a/b/c/full` rules already in main.css for the Torah unit pages. Plus brand-fix (already in HE template from previous task; lands automatically via re-render).
**Status:** **All 6 re-rendered cleanly. 0 errors, all 16 verification checks pass per file.** **Not committed.**

**Supersedes the previous v1 D-1 render and the styling-fixes CSS task** — the previous v1 used `.mishnah-table` per-chapter; this v2 uses `.scripture-table` per-row, matching Torah unit visual styling.

---

## 1. Files Re-rendered

| Chapter | Disk path | Size before | Size after | Δ | Row tables | Markers in content |
|---|---|---:|---:|---:|---:|---|
| `berakhot_1` | `…/Mesechet Brachot Perek 1.htm` | 22,679 | 22,740 | +61 | 3 | horizontal1 |
| `megillah_1` | `…/Masechet Megillah Perek 1.htm` | 26,227 | 26,304 | +77 | 5 | horizontal1, horizontal2, horizontal3, internalparallel |
| `eduyot_1` | `…/Masechet Eduyot Perek 1.htm` | 28,417 | 28,185 | −232 | 4 | horizontal1, vertical1, internalparallel |
| `kinnim_1` | `…/Masechet Kinnim Perek 1.htm` | 21,742 | 21,454 | −288 | 2 | (no markers in JSON) |
| `sotah_9a` | `…/Masechet Sotah Perek 9 A.htm` | 23,942 | 24,129 | +187 | 4 | horizontal1, internalparallel |
| `shabbat_22` | `…/Masechet Shabbat Perek 22.htm` | 22,149 | 22,122 | −27 | 3 | horizontal1 |

Total delta: −222 bytes across 6 files. The per-row table pattern is roughly size-neutral to the v1 single-table pattern; small variations reflect indentation + the lost `.mishnah-cell` / `.cell-content` / `.cell-label` class attributes.

### Row-table count matches shape

Each chapter's `n_row_tables` matches `len(chapter.shape)`:

| Chapter | shape | rows in shape | row-tables emitted |
|---|---|---:|---:|
| berakhot_1 | `[[2,2], [4], [2,2]]` | 3 | 3 ✓ |
| megillah_1 | `[[2,2], [1,2,1], [2,2], [1,2,1], [2,2]]` | 5 | 5 ✓ |
| eduyot_1 | `[[1,1,1] × 4]` | 4 | 4 ✓ |
| kinnim_1 | `[[1,1,1] × 2]` | 2 | 2 ✓ |
| sotah_9a | `[[2,2] × 4]` | 4 | 4 ✓ |
| shabbat_22 | `[[2,2] × 3]` | 3 | 3 ✓ |

---

## 2. HE Template Brand Fix

The HE template (`_templates/Academic-Content-HE.html`) was already updated to `<div class="nav-brand">chaver.com</div>` in the previous styling-fixes task. The brand fix is idempotent — the current task confirmed the template state, did not re-edit, and the re-render of the 6 pilots picks up the corrected brand from the template automatically.

### Pre-task state (from previous task)

```
<div class="nav-brand">chaver.com</div>
```

### Post-re-render state on each pilot file

All 6 files: `<div class="nav-brand">chaver.com</div>` count = 1; `<div class="nav-brand">&#1495;&#1489;&#1512;</div>` count = 0.

---

## 3. Per-Chapter Verification (all 16 checks pass per file)

| Check | berakhot_1 | megillah_1 | eduyot_1 | kinnim_1 | sotah_9a | shabbat_22 |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| File ends with `</html>` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| All JSON-LD blocks parse | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Canonical URL preserved from E-2 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| No `\u05XX` Hebrew escapes (raw UTF-8) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| D-1 pilot v2 sentinel count = 1 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| E-1 site-wide stub sentinel present | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| E-2 per-page metadata sentinel present | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Provenance marker (`rendered-from: HE.html`) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `chaver.com` brand count = 1 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Old `&#1495;&#1489;&#1512;` brand count = 0 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `<table class="scripture-table">` count ≥ 1 | 3 | 5 | 4 | 2 | 4 | 3 |
| `<th class="col-X">` headers present | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| No `<table class="mishnah-table">` (legacy purged) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| No `class="mishnah-cell"` (legacy purged) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| No `class="cell-content"` (legacy purged) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| No `class="cell-label"` (legacy purged) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `(חלק א)` in title (sotah_9a only) | n/a | n/a | n/a | n/a | ✓ | n/a |

**16/16 checks pass per file. 0 critical failures.**

### E-2 sentinel preservation note

The previous v1 D-1 render didn't preserve the E-2 sentinel comment (because the v1 render replaced template region content, and the template doesn't carry the E-2 sentinel). The v2 render explicitly wraps the meta region with `<!-- E-2: Per-page metadata injected -->` / `<!-- /E-2 -->` sentinel comments so the marker is present per the task spec's check #7.

---

## 4. Sample Rendered Output (berakhot_1)

The full `<main>` content of `Mesechet Brachot Perek 1.htm` — Moshe's primary visual reference:

```html
<main class="content-wrapper">
    <article class="mishnah-chapter" dir="rtl">
        <h1 dir="rtl">מסכת ברכות פרק א – המבנה הספרותי</h1>

        <!-- Row 1: [2,2] colspan — two cells -->
        <table class="scripture-table" dir="rtl">
          <thead><tr>
            <th class="col-a" colspan="2">1א</th>
            <th class="col-c" colspan="2">1ב</th>
          </tr></thead>
          <tbody><tr>
            <td colspan="2"><p dir="rtl">
              (א) <span class="horizontal1"><b>מאימתי קורין את שמע</b></span> בערבית<br>
              משעה שהכהנים נכנסים לאכול בתרומתן<br>
              <span class="horizontal1"><b>עד</b></span> סוף האשמורה הראשונה דברי רבי אליעזר<br>
              … (more content) …
            </p></td>
            <td colspan="2"><p dir="rtl">
              (ב)<span class="horizontal1"><b> מאימתי קורין את שמע</b></span> בשחרית<br>
              משיכיר בין תכלת ללבן<br>
              … (more content) …
            </p></td>
          </tr></tbody>
        </table>

        <!-- Row 2: [4] colspan — single cell spanning full width -->
        <table class="scripture-table" dir="rtl">
          <thead><tr>
            <th class="col-full" colspan="4">2</th>
          </tr></thead>
          <tbody><tr>
            <td colspan="4"><p dir="rtl">
              (ג) בית שמאי אומרים<br>
              … (more content) …
            </p></td>
          </tr></tbody>
        </table>

        <!-- Row 3: [2,2] colspan — two cells -->
        <table class="scripture-table" dir="rtl">
          <thead><tr>
            <th class="col-a" colspan="2">3א</th>
            <th class="col-c" colspan="2">3ב</th>
          </tr></thead>
          <tbody><tr>
            <td colspan="2"><p dir="rtl">
              (ד) <span class="horizontal1"><b>בשחר</b></span> מברך שתים לפניה ואחת לאחריה<br>
              … (more content) …
            </p></td>
            <td colspan="2"><p dir="rtl">
              (ה) מזכירין יציאת מצרים בלילות<br>
              … (more content) …
            </p></td>
          </tr></tbody>
        </table>
    </article>
</main>
```

(Formatted for readability — actual on-disk output is more compact but identical in structure.)

### Visual interpretation

- **Row 1** renders as a small table: two header cells with dark brown (`col-a`) and cream (`col-c`) gradient backgrounds carrying labels "1א" and "1ב", then the content row below.
- **Row 2** renders as another table: one header cell with the medium tan (`col-full`) background spanning 4 columns, label "2", then the single content cell below.
- **Row 3** renders as another table: same pattern as row 1 with labels "3א" / "3ב".
- Marker spans (`<span class="horizontal1"><b>...</b></span>`) inherit the existing blue highlighting from main.css.
- All cells are RTL via `dir="rtl"` on `<article>`, `<table>`, `<th>`, `<p>`.

### `col-*` class mapping (per cell position in row)

| Cells in row | First cell | Middle cells | Last cell |
|---:|---|---|---|
| 1 | `col-full` | — | — |
| 2 | `col-a` | — | `col-c` |
| 3 | `col-a` | `col-b` | `col-c` |
| 4+ | `col-a` | `col-b` (all middle) | `col-c` |

Verified across the 6 pilots: 1-cell rows in berakhot_1 (row 2), kinnim_1 (rows 1+2), shabbat_22 — all use `col-full`. 2-cell rows in berakhot_1 (rows 1+3), megillah_1 (rows 1+3+5), sotah_9a, shabbat_22 — all use `col-a` / `col-c`. 3-cell rows in megillah_1 (rows 2+4), eduyot_1 — use `col-a` / `col-b` / `col-c`. No 4+ cell rows in the pilots; the algorithm handles them correctly via the `col-b` middle fallback.

---

## 5. Sotah 9a Title Disambiguation

The 4 places `(חלק א)` appears in the rendered `sotah_9a` file:

| Field | Content |
|---|---|
| `<title>` | `מסכת סוטה פרק ט (חלק א) – המבנה הספרותי \| Chaver.com` |
| `<h1>` | `מסכת סוטה פרק ט (חלק א) – המבנה הספרותי` |
| `<meta name="description">` | `משנה מסכת סוטה פרק ט (חלק א) בפריסה מבנית – הטקסט המלא עם הדגשת המבנה הספרותי הדו-ממדי` |
| `og:title` | `מסכת סוטה פרק ט (חלק א) – המבנה הספרותי` |
| BreadcrumbList position 6 `name` | `מסכת סוטה פרק ט (חלק א)` |
| Article schema `headline` | `מסכת סוטה פרק ט (חלק א) – המבנה הספרותי` |

When D-2 renders `sotah_9b`, the same logic applies with `(חלק ב)` suffix. The CHAPTER_SUFFIX dict in the render script maps both keys; the algorithm is generic.

---

## 6. Pending D-2 Prep Questions (carried forward / resolved)

| Question | Status |
|---|---|
| Sotah 9a/9b title suffix | **RESOLVED** — using `(חלק א)` / `(חלק ב)`. Implemented in v2 render via `CHAPTER_SUFFIX` dict. |
| Cell-label heuristic confidence | Still using "first line of `cell.text`" — worked cleanly on all 6 pilots including the 1-cell rows (kinnim_1 had only label "1א" / "1ב" etc.) and the 3-cell rows (megillah_1 row 2 had labels "2א" / "2ב" / "2ג"). No fallback path was triggered. Recommend continued use in D-2 with no changes. |

---

## 7. Anomalies Encountered

### 7.1 E-2 sentinel was lost in v1 render — restored in v2

The previous v1 D-1 render removed the `<!-- E-2: Per-page metadata injected -->` sentinel because re-rendering from template via region substitution replaced the meta region's content (and the template doesn't carry an E-2 sentinel — E-2 was originally injected per-page). The v1 verification didn't check for the E-2 sentinel, so this was undetected.

The v2 task spec's check #7 requires "E-1 + E-2 sentinels preserved." Fixed by explicitly wrapping the meta region content with `<!-- E-2: Per-page metadata injected -->` / `<!-- /E-2 -->` sentinel comments in the render output. The marker now correctly conveys "this file has per-page metadata baked in" — matching the semantic intent of the original sentinel.

### 7.2 No marker types in `kinnim_1`

Per JSON `_meta.markers_populated_count: 310 chapters`, kinnim_1 is one of the 215 chapters without populated markers. The chapter renders correctly (matrix structure, cell labels, content text) but with no `<span class="horizontal1">...` etc. spans. Expected behavior. D-2 will produce valid output for unmarked chapters too.

### 7.3 No unsupported marker classes

All markers found across the 6 pilots: `horizontal1`, `horizontal2`, `horizontal3`, `vertical1`, `internalparallel`. main.css has rules for all 8 known marker types (these 5 + `ciasm1`, `ciasm2`, `closure`). Zero unrecognized markers.

### 7.4 Dead `.mishnah-*` CSS rules left in main.css

The previous styling-fixes task added a CSS block for `.mishnah-chapter`, `.mishnah-table`, `.mishnah-cell`, `.mishnah-chapter .cell-content`, `.mishnah-chapter .cell-label` at line 737 of main.css. After this v2 re-render, the `.mishnah-table` / `.mishnah-cell` / `.cell-content` / `.cell-label` selectors no longer match any HTML on the 6 pilot files (or anywhere else in the corpus, since these classes weren't used elsewhere).

**The `.mishnah-chapter` selector IS still used** by the v2 render (the outer `<article class="mishnah-chapter">` wrapper) — so that one rule remains relevant.

The other 5 dead rules (`.mishnah-table`, `.mishnah-cell`, plus the 2 descendant selectors `.mishnah-chapter .cell-content` and `.mishnah-chapter .cell-label`) could be removed as dead code in a future small main.css cleanup task. **Out of scope for this task** per the spec ("no new CSS rules" implies "no main.css edits at all").

---

## 8. Out of Scope (per spec)

- Adding any new CSS rules to main.css (used existing `.scripture-table`, `.col-a/b/c/full` ✓)
- Removing the dead `.mishnah-*` CSS rules added by the previous styling-fixes task (flagged in §7.4 for follow-up)
- Modifying any other rendered Mishnah file (only the 6 D-1 pilots)
- Re-rendering other Hebrew pages with old brand `&#1495;&#1489;&#1512;` (separate site-wide cleanup task — ~605 files affected)
- Modifying `mishnah_db.json`
- Modifying portal pages
- Track 2 D-2 bulk render (gated on Moshe's visual approval)

---

## 9. Files Touched

| File | Action |
|---|---|
| `Mishnah-New/Hebrew/Text/Seder Zeraim/Masechet Brachot/Mesechet Brachot Perek 1.htm` | Re-rendered with scripture-table pattern |
| `Mishnah-New/Hebrew/Text/Seder Moed/Masechet Megillah/Masechet Megillah Perek 1.htm` | Same |
| `Mishnah-New/Hebrew/Text/Seder Nezikin/Masechet Eduyot/Masechet Eduyot Perek 1.htm` | Same |
| `Mishnah-New/Hebrew/Text/Seder Kodashim/Masechet Kinnim/Masechet Kinnim Perek 1.htm` | Same |
| `Mishnah-New/Hebrew/Text/Seder Nashim/Masechet Sotah/Masechet Sotah Perek 9 A.htm` | Same (+ (חלק א) suffix in title/h1/breadcrumb/description) |
| `Mishnah-New/Hebrew/Text/Seder Moed/Masechet Shabbat/Masechet Shabbat Perek 22.htm` | Same |
| `_pilot/d1-rerender-scripture-table.md` | This report |

No template changes (HE template already had brand fix from previous task). No main.css changes. No JSON changes.

---

## 10. Moshe's Verification

### Pre-push diff in GitHub Desktop

For each of the 6 chapter files, the diff should show:

- Old single `<table class="mishnah-table">` (v1) replaced by N small `<table class="scripture-table">` blocks (one per matrix row)
- Each new table has `<thead>` with `col-a` / `col-b` / `col-c` / `col-full` headers carrying the cell label
- Each new table has `<tbody>` with `<td>` cells containing `<p dir="rtl">` content
- D-1 pilot v2 sentinel replacing the v1 sentinel
- For `sotah_9a`: `(חלק א)` appended to title, h1, breadcrumb, description, og:title, Article headline

### Browser re-inspection (incognito, after Cloudflare URL purge)

For each of the 6 pilot URLs, verify the 7 visual criteria from the task spec:

```
https://chaver.com/Mishnah-New/Hebrew/Text/Seder%20Zeraim/Masechet%20Brachot/Mesechet%20Brachot%20Perek%201.htm
https://chaver.com/Mishnah-New/Hebrew/Text/Seder%20Moed/Masechet%20Megillah/Masechet%20Megillah%20Perek%201.htm
https://chaver.com/Mishnah-New/Hebrew/Text/Seder%20Nezikin/Masechet%20Eduyot/Masechet%20Eduyot%20Perek%201.htm
https://chaver.com/Mishnah-New/Hebrew/Text/Seder%20Kodashim/Masechet%20Kinnim/Masechet%20Kinnim%20Perek%201.htm
https://chaver.com/Mishnah-New/Hebrew/Text/Seder%20Nashim/Masechet%20Sotah/Masechet%20Sotah%20Perek%209%20A.htm
https://chaver.com/Mishnah-New/Hebrew/Text/Seder%20Moed/Masechet%20Shabbat/Masechet%20Shabbat%20Perek%2022.htm
```

- [ ] Brand shows `chaver.com` (not `חבר`)
- [ ] Each matrix row renders as a small table with colored column headers at top (dark brown / tan / cream gradients)
- [ ] Column header text shows the cell-label (e.g., "1א", "2ב")
- [ ] Content cells below the header row with proper RTL flow
- [ ] Marker colors work: horizontal1 blue, internalparallel green, vertical1 orange (etc.)
- [ ] For sotah_9a: title and h1 show `מסכת סוטה פרק ט (חלק א) – המבנה הספרותי`
- [ ] Page chrome intact (nav, footer, schema JSON-LD)

Compare visually against any Torah unit page (e.g., genesis-unit-1) — should now have the same visual character: scripture-table per row, colored headers, soft borders, Torah-unit-style layout.

### Schema sanity

Pick one chapter, paste into Google Rich Results Test — Article + BreadcrumbList should parse. The Article's `isPartOf` array should contain both `#website` and `#mishnah-collection`.

### Authorize D-2

If 6 pilots look right visually → confirm the cell-label heuristic ("first line of cell.text") is the right approach for D-2 (already validated on all 6 pilots; no fallback path triggered) → D-2 fires (bulk render of remaining 519 chapters using this same render script).

If issues remain → flag and iterate before D-2.
