# D-1 v3 — Subdivision Alignment + Latin Column Labels

**Date:** 2026-05-14
**Sentinel:** `<!-- D-1 pilot v3: subdivision-aligned rendering @ 2026-05-14T16:03:33Z -->`
**Scope:** Re-render the same 6 D-1 pilot files with three render-logic changes. **Not committed.**
**Status:** **All 6 re-rendered cleanly. 0 errors across all verification checks.**

Supersedes D-1 v2 (`d1-rerender-scripture-table.md`). Same files, same template, same metadata — only the matrix-table inner markup changed.

---

## 1. Render-logic changes (v2 → v3)

| Change | v2 | v3 |
|---|---|---|
| Column header labels | Hebrew letter (`1א`, `2ב`) | Latin letter (`1A`, `2B`); spaces stripped (`1 א` → `1A`) |
| `<th>` classes | `class="col-a"` / `col-b` / `col-c` / `col-full` | `class="cell-label col-left"` / `col-middle` / `col-right` / `col-full` |
| Subdivision markers (`A`/`B`/`C`/`D`/`E` in JSON runs) | Plain text in cell body | `<span class="CellSubdivision"><b>a</b></span> ` (lowercase, with trailing space) |
| Table row structure | One `<tr>` per matrix row, all subdivisions in one `<td>` | One `<tr>` per **subdivision** within a matrix row; cells with fewer subdivisions get `rowspan` to span remaining rows |
| Cell-label stripping from body | Already done in v2 | Same — first newline in runs separates label from body |

All four classes — `col-left`, `col-middle`, `col-right`, `col-full` — already exist in `main.css` (lines 380–402) with gradient background rules. `span.CellSubdivision` exists at line 547 (`font-weight: bold; color: #666; margin-right: 5px`). Zero new CSS.

The convention matches Torah unit pages exactly (e.g. `torah-weave/Genesis/genesis-unit-7/genesis-unit-7.html` uses `<th class="cell-label col-left">2A</th>` and `<span class="CellSubdivision"><b>a</b></span>`).

---

## 2. Files re-rendered

| Chapter | Disk path | v2 size | v3 size | Δ | Row tables | Total subdiv spans |
|---|---|---:|---:|---:|---:|---:|
| `berakhot_1` | `…/Mesechet Brachot Perek 1.htm` | 22,740 | 22,939 | +199 | 3 | 0 |
| `megillah_1` | `…/Masechet Megillah Perek 1.htm` | 26,304 | 27,653 | +1,349 | 5 | 14 |
| `eduyot_1` | `…/Masechet Eduyot Perek 1.htm` | 28,185 | 28,885 | +700 | 4 | 6 |
| `kinnim_1` | `…/Masechet Kinnim Perek 1.htm` | 21,454 | 22,424 | +970 | 2 | 12 |
| `sotah_9a` | `…/Masechet Sotah Perek 9 A.htm` | 24,129 | 25,283 | +1,154 | 4 | 12 |
| `shabbat_22` | `…/Masechet Shabbat Perek 22.htm` | 22,122 | 22,959 | +837 | 3 | 8 |

Net total: +5,209 bytes across the 6 files. The growth reflects (a) extra `<tr>` wrappers for subdivision rows, (b) `<span class="CellSubdivision"><b>x</b></span>` overhead per subdivision (~50 bytes each, 52 total subdivisions × ~50 = ~2.6 KB), (c) the additional `cell-label ` class on each `<th>` (~12 bytes × ~25 ths = ~300 bytes).

Subdivision-span counts verified:
- `berakhot_1`: 0 (no subdivisions in any cell) ✓
- `megillah_1`: 14 — rows 2/3/4/5 have subdivs; row 2: 2+0+2=4, row 3: 2+2=4, row 4: 0+2+0=2, row 5: 2+2=4 → 14 ✓
- `eduyot_1`: 6 — only row 3 (idx 2) has subdivs; 3 cells × 2 = 6 ✓
- `kinnim_1`: 12 — both rows: outer cells have A/B/C, middle has 0; 2 rows × 6 = 12 ✓
- `sotah_9a`: 12 — rows 2 and 4 each have 3 subdivs × 2 cells = 6 each → 12 ✓
- `shabbat_22`: 8 — row 1 has A/B/C/D in both cells = 8; rows 2–3 have none ✓

---

## 3. Verification checks (per file)

