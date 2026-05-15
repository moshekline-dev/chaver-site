#!/usr/bin/env python3
"""Repair avot_4 in mishnah_db.json by extracting missing data from the legacy rendered page.

The JSON's `avot_4` has only 5 rows (1 + 2 + 5 + 2 + 5 cells). The legacy page
at `Mishnah-New/Hebrew/Text/Seder Nezikin/Masechet Avot/Masechet Avot Perek 4.htm`
has 8 matrix rows. Missing from the JSON:

  - Row 5 B subdivisions for all 5 cells (in legacy Table 2 row 1)
  - Row 6: 2 cells, shape [4,4]   (in legacy Table 2 row 2)
  - Row 7: 5 cells, shape [1,2,2,2,1]   (in legacy Table 2 row 3)
  - Row 8: 2 cells, shape [4,4]   (in legacy Table 2 row 4)

Final shape: [[8], [4,4], [1,2,2,2,1], [4,4], [1,2,2,2,1], [4,4], [1,2,2,2,1], [4,4]]

Legacy HTML format:
  - <table border="0" cellpadding="0" cellspacing="0" dir="rtl"> with old MsoNormalTable styling
  - <span class="Subunit">LABEL</span> labels (some nested with inner font-family span; row 6/7/8
    use just <span class="Subunit">6</span> then plain text " א" outside the span)
  - <p class="HMC" dir="rtl"> wraps each cell's content
  - <br/> for line breaks (convert to "\n" runs)
  - Row 5 B subdivision cells in Table 2 row 1 have NO Subunit label — they start with literal "B "
  - No marker spans in this particular page (avot chapters have minimal/no marker annotations)

Output format must match existing JSON shape (cell has label, position, text, runs, markers,
optionally subdivisions).
"""
import json
import os
import re
import sys
import tempfile
import time
from bs4 import BeautifulSoup, NavigableString, Tag

REPO_ROOT = '/sessions/sharp-eloquent-mccarthy/mnt/chaver-site'
JSON_PATH = os.path.join(REPO_ROOT, 'Mishnah-New/English/mishnah_db.json')
PAGE_PATH = os.path.join(
    REPO_ROOT,
    'Mishnah-New/Hebrew/Text/Seder Nezikin/Masechet Avot/Masechet Avot Perek 4.htm',
)

# Marker class name normalization: Horizontal1 → horizontal1, etc.
def normalize_marker(class_name):
    if not class_name:
        return None
    cn = class_name.strip()
    # Known marker prefixes (capitalized or lowercased)
    known_lower = {'horizontal1', 'horizontal2', 'horizontal3',
                   'vertical1', 'closure', 'ciasm1', 'ciasm2', 'internalparallel'}
    if cn.lower() in known_lower:
        return cn.lower()
    # Not a recognized marker → return None (treat as no marker)
    return None


def runs_from_element(elem, skip_first_br_after_label=False):
    """Walk children of a <p> or <td>, emitting {text, marker} runs.

    <br/> becomes a "\n" run.
    <span class="Subunit"> is consumed by the caller (this function expects to start
    after the Subunit span).
    <span class="MarkerName"> becomes a marker run.
    Otherwise plain text is collected as marker=None.
    """
    runs = []
    seen_br_after_label = not skip_first_br_after_label  # if False, will swallow first <br/>
    for child in elem.children:
        if isinstance(child, NavigableString):
            text = str(child)
            if not text:
                continue
            runs.append({'text': text, 'marker': None})
        elif isinstance(child, Tag):
            if child.name == 'br':
                if not seen_br_after_label:
                    seen_br_after_label = True
                    continue
                runs.append({'text': '\n', 'marker': None})
            elif child.name == 'span':
                cls = ' '.join(child.get('class', []))
                marker = normalize_marker(cls)
                inner_text = child.get_text()
                if marker:
                    runs.append({'text': inner_text, 'marker': marker})
                else:
                    # Non-marker span (e.g., a nested style span) → treat its text as plain
                    runs.append({'text': inner_text, 'marker': None})
            else:
                # Some other tag — flatten to text
                inner_text = child.get_text()
                if inner_text:
                    runs.append({'text': inner_text, 'marker': None})
    return runs


