# D-1 Mishnah Chapter Styling Fixes

**Date:** 2026-05-14
**Scope:** Two main edits — (1) Add CSS rules for `.mishnah-chapter` / `.mishnah-table` / `.mishnah-cell` / `.cell-content` / `.cell-label` to `main.css` mirroring proven Torah `.matrix-table` styling adapted for RTL Hebrew. (2) Fix Hebrew template's hardcoded brand text `חבר` → `chaver.com`. Plus a small Option-A patch to the 6 D-1 pilot files so they match.
**Status:** **8 files modified cleanly. 0 errors, all defensive checks pass.** **Not committed.**

---

## 1. `main.css` — Mishnah Chapter CSS Block

### Placement

| Property | Value |
|---|---|
| Sentinel comment | `/* === Mishnah chapter page — D-1 pilot styling === */` |
| Inserted at line | **737** (immediately after `.matrix-table .cell-label` rule closing brace at line 735) |
| Block extends through | line 779 (`/* === /Mishnah chapter page styling === */`) |
| Followed by | line 782+ (`/* Color Legend */` — pre-existing next section) |

### Size delta

| Metric | Bytes |
|---|---:|
| Before | 76,188 |
| After | 77,292 |
| **Delta** | **+1,104** |

Within the expected 1,100–1,800 byte range.

### Defensive checks

