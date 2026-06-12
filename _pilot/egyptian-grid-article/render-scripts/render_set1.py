"""
Set 1 (Figs 1, 3-8): inner structure of one book per figure.
Palette from chaver.com Full Torah Map.
"""
import sys
sys.path.insert(0, '/home/claude')
from fig_utils import *

# ============================================================
# FIGURE 1: Covenant Code 5x3 (within Exodus, so Exodus frame)
# Threads 1 and 5 frame threads 2-4 — show with two shades of the inner-cell color.
# Cov Code is inside Exodus but is not a unit-cell of the book matrix,
# so we don't apply the per-unit Full-Map palette. We use the Exodus tint
# (orange-cell) with a slightly darker shade for the frame threads.
# ============================================================
def fig1():
    CW, CH = 1.50, 0.62
    COLS, ROWS = 3, 5
    ML, MR, BOT, TOP = 2.6, 0.7, 0.95, 1.95
    GW, GH = COLS*CW, ROWS*CH
    FW, FH = ML+GW+MR, BOT+GH+TOP
    fig, ax = make_fig(FW, FH)
    def cx(c): return ML + c*CW
    def ry(r): return BOT + GH - (r+1)*CH

    grid = [
        ['22:17',         '22:18',          '22:19'],
        ['22:20',         '22:21\u201323',  '22:24\u201326'],
        ['22:27',         '22:28\u201329',  '22:30'],
        ['23:1\u20133',   '23:4\u20136',    '23:7\u20139'],
        ['23:10\u201311', '23:12\u201313',  '23:14\u201319'],
    ]
    weft = [
        'Thread 1   Outsiders',
        'Thread 2   Disenfranchised',
        'Thread 3   Societal Authority',
        'Thread 4   Justice System',
        'Thread 5   YHWH\u2019s Nation',
    ]
    # Three-column unit palette: L (dark), M (medium), R (light) — per CSS
    col_colors = [COL_L, COL_M, COL_R]
    col_txt    = [COL_L_TXT, COL_M_TXT, COL_R_TXT]
    for r in range(ROWS):
        for c in range(COLS):
            draw_cell(ax, cx(c), ry(r), CW, CH, color=col_colors[c],
                      ec=LIGHT_GRID, lw=0.5)
            label(ax, cx(c)+CW/2, ry(r)+CH/2, grid[r][c],
                  font=SANS_REG, size=11, color=col_txt[c])

    # Exodus frame (since Cov Code is in Exodus)
    draw_book_frame(ax, ML, BOT, GW, GH, 'exodus', lw=2.4)

    # Weft labels
    for r in range(ROWS):
        label(ax, ML-0.20, ry(r)+CH/2, weft[r], size=10, ha='right',
              color=TXT, alpha=0.85)

    # Warp headers above
    top = BOT + GH
    heads = [
        ('L', 'mundane\nimmanent'),
        ('M', 'conceptual\nmiddle'),
        ('R', 'divine\ntranscendent'),
    ]
    for c, (h1, h2) in enumerate(heads):
        x = cx(c)+CW/2
        label(ax, x, top+0.62, h1, font=SANS_BOLD, size=12, va='bottom')
        label(ax, x, top+0.18, h2, font=SANS_REG, size=10, va='bottom',
              color=TXT_SOFT)

    label(ax, ML+GW/2, BOT-0.34,
          'Hocking & Kline, JBL 144/2 (2025).',
          size=10, va='top', color=TXT_SOFT)
    label(ax, ML+GW/2, FH-0.15,
          'Figure 1.  The Covenant Code (Exodus 22:17\u201323:19): Five Threads \u00d7 Three Segments',
          font=SERIF_BOLD, size=13, va='top')
    save(fig, 'fig-01-covenant-code-grid')

