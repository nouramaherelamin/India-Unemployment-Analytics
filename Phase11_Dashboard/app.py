from pathlib import Path
import base64
import json
from urllib.request import urlopen

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ============================================================
# INDIA UNEMPLOYMENT ANALYTICS — PHASE 11
# ============================================================
# Resolve asset paths from the location of app.py, not the
# directory from which Streamlit happens to be launched.
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
ASSET_DIR = BASE_DIR / "assets"

# Use the real Indian flag image as the browser tab icon.
# Prefer a dedicated square favicon; fall back to the existing
# Indian flag wave image if the dedicated file is not present.
FLAG_ICON = ASSET_DIR / "india_flag.png"
if not FLAG_ICON.exists():
    FLAG_ICON = ASSET_DIR / "india_flag_wave.png"

st.set_page_config(
    page_title="India Unemployment Analytics",
    page_icon=str(FLAG_ICON),
    layout="wide",
    initial_sidebar_state="expanded",
)

UNEMP = "Estimated Unemployment Rate (%)"
PART = "Estimated Labour Participation Rate (%)"
EMPLOYED = "Estimated Employed"
COVID_START = pd.Timestamp("2020-03-01")

GREEN = "#006B5B"
GREEN_DARK = "#003E36"
GREEN_2 = "#0B806B"
SAFFRON = "#F28C18"
SAFFRON_2 = "#FFB43B"
NAVY = "#102E55"
RED = "#D92D20"
BLUE = "#2468B1"
TEAL = "#138A72"
BG = "#F3F7F5"
CARD = "#FFFFFF"
LINE = "#D8E6E1"
TEXT = "#10243F"
MUTED = "#66768A"
GRID = "rgba(16,36,63,.10)"

PAGES = [
    "Overview", "National Trends", "Regional Analysis", "Rural vs Urban",
    "Statistical Tests", "Clustering", "Anomaly Detection", "Forecasting",
    "Key Insights", "Data Explorer", "Limitations"
]

NAV_ICONS = {
    "Overview": "National Trends","Regional Analysis": "","Rural vs Urban": "",
    "Statistical Tests": "","Clustering": "","Anomaly Detection": "",
    "Forecasting": "","Key Insights": "","Data Explorer": "","Limitations": "",
}