| Check | Result |
|---|---|
| Atomic write (temp + fsync + rename) | ✓ |
| Post-write byte-size verify | ✓ |
| Sentinel comment exactly once | ✓ (1 occurrence) |
| Brace count balanced ({{ = `}}`)| ✓ (584 = 584) |
| Idempotency (skip if sentinel pre-existed) | ✓ (sentinel was not pre-existing) |

### Inserted CSS (verbatim)

```css
/* === Mishnah chapter page — D-1 pilot styling === */
/* Mirrors .matrix-table styling for visual parity with Torah units */
/* Adapted for RTL Hebrew, vertical-align top, wider canvas */
.mishnah-chapter {
    direction: rtl;
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 1em;
}
.mishnah-chapter h1 {
    text-align: center;
    margin: 1em 0 1.5em;
    font-family: 'David', 'SBL Hebrew', 'Ezra SIL', 'Frank Ruehl', serif;
}
.mishnah-table {
    width: 100%;
    border-collapse: collapse;
    margin: 25px 0;
    background-color: #f8f9fa;
    font-size: 0.95em;
    direction: rtl;
    font-family: 'SBL Hebrew', 'Ezra SIL', 'David', 'Frank Ruehl', serif;
}
.mishnah-cell {
    padding: 12px;
    border: 1px solid #dee2e6;
    text-align: center;
    vertical-align: top;
}
.mishnah-chapter .cell-content {
    margin: 0;
    text-align: center;
    direction: rtl;
    line-height: 1.7;
}
.mishnah-chapter .cell-label {
    display: inline-block;
    font-size: 0.9em;
    color: #666;
    font-weight: bold;
    margin-bottom: 0.5em;
}
/* === /Mishnah chapter page styling === */
```

---

## 2. `_templates/Academic-Content-HE.html` — Brand Text Fix

### Change

Single one-line edit inside the `<header class="site-header">` block:

```diff
- <div class="nav-brand">&#1495;&#1489;&#1512;</div>
+ <div class="nav-brand">chaver.com</div>
```

### Size delta

| Metric | Bytes |
|---|---:|
| Before | 15,052 |
| After | 15,041 |
| **Delta** | **−11** |

(Three HTML entities of 7 chars each = 21 bytes → "chaver.com" = 10 bytes → −11 bytes net.)

### Defensive checks

| Check | Result |
|---|---|
| Atomic write | ✓ |
| Post-write byte verify | ✓ |
| File ends with `</html>` | ✓ |
| `<div class="nav-brand">chaver.com</div>` count = 1 | ✓ |
| `<div class="nav-brand">&#1495;&#1489;&#1512;</div>` count = 0 | ✓ |
| Idempotency check | ✓ (would have skipped if already fixed) |

---

## 3. 6 D-1 Pilot Files — Brand Patch (Option A)

Each file got the same one-line `nav-brand` div replacement so the pre-rendered pilots match the template fix.

### Per-file results

| File | Size before | Size after | Δ | Replacements | JSON-LD blocks | D-1 sentinel |
|---|---:|---:|---:|---:|---:|:-:|
| `Mishnah-New/Hebrew/Text/Seder Zeraim/Masechet Brachot/Mesechet Brachot Perek 1.htm` | 22,690 | 22,679 | −11 | 1 | 3 | ✓ |
| `Mishnah-New/Hebrew/Text/Seder Moed/Masechet Megillah/Masechet Megillah Perek 1.htm` | 26,238 | 26,227 | −11 | 1 | 3 | ✓ |
| `Mishnah-New/Hebrew/Text/Seder Nezikin/Masechet Eduyot/Masechet Eduyot Perek 1.htm` | 28,428 | 28,417 | −11 | 1 | 3 | ✓ |
| `Mishnah-New/Hebrew/Text/Seder Kodashim/Masechet Kinnim/Masechet Kinnim Perek 1.htm` | 21,753 | 21,742 | −11 | 1 | 3 | ✓ |
| `Mishnah-New/Hebrew/Text/Seder Nashim/Masechet Sotah/Masechet Sotah Perek 9 A.htm` | 23,953 | 23,942 | −11 | 1 | 3 | ✓ |
| `Mishnah-New/Hebrew/Text/Seder Moed/Masechet Shabbat/Masechet Shabbat Perek 22.htm` | 22,160 | 22,149 | −11 | 1 | 3 | ✓ |

(JSON-LD block count is 3 per file = E-1 `@graph` stub + BreadcrumbList + Article. The `@graph` block declares 3 entities — WebSite/Org/Person — inside a single `<script>` element. Total entity references = 5, but script blocks = 3. The task spec's "5 blocks" referenced entities; my count above is script tags. Both are correct.)

### Per-file defensive checks

For each of the 6 files, all checks pass:

| Check | Result |
|---|---|
| Replacement count == 1 | ✓ |
| Atomic write + byte-size verify | ✓ |
| File ends with `</html>` | ✓ |
| All JSON-LD blocks parse | ✓ (3/3 per file) |
| D-1 pilot sentinel still present | ✓ |
| `.mishnah-table` markup preserved | ✓ |

---

## 4. Issue → Fix Cross-Reference

The 6 visual issues Moshe surfaced from the megillah_1 screenshot:

| # | Issue | Fix applied |
|---|---|---|
| 1 | Cells of unequal content vertical-centered (rows don't read as rows) | `.mishnah-cell { vertical-align: top; }` |
| 2 | Adjacent cell content runs together — no visible column gap | `.mishnah-cell { padding: 12px; }` + `.mishnah-cell { border: 1px solid #dee2e6; }` |
| 3 | Hebrew template brand says `חבר` instead of `chaver.com` | Template edit + 6 pilot-file patches |
| 4 | Lines inside cells right-align instead of centering | `.mishnah-cell { text-align: center; }` + `.mishnah-chapter .cell-content { text-align: center; }` |
| 5 | Matrix table narrow on desktop, doesn't use available width | `.mishnah-chapter { max-width: 1400px; }` + `.mishnah-table { width: 100%; }` |
| 6 (bonus) | Cell labels (1א, 2, 3א) dominated cell content visually | `.mishnah-chapter .cell-label { font-size: 0.9em; color: #666; display: inline-block; margin-bottom: 0.5em; }` — subtle, doesn't dominate |

### Why these specific values

| Rule | Rationale |
|---|---|
| `max-width: 1400px` | Wider than the default `.content-wrapper` (1200px); matrix tables benefit from horizontal canvas |
| `vertical-align: top` (critical fix for issue 1) | Browser default is `middle`; matrix layout requires `top` for row alignment |
| `padding: 12px` | Matches `.matrix-table td` padding; provides visible column gap (fixes issue 2) |
| `border: 1px solid #dee2e6` | Matches Torah `.matrix-table` cell borders for visual parity |
| `text-align: center` | Fixes issue 4; matches Torah unit cell behavior |
| `background-color: #f8f9fa` | Same light-grey as `.matrix-table`; visual consistency across Torah and Mishnah |
| `line-height: 1.7` | Hebrew text with multi-line cell content needs generous line height for readability |
| Cell-label `font-size: 0.9em; color: #666` | Matches `.matrix-table .cell-label` — subtle visual hierarchy, label doesn't dominate the content |

---

## 5. Out of Scope (flagged for follow-up)

### 5.1 Other Hebrew pages with old brand text

The HE template has been used to render hundreds of Hebrew pages (via Phase B/C/Track 1 migrations). Those pages all have the OLD `<div class="nav-brand">&#1495;&#1489;&#1512;</div>` baked in. A site-wide string-replace task is needed to bring them in line. Estimated scope: ~605 Hebrew migrated pages. Quick `sed`-style operation; can be a small Cowork task later.

This task's scope is ONLY the 6 D-1 pilot files + the template. Other HE pages stay as-is for now.

### 5.2 Marker visual styles inherited from existing `main.css`

The chapter markup uses `.horizontal1`, `.horizontal2`, `.horizontal3`, `.vertical1`, `.internalparallel`, `.ciasm1`, `.ciasm2`, `.closure` classes. These rules already exist in `main.css` (verified during the recon report) — both lowercase (JSON-native) and capitalized (Word-export legacy) forms. **No marker CSS was modified in this task.** Marker color/background styles continue to render via the existing rules.

### 5.3 Legacy `.Mesechet`-cascade rules

`main.css` lines 3337–3361 contain rules for the OLD Hebrew Mishnah cascade (`.Mesechet`, `.Albeck`, `.Perek`, etc.) from the Word-export pipeline. Those rules serve the still-Phase-B-migrated chapter pages that haven't been re-rendered by D-2 yet. **Left untouched** per scope.

### 5.4 Mobile responsive tweaks

The new `.mishnah-chapter` block has no `@media` queries. On narrow viewports (phones), the matrix table will use the default `.matrix-table` mobile rule (already in `main.css` at line 3094-ish: shrink-to-fit `font-size: 0.65em`). If Moshe's re-inspection surfaces mobile-specific issues, a follow-up CSS task can add `@media (max-width: 768px)` rules targeting `.mishnah-table` specifically.

### 5.5 Track 2 D-2 bulk render

Still gated on visual approval. Once Moshe confirms the 6 pilots look right (now styled correctly), authorize D-2 to bulk-render all 525 chapters.

---

## 6. Verification Approach

### What Cowork validated

- DOM structure of the 6 chapter files after the brand patch (5-pages JSON-LD parses, sentinels preserved, file integrity)
- CSS block syntactic validity (brace balance in main.css)
- HE template structure post-edit (still ends with `</html>`)
- Byte-level deltas within expected ranges

### What only browser inspection can confirm

CSS rules render correctly. Specifically:

- Visual padding actually appears between cells
- Hebrew font preference falls back correctly when SBL Hebrew isn't installed
- The 1400px `max-width` doesn't cause overflow on mid-size displays
- Color/border visibility works across light/dark browser themes
- The new rules don't inadvertently shadow any inherited cascade (e.g., a more-specific selector elsewhere that overrides our `vertical-align: top`)

Moshe's browser re-inspection (in incognito, with Cloudflare cache purge for main.css) is the final acceptance gate.

---

## 7. Cache-Bust Recommendation

After push, the changed assets are:

- `torah-weave/Admin/Assets/CSS/main.css` (heavily cached — long TTL)
- `_templates/Academic-Content-HE.html` (template; doesn't render directly; affects future renders only)
- 6 chapter `.htm` files

**For main.css specifically**: Cloudflare caches CSS aggressively. After push, purge `https://chaver.com/torah-weave/Admin/Assets/CSS/main.css` in Cloudflare dashboard, OR add a cache-bust query string in DevTools when verifying.

**For chapter pages**: purge each of the 6 URLs, or wait for natural TTL (usually 1–4 hours).

---

## 8. Files Touched

| File | Action |
|---|---|
| `torah-weave/Admin/Assets/CSS/main.css` | +1,104 B — new Mishnah chapter CSS block inserted at line 737 |
| `_templates/Academic-Content-HE.html` | −11 B — `nav-brand` div content fixed |
| 6 D-1 pilot `.htm` files | −11 B each — `nav-brand` div content fixed |
| `_pilot/d1-styling-fixes.md` | This report |

**Total: 8 files modified + 1 report.**

---

## 9. Moshe's Verification

### Pre-push diff in GitHub Desktop

| File | Expected diff |
|---|---|
| `main.css` | One new ~43-line CSS block inserted after the `.matrix-table .cell-label` rule, bracketed by `/* === Mishnah chapter page — D-1 pilot styling === */` / `/* === /Mishnah chapter page styling === */` |
| `Academic-Content-HE.html` | One-line change in `<div class="nav-brand">` |
| 6 chapter `.htm` files | Identical one-line change in each (the same brand div) |

No other diffs expected.

### After push + Cloudflare cache purge (especially main.css)

Re-inspect the 6 pilot URLs in browser (incognito to bypass browser cache):

```
https://chaver.com/Mishnah-New/Hebrew/Text/Seder%20Zeraim/Masechet%20Brachot/Mesechet%20Brachot%20Perek%201.htm
https://chaver.com/Mishnah-New/Hebrew/Text/Seder%20Moed/Masechet%20Megillah/Masechet%20Megillah%20Perek%201.htm
https://chaver.com/Mishnah-New/Hebrew/Text/Seder%20Nezikin/Masechet%20Eduyot/Masechet%20Eduyot%20Perek%201.htm
https://chaver.com/Mishnah-New/Hebrew/Text/Seder%20Kodashim/Masechet%20Kinnim/Masechet%20Kinnim%20Perek%201.htm
https://chaver.com/Mishnah-New/Hebrew/Text/Seder%20Nashim/Masechet%20Sotah/Masechet%20Sotah%20Perek%209%20A.htm
https://chaver.com/Mishnah-New/Hebrew/Text/Seder%20Moed/Masechet%20Shabbat/Masechet%20Shabbat%20Perek%2022.htm
```

For each page check the 9 visual criteria from the task spec:

1. **Brand shows `chaver.com`** in the header
2. **Cells in same row align at top** (no longer vertically centered)
3. **Visible space/padding between columns**
4. **Text inside cells is centered**
5. **Content uses more horizontal width on desktop**
6. **Cell labels** (1א, 2, 3א) in smaller grey font
7. **Marker colors still working** (horizontal1 blue, internalparallel green, vertical1 orange, etc.)
8. **Hebrew text fonts** look right (SBL Hebrew / David / fallbacks)
9. **No layout regression** on JSON-LD blocks or page chrome

### Schema sanity

Pick one chapter, paste into Google Rich Results Test — Article + BreadcrumbList should still parse.

### Visual reference

Compare a Mishnah chapter page (now styled) against any Torah unit page (e.g., genesis-unit-1) — they should now have the SAME visual character (light bg, bordered cells, centered text, subtle labels, top-aligned).

### Authorize D-2

If all 6 pilots look right visually:

1. Answer the two D-2 prep questions (Sotah suffix display, cell-label heuristic confidence) when I draft D-2
2. I draft D-2; Cowork bulk-renders all 525 chapters

If anything is still off → flag specifics; we iterate before D-2.

---

## 10. Anomalies Encountered

### 10.1 Mid-script defensive-check tuning

The script's initial defensive check `if new_css.rstrip()[-1] != '}':` was too strict — `main.css` ends with a trailing `/* END OF MAIN.CSS */` comment block, so the last non-whitespace character is `/`, not `}`. CSS specs allow trailing comments. Adjusted the check to verify brace balance instead (`new_css.count('{') == new_css.count('}')`). Balance is 584 = 584 — the new block adds 6 rules with 6 opening braces and 6 closing braces, matching.

### 10.2 JSON-LD block count discrepancy in the spec

The task spec says "5 blocks: WebSite, Org, Person, BreadcrumbList, Article" — but the rendered D-1 pilots have **3 script blocks**: the E-1 `@graph` stub (containing WebSite/Org/Person inside one block) + BreadcrumbList + Article. The 5 count in the spec is entities, not script tags. My count of 3 script blocks is correct. Both views are valid.

### 10.3 The HE template fix only affects the template; existing Hebrew pages keep the old brand

Flagged in §5.1. About 605 already-migrated Hebrew pages still have `&#1495;&#1489;&#1512;` in their nav-brand. Out of scope for this task; separate site-wide cleanup task recommended.
