"""
Set 2 v2: Figs 9 and 10 use the exact book diagrams from Set 1.
Unit numbers visible. Same cell colors per Full Torah Map.
"""
import sys
sys.path.insert(0, '/home/claude')
from fig_utils import *
import matplotlib.patches as mpatches

# === Color mappings (consistent across Set 1 and Set 2) ===
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
LEV_UCOLOR = {
    1: LIGHT_CYAN, 2: LIGHT_CYAN, 3: LIGHT_CYAN,
    4: LIGHT_GREEN, 5: LIGHT_GREEN, 6: LIGHT_GREEN,
    10: LIGHT_PERI, 11: LIGHT_PERI, 12: LIGHT_PERI,
    13: INDEP_FILL,
    14: LIGHT_PERI, 15: LIGHT_PERI, 16: LIGHT_PERI,
    17: LIGHT_GREEN, 18: LIGHT_GREEN, 19: LIGHT_GREEN,
    20: LIGHT_CYAN, 21: LIGHT_CYAN, 22: LIGHT_CYAN,
}
EX_UCOLOR_LEFT = {1:ORANGE_CELL,2:ORANGE_CELL,3:ORANGE_CELL,4:ORANGE_CELL,
                  11:MINT_CELL,12:MINT_CELL,13:MINT_CELL,14:MINT_CELL}
EX_UCOLOR_RIGHT = {6:ORANGE_CELL,7:ORANGE_CELL,8:ORANGE_CELL,9:ORANGE_CELL,
                   16:MINT_CELL,17:MINT_CELL,18:MINT_CELL,19:MINT_CELL}
NUM_UCOLOR = {
    1: ORANGE_CELL, 2: ORANGE_CELL, 3: ORANGE_CELL,
    4: MINT_CELL, 5: MINT_CELL, 6: MINT_CELL,
    7: INDEP_FILL,
    8: MINT_CELL, 9: MINT_CELL, 10: MINT_CELL,
    11: ORANGE_CELL, 12: ORANGE_CELL, 13: ORANGE_CELL,
}

def book_frame_box(ax, x0, y0, w, h, book, lw=2.0, pad=0.06):
    ax.add_patch(mpatches.Rectangle(
        (x0-pad, y0-pad), w+2*pad, h+2*pad,
        lw=0, fc=BOOK_BG_TINT[book], zorder=1))
    ax.add_patch(mpatches.Rectangle(
        (x0-pad, y0-pad), w+2*pad, h+2*pad,
        lw=lw, ec=BOOK_FRAME[book], fc='none', zorder=4))


# ============================================================
# Drawing helpers for each book diagram
# ============================================================

def draw_exodus_vertical_full(ax, ox, oy, CW, CH, show_numbers=True, num_size=10):
    """Vertical Exodus: 5 cols wide (with 2 gap cols), 9 rows tall.
    Returns (full_w, full_h)."""
    gap_w = CW
    full_w = 3*CW + 2*gap_w
    full_h = 9*CH
    xL = ox
    xC = ox + CW + gap_w
    xR = ox + 2*CW + 2*gap_w
    def ry(r): return oy + full_h - (r+1)*CH
    # Left col: U1-4 rows 0-3, U11-14 rows 5-8 (row 4 empty)
    for u, r in [(1,0),(2,1),(3,2),(4,3),(11,5),(12,6),(13,7),(14,8)]:
        draw_cell(ax, xL, ry(r), CW, CH, color=EX_UCOLOR_LEFT[u],
                  ec=LIGHT_GRID, lw=0.5)
        if show_numbers:
            label(ax, xL+CW/2, ry(r)+CH/2, str(u), font=SANS_BOLD, size=num_size)
    for u, r in [(6,0),(7,1),(8,2),(9,3),(16,5),(17,6),(18,7),(19,8)]:
        draw_cell(ax, xR, ry(r), CW, CH, color=EX_UCOLOR_RIGHT[u],
                  ec=LIGHT_GRID, lw=0.5)
        if show_numbers:
            label(ax, xR+CW/2, ry(r)+CH/2, str(u), font=SANS_BOLD, size=num_size)
    # Row 4 in outer cols = empty
    draw_cell(ax, xL, ry(4), CW, CH, color=BG, ec=LIGHT_GRID, lw=0.5)
    draw_cell(ax, xR, ry(4), CW, CH, color=BG, ec=LIGHT_GRID, lw=0.5)
    # Independents
    y5  = ry(1) - CH/2
    y10 = ry(4)
    y15 = ry(6) - CH/2
    for u, y in [(5, y5), (10, y10), (15, y15)]:
        draw_cell(ax, xC, y, CW, CH, color=INDEP_FILL,
                  ec=INDEP_BORDER, lw=1.2)
        if show_numbers:
            label(ax, xC+CW/2, y+CH/2, str(u), font=SANS_BOLD, size=num_size)
    return full_w, full_h


