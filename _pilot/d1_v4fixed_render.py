#!/usr/bin/env python3
"""D-1 v4-fixed Mishnah render — exemplar-matched, dir="rtl" removed from content elements.

Supersedes d1_v4_render.py. Critical change: drops dir="rtl" from <article> and <h1>
inside <main> (in addition to the v4 omission of dir="rtl" from <table> and <p>).
The Torah unit exemplars use bare <article> / <h1> — page direction is inherited from
<html lang="he" dir="rtl"> on the template root. The [lang=he], [dir=rtl] CSS rule at
main.css line 593 changes font-family on any descendant element it matches; keeping
dir="rtl" off interior content keeps the cascade clean.

Targets the live Torah unit exemplars:
  * Genesis Unit 1 (2-column)
  * Leviticus Unit 1 (3-column)

Rules vs v3-fix:
  1. <table class="scripture-table"> always — no `three-col`, no `single-col`, no `dir="rtl"`.
  2. <p class="torah"> always — no `dir="rtl"` on <p>. RTL is inherited from <html lang="he" dir="rtl">.
  3. One <th> per cell, one <td> per cell. No colspan anywhere.
  4. rowspan in <tbody> only, for asymmetric subdivision counts.
  5. CellSubdivision lowercase Latin: <span class="CellSubdivision"><b>a</b></span> .
  6. Column header text converted from Hebrew א-ה → A-E; spaces stripped.

Strategy: surgical in-place replacement of just the <main> content region and the D-1 sentinel
in each existing pilot file. Preserves E-1/E-2 boilerplate, schema, canonical, etc. byte-for-byte.

Defensive: atomic write (temp file + fsync + rename), byte-count + ends-with-</html> check,
JSON-LD reparse for every <script type="application/ld+json"> block, sentinel presence check.
"""
import json
import os
import re
import sys
import tempfile
import time
from html import escape

# ===== Config =====
REPO_ROOT = '/sessions/sharp-eloquent-mccarthy/mnt/chaver-site'
JSON_PATH = os.path.join(REPO_ROOT, 'Mishnah-New/English/mishnah_db.json')

ISO_TIMESTAMP = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
SENTINEL_NEW = f'<!-- D-1 pilot v4-fixed: dir-rtl-removed @ {ISO_TIMESTAMP} -->'
PROVENANCE_NEW = f'<!-- rendered-from: _templates/Academic-Content-HE.html @ {ISO_TIMESTAMP} -->'

PILOTS = [
    ('berakhot_1', 'Mishnah-New/Hebrew/Text/Seder Zeraim/Masechet Brachot/Mesechet Brachot Perek 1.htm'),
    ('megillah_1', 'Mishnah-New/Hebrew/Text/Seder Moed/Masechet Megillah/Masechet Megillah Perek 1.htm'),
    ('eduyot_1',   'Mishnah-New/Hebrew/Text/Seder Nezikin/Masechet Eduyot/Masechet Eduyot Perek 1.htm'),
    ('kinnim_1',   'Mishnah-New/Hebrew/Text/Seder Kodashim/Masechet Kinnim/Masechet Kinnim Perek 1.htm'),
    ('sotah_9a',   'Mishnah-New/Hebrew/Text/Seder Nashim/Masechet Sotah/Masechet Sotah Perek 9 A.htm'),
    ('shabbat_22', 'Mishnah-New/Hebrew/Text/Seder Moed/Masechet Shabbat/Masechet Shabbat Perek 22.htm'),
]

CHAPTER_SUFFIX = {'sotah_9a': ' (חלק א)', 'sotah_9b': ' (חלק ב)'}

HE_TO_LATIN = {'א': 'A', 'ב': 'B', 'ג': 'C', 'ד': 'D', 'ה': 'E'}
SUBDIVISION_LETTERS = {'A', 'B', 'C', 'D', 'E'}


def normalize_label(raw: str) -> str:
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
    """Consume runs until first '\\n' in a non-marker run → label; rest = body_runs."""
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
    consumed_newline = False
    for run in runs:
        if consumed_newline:
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
            consumed_newline = True
        elif '\n' in rt and marker is not None:
            body_runs.append(run)
            consumed_newline = True
        else:
            label_parts.append(rt)
    return ''.join(label_parts).strip(), body_runs


def is_subdivision_marker_run(run) -> bool:
    return (run.get('marker') is None and
            run.get('text', '').strip() in SUBDIVISION_LETTERS)


def split_into_subdivisions(body_runs):
    """Return list of (letter_or_None, list_of_runs)."""
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


def render_runs_html(runs) -> str:
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


def col_class(n_cells: int, idx: int) -> str:
    if n_cells == 1:
        return 'col-full'
    if idx == 0:
        return 'col-left'
    if idx == n_cells - 1:
        return 'col-right'
    return 'col-middle'


