# Pilot Megillah Investigation + Hebrew Portal Path Update

**Date:** 2026-05-12
**Status:** Part 1 investigation done. Part 2 two-href edit applied. Preview regenerated. **Not committed.**

---

# Part 1 — Pilot Megillah Investigation

## 1. Verdict on whether a generator exists

**Mixed → effectively "hand-built once by an ad-hoc renderer that wasn't checked in."**

- The repo contains an **extractor** (`_pilot/mishnah_extractor_v2.py`, 36,260 bytes, v2.1.4) which reads `The Whole Structured Mishnah for pdf.docx` and **produces JSON** entries for `mishnah_db.json`. It does not produce HTML.
- The repo contains **no renderer/generator script** that turns JSON into HTML. I grepped every `.py` file in the repo for `horizontal1`, `<span class="Subunit`, `render`, `generate.*html`, `<table` — only the extractor matched, and only because it discusses these as concepts in comments. None of it emits HTML.
- The pilot files (`pilot/megillah-perek-1-marked.html` and `pilot/megillah-perek-1-he.html`) exist as **finished HTML** and were produced by a renderer that operated on `_pilot/megillah_1_extracted.json` (43 KB, a pre-rev9 single-chapter export). The renderer's *algorithm* is fully documented in `_pilot/megillah-1-render-report.md`, but the renderer's *code* is not in the repo. Most likely an assistant-generated script in a prior session that ran once and was discarded.

Practical consequence: a renderer **needs to be written**, but the visual target (pilot HTML), the input shape (JSON), and the algorithm (render report) are all already in hand.

## 2. Pilot file locations

| File | Bytes | Role |
|---|---:|---|
| `pilot/megillah-perek-1-marked.html` | 22,402 | The marker-annotated pilot (Megillah 1 with `horizontal1`/`horizontal2`/`horizontal3`/`internalparallel` spans) — served at `/pilot/megillah-perek-1-marked` |
| `pilot/megillah-perek-1-he.html` | 22,230 | Same chapter, **no marker spans** — plain table |
| `_pilot/megillah_1_extracted.json` | 43,292 | The JSON the renderer consumed |
| `_pilot/megillah-1-render-report.md` | 3,964 | The algorithm description |
| `_pilot/megillah-1-recon-report.md` | 8,919 | Word-doc inspection (how markers are encoded in the docx via character styles) |

## 3. Template inheritance

**Standalone, not template-inherited at render time.**

`pilot/megillah-perek-1-marked.html` is a complete HTML document with `<!DOCTYPE>` … `</html>`. The renderer appears to have used the HE-template scaffolding as a *base* (the head section, the GA snippet, the layout style block, the link to `main.css`) but emitted it inline rather than leaving `{{ region: ... }}` placeholders. The chapter's table is hand-emitted into where the `content` region would have been.

Concretely:
- `<html lang="he" dir="rtl">` ✓
- `<link rel="stylesheet" href="/torah-weave/Admin/Assets/CSS/main.css">` ✓
- Head's embedded `<style>` block is the same one in `_templates/Academic-Content-HE.html` (the "CRITICAL DWT LAYOUT STYLES ONLY" comment etc.) ✓
- **No `{{ region: ... }}` markers, no DWT `#BeginEditable` markers**
- A simple `<header class="banner-new">` welcome bar above the table (the marked variant only)

So the pilot is best described as: *the HE template's scaffolding with a static content body baked in*.

## 4. Structural rendering observations