def draw_lev_3x7(ax, ox, oy, CW, CH, show_numbers=True, num_size=10):
    """Leviticus 3 rows x 7 cols (impurities col dropped, U13 focal).
    Layout (left to right): A B D E F G H
    Returns (full_w, full_h)."""
    full_w = 7*CW
    full_h = 3*CH
    def cx(c): return ox + c*CW
    def ry(r): return oy + full_h - (r+1)*CH

    cols = [
        (0, [1,2,3],     LIGHT_CYAN),    # A
        (1, [4,5,6],     LIGHT_GREEN),   # B
        (2, [10,11,12],  LIGHT_PERI),    # D
        (3, [None,13,None], None),       # E (focal)
        (4, [14,15,16],  LIGHT_PERI),    # F
        (5, [17,18,19],  LIGHT_GREEN),   # G
        (6, [20,21,22],  LIGHT_CYAN),    # H
    ]
    for c, units, color in cols:
        for r, u in enumerate(units):
            if u is None:
                draw_cell(ax, cx(c), ry(r), CW, CH, color=BG,
                          ec=LIGHT_GRID, lw=0.5)
            elif u == 13:
                draw_cell(ax, cx(c), ry(r), CW, CH, color=INDEP_FILL,
                          ec=INDEP_BORDER, lw=1.2)
                if show_numbers:
                    label(ax, cx(c)+CW/2, ry(r)+CH/2, '13',
                          font=SANS_BOLD, size=num_size)
            else:
                draw_cell(ax, cx(c), ry(r), CW, CH, color=color,
                          ec=LIGHT_GRID, lw=0.5)
                if show_numbers:
                    label(ax, cx(c)+CW/2, ry(r)+CH/2, str(u),
                          font=SANS_BOLD, size=num_size)
    return full_w, full_h


def draw_numbers_camp(ax, ox, oy, CELL, show_numbers=True, num_size=10):
    """Numbers 5x5 camp cruciform. Returns (full_w, full_h)."""
    full_w = full_h = 5*CELL
    def cx(c): return ox + c*CELL
    def ry(r): return oy + full_h - (r+1)*CELL
    layout = [
        [None, 4,    6,  9,    None],
        [1,    None, None, None, 11],
        [2,    None, 7,  None, 12],
        [3,    None, None, None, 13],
        [None, 5,    8,  10,   None],
    ]
    for r in range(5):
        for c in range(5):
            u = layout[r][c]
            if u is None:
                draw_cell(ax, cx(c), ry(r), CELL, CELL, color=BG,
                          ec=LIGHT_GRID, lw=0.5)
            elif u == 7:
                draw_cell(ax, cx(c), ry(r), CELL, CELL, color=INDEP_FILL,
                          ec=INDEP_BORDER, lw=1.2)
                if show_numbers:
                    label(ax, cx(c)+CELL/2, ry(r)+CELL/2, '7',
                          font=SANS_BOLD, size=num_size)
            else:
                draw_cell(ax, cx(c), ry(r), CELL, CELL, color=NUM_UCOLOR[u],
                          ec=LIGHT_GRID, lw=0.5)
                if show_numbers:
                    label(ax, cx(c)+CELL/2, ry(r)+CELL/2, str(u),
                          font=SANS_BOLD, size=num_size)
    return full_w, full_h


