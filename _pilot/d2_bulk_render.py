#!/usr/bin/env python3
"""D-2 bulk render — all 525 Mishnah chapters using the D-1 v5-alt proven pattern.

Extends d1_v5alt_render.py with two changes:
  1. Restores `<article class="mishnah-chapter">` on the wrapper (safe now that <th>
     elements no longer carry `cell-label` — the .mishnah-chapter .cell-label rule
     has nothing to match). This activates the new CSS rules at main.css ~line 778:
       .mishnah-chapter .scripture-table { margin: 0; }
       .mishnah-chapter .scripture-table td p.torah:last-child { margin-bottom: 0; }
       .mishnah-chapter .scripture-table td p.torah { text-align: center; }
  2. Iterates ALL 525 chapter keys (excluding `_meta`), using `source_url` from each
     chapter record to derive the disk path (avoids brittle name-normalization).

Strategy: surgical in-place replacement of <main> inner content + sentinel + provenance.
Defensive verification per file. Continues on per-file errors (logs and proceeds).

Sentinel: `<!-- D-2 bulk: mishnah-render @ {ISO_TIMESTAMP} -->`
"""
import json
import os
import re
import sys
import tempfile
import time
import urllib.parse
from html import escape

REPO_ROOT = '/sessions/sharp-eloquent-mccarthy/mnt/chaver-site'
JSON_PATH = os.path.join(REPO_ROOT, 'Mishnah-New/English/mishnah_db.json')

ISO_TIMESTAMP = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
SENTINEL_NEW = f'<!-- D-2 bulk: mishnah-render @ {ISO_TIMESTAMP} -->'
PROVENANCE_NEW = f'<!-- rendered-from: _templates/Academic-Content-HE.html @ {ISO_TIMESTAMP} -->'

URL_PREFIX = 'https://chaver.com/'

HE_TO_LATIN = {'א': 'A', 'ב': 'B', 'ג': 'C', 'ד': 'D', 'ה': 'E'}
SUBDIVISION_LETTERS = {'A', 'B', 'C', 'D', 'E'}

CHAPTER_SUFFIX = {'sotah_9a': ' (חלק א)', 'sotah_9b': ' (חלק ב)'}


# ===== Helpers (identical to v5alt) =====
def normalize_label(raw):
    if not raw:
        return ''
    s = raw.strip().replace(' ', '')
    if not s:
        return ''
    last = s[-1]
    if last in HE_TO_LATIN:
        return s[:-1] + HE_TO_LATIN[last]
    return s


def extract_label_and_body(cell):
    runs = cell.get('runs', [])
    if not runs:
        text = cell.get('text', '') or ''
        lines = text.split('\n', 1)
        label_raw = lines[0].strip() if lines else ''
        body_runs = []
        if len(lines) > 1 and lines[1]:
            body_runs.append({'text': lines[1], 'marker': None})
        return label_raw, body_runs

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
    """v5-alt convention: col-a / col-b / col-c / col-full."""
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
        label_raw, body_runs = extract_label_and_body(cell)
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

    # KEY CHANGE FROM v5alt: restore mishnah-chapter class on <article>
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
    """source_url → relative disk path under REPO_ROOT."""
    if not source_url.startswith(URL_PREFIX):
        raise ValueError(f'URL prefix mismatch: {source_url!r}')
    path_part = source_url[len(URL_PREFIX):]
    decoded = urllib.parse.unquote(path_part)
    if not decoded.endswith('.htm'):
        decoded += '.htm'
    return decoded


# ===== In-place transform =====
MAIN_RE = re.compile(r'(<main class="content-wrapper">)(.*?)(</main>)', re.DOTALL)
SENTINEL_ANY_RE = re.compile(r'<!--\s*D-[12](?:\s+bulk)?\s+pilot[^>]*-->|<!--\s*D-[12][^>]*-->')
PROVENANCE_RE = re.compile(r'<!-- rendered-from: _templates/Academic-Content-HE\.html @ [^>]+-->')


def transform_file(file_text, new_main_inner):
    def main_repl(m):
        return f'{m.group(1)}\n{new_main_inner}\n    {m.group(3)}'
    new_text, n_main = MAIN_RE.subn(main_repl, file_text, count=1)
    if n_main != 1:
        raise RuntimeError(f'Expected 1 <main> match, got {n_main}')

    new_text, n_sent = SENTINEL_ANY_RE.subn(SENTINEL_NEW, new_text, count=1)
    if n_sent != 1:
        # Some files may not have any D-1 sentinel yet (never went through pilot).
        # In that case, prepend the sentinel inside <head> after the opening tag.
        if '<head>' in new_text and SENTINEL_NEW not in new_text:
            new_text = new_text.replace('<head>', f'<head>\n    {SENTINEL_NEW}', 1)
            n_sent = 1
        else:
            raise RuntimeError(f'Could not place sentinel; existing sentinels: {n_sent}')

    new_text, n_prov = PROVENANCE_RE.subn(PROVENANCE_NEW, new_text, count=1)
    if n_prov != 1:
        # Some files may not have a provenance marker; inject after <!DOCTYPE html>
        if '<!DOCTYPE html>' in new_text and PROVENANCE_NEW not in new_text:
            new_text = new_text.replace('<!DOCTYPE html>',
                                        f'<!DOCTYPE html>\n{PROVENANCE_NEW}', 1)
            n_prov = 1
        else:
            raise RuntimeError(f'Could not place provenance; existing: {n_prov}')

    return new_text