The rendered table follows the exact pattern of the existing Hebrew chapter pages (per the render report's structural verification — `Masechet Megillah Perek 1.htm` was used as the visual reference):

- **Table wrapper.** `<div align="right"><table border="0" cellpadding="0" cellspacing="0" dir="rtl" width="100%">`. RTL is asserted on the table itself in addition to `<html dir="rtl">`.
- **Header row.** 4 cells, colspans `[1, 2, 1]`: `<p class="Mesechet">מסכת מגילה</p>` + `<p class="logo">המשנה כדרכה</p>` (colspan=2) + `<p class="Perek">פרק א</p>`.
- **Content rows.** 5 `<tr>` rows with cells matching shape `[[2,2], [1,2,1], [2,2], [1,2,1], [2,2]]`. Each cell carries a `colspan` (e.g., 2-cell rows have colspan=2 each; 3-cell rows have 1/2/1).
- **Trailing empty row.** A 4-cell `<tr>` of empty `<td>`s after the last content row — matches existing pages, presumably a spacing artifact.
- **Subdivisions inside cells.** Subdivisions are rendered **within the cell's single `<p>`**, not as separate rows. The first subdivision's `A` is *folded into the cell-label span*: `<span class="Subunit">2א<br/>A </span>`. Subsequent subdivisions get their own `<span class="Subunit">B </span>` inside the same paragraph. Lines within each subdivision are separated with `<br/>`.
- **Cell labels (non-subdivided).** Just `<span class="Subunit">LABEL<br/></span>` at the top of the cell paragraph.
- **Marker spans.** Each marker run becomes `<span class="{class}">{text}</span>` where `{class}` is one of `horizontal1`, `horizontal2`, `horizontal3`, `internalparallel` (and presumably `vertical1`, `closure`, `ciasm1`, `ciasm2` for other chapters that use them — none in Megillah 1).
- **Plain text + newlines.** Plain runs are emitted as-is; embedded `\n` characters become `<br/>`.

Notable patterns:
- **No hand-edits or TODO comments** in either pilot file's body.
- **Document order is preserved** from the JSON's `runs` array — the renderer never tries to reconstruct text from the `subdivisions` field or the unified `text` field. This is important: it avoids drift between the original docx ordering and the rendered page.
- **No use of the `markers` field** in the renderer. The per-cell `markers` and per-subdivision `markers` arrays in the JSON are dedupe views of what's in `runs`; the renderer ignores them.

## 5. JSON fidelity check (megillah_1, live `mishnah_db.json` rev9)

The live JSON for `megillah_1` and the rendered pilot match exactly on every counted dimension:

| Property | JSON (rev9) | Pilot HTML | Match? |
|---|---:|---:|:---:|
| Shape | `[[2,2],[1,2,1],[2,2],[1,2,1],[2,2]]` | `[[2,2],[1,2,1],[2,2],[1,2,1],[2,2]]` | ✓ |
| Total cells | 12 | 12 | ✓ |
| Cells with subdivisions | 7 | 7 | ✓ |
| `horizontal1` marker runs | 36 | 36 spans | ✓ |
| `horizontal2` marker runs | 2 | 2 spans | ✓ |
| `horizontal3` marker runs | 2 | 2 spans | ✓ |
| `internalparallel` marker runs | 10 | 10 spans | ✓ |
| **Total marker spans** | **50** | **50** | ✓ |
| Subunit spans | 19 (12 cell labels + 7 extra B-subdivision spans) | 19 | ✓ |

About the "62 markers" figure in the task description: the JSON exposes markers in two parallel views — `runs[*].marker` (50 entries, the renderer's actual input) and per-subdivision `markers` lists (12 entries; subdivision-level markers double-count what's already in the runs of the parent cell). 50 + 12 = 62. The renderer reads only the `runs` view; the pilot renders 50 spans, which is the right count and matches the source docx's marker count from the recon report.

**No discrepancies.** The pilot is a faithful rendering of `megillah_1`.

## 6. Recommendation — path to 525 chapters

**Write a fresh renderer.** It's small, the algorithm is fully specified, and the visual target is in hand. Concrete shape:

1. **Input**
   - `Mishnah-New/English/mishnah_db.json` (16.6 MB, rev9, 525 chapters)
   - `_templates/Academic-Content-HE.html` (the scaffold, with `{{ region: ... }}` placeholders intact — we want the renderer to *fill regions* rather than emit the scaffold inline, so future template edits propagate)

2. **Per-chapter algorithm** (transcribed from the render report)
   - Look up `db[<key>]` (e.g., `megillah_1`).
   - Emit the header row from `tractate_he` / "המשנה כדרכה" / `chapter_he` (e.g., `מסכת מגילה` / `המשנה כדרכה` / `פרק א`).
   - For each row in `rows`, emit a `<tr>` containing one `<td colspan="{colspan}">` per cell.
   - Inside each cell, walk the `runs` array in order:
     - First run is the cell label → `<span class="Subunit">LABEL<br/></span>`.
     - If the cell has subdivisions: the first subdivision letter is folded into the label span (`LABEL<br/>A `); subsequent subdivision letters get their own `<span class="Subunit">B </span>` etc. The subdivision boundary is detectable from the `runs` text (the next `(num)` or the next-letter pattern) — but it's safer to walk `subdivisions[]` in parallel and match the run text against the subdivision text.
     - Markered runs → `<span class="{marker}">{text}</span>`.
     - Plain runs → text as-is, with `\n` → `<br/>`.
   - Append the trailing empty 4-cell row.

3. **URL → key mapping**
   - URL scheme `/mishnah/<seder>/<masechet>-<perek>/`, e.g. `/mishnah/moed/megillah-1/`.
   - `seder_en` (lowercase) and `tractate_en` (lowercase) are already in the JSON entries → mapping is mechanical.
   - Special cases: `sotah_9a`, `sotah_9b` → `/mishnah/nashim/sotah-9a/`, `/mishnah/nashim/sotah-9b/`.

4. **Output**
   - 525 files at `mishnah/<seder>/<masechet>-<perek>/index.html` (clean URL → directory + index.html, consistent with existing `/torah-weave/hebrew-full-torah-map/index.html` convention).
   - The Hebrew Mishnah Portal at `mishnah/index.html` is a separate small task that links to all 525 chapters and offers seder-level groupings.

5. **Constraints worth flagging up-front**
   - 310 chapters have markers populated (per `_meta.markers_populated_count`); the other 215 will render as plain text only — that's fine and is the rev9 state of the data.
   - 13 chapters have a "header row" treatment; the render report says the renderer ignored these for the pilot. Re-confirm how the existing chapter pages handle header rows before generating all 525.
   - The two known-empty chapters (`ketubot_14`, `yadayim_4`) had structural shapes added in rev9 but no marker text yet — they'll render but won't be visually interesting.

6. **Suggested approach**
   - Build the renderer first against a 5-chapter sample (e.g., megillah_1, avot_1, berakhot_1, sotah_9a, shabbat_22) covering: marker-rich chapters, subdivisions, header-row treatment, the sotah split, and the shabbat_22 override.
   - Diff each rendered sample against the legacy `Mishnah-New/Hebrew/Text/.../Masechet * Perek *.htm` for structural fidelity (the recon work for Megillah 1 already established this is a clean comparison).
   - Once the sample passes, batch-generate all 525.

The renderer itself is probably a 300–500 line Python file. The bulk of the upcoming work is **deciding the URL layout for sedarim** (e.g., does `/mishnah/zeraim/` 301 from `/mishnah/seder-zeraim/`?), **building the portal page**, and **handling the legacy URL redirects** — none of which is in this task's scope.

---

# Part 2 — Nav and Footer Placeholder Updates

Two `href` values changed in `_templates/Academic-Content-HE.html`. No other content changed.

## Nav — שער המשנה destination

```diff
- <li><a href="/Mishnah-New/Hebrew/Mishnah%20Portal.htm">&#1513;&#1506;&#1512; &#1492;&#1502;&#1513;&#1504;&#1492;</a></li>
+ <li><a href="/mishnah/">&#1513;&#1506;&#1512; &#1492;&#1502;&#1513;&#1504;&#1492;</a></li>
```

Now at line 331 of the template, inside the משנה dropdown. Label `שער המשנה` unchanged.

## Footer — פורטל המשנה destination

```diff
- <li><a href="/Mishnah-New/Hebrew/Mishnah%20Portal.htm">&#1508;&#1493;&#1512;&#1496;&#1500; &#1492;&#1502;&#1513;&#1504;&#1492;</a></li>
+ <li><a href="/mishnah/">&#1508;&#1493;&#1512;&#1496;&#1500; &#1492;&#1502;&#1513;&#1504;&#1492;</a></li>
```

Now at line 380 of the template, inside the footer **המשנה כדרכה** section. Label `פורטל המשנה` unchanged.

## Verification

- `grep` for `Mishnah-New/Hebrew/Mishnah` in `_templates/Academic-Content-HE.html`: **no matches** (stale path is fully gone).
- `grep` for `href="/mishnah/"` in the template: **2 matches** (line 331 and line 380, exactly as intended).
- Preview regenerated: `_pilot/hebrew-nav-render-preview.html`, 14,265 bytes, no unresolved `{{ region: ... }}` markers, 2 occurrences of `href="/mishnah/"` in the rendered page.
- No other template lines changed (head, body wrappers, nav structure, other footer sections, scripts — all preserved).

## Status of the new placeholder

`https://chaver.com/mishnah/` → **HTTP 404** (expected; page yet to be built).

Both the nav and the footer share this one destination, so **building `/mishnah/` once** will resolve both chrome placeholders simultaneously — same one-page-resolves-multiple-links pattern as the existing color-code-guide placeholder.

---

# Recommended Next Task

Based on Part 1 findings:

**"Write the Hebrew Mishnah chapter renderer + build a 5-chapter sample"** — small, contained, low-risk, validates the algorithm against multiple corner cases before fanning out to 525.

Once the sample is reviewed and accepted:
- **Batch-generate all 525 chapters** at `/mishnah/<seder>/<masechet>-<perek>/index.html`.
- **Build the Hebrew Mishnah Portal** at `/mishnah/index.html` (resolves both chrome placeholders).
- **Add 301 redirects** in `_redirects` from the legacy `/Mishnah-New/Hebrew/Text/...` paths to the new clean URLs (probably a generated block — there are 524 legacy pages).

The portal page is the cheapest first deployment win — even a minimal "index" page at `/mishnah/` would clear the two 404s in the chrome, even before the 525 chapter pages exist.

---

## Files Touched

| File | Action |
|---|---|
| `_templates/Academic-Content-HE.html` | Two `href` values updated (lines 331 and 380) — `/Mishnah-New/Hebrew/Mishnah%20Portal.htm` → `/mishnah/` |
| `_pilot/hebrew-nav-render-preview.html` | Regenerated (14,265 bytes) |
| `_pilot/megillah-pilot-investigation.md` | This report |