# ============================================================
# FIGURE 3: Leviticus 8 columns, with ring pairings and impurities marked.
# Colors per Full Torah Map:
#   Cols A (1,2,3) & H (20,21,22) = LIGHT_CYAN     (outer ring)
#   Cols B (4,5,6) & G (17,18,19) = LIGHT_GREEN    (middle ring)
#   Cols D (10,11,12) & F (14,15,16) = LIGHT_PERI  (inner ring)
#   Col C (7,8,9) = IMPURE_GRAY                    (impurities)
#   Col E (Unit 13) = INDEP_FILL + INDEP_BORDER    (focal)
# ============================================================
def fig3():
    CW, CH = 0.95, 0.62
    COLS, ROWS = 8, 3
    ML, MR, BOT, TOP = 1.2, 0.7, 2.6, 1.15
    GW, GH = COLS*CW, ROWS*CH
    FW, FH = ML+GW+MR, BOT+GH+TOP
    fig, ax = make_fig(FW, FH)
    def cx(c): return ML + c*CW
    def ry(r): return BOT + GH - (r+1)*CH

    cols = [
        [1,2,3], [4,5,6], [7,8,9], [10,11,12],
        [None,13,None], [14,15,16], [17,18,19], [20,21,22],
    ]
    col_colors = {
        0: LIGHT_CYAN,   # A outer
        1: LIGHT_GREEN,  # B middle
        2: IMPURE_GRAY,  # C impurities
        3: LIGHT_PERI,   # D inner
        4: None,         # E focal (only Unit 13)
        5: LIGHT_PERI,   # F inner
        6: LIGHT_GREEN,  # G middle
        7: LIGHT_CYAN,   # H outer
    }

    for c in range(COLS):
        for r in range(ROWS):
            u = cols[c][r]
            if c == 4:
                if u is None:
                    draw_cell(ax, cx(c), ry(r), CW, CH,
                              color=BG, ec=LIGHT_GRID, lw=0.5)
                else:
                    draw_cell(ax, cx(c), ry(r), CW, CH,
                              color=INDEP_FILL, ec=INDEP_BORDER, lw=1.6)
                    label(ax, cx(c)+CW/2, ry(r)+CH/2, str(u),
                          font=SANS_BOLD, size=12)
            else:
                if u is None:
                    draw_cell(ax, cx(c), ry(r), CW, CH,
                              color=BG, ec=LIGHT_GRID, lw=0.5)
                else:
                    draw_cell(ax, cx(c), ry(r), CW, CH,
                              color=col_colors[c], ec=LIGHT_GRID, lw=0.5)
                    label(ax, cx(c)+CW/2, ry(r)+CH/2, str(u),
                          font=SANS_BOLD, size=12)

    # Leviticus frame
    draw_book_frame(ax, ML, BOT, GW, GH, 'leviticus', lw=2.4)

    # Column letters above
    top = BOT + GH
    for c, L in enumerate(['A','B','C','D','E','F','G','H']):
        label(ax, cx(c)+CW/2, top+0.15, L, font=SANS_BOLD, size=11, va='bottom',
              color=TXT_SOFT if c == 2 else TXT)

    # Pairing arcs below, labels centered above the inner-ring midpoint
    base = BOT - 0.15
    pairs = [
        (3, 5, 'inner ring',  0.40),
        (1, 6, 'middle ring', 0.80),
        (0, 7, 'outer ring',  1.20),
    ]
    label_x = (cx(3)+CW/2 + cx(5)+CW/2) / 2
    for c0, c1, name, drop in pairs:
        x0, x1 = cx(c0)+CW/2, cx(c1)+CW/2
        y = base - drop
        ax.plot([x0, x0], [base, y], color=ACCENT_BR, lw=1.5)
        ax.plot([x1, x1], [base, y], color=ACCENT_BR, lw=1.5)
        ax.plot([x0, x1], [y, y],     color=ACCENT_BR, lw=1.5)
        label(ax, label_x, y+0.10, name, size=10, color=ACCENT_BR,
              ha='center', va='bottom')

    label(ax, ML+GW/2, FH-0.15,
          'Figure 2.  Leviticus: Eight Columns \u2014 Six Paired, One Removed',
          font=SERIF_BOLD, size=14, va='top')
    save(fig, 'fig-02-leviticus-columns')

