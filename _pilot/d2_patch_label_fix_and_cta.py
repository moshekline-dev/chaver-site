#!/usr/bin/env python3
"""D-2 patch: label-fix + PDF CTA.

Two changes across the 525 rendered Mishnah chapters:
  1. Fix two render bugs in 6 specific chapters
     - Bug 1 (normalize_label): only convert standalone Hebrew column letters
       (digit + optional space + א-ה at end). Don't strip internal spaces.
     - Bug 2 (extract_label_and_body):
         a. If first run is a single Latin subdivision marker (A-E), use it
            as the label.
         b. For single-cell rows where no run contains a newline, treat the
            cell as content with no label.
  2. Inject a PDF download CTA into <article class="mishnah-chapter"> on
     every chapter page (idempotent).

Re-renders only the 6 chapters listed in PATCH_RENDER_KEYS. The other 519
get only the CTA injection + sentinel update (their existing <main> content
is preserved verbatim).

Sentinel: <!-- D-2 patch: label-fix-plus-cta @ {ISO_TIMESTAMP} -->
"""
import json
import os
import re
import sys
import tempfile
import time
import urllib.parse
from html import escape

REPO_ROOT = '/sessions/youthful-busy-hamilton/mnt/chaver-site'
JSON_PATH = os.path.join(REPO_ROOT, 'Mishnah-New/English/mishnah_db.json')

ISO_TIMESTAMP = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
SENTINEL_NEW = f'<!-- D-2 patch: label-fix-plus-cta @ {ISO_TIMESTAMP} -->'

URL_PREFIX = 'https://chaver.com/'

HE_TO_LATIN = {'א': 'A', 'ב': 'B', 'ג': 'C', 'ד': 'D', 'ה': 'E'}
SUBDIVISION_LETTERS = {'A', 'B', 'C', 'D', 'E'}

CHAPTER_SUFFIX = {'sotah_9a': ' (חלק א)', 'sotah_9b': ' (חלק ב)'}

PATCH_RENDER_KEYS = {
    'bavametzia_2',  # Bug 2: row 0 single-cell full mishnah as <th>
    'avot_2',        # Bug 2: row 4 single-cell full mishnah as <th>
    'gittin_3',      # Bug 1: שנה → שנE
    'ketubot_2',     # Bug 1: אשה → אשE; spaces collapsed in 'עדות עצמית'
    'chagigah_2',    # Bug 1: במרכבה → במרכבE; spaces collapsed
    'eduyot_7',      # Bug 2: rows 1-4 subdivision-marker B/C/D/E swallowed content
}

CTA_HTML = (
    '        <!-- PDF CTA — added by D-2 patch -->\n'
    '        <div class="citation-box">\n'
    '            <p><strong>📖 המשנה כדרכה — PDF</strong></p>\n'
    '            <p>\n'
    '                <a href="/Mishnah-New/Hebrew/Text/The%20Structured%20Mishnah.pdf">\n'
    '                    להורדת המשנה כדרכה (PDF)\n'
    '                </a>\n'
    '            </p>\n'
    '        </div>\n'
)
CTA_SENTINEL_COMMENT = '<!-- PDF CTA — added by D-2 patch -->'


# ===== FIXED label/body extraction =====

DIGIT_HE_RE = re.compile(r'^(\d+)\s*([אבגדה])$')


def normalize_label(raw):
    """FIXED: only convert standalone Hebrew column letters after a digit.

    Preserves internal spaces (e.g. 'עדות עצמית', 'במעשה בראשית' stay intact).
    Bare Hebrew words (e.g. 'שנה', 'אשה', 'במרכבה') stay unchanged.
    Digit+Hebrew-letter patterns ('1א', '2 ב', '10ה') convert to digit+Latin.
    """
    if not raw:
        return ''
    s = raw.strip()
    if not s:
        return ''
    m = DIGIT_HE_RE.match(s)
    if m:
        return m.group(1) + HE_TO_LATIN[m.group(2)]
    return s


