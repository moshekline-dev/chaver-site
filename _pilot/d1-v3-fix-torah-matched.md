# D-1 v3-fix — Torah-Matched HTML Structure

**Date:** 2026-05-14
**Sentinel:** `<!-- D-1 pilot v3-fix: torah-matched rendering @ 2026-05-14T18:35:46Z -->`
**Scope:** Re-render the same 6 D-1 pilot files. Structure now matches the live Torah unit exemplar (`torah-weave/Genesis/genesis-unit-1/genesis-unit-1.html`) exactly. **Not committed.**
**Status:** **All 6 re-rendered cleanly. 0 errors. All v3 → v3-fix invariants hold.**

Supersedes D-1 v3 (`d1-v3-subdivision-alignment.md`). Same render-time decisions (Latin labels, lowercase subdivisions, subdivision-per-`<tr>` alignment); the structural change is in how cells map to `<th>`/`<td>` elements.

---

## 1. What v3 got wrong

D-1 v3 mapped the JSON's `cell.position.colspan` field directly to `<th colspan>` and `<td colspan>` attributes. So when a chapter had a 3-cell row with shape `[1,2,1]`, v3 emitted:

```html
<thead><tr>
  <th class="cell-label col-left">2A</th>
  <th class="cell-label col-middle" colspan="2">2B</th>  <!-- colspan -->
  <th class="cell-label col-right">2C</th>
</tr></thead>
<tbody><tr>
  <td>...2A...</td>
  <td colspan="2" rowspan="2">...2B...</td>             <!-- colspan -->
  <td>...2C...</td>
</tr>...</tbody>
```

The Torah unit exemplar uses **no colspan, anywhere**. One `<th>` per cell, one `<td>` per cell. Width distribution is controlled by a table-level class (`single-col`, `three-col`, etc.). The v3 output was visually wrong because the column gradients ran across two columns for the middle cell, the column widths didn't match the cell counts, and the layout broke at narrow viewports.

## 2. The v3-fix structural change