# ============================================================
# FIGURE 4: Genesis 3x7
# Full Map palette per unit:
#   Row 1 outer cols (U1, U17, U18, U19): LIGHT_CYAN
#   Wait — checking data: U1=cyan, U2=cyan, U3=cyan (col A all cyan)
#                          U17,U18,U19=cyan (col G all cyan)
#                          U5,U7,U9 (col C) — U5=green, U7=green, U9=green
#                          U6,U8,U10 (col D) — periwinkle row 2, etc.
# Actually data: U1=cyan,U2=cyan,U3=cyan; U4=pink(indep);
#  U5=green,U6=peri,U7=green,U8=peri,U9=green,U10=peri
#  U11=peri,U12=green,U13=peri,U14=green,U15=peri,U16=green
#  U17=cyan,U18=cyan,U19=cyan
# So col A and col G = LIGHT_CYAN throughout (the "outer" columns at the extremes)
# Middle columns alternate green/peri between odd-numbered units and even-numbered.
# This matches the published Genesis ring structure: outer pair (cols A+G) are
# cosmic/political order (creation+Joseph). Inner cols pair across by triad type.
# ============================================================
def fig4():
    CW, CH = 0.95, 0.62
    COLS, ROWS = 7, 3
    ML, MR, BOT, TOP = 2.4, 0.7, 0.55, 1.55
    GW, GH = COLS*CW, ROWS*CH
    FW, FH = ML+GW+MR, BOT+GH+TOP
    fig, ax = make_fig(FW, FH)
    def cx(c): return ML + c*CW
    def ry(r): return BOT + GH - (r+1)*CH

    # Layout: (row, col) -> unit number (or None)
    layout = [
        [1, None, 5,  6,  11, 12, 17],
        [2, 4,    7,  8,  13, 14, 18],
        [3, None, 9,  10, 15, 16, 19],
    ]
    # Color per unit number (from Full Torah Map)
    UCOLOR = {
        1: LIGHT_CYAN, 2: LIGHT_CYAN, 3: LIGHT_CYAN,
        4: INDEP_FILL,
        5: LIGHT_GREEN, 6: LIGHT_PERI, 7: LIGHT_GREEN, 8: LIGHT_PERI,
        9: LIGHT_GREEN, 10: LIGHT_PERI,
        11: LIGHT_PERI, 12: LIGHT_GREEN, 13: LIGHT_PERI, 14: LIGHT_GREEN,
        15: LIGHT_PERI, 16: LIGHT_GREEN,
        17: LIGHT_CYAN, 18: LIGHT_CYAN, 19: LIGHT_CYAN,
    }

    for r in range(ROWS):
        for c in range(COLS):
            u = layout[r][c]
            if u is None:
                draw_cell(ax, cx(c), ry(r), CW, CH,
                          color=BG, ec=LIGHT_GRID, lw=0.5)
            elif u == 4:
                draw_cell(ax, cx(c), ry(r), CW, CH,
                          color=INDEP_FILL, ec=INDEP_BORDER, lw=1.6)
                label(ax, cx(c)+CW/2, ry(r)+CH/2, '4', font=SANS_BOLD, size=13)
            else:
                draw_cell(ax, cx(c), ry(r), CW, CH,
                          color=UCOLOR[u], ec=LIGHT_GRID, lw=0.5)
                label(ax, cx(c)+CW/2, ry(r)+CH/2, str(u), font=SANS_BOLD, size=13)

    draw_book_frame(ax, ML, BOT, GW, GH, 'genesis', lw=2.4)

    # Genesis (pre-pivot): Row 1 transcendent / Row 2 interface / Row 3 earthly
    label(ax, 0.2, ry(0)+CH/2, 'Row 1  transcendent', size=10, ha='left', color=TXT_SOFT)
    label(ax, 0.2, ry(1)+CH/2, 'Row 2  interface',    size=10, ha='left', color=TXT_SOFT)
    label(ax, 0.2, ry(2)+CH/2, 'Row 3  earthly',      size=10, ha='left', color=TXT_SOFT)

    # Column block labels
    top = BOT + GH
    for c0, c1, name in [(0,0,'Primordial'),(1,1,'Babel'),
                         (2,3,'Abraham cycle'),(4,5,'Jacob cycle'),
                         (6,6,'Joseph')]:
        label(ax, cx(c0)+(c1-c0+1)*CW/2, top+0.15, name, size=10, va='bottom',
              color=TXT_SOFT)

    label(ax, ML+GW/2, FH-0.15,
          'Figure 3.  Genesis: 19 Units in a 3\u00d77 Matrix',
          font=SERIF_BOLD, size=14, va='top')
    save(fig, 'fig-03-genesis-matrix')