JSON_LD_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.DOTALL)


def verify(file_path):
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

    main_match = re.search(r'<main class="content-wrapper">(.*?)</main>', text, re.DOTALL)
    main_inner = main_match.group(1) if main_match else ''

    if re.search(r'<th[^>]*\bcell-label\b', main_inner):
        errors.append('cell-label in <th>')
    if re.search(r'<[a-z][^>]*\bdir="rtl"', main_inner):
        errors.append('dir="rtl" in <main>')
    body_match = re.search(r'<body[^>]*>(.*?)</body>', text, re.DOTALL)
    if body_match:
        body_inner = body_match.group(1)
        # `dir="rtl"` is allowed on <html>, not inside body
        body_rtl = re.findall(r'<[a-z][^>]*\bdir="rtl"', body_inner)
        if body_rtl:
            errors.append(f'dir="rtl" in body ({len(body_rtl)})')

    if '<article class="mishnah-chapter">' not in main_inner:
        errors.append('article.mishnah-chapter missing')
    return size, errors


def atomic_write(file_path, content):
    data = content.encode('utf-8')
    dir_ = os.path.dirname(file_path)
    fd, tmp = tempfile.mkstemp(prefix='.d2-', dir=dir_)
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
    print(f'Chapters to render: {len(chapter_keys)}')

    # Pre-flight: validate every key maps to an existing disk file
    missing_files = []
    for k in chapter_keys:
        url = db[k].get('source_url', '')
        try:
            rel = derive_disk_path(url)
            full = os.path.join(REPO_ROOT, rel)
            if not os.path.exists(full):
                missing_files.append((k, rel))
        except Exception as e:
            missing_files.append((k, str(e)))
    if missing_files:
        print(f'PRE-FLIGHT FAILED: {len(missing_files)} chapters cannot be mapped to disk files')
        for k, info in missing_files[:10]:
            print(f'  {k}: {info}')
        return 1
    print(f'Pre-flight pass: all {len(chapter_keys)} chapters map to existing disk files.')

    rendered = []
    failed = []

    for i, key in enumerate(chapter_keys, 1):
        ch = db[key]
        try:
            rel = derive_disk_path(ch['source_url'])
            full = os.path.join(REPO_ROOT, rel)
            with open(full, encoding='utf-8') as f:
                old_text = f.read()
            old_size = len(old_text.encode('utf-8'))
            inner = render_chapter_main_content(key, ch)
            new_text = transform_file(old_text, inner)
            new_size = atomic_write(full, new_text)
            actual_size, errs = verify(full)
            if errs:
                failed.append((key, rel, '; '.join(errs)))
            rendered.append({'key': key, 'path': rel,
                             'old': old_size, 'new': actual_size, 'errs': errs})
        except Exception as e:
            failed.append((key, ch.get('source_url', ''),
                           f'EXCEPTION: {type(e).__name__}: {e}'))
        if i % 50 == 0:
            print(f'  rendered {i}/{len(chapter_keys)}...')

    # Summary
    print(f'\n=== D-2 Bulk Render Report ===')
    print(f'Timestamp: {ISO_TIMESTAMP}')
    print(f'Rendered OK: {len(rendered)} / {len(chapter_keys)}')
    n_with_errs = sum(1 for r in rendered if r['errs'])
    print(f'With per-file errors: {n_with_errs}')
    print(f'Failed (exception or unrecoverable): {len(failed)}')
    if failed:
        print(f'\nFailures:')
        for k, p, msg in failed[:30]:
            print(f'  {k} [{p}]: {msg}')
        if len(failed) > 30:
            print(f'  ...and {len(failed)-30} more')

    # Aggregate stats
    total_tables = 0
    total_subdivs = 0
    total_thead = 0
    for r in rendered:
        full = os.path.join(REPO_ROOT, r['path'])
        with open(full, encoding='utf-8') as f:
            t = f.read()
        m = re.search(r'<main class="content-wrapper">(.*?)</main>', t, re.DOTALL)
        if m:
            m_inner = m.group(1)
            total_tables += m_inner.count('<table class="scripture-table">')
            total_subdivs += m_inner.count('class="CellSubdivision"')
            total_thead += m_inner.count('<thead>')
    print(f'\nAggregate (rendered files):')
    print(f'  total <table class="scripture-table"> elements: {total_tables:,}')
    print(f'  total <thead> elements: {total_thead:,}')
    print(f'  total CellSubdivision spans: {total_subdivs:,}')

    total_delta = sum(r['new'] - r['old'] for r in rendered)
    print(f'  net byte delta: {total_delta:+,}')

    return 0 if not failed and n_with_errs == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