| Check | berakhot_1 | megillah_1 | eduyot_1 | kinnim_1 | sotah_9a | shabbat_22 |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| File ends with `</html>` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| All JSON-LD blocks reparse | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `D-1 pilot v3:` sentinel count = 1 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `D-1 pilot v2:` sentinel count = 0 (stale removed) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Provenance marker count = 1 (timestamp refreshed) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `chaver.com` brand count = 1 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| E-1 boilerplate preserved (`<!-- /E-1 -->` count = 1) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| E-2 boilerplate preserved (`<!-- /E-2 -->` count = 1) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| No Hebrew letter (א–ה) inside any `<th class="cell-label …">` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `<table class="scripture-table">` count = shape rows | 3/3 | 5/5 | 4/4 | 2/2 | 4/4 | 3/3 |

**60/60 checks pass. 0 critical failures.**

---

## 4. Spot-verified structural cases

### 4.1 Symmetric 2-subdivision row (`megillah_1` row 3)

Both cells have subdivisions a/b. Headers `col-left` (colspan=2) + `col-right` (colspan=2). Body: 2 `<tr>`s, each holding two `<td colspan="2">`s with `<span class="CellSubdivision"><b>a</b></span>` resp. `b`.

### 4.2 Asymmetric (2/0/2) — middle cell rowspan (`megillah_1` row 2)

Shape `[1,2,1]` → 3 cells, max=2 subdivisions:

```html
<thead><tr>
  <th class="cell-label col-left">2A</th>
  <th class="cell-label col-middle" colspan="2">2B</th>
  <th class="cell-label col-right">2C</th>
</tr></thead>
<tbody>
  <tr>
    <td><p dir="rtl"><span class="CellSubdivision"><b>a</b></span> …</p></td>
    <td colspan="2" rowspan="2"><p dir="rtl">…</p></td>
    <td><p dir="rtl"><span class="CellSubdivision"><b>a</b></span> …</p></td>
  </tr>
  <tr>
    <td><p dir="rtl"><span class="CellSubdivision"><b>b</b></span> …</p></td>
    <!-- 2B spans from above -->
    <td><p dir="rtl"><span class="CellSubdivision"><b>b</b></span> …</p></td>
  </tr>
</tbody>
```

Subdivision `a` in cell 2A starts at the same vertical position as subdivision `a` in cell 2C. ✓

### 4.3 Asymmetric (3/0/3) — middle cell rowspan=3 (`kinnim_1` row 1)

Outer cells have a/b/c; middle cell `<td rowspan="3">` spans all 3 subdivision rows.

### 4.4 Asymmetric (0/2/0) — outer cells rowspan (`megillah_1` row 4)

Cell 4A has no subdivisions and gets `<td rowspan="2">`; cell 4B has subdivisions a/b in two separate `<tr>`s; cell 4C has no subdivisions and gets `<td rowspan="2">`.

### 4.5 4-subdivision symmetric (`shabbat_22` row 1)

Both cells have subdivisions a/b/c/d → 4 `<tr>`s, each with two `<td colspan="2">`s holding the matching subdivision.

### 4.6 Spaced Hebrew labels (`sotah_9a` all rows)

JSON labels like `'2 א'` (with space) → rendered as `<th class="cell-label col-left" colspan="2">2A</th>` (Latin, no space). Suffix `(חלק א)` preserved in `<h1>`.

### 4.7 Multi-run labels (`berakhot_1` row 0 cell 1; `eduyot_1` row 0 all cells)

JSON has the label split across multiple runs (e.g. `run[0]='1'`, `run[1]='ב'`, `run[2]='\n'`). The label-extraction walks runs until the first `\n` and concatenates everything before it. Result: `<th class="cell-label col-right" colspan="2">1B</th>` for the berakhot case. ✓

---

## 5. Implementation notes

### Strategy: surgical in-place replacement

The render script does **not** re-render whole files from the template. It loads each existing v2 `.htm`, replaces the inner content of `<main class="content-wrapper">…</main>`, updates the D-1 sentinel comment, and refreshes the provenance timestamp. E-1/E-2 boilerplate, canonical URL, og: meta, BreadcrumbList JSON-LD, Article JSON-LD, Google tag — all preserved byte-for-byte from D-1 v2.

This is safer than re-rendering from the template because it preserves any per-page metadata that may have been adjusted between renders.

### Atomic writes

Each file is written via temp file in the same directory → `fsync` → `os.replace`. Post-write verification reads the file back, checks byte-count, confirms `</html>` terminator, reparses every `<script type="application/ld+json">` block, and confirms exactly one v3 sentinel + zero v2 sentinels.

### Label extraction

Walk `runs[]` from index 0, concatenating `text` until the first `\n` (in a `marker is None` run) is encountered. Everything before the `\n` = label; rest becomes `body_runs`. This handles all three observed label patterns:
1. Single-run label: `[0]='2א'`, `[1]='\n'` (most cells)
2. Split-letter label: `[0]='1'`, `[1]='ב'`, `[2]='\n'` (`berakhot_1`/`eduyot_1` row 0 anomaly)
3. Spaced label: `[0]='1 א'`, `[1]='\n'` (`sotah_9a`)