# ============================================================
# FIGURE 5: Deuteronomy 3x5
# Full Map palette: U1=cyan,U2=green,U3=cyan,U4=green,U5=cyan,U6=green,
#   U7=green,U8=green,U9=green,U10=cyan,U11=cyan,U12=cyan,U13=pink(indep)
# So Col 1: cyan/cyan/cyan? Let's check positions from full-torah-map:
# Deut units placed: U1 top=405 left=891, U2 top=405 left=918, U3 top=459 left=891
#   U4 top=459 left=918, U5 top=513 left=891, U6 top=513 left=918
#   U7 top=405 left=972, U8 top=459 left=972, U9 top=513 left=972
#   U10 top=405 left=1026, U11 top=459 left=1026, U12 top=513 left=1026
#   U13 top=459 left=1080
# So columns by left coord: 891 (U1,U3,U5), 918 (U2,U4,U6), 972 (U7,U8,U9),
#   1026 (U10,U11,U12), 1080 (U13)
# Colors: col 891 = U1 cyan, U3 cyan, U5 cyan -> all cyan
#         col 918 = U2 green, U4 green, U6 green -> all green
#         col 972 = U7,U8,U9 all green
#         col 1026 = U10,U11,U12 all cyan
#         col 1080 = U13 pink (indep)
# So Deut has 5 cols: cyan, green, green, cyan, indep
# Pattern by triad: col 1 cyan + col 2 green = first triad (Past)
#                   col 3 green = second triad (Covenant principles) — both green?
#                   col 4 cyan = third triad (Legal corpus)
#                   col 5 indep = U13 alone
# Actually we have 4 triadic columns + 1 indep, not paired into triads of 3 cells
# But the LAYOUT in the matrix is 3 rows x 5 cols.
# Reading the data, the Deut matrix in the Full Map uses two colors that
# alternate by COLUMN: col1 cyan, col2 green, col3 green, col4 cyan, col5 indep.
# That's the published color scheme - I'll preserve it exactly.
# ============================================================
def fig5():
    CW, CH = 0.95, 0.62
    COLS, ROWS = 5, 3
    ML, MR, BOT, TOP = 2.4, 0.7, 0.55, 1.55
    GW, GH = COLS*CW, ROWS*CH
    FW, FH = ML+GW+MR, BOT+GH+TOP
    fig, ax = make_fig(FW, FH)
    def cx(c): return ML + c*CW
    def ry(r): return BOT + GH - (r+1)*CH

    layout = [
        [1, 2, 7, 10, None],
        [3, 4, 8, 11, 13  ],
        [5, 6, 9, 12, None],
    ]
    UCOLOR = {
        1: LIGHT_CYAN, 3: LIGHT_CYAN, 5: LIGHT_CYAN,
        2: LIGHT_GREEN, 4: LIGHT_GREEN, 6: LIGHT_GREEN,
        7: LIGHT_GREEN, 8: LIGHT_GREEN, 9: LIGHT_GREEN,
        10: LIGHT_CYAN, 11: LIGHT_CYAN, 12: LIGHT_CYAN,
        13: INDEP_FILL,
    }

    for r in range(ROWS):
        for c in range(COLS):
            u = layout[r][c]
            if u is None:
                draw_cell(ax, cx(c), ry(r), CW, CH,
                          color=BG, ec=LIGHT_GRID, lw=0.5)
            elif u == 13:
                draw_cell(ax, cx(c), ry(r), CW, CH,
                          color=INDEP_FILL, ec=INDEP_BORDER, lw=1.6)
                label(ax, cx(c)+CW/2, ry(r)+CH/2, '13', font=SANS_BOLD, size=13)
            else:
                draw_cell(ax, cx(c), ry(r), CW, CH,
                          color=UCOLOR[u], ec=LIGHT_GRID, lw=0.5)
                label(ax, cx(c)+CW/2, ry(r)+CH/2, str(u), font=SANS_BOLD, size=13)

    draw_book_frame(ax, ML, BOT, GW, GH, 'deuteronomy', lw=2.4)

    label(ax, 0.2, ry(0)+CH/2, 'Row 1  earthly',      size=10, ha='left', color=TXT_SOFT)
    label(ax, 0.2, ry(1)+CH/2, 'Row 2  interface',    size=10, ha='left', color=TXT_SOFT)
    label(ax, 0.2, ry(2)+CH/2, 'Row 3  transcendent', size=10, ha='left', color=TXT_SOFT)

    top = BOT + GH
    label(ax, cx(0)+CW*2, top+0.15, 'Four triads', size=10, va='bottom',
          color=TXT_SOFT)
    label(ax, cx(4)+CW/2, top+0.15, 'Independent', size=10, va='bottom',
          color=TXT_SOFT)

    label(ax, ML+GW/2, FH-0.15,
          'Figure 4.  Deuteronomy: 13 Units in a 3\u00d75 Matrix',
          font=SERIF_BOLD, size=14, va='top')
    save(fig, 'fig-04-deuteronomy-matrix')

