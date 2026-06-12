"""
Unified palette derived from chaver.com Full Torah Map and main.css.
Cell colors carry inner-structure meaning per book (as established in the
deployed map); independents and impurities have a single consistent treatment
across all books.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm

SANS_REG  = fm.FontProperties(fname='/home/claude/InstrumentSans-Regular.ttf')
SANS_BOLD = fm.FontProperties(fname='/home/claude/InstrumentSans-Bold.ttf')
SERIF_REG = fm.FontProperties(fname='/home/claude/CrimsonPro-Regular.ttf')
SERIF_BOLD= fm.FontProperties(fname='/home/claude/CrimsonPro-Bold.ttf')

# === Site chrome (from main.css) ===
BG          = '#fdfcf8'
TXT         = '#1a1a1a'
TXT_SOFT    = '#666666'
ACCENT_BR   = '#8b7355'
DIVIDER     = '#a8a8a8'
GRID_LN     = 'rgba(0,0,0,0.2)'   # placeholder
CELL_BORDER = '#888888'           # full map uses rgba(0,0,0,0.2) -> ~#cccccc
LIGHT_GRID  = '#cccccc'
WHITE       = '#ffffff'

# === Cell colors (from chaver.com Full Torah Map) ===
LIGHT_CYAN     = '#D4F2FF'   # Outer ring (Lev A+H); Gen rows 1+3 outer cols; Deut "earthly" cells
LIGHT_GREEN    = '#E6FFEE'   # Middle ring (Lev B+G); Gen Row 3 (Elohim); Deut alternate
LIGHT_PERI     = '#D4D4FF'   # Inner ring (Lev D+F); Gen Row 2 (both names)
ORANGE_CELL    = '#FFCCAA'   # Exodus first-half quads; Numbers flag/corner units
MINT_CELL      = '#C8E6D2'   # Exodus second-half quads; Numbers regular units
IMPURE_GRAY    = '#F0F0F0'   # Lev impurities column
INDEP_FILL     = '#FFE6E6'   # All independent/focal cells across books
INDEP_BORDER   = '#CC0066'   # Independent/focal border

# === Book frame colors (from CSS) ===
GENESIS_FRAME    = '#7ab0f7'
GENESIS_BG       = 'rgba(122,176,247,0.1)'  # placeholder
EXODUS_FRAME     = '#f0b070'
LEVITICUS_FRAME  = '#80d0a0'
NUMBERS_FRAME    = '#f0b070'
DEUT_FRAME       = '#7ab0f7'

BOOK_FRAME = {
    'genesis': GENESIS_FRAME, 'exodus': EXODUS_FRAME,
    'leviticus': LEVITICUS_FRAME, 'numbers': NUMBERS_FRAME,
    'deuteronomy': DEUT_FRAME,
}

# Soft book backgrounds (10% tint) for inside the book frame
BOOK_BG_TINT = {
    'genesis': '#eaf3fd', 'deuteronomy': '#eaf3fd',
    'exodus': '#fef0e0', 'numbers': '#fef0e0',
    'leviticus': '#eaf7ee',
}

MIN_FONT = 10

def make_fig(width, height, dpi=300):
    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi)
    fig.patch.set_facecolor(BG)
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax

def draw_cell(ax, x, y, w, h, color=BG, ec=LIGHT_GRID, lw=0.5, zorder=2):
    ax.add_patch(mpatches.Rectangle(
        (x, y), w, h, lw=lw, ec=ec, fc=color, zorder=zorder))

def draw_border(ax, x, y, w, h, lw=1.4, ec=TXT, zorder=5):
    ax.add_patch(mpatches.Rectangle(
        (x, y), w, h, lw=lw, ec=ec, fc='none', zorder=zorder))

def draw_book_frame(ax, x, y, w, h, book, lw=3.0, pad=0.06):
    """Outer book identity frame in the book's CSS color, with soft tint background.
    Frame is drawn slightly outside the cell area so cells touch their own borders."""
    # Soft tint background
    ax.add_patch(mpatches.Rectangle(
        (x-pad, y-pad), w+2*pad, h+2*pad,
        lw=0, fc=BOOK_BG_TINT[book], zorder=1))
    # Book frame
    ax.add_patch(mpatches.Rectangle(
        (x-pad, y-pad), w+2*pad, h+2*pad,
        lw=lw, ec=BOOK_FRAME[book], fc='none', zorder=4))

def label(ax, x, y, text, font=None, size=MIN_FONT, color=TXT,
          ha='center', va='center', rotation=0, alpha=1.0, zorder=6):
    if font is None:
        font = SANS_REG
    ax.text(x, y, text, ha=ha, va=va, rotation=rotation,
            fontproperties=font, fontsize=max(size, MIN_FONT),
            color=color, alpha=alpha, zorder=zorder)

def save(fig, name):
    pdf = f'/mnt/user-data/outputs/{name}.pdf'
    png = f'/mnt/user-data/outputs/{name}.png'
    fig.savefig(pdf, bbox_inches='tight', pad_inches=0.15)
    fig.savefig(png, bbox_inches='tight', pad_inches=0.15, dpi=300)
    plt.close()
    print(f"Saved: {pdf}")

print("fig_utils v3 loaded")

# === Three-column unit palette (from CSS .scripture-table th.col-*) ===
# Left / col-a: dark warm brown
COL_L      = '#8b7355'
COL_L_TXT  = '#fdfcf8'   # light text on dark column
# Middle / col-b: medium tan (also used by header gradient)
COL_M      = '#c9b899'
COL_M_TXT  = '#3d2f1f'
# Right / col-c: light cream
COL_R      = '#fef5e7'
COL_R_TXT  = '#5d4e37'
