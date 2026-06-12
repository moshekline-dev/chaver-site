"""
Set 3 (Figs 11-15): the Egyptian paradigm and Torah/Amduat correspondence.
"""
import sys
sys.path.insert(0, '/home/claude')
from fig_utils import *
import matplotlib.patches as mpatches
import math

# ============================================================
# FIGURE 11: The Egyptian canon of proportions
# ============================================================
def fig11():
    FW, FH = 6.5, 9.5
    fig, ax = make_fig(FW, FH)
    sq = 0.42
    cx = FW/2
    base_y = 0.7
    grid_w = 4 * sq

    for i in range(20):
        y = base_y + i*sq
        ax.plot([cx - grid_w/2, cx + grid_w/2], [y, y],
                color=LIGHT_GRID, lw=0.5, zorder=1)
    for j in range(5):
        x = cx - grid_w/2 + j*sq
        ax.plot([x, x], [base_y, base_y + 19*sq],
                color=LIGHT_GRID, lw=0.5, zorder=1)

    for i, lbl, color, lw in [
        (0,  'sole',     ACCENT_BR,    1.6),
        (18, 'hairline', INDEP_BORDER, 1.8),
        (19, 'crown',    INDEP_BORDER, 1.8),
    ]:
        y = base_y + i*sq
        ax.plot([cx - grid_w/2 - 0.2, cx + grid_w/2 + 0.2], [y, y],
                color=color, lw=lw, zorder=3)
        label(ax, cx + grid_w/2 + 0.3, y, f'{i} \u2014 {lbl}',
              size=10, ha='left', color=color, va='center')

    figure_color = TXT
    lw_fig = 1.5
    foot_y = base_y
    knee_y = base_y + 6*sq
    butt_y = base_y + 9*sq
    ax.plot([cx - 0.35*sq, cx - 0.35*sq], [foot_y, butt_y],
            color=figure_color, lw=lw_fig)
    ax.plot([cx + 0.35*sq, cx + 0.35*sq], [foot_y, butt_y],
            color=figure_color, lw=lw_fig)
    ax.plot([cx - 0.7*sq, cx - 0.05*sq], [foot_y, foot_y],
            color=figure_color, lw=lw_fig)
    ax.plot([cx + 0.05*sq, cx + 0.7*sq], [foot_y, foot_y],
            color=figure_color, lw=lw_fig)

    shoulder_y = base_y + 16*sq
    ax.plot([cx - 0.85*sq, cx - 0.85*sq], [butt_y, shoulder_y],
            color=figure_color, lw=lw_fig)
    ax.plot([cx + 0.85*sq, cx + 0.85*sq], [butt_y, shoulder_y],
            color=figure_color, lw=lw_fig)
    ax.plot([cx - 0.85*sq, cx + 0.85*sq], [shoulder_y, shoulder_y],
            color=figure_color, lw=lw_fig)
    ax.plot([cx - 0.85*sq, cx + 0.85*sq], [butt_y, butt_y],
            color=figure_color, lw=lw_fig)

    hand_y = base_y + 10*sq
    ax.plot([cx - 1.4*sq, cx - 1.4*sq], [shoulder_y, hand_y],
            color=figure_color, lw=lw_fig)
    ax.plot([cx + 1.4*sq, cx + 1.4*sq], [shoulder_y, hand_y],
            color=figure_color, lw=lw_fig)
    ax.plot([cx - 0.85*sq, cx - 1.4*sq], [shoulder_y, shoulder_y],
            color=figure_color, lw=lw_fig)
    ax.plot([cx + 0.85*sq, cx + 1.4*sq], [shoulder_y, shoulder_y],
            color=figure_color, lw=lw_fig)

    neck_y = base_y + 17*sq
    ax.plot([cx - 0.4*sq, cx - 0.4*sq], [shoulder_y, neck_y],
            color=figure_color, lw=lw_fig)
    ax.plot([cx + 0.4*sq, cx + 0.4*sq], [shoulder_y, neck_y],
            color=figure_color, lw=lw_fig)
    head_actual_center = base_y + 17.75*sq
    head_half_w = 0.8 * sq
    ax.add_patch(mpatches.Ellipse(
        (cx, head_actual_center), 2*head_half_w, 2.5*sq,
        fill=False, ec=figure_color, lw=lw_fig, zorder=2))

    for i in [3, 6, 9, 12, 15]:
        y = base_y + i*sq
        label(ax, cx - grid_w/2 - 0.18, y, str(i), size=9, ha='right',
              color=TXT_SOFT)

    label(ax, FW/2, base_y - 0.45,
          '18 squares define the proportioned figure (sole to hairline).\n'
          '19 squares define the compositional field (sole to crown).',
          size=10, va='top', color=TXT_SOFT)
    label(ax, FW/2, FH-0.15,
          'Figure 11.  The Egyptian Canon of Proportions',
          font=SERIF_BOLD, size=14, va='top')
    save(fig, 'fig-11-canon-of-proportions')