# ============================================================
# FIGURE 6: Exodus — two arrangements side by side
# Full Map: U1-U4 = ORANGE; U5,U10,U15 = INDEP (pink);
#           U6-U9 = ORANGE; U11-U14 = MINT; U16-U19 = MINT
# So orange = first half (Egypt + wilderness/Sinai); mint = second half (Tabernacle)
# ============================================================
def draw_exodus_vertical(ax, ox, oy, CW, CH, gap_w=None):
    """5-column vertical (full-width gaps). Returns (full_w, full_h)."""
    if gap_w is None:
        gap_w = CW
    full_w = 3*CW + 2*gap_w
    full_h = 9*CH
    xL = ox
    xC = ox + CW + gap_w
    xR = ox + 2*CW + 2*gap_w
    def ry_outer(r):
        return oy + full_h - (r+1)*CH
    # First half (orange): U1-4 left col rows 0-3, U6-9 right col rows 0-3
    # Second half (mint): U11-14 left col rows 5-8, U16-19 right col rows 5-8
    for u, r in [(1,0),(2,1),(3,2),(4,3)]:
        draw_cell(ax, xL, ry_outer(r), CW, CH, color=ORANGE_CELL, ec=LIGHT_GRID, lw=0.5)
        label(ax, xL+CW/2, ry_outer(r)+CH/2, str(u), font=SANS_BOLD, size=12)
    for u, r in [(6,0),(7,1),(8,2),(9,3)]:
        draw_cell(ax, xR, ry_outer(r), CW, CH, color=ORANGE_CELL, ec=LIGHT_GRID, lw=0.5)
        label(ax, xR+CW/2, ry_outer(r)+CH/2, str(u), font=SANS_BOLD, size=12)
    for u, r in [(11,5),(12,6),(13,7),(14,8)]:
        draw_cell(ax, xL, ry_outer(r), CW, CH, color=MINT_CELL, ec=LIGHT_GRID, lw=0.5)
        label(ax, xL+CW/2, ry_outer(r)+CH/2, str(u), font=SANS_BOLD, size=12)
    for u, r in [(16,5),(17,6),(18,7),(19,8)]:
        draw_cell(ax, xR, ry_outer(r), CW, CH, color=MINT_CELL, ec=LIGHT_GRID, lw=0.5)
        label(ax, xR+CW/2, ry_outer(r)+CH/2, str(u), font=SANS_BOLD, size=12)
    draw_cell(ax, xL, ry_outer(4), CW, CH, color=BG, ec=LIGHT_GRID, lw=0.5)
    draw_cell(ax, xR, ry_outer(4), CW, CH, color=BG, ec=LIGHT_GRID, lw=0.5)
    # Independents
    y5  = ry_outer(1) - CH/2
    y10 = ry_outer(4)
    y15 = ry_outer(6) - CH/2
    for u, y in [(5, y5), (10, y10), (15, y15)]:
        draw_cell(ax, xC, y, CW, CH,
                  color=INDEP_FILL, ec=INDEP_BORDER, lw=1.4)
        label(ax, xC+CW/2, y+CH/2, str(u), font=SANS_BOLD, size=12)
    return full_w, full_h