def extract_label_and_body(cell, n_cells_in_row):
    """FIXED: handle subdivision-marker-first cells and single-cell content rows.

    Case 1: First run is a single Latin subdivision marker (A-E) → use it as label.
    Case 2: Single-cell row with no \n in any run → treat entire cell as content
            (label from cell.label field, body = all runs).
    Case 3: Otherwise, existing accumulate-until-\n logic.
    """
    runs = cell.get('runs', [])
    json_label = (cell.get('label') or '').strip()

    if not runs:
        text = cell.get('text', '') or ''
        lines = text.split('\n', 1)
        label_raw = json_label or (lines[0].strip() if lines else '')
        body_runs = []
        if len(lines) > 1 and lines[1]:
            body_runs.append({'text': lines[1], 'marker': None})
        return label_raw, body_runs

    # Case 1: First run is a single subdivision marker (A-E)
    if (runs[0].get('marker') is None and
            runs[0].get('text', '').strip() in SUBDIVISION_LETTERS):
        label = runs[0]['text'].strip()
        body_start = 1
        # Skip leading whitespace-only runs after the marker
        while (body_start < len(runs) and
               runs[body_start].get('marker') is None and
               runs[body_start].get('text', '').strip() == ''):
            body_start += 1
        return label, runs[body_start:]

    # Case 2: Single-cell row, no \n anywhere → content, no label
    if n_cells_in_row == 1:
        has_newline = any('\n' in r.get('text', '') for r in runs)
        if not has_newline:
            return json_label, list(runs)

    # Case 3: Standard accumulation until \n (existing behavior)
    label_parts = []
    body_runs = []
    consumed = False
    for run in runs:
        if consumed:
            body_runs.append(run)
            continue
        rt = run.get('text', '')
        marker = run.get('marker')
        if '\n' in rt and marker is None:
            nl_pos = rt.index('\n')
            before = rt[:nl_pos]
            after = rt[nl_pos + 1:]
            if before:
                label_parts.append(before)
            if after:
                body_runs.append({'text': after, 'marker': None})
            consumed = True
        elif '\n' in rt and marker is not None:
            body_runs.append(run)
            consumed = True
        else:
            label_parts.append(rt)
    return ''.join(label_parts).strip(), body_runs


def is_subdivision_marker_run(run):
    return (run.get('marker') is None and
            run.get('text', '').strip() in SUBDIVISION_LETTERS)


def split_into_subdivisions(body_runs):
    marker_positions = [(i, r['text'].strip())
                        for i, r in enumerate(body_runs)
                        if is_subdivision_marker_run(r)]
    if not marker_positions:
        return [(None, body_runs)]
    segments = []
    first_idx = marker_positions[0][0]
    if first_idx > 0:
        preamble = body_runs[:first_idx]
        if any(r.get('text', '').strip() for r in preamble):
            segments.append((None, preamble))
    for j, (mi, letter) in enumerate(marker_positions):
        end = marker_positions[j + 1][0] if j + 1 < len(marker_positions) else len(body_runs)
        start = mi + 1
        while (start < end and
               body_runs[start].get('marker') is None and
               body_runs[start].get('text', '').strip() == ''):
            start += 1
        segments.append((letter, body_runs[start:end]))
    return segments


def render_runs_html(runs):
    parts = []
    for run in runs:
        rt = run.get('text', '')
        marker = run.get('marker')
        if marker:
            parts.append(f'<span class="{escape(marker)}"><b>{escape(rt)}</b></span>')
        else:
            parts.append(escape(rt).replace('\n', '<br>'))
    out = ''.join(parts)
    out = re.sub(r'^(<br>)+', '', out)
    out = re.sub(r'(<br>)+$', '', out)
    return out


def color_class(n_cells, idx):
    if n_cells == 1:
        return 'col-full'
    if n_cells == 2:
        return ['col-a', 'col-c'][idx]
    if idx == 0:
        return 'col-a'
    if idx == n_cells - 1:
        return 'col-c'
    return 'col-b'


