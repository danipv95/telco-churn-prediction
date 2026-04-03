"""
design_system.py
================
Single source of truth for all visual tokens used in the
ChurnGuard Telco Analytics dashboard.

Palette:
  Primary  — Baltic Blue  #05668D  /  Rich Cerulean #427AA1
  Bg       — Alice Blue   #EBF2FA
  Accent   — Lime Moss    #A5BE00  /  Sage Green    #679436
  Neutrals — Blue-tinted grey scale anchored to the primary hue

Usage:
    from utils.design_system import COLORS, TYPOGRAPHY, SPACING, SHAPE, Tokens, css
    st.markdown(css(), unsafe_allow_html=True)
"""

# =============================================================================
# COLOR PRIMITIVES
# =============================================================================
class COLORS:
    # ── Blue-tinted slate scale (anchored to Baltic Blue) ────────────────────
    SLATE_950  = "#021e2b"   # deepest — sidebar bg
    SLATE_900  = "#03314a"   # page titles, dark text
    SLATE_800  = "#05668D"   # Baltic Blue — primary text / headers
    SLATE_700  = "#427AA1"   # Rich Cerulean — secondary text
    SLATE_600  = "#5a8fb5"   # muted text
    SLATE_400  = "#7aa8c4"   # axis labels, placeholders
    SLATE_300  = "#b8d4e8"   # borders light
    SLATE_200  = "#d4e8f5"   # card borders
    SLATE_100  = "#e4f0f8"   # chart grid lines
    SLATE_50   = "#EBF2FA"   # Alice Blue — page background

    # ── Primary scale (Baltic Blue family) ───────────────────────────────────
    PRIMARY_900 = "#021e2b"
    PRIMARY_800 = "#03314a"
    PRIMARY_700 = "#05668D"   # Baltic Blue
    PRIMARY_600 = "#427AA1"   # Rich Cerulean
    PRIMARY_500 = "#5a8fb5"
    PRIMARY_400 = "#7aa8c4"
    PRIMARY_100 = "#d4e8f5"
    PRIMARY_50  = "#EBF2FA"   # Alice Blue

    # ── Accent scale (Lime Moss / Sage Green) ────────────────────────────────
    ACCENT      = "#A5BE00"   # Lime Moss — highlights, CTAs
    ACCENT_DARK = "#679436"   # Sage Green — success, darker accent
    ACCENT_LT   = "#e8f2b3"   # light accent background

    # ── Semantic ─────────────────────────────────────────────────────────────
    SUCCESS     = "#679436"   # Sage Green
    SUCCESS_LT  = "#e8f2b3"
    WARNING     = "#c47d0e"
    WARNING_LT  = "#fef3c7"
    DANGER      = "#c0392b"
    DANGER_LT   = "#fde8e6"
    CRITICAL    = "#7c3aed"
    CRITICAL_LT = "#ede9fe"

    # ── Base ─────────────────────────────────────────────────────────────────
    WHITE = "#ffffff"
    BLACK = "#000000"


# =============================================================================
# TYPOGRAPHY  (DM Sans — same as main.py)
# =============================================================================
class TYPOGRAPHY:
    FONT      = "DM Sans"
    FONT_MONO = "DM Mono"
    FONT_URL  = "https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap"

    # Scale
    XS   = "11px"
    SM   = "12px"
    BASE = "14px"
    MD   = "15px"
    LG   = "18px"
    XL   = "22px"
    XXL  = "28px"
    XXXL = "36px"

    # Weight
    LIGHT  = "300"
    NORMAL = "400"
    MEDIUM = "500"
    SEMI   = "600"
    BOLD   = "700"
    BLACK  = "800"

    # Line height
    TIGHT     = "1.2"
    NORMAL_LH = "1.5"
    RELAXED   = "1.6"


# =============================================================================
# SPACING
# =============================================================================
class SPACING:
    S1  = "4px"
    S2  = "8px"
    S3  = "12px"
    S4  = "16px"
    S5  = "20px"
    S6  = "24px"
    S8  = "32px"
    S10 = "40px"
    S12 = "48px"