def fig6():
    fig_w, fig_h = 11.0, 6.8
    fig, ax = make_fig(fig_w, fig_h)

    CW, CH = 0.62, 0.50
    qx = 0.6
    panel_cy = 1.0 + 9*CH/2
    band_gap = 1.5
    top_band_y = panel_cy + band_gap/2
    bot_band_y = panel_cy - band_gap/2 - 2*CH

    def draw_quad(units, x0, y0, color):
        for i in range(2):
            for j in range(2):
                x, y = x0 + j*CW, y0 + (1-i)*CH
                draw_cell(ax, x, y, CW, CH, color=color, ec=LIGHT_GRID, lw=0.5)
                label(ax, x+CW/2, y+CH/2, str(units[i][j]),
                      font=SANS_BOLD, size=11)
        # No extra inner box; cell borders are enough

    gap_c = 0.55
    xTL = qx
    xC  = qx + 2*CW + gap_c
    xTR = xC + CW + gap_c

    draw_quad([[1,2],[3,4]],     xTL, top_band_y, ORANGE_CELL)
    draw_quad([[6,7],[8,9]],     xTR, top_band_y, ORANGE_CELL)
    draw_quad([[11,12],[13,14]], xTL, bot_band_y, MINT_CELL)
    draw_quad([[16,17],[18,19]], xTR, bot_band_y, MINT_CELL)
    for u, yc in [(5, top_band_y + CH), (10, panel_cy), (15, bot_band_y + CH)]:
        draw_cell(ax, xC, yc-CH/2, CW, CH,
                  color=INDEP_FILL, ec=INDEP_BORDER, lw=1.4)
        label(ax, xC+CW/2, yc, str(u), font=SANS_BOLD, size=11)

    panel_w = xTR + 2*CW - qx
    # Book frame around the entire quad arrangement
    draw_book_frame(ax, qx, bot_band_y - 0.1, panel_w, top_band_y + 2*CH + 0.1 - (bot_band_y - 0.1),
                    'exodus', lw=2.2, pad=0.12)

    label(ax, qx + panel_w/2, bot_band_y - 0.5,
          'Published quad arrangement\n(merkavah layout)', size=10, va='top',
          color=TXT_SOFT)

    CW2, CH2 = 0.55, 0.50
    vx = qx + panel_w + 1.0
    vy = 0.9
    fw2, fh2 = draw_exodus_vertical(ax, vx, vy, CW2, CH2)
    draw_book_frame(ax, vx, vy, fw2, fh2, 'exodus', lw=2.2, pad=0.12)

    label(ax, vx + fw2/2, vy - 0.5,
          'Vertical arrangement\n(five columns)', size=10, va='top',
          color=TXT_SOFT)

    midx = (qx + panel_w + vx) / 2
    label(ax, midx, panel_cy, 'same\n19 units', size=10, color=TXT_SOFT)

    label(ax, fig_w/2, fig_h-0.15,
          'Figure 5.  Exodus: Two Arrangements of the Same Nineteen Units',
          font=SERIF_BOLD, size=14, va='top')
    save(fig, 'fig-05-exodus-two-arrangements')

# ============================================================
# FIGURE 7: Exodus vertical with column continuities
# ============================================================
def fig7():
    CW, CH = 0.70, 0.55
    full_w = 5*CW
    full_h = 9*CH
    ML, MR, BOT, TOP = 3.6, 3.6, 0.95, 1.25
    FW, FH = ML+full_w+MR, BOT+full_h+TOP
    fig, ax = make_fig(FW, FH)
    draw_exodus_vertical(ax, ML, BOT, CW, CH)
    draw_book_frame(ax, ML, BOT, full_w, full_h, 'exodus', lw=2.4, pad=0.12)

    def ry_outer(r):
        return BOT + full_h - (r+1)*CH

    y4  = ry_outer(3) + CH/2
    y11 = ry_outer(5) + CH/2
    hookL = ML - 0.40
    arrow_color = INDEP_BORDER
    ax.plot([ML, hookL], [y4, y4], color=arrow_color, lw=1.6, zorder=8)
    ax.plot([hookL, hookL], [y4, y11], color=arrow_color, lw=1.6, zorder=8)
    ax.annotate('', xy=(ML, y11), xytext=(hookL, y11),
                arrowprops=dict(arrowstyle='->', color=arrow_color, lw=1.6),
                zorder=8)
    y9, y16 = ry_outer(3) + CH/2, ry_outer(5) + CH/2
    hookR = ML + full_w + 0.40
    ax.plot([ML+full_w, hookR], [y9, y9], color=arrow_color, lw=1.6, zorder=8)
    ax.plot([hookR, hookR], [y9, y16], color=arrow_color, lw=1.6, zorder=8)
    ax.annotate('', xy=(ML+full_w, y16), xytext=(hookR, y16),
                arrowprops=dict(arrowstyle='->', color=arrow_color, lw=1.6),
                zorder=8)

    label(ax, 0.4, ry_outer(4)+CH/2 + 0.35,
          'Left column: Unit 4 contains\ntreasure taken from Egypt;\nUnit 11 begins with treasure\nfor building the Tabernacle',
          size=10, ha='left', color=arrow_color)
    label(ax, hookR + 0.25, ry_outer(4)+CH/2 + 0.35,
          'Right column: Unit 9 ends\nwith the Sabbath; Unit 16\nbegins with the Sabbath',
          size=10, ha='left', color=arrow_color)

    label(ax, FW/2, FH-0.15,
          'Figure 6.  Exodus: The Vertical Arrangement with Column Continuities',
          font=SERIF_BOLD, size=13, va='top')
    save(fig, 'fig-06-exodus-vertical')

