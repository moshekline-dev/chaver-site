"""
Set 2 (Figs 8, 9, 10): the threads and the complete grid.
Uses the Full Torah Map palette retained from Set 1.
"""
import sys
sys.path.insert(0, '/home/claude')
from fig_utils import *

# ============================================================
# Unit color mappings (from Full Torah Map)
# ============================================================
GEN_UCOLOR = {
    1: LIGHT_CYAN, 2: LIGHT_CYAN, 3: LIGHT_CYAN,
    4: INDEP_FILL,
    5: LIGHT_GREEN, 6: LIGHT_PERI, 7: LIGHT_GREEN, 8: LIGHT_PERI,
    9: LIGHT_GREEN, 10: LIGHT_PERI,
    11: LIGHT_PERI, 12: LIGHT_GREEN, 13: LIGHT_PERI, 14: LIGHT_GREEN,
    15: LIGHT_PERI, 16: LIGHT_GREEN,
    17: LIGHT_CYAN, 18: LIGHT_CYAN, 19: LIGHT_CYAN,
}
DEUT_UCOLOR = {
    1: LIGHT_CYAN, 3: LIGHT_CYAN, 5: LIGHT_CYAN,
    2: LIGHT_GREEN, 4: LIGHT_GREEN, 6: LIGHT_GREEN,
    7: LIGHT_GREEN, 8: LIGHT_GREEN, 9: LIGHT_GREEN,
    10: LIGHT_CYAN, 11: LIGHT_CYAN, 12: LIGHT_CYAN,
    13: INDEP_FILL,
}
LEV_COL_COLOR = {
    # Map Lev column letter to its ring color
    'A': LIGHT_CYAN,  'B': LIGHT_GREEN, 'C': IMPURE_GRAY,
    'D': LIGHT_PERI,  'E': None,        'F': LIGHT_PERI,
    'G': LIGHT_GREEN, 'H': LIGHT_CYAN,
}