After extraction, `normalize_label()` strips spaces and converts trailing Hebrew letter via `{א→A, ב→B, ג→C, ד→D, ה→E}`.

### Subdivision detection

In `body_runs`, a "subdivision marker run" is one where `marker is None AND text.strip() in {A,B,C,D,E}`. Body is segmented at marker positions; each segment's letter is lowercased and wrapped in `<span class="CellSubdivision"><b>letter</b></span> ` (trailing space matches the Torah-unit convention). The whitespace-only run that typically follows a marker (`{'text': ' ', 'marker': None}`) is skipped to avoid a leading `<br>` in the rendered segment.

### Rowspan algorithm

For a row with `N_i` subdivisions in cell `i` and `max = max(N_i)`:

- If `N_i == max` → one `<td>` per `<tr>`, no rowspan
- If `N_i == 0` → emit `<td rowspan="max">` at `<tr>` 0, skip in subsequent `<tr>`s
- If `0 < N_i < max` → emit `<td>` for subdivisions `0..N_i-2`, then `<td rowspan="(max - N_i + 1)">` for subdivision `N_i-1`, skip in remaining `<tr>`s

`colspan` is preserved from the JSON cell's `position.colspan` field and combined with the row-span attribute.

---

## 6. Anomalies / out-of-scope flags

### 6.1 Sotah 9 split

The canonical JSON (`Mishnah-New/English/mishnah_db.json`) has both `sotah_9a` and `sotah_9b` as separate records (526 total keys = 524 standard + 2 Sotah halves). The corresponding files `…/Masechet Sotah Perek 9 A.htm` and `…/Masechet Sotah Perek 9 B.htm` exist on disk. This v3 task touched only the `A` file (per the pilot list). The B file remains as last rendered by the prior pipeline (`@ 2026-05-13T11:17:22Z`).

**Decision pending for D-2:** is `sotah_9b` ready to be rendered by the v3 pipeline? Its JSON record has `shape=[[1,1,1] × 4]` with appropriate runs and a valid `source_url`. If approved, D-2 will pick it up automatically as one of the 525+1 chapters in the bulk run.

### 6.2 Note on the previous `kinnim_1` shape discrepancy

The D-1 v2 report stated `kinnim_1` shape was `[[1,1,1] × 2]` (2 rows, 3 cells each). The canonical JSON has `[[1,1,1], [1,1,1]]` (also 2 rows, 3 cells each). The v3 render uses the canonical JSON, which agrees with the v2 report's count of "2 row-tables emitted." So no discrepancy in practice — the v2 report's shape notation was just abbreviated.

### 6.3 Dead `.mishnah-*` CSS rules in main.css

The v2 report flagged dead CSS rules (`.mishnah-table`, `.mishnah-cell`, `.mishnah-chapter .cell-content`, `.mishnah-chapter .cell-label`) at lines 737+ of main.css. v3 still uses none of these except `.mishnah-chapter` (the outer `<article class="mishnah-chapter">` wrapper). The other 5 rules remain dead code.

The `.mishnah-chapter .cell-label` rule (display: inline-block; margin-bottom: 0.5em; etc.) WILL now apply to v3's `<th class="cell-label …">` headers because they sit inside `<article class="mishnah-chapter">`. Visual impact is expected to be minor — the existing `.scripture-table thead th` rules dominate for layout (padding, font-weight, color), and the descendant rule's `font-size: 0.9em` and `margin-bottom: 0.5em` may add slight tweaks. **Recommend visual review on the deployed pages.** If undesirable, scope an out-of-tree main.css cleanup to remove the dead `.mishnah-chapter .cell-label` rule (and the other 4 dead `.mishnah-*` rules).

### 6.4 Berakhot 1 row 0 cell 1 — anomalous JSON label

`db['berakhot_1']['rows'][0]['cells'][1]['label'] == '1'` (Hebrew letter `ב` lives in `run[1]`, not the label field). The v3 label-extraction logic recovers the full `'1ב'` → `1B` via the run-walking heuristic. This is a JSON-side data quirk; the renderer handles it correctly. Same pattern in `eduyot_1` row 0 (all cells). **No JSON fix needed.**

---

## 7. Out of scope (per spec)