| Aspect | v3 (broken) | v3-fix |
|---|---|---|
| `<th colspan>` | Yes (from `position.colspan`) | **Never** — one `<th>` per cell |
| `<td colspan>` | Yes (same source) | **Never** — one `<td>` per cell |
| `<td rowspan>` | Yes, for asymmetric subdivisions | **Same** — kept (in `<tbody>` only) |
| Table class | `scripture-table` always | `scripture-table` + width modifier: `single-col` (1-cell), bare (2-cell, default), `three-col` (3-cell) |
| Content paragraph | `<p dir="rtl">` | `<p class="torah" dir="rtl">` (matches Torah exemplar's serif font + line-height) |

All four width classes already exist in `main.css`:
- `.scripture-table tbody td` (default) → `width: 50%` (line 335)
- `.scripture-table.three-col tbody td` → `width: 33.33%` (line 345)
- `.scripture-table.single-col tbody td` → `width: 100%` (line 351)
- `.scripture-table .torah` → Palatino, 1.125rem, line-height 1.8, justify (line 419)

Zero new CSS.

## 3. Files re-rendered (v3 → v3-fix)

| Chapter | v3 size | v3-fix size | Δ | Row tables | Subdiv spans | Asymmetric rowspans |
|---|---:|---:|---:|---:|---:|---:|
| `berakhot_1` | 22,939 | 23,018 | +79 | 3 | 0 | 0 |
| `megillah_1` | 27,653 | 27,901 | +248 | 5 | 14 | 3 (row 2 middle, row 4 left+right) |
| `eduyot_1` | 28,885 | 29,297 | +412 | 4 | 6 | 0 |
| `kinnim_1` | 22,424 | 22,734 | +310 | 2 | 12 | 2 (row 0 middle, row 1 middle) |
| `sotah_9a` | 25,283 | 25,393 | +110 | 4 | 12 | 0 |
| `shabbat_22` | 22,959 | 23,041 | +82 | 3 | 8 | 0 |

Net total: +1,241 bytes (mainly the extra `class="torah"` tokens on every `<p>` — ~13 bytes × ~80 paragraphs ≈ 1 KB, plus the `single-col` / `three-col` class additions).

## 4. Table-class distribution

| Chapter | bare (2-cell) | `single-col` (1-cell) | `three-col` (3-cell) |
|---|---:|---:|---:|
| `berakhot_1` | 2 | 1 | 0 |
| `megillah_1` | 3 | 0 | 2 |
| `eduyot_1` | 0 | 0 | 4 |
| `kinnim_1` | 0 | 0 | 2 |
| `sotah_9a` | 4 | 0 | 0 |
| `shabbat_22` | 3 | 0 | 0 |
| **Totals** | **12** | **1** | **8** |

Sum: 21 row-tables across 21 matrix rows (3+5+4+2+4+3 = 21). ✓

## 5. Header position-class distribution

| Chapter | `col-left` | `col-middle` | `col-right` | `col-full` |
|---|---:|---:|---:|---:|
| `berakhot_1` | 2 | 0 | 2 | 1 |
| `megillah_1` | 5 | 2 | 5 | 0 |
| `eduyot_1` | 4 | 4 | 4 | 0 |
| `kinnim_1` | 2 | 2 | 2 | 0 |
| `sotah_9a` | 4 | 0 | 4 | 0 |
| `shabbat_22` | 3 | 0 | 3 | 0 |
| **Totals** | **20** | **8** | **20** | **1** |

`col-middle` appears only in 3-cell rows (megillah row 2+4, eduyot all 4 rows, kinnim both rows). `col-full` only in `berakhot_1` row 2 (the single full-width row across all 6 pilots).

## 6. Verification (60 checks; all pass)

| Check (per file) | berakhot_1 | megillah_1 | eduyot_1 | kinnim_1 | sotah_9a | shabbat_22 |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| `colspan=` count in `<main>` = 0 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `rowspan` count in `<thead>` = 0 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| No `<t[hd]>` with both `colspan` AND `rowspan` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `<td>` count == `<p class="torah">` count | 5/5 | 19/19 | 15/15 | 14/14 | 16/16 | 12/12 |
| No Hebrew letter (א–ה) in any `<th class="cell-label …">` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `D-1 pilot v3-fix:` sentinel count = 1 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Stale `D-1 pilot v3:` sentinel count = 0 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Stale `D-1 pilot v2:` sentinel count = 0 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Provenance marker count = 1 (timestamp refreshed) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| File ends with `</html>` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| All JSON-LD blocks reparse | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| E-1 + E-2 + `chaver.com` brand preserved | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

## 7. Spot-verified structural cases

### 7.1 Berakhot 1 — mixed widths (2-cell, 1-cell, 2-cell)

Row 1: `<table class="scripture-table" dir="rtl">` (bare, 50%/50%) with `col-left 1A` + `col-right 1B`.
Row 2: `<table class="scripture-table single-col" dir="rtl">` (full-width) with `col-full 2`.
Row 3: bare, `col-left 3A` + `col-right 3B`.

### 7.2 Megillah 1 Row 2 — 3-cell asymmetric, middle has `rowspan="2"`

```html
<table class="scripture-table three-col" dir="rtl">
    <thead>
        <tr><th class="cell-label col-left">2A</th><th class="cell-label col-middle">2B</th><th class="cell-label col-right">2C</th></tr>
    </thead>
    <tbody>
        <tr>
            <td><p class="torah" dir="rtl"><span class="CellSubdivision"><b>a</b></span> (ג) …</p></td>
            <td rowspan="2"><p class="torah" dir="rtl">אף על פי …</p></td>
            <td><p class="torah" dir="rtl"><span class="CellSubdivision"><b>a</b></span> (ד) …</p></td>
        </tr>
        <tr>
            <td><p class="torah" dir="rtl"><span class="CellSubdivision"><b>b</b></span> באלו …</p></td>
            <td><p class="torah" dir="rtl"><span class="CellSubdivision"><b>b</b></span> אין בין אדר …</p></td>
        </tr>
    </tbody>
</table>
```

Three header cells (no colspan), three `<th class="cell-label col-…">` with distinct position classes. Middle `<td rowspan="2">` (no colspan). Subdivision `a` in 2A starts at the same vertical position as subdivision `a` in 2C — exact match to the spec's expected output.

### 7.3 Kinnim 1 Row 0 — 3-cell, middle `rowspan="3"`

3 subdivisions (a/b/c) in 1A and 1C; middle cell `<td rowspan="3">` with no subdivisions, spanning all three subdivision rows.

### 7.4 Megillah 1 Row 4 — 3-cell with outer cells `rowspan="2"`

4A and 4C have no subdivisions; both get `<td rowspan="2">`. Middle 4B has subdivisions a/b across two `<tr>`s.

### 7.5 Shabbat 22 Row 1 — 4 subdivisions

Both cells have subdivisions a/b/c/d. Four `<tr>`s, each with two simple `<td>`s, no rowspan.

### 7.6 Sotah 9a — spaced labels normalized

JSON labels like `'1 א'` → `<th class="cell-label col-left">1A</th>` (Latin, no space). h1 keeps `(חלק א)` suffix.

## 8. Implementation notes

### Strategy: still surgical in-place

The v3-fix render reads each existing v3 `.htm`, replaces the `<main class="content-wrapper">…</main>` inner content, swaps the D-1 sentinel comment, and refreshes the provenance timestamp. E-1/E-2 metadata, canonical URL, og: meta, schema JSON-LD, Google tag — all preserved byte-for-byte from v3 (which had preserved them from v2).

The script (`_pilot/d1_v3fix_render.py`) supersedes `_pilot/d1_v3_render.py`. The old v3 script has been deleted as obsolete; the v3 report (`d1-v3-subdivision-alignment.md`) stays as history.

### Subdivision-row algorithm (unchanged from v3, restated)

For a matrix row with `max = max(N_i)` subdivisions across cells `i`:

- `N_i == max` → one `<td>` per `<tr>`, no rowspan
- `N_i == 0` → emit `<td rowspan="max">` at `<tr>` 0, skip in subsequent `<tr>`s
- `0 < N_i < max` → emit `<td>` for subdivisions 0…N_i−2, then `<td rowspan="max − N_i + 1">` for the last subdivision; skip in remaining `<tr>`s

The only attribute on any `<td>` is `rowspan` (and only when > 1). No colspan.

### Label extraction (unchanged from v3)

Walk `runs[]` until the first `\n` in a non-marker run. Everything before becomes the label; everything after becomes `body_runs`. Handles all three observed label shapes:
1. Single-run label `[0]='2א'` followed by `[1]='\n'`
2. Split-letter label `[0]='1'`, `[1]='ב'`, `[2]='\n'` (berakhot_1 / eduyot_1 row 0)
3. Spaced label `[0]='1 א'`, `[1]='\n'` (sotah_9a)

`normalize_label()` strips spaces and converts trailing Hebrew א–ה → A–E. Latin labels, multi-letter Hebrew words, and bare numbers pass through unchanged.

## 9. Out of scope / D-2 prep

- D-2 bulk render — still gated on Moshe's visual approval of v3-fix.
- **4-cell and 5-cell rows** (per spec, 8 rows total — all in Avot and Eduyot; **none in the v3-fix pilots**): the current `table_class()` falls back to bare `scripture-table` for `n_cells >= 4`, which renders each `<td>` at `width: 50%` (wrong — too wide). Before D-2, decide one of:
  1. Add CSS rules `.scripture-table.four-col tbody td { width: 25%; }` and `.scripture-table.five-col tbody td { width: 20%; }` to main.css, and extend `table_class()` accordingly.
  2. Drop the per-cell width override entirely for `n_cells >= 4` and let the browser auto-distribute (`table-layout: fixed` is on `.scripture-table`, so width:50% per cell over 4–5 cells will overflow visibly — option 1 is preferred).
- **`sotah_9b`** exists in the canonical JSON and on disk (rendered at `2026-05-13T11:17:22Z` by the prior pipeline). Bring it into the v3-fix pipeline at D-2.
- **Dead `.mishnah-chapter .cell-label` rule** in main.css (lines 772–778) still applies to v3-fix's `<th class="cell-label …">` headers (article wrapper still uses `mishnah-chapter`). Visual impact likely minor but worth checking on the rendered pages. Scope a small main.css cleanup if needed.

## 10. Files touched

| File | Action |
|---|---|
| `Mishnah-New/Hebrew/Text/Seder Zeraim/Masechet Brachot/Mesechet Brachot Perek 1.htm` | v3-fix re-rendered (in-place `<main>` content + sentinel + provenance) |
| `Mishnah-New/Hebrew/Text/Seder Moed/Masechet Megillah/Masechet Megillah Perek 1.htm` | Same |
| `Mishnah-New/Hebrew/Text/Seder Nezikin/Masechet Eduyot/Masechet Eduyot Perek 1.htm` | Same |
| `Mishnah-New/Hebrew/Text/Seder Kodashim/Masechet Kinnim/Masechet Kinnim Perek 1.htm` | Same |
| `Mishnah-New/Hebrew/Text/Seder Nashim/Masechet Sotah/Masechet Sotah Perek 9 A.htm` | Same |
| `Mishnah-New/Hebrew/Text/Seder Moed/Masechet Shabbat/Masechet Shabbat Perek 22.htm` | Same |
| `_pilot/d1_v3fix_render.py` | New render script (D-2 will reuse) |
| `_pilot/d1_v3_render.py` | **Deleted** — superseded by v3fix |
| `_pilot/d1-v3-fix-torah-matched.md` | This report |

No template changes. No main.css changes. No JSON changes.

## 11. Pre-push diff in GitHub Desktop (per file)

Each v3 → v3-fix diff should show:

- `<table class="scripture-table" dir="rtl">` → `<table class="scripture-table three-col" dir="rtl">` (for 3-cell rows) or `<table class="scripture-table single-col" dir="rtl">` (for 1-cell rows)
- `<th class="cell-label col-X" colspan="N">` → `<th class="cell-label col-X">` (no colspan)
- `<td colspan="N" rowspan="M">` → `<td rowspan="M">` (colspan dropped) or `<td>` (both dropped where colspan was the only attribute)
- `<p dir="rtl">` → `<p class="torah" dir="rtl">`
- `D-1 pilot v3:` → `D-1 pilot v3-fix:` sentinel swap
- Provenance timestamp refreshed

No changes outside the `<main>` content region.

## 12. Moshe's visual verification checklist

### HTML grep checks

For each of the 6 files:

```
grep -c " colspan=" file.htm        # expect 0
grep -P '<thead>[\s\S]*?rowspan[\s\S]*?</thead>' file.htm   # expect no match
grep -c 'class="torah"' file.htm    # expect equal to <td> count
grep -c 'three-col' file.htm        # expect: berakhot=0, megillah=2, eduyot=4, kinnim=2, sotah=0, shabbat=0
grep -c 'single-col' file.htm       # expect: berakhot=1, others=0
grep -c 'D-1 pilot v3-fix:' file.htm  # expect 1
grep -c 'D-1 pilot v3:' file.htm    # expect 0
```

### Browser inspection

- [ ] Megillah 1 Row 2: three headers (2A, 2B, 2C) on ONE line, evenly spaced ~33% each
- [ ] Megillah 1 Row 2: subdivision `a` in 2A and `a` in 2C start at same vertical position
- [ ] Megillah 1 Row 2: 2B middle cell spans both subdivision rows (no break)
- [ ] Kinnim 1: three columns even-width, no overflow at standard widths
- [ ] Berakhot 1 Row 2: full-width row spans 100% of table width
- [ ] Content text in Palatino serif, line-height 1.8, justified (from `.torah` class)
- [ ] Header backgrounds: col-left dark brown, col-middle tan, col-right cream, col-full tan
- [ ] No layout breakage at narrow viewports (mobile)
- [ ] Schema validates in Google Rich Results Test (Article + BreadcrumbList)

### Authorize D-2

If v3-fix looks right visually → confirm 4-cell/5-cell handling decision (§9 bullet 2) → run D-2 on the full 525-chapter corpus using `d1_v3fix_render.py`.
