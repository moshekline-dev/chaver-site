"""
Mishnah Structural Marker Extractor — v2

Extracts structural markers from 'The Whole Structured Mishnah for pdf.docx'
into JSON entries compatible with mishnah_db.json.

The Word document encodes structural markers via named character styles (not
direct colors). Each style maps to a CSS class used on the chaver.com site:

    Horizontal10      -> horizontal1     (blue #3399FF)
    Horizontal2       -> horizontal2     (teal #008080)
    Horizontal3       -> horizontal3     (dark cyan #008B8B)
    Vertical1         -> vertical1       (brown #8B4513)
    InternalParallel  -> internalparallel (dark red #C00000)
    Closure           -> closure         (purple #77206D)
    Ciasm1            -> ciasm1          (violet #7030A0)
    Ciasm2            -> ciasm2          (violet #7030A0, underlined)

Usage:
    python mishnah_extractor_v2.py <docx_path> [chapter_key] [output_path]

Examples:
    python mishnah_extractor_v2.py "The Whole Structured Mishnah for pdf.docx" megillah_1 out.json
    python mishnah_extractor_v2.py "The Whole Structured Mishnah for pdf.docx" --all all.json
"""

__version__ = "2.0"

import json, re, sys, os
from typing import Dict, List, Optional, Any

try:
    from docx import Document
    from docx.oxml.ns import qn
except ImportError:
    print("ERROR: python-docx required. pip install python-docx")
    sys.exit(1)


STYLE_TO_MARKER: Dict[str, str] = {
    "Horizontal10": "horizontal1",
    "Horizontal2": "horizontal2",
    "Horizontal3": "horizontal3",
    "Vertical1": "vertical1",
    "InternalParallel": "internalparallel",
    "Closure": "closure",
    "Ciasm1": "ciasm1",
    "Ciasm2": "ciasm2",
}

SUBUNIT_STYLE = "Subunit"


def get_run_style(run_el) -> Optional[str]:
    """Get character style name from a run XML element."""
    rpr = run_el.find(qn('w:rPr'))
    if rpr is None:
        return None
    rstyle = rpr.find(qn('w:rStyle'))
    if rstyle is None:
        return None
    return rstyle.get(qn('w:val'))


def extract_run_text(run_el) -> str:
    """Extract text including <w:br/>, <w:tab/>, <w:cr/> from a run."""
    parts = []
    for child in run_el:
        tag = child.tag.split('}')[-1]
        if tag == 't':
            parts.append(child.text or '')
        elif tag == 'br':
            parts.append('\n')
        elif tag == 'tab':
            parts.append('\t')
        elif tag == 'cr':
            parts.append('\n')
    return ''.join(parts)


def extract_chapter(table) -> Dict:
    """Extract a chapter's structure and markers from a Word table."""
    rows_data = []
    for row_idx, row in enumerate(table.rows):
        if row_idx == 0:
            continue
        cells_data = []
        grid_col = 1
        tr_el = row._tr
        seen_tcs = set()
        for tc in tr_el.findall(qn('w:tc')):
            tc_id = id(tc)
            if tc_id in seen_tcs:
                continue
            seen_tcs.add(tc_id)
            tc_pr = tc.find(qn('w:tcPr'))
            colspan = 1
            if tc_pr is not None:
                gs = tc_pr.find(qn('w:gridSpan'))
                if gs is not None:
                    colspan = int(gs.get(qn('w:val'), '1'))
            cell_runs = []
            for para in tc.findall(qn('w:p')):
                for run_el in para.findall(qn('w:r')):
                    style = get_run_style(run_el)
                    text = extract_run_text(run_el)
                    if not text:
                        continue
                    marker = STYLE_TO_MARKER.get(style) if style else None
                    cell_runs.append({"text": text, "marker": marker, "_style": style})
            if not cell_runs:
                grid_col += colspan
                continue
            cell_dict = _parse_cell(cell_runs, row_idx, grid_col, colspan)
            if cell_dict:
                cells_data.append(cell_dict)
            grid_col += colspan
        if cells_data:
            rows_data.append({"row_num": row_idx, "cells": cells_data})
    shape = [[c['position']['colspan'] for c in r['cells']] for r in rows_data]
    header_cells = table.rows[0].cells
    tractate_he = header_cells[0].text.strip()
    chapter_text = header_cells[-1].text.strip()
    chapter_he_match = re.search(r'פרק\s+(.+)', chapter_text)
    chapter_he = chapter_he_match.group(1).strip() if chapter_he_match else ""
    return {"tractate_he": tractate_he, "chapter_he": chapter_he, "shape": shape, "rows": rows_data}