- D-2 bulk render (gated on Moshe's visual approval of v3)
- CSS changes to main.css (no new CSS; dead-rule cleanup flagged in §6.3)
- Portal page changes
- Non-pilot chapter files
- Modifying `mishnah_db.json`
- Site-wide Hebrew brand cleanup (separate task — ~605 files)

---

## 8. Files touched

| File | Action |
|---|---|
| `Mishnah-New/Hebrew/Text/Seder Zeraim/Masechet Brachot/Mesechet Brachot Perek 1.htm` | v3 re-rendered (in-place; `<main>` content + sentinel + provenance) |
| `Mishnah-New/Hebrew/Text/Seder Moed/Masechet Megillah/Masechet Megillah Perek 1.htm` | Same |
| `Mishnah-New/Hebrew/Text/Seder Nezikin/Masechet Eduyot/Masechet Eduyot Perek 1.htm` | Same |
| `Mishnah-New/Hebrew/Text/Seder Kodashim/Masechet Kinnim/Masechet Kinnim Perek 1.htm` | Same |
| `Mishnah-New/Hebrew/Text/Seder Nashim/Masechet Sotah/Masechet Sotah Perek 9 A.htm` | Same |
| `Mishnah-New/Hebrew/Text/Seder Moed/Masechet Shabbat/Masechet Shabbat Perek 22.htm` | Same |
| `_pilot/d1_v3_render.py` | New render script (will be reused by D-2 for the full 525-chapter bulk) |
| `_pilot/d1-v3-subdivision-alignment.md` | This report |

No template changes. No main.css changes. No JSON changes.

---

## 9. Moshe's visual verification checklist

### Browser inspection (incognito, after Cloudflare purge)

| Page | Expected v3 behavior |
|---|---|
| `…/Mesechet Brachot Perek 1.htm` | Headers `1A`/`1B`/`2`/`3A`/`3B` (Latin); rows render same as v2 (no subdivisions to align) |
| `…/Masechet Megillah Perek 1.htm` | Row 2: 2A subdiv `a` and 2C subdiv `a` start at same vertical position; middle 2B spans both. Row 4: 4B subdivs `a`/`b` flow; 4A and 4C span both rows |
| `…/Masechet Eduyot Perek 1.htm` | Only row 3 shows subdivisions `a`/`b` aligned across all 3 cells |
| `…/Masechet Kinnim Perek 1.htm` | Both rows: outer cells show `a`/`b`/`c` aligned; middle cell spans all 3 |
| `…/Masechet Sotah Perek 9 A.htm` | Title `מסכת סוטה פרק ט (חלק א) – המבנה הספרותי`; rows 2 and 4 show subdivisions `a`/`b`/`c` aligned |
| `…/Masechet Shabbat Perek 22.htm` | Row 1 shows 4 subdivisions `a`/`b`/`c`/`d` aligned in both cells |

### General checks

- [ ] `chaver.com` brand in nav (unchanged from v2)
- [ ] Page chrome intact (header, nav, footer, schema JSON-LD)
- [ ] Marker colors render: `horizontal1` blue, `horizontal2`/`horizontal3` distinct, `internalparallel` green, etc.
- [ ] Subdivision labels `a`/`b`/`c`/`d` appear in muted bold gray (`span.CellSubdivision` rule)
- [ ] Column headers `1A`/`2B`/`3C` etc. show gradient backgrounds (`col-left` dark brown, `col-middle` tan, `col-right` cream) — unchanged from v2 visually since `col-a/b/c` and `col-left/middle/right` share the same gradient rules in main.css

### Schema sanity

Paste any of the 6 rendered pages into the Google Rich Results Test. Article + BreadcrumbList should parse. The Article's `isPartOf` array should still contain both `#website` and `#mishnah-collection`.

### Authorize D-2

If 6 pilots look right visually → confirm subdivision-alignment is the right approach for the bulk corpus (estimated 710 rows across 525 chapters have at least one subdivision; 73 rows have asymmetric subdivision counts requiring rowspan) → D-2 bulk render fires using the same `d1_v3_render.py` extended to all 525 chapter records.

If issues remain → flag and iterate before D-2.

---

## 10. Pre-push diff in GitHub Desktop (per file)

Each of the 6 files will diff as:

- Header `<th>` classes change: `col-a` → `cell-label col-left`, `col-b` → `cell-label col-middle`, `col-c` → `cell-label col-right`, `col-full` → `cell-label col-full`
- Header label content change: Hebrew `1א`/`2ב` etc. → Latin `1A`/`2B` etc.
- For chapters with subdivisions: `<tbody>` expands from one `<tr>` per matrix row to N `<tr>`s per matrix row (one per subdivision); inline subdivision letters (`A`/`B`/`C`...) are removed from the cell text and replaced by `<span class="CellSubdivision"><b>a</b></span> ` (lowercase) at the start of each subdivision's `<td>` content
- D-1 sentinel: `v2: scripture-table` → `v3: subdivision-aligned`
- Provenance timestamp: refreshed to v3 render time

No changes outside the `<main>` content region. All E-1/E-2 metadata + JSON-LD schema preserved byte-for-byte.