# ============================================================
# FIGURE 12: The Amduat — 12 hours x 3 registers
# ============================================================
def fig12():
    CW, CH = 0.62, 0.85
    COLS, ROWS = 12, 3
    ML, MR, BOT, TOP = 1.5, 2.6, 1.0, 1.6
    GW, GH = COLS*CW, ROWS*CH
    FW, FH = ML+GW+MR, BOT+GH+TOP
    fig, ax = make_fig(FW, FH)
    def cx(c): return ML + c*CW
    def ry(r): return BOT + GH - (r+1)*CH

    reg_colors = [LIGHT_CYAN, LIGHT_PERI, LIGHT_GREEN]
    top = BOT + GH
    for r in range(ROWS):
        for c in range(COLS):
            draw_cell(ax, cx(c), ry(r), CW, CH, color=reg_colors[r],
                      ec=LIGHT_GRID, lw=0.4)
    for r in (1, 2):
        ax.plot([ML, ML+GW], [BOT+r*CH, BOT+r*CH],
                color=DIVIDER, lw=2.5, zorder=4)
    draw_border(ax, ML, BOT, GW, GH, lw=1.0)

    for c in range(COLS):
        label(ax, cx(c)+CW/2, top+0.18, str(c+1), font=SANS_BOLD, size=11,
              va='bottom', color=TXT_SOFT)

    h6 = cx(5) + CW/2
    ax.plot([h6, h6], [BOT-0.08, BOT+GH+0.10], color=INDEP_BORDER,
            lw=1.8, ls='--', zorder=5)
    label(ax, h6, top+0.55, 'Hour 6\nRa unites with Osiris',
          font=SANS_BOLD, size=10, va='bottom', color=INDEP_BORDER)

    for r, name, sub in [(0, 'upper',  'celestial backdrop'),
                          (1, 'middle', 'the divine barque'),
                          (2, 'lower',  'chthonic forces')]:
        label(ax, ML+GW+0.20, ry(r)+CH*0.62, name, font=SANS_BOLD,
              size=11, ha='left')
        label(ax, ML+GW+0.20, ry(r)+CH*0.30, sub, size=10, ha='left',
              color=TXT_SOFT)

    label(ax, ML+GW/2, BOT-0.30, 'twelve hours of the night',
          size=10, va='top', color=TXT_SOFT)
    label(ax, FW/2, FH-0.15,
          'Figure 12.  The Amduat: Twelve Hours \u00d7 Three Registers',
          font=SERIF_BOLD, size=14, va='top')
    save(fig, 'fig-12-amduat-schematic')


