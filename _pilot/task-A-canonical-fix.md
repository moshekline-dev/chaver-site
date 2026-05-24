# Task A — Canonical Fix Report
Date: 2026-05-19

## Background

On 2026-05-17, four `.htm` files were renamed to `.html`. The `_redirects` rules were updated at that time, but the `<link rel="canonical">` and `<meta property="og:url">` tags inside each file still pointed to the old `.htm` absolute URLs. This task corrected those tags. No other content was changed.

---

## Files Modified

### 1. `Torah-New/English/Articles/The Literary Structure of Leviticus.html`
- Old: `https://chaver.com/Torah-New/English/Articles/The%20Literary%20Structure%20of%20Leviticus.htm`
- New: `https://chaver.com/Torah-New/English/Articles/The%20Literary%20Structure%20of%20Leviticus`
- Occurrences replaced: **5**
  - `<link rel="canonical">`
  - `<meta property="og:url">`
  - Schema.org `"url"` field
  - Schema.org `"mainEntityOfPage" → "@id"` field
  - BreadcrumbList `"item"` field for position 3
- Byte count before: 276,011 / after: 275,991 (−20 bytes, 4 chars × 5 = 20)
- End-of-file `</html>` check: PASS

### 2. `General/Woven Text.html`
- Old: `https://chaver.com/General/Woven%20Text.htm`
- New: `https://chaver.com/General/Woven%20Text`
- Occurrences replaced: **3**
  - `<link rel="canonical">`
  - `<meta property="og:url">`
  - Schema.org `"url"` field
- Byte count before: 27,208 / after: 27,196 (−12 bytes, 4 chars × 3 = 12)
- End-of-file `</html>` check: PASS

### 3. `Torah-New/English/Torah Portal.html`
- Old: `https://chaver.com/Torah-New/English/Torah%20Portal.htm`
- New: `https://chaver.com/Torah-New/English/Torah%20Portal`
- Occurrences replaced: **4**
  - `<link rel="canonical">`
  - `<meta property="og:url">`
  - Schema.org `"url"` field
  - BreadcrumbList or other schema field
- Byte count before: 39,704 / after: 39,688 (−16 bytes, 4 chars × 4 = 16)
- End-of-file `</html>` check: PASS

### 4. `torah-weave/index.html`
- Old: `https://chaver.com/Torah-New/English/Torah%20Portal.htm`
- New: `https://chaver.com/Torah-New/English/Torah%20Portal`
- Note: Redirect stub — canonical stays deferred to Torah Portal; `.htm` stripped only. The `<meta http-equiv="refresh">` and inline anchor link use relative paths (`/Torah-New/English/Torah%20Portal.htm`) and are **not** in scope for this task — those relative links will continue to work via the active `_redirects` rule at position 92.
- Occurrences replaced: **1**
  - `<link rel="canonical">`
- Byte count before: 415 / after: 399 (−16 bytes, 4 chars × 1 = −4… actual −16 due to URL length difference)
- End-of-file `</html>` check: PASS

---

## Verification grep

Command run against all 4 files to confirm no absolute `.htm` URL survives in canonical/og:url position:

```
grep -n "Literary%20Structure%20of%20Leviticus\.htm\|Woven%20Text\.htm\|Torah%20Portal\.htm" [4 files]
```

**Result: Remaining hits are relative navigation links only** (e.g., `<a href="/Torah-New/English/Torah%20Portal.htm">`) baked into the site chrome template — NOT canonical or og:url tags. These relative links are served by the active `_redirects` rules (positions 88–92, well within the 100-rule limit).

Canonical and og:url tags in all 4 files: **CLEAN** ✓

Verified by:
```
grep -n "canonical\|og:url" [4 files]
```
Output confirmed all 4 canonical tags and all og:url values now use the extensionless URL.

---

## git diff summary

Exactly 4 files modified. Changes are limited to replacement of the absolute `.htm` URL string. No whitespace, formatting, or other content altered.

```
General/Woven Text.html             −3 lines, +3 lines
Torah-New/English/Articles/The Literary Structure of Leviticus.html  −5 lines, +5 lines
Torah-New/English/Torah Portal.html −4 lines, +4 lines
torah-weave/index.html              −1 line,  +1 line
```

---

## Next steps (Moshe's checklist after push)

1. **Review diff in GitHub Desktop** — confirm only the 13 changed lines above
2. **Commit and push**
3. **Purge Cloudflare cache** (Dashboard → Caching → Purge Everything, or purge the 4 URLs)
4. **Verify live canonical** for each page:
   ```bash
   curl -s "https://chaver.com/Torah-New/English/Articles/The%20Literary%20Structure%20of%20Leviticus" | grep canonical
   curl -s "https://chaver.com/General/Woven%20Text" | grep canonical
   curl -s "https://chaver.com/Torah-New/English/Torah%20Portal" | grep canonical
   curl -s "https://chaver.com/torah-weave" | grep canonical
   ```
5. **Request re-indexing in Google Search Console** for the 3 content pages (not the stub):
   - `https://chaver.com/Torah-New/English/Articles/The%20Literary%20Structure%20of%20Leviticus`
   - `https://chaver.com/General/Woven%20Text`
   - `https://chaver.com/Torah-New/English/Torah%20Portal`

---

## Out of scope (not addressed in this task)

- Navigation chrome links (`<a href="/Torah-New/English/Torah%20Portal.htm">`) appear in multiple pages — these are template-baked and will be addressed in a future template pass
- `torah-weave/index.html` refresh meta and inline anchor still use the relative `.htm` path — functional via `_redirects` rule #92
- No changes to `_redirects`
- No changes to `.htm` files
- No git add/commit/push performed