def draw_genesis_3x7(ax, ox, oy, CW, CH, show_numbers=True, num_size=10):
    """Genesis 3x7 matrix. Returns (full_w, full_h)."""
    full_w = 7*CW
    full_h = 3*CH
    def cx(c): return ox + c*CW
    def ry(r): return oy + full_h - (r+1)*CH
    layout = [
        [1, None, 5,  6,  11, 12, 17],
        [2, 4,    7,  8,  13, 14, 18],
        [3, None, 9,  10, 15, 16, 19],
    ]
    for r in range(3):
        for c in range(7):
            u = layout[r][c]
            if u is None:
                draw_cell(ax, cx(c), ry(r), CW, CH, color=BG,
                          ec=LIGHT_GRID, lw=0.5)
            elif u == 4:
                draw_cell(ax, cx(c), ry(r), CW, CH, color=INDEP_FILL,
                          ec=INDEP_BORDER, lw=1.2)
                if show_numbers:
                    label(ax, cx(c)+CW/2, ry(r)+CH/2, '4',
                          font=SANS_BOLD, size=num_size)
            else:
                draw_cell(ax, cx(c), ry(r), CW, CH, color=GEN_UCOLOR[u],
                          ec=LIGHT_GRID, lw=0.5)
                if show_numbers:
                    label(ax, cx(c)+CW/2, ry(r)+CH/2, str(u),
                          font=SANS_BOLD, size=num_size)
    return full_w, full_h


def draw_deut_3x5(ax, ox, oy, CW, CH, show_numbers=True, num_size=10):
    """Deuteronomy 3x5 matrix. Returns (full_w, full_h)."""
    full_w = 5*CW
    full_h = 3*CH
    def cx(c): return ox + c*CW
    def ry(r): return oy + full_h - (r+1)*CH
    layout = [
        [1, 2, 7, 10, None],
        [3, 4, 8, 11, 13  ],
        [5, 6, 9, 12, None],
    ]
    for r in range(3):
        for c in range(5):
            u = layout[r][c]
            if u is None:
                draw_cell(ax, cx(c), ry(r), CW, CH, color=BG,
                          ec=LIGHT_GRID, lw=0.5)
            elif u == 13:
                draw_cell(ax, cx(c), ry(r), CW, CH, color=INDEP_FILL,
                          ec=INDEP_BORDER, lw=1.2)
                if show_numbers:
                    label(ax, cx(c)+CW/2, ry(r)+CH/2, '13',
                          font=SANS_BOLD, size=num_size)
            else:
                draw_cell(ax, cx(c), ry(r), CW, CH, color=DEUT_UCOLOR[u],
                          ec=LIGHT_GRID, lw=0.5)
                if show_numbers:
                    label(ax, cx(c)+CW/2, ry(r)+CH/2, str(u),
                          font=SANS_BOLD, size=num_size)
    return full_w, full_h