def render_row_table(row) -> str:
    cells = row.get('cells', [])
    n_cells = len(cells)
    if n_cells == 0:
        return ''

    cell_data = []
    for cell in cells:
        label_raw, body_runs = extract_label_and_body(cell)
        label = normalize_label(label_raw)
        segments = split_into_subdivisions(body_runs)

        subdivs_with_letter = [(letter.lower(), render_runs_html(runs))
                               for letter, runs in segments if letter is not None]
        preambles = [render_runs_html(runs) for letter, runs in segments if letter is None]

        if not subdivs_with_letter:
            html = render_runs_html(body_runs)
            cell_data.append({'label': label, 'subdivisions': [], 'single_html': html})
        else:
            preamble_html = ''.join(preambles).strip()
            if preamble_html:
                first_letter, first_html = subdivs_with_letter[0]
                joined = (preamble_html + '<br>' + first_html) if first_html else preamble_html
                subdivs_with_letter[0] = (first_letter, joined)
            cell_data.append({'label': label, 'subdivisions': subdivs_with_letter, 'single_html': ''})

    max_subdivs = max((len(d['subdivisions']) for d in cell_data), default=0)

    lines = ['<table class="scripture-table">']

    # THEAD — no colspan
    thead_cells = []
    for i, d in enumerate(cell_data):
        cls = col_class(n_cells, i)
        thead_cells.append(f'<th class="cell-label {cls}">{escape(d["label"])}</th>')
    lines.append('    <thead>')
    lines.append('        <tr>' + ''.join(thead_cells) + '</tr>')
    lines.append('    </thead>')

    # TBODY — one <td> per cell, rowspan for asymmetric subdivisions only
    lines.append('    <tbody>')
    if max_subdivs == 0:
        tds = [f'<td><p class="torah">{d["single_html"]}</p></td>' for d in cell_data]
        lines.append('        <tr>' + ''.join(tds) + '</tr>')
    else:
        for r_idx in range(max_subdivs):
            tds = []
            for d in cell_data:
                n = len(d['subdivisions'])
                if n == 0:
                    if r_idx == 0:
                        rs = f' rowspan="{max_subdivs}"' if max_subdivs > 1 else ''
                        tds.append(f'<td{rs}><p class="torah">{d["single_html"]}</p></td>')
                elif n == max_subdivs:
                    letter, content = d['subdivisions'][r_idx]
                    tds.append(
                        f'<td><p class="torah"><span class="CellSubdivision"><b>{letter}</b></span> {content}</p></td>'
                    )
                else:
                    if r_idx < n - 1:
                        letter, content = d['subdivisions'][r_idx]
                        tds.append(
                            f'<td><p class="torah"><span class="CellSubdivision"><b>{letter}</b></span> {content}</p></td>'
                        )
                    elif r_idx == n - 1:
                        letter, content = d['subdivisions'][r_idx]
                        span = max_subdivs - n + 1
                        rs = f' rowspan="{span}"' if span > 1 else ''
                        tds.append(
                            f'<td{rs}><p class="torah"><span class="CellSubdivision"><b>{letter}</b></span> {content}</p></td>'
                        )
            lines.append('        <tr>' + ''.join(tds) + '</tr>')
    lines.append('    </tbody>')
    lines.append('</table>')
    return '\n'.join(lines)


def render_chapter_main_content(key: str, ch: dict) -> str:
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


# ===== In-place surgical update =====
MAIN_RE = re.compile(r'(<main class="content-wrapper">)(.*?)(</main>)', re.DOTALL)
SENTINEL_ANY_RE = re.compile(r'<!--\s*D-1 pilot v[0-9][0-9a-z\-]*:[^>]*-->')
PROVENANCE_RE = re.compile(r'<!-- rendered-from: _templates/Academic-Content-HE\.html @ [^>]+-->')


def transform_file(file_text: str, new_main_inner: str) -> str:
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


# ===== Verification =====
JSON_LD_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.DOTALL)