def render_row_table(row):
    cells = row.get('cells', [])
    n_cells = len(cells)
    if n_cells == 0:
        return ''

    cell_data = []
    for cell in cells:
        label_raw, body_runs = extract_label_and_body(cell, n_cells)
        label = normalize_label(label_raw)
        segments = split_into_subdivisions(body_runs)
        colspan = (cell.get('position', {}) or {}).get('colspan', 1) or 1

        subdivs_with_letter = [(letter.lower(), render_runs_html(runs))
                               for letter, runs in segments if letter is not None]
        preambles = [render_runs_html(runs) for letter, runs in segments if letter is None]

        if not subdivs_with_letter:
            html = render_runs_html(body_runs)
            cell_data.append({'label': label, 'colspan': colspan,
                              'subdivisions': [], 'single_html': html})
        else:
            preamble_html = ''.join(preambles).strip()
            if preamble_html:
                first_letter, first_html = subdivs_with_letter[0]
                joined = (preamble_html + '<br>' + first_html) if first_html else preamble_html
                subdivs_with_letter[0] = (first_letter, joined)
            cell_data.append({'label': label, 'colspan': colspan,
                              'subdivisions': subdivs_with_letter, 'single_html': ''})

    max_subdivs = max((len(d['subdivisions']) for d in cell_data), default=0)

    lines = ['<table class="scripture-table">']

    thead_cells = []
    for i, d in enumerate(cell_data):
        cls = color_class(n_cells, i)
        cs = f' colspan="{d["colspan"]}"' if d['colspan'] > 1 else ''
        thead_cells.append(f'<th class="{cls}"{cs}>{escape(d["label"])}</th>')
    lines.append('    <thead>')
    lines.append('        <tr>' + ''.join(thead_cells) + '</tr>')
    lines.append('    </thead>')

    lines.append('    <tbody>')
    if max_subdivs == 0:
        tds = []
        for d in cell_data:
            cs = f' colspan="{d["colspan"]}"' if d['colspan'] > 1 else ''
            tds.append(f'<td{cs}><p class="torah">{d["single_html"]}</p></td>')
        lines.append('        <tr>' + ''.join(tds) + '</tr>')
    else:
        for r_idx in range(max_subdivs):
            tds = []
            for d in cell_data:
                n = len(d['subdivisions'])
                cs = f' colspan="{d["colspan"]}"' if d['colspan'] > 1 else ''
                if n == 0:
                    if r_idx == 0:
                        rs = f' rowspan="{max_subdivs}"' if max_subdivs > 1 else ''
                        tds.append(f'<td{cs}{rs}><p class="torah">{d["single_html"]}</p></td>')
                elif n == max_subdivs:
                    letter, content = d['subdivisions'][r_idx]
                    tds.append(
                        f'<td{cs}><p class="torah"><span class="CellSubdivision"><b>{letter}</b></span> {content}</p></td>'
                    )
                else:
                    if r_idx < n - 1:
                        letter, content = d['subdivisions'][r_idx]
                        tds.append(
                            f'<td{cs}><p class="torah"><span class="CellSubdivision"><b>{letter}</b></span> {content}</p></td>'
                        )
                    elif r_idx == n - 1:
                        letter, content = d['subdivisions'][r_idx]
                        span = max_subdivs - n + 1
                        rs = f' rowspan="{span}"' if span > 1 else ''
                        tds.append(
                            f'<td{cs}{rs}><p class="torah"><span class="CellSubdivision"><b>{letter}</b></span> {content}</p></td>'
                        )
            lines.append('        <tr>' + ''.join(tds) + '</tr>')
    lines.append('    </tbody>')
    lines.append('</table>')
    return '\n'.join(lines)