# ============================================================
# FIGURE 8: Numbers 5x5 camp
# Full Map per unit:
#   U1,U2,U3 (left side) = ORANGE
#   U4,U5,U6,U8,U9,U10 (flag-axis tribes) = MINT
#   U7 = INDEP (focal, Korach)
#   U11,U12,U13 (right side) = ORANGE
# Re-checking: U4=mint, U5=mint, U6=mint, U7=pink, U8=mint, U9=mint, U10=mint
#   U1=orange, U2=orange, U3=orange (left), U11=orange, U12=orange, U13=orange (right)
# So: ORANGE = the 3-unit sides; MINT = the 4-unit top+bottom rows
# The flag units (2, 6, 8, 12) are NOT specially colored in the Full Map.
# ============================================================
def fig8():
    CELL = 0.80
    COLS = ROWS = 5
    ML, MR, BOT, TOP = 1.0, 1.0, 0.7, 1.4
    GW = GH = COLS*CELL
    FW, FH = ML+GW+MR, BOT+GH+TOP
    fig, ax = make_fig(FW, FH)
    def cx(c): return ML + c*CELL
    def ry(r): return BOT + GH - (r+1)*CELL

    layout = [
        [None, 4,    6,  9,    None],
        [1,    None, None, None, 11],
        [2,    None, 7,  None, 12],
        [3,    None, None, None, 13],
        [None, 5,    8,  10,   None],
    ]
    # Per Full Map: U1-3 + U11-13 = orange; U4-6, U8-10 = mint; U7 = indep
    UCOLOR = {
        1: ORANGE_CELL, 2: ORANGE_CELL, 3: ORANGE_CELL,
        4: MINT_CELL, 5: MINT_CELL, 6: MINT_CELL,
        7: INDEP_FILL,
        8: MINT_CELL, 9: MINT_CELL, 10: MINT_CELL,
        11: ORANGE_CELL, 12: ORANGE_CELL, 13: ORANGE_CELL,
    }
    for r in range(ROWS):
        for c in range(COLS):
            u = layout[r][c]
            if u is None:
                draw_cell(ax, cx(c), ry(r), CELL, CELL,
                          color=BG, ec=LIGHT_GRID, lw=0.5)
            elif u == 7:
                draw_cell(ax, cx(c), ry(r), CELL, CELL,
                          color=INDEP_FILL, ec=INDEP_BORDER, lw=1.6)
                label(ax, cx(c)+CELL/2, ry(r)+CELL/2, '7',
                      font=SANS_BOLD, size=13)
            else:
                draw_cell(ax, cx(c), ry(r), CELL, CELL,
                          color=UCOLOR[u], ec=LIGHT_GRID, lw=0.5)
                label(ax, cx(c)+CELL/2, ry(r)+CELL/2, str(u),
                      font=SANS_BOLD, size=13)

    draw_book_frame(ax, ML, BOT, GW, GH, 'numbers', lw=2.4)

    label(ax, ML+GW/2, FH-0.15,
          'Figure 7.  Numbers: 13 Units as the Desert Camp (5\u00d75)',
          font=SERIF_BOLD, size=14, va='top')
    save(fig, 'fig-07-numbers-camp')

fig4()   # produces fig-03-genesis-matrix
fig5()   # produces fig-04-deuteronomy-matrix
print("\nGenesis and Deuteronomy figs rebuilt.")