# =============================================================================
# BORDERS & SHADOWS
# =============================================================================
class SHAPE:
    RADIUS_SM   = "8px"
    RADIUS_MD   = "12px"
    RADIUS_LG   = "16px"
    RADIUS_XL   = "20px"
    RADIUS_FULL = "9999px"

    SHADOW_XS      = "0 1px 2px rgba(5,102,141,0.04)"
    SHADOW_SM      = "0 1px 4px rgba(5,102,141,0.07)"
    SHADOW_MD      = "0 4px 12px rgba(5,102,141,0.10)"
    SHADOW_LG      = "0 8px 24px rgba(5,102,141,0.13)"
    SHADOW_PRIMARY = "0 4px 14px rgba(5,102,141,0.22)"


# =============================================================================
# COMPONENT TOKENS
# =============================================================================
class Tokens:
    # ── Page ─────────────────────────────────────────────────────────────────
    PAGE_BG      = COLORS.SLATE_50       # Alice Blue
    PAGE_PADDING = f"{SPACING.S6} {SPACING.S8}"
    MAX_WIDTH    = "1400px"

    # ── Sidebar ──────────────────────────────────────────────────────────────
    SIDEBAR_BG     = COLORS.SLATE_950
    SIDEBAR_TEXT   = COLORS.PRIMARY_400
    SIDEBAR_HEADER = COLORS.WHITE
    SIDEBAR_MUTED  = "rgba(255,255,255,0.35)"
    SIDEBAR_BORDER = "rgba(255,255,255,0.08)"
    SIDEBAR_ACCENT = COLORS.PRIMARY_700
    SIDEBAR_HOVER  = "rgba(5,102,141,0.25)"

    # ── Cards ────────────────────────────────────────────────────────────────
    CARD_BG           = COLORS.WHITE
    CARD_BORDER       = COLORS.SLATE_200
    CARD_RADIUS       = SHAPE.RADIUS_LG
    CARD_SHADOW       = SHAPE.SHADOW_SM
    CARD_PADDING      = f"{SPACING.S5} {SPACING.S6}"
    CARD_HOVER_SHADOW = SHAPE.SHADOW_MD

    # ── KPI Cards ────────────────────────────────────────────────────────────
    KPI_VALUE_SIZE   = TYPOGRAPHY.XXL
    KPI_VALUE_WEIGHT = TYPOGRAPHY.BLACK
    KPI_VALUE_COLOR  = COLORS.SLATE_900
    KPI_LABEL_SIZE   = TYPOGRAPHY.XS
    KPI_LABEL_WEIGHT = TYPOGRAPHY.SEMI
    KPI_LABEL_COLOR  = COLORS.SLATE_400
    KPI_DELTA_SIZE   = TYPOGRAPHY.SM
    KPI_DELTA_COLOR  = COLORS.SLATE_400

    # ── Section headers ──────────────────────────────────────────────────────
    SECTION_TITLE_SIZE   = TYPOGRAPHY.MD
    SECTION_TITLE_WEIGHT = TYPOGRAPHY.BOLD
    SECTION_TITLE_COLOR  = COLORS.SLATE_900
    SECTION_DESC_SIZE    = TYPOGRAPHY.SM
    SECTION_DESC_COLOR   = COLORS.SLATE_400

    # ── Page headers ─────────────────────────────────────────────────────────
    PAGE_TITLE_SIZE   = TYPOGRAPHY.XL
    PAGE_TITLE_WEIGHT = TYPOGRAPHY.BLACK
    PAGE_TITLE_COLOR  = COLORS.SLATE_900
    PAGE_SUB_SIZE     = TYPOGRAPHY.SM
    PAGE_SUB_COLOR    = COLORS.SLATE_400

    # ── Charts ───────────────────────────────────────────────────────────────
    CHART_BG         = COLORS.WHITE
    CHART_GRID       = COLORS.SLATE_100
    CHART_AXIS_COLOR = COLORS.SLATE_400
    CHART_FONT_SIZE  = 11
    CHART_PRIMARY    = COLORS.PRIMARY_700   # Baltic Blue
    CHART_SECONDARY  = COLORS.PRIMARY_100
    CHART_ACCENT     = COLORS.ACCENT        # Lime Moss
    CHART_FONT       = TYPOGRAPHY.FONT

    # ── Insight boxes ─────────────────────────────────────────────────────────
    INSIGHT_BG        = COLORS.ACCENT_LT
    INSIGHT_BORDER    = COLORS.ACCENT
    INSIGHT_ACCENT    = COLORS.ACCENT_DARK
    INSIGHT_TEXT      = COLORS.SLATE_900
    INSIGHT_FONT_SIZE = TYPOGRAPHY.SM
    INSIGHT_LINE_HT   = TYPOGRAPHY.RELAXED

    # ── Risk semantic colors ─────────────────────────────────────────────────
    RISK_LOW      = COLORS.SUCCESS
    RISK_MEDIUM   = COLORS.WARNING
    RISK_HIGH     = COLORS.DANGER
    RISK_CRITICAL = COLORS.CRITICAL

    RISK_COLORS = {
        "Low":      COLORS.SUCCESS,
        "Medium":   COLORS.WARNING,
        "High":     COLORS.DANGER,
        "Critical": COLORS.CRITICAL,
    }

    # ── Borders ──────────────────────────────────────────────────────────────
    BORDER_DEFAULT = COLORS.SLATE_200
    BORDER_SUBTLE  = COLORS.SLATE_100
    DIVIDER        = COLORS.SLATE_200

    # ── Badge / tag ──────────────────────────────────────────────────────────
    BADGE_BG    = COLORS.PRIMARY_100
    BADGE_COLOR = COLORS.PRIMARY_700