def coalesce_runs(runs):
    """Merge adjacent marker=None runs whose text concatenates cleanly.
    Keep marker runs separate. This matches the JSON's existing style where
    same-marker adjacent text often gets merged into single runs.
    """
    out = []
    for r in runs:
        if (out and out[-1].get('marker') is None and r.get('marker') is None):
            # Merge IF both plain text (no marker)
            # But we don't want to merge into a leading "\n" + content pattern
            # Looking at existing JSON: newlines stay as their own runs ("\n" is its own run)
            # And content lines combine with leading "\n" sometimes ("\nכל המקים...")
            # For safety, DON'T coalesce — keep runs separate as they are
            out.append(r)
        else:
            out.append(r)
    return out


def extract_cell_runs(td, has_subunit_label):
    """Extract label and body runs from a <td> in the legacy format.

    Returns (label_str, all_runs_list).

    If has_subunit_label: there's a <span class="Subunit">...</span> at the start of the <p>.
    Otherwise the cell content starts with text (like "B (י)...") — these are Row 5 B
    subdivisions appended to existing cells.
    """
    p = td.find('p')
    if p is None:
        # Sometimes content is directly in TD
        p = td

    runs = []
    label = ''

    # Walk children of <p>
    children = list(p.children)
    i = 0

    if has_subunit_label and children:
        # First non-string child should be <span class="Subunit">
        # Find the Subunit span
        for j, c in enumerate(children):
            if isinstance(c, Tag) and c.name == 'span' and 'Subunit' in c.get('class', []):
                # Extract label
                label = c.get_text().strip()
                # The label could be like "5א\nA" (where inner has font-family wrap around <br/>A)
                # Check for inner content
                # Use direct text content
                inner_text = c.get_text()
                # Add first run: just the label (Hebrew/number portion, before any nested A/B)
                # Special handling: if label contains pattern like "5א\nA" or "5בA" (from inner br),
                # we need to split into multiple runs
                # The Subunit span for row 5 in this page contains: "5א<br/>A"
                # get_text would give "5אA" (without the br as \n)
                # We need to detect the structure

                # Re-parse the inner HTML to find <br/> within the Subunit span
                # Walk children of the Subunit span
                inner_runs = []
                for ic in c.children:
                    if isinstance(ic, NavigableString):
                        s = str(ic)
                        if s:
                            inner_runs.append({'text': s, 'marker': None})
                    elif isinstance(ic, Tag):
                        if ic.name == 'br':
                            inner_runs.append({'text': '\n', 'marker': None})
                        elif ic.name == 'span':
                            # nested style span — recurse
                            for iic in ic.children:
                                if isinstance(iic, NavigableString):
                                    s = str(iic)
                                    if s:
                                        inner_runs.append({'text': s, 'marker': None})
                                elif isinstance(iic, Tag) and iic.name == 'br':
                                    inner_runs.append({'text': '\n', 'marker': None})
                                elif isinstance(iic, Tag):
                                    inner_runs.append({'text': iic.get_text(), 'marker': None})
                        else:
                            inner_runs.append({'text': ic.get_text(), 'marker': None})

                # Append the Subunit's inner runs to our runs list
                # For label, take just the first non-newline run's text (e.g., "5א")
                if inner_runs:
                    first = inner_runs[0]['text']
                    label = first.strip()
                runs.extend(inner_runs)

                # Now look at what's AFTER the Subunit span in the <p>
                # For row 6/7/8 cells: there's " א" text after the Subunit span
                rest_children = children[j+1:]
                # The remaining children form the body
                rest_runs = []
                seen_first_br = False
                for rc in rest_children:
                    if isinstance(rc, NavigableString):
                        s = str(rc)
                        if s:
                            rest_runs.append({'text': s, 'marker': None})
                    elif isinstance(rc, Tag):
                        if rc.name == 'br':
                            rest_runs.append({'text': '\n', 'marker': None})
                        elif rc.name == 'span':
                            cls = ' '.join(rc.get('class', []))
                            marker = normalize_marker(cls)
                            text = rc.get_text()
                            if marker:
                                rest_runs.append({'text': text, 'marker': marker})
                            else:
                                rest_runs.append({'text': text, 'marker': None})
                        else:
                            rest_runs.append({'text': rc.get_text(), 'marker': None})
                runs.extend(rest_runs)
                break
    else:
        # No Subunit label — extract all content as runs
        for c in children:
            if isinstance(c, NavigableString):
                s = str(c)
                if s:
                    runs.append({'text': s, 'marker': None})
            elif isinstance(c, Tag):
                if c.name == 'br':
                    runs.append({'text': '\n', 'marker': None})
                elif c.name == 'span':
                    cls = ' '.join(c.get('class', []))
                    marker = normalize_marker(cls)
                    text = c.get_text()
                    if marker:
                        runs.append({'text': text, 'marker': marker})
                    else:
                        runs.append({'text': text, 'marker': None})
                else:
                    runs.append({'text': c.get_text(), 'marker': None})

    return label, runs


