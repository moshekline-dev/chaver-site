#!/usr/bin/env python3
"""D-1 v3-fix Mishnah render — Torah-matched HTML structure.

Supersedes d1_v3_render.py. Same subdivision-alignment logic, same Latin column labels,
same CellSubdivision lowercase markers — but:

  1. NO colspan on <th> or <td>. Ever. One <th> per cell, one <td> per cell.
  2. Add `single-col` class to <table> for 1-cell rows (sets td width:100% via main.css).
  3. Add `three-col` class to <table> for 3-cell rows (sets td width:33.33% via main.css).
  4. Default 2-cell rows: bare `scripture-table` (td width:50% via main.css).
  5. Content wrapped in `<p class="torah" dir="rtl">` instead of `<p dir="rtl">`.
  6. rowspan still allowed in <tbody> for asymmetric subdivisions (NEVER in <thead>).

This matches the live Torah unit exemplar at torah-weave/Genesis/genesis-unit-1/genesis-unit-1.html.

Strategy: surgical in-place replacement of just the <main> content region and the D-1 sentinel
in each existing D-1 v3 file. Preserves E-1/E-2 boilerplate, schema, canonical, etc. exactly
as deployed.

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
SENTINEL_NEW = f'<!-- D-1 pilot v3-fix: torah-matched rendering @ {ISO_TIMESTAMP} -->'
PROVENANCE_NEW = f'<!-- rendered-from: _templates/Academic-Content-HE.html @ {ISO_TIMESTAMP} -->'

# 6 pilots: (json_key, disk_path_relative_to_repo)
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


# ===== Label normalization =====
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


# ===== Cell parsing =====
def extract_label_and_body(cell):
    """Consume runs[] until first '\\n' (in a non-marker run); everything before = label."""
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


# ===== HTML rendering =====
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
    """Position class only — never a width class. Width comes from table-level single-col/three-col."""
    if n_cells == 1:
        return 'col-full'
    if idx == 0:
        return 'col-left'
    if idx == n_cells - 1:
        return 'col-right'
    return 'col-middle'


def table_class(n_cells: int) -> str:
    """Width-distribution class on the <table> itself.
    1 cell  → single-col (td width:100%)
    2 cells → bare       (td width:50% — main.css default)
    3 cells → three-col  (td width:33.33%)
    4+ cells (not in pilots) → fall back to bare; D-2 may need a four-col / five-col rule.
    """
    if n_cells == 1:
        return 'scripture-table single-col'
    if n_cells == 3:
        return 'scripture-table three-col'
    return 'scripture-table'


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
            cell_data.append({
                'label': label, 'subdivisions': [], 'single_html': html,
            })
        else:
            preamble_html = ''.join(preambles).strip()
            if preamble_html:
                first_letter, first_html = subdivs_with_letter[0]
                joined = (preamble_html + '<br>' + first_html) if first_html else preamble_html
                subdivs_with_letter[0] = (first_letter, joined)
            cell_data.append({
                'label': label, 'subdivisions': subdivs_with_letter, 'single_html': '',
            })

    max_subdivs = max((len(d['subdivisions']) for d in cell_data), default=0)
    tc = table_class(n_cells)

    lines = [f'<table class="{tc}" dir="rtl">']

    # THEAD — no colspan, one <th> per cell
    thead_cells = []
    for i, d in enumerate(cell_data):
        cls = col_class(n_cells, i)
        thead_cells.append(f'<th class="cell-label {cls}">{escape(d["label"])}</th>')
    lines.append('    <thead>')
    lines.append('        <tr>' + ''.join(thead_cells) + '</tr>')
    lines.append('    </thead>')

    # TBODY
    lines.append('    <tbody>')
    if max_subdivs == 0:
        # Single <tr>, one <td> per cell
        tds = []
        for d in cell_data:
            tds.append(f'<td><p class="torah" dir="rtl">{d["single_html"]}</p></td>')
        lines.append('        <tr>' + ''.join(tds) + '</tr>')
    else:
        for r_idx in range(max_subdivs):
            tds = []
            for d in cell_data:
                n = len(d['subdivisions'])
                if n == 0:
                    if r_idx == 0:
                        rs = f' rowspan="{max_subdivs}"' if max_subdivs > 1 else ''
                        tds.append(f'<td{rs}><p class="torah" dir="rtl">{d["single_html"]}</p></td>')
                    # else: spans from above — no emit
                elif n == max_subdivs:
                    letter, content = d['subdivisions'][r_idx]
                    tds.append(
                        f'<td><p class="torah" dir="rtl"><span class="CellSubdivision"><b>{letter}</b></span> {content}</p></td>'
                    )
                else:
                    # n < max_subdivs
                    if r_idx < n - 1:
                        letter, content = d['subdivisions'][r_idx]
                        tds.append(
                            f'<td><p class="torah" dir="rtl"><span class="CellSubdivision"><b>{letter}</b></span> {content}</p></td>'
                        )
                    elif r_idx == n - 1:
                        letter, content = d['subdivisions'][r_idx]
                        span = max_subdivs - n + 1
                        rs = f' rowspan="{span}"' if span > 1 else ''
                        tds.append(
                            f'<td{rs}><p class="torah" dir="rtl"><span class="CellSubdivision"><b>{letter}</b></span> {content}</p></td>'
                        )
                    # else: spans from above
            lines.append('        <tr>' + ''.join(tds) + '</tr>')
    lines.append('    </tbody>')
    lines.append('</table>')
    return '\n'.join(lines)


def render_chapter_main_content(key: str, ch: dict) -> str:
    tractate_he = ch.get('tractate_he', '')
    chapter_he = ch.get('chapter_he', '')
    suffix = CHAPTER_SUFFIX.get(key, '')
    h1_text = f'{tractate_he} פרק {chapter_he}{suffix} – המבנה הספרותי'

    parts = ['        <article class="mishnah-chapter" dir="rtl">',
             f'        <h1 dir="rtl">{escape(h1_text)}</h1>']
    for row in ch.get('rows', []):
        table_html = render_row_table(row)
        indented = '\n'.join('        ' + line if line else line
                             for line in table_html.split('\n'))
        parts.append(indented)
    parts.append('        </article>')
    return '\n'.join(parts)


# ===== In-place surgical update =====
MAIN_RE = re.compile(r'(<main class="content-wrapper">)(.*?)(</main>)', re.DOTALL)
# Match v2 / v3 / v3-fix sentinels (handles any future "v[N][-suffix]" form)
SENTINEL_ANY_RE = re.compile(r'<!--\s*D-1 pilot v[0-9][0-9a-z\-]*:[^>]*-->')
PROVENANCE_RE = re.compile(r'<!-- rendered-from: _templates/Academic-Content-HE\.html @ [^>]+-->')


def transform_file(file_text: str, new_main_inner: str) -> str:
    def main_repl(m):
        return f'{m.group(1)}\n{new_main_inner}\n    {m.group(3)}'
    new_text, n_main = MAIN_RE.subn(main_repl, file_text, count=1)
    if n_main != 1:
        raise RuntimeError(f'Expected exactly 1 <main> match, got {n_main}')
    new_text, n_sent = SENTINEL_ANY_RE.subn(SENTINEL_NEW, new_text, count=1)
    if n_sent != 1:
        raise RuntimeError(f'Expected exactly 1 D-1 sentinel match, got {n_sent}')
    new_text, n_prov = PROVENANCE_RE.subn(PROVENANCE_NEW, new_text, count=1)
    if n_prov != 1:
        raise RuntimeError(f'Expected exactly 1 provenance match, got {n_prov}')
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

    # JSON-LD reparse
    for blk in JSON_LD_RE.findall(text):
        try:
            json.loads(blk)
        except Exception as e:
            errors.append(f'JSON-LD parse error: {e}')

    # Sentinel
    if text.count(SENTINEL_NEW) != 1:
        errors.append(f'v3-fix sentinel count = {text.count(SENTINEL_NEW)}, want 1')
    if 'D-1 pilot v3:' in text and 'v3-fix' not in 'D-1 pilot v3:':
        errors.append('stale v3 sentinel still present')

    # NO colspan anywhere — that's the headline rule
    # We narrow this to inside the <main> content
    main_match = re.search(r'<main class="content-wrapper">(.*?)</main>', text, re.DOTALL)
    main_inner = main_match.group(1) if main_match else ''
    n_colspan = len(re.findall(r'\scolspan=', main_inner))
    if n_colspan != 0:
        errors.append(f'colspan count in <main> = {n_colspan}, want 0')

    # rowspan ONLY in tbody, never in thead
    thead_blocks = re.findall(r'<thead>.*?</thead>', main_inner, re.DOTALL)
    for t in thead_blocks:
        if 'rowspan' in t:
            errors.append('rowspan found in <thead> — must be tbody only')
            break

    # Every <td> has a <p class="torah" dir="rtl"> inside (or <p class="torah"> with separate dir)
    n_td = main_inner.count('<td')
    n_torah_p = len(re.findall(r'<p class="torah"[^>]*>', main_inner))
    if n_td != n_torah_p:
        errors.append(f'<td> count ({n_td}) != <p class="torah"> count ({n_torah_p})')

    # 1-cell rows have scripture-table single-col; 3-cell rows have three-col
    # Count tables per type — just sanity, not strict
    n_single = main_inner.count('class="scripture-table single-col"')
    n_three = main_inner.count('class="scripture-table three-col"')
    n_bare = (main_inner.count('class="scripture-table"') -
              main_inner.count('class="scripture-table single-col"') -
              main_inner.count('class="scripture-table three-col"'))
    # nothing strict — just record

    # No Hebrew letters in <th>
    he_th = re.findall(r'<th class="cell-label [^"]*">[^<]*[א-ה][^<]*</th>', text)
    if he_th:
        errors.append(f'th still has Hebrew letters: {he_th[:2]}')

    # E-1 + E-2 + brand
    if '<!-- /E-1 -->' not in text:
        errors.append('E-1 boilerplate missing')
    if '<!-- /E-2 -->' not in text:
        errors.append('E-2 boilerplate missing')
    if '<div class="nav-brand">chaver.com</div>' not in text:
        errors.append('chaver.com brand missing')

    return size, errors, {
        'colspan_count': n_colspan,
        'tables_single_col': n_single,
        'tables_three_col': n_three,
        'tables_bare': n_bare,
        'td_count': n_td,
        'torah_p_count': n_torah_p,
        'subdiv_spans': main_inner.count('class="CellSubdivision"'),
        'rowspan_in_tbody': main_inner.count('rowspan='),  # all rowspans
    }


def atomic_write(file_path: str, content: str) -> int:
    data = content.encode('utf-8')
    dir_ = os.path.dirname(file_path)
    fd, tmp = tempfile.mkstemp(prefix='.d1v3fix-', dir=dir_)
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

    print('\n=== D-1 v3-fix Render Report ===')
    print(f'Timestamp: {ISO_TIMESTAMP}')
    print(f'Pilots rendered: {len(rendered)}; failed: {len(failed)}')
    print()
    print('| Key | Old size | New size | Δ | Rows | colspan | td/p.torah | scr-tbl bare/single/three | subdiv spans | rowspan | Errors |')
    print('|---|---:|---:|---:|---:|---:|---|---|---:|---:|---|')
    for r in rendered:
        s = r['stats']
        err_str = '; '.join(r['errors']) if r['errors'] else '✓'
        ttype = f"{s['tables_bare']}/{s['tables_single_col']}/{s['tables_three_col']}"
        print(f'| {r["key"]} | {r["old_size"]:,} | {r["new_size"]:,} | {r["delta"]:+,} | {r["n_rows"]} | {s["colspan_count"]} | {s["td_count"]}/{s["torah_p_count"]} | {ttype} | {s["subdiv_spans"]} | {s["rowspan_in_tbody"]} | {err_str} |')
    if failed:
        print('\nFailures:')
        for k, msg in failed:
            print(f'  - {k}: {msg}')
    return 0 if not failed and all(not r['errors'] for r in rendered) else 1


if __name__ == '__main__':
    sys.exit(main())