# ============================================================
# FIGURE 13: Single integrated 5-level diagram
# ============================================================
def fig13():
    FW, FH = 9.5, 9.2
    fig, ax = make_fig(FW, FH)

    CW = 3.2
    GAP = 0.4
    LH = 0.85
    INNER_H = 0.65
    DIV_H = 0.18

    total_w = 2*CW + GAP
    LX = (FW - total_w) / 2
    RX = LX + CW + GAP

    BOT = 1.3
    floor_y      = BOT
    div2_y       = floor_y + LH
    middle_bot_y = div2_y + DIV_H
    middle_top_y = middle_bot_y + 3*INNER_H
    div1_y       = middle_top_y
    ceiling_y    = div1_y + DIV_H

    def cell_pair(y, h, color, l_main, l_sub, r_main, r_sub,
                  main_size=11, sub_size=10):
        draw_cell(ax, LX, y, CW, h, color=color, ec=TXT, lw=0.6)
        draw_cell(ax, RX, y, CW, h, color=color, ec=TXT, lw=0.6)
        if l_sub:
            label(ax, LX+CW/2, y+h*0.62, l_main, font=SANS_BOLD, size=main_size)
            label(ax, LX+CW/2, y+h*0.28, l_sub, font=SANS_REG, size=sub_size,
                  color=TXT_SOFT)
        else:
            label(ax, LX+CW/2, y+h/2, l_main, font=SANS_BOLD, size=main_size)
        if r_sub:
            label(ax, RX+CW/2, y+h*0.62, r_main, font=SANS_BOLD, size=main_size)
            label(ax, RX+CW/2, y+h*0.28, r_sub, font=SANS_REG, size=sub_size,
                  color=TXT_SOFT)
        else:
            label(ax, RX+CW/2, y+h/2, r_main, font=SANS_BOLD, size=main_size)

    # Ceiling = Exodus (orange)
    cell_pair(ceiling_y, LH, ORANGE_CELL,
              'ceiling', 'astronomical scenes (Nut)',
              'Exodus', 'sapphire pavement (Unit 10)')

    # Divider 1
    draw_cell(ax, LX, div1_y, CW, DIV_H, color=DIVIDER, lw=0)
    draw_cell(ax, RX, div1_y, CW, DIV_H, color=DIVIDER, lw=0)

    # Middle 3 sub-rows (the journey itself)
    sub_rows = [
        (LIGHT_CYAN,  'upper register',  'celestial backdrop',
                       'Row 1',           'transcendent'),
        (LIGHT_PERI,  'middle register', 'the divine barque',
                       'Row 2',           'interface'),
        (LIGHT_GREEN, 'lower register',  'chthonic forces',
                       'Row 3',           'earthly'),
    ]
    for i, (color, lm, ls, rm, rs) in enumerate(sub_rows):
        y = middle_top_y - (i+1)*INNER_H
        draw_cell(ax, LX, y, CW, INNER_H, color=color, ec=TXT, lw=0.5)
        label(ax, LX+CW/2, y+INNER_H*0.62, lm, font=SANS_BOLD, size=10)
        label(ax, LX+CW/2, y+INNER_H*0.28, ls, font=SANS_REG, size=9,
              color=TXT_SOFT)
        draw_cell(ax, RX, y, CW, INNER_H, color=color, ec=TXT, lw=0.5)
        label(ax, RX+CW/2, y+INNER_H*0.62, rm, font=SANS_BOLD, size=10)
        label(ax, RX+CW/2, y+INNER_H*0.28, rs, font=SANS_REG, size=9,
              color=TXT_SOFT)
    # Wall-level outer labels
    label(ax, LX-0.20, middle_bot_y + 3*INNER_H/2,
          'walls\n(the Amduat journey)',
          size=10, ha='right', font=SANS_BOLD, color=TXT_SOFT)
    label(ax, RX+CW+0.20, middle_bot_y + 3*INNER_H/2,
          'Gen \u00b7 Lev \u00b7 Deut\n(the horizontal thread)',
          size=10, ha='left', font=SANS_BOLD, color=TXT_SOFT)

    # Divider 2
    draw_cell(ax, LX, div2_y, CW, DIV_H, color=DIVIDER, lw=0)
    draw_cell(ax, RX, div2_y, CW, DIV_H, color=DIVIDER, lw=0)

    # Floor = Numbers (orange)
    cell_pair(floor_y, LH, ORANGE_CELL,
              'floor', 'Book of the Earth',
              'Numbers', 'earth opens for Korach (Unit 7)')

    # Column headers
    label(ax, LX+CW/2, ceiling_y+LH+0.32, 'The royal tomb',
          font=SERIF_BOLD, size=12, va='bottom')
    label(ax, RX+CW/2, ceiling_y+LH+0.32, 'The vertical thread',
          font=SERIF_BOLD, size=12, va='bottom')

    label(ax, FW/2, BOT-0.40,
          'Two levels around the journey; three registers within it.',
          size=10, va='top', color=TXT_SOFT)
    label(ax, FW/2, FH-0.15,
          'Figure 13.  Torah and Amduat: Architecture at Two Scales',
          font=SERIF_BOLD, size=14, va='top')
    save(fig, 'fig-13-torah-amduat-correspondence')