def compose_label(label_text, after_text):
    """For rows 6/7/8: Subunit gives "6", then plain text after is " א" — combine for label.
    Returns normalized label like "6א" (no space).
    """
    combined = (label_text + after_text).strip()
    # Strip any whitespace inside
    return re.sub(r'\s+', '', combined)


def text_from_runs(runs):
    """Concatenate run texts."""
    return ''.join(r['text'] for r in runs)


def markers_summary(runs):
    """List of {type, text} for each marker run, in order."""
    out = []
    for r in runs:
        if r.get('marker'):
            out.append({'type': r['marker'], 'text': r['text']})
    return out


def find_mishnah_num(runs):
    """Find first '(X)' pattern in run texts and return X."""
    full = text_from_runs(runs)
    m = re.search(r'\(([֐-׿]+)\)', full)
    return m.group(1) if m else ''


def build_subdivisions_field(runs):
    """Walk runs, segment by A/B/C/D/E markers, build subdivisions list."""
    SUBDIV = {'A', 'B', 'C', 'D', 'E'}
    # Find marker positions
    markers = [(i, r['text'].strip())
               for i, r in enumerate(runs)
               if r.get('marker') is None and r['text'].strip() in SUBDIV]
    if not markers:
        return []
    subs = []
    for j, (pos, letter) in enumerate(markers):
        end = markers[j + 1][0] if j + 1 < len(markers) else len(runs)
        segment_runs = runs[pos + 1:end]
        # Skip leading whitespace-only run after marker
        while (segment_runs and segment_runs[0].get('marker') is None and
               segment_runs[0]['text'].strip() == ''):
            segment_runs = segment_runs[1:]
        seg_text = text_from_runs(segment_runs).rstrip()
        # Add trailing \n\n to match existing pattern (see avot_4 existing subdivisions)
        if not seg_text.endswith('\n\n'):
            seg_text += '\n\n' if not seg_text.endswith('\n') else '\n'
        subs.append({
            'label': letter,
            'text': seg_text,
            'markers': markers_summary(segment_runs),
            'mishnah_num_he': find_mishnah_num(segment_runs),
        })
    return subs


# ==========================================
# Main extraction
# ==========================================