# ============================================================
# FIGURE 8: Horizontal thread - 19 columns RTL
# Reading order (RTL): Genesis (right, east) -> Leviticus (center) -> Deut (left, west)
# Genesis 7 cols (RTL: rightmost is U1 col, leftmost is U17 col)
# Lev 7 cols (impurities removed): A B D E F G H
# Deut 5 cols: 4 triads + U13 independent
# ============================================================
def fig8():
    CW, CH = 0.62, 0.62
    COLS, ROWS = 19, 3
    ML, MR, BOT, TOP = 2.4, 2.4, 1.9, 1.8
    GW, GH = COLS*CW, ROWS*CH
    FW, FH = ML+GW+MR, BOT+GH+TOP
    fig, ax = make_fig(FW, FH)

    # Helper: place a 1-indexed column index c (1..19) at x-position.
    # c=1 is leftmost (Deut U13 area, the western end).
    # c=19 is rightmost (Genesis primordial = U1 area, the eastern end).
    def cx(c): return ML + (c-1)*CW
    def ry(r): return BOT + GH - (r+1)*CH   # r=0 top row

    # Column allocation (left to right on page, but reading goes RIGHT to LEFT
    # in the Hebrew sense):
    #   cols 1-5: Deuteronomy (leftmost = Deut col 5 = independent U13; rightmost-of-Deut = col 1)
    #             Reading RTL: Deut col 1 is encountered first (after Lev's leftmost), col 5 last.
    #             In Deut's matrix: col 5 = U13 (independent). When laid into the
    #             horizontal thread with Gen on the right, the Deut block should
    #             read "first triad" on the right of the Deut block (adjacent to
    #             Lev) and "U13" on the left (western end). So Deut col 1 (first
    #             triad) -> page col 5; Deut col 5 (U13) -> page col 1.
    # cols 6-12: Leviticus 7 cols (A=H, B=G, D=F, E in the middle).
    #            RTL: A is east-most of Lev = page col 12 (rightmost of Lev block);
    #                 H is west-most of Lev = page col 6.
    #            Page col 9 = Lev col E (the pivot)? Let's count:
    #              page col 6  = Lev H
    #              page col 7  = Lev G
    #              page col 8  = Lev F
    #              page col 9  = Lev E (pivot)
    #              page col 10 = Lev D
    #              page col 11 = Lev B
    #              page col 12 = Lev A
    # cols 13-19: Genesis 7 cols.
    #            Gen "col 1" (Primordial, U1-3) is the east-most -> page col 19.
    #            Gen "col 7" (Joseph, U17-19) is adjacent to Lev's east edge -> page col 13.
    PIVOT_C = 11  # Page column of Lev E (the pivot)

    # Build a list: page_col -> ('book', book_internal_col_index, units_in_that_col)
    # Then color them.

    # Genesis units: each Genesis column is a triad (rows 1,2,3) except col 2 (Babel,
    # only Row 2 = U4)
    # Gen internal col 1 (Primordial): U1, U2, U3
    # Gen internal col 2 (Babel):       (None, U4, None)
    # Gen internal col 3 (Abraham-A):   U5, U7, U9
    # Gen internal col 4 (Abraham-B):   U6, U8, U10
    # Gen internal col 5 (Jacob-A):     U11, U13, U15
    # Gen internal col 6 (Jacob-B):     U12, U14, U16
    # Gen internal col 7 (Joseph):      U17, U18, U19
    gen_cols_internal = {
        1: (1, 2, 3),     # Primordial
        2: (None, 4, None),
        3: (5, 7, 9),
        4: (6, 8, 10),
        5: (11, 13, 15),
        6: (12, 14, 16),
        7: (17, 18, 19),
    }
    # Map Gen internal col -> page col (eastmost = page col 19)
    # Gen internal 1 (Primordial, east) -> page 19
    # Gen internal 7 (Joseph, west, adjacent to Lev) -> page 13
    gen_internal_to_page = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7}

    # Deut units (from Full Map: 5 internal cols)
    # Deut internal col 1: U1, U3, U5 (cyan)
    # Deut internal col 2: U2, U4, U6 (green)
    # Deut internal col 3: U7, U8, U9 (green)
    # Deut internal col 4: U10, U11, U12 (cyan)
    # Deut internal col 5: U13 (indep) at row 2 only
    deut_cols_internal = {
        1: (1, 3, 5),
        2: (2, 4, 6),
        3: (7, 8, 9),
        4: (10, 11, 12),
        5: (None, 13, None),
    }
    # Deut internal col 1 (east, adjacent to Lev) -> page col 5
    # Deut internal col 5 (west, U13 at the end) -> page col 1
    deut_internal_to_page = {1: 15, 2: 16, 3: 17, 4: 18, 5: 19}

    # Leviticus: 7 cols (no impurities). Each col is 3 rows.
    # Lev col A: U1, U2, U3 (cyan, outer)
    # Lev col B: U4, U5, U6 (green, middle)
    # Lev col D: U10, U11, U12 (peri, inner)
    # Lev col E: (None, U13, None) at row 2 only — focal
    # Lev col F: U14, U15, U16 (peri, inner)
    # Lev col G: U17, U18, U19 (green, middle)
    # Lev col H: U20, U21, U22 (cyan, outer)
    lev_cols_internal = {
        'A': (1, 2, 3),
        'B': (4, 5, 6),
        'D': (10, 11, 12),
        'E': (None, 13, None),
        'F': (14, 15, 16),
        'G': (17, 18, 19),
        'H': (20, 21, 22),
    }
    # Mapping: Lev internal letter -> page col
    lev_internal_to_page = {'A': 8, 'B': 9, 'D': 10, 'E': 11, 'F': 12, 'G': 13, 'H': 14}

    # Lev unit -> Full Map color
    LEV_UCOLOR = {
        1: LIGHT_CYAN, 2: LIGHT_CYAN, 3: LIGHT_CYAN,
        4: LIGHT_GREEN, 5: LIGHT_GREEN, 6: LIGHT_GREEN,
        10: LIGHT_PERI, 11: LIGHT_PERI, 12: LIGHT_PERI,
        13: INDEP_FILL,
        14: LIGHT_PERI, 15: LIGHT_PERI, 16: LIGHT_PERI,
        17: LIGHT_GREEN, 18: LIGHT_GREEN, 19: LIGHT_GREEN,
        20: LIGHT_CYAN, 21: LIGHT_CYAN, 22: LIGHT_CYAN,
    }

    def place_unit(page_col, page_row, u, color):
        x = cx(page_col)
        y = ry(page_row)
        if color == INDEP_FILL:
            draw_cell(ax, x, y, CW, CH, color=INDEP_FILL, ec=INDEP_BORDER, lw=1.4)
        else:
            draw_cell(ax, x, y, CW, CH, color=color, ec=LIGHT_GRID, lw=0.5)
        label(ax, x+CW/2, y+CH/2, str(u), font=SANS_BOLD, size=10)

    def place_empty(page_col, page_row):
        x = cx(page_col)
        y = ry(page_row)
        draw_cell(ax, x, y, CW, CH, color=BG, ec=LIGHT_GRID, lw=0.5)

    # Genesis
    for ic, units in gen_cols_internal.items():
        pc = gen_internal_to_page[ic]
        for r, u in enumerate(units):
            if u is None:
                place_empty(pc, r)
            else:
                place_unit(pc, r, u, GEN_UCOLOR[u])

    # Leviticus
    for letter, units in lev_cols_internal.items():
        pc = lev_internal_to_page[letter]
        for r, u in enumerate(units):
            if u is None:
                place_empty(pc, r)
            else:
                place_unit(pc, r, u, LEV_UCOLOR[u])

    # Deuteronomy
    for ic, units in deut_cols_internal.items():
        pc = deut_internal_to_page[ic]
        for r, u in enumerate(units):
            if u is None:
                place_empty(pc, r)
            else:
                place_unit(pc, r, u, DEUT_UCOLOR[u])

    # Book frames (one per book, using draw_book_frame logic)
    # Genesis: page cols 13-19
    gen_x0  = cx(1);  gen_w  = 7*CW
    lev_x0  = cx(8);  lev_w  = 7*CW
    deut_x0 = cx(15); deut_w = 5*CW

    # Soft tint backgrounds beneath (zorder=1)
    import matplotlib.patches as mpatches
    for x0, w, book in [(gen_x0, gen_w, 'genesis'),
                         (lev_x0, lev_w, 'leviticus'),
                         (deut_x0, deut_w, 'deuteronomy')]:
        ax.add_patch(mpatches.Rectangle(
            (x0-0.04, BOT-0.04), w+0.08, GH+0.08,
            lw=0, fc=BOOK_BG_TINT[book], zorder=1))
        ax.add_patch(mpatches.Rectangle(
            (x0-0.04, BOT-0.04), w+0.08, GH+0.08,
            lw=2.4, ec=BOOK_FRAME[book], fc='none', zorder=4))

    # Book labels below
    label(ax, gen_x0 + gen_w/2,  BOT-0.22, 'Genesis',
          font=SANS_BOLD, size=11, va='top', color=BOOK_FRAME['genesis'])
    label(ax, lev_x0 + lev_w/2,  BOT-0.22, 'Leviticus',
          font=SANS_BOLD, size=11, va='top', color=BOOK_FRAME['leviticus'])
    label(ax, deut_x0 + deut_w/2, BOT-0.22, 'Deuteronomy',
          font=SANS_BOLD, size=11, va='top', color=BOOK_FRAME['deuteronomy'])

    # Orientation note beneath the grid
    label(ax, ML+GW/2, BOT-0.62,
          'Leviticus is oriented like Genesis up to Unit 13, '
          'then like Deuteronomy from Unit 13 onward.',
          size=10, va='top', color=TXT_SOFT)



    top = BOT + GH

    # Row labels — Gen is on the left (pre-pivot), Deut on the right (post-pivot)
    label(ax, 0.2, ry(0)+CH/2, 'Row 1  transcendent',
          size=9, ha='left', color=TXT_SOFT)
    label(ax, 0.2, ry(1)+CH/2, 'Row 2  interface',
          size=9, ha='left', color=TXT_SOFT)
    label(ax, 0.2, ry(2)+CH/2, 'Row 3  earthly',
          size=9, ha='left', color=TXT_SOFT)

    label(ax, ML+GW+0.20, ry(0)+CH/2, 'Row 1  earthly',
          size=9, ha='left', color=TXT_SOFT)
    label(ax, ML+GW+0.20, ry(1)+CH/2, 'Row 2  interface',
          size=9, ha='left', color=TXT_SOFT)
    label(ax, ML+GW+0.20, ry(2)+CH/2, 'Row 3  transcendent',
          size=9, ha='left', color=TXT_SOFT)

    # Mark the pivot (Lev U13) with an arrow/label above
    pivot_x = cx(PIVOT_C) + CW/2
    label(ax, pivot_x, top+0.12, 'pivot', size=10, va='bottom',
          color=INDEP_BORDER, font=SANS_BOLD)

    label(ax, FW/2, FH-0.15,
          'Figure 8.  The Horizontal Thread: 19 Columns',
          font=SERIF_BOLD, size=14, va='top')
    save(fig, 'fig-08-horizontal-thread')