# =============================================================================
# CHART HELPERS
# =============================================================================
class ChartTheme:
    """Reusable Plotly layout and axis configs."""

    @staticmethod
    def layout(title: str = "", height: int = 280) -> dict:
        return dict(
            title=dict(
                text=title,
                font=dict(size=13, color=Tokens.SECTION_TITLE_COLOR,
                          family=TYPOGRAPHY.FONT),
            ),
            height=height,
            margin=dict(l=10, r=10, t=30 if title else 10, b=10),
            paper_bgcolor=Tokens.CHART_BG,
            plot_bgcolor=Tokens.CHART_BG,
            font=dict(family=TYPOGRAPHY.FONT, color=Tokens.CHART_AXIS_COLOR,
                      size=Tokens.CHART_FONT_SIZE),
            showlegend=True,
            legend=dict(
                font=dict(size=11, family=TYPOGRAPHY.FONT),
                bgcolor="rgba(0,0,0,0)",
            ),
        )

    @staticmethod
    def axis() -> dict:
        return dict(
            showgrid=True,
            gridcolor=Tokens.CHART_GRID,
            gridwidth=1,
            showline=False,
            zeroline=False,
            tickfont=dict(size=11, color=Tokens.CHART_AXIS_COLOR,
                          family=TYPOGRAPHY.FONT),
        )

    @staticmethod
    def gradient_primary() -> dict:
        return {
            "type": "linear", "x": 0, "y": 0, "x2": 0, "y2": 1,
            "colorStops": [
                {"offset": 0, "color": COLORS.PRIMARY_700},
                {"offset": 1, "color": COLORS.PRIMARY_600},
            ]
        }

    @staticmethod
    def gradient_primary_h() -> dict:
        return {
            "type": "linear", "x": 1, "y": 0, "x2": 0, "y2": 0,
            "colorStops": [
                {"offset": 0, "color": COLORS.PRIMARY_700},
                {"offset": 1, "color": COLORS.PRIMARY_600},
            ]
        }

    TOOLTIP = dict(
        backgroundColor=COLORS.SLATE_900,
        borderColor=COLORS.SLATE_900,
        textStyle={"color": COLORS.WHITE, "fontSize": 11,
                   "fontFamily": TYPOGRAPHY.FONT},
    )


