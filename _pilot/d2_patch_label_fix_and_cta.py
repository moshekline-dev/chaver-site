#!/usr/bin/env python3
"""D-2 patch: label-fix + PDF CTA.

Two passes:
  Patch 1 (2026-05-15T04:49:49Z) — 6 chapters re-rendered, all 525 got
  CTA + sentinel.
  Patch 2 (same timestamp, same script) — 16 additional chapters re-rendered
  after two function tightenings (skip leading whitespace before subdivision
  marker; bare Hebrew letter conversion) plus Tightening 3 (long recovered
  label + multi-line cell → content with no label).

Function rules (final state):

  normalize_label:
    - '^(\\d+)\\s*([אבגדה])$'  → digit + Latin (e.g. '1א' → '1A', '2 ב' → '2B')
    - '^([אבגדה])$'             → bare Hebrew letter → Latin (e.g. 'ב' → 'B')
    - otherwise unchanged. Internal spaces preserved.

  extract_label_and_body:
    - Empty runs → fall back to cell.label / cell.text split.
    - Skip leading whitespace-only runs.
    - Case 1: first non-ws run is A-E (Latin) → use as label, body = rest.
    - Case 2: 1-cell row with no \\n anywhere → content, no label.
    - Case 3: standard accumulate-until-\\n. Then if the recovered label is
      longer than 10 chars AND the runs contain \\n, treat the whole cell as
      content with json_label as the (typically empty) label.

  render_chapter_main_content:
    - Always embeds the CTA inside <article class="mishnah-chapter">.

Sentinel: <!-- D-2 patch: label-fix-plus-cta @ {ISO_TIMESTAMP} -->

Run-once: this script is idempotent. On re-run it replaces <main> for every
key in PATCH_RENDER_KEYS using the current function logic; for keys NOT in
PATCH_RENDER_KEYS, it leaves <main> alone and only refreshes the sentinel +
ensures the CTA is present.
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

# To preserve the original patch timestamp across re-runs, set this env var:
#   D2_PATCH_TIMESTAMP=2026-05-15T04:49:49Z python3 d2_patch_label_fix_and_cta.py
ISO_TIMESTAMP = os.environ.get('D2_PATCH_TIMESTAMP') or time.strftime(
    '%Y-%m-%dT%H:%M:%SZ', time.gmtime())
SENTINEL_NEW = f'<!-- D-2 patch: label-fix-plus-cta @ {ISO_TIMESTAMP} -->'

URL_PREFIX = 'https://chaver.com/'

HE_TO_LATIN = {'א': 'A', 'ב': 'B', 'ג': 'C', 'ד': 'D', 'ה': 'E'}
SUBDIVISION_LETTERS = {'A', 'B', 'C', 'D', 'E'}
CHAPTER_SUFFIX = {'sotah_9a': ' (חלק א)', 'sotah_9b': ' (חלק ב)'}

# 22 chapters total: 6 from the first patch + 16 from the follow-up.
PATCH_RENDER_KEYS = {
    # --- First patch (6) ---
    'bavametzia_2', 'avot_2', 'gittin_3', 'ketubot_2', 'chagigah_2', 'eduyot_7',
    # --- Follow-up patch (16) ---
    'bavabatra_3', 'makkot_3', 'shabbat_7', 'avodazara_5', 'beitzah_3',
    'ketubot_4', 'ketubot_5', 'ketubot_8', 'pesachim_9', 'sanhedrin_1',
    'shabbat_12', 'shabbat_15', 'shabbat_16', 'shabbat_6', 'shekalim_2',
    'zevachim_6',
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
    '        </div>'
)
CTA_SENTINEL_COMMENT = '<!-- PDF CTA — added by D-2 patch -->'


# ============================ Label / body extraction ============================

DIGIT_HE_RE = re.compile(r'^(\d+)\s*([אבגדה])$')
BARE_HE_RE = re.compile(r'^([אבגדה])$')


def normalize_label(raw):
    if not raw:
        return ''
    s = raw.strip()
    if not s:
        return ''
    m = DIGIT_HE_RE.match(s)
    if m:
        return m.group(1) + HE_TO_LATIN[m.group(2)]
    m = BARE_HE_RE.match(s)
    if m:
        return HE_TO_LATIN[m.group(1)]
    return s


def extract_label_and_body(cell, n_cells_in_row):
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

    # Skip leading whitespace-only runs
    start = 0
    while (start < len(runs) and
           runs[start].get('marker') is None and
           runs[start].get('text', '').strip() == ''):
        start += 1

    # Case 1: first non-ws run is a single Latin subdivision marker (A-E)
    if (start < len(runs) and
            runs[start].get('marker') is None and
            runs[start].get('text', '').strip() in SUBDIVISION_LETTERS):
        label = runs[start]['text'].strip()
        body_start = start + 1
        while (body_start < len(runs) and
               runs[body_start].get('marker') is None and
               runs[body_start].get('text', '').strip() == ''):
            body_start += 1
        return label, runs[body_start:]

    # Case 2: single-cell row with no \n anywhere → content, no label
    if n_cells_in_row == 1:
        has_nl = any('\n' in r.get('text', '') for r in runs)
        if not has_nl:
            return json_label, list(runs)

    # Case 3: standard accumulation
    label_parts, body_runs, consumed = [], [], False
    for run in runs:
        if consumed:
            body_runs.append(run)
            continue
        rt = run.get('text', '')
        marker = run.get('marker')
        if '\n' in rt and marker is None:
            nl_pos = rt.index('\n')
            before, after = rt[:nl_pos], rt[nl_pos + 1:]
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
    candidate_label = ''.join(label_parts).strip()

    # Tightening 3: long recovered label + multi-line cell → content
    if len(candidate_label) > 10:
        has_nl_in_runs = any('\n' in r.get('text', '') for r in runs)
        if has_nl_in_runs:
            return json_label, list(runs)

    return candidate_label, body_runs


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
        s = mi + 1
        while (s < end and
               body_runs[s].get('marker') is None and
               body_runs[s].get('text', '').strip() == ''):
            s += 1
        segments.append((letter, body_runs[s:end]))
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
                    tds.append(f'<td{cs}><p class="torah"><span class="CellSubdivision"><b>{letter}</b></span> {content}</p></td>')
                else:
                    if r_idx < n - 1:
                        letter, content = d['subdivisions'][r_idx]
                        tds.append(f'<td{cs}><p class="torah"><span class="CellSubdivision"><b>{letter}</b></span> {content}</p></td>')
                    elif r_idx == n - 1:
                        letter, content = d['subdivisions'][r_idx]
                        span = max_subdivs - n + 1
                        rs = f' rowspan="{span}"' if span > 1 else ''
                        tds.append(f'<td{cs}{rs}><p class="torah"><span class="CellSubdivision"><b>{letter}</b></span> {content}</p></td>')
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
    parts.append(CTA_HTML)
    parts.append('        </article>')
    return '\n'.join(parts)


# =================================== Transforms ===================================

def derive_disk_path(source_url):
    if not source_url.startswith(URL_PREFIX):
        raise ValueError(f'URL prefix mismatch: {source_url!r}')
    path_part = source_url[len(URL_PREFIX):]
    decoded = urllib.parse.unquote(path_part)
    if not decoded.endswith('.htm'):
        decoded += '.htm'
    return decoded


MAIN_RE = re.compile(r'(<main class="content-wrapper">)(.*?)(</main>)', re.DOTALL)
ARTICLE_RE = re.compile(r'(<article class="mishnah-chapter">.*?)(\n\s*</article>)', re.DOTALL)
D2_SENTINEL_RE = re.compile(r'<!--\s*D-2[^>]*-->')


def replace_main(file_text, new_main_inner):
    def repl(m):
        return f'{m.group(1)}\n{new_main_inner}\n    {m.group(3)}'
    new_text, n = MAIN_RE.subn(repl, file_text, count=1)
    if n != 1:
        raise RuntimeError(f'Expected 1 <main> match, got {n}')
    return new_text


def ensure_cta(file_text):
    """Inject CTA inside <article> if missing. Idempotent."""
    if CTA_SENTINEL_COMMENT in file_text:
        return file_text, False
    def repl(m):
        return f'{m.group(1)}\n{CTA_HTML}{m.group(2)}'
    new_text, n = ARTICLE_RE.subn(repl, file_text, count=1)
    if n != 1:
        raise RuntimeError('article wrapper not found for CTA injection')
    return new_text, True


def update_sentinel(file_text):
    new_text, n = D2_SENTINEL_RE.subn(SENTINEL_NEW, file_text, count=1)
    if n != 1:
        if '<head>' in file_text and SENTINEL_NEW not in file_text:
            return file_text.replace('<head>', f'<head>\n    {SENTINEL_NEW}', 1)
        raise RuntimeError(f'Expected 1 D-2 sentinel match, got {n}')
    return new_text


JSON_LD_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.DOTALL)


def verify_file(file_path):
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
    if CTA_SENTINEL_COMMENT not in text:
        errors.append('CTA missing')
    if 'The%20Structured%20Mishnah.pdf' not in text:
        errors.append('PDF link missing')
    if text.count('<article class="mishnah-chapter">') != 1:
        errors.append('article wrapper count != 1')
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
    with open(JSON_PATH, encoding='utf-8') as f:
        db = json.load(f)
    chapter_keys = [k for k in db if not k.startswith('_')]
    print(f'Sentinel: {SENTINEL_NEW}')
    print(f'Chapters to process: {len(chapter_keys)}')
    print(f'Re-render targets: {len(PATCH_RENDER_KEYS)}')

    missing = []
    for k in chapter_keys:
        try:
            rel = derive_disk_path(db[k]['source_url'])
            if not os.path.exists(os.path.join(REPO_ROOT, rel)):
                missing.append((k, rel))
        except Exception as e:
            missing.append((k, str(e)))
    if missing:
        print(f'PRE-FLIGHT FAILED: {len(missing)} chapters cannot be mapped')
        return 1
    for k in PATCH_RENDER_KEYS:
        if k not in db:
            print(f'ERROR: re-render key {k!r} not in JSON')
            return 1

    rendered, failed = [], []
    for i, key in enumerate(chapter_keys, 1):
        ch = db[key]
        try:
            rel = derive_disk_path(ch['source_url'])
            full = os.path.join(REPO_ROOT, rel)
            with open(full, encoding='utf-8') as f:
                old_text = f.read()
            old_size = len(old_text.encode('utf-8'))
            new_text = old_text
            if key in PATCH_RENDER_KEYS:
                inner = render_chapter_main_content(key, ch)
                new_text = replace_main(new_text, inner)
            new_text, _ = ensure_cta(new_text)
            new_text = update_sentinel(new_text)
            new_size = atomic_write(full, new_text)
            size, errs = verify_file(full)
            rendered.append({'key': key, 'old': old_size, 'new': size, 'errs': errs,
                             'rendered': key in PATCH_RENDER_KEYS})
            if errs:
                failed.append((key, rel, '; '.join(errs)))
        except Exception as e:
            failed.append((key, ch.get('source_url', ''),
                           f'EXCEPTION: {type(e).__name__}: {e}'))
        if i % 50 == 0:
            print(f'  processed {i}/{len(chapter_keys)}...')

    print(f'\n=== D-2 Patch Report ===')
    print(f'Processed: {len(rendered)} / {len(chapter_keys)}')
    print(f'Re-rendered: {sum(1 for r in rendered if r["rendered"])}')
    n_errs = sum(1 for r in rendered if r['errs'])
    print(f'Verify errors: {n_errs}')
    print(f'Failures: {len(failed)}')
    if failed:
        for k, p_, msg in failed[:30]:
            print(f'  {k}: {msg}')
    return 0 if not failed and n_errs == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
