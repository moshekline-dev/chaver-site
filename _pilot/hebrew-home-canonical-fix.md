# Hebrew Home Page Canonical Fix

**Date:** 2026-05-12
**File:** `hebrew index.html` (repo root)
**Status:** Fix applied. All 7 verification checks pass. **Not committed.**

---

## ⚠ Scope Note Up Front

The spec described 3 broken lines and asked for 3 edits. The actual file had **6 broken URL references** in the head section — the same bug patterns repeated in lines the spec didn't enumerate. The verification checks 5 and 6 ("no occurrences of `hebrew-portal`" / "no occurrences of `hebrew%20"`") can only be satisfied by fixing all 6. I treated check 7 ("rest of file unchanged") as "outside the canonical/SEO URL tags, nothing else modified" — the natural reading that resolves the spec's internal contradiction.

You'll see 6 modifications, not 3, in GitHub Desktop. Each is documented below so you can selectively revert any of them.

---

## 1. Before / After — Every Modified Line

### Edit A — Line 5 (truncated canonical → fixed)

```diff
- <link rel="canonical" href="https://chaver.com/hebrew%20">
+ <link rel="canonical" href="https://chaver.com/hebrew%20index">
```

### Edit B — Line 7 (truncated alternate hreflang="he" → fixed)

This was the **same truncation bug** as line 5 but on the alternate-hreflang tag. Same fix.

```diff
- <link rel="alternate" hreflang="he" href="https://chaver.com/hebrew%20">
+ <link rel="alternate" hreflang="he" href="https://chaver.com/hebrew%20index">
```

### Edit C — Lines 18–20 removed (duplicate broken hreflang block)

The head section had a **second** canonical + hreflang block at lines 18–20 with `hebrew-portal` URLs. The hreflang block at lines 4–8 already covers en / he / x-default correctly (after edits A and B), so the 18–20 block is pure duplication on top of being broken. All three lines removed.

```diff
      <meta name="author" content="Moshe Kline">
-     <link rel="canonical" href="https://chaver.com/hebrew-portal">
-     <link rel="alternate" hreflang="he" href="https://chaver.com/hebrew-portal">
-     <link rel="alternate" hreflang="en" href="https://chaver.com/">
-     
      <!-- Open Graph / Facebook -->
```

(Line 20's `hreflang="en" href="https://chaver.com/"` was a duplicate of the existing line 6, so removing it loses no information.)

### Edit D — Line 24 (og:url → fixed, now at line 21)

```diff
- <meta property="og:url" content="https://chaver.com/hebrew-portal">
+ <meta property="og:url" content="https://chaver.com/hebrew%20index">
```

### Edit E — Line 43 (schema.org JSON-LD url → fixed, now at line 40)

```diff
-         "url": "https://chaver.com/hebrew-portal.html",
+         "url": "https://chaver.com/hebrew%20index",
```

Note: this line also had the `.html` suffix while the rest of the site uses extensionless URLs as canonical. Both problems fixed in one substitution.

---

## 2. Verification — 7 Programmatic Checks All Passed

| # | Check | Result |
|---|---|---|
| 1 | Exactly 1 `rel="canonical"` tag | ✓ — line 5 only |
| 2 | Canonical href = `https://chaver.com/hebrew%20index` | ✓ |
| 3 | Exactly 1 `property="og:url"` tag | ✓ — line 21 only |
| 4 | og:url content = `https://chaver.com/hebrew%20index` | ✓ |
| 5 | No `hebrew-portal` anywhere in the file | ✓ — `grep` returned 0 matches |
| 6 | No truncated `hebrew%20"` anywhere | ✓ — `grep` returned 0 matches |
| 7 | Outside the SEO URL tags, no other lines modified | ✓ — title, meta description, keywords, Twitter card, second JSON-LD Book schema, body, footer, all untouched |

---

## 3. Final SEO URL State in the File

After the edits, the head section's URL declarations are consistent and minimal:

| Line | Tag | Value |
|---|---|---|
| 5 | `<link rel="canonical">` | `https://chaver.com/hebrew%20index` |
| 6 | `<link rel="alternate" hreflang="en">` | `https://chaver.com/` |
| 7 | `<link rel="alternate" hreflang="he">` | `https://chaver.com/hebrew%20index` |
| 8 | `<link rel="alternate" hreflang="x-default">` | `https://chaver.com/` |
| 21 | `<meta property="og:url">` | `https://chaver.com/hebrew%20index` |
| 40 | schema.org JSON-LD `"url"` | `https://chaver.com/hebrew%20index` |

Each is unique. Each points at the live page's canonical URL. No competing or contradictory signals for Google to weigh.

---

## 4. Structural Integrity Confirmation

The file's overall structure is preserved. I read the file via the Read tool after the edits — the `<!DOCTYPE>` declaration, `<html lang="he" dir="rtl">`, the rest of the head (title, descriptions, Twitter card, Open Graph image, OG locale, the Book schema JSON-LD block at lines 47+), nav, body content, and footer are untouched. The only modifications are the 6 enumerated edits above.

The net line-count change is **−3 lines** (three duplicate broken-URL lines removed at the old lines 18–20; the four edits A/B/D/E are same-line substitutions).

---

## 5. Expected SEO Impact

Per the task spec's "Why this matters" section: the page gets ~14 Bing AI citations per week, indicating real Hebrew-language search demand. Before this fix, Google would see:

- Two `<link rel="canonical">` tags (multiple canonicals = ambiguity signal → Google may pick one, suppress the page, or do neither)
- Both canonicals pointed at URLs that 404 or are truncated nonsense
- og:url disagreed with both canonicals
- Schema.org JSON-LD added a fourth distinct URL claim

After the fix: one canonical, one og:url, one schema URL, all matching the live page's actual address. Google should re-index over the next 2–4 weeks and stop suppressing it from search results.

---

## 6. Files Touched

| File | Action |
|---|---|
| `hebrew index.html` | 6 modifications in the head section as documented (4 same-line substitutions + 3 deleted duplicate lines = net −3 lines) |
| `_pilot/hebrew-home-canonical-fix.md` | This report |

No commits. Review the diff in GitHub Desktop; each of the 6 edits is a discrete, reviewable change.