# ------------------------------------------------------------
# Global CSS
# ------------------------------------------------------------
st.markdown(f"""
<style>
:root{{--green:{GREEN};--green-dark:{GREEN_DARK};--saffron:{SAFFRON};--navy:{NAVY};--bg:{BG};--card:{CARD};--line:{LINE};--text:{TEXT};--muted:{MUTED};}}
.stApp{{background:linear-gradient(180deg,#F7FAF9 0%,#EEF4F2 100%)!important;color:var(--text)!important;}}
.block-container{{max-width:1600px!important;padding:0 1rem 2rem!important;}}
.stApp .stMarkdown,.stApp .stMarkdown p,.stApp label,.stApp [data-testid="stWidgetLabel"],.stApp [data-testid="stWidgetLabel"] p{{color:var(--text)!important;}}
[data-testid="stCaptionContainer"],[data-testid="stCaptionContainer"] p{{color:var(--muted)!important;}}

/* Sidebar */
section[data-testid="stSidebar"]{{
    background:linear-gradient(180deg,rgba(0,49,43,.98),rgba(0,65,57,.99)),url("assets/sidebar_brand.png") bottom center/100% auto no-repeat!important;
    border-right:0!important;
}}
section[data-testid="stSidebar"] .block-container{{padding:1rem .75rem 1.2rem!important;}}
section[data-testid="stSidebar"] .stMarkdown,section[data-testid="stSidebar"] .stMarkdown p,section[data-testid="stSidebar"] label,section[data-testid="stSidebar"] [data-testid="stWidgetLabel"]{{color:white!important;}}
section[data-testid="stSidebar"] [data-testid="stRadio"] label{{border-radius:10px!important;padding:.5rem .6rem!important;color:#F4FBF9!important;transition:.18s ease;font-weight:650!important;}}
section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover{{background:rgba(255,255,255,.08)!important;transform:translateX(2px);}}
section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked){{background:linear-gradient(90deg,#F28C18,#F6A01D)!important;color:white!important;font-weight:850!important;box-shadow:0 6px 18px rgba(0,0,0,.18);}}
section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p,section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) span{{color:white!important;}}
section[data-testid="stSidebar"] [data-testid="stExpander"]{{background:rgba(255,255,255,.06)!important;border:1px solid rgba(255,255,255,.12)!important;border-radius:12px!important;}}
section[data-testid="stSidebar"] [data-testid="stExpander"] summary{{color:white!important;}}
.sidebar-brand{{position:relative;min-height:150px;padding:.35rem .55rem 1rem;border-bottom:1px solid rgba(255,255,255,.12);margin-bottom:.8rem;overflow:hidden;}}
.sidebar-brand-map{{position:absolute;top:0px;left:45%;transform:translateX(-50%);width:150px;z-index:1;}}
.sidebar-brand-map img{{ width:150%; height:auto; display:block;}}
.sidebar-title{{position:relative;z-index:2;font-family:Georgia,serif;font-size:1.1rem;font-weight:900;color:#fff;line-height:1.03;margin-top:6.2rem;letter-spacing:.03em;text-align:left;}}
.sidebar-sub{{position:relative;z-index:2;font-size:.64rem;color:#B7D7D0;margin-top:.45rem;line-height:1.4;}}
.sidebar-foot{{margin-top:1rem;padding:.8rem;border:1px solid rgba(255,255,255,.11);border-radius:12px;background:rgba(0,0,0,.12);color:#D8ECE8;font-size:.65rem;line-height:1.5;}}

/* =========================================================
   HERO — image landmarks + integrated Indian flag
   ========================================================= */
.hero{{
    position:relative!important;
    overflow:hidden!important;
    background:#fff!important;
    border:1px solid #E5E1D7!important;
    border-radius:0 0 26px 26px!important;
    height:280px!important;
    min-height:280px!important;
    padding:2rem 2.5rem!important;
    margin:0 0 1.6rem!important;
    box-shadow:0 14px 36px rgba(16,35,63,.10)!important;
    isolation:isolate!important;
}}
.hero-bg{{
    position:absolute!important;
    right:0!important;
    top:0!important;
    width:62%!important;
    height:100%!important;
    object-fit:cover!important;
    object-position:right center!important;
    opacity:.92!important;
    mask-image:linear-gradient(90deg,transparent 0%,rgba(0,0,0,.08) 15%,rgba(0,0,0,.55) 42%,black 70%)!important;
    -webkit-mask-image:linear-gradient(90deg,transparent 0%,rgba(0,0,0,.08) 15%,rgba(0,0,0,.55) 42%,black 70%)!important;
    z-index:-3!important;
}}
.hero-wave{{
    position:absolute!important;
    left:-2%!important;
    bottom:-2px!important;
    width:70%!important;
    height:auto!important;
    max-height:none!important;
    object-fit:contain!important;
    object-position:left bottom!important;
    opacity:.84!important;
    z-index:-1!important;
    mask-image:linear-gradient(90deg,black 0%,black 45%,rgba(0,0,0,.75) 65%,transparent 100%)!important;
    -webkit-mask-image:linear-gradient(90deg,black 0%,black 45%,rgba(0,0,0,.75) 65%,transparent 100%)!important;
}}
.hero:before{{
    content:""!important;
    position:absolute!important;
    inset:0!important;
    background:linear-gradient(90deg,rgba(255,255,255,.90) 0%,rgba(255,255,255,.84) 27%,rgba(255,255,255,.58) 43%,rgba(255,255,255,.16) 67%,rgba(255,255,255,0) 100%)!important;
    z-index:0!important;
    pointer-events:none!important;
}}
.hero:after{{
    content:""!important;
    position:absolute!important;
    left:-100px!important;
    bottom:-100px!important;
    width:650px!important;
    height:190px!important;
    background:radial-gradient(ellipse,rgba(242,140,24,.12),transparent 70%)!important;
    z-index:0!important;
    pointer-events:none!important;
}}
.hero-grid{{
    position:relative!important;
    z-index:10!important;
    display:grid!important;
    grid-template-columns:minmax(0,1fr) auto!important;
    gap:2rem!important;
    align-items:center!important;
    height:235px!important;
    min-height:235px!important;
}}
.hero-grid > div:first-child{{
    position:relative!important;
    z-index:20!important;
    padding:.35rem .7rem .45rem!important;
    border-radius:14px!important;
    background:transparent!important;
    backdrop-filter:none!important;
}}
.hero-eyebrow{{color:#006B5B;font-family:Inter,Arial,sans-serif;font-size:.67rem;font-weight:800;letter-spacing:.16em;text-transform:uppercase;margin-bottom:.55rem;}}
.hero-title{{font-family:Inter,Arial,sans-serif;font-size:clamp(2.25rem,4vw,3.65rem);line-height:.98;margin:0;color:#102E55;font-weight:900;letter-spacing:-.035em;text-transform:uppercase;white-space:nowrap;text-shadow:0 1px 2px rgba(255,255,255,.9);}}
.hero-title .green{{color:#006B5B;}}.hero-title .saffron{{color:#E8750B;}}
.hero-sub{{font-family:Inter,Arial,sans-serif;font-size:.82rem;color:#173A64;margin-top:.75rem;max-width:760px;line-height:1.55;font-weight:600;text-shadow:0 1px 2px rgba(255,255,255,.95);}}
.hero-badge{{position:relative;z-index:30;justify-self:end;text-align:center;background:linear-gradient(135deg,#123B68,#102E55);color:#fff;padding:.58rem 1rem;border-radius:12px;font-family:Inter,Arial,sans-serif;font-weight:800;font-size:.72rem;white-space:nowrap;box-shadow:0 8px 18px rgba(18,49,91,.20);}}
.hero-mini{{margin-top:.45rem;font-family:Inter,Arial,sans-serif;font-size:.62rem;color:#4D657C;font-weight:700;letter-spacing:.01em;}}

/* KPI / cards */
.kpi-grid{{display:grid;grid-template-columns:repeat(5,1fr);gap:.7rem;margin:.7rem 0 1rem;}}
.kpi{{background:#fff;border:1px solid var(--line);border-radius:13px;padding:.78rem .85rem;min-height:106px;box-shadow:0 7px 18px rgba(16,35,63,.05);transition:.2s ease;}}
.kpi:hover{{transform:translateY(-3px);box-shadow:0 12px 25px rgba(16,35,63,.09);border-color:#C3D9D1;}}
.kpi-top{{display:flex;align-items:center;gap:.5rem;}}
.kpi-icon{{width:36px;height:36px;border-radius:10px;background:#EAF6F2;display:flex;align-items:center;justify-content:center;overflow:hidden;}}
.kpi-icon img{{width:29px;height:29px;object-fit:contain;}}
.kpi-label{{font-size:.65rem;color:var(--text);line-height:1.2;font-weight:750;}}
.kpi-value{{font-size:1.65rem;font-weight:900;color:var(--navy);line-height:1.1;margin-top:.4rem;}}
.kpi-note{{font-size:.59rem;color:var(--muted);margin-top:.2rem;}}
.section-head{{display:flex;align-items:center;gap:.5rem;margin:.45rem 0 .3rem;justify-content:space-between;}}
.section-left{{display:flex;align-items:center;gap:.5rem;}}
.section-icon{{width:30px;height:30px;border-radius:8px;background:#F0F7F4;display:flex;align-items:center;justify-content:center;overflow:hidden;flex:0 0 auto;}}
.section-icon img{{width:24px;height:24px;object-fit:contain;}}
.section-title{{font-size:1.1rem!important;font-weight:900!important;color:var(--navy)!important;letter-spacing:-.02em!important;}}
.section-subtitle{{font-size:.68rem!important;color:var(--muted)!important;}}
.section-badge{{margin-left:auto;font-size:.62rem;font-weight:750;color:var(--muted);background:#fff;border:1px solid var(--line);border-radius:8px;padding:.25rem .55rem;white-space:nowrap;}}
.insight{{background:#F7FBF9;border:1px solid #D8EAE4;border-left:4px solid var(--green);border-radius:12px;padding:.75rem .9rem;color:#27405E;line-height:1.45;font-size:.75rem;margin:.45rem 0 .7rem;}}
.insight strong{{color:var(--green);}}
[data-testid="stPlotlyChart"],[data-testid="stDataFrame"]{{background:#fff!important;border:1px solid var(--line)!important;border-radius:14px!important;box-shadow:0 7px 18px rgba(16,35,63,.045)!important;overflow:hidden!important;}}
[data-testid="stMetric"],
div[data-testid="stMetric"]{{
    background:#FFFFFF!important;
    border:1px solid #C7DCD5!important;
    border-radius:18px!important;
    min-height:112px!important;
    height:112px!important;
    padding:1rem 1.1rem!important;
    box-sizing:border-box!important;
    box-shadow:0 8px 22px rgba(16,35,63,.07)!important;
}}
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p{{
    color:#66768A!important;
    font-size:.76rem!important;
    font-weight:700!important;
    margin:0!important;
}}
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] div{{
    color:#102E55!important;
    font-size:2.05rem!important;
    font-weight:900!important;
    line-height:1.1!important;
    margin-top:.3rem!important;
}}
[data-baseweb="select"]>div{{background:#fff!important;border-color:var(--line)!important;color:var(--text)!important;}}
hr{{border-color:var(--line)!important;}} footer{{visibility:hidden;}}

.national-metrics{{
    width:100%!important;
    margin:.2rem 0 1.25rem!important;
}}
.national-metrics [data-testid="column"]{{
    min-width:0!important;
}}
@media(max-width:1000px){{
    .kpi-grid{{grid-template-columns:repeat(2,1fr);}}
    .hero{{height:270px!important;min-height:270px!important;}}
    .hero-grid{{grid-template-columns:1fr;height:225px;min-height:225px;}}
    .hero-bg{{width:65%;opacity:.45;}}
    .hero-wave{{width:75%;opacity:.58;}}
    .hero-badge{{justify-self:start;}}
    .hero-title{{font-size:2.5rem;white-space:normal;}}
}}
@media(max-width:650px){{
    .kpi-grid{{grid-template-columns:1fr;}}
    .hero{{height:250px!important;min-height:250px!important;padding:1.15rem!important;}}
    .hero-bg{{display:none;}}
    .hero-wave{{left:-12%;width:96%;height:auto!important;max-height:none!important;opacity:.42;}}
    .hero-grid{{height:210px!important;min-height:210px!important;grid-template-columns:1fr!important;}}
    .hero-title{{font-size:1.8rem;white-space:normal;}}
    .hero-sub{{font-size:.7rem;}}
    [data-testid="stMetric"]{{height:100px!important;min-height:100px!important;}}
}}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def asset_uri(name):
    p = ASSET_DIR / name
    if not p.exists():
        return ""
    mime = "image/png"
    if p.suffix.lower() in {".jpg", ".jpeg"}:
        mime = "image/jpeg"
    elif p.suffix.lower() == ".webp":
        mime = "image/webp"
    encoded = base64.b64encode(p.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def read_csv(name, **kwargs):
    p = DATA_DIR / name
    return pd.read_csv(p, **kwargs) if p.exists() else pd.DataFrame()


INDIA_GEOJSON_URL = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"


@st.cache_data(show_spinner=False, ttl=60 * 60 * 24)
def load_india_geojson():
    try:
        with urlopen(INDIA_GEOJSON_URL, timeout=6) as resp:
            geo = json.load(resp)
        for feat in geo.get("features", []):
            if feat.get("properties", {}).get("ST_NM") == "Ladakh":
                feat["properties"]["ST_NM"] = "Jammu & Kashmir"
        return geo
    except Exception:
        return None


def plot_layout(fig, height=330, title=None):
    fig.update_layout(
        height=height,
        title=title,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(color=TEXT, family="Arial, sans-serif", size=11),
        margin=dict(l=48, r=22, t=28 if title else 14, b=42),
        hoverlabel=dict(bgcolor=NAVY, font_color="white"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT, size=10)),
    )
    fig.update_xaxes(showgrid=False, linecolor="#C9D6D1", zeroline=False)
    fig.update_yaxes(gridcolor=GRID, linecolor="#C9D6D1", zeroline=False)
    return fig


def kpi(icon_file, label, value, note):
    uri = asset_uri(icon_file)
    icon_html = f'<img src="{uri}">' if uri else ""
    return f'<div class="kpi"><div class="kpi-top"><div class="kpi-icon">{icon_html}</div><div class="kpi-label">{label}</div></div><div class="kpi-value">{value}</div><div class="kpi-note">{note}</div></div>'


def section(title, subtitle="", badge=None):
    icon_map = {
        "National Trends": "section_national.png",
        "National Unemployment Trend": "section_national.png",
        "Regional Analysis": "section_regional.png",
        "Regional Unemployment — COVID Shock": "section_regional.png",
        "Rural vs Urban": "section_rural.png",
        "Rural vs Urban Unemployment Trend": "section_rural.png",
        "Statistical Tests": "sidebar_statistical_tests.png",
        "Clustering": "section_clusters(1).png",
        "Regional Clusters — PCA View": "section_clusters(1).png",
        "Anomaly Detection": "section_anomaly(1).png",
        "Anomaly Timeline": "section_anomaly(1).png",
        "Forecasting": "section_forecast(1).png",
        "Forecast vs Actual": "section_forecast(1).png",
        "Key Insights": "section_insights.png",
        "Limitations": "section_insights.png",
        "Data Explorer": "kpi_national.png",
    }
    uri = asset_uri(icon_map.get(title, "india_map.png"))
    icon_html = f'<img src="{uri}">' if uri else ""
    badge_html = f'<div class="section-badge">{badge}</div>' if badge else ""
    st.markdown(
        f'<div class="section-head"><div class="section-left"><div class="section-icon">{icon_html}</div><div><div class="section-title">{title}</div><div class="section-subtitle">{subtitle}</div></div></div>{badge_html}</div>',
        unsafe_allow_html=True,
    )


def fmt_p_values(frame):
    if frame.empty:
        return frame
    out = frame.copy()
    p_cols = [c for c in out.columns if c.lower().endswith("p_value") or c.lower().endswith("_p")]
    for c in p_cols:
        out[c] = out[c].apply(lambda v: "< 0.0001" if pd.notna(v) and v < 0.0001 else (f"{v:.4f}" if pd.notna(v) else v))
    return out

# ------------------------------------------------------------
# Load data
# ------------------------------------------------------------
df = read_csv("cleaned_data.csv")
if df.empty:
    st.error("cleaned_data.csv is missing from the data folder.")
    st.stop()

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Region"] = df["Region"].astype(str).str.strip()
df["Area"] = df["Area"].astype(str).str.strip()
df["Period"] = np.where(df["Date"] < COVID_START, "Pre-COVID", "COVID")
regions = sorted(df["Region"].dropna().unique())
areas = sorted(df["Area"].dropna().unique())

# ------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------
with st.sidebar:
    brand_map = asset_uri("india_map.png")
    st.markdown(
        f'''<div class="sidebar-brand"><div class="sidebar-brand-map"><img src="{brand_map}"></div><div class="sidebar-title">INDIA<br>UNEMPLOYMENT<br>ANALYTICS</div><div class="sidebar-sub">Regional Diagnostic · May 2019 — June 2020</div></div>''',
        unsafe_allow_html=True,
    )
    page = st.radio("Navigation", PAGES, format_func=lambda p: f"{NAV_ICONS.get(p,'')}  {p}", label_visibility="collapsed")
    with st.expander("FILTERS", expanded=False):
        selected_regions = st.multiselect("Region", regions, default=regions)
        selected_areas = st.multiselect("Area", areas, default=areas)
        selected_periods = st.multiselect("Period", ["Pre-COVID", "COVID"], default=["Pre-COVID", "COVID"])
        d0, d1 = df["Date"].min().date(), df["Date"].max().date()
        date_range = st.date_input("Date range", value=(d0, d1), min_value=d0, max_value=d1)
    st.markdown('<div class="sidebar-foot"><b>DATA FOR A STRONGER INDIA</b><br>740 clean observations · 28 regions · 2 areas · 14 monthly dates.<br><br><b>COVID PERIOD</b><br>March–June 2020.</div>', unsafe_allow_html=True)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
else:
    start_date, end_date = df["Date"].min(), df["Date"].max()

filtered = df[
    df["Region"].isin(selected_regions)
    & df["Area"].isin(selected_areas)
    & df["Period"].isin(selected_periods)
    & df["Date"].between(start_date, end_date)
].copy()

# ------------------------------------------------------------
# Header — flag is an image, blended into the hero
# ------------------------------------------------------------
peak_month = df.groupby("Date")[UNEMP].mean()
peak_value = float(peak_month.max())
peak_date = peak_month.idxmax()
hero_bg = asset_uri("india_hero.jpg")
wave = asset_uri("india_flag_wave.png")

st.markdown(
    f'''
    <div class="hero">
      <img class="hero-bg" src="{hero_bg}" alt="India landmarks">
      <img class="hero-wave" src="{wave}" alt="Indian tricolor">
      <div class="hero-grid">
        <div>
          <div class="hero-eyebrow">Labour Market Diagnostic · Complete Project</div>
          <h1 class="hero-title"><span class="green">INDIA</span> <span class="saffron">UNEMPLOYMENT</span> <span>ANALYTICS</span></h1>
          <div class="hero-sub">A data-driven analysis of employment trends, regional disparities, COVID-19 shock &amp; forecasting.</div>
          <div class="hero-mini">Cleaned dataset · 740 observations · 28 regions · 14 monthly dates</div>
        </div>
        <div><div class="hero-badge">2019 - 2020</div></div>
      </div>
    </div>
    ''',
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# Overview
# ------------------------------------------------------------
if page == "Overview":
    pre = df.loc[df["Period"] == "Pre-COVID", UNEMP].mean()
    covid = df.loc[df["Period"] == "COVID", UNEMP].mean()
    shock = covid - pre

    st.markdown(
        '<div class="kpi-grid">'
        + kpi("kpi_national.png", "National Average Unemployment", f"{df[UNEMP].mean():.2f}%", "Overall cleaned dataset")
        + kpi("kpi_peak.png", "Peak Unemployment Rate", f"{peak_value:.2f}%", peak_date.strftime("%B %Y"))
        + kpi("kpi_regions.png", "Regions Analyzed", "28", "20 fully covered · 8 incomplete")
        + kpi("kpi_rural.png", "Rural Average Rate", f"{df.loc[df.Area=='Rural',UNEMP].mean():.2f}%", "All available observations")
        + kpi("kpi_urban.png", "Urban Average Rate", f"{df.loc[df.Area=='Urban',UNEMP].mean():.2f}%", "All available observations")
        + '</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns(2, gap="medium")
    with left:
        section("National Unemployment Trend", "Monthly mean unemployment across all available regions and areas.", "National")
        monthly = df.groupby("Date", as_index=False)[UNEMP].mean().rename(columns={UNEMP: "Rate"})
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=monthly.Date, y=monthly.Rate, mode="lines+markers", name="Unemployment", line=dict(color=BLUE, width=3), marker=dict(size=6), fill="tozeroy", fillcolor="rgba(36,104,177,.08)"))
        fig.add_vrect(x0=COVID_START, x1=monthly.Date.max(), fillcolor="rgba(217,48,37,.08)", line_width=0)
        fig.add_vline(x=COVID_START, line_dash="dash", line_color=RED, annotation_text="COVID-19", annotation_position="top left")
        fig.update_yaxes(title="Unemployment Rate (%)")
        plot_layout(fig, 330)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with right:
        section("Regional Unemployment — COVID Shock", "Change in mean unemployment: COVID period minus pre-COVID period.", "COVID Shock")
        prof = read_csv("regional_profiles.csv")
        if not prof.empty:
            geo = load_india_geojson()
            if geo is not None and "Region" in prof.columns and "Shock_Magnitude_pp" in prof.columns:
                fig = px.choropleth(
                    prof, geojson=geo, locations="Region", featureidkey="properties.ST_NM",
                    color="Shock_Magnitude_pp", color_continuous_scale=["#FFFFFF", SAFFRON_2, SAFFRON, RED],
                    hover_name="Region", labels={"Shock_Magnitude_pp": "Change in unemployment (pp)"},
                )
                fig.update_traces(marker_line_color="#FFFFFF", marker_line_width=0.6)
                fig.update_geos(fitbounds="locations", visible=False, bgcolor="rgba(0,0,0,0)")
                fig.update_layout(height=330, margin=dict(l=0, r=0, t=6, b=0), paper_bgcolor="#FFFFFF", font=dict(color=TEXT, family="Arial, sans-serif"), coloraxis_colorbar=dict(title="Change in<br>Unemployment Rate<br>(pp)", thickness=12, len=.85))
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            else:
                top = prof.sort_values("Shock_Magnitude_pp", ascending=False).sort_values("Shock_Magnitude_pp")
                fig = px.bar(top, x="Shock_Magnitude_pp", y="Region", orientation="h")
                fig.update_traces(marker_color=np.where(top["Shock_Magnitude_pp"] >= 0, SAFFRON, TEAL))
                fig.update_xaxes(title="Change in unemployment (percentage points)")
                plot_layout(fig, 330)
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    left2, right2 = st.columns(2, gap="medium")
    with left2:
        section("Rural vs Urban Unemployment Trend", "Monthly means by area; the COVID period is highlighted.", "Both Areas")
        area_month = df.groupby(["Date", "Area"], as_index=False)[UNEMP].mean()
        fig = px.line(area_month, x="Date", y=UNEMP, color="Area", markers=True, color_discrete_map={"Rural": GREEN_2, "Urban": SAFFRON})
        fig.add_vrect(x0=COVID_START, x1=area_month.Date.max(), fillcolor="rgba(217,48,37,.06)", line_width=0)
        fig.update_yaxes(title="Unemployment Rate (%)")
        plot_layout(fig, 330)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with right2:
        section("Regional Clusters — PCA View", "K-Means selected k = 2 after silhouette diagnostics.", "PCA Clusters")
        scores = read_csv("pca_region_scores.csv")
        membership = read_csv("cluster_membership.csv")
        if not scores.empty and not membership.empty:
            if "Region" not in membership.columns and "Regions" in membership.columns:
                membership = membership.assign(Region=membership["Regions"].astype(str).str.split(",")).explode("Region")
                membership["Region"] = membership["Region"].str.strip()
            merge_key = "Region" if "Region" in scores.columns and "Region" in membership.columns else scores.columns[0]
            m = scores.merge(membership, on=merge_key, how="left")
            xcol = next((c for c in scores.columns if c.lower() in ["pc1", "pca1", "pc_1", "component_1"]), None)
            ycol = next((c for c in scores.columns if c.lower() in ["pc2", "pca2", "pc_2", "component_2"]), None)
            if xcol and ycol and "Cluster" in m.columns:
                fig = px.scatter(m, x=xcol, y=ycol, color="Cluster", hover_name=merge_key, color_discrete_sequence=[RED, GREEN_2, SAFFRON, BLUE])
                fig.update_xaxes(title="Principal Component 1")
                fig.update_yaxes(title="Principal Component 2")
                plot_layout(fig, 330)
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    a, b, c = st.columns([1, 1, 1], gap="medium")
    with a:
        section("Anomaly Timeline", "Combined IQR + rolling-z-score anomaly flags.", "Monthly")
        anomalies = read_csv("anomaly_log.csv")
        if not anomalies.empty:
            anomalies["Date"] = pd.to_datetime(anomalies["Date"], errors="coerce")
            mon = anomalies.groupby("Date").size().reset_index(name="Flags")
            fig = px.bar(mon, x="Date", y="Flags")
            fig.update_traces(marker_color=RED)
            plot_layout(fig, 270)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    with b:
        section("Forecast vs Actual", "Rolling-origin one-step-ahead benchmark; not a long-horizon forecast.", "Forecast Results")
        vals = read_csv("rolling_origin_forecast_values.csv")
        if not vals.empty:
            date_col = next((c for c in vals.columns if "date" in c.lower() or c.lower() == "ds"), None)
            if date_col:
                vals[date_col] = pd.to_datetime(vals[date_col], errors="coerce")
                actual_col = next((c for c in vals.columns if c.lower() in ["actual", "y_true", "observed"]), None)
                forecast_col = next((c for c in vals.columns if "drift" in c.lower()), None)
                if actual_col and forecast_col:
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=vals[date_col], y=vals[actual_col], mode="lines+markers", name="Actual", line=dict(color=BLUE, width=2.5)))
                    fig.add_trace(go.Scatter(x=vals[date_col], y=vals[forecast_col], mode="lines+markers", name="Drift", line=dict(color=SAFFRON, width=2, dash="dash")))
                    plot_layout(fig, 270)
                    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    with c:
        section("Key Insights", "Evidence synthesized from Phases 3–10.")
        st.markdown(f'<div class="insight"><strong>1 · COVID shock:</strong> mean unemployment rose from {pre:.2f}% pre-COVID to {covid:.2f}% during Mar–Jun 2020 (+{shock:.2f} pp).</div><div class="insight"><strong>2 · Peak:</strong> national mean unemployment reached {peak_value:.2f}% in {peak_date.strftime("%B %Y")}.</div><div class="insight"><strong>3 · Regional heterogeneity:</strong> Puducherry recorded the largest regional shock at +37.36 pp.</div><div class="insight"><strong>4 · Statistical caution:</strong> balanced Rural–Urban comparison was significant pre-COVID (p=.00039) but not during COVID (p=.14983).</div>', unsafe_allow_html=True)

elif page == "National Trends":
    section("National Trends", "Monthly national aggregates and pre-COVID vs COVID comparison.")
    monthly = filtered.groupby("Date", as_index=False).agg(Unemployment=(UNEMP, "mean"), Participation=(PART, "mean"), Employed=(EMPLOYED, "mean"))
    if monthly.empty:
        st.warning("No observations match the selected filters.")
    else:
        st.markdown('<div class="national-metrics">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 1, 1], gap="medium")
        c1.metric("Mean unemployment", f"{monthly.Unemployment.mean():.2f}%")
        c2.metric("Peak", f"{monthly.Unemployment.max():.2f}%")
        c3.metric("Mean participation", f"{monthly.Participation.mean():.2f}%")
        st.markdown('</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=monthly.Date, y=monthly.Unemployment, mode="lines+markers", name="Unemployment", line=dict(color=BLUE, width=3)))
        fig.add_trace(go.Scatter(x=monthly.Date, y=monthly.Participation, mode="lines+markers", name="Participation", line=dict(color=GREEN_2, width=2), yaxis="y2"))
        fig.add_vrect(x0=COVID_START, x1=monthly.Date.max(), fillcolor="rgba(217,48,37,.07)", line_width=0)
        fig.update_layout(yaxis=dict(title="Unemployment (%)"), yaxis2=dict(title="Participation (%)", overlaying="y", side="right"))
        plot_layout(fig, 430)
        st.plotly_chart(fig, use_container_width=True)
        period = filtered.groupby("Period", as_index=False)[UNEMP].mean()
        fig2 = px.bar(period, x="Period", y=UNEMP, text_auto=".2f", color="Period", color_discrete_map={"Pre-COVID": BLUE, "COVID": SAFFRON})
        plot_layout(fig2, 330)
        st.plotly_chart(fig2, use_container_width=True)

elif page == "Regional Analysis":
    section("Regional Analysis", "Regional baseline, COVID shock and recovery profile.")
    p = read_csv("regional_profiles.csv")
    if not p.empty:
        fig = px.bar(p.sort_values("Shock_Magnitude_pp"), x="Shock_Magnitude_pp", y="Region", orientation="h", color="Shock_Magnitude_pp", color_continuous_scale="Oranges")
        fig.update_layout(coloraxis_showscale=False)
        plot_layout(fig, 700)
        st.plotly_chart(fig, use_container_width=True)
        cols = [c for c in ["Region", "Coverage_Status", "Pre_COVID_Mean", "COVID_Mean", "Shock_Magnitude_pp", "June_2020_Mean", "Recovery_Status"] if c in p.columns]
        st.dataframe(p.sort_values("Shock_Magnitude_pp", ascending=False)[cols], use_container_width=True, hide_index=True)

elif page == "Rural vs Urban":
    section("Rural vs Urban", "Period-specific area comparison with the statistical tests from Phase 4.")
    area = filtered.groupby(["Period", "Area"], as_index=False)[UNEMP].mean()
    fig = px.bar(area, x="Period", y=UNEMP, color="Area", barmode="group", text_auto=".2f", color_discrete_map={"Rural": GREEN_2, "Urban": SAFFRON})
    plot_layout(fig, 390)
    st.plotly_chart(fig, use_container_width=True)
    mw = read_csv("mann_whitney_balanced_rural_vs_urban.csv")
    if not mw.empty:
        st.dataframe(fmt_p_values(mw), use_container_width=True, hide_index=True)
    st.markdown('<div class="insight"><strong>Interpretation:</strong> the balanced-region Mann–Whitney test was significant pre-COVID (p = .00039) and not significant during COVID (p = .14983). Effect sizes were small.</div>', unsafe_allow_html=True)

elif page == "Statistical Tests":
    section("Statistical Tests", "Correlations, Rural–Urban comparisons and regional Kruskal–Wallis evidence.")
    corr = read_csv("correlation_tests.csv")
    mw = read_csv("mann_whitney_balanced_rural_vs_urban.csv")
    kw = read_csv("kruskal_wallis_regional.csv")
    if not corr.empty:
        st.markdown("**Correlation tests**")
        st.dataframe(fmt_p_values(corr), use_container_width=True, hide_index=True)
    x, y = st.columns(2)
    with x:
        st.markdown("**Balanced Rural vs Urban**")
        if not mw.empty:
            st.dataframe(fmt_p_values(mw), use_container_width=True, hide_index=True)
    with y:
        st.markdown("**Regional differences**")
        if not kw.empty:
            st.dataframe(fmt_p_values(kw), use_container_width=True, hide_index=True)
    st.markdown('<div class="insight"><strong>Scope:</strong> these tests support descriptive associations and group differences; they do not establish causality.</div>', unsafe_allow_html=True)

elif page == "Clustering":
    section("Regional Clustering", "Seven standardized regional features were evaluated with K-Means and PCA.")
    ce = read_csv("cluster_k_evaluation.csv")
    if not ce.empty:
        fig = px.line(ce, x="k", y="silhouette", markers=True)
        fig.update_traces(line_color=GREEN_2)
        plot_layout(fig, 320)
        st.plotly_chart(fig, use_container_width=True)
    cp = read_csv("cluster_profiles.csv")
    cm = read_csv("cluster_membership.csv")
    if not cp.empty:
        st.dataframe(cp, use_container_width=True, hide_index=True)
    if not cm.empty:
        st.dataframe(cm, use_container_width=True, hide_index=True)
    st.markdown('<div class="insight"><strong>Selected k = 2.</strong> Silhouette = 0.4183. One cluster contains 24 regions and the other 4 regions, so interpretation should remain descriptive.</div>', unsafe_allow_html=True)

elif page == "Anomaly Detection":
    section("Anomaly Detection", "IQR and trailing rolling-z-score flags, classified using the project rules.")
    a = read_csv("anomaly_log.csv")
    if not a.empty:
        a["Date"] = pd.to_datetime(a["Date"], errors="coerce")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Flagged", len(a))
        c2.metric("Data-quality", int(a["Anomaly_Category"].astype(str).str.contains("Data-quality", case=False, na=False).sum()))
        c3.metric("COVID-related", int(a["Anomaly_Category"].astype(str).str.contains("COVID", case=False, na=False).sum()))
        c4.metric("Regions affected", a.Region.nunique())
        mon = a.groupby("Date").size().reset_index(name="Flags")
        fig = px.bar(mon, x="Date", y="Flags")
        fig.update_traces(marker_color=RED)
        plot_layout(fig, 360)
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(a, use_container_width=True, hide_index=True)

elif page == "Forecasting":
    section("Forecasting", "Rolling-origin one-step-ahead benchmarks for a 14-month national series.")
    m = read_csv("forecast_model_metrics.csv")
    if not m.empty:
        st.dataframe(m, use_container_width=True, hide_index=True)
        if "MAE" in m.columns and "Model" in m.columns:
            fig = px.bar(m.sort_values("MAE"), x="MAE", y="Model", orientation="h", color="MAE", color_continuous_scale="Oranges")
            fig.update_layout(coloraxis_showscale=False)
            plot_layout(fig, 380)
            st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="insight"><strong>Forecasting limitation:</strong> the series is only 14 months long and contains a structural COVID shock. Results are scoped to benchmark comparisons; long-horizon seasonal forecasting is not supported.</div>', unsafe_allow_html=True)

elif page == "Key Insights":
    section("Key Insights", "Consolidated findings from Phases 1–10.")
    findings = read_csv("phase10_key_findings.csv")
    if not findings.empty:
        st.dataframe(findings, use_container_width=True, hide_index=True)
    else:
        st.markdown('<div class="insight"><strong>National shock:</strong> mean unemployment rose from 9.51% to 17.77%.</div><div class="insight"><strong>Regional heterogeneity:</strong> Puducherry had the largest shock (+37.36 pp).</div><div class="insight"><strong>Coverage:</strong> 20 regions are fully covered and 8 are incomplete.</div>', unsafe_allow_html=True)

elif page == "Data Explorer":
    section("Data Explorer", "Inspect the cleaned observations using the sidebar filters.")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows", len(filtered))
    c2.metric("Regions", filtered.Region.nunique())
    c3.metric("Areas", filtered.Area.nunique())
    c4.metric("Months", filtered.Date.nunique())
    cols = [c for c in ["Region", "Date", "Area", "Period", UNEMP, EMPLOYED, PART] if c in filtered.columns]
    st.dataframe(filtered[cols].sort_values(["Date", "Region", "Area"]), use_container_width=True, hide_index=True, height=560)

elif page == "Limitations":
    section("Limitations", "Important analytical constraints carried through the project.")
    lim = read_csv("phase10_limitations.csv")
    if not lim.empty:
        st.dataframe(lim, use_container_width=True, hide_index=True)
    st.markdown('<div class="insight"><strong>Short time window:</strong> 14 monthly observations limit time-series inference.</div><div class="insight"><strong>Uneven coverage:</strong> 20 regions are fully covered; 8 are incomplete.</div><div class="insight"><strong>COVID structural shock:</strong> the period dominates variance and should not be treated as ordinary seasonality.</div><div class="insight"><strong>No causal claims:</strong> the dataset supports associations and descriptive comparisons, not causal attribution.</div><div class="insight"><strong>Clustering:</strong> only 28 regions are available, with one cluster containing four regions.</div>', unsafe_allow_html=True)

# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------
st.markdown(
    '''
    <hr>
    <div style="
        text-align:center;
        color:#7A8793;
        font-size:.68rem;
        line-height:1.7;
        padding:.35rem 0 .2rem;
    ">
        <b style="color:#006B5B">INDIA UNEMPLOYMENT ANALYTICS</b>
        · COMPLETE PROJECT DASHBOARD
        <br>
        May 2019 — June 2020 · Streamlit + Plotly
        <br>
        <span style="color:#536579">
            © 2026 <b style="color:#006B5B">Noura Maher Elamin</b>
            · All Rights Reserved
        </span>
        <br>
        <a href="https://www.linkedin.com/in/nouramaherelamin/"
           target="_blank"
           style="color:#0A66C2;text-decoration:none;font-weight:700;">
            LinkedIn
        </a>
        <span style="color:#B0BAC4"> · </span>
        <a href="https://github.com/nouramaherelamin"
           target="_blank"
           style="color:#102E55;text-decoration:none;font-weight:700;">
            GitHub
        </a>
    </div>
    ''',
    unsafe_allow_html=True,
)
