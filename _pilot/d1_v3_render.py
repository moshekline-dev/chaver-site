#!/usr/bin/env python3
"""D-1 v3 Mishnah render — subdivision-aligned <tr>s + Latin column labels + CellSubdivision spans.

Strategy: surgical in-place replacement of just the <main> content region and the D-1 sentinel
in each existing D-1 v2 file. Preserves E-1/E-2 boilerplate, schema, canonical, etc. exactly
as deployed.

Changes from v2:
  1. Column header labels Hebrew → Latin (1א → 1A); strip spaces (`1 א` → `1A`).
  2. <th> classes: `cell-label col-left/middle/right/full` (was `col-a/b/c/full`).
  3. Subdivision markers (`A`,`B`,`C`,`D`,`E` in runs) → lowercase, wrapped in
     <span class="CellSubdivision"><b>a</b></span>.
  4. Each subdivision gets its own <tr>; parallel subdivisions across cells align vertically;
     cells with fewer subdivisions use rowspan to span remaining rows.

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
SENTINEL_V3 = f'<!-- D-1 pilot v3: subdivision-aligned rendering @ {ISO_TIMESTAMP} -->'
PROVENANCE_V3 = f'<!-- rendered-from: _templates/Academic-Content-HE.html @ {ISO_TIMESTAMP} -->'

# 6 pilots: (json_key, disk_path_relative_to_repo)
PILOTS = [
    ('berakhot_1', 'Mishnah-New/Hebrew/Text/Seder Zeraim/Masechet Brachot/Mesechet Brachot Perek 1.htm'),
    ('megillah_1', 'Mishnah-New/Hebrew/Text/Seder Moed/Masechet Megillah/Masechet Megillah Perek 1.htm'),
    ('eduyot_1',   'Mishnah-New/Hebrew/Text/Seder Nezikin/Masechet Eduyot/Masechet Eduyot Perek 1.htm'),
    ('kinnim_1',   'Mishnah-New/Hebrew/Text/Seder Kodashim/Masechet Kinnim/Masechet Kinnim Perek 1.htm'),
    ('sotah_9a',   'Mishnah-New/Hebrew/Text/Seder Nashim/Masechet Sotah/Masechet Sotah Perek 9 A.htm'),
    ('shabbat_22', 'Mishnah-New/Hebrew/Text/Seder Moed/Masechet Shabbat/Masechet Shabbat Perek 22.htm'),
]

# Chapter title suffix for split-chapter files
CHAPTER_SUFFIX = {'sotah_9a': ' (חלק א)', 'sotah_9b': ' (חלק ב)'}

# Hebrew column letters → Latin
HE_TO_LATIN = {'א': 'A', 'ב': 'B', 'ג': 'C', 'ד': 'D', 'ה': 'E'}
SUBDIVISION_LETTERS = {'A', 'B', 'C', 'D', 'E'}


# ===== Label normalization =====
def normalize_label(raw: str) -> str:
    """'1א' → '1A'; '1 א' → '1A'; '2ב' → '2B'. Latin / words / plain numbers unchanged."""
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
    """Walk runs[]; consume everything up to the first '\\n' as the label;
    rest becomes body_runs (a list of run-dicts).

    Handles split-label runs (e.g. run[0]='1', run[1]='ב', run[2]='\\n').
    """
    runs = cell.get('runs', [])
    if not runs:
        # No runs → fall back to text field
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
            # newline inside marker — rare; treat whole run as body
            body_runs.append(run)
            consumed_newline = True
        else:
            label_parts.append(rt)
    return ''.join(label_parts).strip(), body_runs


def is_subdivision_marker_run(run) -> bool:
    return (run.get('marker') is None and
            run.get('text', '').strip() in SUBDIVISION_LETTERS)


def split_into_subdivisions(body_runs):
    """Return list of (letter_or_None, list_of_runs).
    None-letter segments are pre-marker preambles (rare in practice).
    Letter segments start AFTER the marker run (which is itself dropped).
    """
    marker_positions = [(i, r['text'].strip())
                        for i, r in enumerate(body_runs)
                        if is_subdivision_marker_run(r)]
    if not marker_positions:
        return [(None, body_runs)]

    segments = []
    # Preamble before first marker
    first_idx = marker_positions[0][0]
    if first_idx > 0:
        preamble = body_runs[:first_idx]
        if any(r.get('text', '').strip() for r in preamble):
            segments.append((None, preamble))

    for j, (mi, letter) in enumerate(marker_positions):
        end = marker_positions[j + 1][0] if j + 1 < len(marker_positions) else len(body_runs)
        start = mi + 1
        # Skip pure-whitespace run immediately after the marker (the ' ' separator)
        while (start < end and
               body_runs[start].get('marker') is None and
               body_runs[start].get('text', '').strip() == ''):
            start += 1
        segments.append((letter, body_runs[start:end]))
    return segments


# ===== HTML rendering =====
def render_runs_html(runs) -> str:
    """Concat runs to HTML. Markers → <span class="<marker>"><b>...</b></span>.
    \\n in plain runs → <br>. Trim leading/trailing <br>.
    """
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
    # Collapse leading whitespace that follows a <br>... actually keep as-is, harmless.
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
        colspan = (cell.get('position', {}) or {}).get('colspan', 1) or 1

        subdivs_with_letter = [(letter.lower(), render_runs_html(runs))
                               for letter, runs in segments if letter is not None]
        preambles = [render_runs_html(runs) for letter, runs in segments if letter is None]

        if not subdivs_with_letter:
            # No subdivisions — concatenate all body runs
            html = render_runs_html(body_runs)
            cell_data.append({
                'label': label, 'colspan': colspan,
                'subdivisions': [], 'single_html': html,
            })
        else:
            # If there's a non-empty preamble before the first subdivision, prepend it to that subdivision
            preamble_html = ''.join(preambles).strip()
            if preamble_html:
                first_letter, first_html = subdivs_with_letter[0]
                joined = (preamble_html + '<br>' + first_html) if first_html else preamble_html
                subdivs_with_letter[0] = (first_letter, joined)
            cell_data.append({
                'label': label, 'colspan': colspan,
                'subdivisions': subdivs_with_letter, 'single_html': '',
            })

    max_subdivs = max((len(d['subdivisions']) for d in cell_data), default=0)

    lines = ['<table class="scripture-table" dir="rtl">']
    # THEAD
    thead = []
    for i, d in enumerate(cell_data):
        cls = col_class(n_cells, i)
        cs = f' colspan="{d["colspan"]}"' if d['colspan'] > 1 else ''
        thead.append(f'<th class="cell-label {cls}"{cs}>{escape(d["label"])}</th>')
    lines.append('  <thead><tr>' + ''.join(thead) + '</tr></thead>')

    # TBODY
    lines.append('  <tbody>')
    if max_subdivs == 0:
        row_cells = []
        for d in cell_data:
            cs = f' colspan="{d["colspan"]}"' if d['colspan'] > 1 else ''
            row_cells.append(f'<td{cs}><p dir="rtl">{d["single_html"]}</p></td>')
        lines.append('    <tr>' + ''.join(row_cells) + '</tr>')
    else:
        for r_idx in range(max_subdivs):
            row_cells = []
            for d in cell_data:
                n = len(d['subdivisions'])
                cs = f' colspan="{d["colspan"]}"' if d['colspan'] > 1 else ''
                if n == 0:
                    if r_idx == 0:
                        rs = f' rowspan="{max_subdivs}"' if max_subdivs > 1 else ''
                        row_cells.append(f'<td{cs}{rs}><p dir="rtl">{d["single_html"]}</p></td>')
                    # else: spans from above — emit nothing
                elif n == max_subdivs:
                    letter, content = d['subdivisions'][r_idx]
                    row_cells.append(
                        f'<td{cs}><p dir="rtl"><span class="CellSubdivision"><b>{letter}</b></span> {content}</p></td>'
                    )
                else:
                    # n < max_subdivs, asymmetric
                    if r_idx < n - 1:
                        letter, content = d['subdivisions'][r_idx]
                        row_cells.append(
                            f'<td{cs}><p dir="rtl"><span class="CellSubdivision"><b>{letter}</b></span> {content}</p></td>'
                        )
                    elif r_idx == n - 1:
                        letter, content = d['subdivisions'][r_idx]
                        span = max_subdivs - n + 1
                        rs = f' rowspan="{span}"' if span > 1 else ''
                        row_cells.append(
                            f'<td{cs}{rs}><p dir="rtl"><span class="CellSubdivision"><b>{letter}</b></span> {content}</p></td>'
                        )
                    # else: spans from above
            lines.append('    <tr>' + ''.join(row_cells) + '</tr>')
    lines.append('  </tbody>')
    lines.append('</table>')
    return '\n'.join(lines)


def render_chapter_main_content(key: str, ch: dict) -> str:
    """Build the inner content of <main class="content-wrapper"> — the <article> + h1 + tables."""
    tractate_he = ch.get('tractate_he', '')
    chapter_he = ch.get('chapter_he', '')
    suffix = CHAPTER_SUFFIX.get(key, '')
    h1_text = f'{tractate_he} פרק {chapter_he}{suffix} – המבנה הספרותי'

    parts = ['        <article class="mishnah-chapter" dir="rtl">',
             f'        <h1 dir="rtl">{escape(h1_text)}</h1>']
    for row in ch.get('rows', []):
        table_html = render_row_table(row)
        # Indent table block for readability
        indented = '\n'.join('        ' + line if line else line
                             for line in table_html.split('\n'))
        parts.append(indented)
    parts.append('        </article>')
    return '\n'.join(parts)


# ===== In-place surgical update of existing v2 file =====
MAIN_RE = re.compile(
    r'(<main class="content-wrapper">)(.*?)(</main>)',
    re.DOTALL,
)
SENTINEL_V2_RE = re.compile(r'<!-- D-1 pilot v[0-9]+: [^>]*-->')
PROVENANCE_RE = re.compile(r'<!-- rendered-from: _templates/Academic-Content-HE\.html @ [^>]+-->')


def transform_file(file_text: str, new_main_inner: str) -> str:
    """Replace <main> inner content + update sentinel + provenance timestamp."""
    # 1. Replace main content
    def main_repl(m):
        return f'{m.group(1)}\n{new_main_inner}\n    {m.group(3)}'
    new_text, n_main = MAIN_RE.subn(main_repl, file_text, count=1)
    if n_main != 1:
        raise RuntimeError(f'Expected exactly 1 <main> match, got {n_main}')
    # 2. Replace D-1 sentinel
    new_text, n_sent = SENTINEL_V2_RE.subn(SENTINEL_V3, new_text, count=1)
    if n_sent != 1:
        raise RuntimeError(f'Expected exactly 1 D-1 sentinel match, got {n_sent}')
    # 3. Update provenance timestamp
    new_text, n_prov = PROVENANCE_RE.subn(PROVENANCE_V3, new_text, count=1)
    if n_prov != 1:
        raise RuntimeError(f'Expected exactly 1 provenance match, got {n_prov}')
    return new_text


# ===== Verification =====
JSON_LD_RE = re.compile(
    r'<script type="application/ld\+json">(.*?)</script>',
    re.DOTALL,
)


def verify(file_path: str, original_bytes: int):
    errors = []
    with open(file_path, 'rb') as f:
        data = f.read()
    size = len(data)
    if size < 5000:
        errors.append(f'suspiciously small: {size} bytes')
    if not data.rstrip().endswith(b'</html>'):
        errors.append('does not end with </html>')
    text = data.decode('utf-8')
    # All JSON-LD blocks reparse
    for blk in JSON_LD_RE.findall(text):
        try:
            json.loads(blk)
        except Exception as e:
            errors.append(f'JSON-LD parse error: {e}')
    # Sentinel present, only once
    if text.count(SENTINEL_V3) != 1:
        errors.append(f'sentinel count = {text.count(SENTINEL_V3)}, want 1')
    # No v2 sentinel left
    if 'D-1 pilot v2:' in text:
        errors.append('stale v2 sentinel still present')
    # E-1 + E-2 boilerplate preserved
    if '<!-- /E-1 -->' not in text:
        errors.append('E-1 boilerplate missing')
    if '<!-- /E-2 -->' not in text:
        errors.append('E-2 boilerplate missing')
    if '<div class="nav-brand">chaver.com</div>' not in text:
        errors.append('chaver.com brand missing')
    # Latin labels — no Hebrew letter on header th anymore for these 6 pilots
    # (all pilot labels use Hebrew letters)
    # Spot-check: each <th class="cell-label ..."> should not contain Hebrew א/ב/ג/ד/ה
    he_th_pattern = re.compile(r'<th class="cell-label [^"]*">[^<]*[א-ה][^<]*</th>')
    bad_th = he_th_pattern.findall(text)
    if bad_th:
        errors.append(f'th still contains Hebrew letters: {bad_th[:3]}')
    return size, errors


def atomic_write(file_path: str, content: str) -> int:
    """Write content to file_path atomically. Returns final byte count."""
    data = content.encode('utf-8')
    dir_ = os.path.dirname(file_path)
    fd, tmp = tempfile.mkstemp(prefix='.d1v3-', dir=dir_)
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
            actual_size, errs = verify(path, new_size)
            if errs:
                failed.append((key, '; '.join(errs)))
            rendered.append({
                'key': key,
                'path': rel,
                'old_size': old_size,
                'new_size': actual_size,
                'delta': actual_size - old_size,
                'n_rows': len(ch.get('rows', [])),
                'errors': errs,
            })
        except Exception as e:
            failed.append((key, f'EXCEPTION: {type(e).__name__}: {e}'))

    # Report
    print('\n=== D-1 v3 Render Report ===')
    print(f'Timestamp: {ISO_TIMESTAMP}')
    print(f'Pilots rendered: {len(rendered)}; failed: {len(failed)}')
    print()
    print('| Key | Old size | New size | Δ | Rows | Errors |')
    print('|---|---:|---:|---:|---:|---|')
    for r in rendered:
        err_str = '; '.join(r['errors']) if r['errors'] else '✓'
        print(f'| {r["key"]} | {r["old_size"]:,} | {r["new_size"]:,} | {r["delta"]:+,} | {r["n_rows"]} | {err_str} |')
    if failed:
        print('\nFailures:')
        for k, msg in failed:
            print(f'  - {k}: {msg}')
    return 0 if not failed and all(not r['errors'] for r in rendered) else 1


if __name__ == '__main__':
    sys.exit(main())