# ============================================================
# FIGURE 9: Vertical thread - 19 rows
# Each book is drawn as its full 2-D unit grid (per the prior Fig 10 work).
# Exodus 9x5, Lev 3x7 (no impurities col), Numbers 5x5.
# Register dividers between books span the widest book's width (Lev = 7).
# ============================================================
def fig9():
    CELL = 0.42
    FIELD = 7   # widest book (Lev)
    ML, MR, BOT, TOP = 2.7, 2.7, 0.5, 1.15
    GW = FIELD * CELL
    TOTAL_ROWS = 19
    GH = TOTAL_ROWS * CELL
    FW, FH = ML+GW+MR, BOT+GH+TOP
    fig, ax = make_fig(FW, FH)

    def colx(c): return ML + (c-1)*CELL   # c 1-indexed
    def rowy(r): return BOT + GH - r*CELL

    # ---------------- Exodus (rows 1-9, 5 cols centered in 7-col field) ----------------
    EX_COLS = 5
    ex_c0 = (FIELD - EX_COLS) // 2 + 1   # 2
    def ex_field_col(c): return ex_c0 + c - 1

    # Exodus unit colors (Full Map): U1-U9 = orange, U10 = indep, U11-U19 = mint
    EX_UCOLOR = {
        1: ORANGE_CELL, 2: ORANGE_CELL, 3: ORANGE_CELL, 4: ORANGE_CELL,
        5: INDEP_FILL,
        6: ORANGE_CELL, 7: ORANGE_CELL, 8: ORANGE_CELL, 9: ORANGE_CELL,
        10: INDEP_FILL,
        11: MINT_CELL, 12: MINT_CELL, 13: MINT_CELL, 14: MINT_CELL,
        15: INDEP_FILL,
        16: MINT_CELL, 17: MINT_CELL, 18: MINT_CELL, 19: MINT_CELL,
    }
    # Empty cells
    for r in range(1, 10):
        for c in range(1, EX_COLS+1):
            fc = ex_field_col(c)
            draw_cell(ax, colx(fc), rowy(r), CELL, CELL,
                      color=BG, ec=LIGHT_GRID, lw=0.5)
    # Outer left col (Ex internal col 1): U1-U4 rows 1-4, U11-U14 rows 6-9
    left  = [(1,1),(2,2),(3,3),(4,4),(11,6),(12,7),(13,8),(14,9)]
    right = [(6,1),(7,2),(8,3),(9,4),(16,6),(17,7),(18,8),(19,9)]
    for u, r in left:
        fc = ex_field_col(1)
        draw_cell(ax, colx(fc), rowy(r), CELL, CELL, color=EX_UCOLOR[u],
                  ec=LIGHT_GRID, lw=0.5)
    for u, r in right:
        fc = ex_field_col(5)
        draw_cell(ax, colx(fc), rowy(r), CELL, CELL, color=EX_UCOLOR[u],
                  ec=LIGHT_GRID, lw=0.5)
    # Independents at Ex col 3 with half-row offsets
    y5  = rowy(2) - CELL/2
    y10 = rowy(5)
    y15 = rowy(7) - CELL/2
    fc3 = ex_field_col(3)
    for y in [y5, y10, y15]:
        draw_cell(ax, colx(fc3), y, CELL, CELL, color=INDEP_FILL,
                  ec=INDEP_BORDER, lw=0.9)

    # Exodus frame
    import matplotlib.patches as mpatches
    ax.add_patch(mpatches.Rectangle(
        (colx(ex_c0)-0.05, rowy(9)-0.05), EX_COLS*CELL+0.10, 9*CELL+0.10,
        lw=0, fc=BOOK_BG_TINT['exodus'], zorder=1))
    ax.add_patch(mpatches.Rectangle(
        (colx(ex_c0)-0.05, rowy(9)-0.05), EX_COLS*CELL+0.10, 9*CELL+0.10,
        lw=2.0, ec=BOOK_FRAME['exodus'], fc='none', zorder=4))
    label(ax, colx(ex_c0)+EX_COLS*CELL/2, rowy(5)+CELL/2, 'Exodus',
          font=SERIF_BOLD, size=12, color=BOOK_FRAME['exodus'])
    label(ax, ML+GW+0.18, rowy(5)+CELL/2, '9 rows', size=9, ha='left',
          color=TXT_SOFT)

    # Divider 1 (row 10)
    draw_cell(ax, ML, rowy(10), GW, CELL, color=DIVIDER, lw=0)
    label(ax, 0.2, rowy(10)+CELL/2, 'register divider', size=9, ha='left',
          color=DIVIDER)
    label(ax, ML+GW+0.18, rowy(10)+CELL/2, '1 row', size=9, ha='left',
          color=TXT_SOFT)

    # Leviticus (rows 11-13, 7 cols full field) — no impurities col
    # Lev units in the 7-col layout (impurities removed):
    #  col 1 (A): U1,U2,U3 cyan
    #  col 2 (B): U4,U5,U6 green
    #  col 3 (D): U10,U11,U12 peri
    #  col 4 (E): (None, U13, None) focal/empty
    #  col 5 (F): U14,U15,U16 peri
    #  col 6 (G): U17,U18,U19 green
    #  col 7 (H): U20,U21,U22 cyan
    LEV_COLS_LAYOUT = [
        (1,  [1,2,3],     LIGHT_CYAN),
        (2,  [4,5,6],     LIGHT_GREEN),
        (3,  [10,11,12],  LIGHT_PERI),
        (4,  [None,13,None], None),   # focal column
        (5,  [14,15,16],  LIGHT_PERI),
        (6,  [17,18,19],  LIGHT_GREEN),
        (7,  [20,21,22],  LIGHT_CYAN),
    ]
    for c, units, color in LEV_COLS_LAYOUT:
        for i, u in enumerate(units):
            r_global = 11 + i
            if u is None:
                draw_cell(ax, colx(c), rowy(r_global), CELL, CELL,
                          color=BG, ec=LIGHT_GRID, lw=0.5)
            elif u == 13:
                draw_cell(ax, colx(c), rowy(r_global), CELL, CELL,
                          color=INDEP_FILL, ec=INDEP_BORDER, lw=0.9)
            else:
                draw_cell(ax, colx(c), rowy(r_global), CELL, CELL,
                          color=color, ec=LIGHT_GRID, lw=0.5)
    # Lev frame
    ax.add_patch(mpatches.Rectangle(
        (colx(1)-0.05, rowy(13)-0.05), FIELD*CELL+0.10, 3*CELL+0.10,
        lw=0, fc=BOOK_BG_TINT['leviticus'], zorder=1))
    ax.add_patch(mpatches.Rectangle(
        (colx(1)-0.05, rowy(13)-0.05), FIELD*CELL+0.10, 3*CELL+0.10,
        lw=2.0, ec=BOOK_FRAME['leviticus'], fc='none', zorder=4))
    label(ax, colx(1)+FIELD*CELL/2, rowy(12)+CELL/2, 'Leviticus',
          font=SERIF_BOLD, size=12, color=BOOK_FRAME['leviticus'])
    label(ax, ML+GW+0.18, rowy(12)+CELL/2, '3 rows', size=9, ha='left',
          color=TXT_SOFT)

    # Divider 2 (row 14)
    draw_cell(ax, ML, rowy(14), GW, CELL, color=DIVIDER, lw=0)
    label(ax, 0.2, rowy(14)+CELL/2, 'register divider', size=9, ha='left',
          color=DIVIDER)
    label(ax, ML+GW+0.18, rowy(14)+CELL/2, '1 row', size=9, ha='left',
          color=TXT_SOFT)

    # Numbers (rows 15-19, 5 cols centered in field)
    NUM_COLS = 5
    num_c0 = (FIELD - NUM_COLS) // 2 + 1
    def num_field_col(c): return num_c0 + c - 1

    # Empty grid
    for r in range(15, 20):
        for c in range(1, NUM_COLS+1):
            fc = num_field_col(c)
            draw_cell(ax, colx(fc), rowy(r), CELL, CELL,
                      color=BG, ec=LIGHT_GRID, lw=0.5)
    # Numbers cruciform with Full-Map colors
    num_layout = [
        [None, 4,    6,  9,    None],
        [1,    None, None, None, 11],
        [2,    None, 7,    None, 12],
        [3,    None, None, None, 13],
        [None, 5,    8,  10,   None],
    ]
    NUM_UCOLOR = {
        1: ORANGE_CELL, 2: ORANGE_CELL, 3: ORANGE_CELL,
        4: MINT_CELL, 5: MINT_CELL, 6: MINT_CELL,
        7: INDEP_FILL,
        8: MINT_CELL, 9: MINT_CELL, 10: MINT_CELL,
        11: ORANGE_CELL, 12: ORANGE_CELL, 13: ORANGE_CELL,
    }
    for i, row in enumerate(num_layout):
        r_g = 15 + i
        for j, u in enumerate(row):
            if u is None: continue
            fc = num_field_col(j+1)
            if u == 7:
                draw_cell(ax, colx(fc), rowy(r_g), CELL, CELL,
                          color=INDEP_FILL, ec=INDEP_BORDER, lw=0.9)
            else:
                draw_cell(ax, colx(fc), rowy(r_g), CELL, CELL,
                          color=NUM_UCOLOR[u], ec=LIGHT_GRID, lw=0.5)

    # Numbers frame
    ax.add_patch(mpatches.Rectangle(
        (colx(num_c0)-0.05, rowy(19)-0.05), NUM_COLS*CELL+0.10, 5*CELL+0.10,
        lw=0, fc=BOOK_BG_TINT['numbers'], zorder=1))
    ax.add_patch(mpatches.Rectangle(
        (colx(num_c0)-0.05, rowy(19)-0.05), NUM_COLS*CELL+0.10, 5*CELL+0.10,
        lw=2.0, ec=BOOK_FRAME['numbers'], fc='none', zorder=4))
    label(ax, colx(num_c0)+NUM_COLS*CELL/2, rowy(17)+CELL/2, 'Numbers',
          font=SERIF_BOLD, size=12, color=BOOK_FRAME['numbers'])
    label(ax, ML+GW+0.18, rowy(17)+CELL/2, '5 rows', size=9, ha='left',
          color=TXT_SOFT)

    # Center-unit annotations (left side, flush left)
    label(ax, 0.2, rowy(5)+CELL/2,
          'sapphire pavement\n(Exodus Unit 10)', size=9, ha='left', color=TXT_SOFT)
    label(ax, 0.2, rowy(12)+CELL/2,
          '\u201cI YHWH your deity\nam holy\u201d (Lev Unit 13)',
          size=9, ha='left', color=TXT_SOFT)
    label(ax, 0.2, rowy(17)+CELL/2,
          'earth opens for Korach\n(Numbers Unit 7)',
          size=9, ha='left', color=TXT_SOFT)

    # Total bracket on right
    bx = ML + GW + 1.10
    ax.plot([bx, bx], [rowy(19), rowy(1)+CELL], color=TXT, lw=0.9)
    ax.plot([bx-0.07, bx], [rowy(19), rowy(19)], color=TXT, lw=0.9)
    ax.plot([bx-0.07, bx], [rowy(1)+CELL, rowy(1)+CELL], color=TXT, lw=0.9)
    label(ax, bx+0.12, BOT+GH/2, '19 rows\n9 + 1 + 3 + 1 + 5',
          size=9, ha='left', color=TXT_SOFT)

    label(ax, FW/2, FH-0.15,
          'Figure 9.  The Vertical Thread: 19 Rows',
          font=SERIF_BOLD, size=14, va='top')
    save(fig, 'fig-09-vertical-thread')