# =============================================================================
# GLOBAL CSS
# =============================================================================
def css() -> str:
    return f"""
<style>
@import url('{TYPOGRAPHY.FONT_URL}');

*, html, body {{ font-family: '{TYPOGRAPHY.FONT}', sans-serif !important; box-sizing: border-box; }}
.stApp {{ background-color: {Tokens.PAGE_BG} !important; }}
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main {{ background-color: {Tokens.PAGE_BG} !important; }}
.block-container {{ padding: 2rem 2.5rem !important; max-width: {Tokens.MAX_WIDTH} !important; }}

[data-testid="stSidebar"] {{
    background-color: {Tokens.SIDEBAR_BG} !important;
    border-right: 1px solid {Tokens.SIDEBAR_BORDER} !important;
}}
[data-testid="stSidebar"] > div:first-child {{ padding: 1.5rem 1.2rem !important; }}
[data-testid="stSidebar"] * {{ color: {COLORS.WHITE} !important; }}
[data-testid="stSidebar"] hr {{ border-color: {Tokens.SIDEBAR_BORDER} !important; margin: 1rem 0 !important; }}
[data-testid="stSidebar"] .stRadio > label {{ display: none !important; }}
[data-testid="stSidebar"] .stRadio > div {{ gap: 1px !important; }}
[data-testid="stSidebar"] .stRadio label {{
    background: transparent !important; border-radius: {SHAPE.RADIUS_SM} !important;
    padding: 9px 12px !important; font-size: {TYPOGRAPHY.BASE} !important;
    font-weight: {TYPOGRAPHY.NORMAL} !important; line-height: {TYPOGRAPHY.TIGHT} !important;
    cursor: pointer !important; transition: background 0.12s ease !important;
    border: none !important; outline: none !important; box-shadow: none !important;
    color: rgba(255,255,255,0.5) !important; width: 100% !important; display: block !important;
}}
[data-testid="stSidebar"] .stRadio label:hover {{
    background: {Tokens.SIDEBAR_HOVER} !important; color: rgba(255,255,255,0.9) !important;
}}
[data-testid="stSidebar"] .stRadio label p {{ margin: 0 !important; font-size: {TYPOGRAPHY.BASE} !important; }}
[data-testid="stSidebar"] .stRadio label > div:first-child {{ display: none !important; }}
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSlider label {{
    font-size: {TYPOGRAPHY.XS} !important; font-weight: {TYPOGRAPHY.SEMI} !important;
    text-transform: uppercase !important; letter-spacing: 0.8px !important;
    color: {Tokens.SIDEBAR_MUTED} !important;
}}
[data-testid="stSidebar"] [data-baseweb="select"] > div {{
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid {Tokens.SIDEBAR_BORDER} !important;
    border-radius: {SHAPE.RADIUS_SM} !important;
}}

[data-testid="metric-container"] {{
    background-color: {Tokens.CARD_BG}; border: 1px solid {Tokens.CARD_BORDER};
    border-radius: {Tokens.CARD_RADIUS}; padding: {SPACING.S5};
    box-shadow: {Tokens.CARD_SHADOW}; transition: box-shadow 0.15s;
}}
[data-testid="metric-container"]:hover {{ box-shadow: {Tokens.CARD_HOVER_SHADOW}; }}
[data-testid="stMetricLabel"] {{
    color: {Tokens.KPI_LABEL_COLOR} !important; font-size: {Tokens.KPI_LABEL_SIZE} !important;
    font-weight: {Tokens.KPI_LABEL_WEIGHT} !important; text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
}}
[data-testid="stMetricValue"] {{
    color: {Tokens.KPI_VALUE_COLOR} !important; font-size: {Tokens.KPI_VALUE_SIZE} !important;
    font-weight: {Tokens.KPI_VALUE_WEIGHT} !important; letter-spacing: -0.5px !important;
}}
[data-testid="stMetricDelta"] {{ font-size: {Tokens.KPI_DELTA_SIZE} !important; }}

h1 {{
    color: {Tokens.PAGE_TITLE_COLOR} !important; font-size: {Tokens.PAGE_TITLE_SIZE} !important;
    font-weight: {Tokens.PAGE_TITLE_WEIGHT} !important; letter-spacing: -0.3px !important;
}}
h2 {{
    color: {Tokens.SECTION_TITLE_COLOR} !important; font-size: {Tokens.SECTION_TITLE_SIZE} !important;
    font-weight: {Tokens.SECTION_TITLE_WEIGHT} !important;
}}
h3 {{
    color: {Tokens.SECTION_TITLE_COLOR} !important; font-size: {TYPOGRAPHY.MD} !important;
    font-weight: {TYPOGRAPHY.SEMI} !important;
}}

.ds-card {{
    background: {Tokens.CARD_BG}; border: 1px solid {Tokens.CARD_BORDER};
    border-radius: {Tokens.CARD_RADIUS}; padding: {Tokens.CARD_PADDING};
    box-shadow: {Tokens.CARD_SHADOW}; margin-bottom: {SPACING.S4}; transition: box-shadow 0.15s;
}}
.ds-card:hover {{ box-shadow: {Tokens.CARD_HOVER_SHADOW}; }}

.ds-section-title {{
    font-size: {Tokens.SECTION_TITLE_SIZE}; font-weight: {Tokens.SECTION_TITLE_WEIGHT};
    color: {Tokens.SECTION_TITLE_COLOR}; margin: 0 0 2px 0; letter-spacing: -0.1px;
}}
.ds-section-desc {{
    font-size: {Tokens.SECTION_DESC_SIZE}; color: {Tokens.SECTION_DESC_COLOR};
    margin: 0 0 {SPACING.S4} 0;
}}

.ds-page-title {{
    font-size: {Tokens.PAGE_TITLE_SIZE}; font-weight: {Tokens.PAGE_TITLE_WEIGHT};
    color: {Tokens.PAGE_TITLE_COLOR}; margin: 0 0 4px 0; letter-spacing: -0.3px;
}}
.ds-page-subtitle {{ font-size: {Tokens.PAGE_SUB_SIZE}; color: {Tokens.PAGE_SUB_COLOR}; margin: 0; }}

.ds-insight {{
    background: {Tokens.INSIGHT_BG}; border: 1px solid {Tokens.INSIGHT_BORDER};
    border-left: 3px solid {Tokens.INSIGHT_ACCENT};
    border-radius: 0 {SHAPE.RADIUS_SM} {SHAPE.RADIUS_SM} 0;
    padding: {SPACING.S3} {SPACING.S4}; margin-top: {SPACING.S4};
    font-size: {Tokens.INSIGHT_FONT_SIZE}; color: {Tokens.INSIGHT_TEXT};
    line-height: {Tokens.INSIGHT_LINE_HT};
}}

.ds-divider {{ height: 1px; background: {Tokens.DIVIDER}; margin: {SPACING.S5} 0; border: none; }}

div[data-testid="stDataFrame"] {{
    border: 1px solid {Tokens.CARD_BORDER} !important;
    border-radius: {SHAPE.RADIUS_MD} !important; overflow: hidden !important;
}}

.stDownloadButton > button {{
    background: {COLORS.PRIMARY_700} !important; color: {COLORS.WHITE} !important;
    border: none !important; border-radius: {SHAPE.RADIUS_SM} !important;
    font-size: {TYPOGRAPHY.SM} !important; font-weight: {TYPOGRAPHY.SEMI} !important;
    padding: 7px 18px !important; box-shadow: {SHAPE.SHADOW_PRIMARY} !important;
    transition: background 0.15s !important;
}}
.stDownloadButton > button:hover {{ background: {COLORS.PRIMARY_800} !important; }}

[data-testid="stSlider"] [role="slider"] {{ background: {COLORS.PRIMARY_700} !important; }}

#MainMenu, footer, header {{ visibility: hidden; }}
</style>
"""


# =============================================================================
# SHORTHAND ALIASES
# =============================================================================
NAVY    = COLORS.SLATE_900
BLUE    = COLORS.PRIMARY_700
BLUE_LT = COLORS.PRIMARY_100
BG      = Tokens.PAGE_BG
BORDER  = Tokens.CARD_BORDER
RED     = COLORS.DANGER
AMBER   = COLORS.WARNING
GREEN   = COLORS.SUCCESS
GRAY    = COLORS.SLATE_600
ACCENT  = COLORS.ACCENT

# Class-name aliases for backwards compat
Colors     = COLORS
Typography = TYPOGRAPHY
Spacing    = SPACING
Shape      = SHAPE