def _parse_cell(runs, row_num, grid_col, colspan):
    """Parse a cell's runs into a structured cell dict."""
    if not runs:
        return None
    label = ""
    if runs[0].get('_style') == SUBUNIT_STYLE:
        label = runs[0]['text'].strip()
    elif runs:
        first = runs[0]['text'].strip()
        if re.match(r'^\d+[א-ת]$', first):
            label = first
    output_runs = [{"text": r["text"], "marker": r["marker"]} for r in runs]
    markers = [{"type": r["marker"], "text": r["text"]} for r in runs if r["marker"]]
    full_text = ''.join(r['text'] for r in runs)
    subdivisions = _detect_subdivisions(runs)
    cell_dict = {
        "label": label,
        "position": {"row": row_num, "col": grid_col, "colspan": colspan},
        "text": full_text,
        "runs": output_runs,
        "markers": markers,
    }
    if subdivisions:
        cell_dict["subdivisions"] = subdivisions
    return cell_dict


def _detect_subdivisions(runs):
    """Detect A/B/C subdivisions within a cell."""
    sub_indices = []
    for i, r in enumerate(runs):
        if (r.get('_style') == SUBUNIT_STYLE and
            re.match(r'^[A-Z]$', r['text'].strip())):
            sub_indices.append(i)
    if not sub_indices:
        return []
    subdivisions = []
    for idx, sub_idx in enumerate(sub_indices):
        sub_label = runs[sub_idx]['text'].strip()
        end_idx = sub_indices[idx + 1] if idx + 1 < len(sub_indices) else len(runs)
        start = sub_idx + 1
        if start < end_idx and runs[start]['text'] == ' ' and runs[start]['marker'] is None:
            start += 1
        sub_text = ''.join(r['text'] for r in runs[start:end_idx])
        sub_markers = [{"type": r["marker"], "text": r["text"]}
                       for r in runs[start:end_idx] if r["marker"]]
        mishnah_num = None
        num_match = re.match(r'\(?([א-ת]+)\)?', sub_text.lstrip())
        if num_match:
            mishnah_num = num_match.group(1)
        subdivisions.append({
            "label": sub_label, "text": sub_text,
            "markers": sub_markers, "mishnah_num_he": mishnah_num
        })
    return subdivisions


HEBREW_LETTERS = "אבגדהוזחטיכלמנסעפצקרשת"


def _hebrew_chapter_num_to_str(num):
    """Convert chapter number (1-22) to Hebrew letter."""
    if 1 <= num <= 22:
        return HEBREW_LETTERS[num - 1]
    return str(num)