def render_chapter_main_content(key, ch):
    tractate_he = ch.get('tractate_he', '')
    chapter_he = ch.get('chapter_he', '')
    suffix = CHAPTER_SUFFIX.get(key, '')
    h1_text = f'{tractate_he} פרק {chapter_he}{suffix} – המבנה הספרותי'

    parts = ['        <article class="mishnah-chapter">',
             f'        <h1>{escape(h1_text)}</h1>']
    for row in ch.get('rows', []):
        table_html = render_row_table(row)
        indented = '\n'.join('        ' + line if line else line
                             for line in table_html.split('\n'))
        parts.append(indented)
    parts.append('        </article>')
    return '\n'.join(parts)


# ===== Path mapping =====
def derive_disk_path(source_url):
    if not source_url.startswith(URL_PREFIX):
        raise ValueError(f'URL prefix mismatch: {source_url!r}')
    path_part = source_url[len(URL_PREFIX):]
    decoded = urllib.parse.unquote(path_part)
    if not decoded.endswith('.htm'):
        decoded += '.htm'
    return decoded


# ===== Transforms =====
MAIN_RE = re.compile(r'(<main class="content-wrapper">)(.*?)(</main>)', re.DOTALL)
# Match any prior D-2 sentinel form (bulk or patch)
D2_SENTINEL_RE = re.compile(r'<!--\s*D-2[^>]*-->')
# Find </article> inside <article class="mishnah-chapter">...</article>
ARTICLE_RE = re.compile(
    r'(<article class="mishnah-chapter">.*?)(\n\s*</article>)',
    re.DOTALL,
)


def replace_main(file_text, new_main_inner):
    """Substitute <main> inner content (used only for re-render targets)."""
    def repl(m):
        return f'{m.group(1)}\n{new_main_inner}\n    {m.group(3)}'
    new_text, n = MAIN_RE.subn(repl, file_text, count=1)
    if n != 1:
        raise RuntimeError(f'Expected 1 <main> match, got {n}')
    return new_text


def inject_cta(file_text):
    """Insert PDF CTA inside <article class='mishnah-chapter'> before </article>.

    Idempotent: skip if CTA_SENTINEL_COMMENT already present.
    """
    if CTA_SENTINEL_COMMENT in file_text:
        return file_text, False
    def repl(m):
        return f'{m.group(1)}\n{CTA_HTML.rstrip()}{m.group(2)}'
    new_text, n = ARTICLE_RE.subn(repl, file_text, count=1)
    if n != 1:
        raise RuntimeError(f'Could not find <article class="mishnah-chapter">...</article> wrapper')
    return new_text, True


def update_sentinel(file_text):
    """Replace any existing D-2 sentinel with SENTINEL_NEW."""
    new_text, n = D2_SENTINEL_RE.subn(SENTINEL_NEW, file_text, count=1)
    if n != 1:
        raise RuntimeError(f'Expected 1 D-2 sentinel match, got {n}')
    return new_text


# ===== Verify =====
JSON_LD_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.DOTALL)


def verify(file_path, expect_cta=True):
    errors = []
    with open(file_path, 'rb') as f:
        data = f.read()
    size = len(data)
    if size < 5000:
        errors.append(f'too small ({size}B)')
    if not data.rstrip().endswith(b'</html>'):
        errors.append('no </html>')
    text = data.decode('utf-8')
    for blk in JSON_LD_RE.findall(text):
        try:
            json.loads(blk)
        except Exception as e:
            errors.append(f'JSON-LD: {e}')
            break
    if text.count(SENTINEL_NEW) != 1:
        errors.append(f'sentinel_count={text.count(SENTINEL_NEW)}')
    if expect_cta:
        if 'The%20Structured%20Mishnah.pdf' not in text:
            errors.append('CTA missing')
        if text.count(CTA_SENTINEL_COMMENT) != 1:
            errors.append(f'cta_sentinel_count={text.count(CTA_SENTINEL_COMMENT)}')
    return size, errors


def atomic_write(file_path, content):
    data = content.encode('utf-8')
    dir_ = os.path.dirname(file_path)
    fd, tmp = tempfile.mkstemp(prefix='.d2patch-', dir=dir_)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, file_path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise
    return len(data)