# ============================================================
# FIGURE 9: vertical thread - stacked book diagrams
# Exodus (vertical, 9 rows) - divider - Leviticus (3x7) - divider - Numbers (5x5)
# All three centered on the same vertical axis.
# ============================================================
def fig9():
    # All diagrams use the same CELL size for visual consistency.
    CELL = 0.45
    # Exodus vertical: 5 cols (with gap=cell width) x 9 rows
    EX_W = 5*CELL
    EX_H = 9*CELL
    # Leviticus: 7 cols x 3 rows
    LEV_W = 7*CELL
    LEV_H = 3*CELL
    # Numbers: 5 cols x 5 rows
    NUM_W = 5*CELL
    NUM_H = 5*CELL
    # Register divider height = 1 cell row, spanning the widest book (Lev = 7)
    DIV_W = LEV_W
    DIV_H = CELL

    # Total stack height
    PAD_BOOK = 0.0   # dividers are touching; no extra padding
    total_h = EX_H + DIV_H + LEV_H + DIV_H + NUM_H

    ML, MR, BOT, TOP = 2.6, 2.6, 0.5, 1.15
    # Center every block horizontally on the same x-axis
    center_x = ML + LEV_W/2  # use Lev's width as reference (the widest)
    FW = ML + LEV_W + MR
    FH = BOT + total_h + TOP
    fig, ax = make_fig(FW, FH)

    # y-positions (bottom-up)
    num_y = BOT
    div2_y = num_y + NUM_H
    lev_y = div2_y + DIV_H
    div1_y = lev_y + LEV_H
    ex_y = div1_y + DIV_H

    # Numbers (5x5)
    num_x = center_x - NUM_W/2
    draw_numbers_camp(ax, num_x, num_y, CELL)
    book_frame_box(ax, num_x, num_y, NUM_W, NUM_H, 'numbers', lw=2.0)
    label(ax, num_x + NUM_W/2, num_y + NUM_H/2, 'Numbers',
          font=SERIF_BOLD, size=12, color=BOOK_FRAME['numbers'], alpha=0)
    # Use a more discreet book label (above/below diagram)
    label(ax, num_x - 0.20, num_y + NUM_H/2, 'Numbers\n(5 rows)',
          font=SANS_BOLD, size=10, ha='right', color=BOOK_FRAME['numbers'])

    # Divider 2
    div_x = center_x - DIV_W/2
    draw_cell(ax, div_x, div2_y, DIV_W, DIV_H, color=DIVIDER, lw=0)
    label(ax, div_x - 0.20, div2_y + DIV_H/2,
          'register divider', size=9, ha='right', color=DIVIDER)

    # Leviticus (3x7)
    lev_x = center_x - LEV_W/2
    draw_lev_3x7(ax, lev_x, lev_y, CELL, CELL)
    book_frame_box(ax, lev_x, lev_y, LEV_W, LEV_H, 'leviticus', lw=2.0)
    label(ax, lev_x - 0.20, lev_y + LEV_H/2, 'Leviticus\n(3 rows)',
          font=SANS_BOLD, size=10, ha='right', color=BOOK_FRAME['leviticus'])

    # Divider 1
    draw_cell(ax, div_x, div1_y, DIV_W, DIV_H, color=DIVIDER, lw=0)
    label(ax, div_x - 0.20, div1_y + DIV_H/2,
          'register divider', size=9, ha='right', color=DIVIDER)

    # Exodus (vertical, 9 rows)
    ex_x = center_x - EX_W/2
    draw_exodus_vertical_full(ax, ex_x, ex_y, CELL, CELL)
    book_frame_box(ax, ex_x, ex_y, EX_W, EX_H, 'exodus', lw=2.0)
    label(ax, ex_x - 0.20, ex_y + EX_H/2, 'Exodus\n(9 rows)',
          font=SANS_BOLD, size=10, ha='right', color=BOOK_FRAME['exodus'])

    # Right-side row count annotations
    label(ax, center_x + LEV_W/2 + 0.20, ex_y + EX_H/2, '9 rows',
          size=9, ha='left', color=TXT_SOFT)
    label(ax, center_x + LEV_W/2 + 0.20, div1_y + DIV_H/2, '1 row',
          size=9, ha='left', color=TXT_SOFT)
    label(ax, center_x + LEV_W/2 + 0.20, lev_y + LEV_H/2, '3 rows',
          size=9, ha='left', color=TXT_SOFT)
    label(ax, center_x + LEV_W/2 + 0.20, div2_y + DIV_H/2, '1 row',
          size=9, ha='left', color=TXT_SOFT)
    label(ax, center_x + LEV_W/2 + 0.20, num_y + NUM_H/2, '5 rows',
          size=9, ha='left', color=TXT_SOFT)

    # Total bracket on the far right
    bx = center_x + LEV_W/2 + 1.10
    by_top = ex_y + EX_H
    by_bot = num_y
    ax.plot([bx, bx], [by_bot, by_top], color=TXT, lw=0.9)
    ax.plot([bx-0.07, bx], [by_top, by_top], color=TXT, lw=0.9)
    ax.plot([bx-0.07, bx], [by_bot, by_bot], color=TXT, lw=0.9)
    label(ax, bx+0.10, (by_top+by_bot)/2,
          '19 rows\n9 + 1 + 3 + 1 + 5',
          size=9, ha='left', color=TXT_SOFT)

    label(ax, FW/2, FH-0.15,
          'Figure 9.  The Vertical Thread: 19 Rows',
          font=SERIF_BOLD, size=14, va='top')
    save(fig, 'fig-09-vertical-thread')


