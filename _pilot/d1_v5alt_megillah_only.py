#!/usr/bin/env python3
"""D-1 v5-alt — chat-Claude's proposed fix, applied to megillah_1 ONLY for A/B comparison.

Difference vs my d1_v5_render.py:
  * Drops `cell-label` from <th> classes — uses only `col-a` / `col-b` / `col-c` / `col-full`.
  * Restores colspan attribute on <th> AND <td> from JSON `position.colspan`.
  * Keeps the bare <article> wrapper that my v5 already produced.

Sentinel: `<!-- D-1 pilot v5-alt: drop-cell-label-restore-colspans @ ... -->`

This is a single-chapter experiment to compare the two fixes visually on the live site:
  - megillah_1  → chat-Claude's variant (this script)
  - berakhot_1, eduyot_1, kinnim_1, sotah_9a, shabbat_22  → my v5 (unchanged)

Strategy: surgical in-place — find <article>...</article>, replace the tables between the
first <table and the last </table>, swap the D-1 sentinel.
"""
import json
import os
import re
import sys
import tempfile
import time
from html import escape

REPO_ROOT = '/sessions/sharp-eloquent-mccarthy/mnt/chaver-site'
JSON_PATH = os.path.join(REPO_ROOT, 'Mishnah-New/English/mishnah_db.json')

ISO_TIMESTAMP = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
SENTINEL_NEW = f'<!-- D-1 pilot v5-alt: drop-cell-label-restore-colspans @ {ISO_TIMESTAMP} -->'
PROVENANCE_NEW = f'<!-- rendered-from: _templates/Academic-Content-HE.html @ {ISO_TIMESTAMP} -->'

PILOT_KEY = 'megillah_1'
PILOT_PATH = 'Mishnah-New/Hebrew/Text/Seder Moed/Masechet Megillah/Masechet Megillah Perek 1.htm'

HE_TO_LATIN = {'א': 'A', 'ב': 'B', 'ג': 'C', 'ד': 'D', 'ה': 'E'}
SUBDIVISION_LETTERS = {'A', 'B', 'C', 'D', 'E'}


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
    """Use the v2/chat-Claude naming: col-a / col-b / col-c / col-full."""
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

    # THEAD — colspan from JSON shape, color class only (no `cell-label`)
    thead_cells = []
    for i, d in enumerate(cell_data):
        cls = color_class(n_cells, i)
        cs = f' colspan="{d["colspan"]}"' if d['colspan'] > 1 else ''
        thead_cells.append(f'<th class="{cls}"{cs}>{escape(d["label"])}</th>')
    lines.append('    <thead>')
    lines.append('        <tr>' + ''.join(thead_cells) + '</tr>')
    lines.append('    </thead>')

    # TBODY — colspan from JSON shape, rowspan for asymmetric subdivisions
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


CHAPTER_SUFFIX = {'sotah_9a': ' (חלק א)', 'sotah_9b': ' (חלק ב)'}

def render_chapter_main_content(key, ch):
    tractate_he = ch.get('tractate_he', '')
    chapter_he = ch.get('chapter_he', '')
    suffix = CHAPTER_SUFFIX.get(key, '')
    h1_text = f'{tractate_he} פרק {chapter_he}{suffix} – המבנה הספרותי'

    parts = ['        <article>',
             f'        <h1>{escape(h1_text)}</h1>']
    for row in ch.get('rows', []):
        table_html = render_row_table(row)
        indented = '\n'.join('        ' + line if line else line
                             for line in table_html.split('\n'))
        parts.append(indented)
    parts.append('        </article>')
    return '\n'.join(parts)


MAIN_RE = re.compile(r'(<main class="content-wrapper">)(.*?)(</main>)', re.DOTALL)
SENTINEL_ANY_RE = re.compile(r'<!--\s*D-1 pilot v[0-9][0-9a-z\-]*:[^>]*-->')
PROVENANCE_RE = re.compile(r'<!-- rendered-from: _templates/Academic-Content-HE\.html @ [^>]+-->')


def transform_file(file_text, new_main_inner):
    def main_repl(m):
        return f'{m.group(1)}\n{new_main_inner}\n    {m.group(3)}'
    new_text, n_main = MAIN_RE.subn(main_repl, file_text, count=1)
    if n_main != 1:
        raise RuntimeError(f'Expected 1 <main> match, got {n_main}')
    new_text, n_sent = SENTINEL_ANY_RE.subn(SENTINEL_NEW, new_text, count=1)
    if n_sent != 1:
        raise RuntimeError(f'Expected 1 D-1 sentinel match, got {n_sent}')
    new_text, n_prov = PROVENANCE_RE.subn(PROVENANCE_NEW, new_text, count=1)
    if n_prov != 1:
        raise RuntimeError(f'Expected 1 provenance match, got {n_prov}')
    return new_text


def atomic_write(file_path, content):
    data = content.encode('utf-8')
    dir_ = os.path.dirname(file_path)
    fd, tmp = tempfile.mkstemp(prefix='.d1v5alt-', dir=dir_)
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
    with open(JSON_PATH, encoding='utf-8') as f:
        db = json.load(f)
    ch = db[PILOT_KEY]
    path = os.path.join(REPO_ROOT, PILOT_PATH)
    with open(path, encoding='utf-8') as f:
        old_text = f.read()
    old_size = len(old_text.encode('utf-8'))
    inner = render_chapter_main_content(PILOT_KEY, ch)
    new_text = transform_file(old_text, inner)
    new_size = atomic_write(path, new_text)

    # Verify
    with open(path, encoding='utf-8') as f:
        text = f.read()
    main_inner = re.search(r'<main class="content-wrapper">(.*?)</main>', text, re.DOTALL).group(1)

    checks = {
        'ends_with_html': text.rstrip().endswith('</html>'),
        'sentinel_count_1': text.count(SENTINEL_NEW) == 1,
        'no_cell_label_in_th': not bool(re.search(r'<th[^>]*\bcell-label\b', main_inner)),
        'no_mishnah_chapter_class': '<article class="mishnah-chapter"' not in text,
        'th_count': len(re.findall(r'<th\b', main_inner)),
        'td_count': len(re.findall(r'<td\b', main_inner)),
        'colspan_count_in_main': len(re.findall(r'\scolspan=', main_inner)),
        'subdiv_count': main_inner.count('class="CellSubdivision"'),
        'col_a_count': main_inner.count('class="col-a"') + main_inner.count('class="col-a "'),
    }

    print(f'megillah_1 v5-alt rendered')
    print(f'  old: {old_size:,} bytes  →  new: {new_size:,} bytes  ({new_size - old_size:+,})')
    for k, v in checks.items():
        print(f'  {k}: {v}')

    # Spot-print row 2 table HTML so we can eyeball
    print('\n--- Row 2 rendered HTML (extract) ---')
    match = re.search(r'<table class="scripture-table">[^<]*<thead>[^<]*<tr>[^<]*<th[^>]*>2A</th>.*?</table>', text, re.DOTALL)
    if match:
        print(match.group(0))
    return 0


if __name__ == '__main__':
    sys.exit(main())