def main():
    print(f'Reading HTML page: {PAGE_PATH}')
    with open(PAGE_PATH, encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Find tables — first is the chrome table with "Mesechet/logo/Perek" header,
    # actually that's the FIRST table. The content tables are #1 (rows 1-5) and #2 (rows 5b-8)
    # Wait — re-reading: the FIRST <table> is the content table (with the mesechet header row at top
    # then content rows). So there are 2 content tables matching what the spec says.
    all_tables = soup.find_all('table')
    print(f'All <table> elements: {len(all_tables)}')

    # We want the content tables. The first table contains the chapter header at top,
    # then rows 1-5. The second table contains rows 5b-8.
    # Per inspection: there are exactly 2 tables and both are content tables.
    if len(all_tables) != 2:
        raise RuntimeError(f'Expected 2 tables, got {len(all_tables)}')

    table1 = all_tables[0]
    table2 = all_tables[1]

    # Table 2 structure (the missing data):
    #   tr 0: 5 tds — Row 5 B subdivisions (cells WITHOUT Subunit label)
    #   tr 1: 2 tds — Row 6 (cells WITH Subunit label "6" then " א"/" ב")
    #   tr 2: 5 tds — Row 7 (cells WITH Subunit label "7" then " א".." ה")
    #   tr 3: 2 tds — Row 8 (cells WITH Subunit label "8" then " א"/" ב")

    t2_rows = table2.find_all('tr', recursive=False)
    if not t2_rows:
        # tbody wrapping
        tbody = table2.find('tbody')
        t2_rows = tbody.find_all('tr', recursive=False) if tbody else []
    print(f'Table 2 row count: {len(t2_rows)}')

    if len(t2_rows) != 4:
        raise RuntimeError(f'Expected 4 rows in Table 2, got {len(t2_rows)}')

    # ROW 5 B subdivisions (Table 2 row 0): 5 cells, no Subunit
    r5b_tds = t2_rows[0].find_all('td', recursive=False)
    print(f'Row 5 B cells: {len(r5b_tds)}')
    assert len(r5b_tds) == 5, f'Row 5 B: expected 5 cells, got {len(r5b_tds)}'

    r5b_cells = []
    for td in r5b_tds:
        _, runs = extract_cell_runs(td, has_subunit_label=False)
        r5b_cells.append(runs)

    # ROW 6 (Table 2 row 1): 2 cells, shape [4,4]
    r6_tds = t2_rows[1].find_all('td', recursive=False)
    assert len(r6_tds) == 2, f'Row 6: expected 2 cells, got {len(r6_tds)}'

    # ROW 7 (Table 2 row 2): 5 cells, shape [1,2,2,2,1]
    r7_tds = t2_rows[2].find_all('td', recursive=False)
    assert len(r7_tds) == 5, f'Row 7: expected 5 cells, got {len(r7_tds)}'

    # ROW 8 (Table 2 row 3): 2 cells, shape [4,4]
    r8_tds = t2_rows[3].find_all('td', recursive=False)
    assert len(r8_tds) == 2, f'Row 8: expected 2 cells, got {len(r8_tds)}'

    # Helper to extract label/runs for rows 6/7/8 cells
    def extract_labeled_cell(td):
        p = td.find('p')
        children = list(p.children) if p else []
        # Find Subunit span
        label_inner = ''
        label_runs = []
        rest_runs = []
        found_subunit = False
        for j, c in enumerate(children):
            if isinstance(c, Tag) and c.name == 'span' and 'Subunit' in c.get('class', []):
                label_inner = c.get_text().strip()
                # Subunit content is just a number for rows 6/7/8
                label_runs.append({'text': label_inner, 'marker': None})
                found_subunit = True
                # Process rest
                for rc in children[j+1:]:
                    if isinstance(rc, NavigableString):
                        s = str(rc)
                        if s:
                            rest_runs.append({'text': s, 'marker': None})
                    elif isinstance(rc, Tag):
                        if rc.name == 'br':
                            rest_runs.append({'text': '\n', 'marker': None})
                        elif rc.name == 'span':
                            cls = ' '.join(rc.get('class', []))
                            marker = normalize_marker(cls)
                            tx = rc.get_text()
                            if marker:
                                rest_runs.append({'text': tx, 'marker': marker})
                            else:
                                rest_runs.append({'text': tx, 'marker': None})
                        else:
                            rest_runs.append({'text': rc.get_text(), 'marker': None})
                break
        if not found_subunit:
            raise RuntimeError(f'No Subunit found in cell: {td}')

        # rest_runs starts with " א" (or " ב", etc.) then a <br/> then content
        # Combine label_inner + first-rest-run-text-up-to-first-strip to get the label
        # Pattern: label_runs=[{"text":"6"}], rest_runs=[{"text":" א"}, {"text":"\n"}, {"text":"(טז) ..."}]
        # Label should be "6א" (no space)
        label = label_inner
        # Look at first rest run — it starts with " " then a Hebrew letter
        if rest_runs and rest_runs[0].get('marker') is None:
            m = re.match(r'^\s*([א-ה])\s*$', rest_runs[0]['text'])
            if m:
                label = label_inner + m.group(1)

        # Combined runs: label runs + rest runs
        all_runs = label_runs + rest_runs
        return label, all_runs

    row6_cells = [extract_labeled_cell(td) for td in r6_tds]
    row7_cells = [extract_labeled_cell(td) for td in r7_tds]
    row8_cells = [extract_labeled_cell(td) for td in r8_tds]

    print(f'\nExtracted:')
    print(f'  Row 5 B: 5 cells, total {sum(len(text_from_runs(c)) for c in r5b_cells)} chars')
    for label, runs in row6_cells:
        print(f'  Row 6 cell: label={label!r}  {len(text_from_runs(runs))} chars')
    for label, runs in row7_cells:
        print(f'  Row 7 cell: label={label!r}  {len(text_from_runs(runs))} chars')
    for label, runs in row8_cells:
        print(f'  Row 8 cell: label={label!r}  {len(text_from_runs(runs))} chars')

    # ==========================================
    # Patch the JSON
    # ==========================================
    print(f'\nLoading JSON: {JSON_PATH}')
    with open(JSON_PATH, encoding='utf-8') as f:
        db = json.load(f)

    ch = db['avot_4']

    # ROW 5: Append B subdivision runs to each cell
    # The existing row 5 cells have A subdivision content. We append B runs.
    # Pattern from megillah_1 row 2 cell 0: existing content ends with last subdivision content (no extra \n),
    # then "\n" run, then "B" run, then " " run, then B content runs.
    # But avot_4 cell 0 currently has trailing \n\n. We'll keep those and just append B.
    row5 = ch['rows'][4]
    for idx, b_runs in enumerate(r5b_cells):
        cell = row5['cells'][idx]
        # Strip leading "B " from b_runs since we'll emit "B" as a standalone marker run
        # b_runs[0] is typically {"text": "B (י) רבי מאיר אומר", "marker": null}
        # We need to convert to: "B" marker run, " " space run, "(י) רבי מאיר אומר" content run, etc.
        if not b_runs:
            continue
        first = b_runs[0]
        m = re.match(r'^([A-E])\s+(.*)$', first['text'], re.DOTALL)
        if m:
            letter = m.group(1)
            remainder = m.group(2)
            transformed = [
                {'text': letter, 'marker': None},
                {'text': ' ', 'marker': None},
                {'text': remainder, 'marker': None},
            ] + b_runs[1:]
        else:
            transformed = b_runs  # fallback

        # Append to existing cell runs
        cell['runs'].extend(transformed)
        # Update cell text
        cell['text'] = text_from_runs(cell['runs'])
        # Rebuild subdivisions field from full runs
        cell['subdivisions'] = build_subdivisions_field(cell['runs'])
        # Markers list (no markers in this page, but for completeness)
        cell['markers'] = markers_summary(cell['runs'])

    # NEW ROWS 6, 7, 8
    def make_row(row_num, cells_data, shape):
        """Build a row dict matching the existing JSON structure."""
        cells = []
        col_pos = 1
        for ci, (label, runs) in enumerate(cells_data):
            colspan = shape[ci]
            cell = {
                'label': label,
                'position': {'row': row_num, 'col': col_pos, 'colspan': colspan},
                'text': text_from_runs(runs),
                'runs': runs,
                'markers': markers_summary(runs),
            }
            subs = build_subdivisions_field(runs)
            if subs:
                cell['subdivisions'] = subs
            cells.append(cell)
            col_pos += colspan
        return {'row_num': row_num, 'cells': cells}

    # Existing row entries don't have 'row_num' field — check
    has_row_num = 'row_num' in ch['rows'][0]

    row6 = make_row(6, row6_cells, [4, 4])
    row7 = make_row(7, row7_cells, [1, 2, 2, 2, 1])
    row8 = make_row(8, row8_cells, [4, 4])

    if not has_row_num:
        # remove row_num key to match existing format
        for r in (row6, row7, row8):
            r.pop('row_num', None)

    ch['rows'].append(row6)
    ch['rows'].append(row7)
    ch['rows'].append(row8)

    # Update shape
    ch['shape'] = [[8], [4,4], [1,2,2,2,1], [4,4], [1,2,2,2,1], [4,4], [1,2,2,2,1], [4,4]]

    # ==========================================
    # Verify
    # ==========================================
    # Count total Hebrew chars in avot_4
    HEB_RE = re.compile(r'[א-׿]')
    total_chars = sum(len(HEB_RE.findall(r['text']))
                      for row in ch['rows']
                      for cell in row['cells']
                      for r in cell['runs'])
    print(f'\nPost-patch avot_4 stats:')
    print(f'  rows: {len(ch["rows"])}')
    print(f'  shape: {ch["shape"]}')
    print(f'  total Hebrew chars: {total_chars}')

    # Verify all 22 mishnayot present
    full_text = ' '.join(cell['text']
                         for row in ch['rows']
                         for cell in row['cells'])
    HEB_MISHNAH = ['א','ב','ג','ד','ה','ו','ז','ח','ט','י','יא','יב','יג','יד','טו','טז','יז','יח','יט','כ','כא','כב']
    found = []
    missing = []
    for m in HEB_MISHNAH:
        if f'({m})' in full_text:
            found.append(m)
        else:
            missing.append(m)
    print(f'  Mishnayot found: {len(found)}/22')
    if missing:
        print(f'  MISSING: {missing}')

    # ==========================================
    # Atomic write
    # ==========================================
    print(f'\nWriting patched JSON...')
    data = json.dumps(db, ensure_ascii=False, indent=2)
    dir_ = os.path.dirname(JSON_PATH)
    fd, tmp = tempfile.mkstemp(prefix='.mishdb-', dir=dir_)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, JSON_PATH)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise
    print(f'  Wrote {len(data.encode("utf-8")):,} bytes')

    # Verify reparse
    with open(JSON_PATH, encoding='utf-8') as f:
        verify = json.load(f)
    assert 'avot_4' in verify
    assert len(verify['avot_4']['rows']) == 8
    print(f'  JSON re-parses cleanly')

    return 0 if not missing else 1


if __name__ == '__main__':
    sys.exit(main())
