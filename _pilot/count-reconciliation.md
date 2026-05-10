# Count Reconciliation: 128 vs 148 Chapters with Markers

**Date:** 2026-05-10

---

## 1. Counts by Definition

| Definition | Count | Complement (to populate) |
|---|---|---|
| Cell-level markers only (cell.markers non-empty, no sub markers) | 46 | — |
| Subdivision markers only (no cell-level markers) | 20 | — |
| Both cell AND subdivision markers | 82 | — |
| **Union (any markers anywhere)** | **148** | **376** |
| Cell-level only (ignoring subdivisions) | 128 | 396 |
| No markers at all | 376 | — |

Total: 524 chapters.

---

## 2. Source of the Discrepancy

The **128** figure (used in MIGRATION-STATE.md) came from a Python check that only looked at `cell.markers`:

```python
has_markers = any(c.get('markers') for r in v.get('rows',[]) for c in r.get('cells',[]))
```

This misses 20 chapters where markers exist ONLY inside `cell.subdivisions[*].markers` — not at the cell summary level.

The **148** figure (the correct count) includes ALL chapters with any structural markup, whether at cell level or subdivision level.

---

## 3. The 20-Chapter Difference Set

These chapters have subdivision-level markers but no cell-level markers:

| Chapter key | Sub markers | Types present |
|---|---|---|
| `bavametzia_7` | 19 | internal_parallel |
| `berakhot_8` | 7 | horizontal1 |
| `berakhot_9` | 7 | horizontal1, vertical1 |
| `challah_1` | 24 | closure, horizontal1, horizontal2, horizontal3, internal_parallel, vertical1 |
| `challah_2` | 20 | horizontal2, horizontal3, internal_parallel, vertical1 |
| `challah_3` | 9 | horizontal1, vertical1 |
| `eruvin_10` | 51 | chiastic1, chiastic2, closure, horizontal1, internal_parallel |
| `kilayim_6` | 9 | vertical1 |
| `maaser_sheni_5` | 18 | horizontal1, horizontal2, horizontal3, internal_parallel |
| `maasrot_3` | 4 | internal_parallel |
| `middot_3` | 14 | horizontal1, internal_parallel |
| `moed_katan_1` | 38 | chiastic1, chiastic2, horizontal1, horizontal2, horizontal3, internal_parallel, vertical1 |
| `orlah_2` | 19 | horizontal1, internal_parallel |
| `peah_1` | 10 | horizontal1, internal_parallel, vertical1 |
| `peah_4` | 9 | horizontal1, internal_parallel |
| `peah_7` | 2 | horizontal1 |
| `sukkah_3` | 12 | horizontal1, vertical1 |
| `terumot_11` | 4 | internal_parallel |
| `terumot_2` | 16 | horizontal1, horizontal2, horizontal3, internal_parallel, vertical1 |
| `terumot_9` | 3 | internal_parallel |

These are NOT empty chapters. Several have extensive markup (eruvin_10: 51 markers across 5 types; moed_katan_1: 38 markers across 7 types). They must not be overwritten.

---

## 4. Recommendation for Pass 3

**Use the strict/union definition:** skip a chapter if ANY markers exist at either level.

Rationale:
- The 20 subdivision-only chapters contain real, manually-entered structural analysis (up to 51 markers per chapter, using all marker types including rare ones like chiastic1/chiastic2 and closure).
- Overwriting them with a fresh extraction would destroy existing data that may have been manually curated.
- The conservative approach (skip 148, populate 376) loses nothing — we can always re-extract the 148 later in a separate comparison pass if the docx has updates.
- The "pragmatic" option (extract everything but log changes) is unnecessarily risky for a first bulk run. Better to skip safely, then do a targeted comparison pass for the 148.

**Implementation:**

```python
def has_any_markers(chapter):
    for row in chapter.get('rows', []):
        for cell in row.get('cells', []):
            if cell.get('markers'):
                return True
            for sub in cell.get('subdivisions', []):
                if sub.get('markers'):
                    return True
    return False
```

---

## 5. MIGRATION-STATE.md Updated

Section 3 ("Mishnah dataset current state") now reflects:
- 148 chapters with existing markers (union definition)
- 376 chapters to populate
- Explicit note about the skip criterion for Pass 3
