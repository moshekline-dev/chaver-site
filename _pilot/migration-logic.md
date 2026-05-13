# Migration Logic Spec — for the Bulk Migration Task

**Date:** 2026-05-13
**Purpose:** Documented algorithm + utilities for migrating DWT-attached `.html`/`.htm` pages to the new `_templates/Academic-Content-{EN,HE}.html` system. This doc consolidates everything the 4-page pilot established. The bulk migration script can implement it directly.

---

## 1. File Discovery

Find every page in the repo that is DWT-attached:

```python
import re
from pathlib import Path

REPO = Path('chaver-site')

def is_dwt_attached(path):
    if not path.suffix.lower() in ('.htm', '.html'):
        return False
    try:
        text = path.read_text(encoding='utf-8', errors='replace')
    except Exception:
        return False
    return '<!-- #BeginTemplate' in text

# Or use the existing template-registry.csv as the source of truth.
```

**Extension handling:** accept both `.htm` and `.html`. Some pages have one, some the other; both are valid. Two of the four pilot pages were `.html` despite the spec naming them `.htm` (Cloudflare clean-URL behavior hides the extension).

**Standalone pages:** any HTML file without `<!-- #BeginTemplate` and that we want to migrate. These need per-page judgment (the pilot's `hebrew index.html` was the only one).

---

## 2. Language Detection

Apply these rules in order — first match wins. If signals disagree (e.g., `lang="en"` but path is `/Hebrew/`), the path/DWT signal overrides the `<html lang>` declaration (this is the MAVO bug pattern):

1. Path contains `/Hebrew/` (case-sensitive `Hebrew`) → **HE**
2. Path contains `/hebrew` (case-insensitive) → **HE**
3. Source DWT is `hebrew.dwt` → **HE**
4. Source has `<html lang="he"...>` → **HE**
5. Otherwise → **EN**

When HE is forced because of path/DWT but the source has `<html lang="en">`, **log this as a `lang_corrected` event** so the migration report can call it out per-file. The new HE template hard-codes `<html lang="he" dir="rtl">` so just using the HE template implements the correction.

---

## 3. Region Extraction

### For `Academic-Content-DWT.dwt`-attached pages

5 regions, direct 1:1 mapping:

| Source region | Target placeholder |
|---|---|
| `doctitle` | `{{ region: doctitle }}` |
| `meta` | `{{ region: meta }}` |
| `additional-styles` | `{{ region: additional-styles }}` |
| `content` | `{{ region: content }}` |
| `page-scripts` | `{{ region: page-scripts }}` |

### For `hebrew.dwt`-attached pages

4 regions, with one rename:

| Source region | Target placeholder |
|---|---|
| `doctitle` | `{{ region: doctitle }}` |
| *(no `meta` region in hebrew.dwt)* | `{{ region: meta }}` ← empty string |
| `additional-styles` | `{{ region: additional-styles }}` |
| `start` | `{{ region: content }}` ← **name change** |
| `page-scripts` | `{{ region: page-scripts }}` |

### For `English.dwt`-attached pages

`English.dwt` is a third DWT type identified in the pre-migration survey (37 pages total). The survey found two region variants:

**Variant A — standard 5-region (31 pages):** same region names as `Academic-Content-DWT.dwt`. Use the same direct 1:1 mapping.

**Variant B — `writehere` region (6 pages in `torah-commentary-project/Commentaries/`):** 4 regions; `writehere` is the body content equivalent, with no `meta` region.

| Source region | Target placeholder |
|---|---|
| `doctitle` | `{{ region: doctitle }}` |
| *(no `meta` region in this variant)* | `{{ region: meta }}` ← empty string |
| `additional-styles` | `{{ region: additional-styles }}` |
| `writehere` | `{{ region: content }}` ← **name change** |
| `page-scripts` | `{{ region: page-scripts }}` |

The migration script picks the variant at runtime based on which regions are present:

```python
def map_english_dwt_regions(raw_regions):
    if 'writehere' in raw_regions:
        return {
            'doctitle': raw_regions.get('doctitle', ''),
            'meta': '',
            'additional-styles': raw_regions.get('additional-styles', ''),
            'content': raw_regions.get('writehere', ''),
            'page-scripts': raw_regions.get('page-scripts', ''),
        }
    # Standard 5-region variant — same mapping as Academic-Content-DWT
    return {k: raw_regions.get(k, '') for k in ['doctitle', 'meta', 'additional-styles', 'content', 'page-scripts']}
```

`English.dwt` pages with neither pattern (e.g., missing required regions) should be flagged for manual review, not auto-migrated.

### For standalone HTML files (per-page judgment)

Used for the pilot's `hebrew index.html`:

| Region | How extracted |
|---|---|
| `doctitle` | `<title>...</title>` from `<head>` (the entire tag, not just inner text) |
| `meta` | All `<head>` content **minus** charset, viewport, the `<title>`, the inline `<style>`, and any `<link rel="stylesheet" href="…main.css">` (template owns these) |
| `additional-styles` | The inline `<style>` block from `<head>` — kept verbatim, will be cleaned by `clean_nav_css_from_inline_style()` after substitution |
| `content` | `<body>` content between `</header>` and `<footer>` (if `<main>` exists in the body, use its inner contents instead) |
| `page-scripts` | Page-specific `<script>` blocks at end of body, excluding old `toggleMenu()`-style nav handlers (the new template owns those) and GA snippet (template owns) — usually empty for legacy standalone pages |

### Extraction regex (for DWT pages)

```python
RE_EDITABLE = re.compile(
    r'<!--\s*#BeginEditable\s+"([^"]+)"\s*-->'
    r'(.*?)'
    r'<!--\s*#EndEditable\s*-->',
    re.DOTALL
)

def extract_dwt_regions(text):
    return {m.group(1): m.group(2) for m in RE_EDITABLE.finditer(text)}
```

---

## 4. Template Substitution

```python
def render(template, regions):
    out = template
    for name in ['doctitle', 'meta', 'additional-styles', 'content', 'page-scripts']:
        out = out.replace('{{ region: ' + name + ' }}', regions.get(name, ''))
    return out
```

Simple string replacement — no template engine. The templates have exactly one occurrence of each placeholder.

---

## 5. Post-Substitution CSS Cleanup (REQUIRED)

After `render(...)`, run `clean_nav_css_from_inline_style()` to strip orphan nav-targeting rules from any inline `<style>` blocks. This catches:

- Rules inherited from the **template's** "CRITICAL DWT LAYOUT STYLES" inline `<style>` block (the templates still have several `header.site-header`, `nav ul`, `.main-nav`, etc. rules that earlier cleanup tasks missed).
- Rules carried over in a page's `additional-styles` region (if any DWT page authored its own conflicting nav CSS).

The utility lives at `_pilot/nav_css_cleanup.py`. Import and call:

```python
import sys; sys.path.insert(0, '_pilot')
from nav_css_cleanup import clean_nav_css_from_inline_style, check_mobile_nav_not_hidden

migrated_html = render(template, regions)
migrated_html = clean_nav_css_from_inline_style(migrated_html)
```

### What it removes (selector patterns, OUTSIDE `@media print`)

- `header.site-header` (any compound — `.site-header`, `header.site-header:hover`, etc.)
- `footer.site-footer` (any compound)
- `nav`, `nav ul`, `nav ul.show`, `nav li`, `nav a` (bare-element nav selectors)
- `.main-nav` (any compound)
- `.menu-toggle` (any compound)
- `.has-dropdown` (any compound)
- `.dropdown`, `.dropdown-toggle` (any compound)
- `.site-banner` (the new template owns this)

### What it preserves

- Reset rules (`* { … }`)
- `main.content-wrapper`, page-content classes
- `.footer-container`, `.footer-content`, `.footer-section ul`, `.footer-bottom`
- Any selector not matching the patterns above
- The entire `@media print { … }` block (kept verbatim — those rules legitimately hide chrome for printing)
- Whitespace and comments around kept rules

### Behavior

- Recursive: traverses nested `@media` blocks (e.g., `@media (max-width: 768px) { @media (max-height: 500px) and (orientation: landscape) { … } }`).
- Empty `@media` blocks after inner filtering are dropped.
- Brace-balanced parser — correctly handles comments in selectors, nested at-rules, arbitrary whitespace.

---

## 5b. `rendered-from` Provenance Marker (REQUIRED)

After the CSS cleanup, the migration script prepends a single HTML comment immediately after the `<!DOCTYPE html>` line:

```html
<!DOCTYPE html>
<!-- rendered-from: _templates/Academic-Content-EN.html @ 2026-05-13T10:30:00Z -->
<html lang="en">
```

The marker records:

- **Which template the page was rendered from** (relative repo path, e.g., `_templates/Academic-Content-EN.html` or `_templates/Academic-Content-HE.html`)
- **When the render happened** (ISO 8601 UTC timestamp)

This marker becomes the source of truth for "which template owns this page" — replacing the implicit path/extension/lang inference once the migration is complete. Re-render tasks find re-renderable pages by `grep`'ing for this comment:

```bash
grep -rl "rendered-from: _templates/" --include="*.htm" --include="*.html" .
```

### Insertion logic

```python
from datetime import datetime, timezone

def insert_provenance_marker(html, template_path):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    marker = f'\n<!-- rendered-from: {template_path} @ {ts} -->'
    # Insert immediately after <!DOCTYPE html> (any whitespace/CR after it is preserved)
    return re.sub(r'(?i)(<!DOCTYPE html>)', r'\1' + marker, html, count=1)
```

The insertion uses a case-insensitive single-replace to be robust against different DOCTYPE casings and trailing-whitespace variations.

### Idempotency

If a `<!-- rendered-from: ... -->` comment is already present, the script should **replace** it with a fresh marker rather than appending a second one. Implementation:

```python
def insert_or_update_provenance(html, template_path):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    marker = f'<!-- rendered-from: {template_path} @ {ts} -->'
    # If existing marker present, replace it
    if re.search(r'<!--\s*rendered-from:[^>]*-->', html):
        return re.sub(r'<!--\s*rendered-from:[^>]*-->', marker, html, count=1)
    # Otherwise insert after DOCTYPE
    return re.sub(r'(?i)(<!DOCTYPE html>)', r'\1\n' + marker, html, count=1)
```

This way a re-render produces a single, fresh marker — no marker pile-up.

---

## 6. Verification Checks (per file, after cleanup)

### Baseline checks from the 4-page pilot

| # | Check | Method |
|---|---|---|
| 1 | New nav markup present | `class="nav-toggle"` count = 1; `<button type="button">` count = 2 (EN) or 3 (HE) |
| 2 | Old DWT markers removed | No `#BeginTemplate`, `#BeginEditable`, `#EndEditable`, `#EndTemplate` |
| 3 | Old nav markup removed | No `class="menu-toggle"` button; no `onclick="toggleMenu()"` |
| 4 | Correct lang attribute | EN: `<html lang="en">`; HE: `<html lang="he" dir="rtl">` |
| 5 | Content preserved | Word count of original `content` (or `start`) region ≈ migrated `<main>` content (±1%) |
| 6 | Title preserved | Migrated `<title>` matches original |
| 7 | Meta region preserved | Original `<meta>`, `rel="canonical"`, OG, schema.org tags all present in migrated `<head>` |
| 8 | No broken references | Set of `href` and `src` values from original content content matches migrated |

### NEW check 9: Mobile nav not hidden by inline CSS

```python
findings = check_mobile_nav_not_hidden(migrated_html)
if findings:
    skip_this_file()  # flag for manual review
```

Returns a list of selectors that — inside a `@media (max-width: ≤768px)` block — set `display: none` on a selector that would match the new top-level nav (`.nav-menu`, `nav ul`, `header.site-header`, `header > nav`). Empty list = pass. Non-empty = fail; that file needs manual review.

In the pilot, Woven-Torah-Method had 2 such findings before cleanup and 0 after. The pattern was `nav ul { display: none }` inside `@media (max-width: 768px)` — a leftover from the old hamburger system.

### NEW check 13: `rendered-from` provenance marker present

```python
def has_provenance_marker(html, template_path):
    pat = re.compile(
        r'<!--\s*rendered-from:\s*' + re.escape(template_path) +
        r'\s*@\s*\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\s*-->'
    )
    return len(pat.findall(html)) == 1
```

Exactly one `<!-- rendered-from: <template_path> @ <ISO 8601 timestamp> -->` comment must be present in the migrated file, immediately after `<!DOCTYPE html>`. Zero markers or multiple markers ⇒ fail.

---

## 7. Backup Discipline

Before overwriting any source file, copy it to `_backup-pre-migration/<same/relative/path>`. This is the rollback path:

```bash
mkdir -p _backup-pre-migration/$(dirname "$rel")
cp "$rel" "_backup-pre-migration/$rel"
```

Verify backup byte-identical (`stat -c %s` on both files) before proceeding.

If any file's verification check fails, **do not overwrite the original** — leave it untouched. The backup is only needed for files that were already migrated and need to be rolled back.

---

## 8. Standalone-Page Handling (for the rare cases beyond `hebrew index.html`)

If the bulk migration encounters a standalone HTML file (no DWT marker) that isn't `hebrew index.html`, **flag it for manual review rather than auto-migrating**. The standalone-extraction logic (head-content filtering, `</header>`-to-`<footer>` content extraction) is heuristic and worked for the home page because its structure was predictable, but other standalone pages may have unusual layouts.

For the pilot's hebrew home, the manual review confirmed:

- 3 schema.org JSON-LD blocks (FAQPage, Book, WebSite) preserved in `meta` region.
- Google Fonts `<link>` preserved.
- Old `<header>` / `<footer>` in body discarded (new template provides both).
- Old `toggleMenu()` script at end of body discarded.
- Custom inline `<style>` (~11.6 KB of page-specific design) preserved — the cleanup pass strips only the nav-targeting bits.

---

## 9. Reporting

For each batch run, output a report `_pilot/bulk-migration-batch-<date>.md` with:

- Total files attempted
- Total files migrated successfully
- Total files skipped (with reason)
- Per-language counts (EN / HE)
- Per-DWT counts (`Academic-Content-DWT` / `hebrew.dwt` / standalone)
- List of files where `lang` was corrected (path/DWT signaled HE but source had `lang="en"`)
- List of files that failed `check_mobile_nav_not_hidden()` (manual review needed)
- Backup directory size + file count

---

## 10. Order of Operations Recap

For each source file:

1. **Detect** language (Section 2) and DWT type (Section 3).
2. **Back up** to `_backup-pre-migration/<rel>`. Verify byte-identical.
3. **Extract** regions per DWT type (Section 3).
4. **Render** by substituting regions into the appropriate template (Section 4).
5. **Clean** orphan nav CSS via `clean_nav_css_from_inline_style()` (Section 5).
6. **Verify** all 9 checks (Section 6).
7. If all checks pass → **save** in place (overwrites the original).
8. If any check fails → **leave original alone**, log to skip list with reason.

---

## 11. Known Open Items Before Scaling

- **Template orphan CSS.** Both `_templates/Academic-Content-EN.html` and `Academic-Content-HE.html` still contain orphan nav CSS in their inline `<style>` blocks. Running `clean_nav_css_from_inline_style()` on the **templates** themselves before the bulk run would mean each migrated page no longer inherits orphan rules from the template; the per-page cleanup pass becomes a defensive double-check rather than load-bearing.
- **`Academic-Content-DWT.dwt` and `hebrew.dwt` files** in `Dynamic Web Templates/` — not migrated by this task. They're stale and can be removed once all DWT-attached pages are migrated and the migration is verified.
- **Stale `.menu-toggle` / `.main-nav` rules in `main.css`** — previously removed in an earlier task; verified gone.
- **`/mishnah/` 404** — separate content task; the new nav has a placeholder link that resolves once the portal page is built.

---

## 12. Reference Implementation Snippet

```python
# bulk_migrate.py — outline
from pathlib import Path
import sys, re
sys.path.insert(0, str(Path(__file__).parent))
from nav_css_cleanup import (
    clean_nav_css_from_inline_style, check_mobile_nav_not_hidden,
)

REPO = Path('.')
BACKUP = REPO / '_backup-pre-migration'
TPL_EN = (REPO / '_templates' / 'Academic-Content-EN.html').read_text(encoding='utf-8')
TPL_HE = (REPO / '_templates' / 'Academic-Content-HE.html').read_text(encoding='utf-8')

RE_EDITABLE = re.compile(
    r'<!--\s*#BeginEditable\s+"([^"]+)"\s*-->(.*?)<!--\s*#EndEditable\s*-->',
    re.DOTALL
)

def detect_lang(path: Path, source: str) -> str:
    if '/Hebrew/' in str(path):           return 'HE'
    if 'hebrew' in str(path).lower():      return 'HE'
    if 'hebrew.dwt' in source.lower():     return 'HE'
    if re.search(r'<html\s[^>]*lang="he"', source): return 'HE'
    return 'EN'

def detect_dwt(source: str) -> str:
    m = re.search(r'#BeginTemplate\s+"[^"]*?/([^/"]+)\.dwt"', source)
    return m.group(1) + '.dwt' if m else 'standalone'

def migrate_one(path: Path) -> dict:
    source = path.read_text(encoding='utf-8', errors='replace')
    lang = detect_lang(path, source)
    dwt = detect_dwt(source)
    template = TPL_HE if lang == 'HE' else TPL_EN
    
    if dwt == 'Academic-Content-DWT.dwt':
        regions = {m.group(1): m.group(2) for m in RE_EDITABLE.finditer(source)}
    elif dwt == 'hebrew.dwt':
        raw = {m.group(1): m.group(2) for m in RE_EDITABLE.finditer(source)}
        regions = {
            'doctitle': raw.get('doctitle', ''),
            'meta': '',  # no meta region in hebrew.dwt
            'additional-styles': raw.get('additional-styles', ''),
            'content': raw.get('start', ''),       # rename
            'page-scripts': raw.get('page-scripts', ''),
        }
    else:
        # standalone — flag for manual review
        return {'status': 'skip', 'reason': 'standalone — manual review required'}
    
    rendered = template
    for k, v in regions.items():
        rendered = rendered.replace('{{ region: ' + k + ' }}', v)
    
    cleaned = clean_nav_css_from_inline_style(rendered)
    
    findings = check_mobile_nav_not_hidden(cleaned)
    if findings:
        return {'status': 'skip', 'reason': f'mobile nav hidden: {findings}'}
    
    # Backup + save
    backup_path = BACKUP / path.relative_to(REPO)
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    backup_path.write_bytes(path.read_bytes())  # byte-exact
    path.write_text(cleaned, encoding='utf-8')
    return {'status': 'ok', 'lang': lang, 'dwt': dwt}
```

---

## Files Referenced

| Path | Role |
|---|---|
| `_templates/Academic-Content-EN.html` | English target template |
| `_templates/Academic-Content-HE.html` | Hebrew target template |
| `_pilot/nav_css_cleanup.py` | CSS cleanup utility + verification check |
| `_pilot/migration-test-4pages.md` | Pilot results (4 representative pages, all 8 baseline checks passed) |
| `_pilot/woven-torah-method-fix.md` | Mid-pilot finding + fix that motivated check #9 |
| `_pilot/migration-logic.md` | This document |
| `_backup-pre-migration/` | Rollback path — 1:1 backup before migration |
