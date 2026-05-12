# Mishnah Chapter Renderer — Design Notes

Working file capturing decisions for the upcoming Hebrew Mishnah chapter renderer (input: `Mishnah-New/English/mishnah_db.json` rev9 / 525 chapters; output: clean URLs under `/mishnah/<seder>/<masechet>-<perek>/`).

---

## Subdivision Rendering

**Decision: Subdivisions render as SEPARATE table rows, not folded into the parent cell's paragraph.**

The pilot Megillah page (`pilot/megillah-perek-1-marked.html`) folds subdivisions into the cell's single paragraph — the first subdivision letter (`A`) is part of the cell-label span, subsequent letters (`B`, `C`) get their own inline spans inside the same `<p>`. This is wrong for the production renderer.

The correct rendering: each subdivision becomes its own table row, so horizontal parallelism across columns works visually. Across columns, subdivision `A` lines up horizontally with the next column's subdivision `A`, etc.

### Why this matters

In the woven matrix, subdivisions within a cell are a sub-level of the row × column structure. They establish micro-horizontal parallels that are part of the scholarly markup. If they're stacked vertically within a cell, the eye can't track parallelism between them and the next column's subdivisions. Separate rows force the alignment that makes the structure readable.

### Implementation implication for the renderer

When a row has at least one cell with subdivisions, the row is rendered as multiple `<tr>` elements:

- First sub-row: the cell label (e.g., `2א`) in the leftmost cell of each multi-subdivision cell; cells without subdivisions span all sub-rows via `rowspan`.
- Each subsequent sub-row: one subdivision (`A`, `B`, `C`) per cell that has subdivisions.

For cells in the same row that have *different numbers of subdivisions*, the row count is the max across cells; cells with fewer subdivisions either get empty trailing rows or extend their last subdivision via `rowspan`. **Decision needed at renderer build time.** Plausible defaults:

1. **Extend-via-rowspan**: the cell with fewer subdivisions has its last subdivision span the remaining sub-rows. Reads as "this content continues." Risk: visually implies the subdivision belongs to multiple parallel rows.
2. **Empty trailing rows**: the cell with fewer subdivisions gets empty `<td>`s for the remaining sub-rows. Reads as "no parallel here." Risk: produces blank cells inside the matrix.

Recommend trying *empty trailing rows* first — it's the more honest visual: "no content here at this micro-row," and avoids accidental misreading of `rowspan` as a substantive structural claim.

### Reference

The pilot at `/pilot/megillah-perek-1-marked` does NOT follow this convention. Do not use it as the visual model for subdivisions. The existing legacy chapter pages at `/Mishnah-New/Hebrew/Text/Seder X/Masechet Y/Masechet Y Perek N.htm` should be checked to see how they handle subdivision rendering — they may already use separate rows.

---

## JSON Source Conventions (reminder)

From `_pilot/megillah-pilot-investigation.md` (Part 1, Section 5):

- The renderer reads `db[key].rows[*].cells[*].runs[]` — that's the authoritative ordered stream.
- Markers in `runs[*].marker` are the renderable ones; the per-cell `markers` list and per-subdivision `markers` list are dedupe views and should not be re-emitted.
- Cell shape comes from `db[key].shape` (e.g., `[[2,2], [1,2,1], [2,2]]`) — colspan derives from this.
- Subdivision content lives in `cells[*].subdivisions[]` with parallel `runs` semantics inside each.

---

## Open Decisions (to revisit before renderer build)

- Empty-trailing-rows vs. rowspan for uneven subdivision counts (above).
- Mishnah-num prefix handling. The docx text includes `(א)`, `(ב)` etc. inside cells; some legacy pages preserve this, others strip. Pilot preserves. Production renderer should preserve until/unless Moshe specifies otherwise.
- Header-row chapter treatment. 13 chapters have a "header row" classifier firing (`avot_1`, `avot_2`, `beitzah_5`, `kilayim_1`, `meilah_1`, `middot_5`, `sanhedrin_7`, `shabbat_7`, `tahorot_1`). The renderer needs to know how those header rows display in the table.
- `sotah_9` split. The JSON has `sotah_9a` and `sotah_9b` only (no unified `sotah_9`). URL convention should be `/mishnah/nashim/sotah-9a/` and `/mishnah/nashim/sotah-9b/` (already noted in the path scheme).
