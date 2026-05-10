# Reverse-Engineer Notes: Academic-Content-DWT

## Source Page

- **File:** `torah-weave/Genesis/genesis-unit-1/genesis-unit-1-commentary.html`
- **Size:** 56,243 bytes, 924 lines
- **DWT:** `Dynamic Web Templates/Academic-Content-DWT.dwt`
- **Chosen because:** Representative Academic-Content page with all five editable regions populated. Used by 907 of the 933 DWT-attached pages.

## Editable Regions Extracted

| Region | Bytes | Lines | Content Summary |
|---|---|---|---|
| `doctitle` | 91 | 1 | `<title>` element |
| `meta` | 3,952 | 66 | Meta description, keywords, OG tags, Twitter cards, schema.org JSON-LD |
| `additional-styles` | 56 | 1 | Comment placeholder (page-specific CSS overrides) |
| `content` | 36,594 | 417 | Full page body: breadcrumb, header, article, nav, citation box |
| `page-scripts` | 48 | 1 | Comment placeholder (page-specific JS) |

**Total region content:** 40,741 bytes (72% of file)
**Scaffolding (template):** 14,898 bytes (EN), 14,908 bytes (HE)

## Files Created

| File | Size | Description |
|---|---|---|
| `Academic-Content-EN.html` | 14,898 B | English template scaffolding |
| `Academic-Content-HE.html` | 14,908 B | Hebrew variant (`lang="he" dir="rtl"`) |
| `_validation/genesis-unit-1-commentary-rendered.html` | 56,243 B | Round-trip reconstruction |

## Round-Trip Validation

**Result: PASS — byte-identical**

The rendered file (scaffolding + regions + re-inserted DWT markers) produces output identical to the original source file at the byte level. `cmp` reports no differences.

## EN vs. HE Structural Differences

The only difference between the two template files is the `<html>` tag:

- **EN:** `<html lang="en">`
- **HE:** `<html lang="he" dir="rtl">`

No other scaffolding differences exist. Properties that might be expected to differ (such as `og:locale` or `schema:inLanguage`) are located inside the `meta` editable region, not in the template scaffolding. This means:

### Decisions Requiring Human Judgment

1. **`og:locale` and `inLanguage`**: These are per-page values currently inside the `meta` region. If the migration system should set these automatically based on template variant, they would need to move from region content into the template scaffolding.

2. **`dir="rtl"` scope**: The HE template sets `dir="rtl"` on the `<html>` element. Some Hebrew pages may have mixed-direction content needing `dir="ltr"` overrides on specific elements. The current DWT does not handle this — all 692 Hebrew pages share the same `lang="en"` tag from the DWT, so this is an existing gap the migration can fix.

3. **Google Analytics**: The GA tag (`G-KNYXKY3VV1`) is baked into the scaffolding. If this needs to change per-environment or be removed for dev/staging, it would need to become a region or build-time variable.

4. **CSS path**: The scaffolding hardcodes `/torah-weave/Admin/Assets/CSS/main.css` as an absolute path. This works on the live site but may need adjustment if pages are ever served from a different base path.

## Placeholder Format

Editable regions in the template files are marked as:

```
    {{ region: name }}
```

Each placeholder sits on its own line with the same indentation as the original `<!-- #BeginEditable -->` marker. During migration, replace the entire placeholder line with the page's region content (preserving the content exactly as extracted, including its own indentation and line endings).

## Method

Extraction used position-based splitting rather than regex content capture to avoid whitespace boundary errors. Each region's content is defined as everything between the newline after `<!-- #BeginEditable "name" -->` and the start of the line containing `<!-- #EndEditable -->`. This preserves all original whitespace, `\r\n` line endings, and indentation exactly.