# ============================================================
# FIGURE 14: Torah and Amduat side by side
# ============================================================
def fig14():
    FW, FH = 11.5, 8.0
    fig, ax = make_fig(FW, FH)

    CELL = 0.22
    GEN_W = 7*CELL; LEV_W = 7*CELL; DEUT_W = 5*CELL
    BAND_H = 3*CELL; BAND_W = GEN_W + LEV_W + DEUT_W
    EX_W = 5*CELL; EX_H = 9*CELL
    NUM_W = 5*CELL; NUM_H = 5*CELL
    DIV_H = CELL
    TOTAL_H = EX_H + DIV_H + BAND_H + DIV_H + NUM_H

    LX_torah = 0.6
    LY_torah = 1.6
    num_y = LY_torah
    div2_y = num_y + NUM_H
    band_y = div2_y + DIV_H
    div1_y = band_y + BAND_H
    ex_y = div1_y + DIV_H
    gen_x = LX_torah
    lev_x = LX_torah + GEN_W
    deut_x = LX_torah + GEN_W + LEV_W
    lev_center_x = lev_x + LEV_W/2
    ex_x = lev_center_x - EX_W/2
    num_x = lev_center_x - NUM_W/2

    draw_cell(ax, gen_x, band_y, GEN_W, BAND_H, color=LIGHT_CYAN,
              ec=BOOK_FRAME['genesis'], lw=1.5)
    label(ax, gen_x+GEN_W/2, band_y+BAND_H/2, 'Genesis',
          font=SANS_BOLD, size=9, color=BOOK_FRAME['genesis'])
    draw_cell(ax, lev_x, band_y, LEV_W, BAND_H, color=LIGHT_PERI,
              ec=BOOK_FRAME['leviticus'], lw=1.5)
    draw_cell(ax, lev_x+3*CELL, band_y+CELL, CELL, CELL,
              color=INDEP_FILL, ec=INDEP_BORDER, lw=1.0)
    draw_cell(ax, deut_x, band_y, DEUT_W, BAND_H, color=LIGHT_GREEN,
              ec=BOOK_FRAME['deuteronomy'], lw=1.5)
    label(ax, deut_x+DEUT_W/2, band_y+BAND_H/2, 'Deut',
          font=SANS_BOLD, size=9, color=BOOK_FRAME['deuteronomy'])

    div_x = lev_center_x - LEV_W/2
    draw_cell(ax, div_x, div1_y, LEV_W, DIV_H, color=DIVIDER, lw=0)
    draw_cell(ax, div_x, div2_y, LEV_W, DIV_H, color=DIVIDER, lw=0)
    label(ax, lev_center_x, div1_y+DIV_H/2, 'Leviticus',
          font=SANS_BOLD, size=9, color=TXT)

    draw_cell(ax, ex_x, ex_y, EX_W, EX_H, color=ORANGE_CELL,
              ec=BOOK_FRAME['exodus'], lw=1.5)
    label(ax, ex_x+EX_W/2, ex_y+EX_H/2, 'Exodus',
          font=SANS_BOLD, size=10, color=BOOK_FRAME['exodus'])
    draw_cell(ax, ex_x+2*CELL, ex_y+EX_H/2-CELL/2, CELL, CELL,
              color=INDEP_FILL, ec=INDEP_BORDER, lw=1.0)

    draw_cell(ax, num_x, num_y, NUM_W, NUM_H, color=ORANGE_CELL,
              ec=BOOK_FRAME['numbers'], lw=1.5)
    label(ax, num_x+NUM_W/2, num_y+NUM_H/2, 'Numbers',
          font=SANS_BOLD, size=10, color=BOOK_FRAME['numbers'])
    draw_cell(ax, num_x+2*CELL, num_y+2*CELL, CELL, CELL,
              color=INDEP_FILL, ec=INDEP_BORDER, lw=1.0)

    label(ax, LX_torah+BAND_W/2, LY_torah+TOTAL_H+0.30,
          'The Torah: 19 \u00d7 19',
          font=SANS_BOLD, size=12, va='bottom')

    ACW, ACH = 0.36, 0.85
    AX, AY = 7.0, 2.6
    AG_W, AG_H = 12*ACW, 3*ACH
    def acx(c): return AX + c*ACW
    def acy(r): return AY + AG_H - (r+1)*ACH

    for r in range(3):
        for c in range(12):
            color = [LIGHT_CYAN, LIGHT_PERI, LIGHT_GREEN][r]
            draw_cell(ax, acx(c), acy(r), ACW, ACH, color=color,
                      ec=LIGHT_GRID, lw=0.4)
    for r in (1, 2):
        ax.plot([AX, AX+AG_W], [AY + r*ACH, AY + r*ACH],
                color=DIVIDER, lw=2.0, zorder=4)
    draw_border(ax, AX, AY, AG_W, AG_H, lw=0.9)

    h6 = acx(5) + ACW/2
    ax.plot([h6, h6], [AY-0.04, AY+AG_H+0.10], color=INDEP_BORDER,
            lw=1.5, ls='--')
    label(ax, h6, AY+AG_H+0.16, 'Hour 6',
          font=SANS_BOLD, size=10, va='bottom', color=INDEP_BORDER)

    for r, name in enumerate(['upper', 'middle', 'lower']):
        label(ax, AX+AG_W+0.14, acy(r)+ACH/2, name, size=10, ha='left',
              color=TXT_SOFT)

    label(ax, AX+AG_W/2, AY+AG_H+0.55,
          'The Amduat: 12 hours \u00d7 3 registers',
          font=SANS_BOLD, size=12, va='bottom')

    label(ax, FW/2, 0.85,
          'Shared features: sequential journey  \u00b7  three semantic registers  \u00b7  '
          'central pivot  \u00b7  register dividers  \u00b7  square / rectangular module',
          size=10, va='center', color=TXT_SOFT)
    label(ax, FW/2, FH-0.15,
          'Figure 14.  The Torah and the Amduat: One Compositional Paradigm',
          font=SERIF_BOLD, size=14, va='top')
    save(fig, 'fig-14-torah-amduat-side-by-side')