def main():
    print(f'Loading JSON: {JSON_PATH}')
    with open(JSON_PATH, encoding='utf-8') as f:
        db = json.load(f)
    chapter_keys = [k for k in db if not k.startswith('_')]
    print(f'Chapters to process: {len(chapter_keys)}')
    print(f'Re-render targets: {sorted(PATCH_RENDER_KEYS)}')

    # Pre-flight
    missing = []
    for k in chapter_keys:
        try:
            rel = derive_disk_path(db[k]['source_url'])
            full = os.path.join(REPO_ROOT, rel)
            if not os.path.exists(full):
                missing.append((k, rel))
        except Exception as e:
            missing.append((k, str(e)))
    if missing:
        print(f'PRE-FLIGHT FAILED: {len(missing)} chapters cannot be mapped')
        for k, info in missing[:10]:
            print(f'  {k}: {info}')
        return 1
    print(f'Pre-flight pass: all {len(chapter_keys)} chapters map to disk files.')

    # Verify all keys in PATCH_RENDER_KEYS exist in JSON
    for k in PATCH_RENDER_KEYS:
        if k not in db:
            print(f'ERROR: re-render key {k!r} not in JSON')
            return 1

    rendered = []
    cta_added = []
    cta_skipped = []
    failed = []

    for i, key in enumerate(chapter_keys, 1):
        ch = db[key]
        try:
            rel = derive_disk_path(ch['source_url'])
            full = os.path.join(REPO_ROOT, rel)
            with open(full, encoding='utf-8') as f:
                old_text = f.read()
            old_size = len(old_text.encode('utf-8'))

            new_text = old_text

            # Re-render <main> ONLY for the 6 target chapters
            if key in PATCH_RENDER_KEYS:
                inner = render_chapter_main_content(key, ch)
                new_text = replace_main(new_text, inner)

            # Inject CTA (idempotent)
            new_text, cta_was_added = inject_cta(new_text)

            # Update sentinel
            new_text = update_sentinel(new_text)

            new_size = atomic_write(full, new_text)
            actual_size, errs = verify(full, expect_cta=True)
            if errs:
                failed.append((key, rel, '; '.join(errs)))

            entry = {'key': key, 'path': rel,
                     'old': old_size, 'new': actual_size,
                     'rendered': key in PATCH_RENDER_KEYS,
                     'cta_added': cta_was_added,
                     'errs': errs}
            rendered.append(entry)
            if cta_was_added:
                cta_added.append(key)
            else:
                cta_skipped.append(key)
        except Exception as e:
            failed.append((key, ch.get('source_url', ''),
                           f'EXCEPTION: {type(e).__name__}: {e}'))
        if i % 50 == 0:
            print(f'  processed {i}/{len(chapter_keys)}...')

    # Summary
    print(f'\n=== D-2 Patch Report ===')
    print(f'Timestamp: {ISO_TIMESTAMP}')
    print(f'Processed: {len(rendered)} / {len(chapter_keys)}')
    n_rendered = sum(1 for r in rendered if r['rendered'])
    print(f'Re-rendered (full <main>): {n_rendered}')
    print(f'CTA injected: {len(cta_added)}')
    print(f'CTA skipped (already present): {len(cta_skipped)}')
    print(f'Failed: {len(failed)}')
    if failed:
        print('\nFailures:')
        for k, p, msg in failed[:30]:
            print(f'  {k} [{p}]: {msg}')

    n_with_errs = sum(1 for r in rendered if r['errs'])
    print(f'\nFiles with verify errors: {n_with_errs}')
    if n_with_errs:
        for r in rendered[:30]:
            if r['errs']:
                print(f'  {r["key"]}: {r["errs"]}')

    total_delta = sum(r['new'] - r['old'] for r in rendered)
    print(f'Net byte delta: {total_delta:+,}')

    return 0 if not failed and n_with_errs == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
