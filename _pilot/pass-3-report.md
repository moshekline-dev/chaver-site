# Pass 3 Report: Full Corpus Extraction

**Date:** 2026-05-10
**Extractor:** `_pilot/mishnah_extractor_v2.py` (v2.0)

---

## 1. Mapping Summary

| Metric | Count |
|---|---|
| Total docx tables | 544 |
| Tables with standard header (`מסכת X / פרק Y`) | 256 |
| Phase 1 (header matching) | 226 chapters |
| Phase 2 (text fingerprint, Jaccard > 0.4) | 175 chapters |
| Phase 3 (lower threshold, Jaccard > 0.25) | 36 chapters |
| **Total mapped** | **460** |
| JSON chapters with no docx match | 64 (52 in populate set, 12 in skip set) |
| Unmapped docx tables (front matter/dividers) | 84 |

The 52 unmatched populate-set chapters have no docx source available through automated matching. Their markers remain empty.

### Unmatched populate chapters by tractate (top causes)

These are concentrated in Seder Kodashim, Taharot, and some Nezikin tractates — likely because these tractates use non-standard table formats or alternate spellings in the docx that the matching algorithm couldn't resolve.

---

## 2. Classification Verification

| Category | Count | Expected | Match? |
|---|---|---|---|
| Skip (has markers, any level) | 148 | 148 | YES |
| Populate (no markers anywhere) | 376 | 376 | YES |

**VERIFIED before extraction began.**

---

## 3. Skipped-Chapters Byte-Identity Check

**PASS — all 148 chapters byte-identical after extraction.**

Every skipped chapter was serialized to JSON (with `sort_keys=True`) before and after the extraction pass. All 148 snapshots matched exactly. No existing scholarship was disturbed.

---

## 4. Extraction Results

| Outcome | Chapters |
|---|---|
| Successfully populated | 184 |
| No docx source (unmatched) | 52 |
| Shape mismatch (skipped) | 140 |
| **Total populate-set** | **376** |

### Shape mismatches

140 chapters were matched to docx tables but the cell counts didn't align (e.g., JSON expects 3 cells in a row but the docx table has 2). These were skipped entirely — no partial population.

Top affected tractates: Kelim (10), Negaim (10), Oholot (9), Niddah (8), Zevachim (8), Chullin (7), Menachot (7).

**Root cause:** The docx merged-cell structure may differ from what's recorded in the JSON. In `[1,2,1]`-shaped rows (3 cells with the middle spanning 2 columns), the raw XML sometimes presents 2 physical `<w:tc>` elements where the JSON expects 3. This needs investigation in a follow-up pass — likely a colspan-awareness fix in the extraction loop.

### Unknown character styles

One unknown style found: `Albeck` in `kilayim_9`. This is likely a citation/reference style (referring to the Albeck Mishnah edition), not a structural marker. Ignored.

---

## 5. Marker Totals

### By type (before → after)

| Marker type | Before | After | Delta |
|---|---|---|---|
| `horizontal1` | 1,127 | 3,138 | +2,011 |
| `internalparallel` | 0 | 1,238 | +1,238 |
| `vertical1` | 499 | 835 | +336 |
| `horizontal2` | 148 | 354 | +206 |
| `horizontal3` | 163 | 308 | +145 |
| `closure` | 53 | 138 | +85 |
| `internal_parallel` | 233 | 233 | 0 |
| `chiastic1` | 27 | 27 | 0 |
| `chiastic2` | 26 | 26 | 0 |
| `ciasm1` | 0 | 10 | +10 |
| `ciasm2` | 0 | 9 | +9 |
| **TOTAL** | **2,276** | **6,316** | **+4,040** |

### IMPORTANT: Naming inconsistency detected

The existing 148 chapters use: `internal_parallel`, `chiastic1`, `chiastic2`
The new 184 chapters use: `internalparallel`, `ciasm1`, `ciasm2`

These refer to the same structural features but are named differently:

| Existing (148 chapters) | New extraction (184 chapters) | Same feature? |
|---|---|---|
| `internal_parallel` | `internalparallel` | Yes — InternalParallel style |
| `chiastic1` | `ciasm1` | Yes — Ciasm1 style |
| `chiastic2` | `ciasm2` | Yes — Ciasm2 style |