# ============================================================
# FIGURE 10: The complete 19x19 Torah grid
# Cross-shape:
#   Horizontal thread = 3 rows of Gen+Lev+Deut across the full 19 cols
#   Vertical thread = Exodus (above Lev) + Numbers (below Lev),
#     occupying only the central columns of the field, the same columns Lev uses.
#   Register dividers above Lev (between Ex and the horizontal band)
#                 and below Lev (between the horizontal band and Num).
# ============================================================
def fig10():
    CELL = 0.30
    SIZE = 19
    ML, MR, BOT, TOP = 1.7, 1.7, 1.4, 1.8
    GW = GH = SIZE * CELL
    FW, FH = ML+GW+MR, BOT+GH+TOP
    fig, ax = make_fig(FW, FH)

    def colx(c): return ML + (c-1)*CELL   # c 1-indexed, left to right
    def rowy(r): return BOT + GH - r*CELL  # r 1-indexed top to bottom

    # Layout: rows 9, 11 = top register divider above Lev? Let's match Fig 9:
    # Exodus rows 1-9, divider row 10, Lev rows 11-13, divider row 14, Numbers rows 15-19.
    # That's the same row arrangement as Fig 9.
    # Columns: same as Fig 8 -- Deut 1-5, Lev 6-12, Gen 13-19.
    # The vertical thread (Exodus and Numbers) occupies the cols Lev uses,
    # but we need to place Exodus (5 cols centered) and Numbers (5 cols centered)
    # somewhere within Lev's 7-col span (cols 6-12).
    # The Lev cols 6-12 map to letters: 6=H, 7=G, 8=F, 9=E (focal), 10=D, 11=B, 12=A
    # The pivot column is page col 9 (Lev E). Exodus and Numbers should center
    # on col 9. With 5 cols centered: cols 7-11.

    PIVOT_C = 9

    # Genesis cells (rows 11-13, cols 13-19)
    gen_internal_to_page = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7}
    gen_cols_internal = {
        1: (1, 2, 3), 2: (None, 4, None), 3: (5, 7, 9), 4: (6, 8, 10),
        5: (11, 13, 15), 6: (12, 14, 16), 7: (17, 18, 19),
    }
    for ic, units in gen_cols_internal.items():
        pc = gen_internal_to_page[ic]
        for r, u in enumerate(units):
            r_g = 11 + r
            if u is None:
                draw_cell(ax, colx(pc), rowy(r_g), CELL, CELL,
                          color=BG, ec=LIGHT_GRID, lw=0.3)
            elif u == 4:
                draw_cell(ax, colx(pc), rowy(r_g), CELL, CELL,
                          color=INDEP_FILL, ec=INDEP_BORDER, lw=0.8)
            else:
                draw_cell(ax, colx(pc), rowy(r_g), CELL, CELL,
                          color=GEN_UCOLOR[u], ec=LIGHT_GRID, lw=0.3)

    # Leviticus cells (rows 11-13, cols 6-12)
    LEV_UCOLOR = {
        1: LIGHT_CYAN, 2: LIGHT_CYAN, 3: LIGHT_CYAN,
        4: LIGHT_GREEN, 5: LIGHT_GREEN, 6: LIGHT_GREEN,
        10: LIGHT_PERI, 11: LIGHT_PERI, 12: LIGHT_PERI,
        13: INDEP_FILL,
        14: LIGHT_PERI, 15: LIGHT_PERI, 16: LIGHT_PERI,
        17: LIGHT_GREEN, 18: LIGHT_GREEN, 19: LIGHT_GREEN,
        20: LIGHT_CYAN, 21: LIGHT_CYAN, 22: LIGHT_CYAN,
    }
    lev_cols_internal = {
        'A': (1, 2, 3), 'B': (4, 5, 6), 'D': (10, 11, 12),
        'E': (None, 13, None),
        'F': (14, 15, 16), 'G': (17, 18, 19), 'H': (20, 21, 22),
    }
    lev_internal_to_page = {'A': 8, 'B': 9, 'D': 10, 'E': 11, 'F': 12, 'G': 13, 'H': 14}
    for letter, units in lev_cols_internal.items():
        pc = lev_internal_to_page[letter]
        for r, u in enumerate(units):
            r_g = 11 + r
            if u is None:
                draw_cell(ax, colx(pc), rowy(r_g), CELL, CELL,
                          color=BG, ec=LIGHT_GRID, lw=0.3)
            elif u == 13:
                draw_cell(ax, colx(pc), rowy(r_g), CELL, CELL,
                          color=INDEP_FILL, ec=INDEP_BORDER, lw=0.8)
            else:
                draw_cell(ax, colx(pc), rowy(r_g), CELL, CELL,
                          color=LEV_UCOLOR[u], ec=LIGHT_GRID, lw=0.3)

    # Deuteronomy cells (rows 11-13, cols 1-5)
    deut_internal_to_page = {1: 15, 2: 16, 3: 17, 4: 18, 5: 19}
    deut_cols_internal = {
        1: (1, 3, 5), 2: (2, 4, 6), 3: (7, 8, 9), 4: (10, 11, 12),
        5: (None, 13, None),
    }
    for ic, units in deut_cols_internal.items():
        pc = deut_internal_to_page[ic]
        for r, u in enumerate(units):
            r_g = 11 + r
            if u is None:
                draw_cell(ax, colx(pc), rowy(r_g), CELL, CELL,
                          color=BG, ec=LIGHT_GRID, lw=0.3)
            elif u == 13:
                draw_cell(ax, colx(pc), rowy(r_g), CELL, CELL,
                          color=INDEP_FILL, ec=INDEP_BORDER, lw=0.8)
            else:
                draw_cell(ax, colx(pc), rowy(r_g), CELL, CELL,
                          color=DEUT_UCOLOR[u], ec=LIGHT_GRID, lw=0.3)

    # Exodus cells (rows 1-9, cols 7-11) — vertical thread above
    EX_UCOLOR = {
        1: ORANGE_CELL, 2: ORANGE_CELL, 3: ORANGE_CELL, 4: ORANGE_CELL,
        5: INDEP_FILL,
        6: ORANGE_CELL, 7: ORANGE_CELL, 8: ORANGE_CELL, 9: ORANGE_CELL,
        10: INDEP_FILL,
        11: MINT_CELL, 12: MINT_CELL, 13: MINT_CELL, 14: MINT_CELL,
        15: INDEP_FILL,
        16: MINT_CELL, 17: MINT_CELL, 18: MINT_CELL, 19: MINT_CELL,
    }
    # Empty Exodus field
    for r in range(1, 10):
        for c in range(7, 12):
            draw_cell(ax, colx(c), rowy(r), CELL, CELL,
                      color=BG, ec=LIGHT_GRID, lw=0.3)
    # Left col (page col 7): U1-U4 rows 1-4, U11-U14 rows 6-9
    # Right col (page col 11): U6-U9 rows 1-4, U16-U19 rows 6-9
    for u, r in [(1,1),(2,2),(3,3),(4,4),(11,6),(12,7),(13,8),(14,9)]:
        draw_cell(ax, colx(7), rowy(r), CELL, CELL, color=EX_UCOLOR[u],
                  ec=LIGHT_GRID, lw=0.3)
    for u, r in [(6,1),(7,2),(8,3),(9,4),(16,6),(17,7),(18,8),(19,9)]:
        draw_cell(ax, colx(11), rowy(r), CELL, CELL, color=EX_UCOLOR[u],
                  ec=LIGHT_GRID, lw=0.3)
    # Independents in col 9 with half-row offsets
    y5  = rowy(2) - CELL/2
    y10 = rowy(5)
    y15 = rowy(7) - CELL/2
    for y in [y5, y10, y15]:
        draw_cell(ax, colx(9), y, CELL, CELL, color=INDEP_FILL,
                  ec=INDEP_BORDER, lw=0.6)

    # Register divider row 10 — spans Lev's full 7-col width
    import matplotlib.patches as mpatches
    for c in range(6, 13):
        draw_cell(ax, colx(c), rowy(10), CELL, CELL, color=DIVIDER, lw=0)

    # Register divider row 14
    for c in range(6, 13):
        draw_cell(ax, colx(c), rowy(14), CELL, CELL, color=DIVIDER, lw=0)

    # Numbers cells (rows 15-19, cols 7-11)
    NUM_UCOLOR = {
        1: ORANGE_CELL, 2: ORANGE_CELL, 3: ORANGE_CELL,
        4: MINT_CELL, 5: MINT_CELL, 6: MINT_CELL,
        7: INDEP_FILL,
        8: MINT_CELL, 9: MINT_CELL, 10: MINT_CELL,
        11: ORANGE_CELL, 12: ORANGE_CELL, 13: ORANGE_CELL,
    }
    num_layout = [
        [None, 4,    6,  9,    None],
        [1,    None, None, None, 11],
        [2,    None, 7,    None, 12],
        [3,    None, None, None, 13],
        [None, 5,    8,  10,   None],
    ]
    for r in range(15, 20):
        for c in range(7, 12):
            draw_cell(ax, colx(c), rowy(r), CELL, CELL,
                      color=BG, ec=LIGHT_GRID, lw=0.3)
    for i, row in enumerate(num_layout):
        r_g = 15 + i
        for j, u in enumerate(row):
            if u is None: continue
            c = 7 + j
            if u == 7:
                draw_cell(ax, colx(c), rowy(r_g), CELL, CELL,
                          color=INDEP_FILL, ec=INDEP_BORDER, lw=0.6)
            else:
                draw_cell(ax, colx(c), rowy(r_g), CELL, CELL,
                          color=NUM_UCOLOR[u], ec=LIGHT_GRID, lw=0.3)

    # Book frames
    # Genesis: cols 13-19, rows 11-13
    def book_frame(x0, y0, w, h, book, lw=1.6, pad=0.04):
        ax.add_patch(mpatches.Rectangle(
            (x0-pad, y0-pad), w+2*pad, h+2*pad,
            lw=0, fc=BOOK_BG_TINT[book], zorder=0))
        ax.add_patch(mpatches.Rectangle(
            (x0-pad, y0-pad), w+2*pad, h+2*pad,
            lw=lw, ec=BOOK_FRAME[book], fc='none', zorder=4))
    book_frame(colx(13), rowy(13), 7*CELL, 3*CELL, 'genesis')
    book_frame(colx(6),  rowy(13), 7*CELL, 3*CELL, 'leviticus')
    book_frame(colx(1),  rowy(13), 5*CELL, 3*CELL, 'deuteronomy')
    book_frame(colx(7),  rowy(9),  5*CELL, 9*CELL, 'exodus')
    book_frame(colx(7),  rowy(19), 5*CELL, 5*CELL, 'numbers')

    # Outer 19x19 field frame
    draw_border(ax, ML, BOT, GW, GH, lw=0.6, ec=ACCENT_BR)

    # Book labels
    label(ax, colx(7)+5*CELL/2, rowy(5)+CELL/2, 'Exodus',
          font=SERIF_BOLD, size=11, color=BOOK_FRAME['exodus'])
    label(ax, colx(7)+5*CELL/2, rowy(17)+CELL/2, 'Numbers',
          font=SERIF_BOLD, size=11, color=BOOK_FRAME['numbers'])
    label(ax, colx(13)+7*CELL/2, BOT-0.20, 'Genesis', font=SANS_BOLD,
          size=10, va='top', color=BOOK_FRAME['genesis'])
    label(ax, colx(6)+7*CELL/2, BOT-0.20, 'Leviticus', font=SANS_BOLD,
          size=10, va='top', color=BOOK_FRAME['leviticus'])
    label(ax, colx(1)+5*CELL/2, BOT-0.20, 'Deuteronomy', font=SANS_BOLD,
          size=10, va='top', color=BOOK_FRAME['deuteronomy'])

    # East/West indicators
    label(ax, colx(13)+7*CELL/2, BOT-0.50, '(east)', size=9, va='top', color=TXT_SOFT)
    label(ax, colx(1)+5*CELL/2,  BOT-0.50, '(west)', size=9, va='top', color=TXT_SOFT)

    # RTL arrow above the grid
    top = BOT + GH
    ay = top + 0.55
    ax.annotate('', xy=(ML+0.1, ay), xytext=(ML+GW-0.1, ay),
                arrowprops=dict(arrowstyle='->', color=TXT, lw=1.0))
    label(ax, ML+GW/2, ay+0.15, 'reading direction (right to left)',
          size=10, va='bottom', color=TXT_SOFT)

    label(ax, FW/2, FH-0.15,
          'Figure 10.  The Complete 19 \u00d7 19 Torah Grid',
          font=SERIF_BOLD, size=14, va='top')
    save(fig, 'fig-10-torah-grid-19x19')


fig8()
print("\nfig 8 rebuilt LTR.")