# ============================================================
# FIGURE 10: Complete 19x19 Torah grid
# Layout: Horizontal band of Gen+Lev+Deut at middle.
#         Exodus stacked above Lev; Numbers stacked below Lev.
#         Register dividers separating Ex/Lev and Lev/Num.
# Genesis and Deuteronomy use their own internal diagrams (3x7 and 3x5)
# placed flush with Lev on left and right of the horizontal band.
# ============================================================
def fig10():
    CELL = 0.34
    # Horizontal band: Gen (7) + Lev (7) + Deut (5) = 19 cols, all 3 rows tall
    GEN_W = 7*CELL
    LEV_W = 7*CELL
    DEUT_W = 5*CELL
    BAND_H = 3*CELL
    BAND_W = GEN_W + LEV_W + DEUT_W  # 19 * CELL

    # Vertical thread: Exodus (5 cols x 9 rows) and Numbers (5 cols x 5 rows)
    EX_W = 5*CELL
    EX_H = 9*CELL
    NUM_W = 5*CELL
    NUM_H = 5*CELL
    DIV_H = CELL
    # Divider width = Lev width (the divider is between Lev and the books above/below)
    DIV_W = LEV_W

    # Total vertical span:
    TOTAL_H = EX_H + DIV_H + BAND_H + DIV_H + NUM_H
    TOTAL_W = BAND_W  # the horizontal band is widest

    ML, MR, BOT, TOP = 1.0, 1.0, 1.2, 1.6
    FW = ML + TOTAL_W + MR
    FH = BOT + TOTAL_H + TOP
    fig, ax = make_fig(FW, FH)

    # Position the horizontal band such that Lev center is at horizontal center
    # of the whole grid? No — band spans full width. Place band at y = middle.
    num_y = BOT
    div2_y = num_y + NUM_H
    band_y = div2_y + DIV_H
    div1_y = band_y + BAND_H
    ex_y = div1_y + DIV_H

    # X positions for horizontal band components
    gen_x = ML
    lev_x = ML + GEN_W
    deut_x = ML + GEN_W + LEV_W

    # Vertical thread x: center on Lev (which spans gen_x+GEN_W to gen_x+GEN_W+LEV_W)
    lev_center_x = lev_x + LEV_W/2
    ex_x = lev_center_x - EX_W/2
    num_x = lev_center_x - NUM_W/2
    div_x = lev_center_x - DIV_W/2

    # Draw horizontal band: Genesis | Leviticus | Deuteronomy
    draw_genesis_3x7(ax, gen_x, band_y, CELL, CELL, num_size=8)
    book_frame_box(ax, gen_x, band_y, GEN_W, BAND_H, 'genesis', lw=1.8, pad=0.04)

    draw_lev_3x7(ax, lev_x, band_y, CELL, CELL, num_size=8)
    book_frame_box(ax, lev_x, band_y, LEV_W, BAND_H, 'leviticus', lw=1.8, pad=0.04)

    draw_deut_3x5(ax, deut_x, band_y, CELL, CELL, num_size=8)
    book_frame_box(ax, deut_x, band_y, DEUT_W, BAND_H, 'deuteronomy', lw=1.8, pad=0.04)

    # Dividers
    draw_cell(ax, div_x, div1_y, DIV_W, DIV_H, color=DIVIDER, lw=0)
    draw_cell(ax, div_x, div2_y, DIV_W, DIV_H, color=DIVIDER, lw=0)

    # Exodus above
    draw_exodus_vertical_full(ax, ex_x, ex_y, CELL, CELL, num_size=8)
    book_frame_box(ax, ex_x, ex_y, EX_W, EX_H, 'exodus', lw=1.8, pad=0.04)

    # Numbers below
    draw_numbers_camp(ax, num_x, num_y, CELL, num_size=8)
    book_frame_box(ax, num_x, num_y, NUM_W, NUM_H, 'numbers', lw=1.8, pad=0.04)

    # Book labels
    label(ax, gen_x + GEN_W/2, band_y - 0.30, 'Genesis',
          font=SANS_BOLD, size=11, va='top', color=BOOK_FRAME['genesis'])
    # Leviticus label sits inside the upper register divider, in black
    label(ax, lev_x + LEV_W/2, div1_y + DIV_H/2, 'Leviticus',
          font=SANS_BOLD, size=11, color=TXT)
    label(ax, deut_x + DEUT_W/2, band_y - 0.30, 'Deuteronomy',
          font=SANS_BOLD, size=11, va='top', color=BOOK_FRAME['deuteronomy'])
    label(ax, ex_x - 0.20, ex_y + EX_H/2, 'Exodus',
          font=SANS_BOLD, size=11, ha='right', color=BOOK_FRAME['exodus'])
    label(ax, num_x - 0.20, num_y + NUM_H/2, 'Numbers',
          font=SANS_BOLD, size=11, ha='right', color=BOOK_FRAME['numbers'])

    # Total dimensions
    label(ax, FW/2, BOT - 0.65,
          '19 columns \u00d7 19 rows',
          size=10, va='top', color=TXT_SOFT)

    label(ax, FW/2, FH-0.15,
          'Figure 10.  The Complete 19 \u00d7 19 Torah Grid',
          font=SERIF_BOLD, size=14, va='top')
    save(fig, 'fig-10-torah-grid-19x19')


fig9()
fig10()
print("\nFigs 9 and 10 rebuilt with book diagrams.")