TRACTATE_NAMES = {
    "מגילה": "megillah",
    "מגלה": "megillah",
    "ברכות": "berakhot",
    "שבת": "shabbat",
    "עירובין": "eruvin",
    "פסחים": "pesachim",
    "שקלים": "shekalim",
    "יומא": "yoma",
    "סוכה": "sukkah",
    "ביצה": "beitzah",
    "ראש השנה": "rosh_hashana",
    "תענית": "taanit",
    "מועד קטן": "moed_katan",
    "חגיגה": "chagigah",
    "יבמות": "yevamot",
    "כתובות": "ketubot",
    "נדרים": "nedarim",
    "נזיר": "nazir",
    "סוטה": "sotah",
    "גיטין": "gittin",
    "קידושין": "kiddushin",
    "בבא קמא": "bava_kamma",
    "בבא מציעא": "bava_metzia",
    "בבא בתרא": "bava_batra",
    "סנהדרין": "sanhedrin",
    "מכות": "makkot",
    "שבועות": "shevuot",
    "עדויות": "eduyot",
    "עבודה זרה": "avodah_zarah",
    "אבות": "avot",
    "הוריות": "horayot",
    "זבחים": "zevachim",
    "מנחות": "menachot",
    "חולין": "chullin",
    "בכורות": "bekhorot",
    "ערכין": "arakhin",
    "תמורה": "temurah",
    "כריתות": "keritot",
    "מעילה": "meilah",
    "תמיד": "tamid",
    "מדות": "middot",
    "קנים": "kinnim",
    "כלים": "kelim",
    "אהלות": "ohalot",
    "נגעים": "negaim",
    "פרה": "parah",
    "טהרות": "toharot",
    "מקואות": "mikvaot",
    "נדה": "niddah",
    "מכשירין": "makhshirin",
    "זבים": "zavim",
    "טבול יום": "tevul_yom",
    "ידים": "yadayim",
    "עוקצין": "uktzin",
    "פאה": "peah",
    "דמאי": "demai",
    "כלאים": "kilayim",
    "שביעית": "sheviit",
    "תרומות": "terumot",
    "מעשרות": "maasrot",
    "מעשר שני": "maaser_sheni",
    "חלה": "challah",
    "ערלה": "orlah",
    "בכורים": "bikkurim",
}


def _match_tractate(hebrew_text):
    """Match Hebrew tractate text to English key."""
    for heb, eng in TRACTATE_NAMES.items():
        if heb in hebrew_text:
            return eng
    return None


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    docx_path = sys.argv[1]
    if not os.path.exists(docx_path):
        print(f"ERROR: File not found: {docx_path}")
        sys.exit(1)
    print(f"Loading: {docx_path}")
    doc = Document(docx_path)
    print(f"  Tables: {len(doc.tables)}")

    if len(sys.argv) >= 3 and sys.argv[2] == '--all':
        output_path = sys.argv[3] if len(sys.argv) > 3 else 'all_chapters.json'
        print('Extracting all chapters...')
        results = {}
        for table in doc.tables:
            if len(table.rows) < 2:
                continue
            hcells = table.rows[0].cells
            if len(hcells) < 3:
                continue
            c0 = hcells[0].text.strip()
            cl = hcells[-1].text.strip()
            if 'מסכת' in c0 and 'פרק' in cl:
                chapter_data = extract_chapter(table)
                key = f"{c0}|{cl}"
                results[key] = chapter_data
        print(f"  Found {len(results)} chapters")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"  Written to: {output_path}")

    elif len(sys.argv) >= 3:
        chapter_key = sys.argv[2]
        output_path = sys.argv[3] if len(sys.argv) > 3 else f'{chapter_key}_extracted.json'
        parts = chapter_key.rsplit('_', 1)
        if len(parts) != 2:
            print(f"ERROR: Invalid key: {chapter_key}")
            sys.exit(1)
        tractate_name = parts[0]
        chapter_num = int(parts[1])
        chapter_he = _hebrew_chapter_num_to_str(chapter_num)
        target_perek = 'פרק ' + chapter_he
        print(f"  Looking for: {chapter_key} (ch. {chapter_he})")
        found_table = None
        for table in doc.tables:
            if len(table.rows) < 2:
                continue
            hcells = table.rows[0].cells
            if len(hcells) < 3:
                continue
            c0 = hcells[0].text.strip()
            cl = hcells[-1].text.strip()
            if 'מסכת' in c0 and target_perek in cl:
                eng = _match_tractate(c0)
                if eng and eng == tractate_name:
                    found_table = table
                    print(f"  Found: {c0} / {cl}")
                    break
        if found_table is None:
            print(f"ERROR: Table not found for {chapter_key}")
            sys.exit(1)
        chapter_data = extract_chapter(found_table)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(chapter_data, f, ensure_ascii=False, indent=2)
        total_m = sum(len(c['markers']) for r in chapter_data['rows'] for c in r['cells'])
        total_c = sum(len(r['cells']) for r in chapter_data['rows'])
        sub_c = sum(1 for r in chapter_data['rows'] for c in r['cells'] if c.get('subdivisions'))
        print(f"  Cells: {total_c}, Markers: {total_m}, Subdivided: {sub_c}")
        print(f"  Written to: {output_path}")
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == '__main__':
    main()