# ============================================================
# FIGURE 14 (formerly 15): The Beautiful Weave — Deuteronomy Unit 8
# 5 pairs x 2 sub-rows x 3 columns. Template based on Fig 1.
# ============================================================
def fig15():
    CW, CH = 1.50, 0.50
    COLS, ROWS = 3, 10
    ML, MR, BOT, TOP = 3.0, 0.7, 1.05, 1.85
    GW, GH = COLS*CW, ROWS*CH
    FW, FH = ML+GW+MR, BOT+GH+TOP
    fig, ax = make_fig(FW, FH)
    def cx(c): return ML + c*CW
    def ry(r): return BOT + GH - (r+1)*CH

    # Verse refs per (row, col)
    verses = [
        ['21:10',   '22:13',   '24:1'],   # a-i
        ['21:15',   '22:22',   '24:5'],   # a-ii
        ['21:18',   '23:2',    '24:7'],   # b-i
        ['21:22',   '23:10',   '24:8'],   # b-ii
        ['22:1',    '23:16',   '24:10'],  # c-i
        ['22:4',    '23:18',   '24:14'],  # c-ii
        ['22:5',    '23:20',   '24:16'],  # d-i
        ['22:6',    '23:22',   '24:17'],  # d-ii
        ['22:8',    '23:25',   '24:19'],  # e-i
        ['22:10',   '23:26',   '24:20'],  # e-ii
    ]

    # Three-column CSS palette
    col_colors = [COL_L, COL_M, COL_R]
    col_txt    = [COL_L_TXT, COL_M_TXT, COL_R_TXT]

    for r in range(ROWS):
        for c in range(COLS):
            draw_cell(ax, cx(c), ry(r), CW, CH, color=col_colors[c],
                      ec=LIGHT_GRID, lw=0.5)
            label(ax, cx(c)+CW/2, ry(r)+CH/2, verses[r][c],
                  font=SANS_REG, size=10, color=col_txt[c])

    # Deuteronomy book frame
    ax.add_patch(mpatches.Rectangle(
        (ML-0.06, BOT-0.06), GW+0.12, GH+0.12,
        lw=0, fc=BOOK_BG_TINT['deuteronomy'], zorder=0))
    ax.add_patch(mpatches.Rectangle(
        (ML-0.06, BOT-0.06), GW+0.12, GH+0.12,
        lw=2.4, ec=BOOK_FRAME['deuteronomy'], fc='none', zorder=5))

    # Pair labels on the left (each pair spans two sub-rows)
    pair_names = ['Pair 1', 'Pair 2', 'Pair 3', 'Pair 4', 'Pair 5']
    for p in range(5):
        # Pair p occupies rows 2p and 2p+1
        y_pair_top = ry(2*p) + CH      # top of upper sub-row
        y_pair_bot = ry(2*p+1)         # bottom of lower sub-row
        y_mid = (y_pair_top + y_pair_bot) / 2
        label(ax, ML-0.55, y_mid, pair_names[p], size=11, ha='right',
              font=SANS_BOLD, color=ACCENT_BR)
        # Sub-row markers (i / ii) — small, in margin
        label(ax, ML-0.12, ry(2*p)+CH/2, 'i', size=9, ha='right',
              color=TXT_SOFT, alpha=0.7)
        label(ax, ML-0.12, ry(2*p+1)+CH/2, 'ii', size=9, ha='right',
              color=TXT_SOFT, alpha=0.7)
        # Faint line separating pairs (between p and p+1) — except after last
        if p < 4:
            yline = ry(2*p+1)
            ax.plot([cx(0), cx(0)+GW], [yline, yline],
                    color=ACCENT_BR, lw=1.2, alpha=0.4, zorder=3)

    # Column headers above
    top = BOT + GH
    heads = [
        ('L', 'self'),
        ('M', 'self-and-other'),
        ('R', 'other'),
    ]
    for c, (h1, h2) in enumerate(heads):
        x = cx(c)+CW/2
        label(ax, x, top+0.55, h1, font=SANS_BOLD, size=12, va='bottom')
        label(ax, x, top+0.20, h2, font=SANS_REG, size=10, va='bottom',
              color=TXT_SOFT)

    # Caption
    label(ax, ML+GW/2, BOT-0.34,
          'Deuteronomy Unit 8 (21:10\u201325:4) \u2014 five pairs of laws, three columns.',
          size=10, va='top', color=TXT_SOFT)
    label(ax, ML+GW/2, FH-0.15,
          'Figure 14.  The Beautiful Weave: 5 Pairs \u00d7 3 Columns',
          font=SERIF_BOLD, size=13, va='top')
    save(fig, 'fig-14-beautiful-weave')


fig13()
fig15()  # now produces fig-14-beautiful-weave
print("\nFig 13 and (now) Fig 14 rebuilt.")