def verify(file_path: str):
    errors = []
    with open(file_path, 'rb') as f:
        data = f.read()
    size = len(data)
    if size < 5000:
        errors.append(f'suspiciously small: {size} bytes')
    if not data.rstrip().endswith(b'</html>'):
        errors.append('does not end with </html>')
    text = data.decode('utf-8')

    for blk in JSON_LD_RE.findall(text):
        try:
            json.loads(blk)
        except Exception as e:
            errors.append(f'JSON-LD parse error: {e}')

    if text.count(SENTINEL_NEW) != 1:
        errors.append(f'v4 sentinel count = {text.count(SENTINEL_NEW)}, want 1')

    # The v4 spec's automated checks
    main_match = re.search(r'<main class="content-wrapper">(.*?)</main>', text, re.DOTALL)
    main_inner = main_match.group(1) if main_match else ''

    # No three-col / single-col on table
    if re.search(r'<table[^>]*\b(three-col|single-col)\b', main_inner):
        errors.append('three-col or single-col found on table')

    # No dir="rtl" anywhere in <main> (article, h1, table, p — anywhere)
    rtl_hits = re.findall(r'<[a-z][^>]*\bdir="rtl"[^>]*>', main_inner)
    if rtl_hits:
        errors.append(f'dir="rtl" found in <main> on {len(rtl_hits)} element(s): {rtl_hits[:3]}')

    # No colspan in thead
    thead_blocks = re.findall(r'<thead>.*?</thead>', main_inner, re.DOTALL)
    for t in thead_blocks:
        if 'colspan' in t:
            errors.append('colspan in <thead>')
            break

    # No colspan anywhere in main
    if re.search(r'\scolspan=', main_inner):
        errors.append('colspan in <main>')

    # Latin TH labels only
    if re.search(r'<th class="cell-label [^"]*">[^<]*[א-ה][^<]*</th>', text):
        errors.append('Hebrew letter in <th>')

    # CellSubdivision lowercase only
    bad_case = re.findall(r'CellSubdivision"><b>([A-E])</b>', text)
    if bad_case:
        errors.append(f'uppercase CellSubdivision letters: {bad_case}')

    # E-1 + E-2 + brand
    if '<!-- /E-1 -->' not in text:
        errors.append('E-1 missing')
    if '<!-- /E-2 -->' not in text:
        errors.append('E-2 missing')
    if '<div class="nav-brand">chaver.com</div>' not in text:
        errors.append('chaver.com brand missing')

    # All <td> have <p class="torah"> inside
    n_td = len(re.findall(r'<td[^>]*>', main_inner))
    n_p_torah = len(re.findall(r'<p class="torah"[^>]*>', main_inner))
    if n_td != n_p_torah:
        errors.append(f'<td>={n_td} != <p class="torah">={n_p_torah}')

    return size, errors, {
        'n_td': n_td,
        'n_p_torah': n_p_torah,
        'subdiv_spans': main_inner.count('class="CellSubdivision"'),
        'rowspan_count': main_inner.count('rowspan='),
        'th_count': main_inner.count('<th '),
    }


def atomic_write(file_path: str, content: str) -> int:
    data = content.encode('utf-8')
    dir_ = os.path.dirname(file_path)
    fd, tmp = tempfile.mkstemp(prefix='.d1v4fixed-', dir=dir_)
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

    rendered = []
    failed = []

    for key, rel in PILOTS:
        if key not in db:
            failed.append((key, 'JSON key missing'))
            continue
        path = os.path.join(REPO_ROOT, rel)
        if not os.path.exists(path):
            failed.append((key, f'file missing: {path}'))
            continue
        try:
            ch = db[key]
            inner = render_chapter_main_content(key, ch)
            with open(path, encoding='utf-8') as f:
                old_text = f.read()
            old_size = len(old_text.encode('utf-8'))
            new_text = transform_file(old_text, inner)
            new_size = atomic_write(path, new_text)
            actual_size, errs, stats = verify(path)
            if errs:
                failed.append((key, '; '.join(errs)))
            rendered.append({
                'key': key, 'path': rel,
                'old_size': old_size, 'new_size': actual_size,
                'delta': actual_size - old_size,
                'n_rows': len(ch.get('rows', [])),
                'errors': errs, 'stats': stats,
            })
        except Exception as e:
            failed.append((key, f'EXCEPTION: {type(e).__name__}: {e}'))

    print('\n=== D-1 v4-fixed Render Report ===')
    print(f'Timestamp: {ISO_TIMESTAMP}')
    print(f'Pilots rendered: {len(rendered)}; failed: {len(failed)}')
    print()
    print('| Key | Old | New | Δ | Rows | th/td/p | subdiv | rowspan | Errors |')
    print('|---|---:|---:|---:|---:|---|---:|---:|---|')
    for r in rendered:
        s = r['stats']
        err_str = '; '.join(r['errors']) if r['errors'] else '✓'
        ttp = f"{s['th_count']}/{s['n_td']}/{s['n_p_torah']}"
        print(f'| {r["key"]} | {r["old_size"]:,} | {r["new_size"]:,} | {r["delta"]:+,} | {r["n_rows"]} | {ttp} | {s["subdiv_spans"]} | {s["rowspan_count"]} | {err_str} |')
    if failed:
        print('\nFailures:')
        for k, msg in failed:
            print(f'  - {k}: {msg}')
    return 0 if not failed and all(not r['errors'] for r in rendered) else 1


if __name__ == '__main__':
    sys.exit(main())
   ttp = f"{s['th_count']}/{s['n_td']}/{s['n_p_torah']}"
        print(f'| {r["key"]} | {r["old_size"]:,} | {r["new_size"]:,} | {r["delta"]:+,} | {r["n_rows"]} | {ttp} | {s["subdiv_spans"]} | {s["rowspan_count"]} | {err_str} |')
    if failed:
        print('\nFailures:')
        for k, msg in failed:
            print(f'  - {k}: {msg}')
    return 0 if not failed and all(not r['errors'] for r in rendered) else 1


if __name__ == '__main__':
    sys.exit(main())