**Action needed:** Before HTML rendering, either:
- (a) Normalize the existing names to match CSS classes (`internalparallel`, `ciasm1`, `ciasm2`), or
- (b) Add CSS rules for both naming conventions, or
- (c) Normalize the new names to match existing convention

Recommendation: Option (a) — normalize everything to CSS class names. The CSS classes are the canonical identifiers. This is a simple find-and-replace on the 148 existing chapters in a future task.

---

## 6. Subdivision Totals

| Metric | Before | After |
|---|---|---|
| Chapters with subdivisions | 316 | 367 |
| Chapters with subdivision-level markers | 102 | 285 |

51 new chapters gained subdivisions; 183 new chapters gained subdivision-level markers.

---

## 7. Anomalies

1. **Naming inconsistency** (see §5) — existing data uses `internal_parallel`/`chiastic1`/`chiastic2`; new extraction uses `internalparallel`/`ciasm1`/`ciasm2`. Both are correct for their respective sources; normalization needed.

2. **Shape mismatches (140 chapters)** — cell count in extracted docx doesn't match JSON. Most likely a merged-cell counting issue in the extraction loop (physical `<w:tc>` elements vs logical cells with colspans). Fixable in a follow-up pass with colspan-aware cell counting.

3. **Unknown style `Albeck`** in `kilayim_9` — appears to be a citation reference, not a structural marker. One occurrence; safely ignored.

4. **52 unmatched chapters** — no docx table could be confidently matched. These are mostly in Kodashim/Taharot tractates. May require manual identification or document-order inference in a follow-up.

---

## 8. Sample Populated Chapters

### `avodazara_2` (Seder Nezikin)
- Cell markers: 21, Subdivision markers: 0
- Examples: `[horizontal3] מתרפאין`, `[horizontal2] מפני ש`, `[horizontal3] מילדת`

### `bavabatra_1` (Seder Nezikin)
- Cell markers: 16, Subdivision markers: 0
- Examples: `[closure] שרצו`, `[horizontal1] מקום שנהגו`, `[horizontal1] מקום שנהגו`

### `bavametzia_1` (Seder Nezikin)
- Cell markers: 4, Subdivision markers: 13
- Examples: `[horizontal1] מציאת בנו ובתו`, `[horizontal1] הרי אלו`

### `bavakamma_1` (Seder Nezikin)
- Cell markers: 5, Subdivision markers: 0
- Examples: `[horizontal1] וכשהזיק חב המזיק לשלם...`, `[horizontal1] תמין`

### `avot_1` (Seder Nezikin)
- Cell markers: 5, Subdivision markers: 0
- Examples: `[horizontal3] כעבדים`, `[horizontal2] התורה`

---

## 9. File Size

| Metric | Value |
|---|---|
| Before | 5,099,317 bytes |
| After | 5,507,876 bytes |
| Delta | +408,559 bytes (+8.0%) |

---

## 10. Summary

| What | Value |
|---|---|
| Chapters populated in this pass | 184 of 376 (49%) |
| Markers added | +4,040 |
| Total markers now | 6,316 |
| Skip chapters disturbed | 0 (all 148 byte-identical) |
| Chapters still empty | 192 (52 unmatched + 140 shape mismatch) |
| JSON version | `2026-05-rev4` |

### Follow-up tasks for a future pass

1. **Fix naming inconsistency** — normalize `internal_parallel` → `internalparallel`, `chiastic1` → `ciasm1`, `chiastic2` → `ciasm2` across all 148 existing chapters.
2. **Fix shape mismatch** — investigate the 140 chapters with cell-count disagreements. Likely needs colspan-aware extraction that accounts for how python-docx reports merged cells vs how the JSON stores them.
3. **Match remaining 52 chapters** — use document-order inference or manual identification to match the 52 unmatched populate chapters to their docx tables.

---

## Files Modified

- `Mishnah-New/English/mishnah_db.json` — updated with 4,040 new markers across 184 chapters; `_meta` bumped to rev4

## Files Created

- `_pilot/pass-3-report.md` — this report
