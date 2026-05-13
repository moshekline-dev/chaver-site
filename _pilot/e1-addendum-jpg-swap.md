# E-1 Addendum — Swap og:image PNG → JPG

**Date:** 2026-05-13
**Scope:** Replace the 37 KB PNG default OG image with a 191 KB JPG across the same 781 files E-1 touched. WhatsApp was rendering small-thumbnail cards from the PNG; the JPG renders correctly as the large hero card.
**Status:** **All 781 files updated. 0 errors. JPG file verified at correct dimensions/format/size.** Applies on top of E-1's uncommitted changes — push as one combined commit. **Not committed.**

---

## 1. Headline

| Metric | Value |
|---|---:|
| JPG saved to repo | `torah-weave/Admin/Assets/Images/og-default-1200x630.jpg` |
| JPG file size | 195,859 B (191.3 KB) |
| JPG dimensions | 1200 × 630 ✓ |
| JPG format | JPEG (SOI 0xFFD8) ✓ |
| Files in scope | 781 (2 templates + 174 EN + 605 HE) |
| Files updated | 781 (100%) |
| Files with PNG remaining in og: context | 0 ✓ |
| Files with `og:image:type` set to `image/jpeg` | 781 / 781 ✓ |
| Files with PNG remaining in non-og:meta context | 0 ✓ |
| Files ending with `</html>` | 781 / 781 ✓ |
| JSON-LD parse errors introduced | 0 ✓ |
| Mean size delta per file | +1 byte (`.png` → `.jpg` is 0 chars, but `image/png` → `image/jpeg` is +1) |
| Old PNG file kept in repo | yes (37,345 B at same path; not deleted) |

---

## 2. Part 1 — JPG File Saved and Verified

The JPG file was saved at the canonical path. Programmatic validation:

```
Size: 195859 bytes (191.3 KB)        ← within the 100-300 KB range ✓
Is JPEG (SOI 0xFFD8): True            ← magic bytes match ✓
Dimensions: 1200×630                  ← matches spec ✓
```

All four checks pass. The PNG counterpart (37,345 B) is intentionally retained at `og-default-1200x630.png` in case any external references exist; we'll add a redirect later if needed.

---

## 3. Part 2 — Bulk Replacement Results

Per-file operations:

1. **Literal string replace**: `og-default-1200x630.png` → `og-default-1200x630.jpg`. Each file had 3 such occurrences (`og:image`, `og:image:secure_url`, `twitter:image`), all replaced.
2. **Scoped regex replace** inside `<meta property="og:image:type">` only: `image/png` → `image/jpeg`. Exactly 1 occurrence per file.

The bulk run was executed in two phases due to a bash timeout mid-pass: first pass updated 627 files before timeout, resume pass updated the remaining 154 files. Result is equivalent to a single atomic run.

### Per-language breakdown

| Set | Files updated |
|---:|---:|
| Templates (EN + HE) | 2 / 2 |
| Migrated EN | 174 / 174 |
| Migrated HE | 605 / 605 |
| **Total** | **781 / 781 (100%)** |

### File size deltas

| Statistic | Bytes |
|---|---:|
| Per-file delta | +1 (the `og:image:type` value gains 1 char: `image/png` → `image/jpeg`) |
| Total corpus delta | +781 bytes |
| File-name swap delta | 0 (`.png` and `.jpg` are both 4 chars) |

---

## 4. Per-File Verification (Full Audit)

| Check | Pass count | Result |
|---|---:|---|
| File contains `og-default-1200x630.jpg` (at least one) | 781 / 781 | ✓ |
| JPG appears exactly 3 times per file (image + secure_url + twitter:image) | 781 / 781 | ✓ |
| `<meta property="og:image:type" content="image/jpeg">` present | 781 / 781 | ✓ |
| No `<meta property="og:image:type" content="image/png">` remaining | 781 / 781 | ✓ |
| No `og-default-1200x630.png` in og: or twitter: meta contexts | 781 / 781 | ✓ |
| No `og-default-1200x630.png` in non-meta content (would be benign but flagged) | 781 / 781 | ✓ — none |
| File ends with `</html>` | 781 / 781 | ✓ |
| All JSON-LD blocks parse cleanly | 781 / 781 | ✓ |

---

## 5. Anomalies Encountered

### 5.1 Bash timeout mid-run

The first script invocation timed out at 45 seconds with 627 of 781 files complete. The script writes each file individually, so partial progress was persisted to disk. A resume script identified the remaining 154 files (still containing `.png` in their head) and completed them.

The resume script also had a fallback for the rare case where the filename swap was done but the `og:image:type` was not yet (none occurred in practice — the two replacements happen together per file). Final state matches what a single atomic run would have produced.

### 5.2 No other anomalies

No truncated files, no JSON-LD breakage, no benign-content PNG mentions. The replacement is purely surgical: 3 filename swaps + 1 mime-type swap per file.

---

## 6. Files Touched

| Category | Count |
|---|---:|
| `_templates/Academic-Content-EN.html` | 1 |
| `_templates/Academic-Content-HE.html` | 1 |
| Migrated EN files | 174 |
| Migrated HE files | 605 |
| `_pilot/e1-addendum-jpg-swap.md` (this report) | 1 |
| New asset: `torah-weave/Admin/Assets/Images/og-default-1200x630.jpg` | 1 (new) |
| Old asset: `torah-weave/Admin/Assets/Images/og-default-1200x630.png` | 0 (kept in place, unchanged) |

**Total file touches: 781 unique HTML/template files + 1 new asset = 782 changes.**

---

## 7. Moshe's Verification Checklist

### Spot-check via GitHub Desktop diff view (before pushing)

1. **Templates** — open `_templates/Academic-Content-EN.html` and `_templates/Academic-Content-HE.html` in the diff viewer. Confirm the 4 lines that changed: 3 in the E-1 block (og:image / og:image:secure_url / twitter:image content URLs swapped from `.png` to `.jpg`) and 1 line for `og:image:type` (`image/png` → `image/jpeg`).
2. **Sample 3 migrated pages** across both languages — same diff pattern, exactly 4 lines per file.
3. **JPG file** — confirm `og-default-1200x630.jpg` shows up as a new file in the working tree (195,859 B). The `og-default-1200x630.png` should appear unchanged (still 37,345 B).

### Push as one combined commit with E-1

```
git add -A
git commit -m "E-1: site-wide SEO/AEO boilerplate + JPG OG image"
git push
```

### After deploy

1. **Facebook Sharing Debugger** — paste `https://chaver.com/`, click "Scrape Again", confirm the large-card render with the cruciform image.
2. **WhatsApp** — share `https://chaver.com/` in a fresh conversation (one where chaver.com hasn't been shared before, or use a different device). Should render as a large card with the cruciform image. If it still shows a small icon, wait an hour for WhatsApp's CDN to refresh, then retry from a different account.
3. **Twitter Card Validator** — should show the JPG as the card image (`summary_large_image`).
4. **LinkedIn Post Inspector** — same.

### Rollback

```bash
git revert <commit-hash>
```

Or pre-commit, GitHub Desktop's "Discard changes" works per-file (but you'd lose E-1's changes too unless you discard selectively).

---

## 8. Out of Scope (per task spec)

- Anything beyond og:image and og:image:type meta tags
- Removing the old PNG file (kept in place per task spec — 301 redirect deferred)
- E-2 work (per-page canonical, breadcrumb, article schema)
- E-3 work (special pages)
