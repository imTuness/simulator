# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 09:58:36 2026

@author: JU
"""

"""
Stock Simulator Dashboard
Run with: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os, re, glob

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Stock Simulator",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# PALETTE
# ─────────────────────────────────────────────
PETROL   = "#2E6E7E"
PETROL_L = "#3D8FA3"
PETROL_D = "#1C4A57"
ORANGE   = "#E87722"
GREY_BG  = "#EAECEF"   # sidebar
WHITE    = "#FFFFFF"   # main
GREY_BDR = "#CDD1D9"
GREY_MID = "#6B7280"
GREY_TXT = "#1F2937"

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {{
    font-family: 'IBM Plex Sans', sans-serif;
    color: {GREY_TXT};
}}

/* ── Main: white ── */
.main, .block-container {{
    background-color: {WHITE} !important;
}}
.block-container {{
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}}

/* ── Sidebar: light grey ── */
section[data-testid="stSidebar"] {{
    background-color: {GREY_BG} !important;
    border-right: 2px solid {GREY_BDR} !important;
    min-width: 230px !important;
    max-width: 260px !important;
}}
/* All text in sidebar: dark */
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] label {{
    color: {GREY_TXT} !important;
    font-size: 0.78rem !important;
}}
/* Inputs & selects: white bg, dark text */
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea,
section[data-testid="stSidebar"] select,
section[data-testid="stSidebar"] [data-baseweb="select"] div,
section[data-testid="stSidebar"] [data-baseweb="input"] div {{
    background-color: {WHITE} !important;
    color: {GREY_TXT} !important;
    font-size: 0.78rem !important;
}}
section[data-testid="stSidebar"] [data-baseweb="select"] {{
    background-color: {WHITE} !important;
}}
/* Radio buttons */
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {{
    background: {WHITE} !important;
    border: 1px solid {GREY_BDR} !important;
    border-radius: 5px;
    padding: 5px 10px;
    margin: 2px 0;
    color: {GREY_TXT} !important;
    font-size: 0.78rem !important;
    font-weight: 400 !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
}}
section[data-testid="stSidebar"] hr {{
    border-color: {GREY_BDR} !important;
    margin: 8px 0 !important;
}}
/* ── Logo images in sidebar ── */
section[data-testid="stSidebar"] img {{
    object-fit: contain !important;
    max-height: 46px !important;
    padding: 2px 0 !important;
}}
/* logo columns flush */
section[data-testid="stSidebar"] [data-testid="column"] {{
    padding-left: 2px !important;
    padding-right: 2px !important;
}}
/* Step labels */
.step-lbl {{
    font-size: 0.62rem;
    font-weight: 600;
    color: {PETROL} !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin: 8px 0 2px 0;
}}
/* Param description labels */
.param-desc {{
    font-size: 0.68rem;
    color: {GREY_MID};
    font-style: italic;
    margin: 2px 0 4px 0;
    line-height: 1.4;
}}

/* ── Page title ── */
.db-title {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.8rem;
    font-weight: 600;
    color: {PETROL_D};
    line-height: 1.15;
}}
.db-title span {{ color: {ORANGE}; }}
.db-sub {{
    font-size: 1.05rem;
    color: {GREY_MID};
    margin-top: 4px;
    margin-bottom: 1rem;
    font-weight: 400;
}}

/* ── Section headers ── */
.sec-hdr {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    font-weight: 600;
    color: {PETROL};
    text-transform: uppercase;
    letter-spacing: 0.15em;
    border-left: 3px solid {ORANGE};
    padding-left: 8px;
    margin: 1.4rem 0 0.7rem 0;
}}

/* ── KPI cards ── */
.kcard {{
    background: {GREY_BG};
    border: 1px solid {GREY_BDR};
    border-radius: 8px;
    padding: 11px 14px;
    margin-bottom: 8px;
    border-top: 3px solid {PETROL_L};
}}
.kcard.orange {{ border-top-color: {ORANGE}; }}
.kcard.good   {{ border-top-color: #2E8B57; }}
.kcard.warn   {{ border-top-color: #C9850A; }}
.kcard.bad    {{ border-top-color: #C0392B; }}
.klbl {{
    font-size: 0.64rem;
    color: {GREY_MID};
    text-transform: uppercase;
    letter-spacing: 0.09em;
    margin-bottom: 4px;
}}
.kval {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.1rem;
    font-weight: 600;
    color: {GREY_TXT};
}}
.kval.good   {{ color: #2E8B57; }}
.kval.warn   {{ color: #C9850A; }}
.kval.bad    {{ color: #C0392B; }}
.kval.petrol {{ color: {PETROL_D}; }}
.kval.orange {{ color: {ORANGE}; }}

/* ── Best combo ── */
.bestbox {{
    background: {GREY_BG};
    border: 1.5px solid {PETROL};
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 0.5rem;
}}
.bestbox-ttl {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.64rem;
    color: {ORANGE};
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 7px;
}}
.best-combo {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.95rem;
    font-weight: 600;
    color: {PETROL_D};
}}
.best-badge {{
    display: inline-block;
    background: {PETROL_D};
    color: white;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    padding: 2px 9px;
    border-radius: 20px;
    margin-left: 7px;
    vertical-align: middle;
}}
.best-detail {{
    font-size: 0.78rem;
    color: {GREY_MID};
    margin-top: 5px;
    line-height: 1.7;
}}

/* ── Overview stat ── */
.ovcard {{
    background: {WHITE};
    border: 1px solid {GREY_BDR};
    border-radius: 8px;
    padding: 12px 16px;
    text-align: center;
    border-top: 3px solid {PETROL};
}}
.ovcard.orange {{ border-top-color: {ORANGE}; }}
.ovcard.good   {{ border-top-color: #2E8B57; }}
.ovcard.warn   {{ border-top-color: #C9850A; }}
.ovlbl {{
    font-size: 0.62rem;
    color: {GREY_MID};
    text-transform: uppercase;
    letter-spacing: 0.09em;
    margin-bottom: 4px;
}}
.ovval {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.3rem;
    font-weight: 600;
    color: {PETROL_D};
}}
.ovval.orange {{ color: {ORANGE}; }}
.ovval.good   {{ color: #2E8B57; }}
.ovval.warn   {{ color: #C9850A; }}

/* ── Baseline comparison card ── */
.baseline-card {{
    background: {WHITE};
    border: 1.5px solid {PETROL_L};
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 0.6rem;
}}
.baseline-ttl {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    color: {PETROL};
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 8px;
}}
.delta-pos {{ color: #2E8B57; font-weight: 600; }}
.delta-neg {{ color: #C0392B; font-weight: 600; }}
.delta-neu {{ color: {GREY_MID}; }}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

POLICY_MAP = {
    "min_max":"Min-Max","minmax":"Min-Max",
    "order_level":"Order Level","orderlevel":"Order Level",
    "order_cycle":"Order Cycle","ordercycle":"Order Cycle",
}
def policy_label(p):
    return POLICY_MAP.get(p.lower().replace("-","_"), p.replace("_"," ").title())


@st.cache_data
def load_abc_xyz(folder):
    patterns = [
        "*ABC*XYZ*.xlsx", "*abc*xyz*.xlsx",
        "*Analise*ABC*.xlsx", "*analise*abc*.xlsx",
        "*ABC*.xlsx",
    ]
    files = []
    for pat in patterns:
        files = glob.glob(os.path.join(folder, pat))
        if files:
            break
    if not files:
        return None, "ABC/XYZ Excel file not found."
    try:
        xl = pd.ExcelFile(files[0])
        sheet = "Dados" if "Dados" in xl.sheet_names else xl.sheet_names[0]
        df = pd.read_excel(files[0], sheet_name=sheet)
        sku_col   = next((c for c in df.columns if "sku" in c.lower()), None)
        cls_col   = next((c for c in df.columns if "classe" in c.lower() or "class" in c.lower()), None)
        if not sku_col or not cls_col:
            return None, f"Could not find SKU/Class columns. Columns found: {list(df.columns)}"
        df = df[[sku_col, cls_col]].dropna()
        df.columns = ["sku", "Classe_ABC_XYZ"]
        df["Classe_ABC_XYZ"] = df["Classe_ABC_XYZ"].astype(str).str.strip()
        return df, None
    except Exception as e:
        return None, str(e)


@st.cache_data
def load_baseline_excel(folder):
    """
    Load baseline fill rate & coverage Excel (current real-world data).
    Expects columns: sku (or SKU), fill_rate / fill rate, cobertura / coverage / coverage_days,
    and optionally Classe_ABC_XYZ / classe.
    """
    patterns = [
        "*baseline*.xlsx", "*Baseline*.xlsx",
        "*atual*.xlsx", "*Atual*.xlsx",
        "*current*.xlsx", "*Current*.xlsx",
        "*real*.xlsx", "*Real*.xlsx",
        "*fillrate*.xlsx", "*fill_rate*.xlsx",
    ]
    files = []
    for pat in patterns:
        files = glob.glob(os.path.join(folder, pat))
        if files:
            break
    if not files:
        return None, "Baseline Excel not found (looking for *baseline*, *atual*, *current*, *real* .xlsx)."
    try:
        xl = pd.ExcelFile(files[0])
        sheet = xl.sheet_names[0]
        df = pd.read_excel(files[0], sheet_name=sheet)
        df.columns = [str(c).strip() for c in df.columns]

        sku_col = next((c for c in df.columns if "sku" in c.lower()), None)
        fr_col  = next((c for c in df.columns if "fill" in c.lower()), None)
        cob_col = next((c for c in df.columns if "cobertura" in c.lower()
                        or "coverage" in c.lower() or "cobertura" in c.lower()), None)
        cls_col = next((c for c in df.columns if c.lower() == "classe_abc_xyz"), None)
        if cls_col is None:
            cls_col = next((c for c in df.columns if "abc_xyz" in c.lower()), None)
        if cls_col is None:
            cls_col = next((c for c in df.columns if "classe" in c.lower() or "class" in c.lower()), None)
        
        keep = [c for c in [sku_col, fr_col, cob_col, cls_col] if c]
        if not sku_col:
            return None, f"SKU column not found. Columns: {list(df.columns)}"
        df = df[keep].dropna(subset=[sku_col])
        rename = {sku_col: "sku"}
        if fr_col:  rename[fr_col]  = "baseline_fill_rate"
        if cob_col: rename[cob_col] = "baseline_cobertura"
        if cls_col: rename[cls_col] = "Classe_ABC_XYZ"
        df = df.rename(columns=rename)
        return df, None
    except Exception as e:
        return None, str(e)


@st.cache_data
def load_moq_params(folder):
    """
    Load MOQ from 20260210_stock_policy_parameters.parquet.
    Returns dict {sku: moq_value} — NaN/missing → shown as '-'.
    """
    path = os.path.join(folder, "20260210_stock_policy_parameters.parquet")
    if not os.path.exists(path):
        # fallback: any *stock_policy_parameters* parquet
        candidates = glob.glob(os.path.join(folder, "*stock_policy_parameters*.parquet"))
        if not candidates:
            return {}, "File 20260210_stock_policy_parameters.parquet not found."
        path = candidates[0]
    try:
        df = pd.read_parquet(path)
        # detect SKU column
        sku_col = next((c for c in df.columns if c.lower() in ("sku","sku_code","item","item_code")), None)
        if sku_col is None:
            sku_col = next((c for c in df.columns if "sku" in c.lower()), None)
        # detect MOQ column — prefer moq_units, then moq
        moq_col = next((c for c in df.columns if c.lower() == "moq_units"), None)
        if moq_col is None:
            moq_col = next((c for c in df.columns if "moq" in c.lower()), None)
        if sku_col is None or moq_col is None:
            return {}, f"Could not find SKU/MOQ columns. Found: {list(df.columns)}"
        mapping = df.set_index(sku_col)[moq_col].to_dict()
        return mapping, None
    except Exception as e:
        return {}, str(e)
    
def parse_parquet_name(filepath: str) -> dict:
    import os, re

    name = os.path.splitext(os.path.basename(filepath))[0]

    meta = {
        "filepath": filepath,
        "filename": name,
    }

    # tenta extrair simulator / ns / k / policy
    ns_m = re.search(r"simulator[_\s]?(\d+)", name, re.IGNORECASE)
    k_m  = re.search(r"k[=_](\d+(?:\.\d+)?)", name, re.IGNORECASE)

    meta["ns"] = ns_m.group(1) if ns_m else "N/A"
    meta["k"]  = k_m.group(1) if k_m else "N/A"

    meta["policy"] = name
    if ns_m:
        meta["policy"] = name[ns_m.end():k_m.start()].strip("_- ") if k_m else name[ns_m.end():]

    return meta

@st.cache_data
def list_parquets(folder):
    files = glob.glob(os.path.join(folder, "simulator*.parquet"))
    if not files:
        files = glob.glob(os.path.join(folder, "*.parquet"))
    return [parse_parquet_name(f) for f in files]


@st.cache_data
def load_parquet(path):
    df = pd.read_parquet(path)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
    return df


def compute_metrics(df):
    if df.empty:
        return {}
    m = {}
    if "soh_final" in df.columns:
        m["stock_medio"]  = df["soh_final"].mean()
        m["stock_minimo"] = df["soh_final"].min()
        m["stock_maximo"] = df["soh_final"].max()
        m["pct_zero"]     = (df["soh_final"] == 0).mean() * 100
    else:
        m["stock_medio"] = m["stock_minimo"] = m["stock_maximo"] = m["pct_zero"] = np.nan

    ss_c = next((c for c in ["SS_s","ss","safety_stock","SS"] if c in df.columns), None)
    m["ss_medio"] = df[ss_c].mean() if ss_c else np.nan

    cob_c = next((c for c in ["cobertura_dias","coverage_days","cobertura"] if c in df.columns), None)
    if cob_c:
        m["cobertura"] = df[cob_c].mean()
    elif "soh_final" in df.columns and "demand" in df.columns:
        d = df["demand"].mean()
        m["cobertura"] = df["soh_final"].mean() / d if d > 0 else np.nan
    else:
        m["cobertura"] = np.nan

    if "stockout" in df.columns:
        dias = len(df)
        m["stockout_days"] = int(df["stockout"].sum())
        m["csl"]           = (df["stockout"] == 0).sum() / dias * 100 if dias else np.nan
        # Fill Rate = 1 - (soma stockout / soma demand)
        total_demand  = df["demand"].sum() if "demand" in df.columns else 0
        total_stockout = df["stockout"].sum()
        if total_demand > 0:
            m["fill_rate"]   = (1 - total_stockout / total_demand) * 100
            m["stockout_rate"] = (total_stockout / total_demand) * 100
        else:
            m["fill_rate"]   = 100.0
            m["stockout_rate"] = 0.0
    else:
        m["stockout_days"] = m["csl"] = m["fill_rate"] = np.nan

    enc_c = next((c for c in ["encomendas_pedidas","encomendas_colocadas","num_encomendas"] if c in df.columns), None)
    m["num_orders"] = int(df[enc_c].sum()) if enc_c else np.nan

    moq_c = next((c for c in ["moq","MOQ"] if c in df.columns), None)
    m["moq"] = df[moq_c].mean() if moq_c else np.nan

    cs_c  = next((c for c in ["custo_stock_diario","custo_stock","stock_cost"] if c in df.columns), None)
    ct_c  = next((c for c in ["custo_transporte","transport_cost","custo_transporte_diario"] if c in df.columns), None)
    ctt_c = next((c for c in ["custo_total","total_cost"] if c in df.columns), None)
    m["cost_stock"]     = df[cs_c].sum()  if cs_c  else np.nan
    m["cost_transport"] = df[ct_c].sum()  if ct_c  else np.nan
    cs_v, ct_v = m.get("cost_stock", np.nan), m.get("cost_transport", np.nan)
    if ctt_c:
        m["cost_total"] = df[ctt_c].sum()
    elif not (np.isnan(cs_v) or np.isnan(ct_v)):
        m["cost_total"] = cs_v + ct_v
    else:
        m["cost_total"] = np.nan
    return m


def fv(val, fmt, suf="", pre=""):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return "—"
    return f"{pre}{val:{fmt}}{suf}"


def mcss(key, val):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return "",""
    if key in ["fill_rate","csl"]:
        q = "good" if val>=95 else ("warn" if val>=85 else "bad")
        return q,q
    if key == "stockout_rate":
        q = "good" if val==0 else ("warn" if val<=5 else "bad")
        return q,q 
    if key == "pct_zero":
        q = "good" if val==0 else ("warn" if val<5 else "bad")
        return q,q
    if key in ["cost_total","cost_stock","cost_transport"]:
        return "orange","orange"
    if key in ["stock_medio","ss_medio","cobertura"]:
        return "","petrol"
    return "",""


PLOT = dict(
    template="plotly_white",
    paper_bgcolor=WHITE,
    plot_bgcolor="#FAFBFC",
    font=dict(family="IBM Plex Sans, sans-serif", color=GREY_TXT),
)


def find_best(parquets_meta, df_abc, mode, sku_or_class, fill_rate_target=95.0):
    """
    Pareto / constrained optimisation:
      1. Keep only combinations where fill_rate >= fill_rate_target
      2. Among those, pick the one with lowest total cost
      3. If none meets the target, relax and pick highest fill_rate (then lowest cost)
    Returns (best_row, df_all_combos, met_target: bool)
    """
    rows = []
    for meta in parquets_meta:
        try:
            df = load_parquet(meta["filepath"])
            if mode == "SKU":
                df_f = df[df["sku"] == sku_or_class].copy()
            else:
                skus = df_abc[df_abc["Classe_ABC_XYZ"] == sku_or_class]["sku"].unique()
                df_f = df[df["sku"].isin(skus)].copy()
            if df_f.empty: continue
            m = compute_metrics(df_f)
            fr = m.get("fill_rate", np.nan)
            ct = m.get("cost_total", np.nan)
            if np.isnan(fr) or np.isnan(ct) or ct == 0: continue
            rows.append({"policy": meta["policy"], "ns": meta["ns"], "k": meta["k"],
                         "fill_rate": fr, "cost_total": ct})
        except Exception:
            continue
    if not rows:
        return None
    df_r = pd.DataFrame(rows)

    feasible = df_r[df_r["fill_rate"] >= fill_rate_target]
    if not feasible.empty:
        best = feasible.sort_values("cost_total").iloc[0]
        met_target = True
    else:
        # relax: best fill rate possible, then minimum cost
        best_fr = df_r["fill_rate"].max()
        best = df_r[df_r["fill_rate"] == best_fr].sort_values("cost_total").iloc[0]
        met_target = False

    return best, df_r, met_target


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    # ── Logos side by side (NOVA IMS + LTPLabs) ──
    # Each logo is loaded via st.image with a public URL.
    # If a URL fails to load the browser simply shows nothing — no crash.
    EEUM_LOGO = "https://www.eng.uminho.pt/SiteAssets/Logo.PNG"
    LTPLABS_LOGO = "https://apgei.pt/wp-content/uploads/2023/02/logo_3.png"
    
    col_logo1, col_logo2 = st.columns(2)
    with col_logo1:
        st.image(EEUM_LOGO, width=150)
    with col_logo2:
        st.image(LTPLABS_LOGO, width=70)

    # ── Title & group info ──
    st.markdown(f"""
    <div style='padding:6px 0 10px 0;'>
      <div style='font-family:IBM Plex Mono,monospace;font-size:1.18rem;
                  font-weight:600;color:{PETROL_D};letter-spacing:-0.01em;'>Stock Simulator</div>
      <div style='font-size:0.70rem;color:{GREY_MID};margin-top:2px;'>Analysis Dashboard</div>
      <div style='font-size:0.68rem;color:{PETROL};font-weight:600;margin-top:4px;'>Group 3 – MEGI</div>
      <div style='font-size:0.65rem;color:{GREY_MID};margin-top:1px;'>Supply Chain Management</div>
      <div style='font-size:0.65rem;color:{GREY_MID};margin-top:1px;'>2025/2026</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")

    # ① Folder
    st.markdown(f"<div class='step-lbl'>① Data Folder</div>", unsafe_allow_html=True)
    folder = st.text_input(
        "fi", value=os.getcwd(), label_visibility="collapsed",
        help="Folder containing .parquet and ABC/XYZ Excel files"
    )

    if not os.path.isdir(folder):
        st.error("Folder not found.")
        st.stop()

    parquets_meta = list_parquets(folder)
    if not parquets_meta:
        st.error("No .parquet files found.")
        st.stop()

    st.caption(f"✓ {len(parquets_meta)} parquet file(s) found")
    df_abc, abc_error = load_abc_xyz(folder)
    if df_abc is not None:
        st.caption(f"✓ ABC/XYZ file loaded ({len(df_abc)} SKUs)")
    else:
        st.caption(f"⚠ ABC/XYZ: {abc_error}")

    # Load MOQ params (optional)
    moq_map, moq_error = load_moq_params(folder)
    if moq_map:
        st.caption(f"✓ MOQ params loaded ({len(moq_map)} SKUs)")
    else:
        st.caption(f"ℹ MOQ: {moq_error}")

    st.markdown("---")

    # ② Mode
    st.markdown(f"<div class='step-lbl'>② Analysis Mode</div>", unsafe_allow_html=True)
    mode = st.radio("mode", ["Overview","By SKU","By ABC/XYZ Class"],
                    label_visibility="collapsed")

    # ③ SKU / Class
    sku_sel = None
    class_sel = None
    skus_in_class = []

    if mode == "By SKU":
        st.markdown("---")
        st.markdown(f"<div class='step-lbl'>③ Select SKU</div>", unsafe_allow_html=True)
        all_skus = set()
        for meta in parquets_meta:
            try:
                df_tmp = load_parquet(meta["filepath"])
                if "sku" in df_tmp.columns:
                    all_skus.update(df_tmp["sku"].unique())
            except Exception:
                pass
        all_skus = sorted(all_skus)
        if not all_skus:
            st.error("No SKUs found.")
            st.stop()
        sku_sel = st.selectbox("SKU", all_skus, label_visibility="collapsed")
        if df_abc is not None:
            match = df_abc[df_abc["sku"] == sku_sel]["Classe_ABC_XYZ"]
            sku_class = match.values[0] if len(match) > 0 else "—"
            st.caption(f"ABC/XYZ Class: {sku_class}")

    elif mode == "By ABC/XYZ Class":
        st.markdown("---")
        st.markdown(f"<div class='step-lbl'>③ Select Class</div>", unsafe_allow_html=True)
        if df_abc is None:
            st.error(f"ABC/XYZ not loaded: {abc_error}")
            st.stop()
        # FIX 2: Use actual Classe_ABC_XYZ values from the ABC/XYZ excel
        classes = sorted(df_abc["Classe_ABC_XYZ"].unique())
        class_sel = st.selectbox("ABC/XYZ Class", classes, label_visibility="collapsed")
        skus_in_class = df_abc[df_abc["Classe_ABC_XYZ"] == class_sel]["sku"].unique()
        st.caption(f"{len(skus_in_class)} SKU(s) in this class")

    # ④ Simulation params (only when not Overview)
    selected_file = None
    policy_sel = None
    ns_sel = None
    k_sel = None
    fill_rate_target = 95.0  # default, overridden by slider when not Overview

    if mode != "Overview":
        st.markdown("---")
        st.markdown(f"<div class='step-lbl'>④ Simulation Parameters</div>", unsafe_allow_html=True)

        # FIX 3: Description above each parameter
        st.markdown(
            f"<div class='param-desc'>📋 <b>Policy</b> — Inventory replenishment strategy used in the simulation.</div>",
            unsafe_allow_html=True
        )
        policies_raw = sorted(set(m["policy"] for m in parquets_meta))
        pol_opts     = [policy_label(p) for p in policies_raw]
        pol_disp     = st.selectbox("Policy", pol_opts, label_visibility="collapsed")
        policy_sel   = policies_raw[pol_opts.index(pol_disp)]

        st.markdown(
            f"<div class='param-desc'>🎯 <b>Service Level (%)</b> — Target non-stockout probability used to compute safety stock.</div>",
            unsafe_allow_html=True
        )
        ns_opts = sorted(set(m["ns"] for m in parquets_meta if m["policy"] == policy_sel))
        ns_sel  = st.selectbox("Service Level (%)", ns_opts, label_visibility="collapsed")

        st.markdown(
            f"<div class='param-desc'>⚖️ <b>k value</b> — Safety factor multiplier applied to demand variability (higher k = more safety stock).</div>",
            unsafe_allow_html=True
        )
        k_opts = sorted(set(
            m["k"] for m in parquets_meta
            if m["policy"] == policy_sel and m["ns"] == ns_sel
        ))
        k_sel = st.selectbox("k value", k_opts, label_visibility="collapsed")

        selected_file = next(
            (m["filepath"] for m in parquets_meta
             if m["policy"] == policy_sel and m["ns"] == ns_sel and m["k"] == k_sel),
            None
        )
        if not selected_file:
            st.error("Combination not found.")
            st.stop()

        # ⑤ Fill Rate target for Best Combination finder
        st.markdown("---")
        st.markdown(f"<div class='step-lbl'>⑤ Best Combination Target</div>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='param-desc'>🎯 Minimum Fill Rate β to satisfy. The cheapest combination that meets this threshold is recommended.</div>",
            unsafe_allow_html=True
        )
        fill_rate_target = st.slider(
            "Min Fill Rate β (%)", min_value=70, max_value=100, value=95, step=1,
            label_visibility="collapsed"
        )


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────

sub = "Global Overview — all files considered" if mode == "Overview" else \
      (f"SKU {sku_sel}" if mode == "By SKU" else f"Class {class_sel}")

col_h, col_kpi = st.columns([4,1])
with col_h:
    st.markdown(f"""
    <div class="db-title"><span style="font-size:1.6rem;">📦</span> Stock Management Simulator <span style="white-space:nowrap;">Dashboard</span></div>
    <div class="db-sub">{sub}{f' &nbsp;·&nbsp; {pol_disp} &nbsp;·&nbsp; SL {ns_sel}% &nbsp;·&nbsp; k={k_sel}' if mode != 'Overview' else ''}</div>
    """, unsafe_allow_html=True)
with col_kpi:
    st.markdown(f"""
    <div style='text-align:right;padding-top:4px;'>
      ...
    </div>""", unsafe_allow_html=True)

# ═════════════════════════════════════════════
# OVERVIEW MODE  (FIX 4: show real metrics)
# ═════════════════════════════════════════════

if mode == "Overview":

    @st.cache_data
    def load_all_metrics(parquets_meta_frozen):
        records = []
        for (filepath, policy, ns, k) in parquets_meta_frozen:
            try:
                df = load_parquet(filepath)
                # Count simulated days (global)
                if "date" in df.columns:
                    n_days_file = df["date"].nunique()
                else:
                    n_days_file = len(df)

                for sku, grp in (df.groupby("sku") if "sku" in df.columns else [("all", df)]):
                    m = compute_metrics(grp)
                    m["sku"]    = sku
                    m["policy"] = policy
                    m["ns"]     = ns
                    m["k"]      = k
                    m["n_days"] = n_days_file
                    records.append(m)
            except Exception:
                pass
        return pd.DataFrame(records)

    df_all = load_all_metrics(tuple(
        (m["filepath"], m["policy"], m["ns"], m["k"]) for m in parquets_meta
    ))

    if df_all.empty:
        st.warning("Could not load data from parquet files.")
        st.stop()

    # ── Compute overview KPIs
    avg_fr      = df_all["fill_rate"].mean()      if "fill_rate"      in df_all else np.nan
    avg_csl     = df_all["csl"].mean()            if "csl"            in df_all else np.nan
    avg_ct      = df_all["cost_total"].mean()     if "cost_total"     in df_all else np.nan
    avg_so      = df_all["stockout_days"].mean()  if "stockout_days"  in df_all else np.nan
    avg_cob     = df_all["cobertura"].mean()      if "cobertura"      in df_all else np.nan
    avg_ss      = df_all["ss_medio"].mean()       if "ss_medio"       in df_all else np.nan
    n_skus_total = df_all["sku"].nunique()        if "sku"            in df_all else 0
    n_combos     = len(parquets_meta)
    n_days_sim   = int(df_all["n_days"].max())    if "n_days"         in df_all else 0
    n_classes    = df_abc["Classe_ABC_XYZ"].nunique() if df_abc is not None else 0

    # ── Row 1: structural KPIs
    st.markdown("<div class='sec-hdr'>◆ Study Scope</div>", unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    for col, val, lbl, cls in [
        (c1, str(n_skus_total),  "Total SKUs in Study",     ""),
        (c2, str(n_classes),     "ABC/XYZ Classes",         ""),
        (c3, f"{n_days_sim:,} days",  "Simulated Days",  ""),
        (c4, str(n_combos),      "Parameter Combinations",  "orange"),
    ]:
        with col:
            st.markdown(f"""
            <div class="ovcard {cls}">
              <div class="ovlbl">{lbl}</div>
              <div class="ovval {cls}">{val}</div>
            </div>""", unsafe_allow_html=True)

    # ── Row 2: performance KPIs
    st.markdown("<div class='sec-hdr'>◆ Simulated Performance (avg across all SKUs & combinations)</div>",
                unsafe_allow_html=True)
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    fr_cls  = "good" if not np.isnan(avg_fr)  and avg_fr  >= 95 else ("warn" if not np.isnan(avg_fr)  and avg_fr  >= 85 else "")
    csl_cls = "good" if not np.isnan(avg_csl) and avg_csl >= 95 else ("warn" if not np.isnan(avg_csl) and avg_csl >= 85 else "")
    for col, val, lbl, cls in [
        (c1, f"{avg_fr:,.1f}%"  if not np.isnan(avg_fr)  else "—", "Avg Fill Rate β",      fr_cls),
        (c2, f"{avg_csl:,.1f}%" if not np.isnan(avg_csl) else "—", "Avg CSL α",             csl_cls),
        (c3, f"{avg_so:,.1f} days"  if not np.isnan(avg_so)  else "—", "Avg Stockout Days",        ""),
        (c4, f"{avg_cob:,.0f} days" if not np.isnan(avg_cob) else "—", "Avg Stock Coverage",       ""),
        (c5, f"{avg_ss:,.1f} units" if not np.isnan(avg_ss)  else "—", "Avg Safety Stock",          ""),
        (c6, f"€{avg_ct:,.0f}" if not np.isnan(avg_ct)  else "—", "Avg Total Cost / SKU",  "orange"),
    ]:
        with col:
            st.markdown(f"""
            <div class="ovcard {cls}">
              <div class="ovlbl">{lbl}</div>
              <div class="ovval {cls}">{val}</div>
            </div>""", unsafe_allow_html=True)

     # ── Policy comparison
    st.markdown("<div class='sec-hdr'>◆ Policy Comparison — Avg Fill Rate & Cost</div>",
                unsafe_allow_html=True)

    if "policy" in df_all.columns and "fill_rate" in df_all.columns:
        df_pol = df_all.groupby("policy").agg(
            fill_rate=("fill_rate","mean"),
            cost_total=("cost_total","mean"),
            stockout_days=("stockout_days","mean"),
        ).reset_index()
        df_pol["Policy"] = df_pol["policy"].apply(policy_label)

        col_a, col_b = st.columns(2)
        with col_a:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=df_pol["Policy"], y=df_pol["fill_rate"],
                marker_color=PETROL, name="Avg Fill Rate β (%)"
            ))
            fig.update_layout(**PLOT, height=280, margin=dict(l=10,r=10,t=30,b=10),
                              title="Avg Fill Rate β by Policy",
                              yaxis=dict(gridcolor=GREY_BDR, title="%"),
                              xaxis=dict(gridcolor=GREY_BDR))
            st.plotly_chart(fig, use_container_width=True)

        with col_b:
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(
                x=df_pol["Policy"], y=df_pol["cost_total"],
                marker_color=ORANGE, name="Avg Total Cost (€)"
            ))
            fig2.update_layout(**PLOT, height=280, margin=dict(l=10,r=10,t=30,b=10),
                               title="Avg Total Cost by Policy",
                               yaxis=dict(gridcolor=GREY_BDR, title="€"),
                               xaxis=dict(gridcolor=GREY_BDR))
            st.plotly_chart(fig2, use_container_width=True)

    # ── ABC/XYZ Class breakdown
    if df_abc is not None and "sku" in df_all.columns:
        st.markdown("<div class='sec-hdr'>◆ Performance by ABC/XYZ Class — Best Combination</div>",
                    unsafe_allow_html=True)

        # Para cada classe, encontrar a melhor combinação
        classes_list = sorted(df_abc["Classe_ABC_XYZ"].unique())
        best_rows = []
        for cls in classes_list:
            skus_cls = df_abc[df_abc["Classe_ABC_XYZ"] == cls]["sku"].unique()
            res_cls = find_best(parquets_meta, df_abc, "CLASS", cls, fill_rate_target=95.0)
            if res_cls:
                best_cls, _, _ = res_cls
                best_rows.append({
                    "Class": cls,
                    "Best Combination": f"{policy_label(best_cls['policy'])} · NS {best_cls['ns']}% · k={best_cls['k']}",
                    "Fill Rate β (%)": round(best_cls["fill_rate"], 2),
                    "Total Cost (€)": round(best_cls["cost_total"], 2),
                })
            else:
                best_rows.append({
                    "Class": cls,
                    "Best Combination": "—",
                    "Fill Rate β (%)": None,
                    "Total Cost (€)": None,
                })

        df_best_cls = pd.DataFrame(best_rows)

        col_cls_bar, col_cls_tbl = st.columns([1, 1])
        with col_cls_bar:
            fig_cls = go.Figure()
            fig_cls.add_trace(go.Bar(
                x=df_best_cls["Class"],
                y=df_best_cls["Fill Rate β (%)"],
                marker_color=PETROL, name="Best Fill Rate β (%)",
            ))
            fig_cls.update_layout(**PLOT, height=260, margin=dict(l=10,r=10,t=30,b=10),
                                  title="Best Fill Rate β by ABC/XYZ Class",
                                  yaxis=dict(gridcolor=GREY_BDR, title="%"),
                                  xaxis=dict(gridcolor=GREY_BDR))
            st.plotly_chart(fig_cls, use_container_width=True)

        with col_cls_tbl:
            fmt_best = {
                "Fill Rate β (%)": "{:.2f}",
                "Total Cost (€)": "{:,.2f}",
            }
            styled_best = df_best_cls.style.format(fmt_best, na_rep="—")
            styled_best = styled_best.background_gradient(
                subset=["Fill Rate β (%)"], cmap="RdYlGn", vmin=80, vmax=100
            )
            st.dataframe(styled_best, use_container_width=True, height=260, hide_index=True)
   
    # ── SKU Distribution
    st.markdown("<div class='sec-hdr'>◆ SKU Distribution — Fill Rate & Cost</div>",
                unsafe_allow_html=True)

    df_sku_avg = df_all.groupby("sku").agg(
        fill_rate=("fill_rate","mean"),
        cost_total=("cost_total","mean"),
        stockout_days=("stockout_days","mean"),
    ).reset_index().dropna(subset=["fill_rate","cost_total"])

    if not df_sku_avg.empty:
        col_hist, col_scatter = st.columns(2)
        with col_hist:
            fig_h = go.Figure()
            fig_h.add_trace(go.Histogram(
                x=df_sku_avg["fill_rate"], nbinsx=20,
                marker_color=PETROL, opacity=0.85, name="SKUs"
            ))
            fig_h.update_layout(**PLOT, height=270, margin=dict(l=10,r=10,t=30,b=10),
                                title="Fill Rate β Distribution (avg per SKU)",
                                xaxis=dict(title="%", gridcolor=GREY_BDR),
                                yaxis=dict(title="Number of SKUs", gridcolor=GREY_BDR))
            st.plotly_chart(fig_h, use_container_width=True)

        with col_scatter:
            fig_s = go.Figure()
            fig_s.add_trace(go.Scatter(
                x=df_sku_avg["cost_total"], y=df_sku_avg["fill_rate"],
                mode="markers",
                marker=dict(color=ORANGE, size=6, opacity=0.7,
                            line=dict(color=PETROL_D, width=0.5)),
                text=df_sku_avg["sku"],
                hovertemplate="<b>%{text}</b><br>Cost: €%{x:,.0f}<br>Fill Rate: %{y:.1f}%<extra></extra>",
            ))
            fig_s.update_layout(**PLOT, height=270, margin=dict(l=10,r=10,t=30,b=10),
                                title="Fill Rate vs Cost per SKU (avg)",
                                xaxis=dict(title="Total Cost (€)", gridcolor=GREY_BDR),
                                yaxis=dict(title="Fill Rate β (%)", gridcolor=GREY_BDR))
            st.plotly_chart(fig_s, use_container_width=True)

    # ── Top / Bottom SKU ranking
    st.markdown("<div class='sec-hdr'>◆ SKU Ranking</div>", unsafe_allow_html=True)

    if not df_sku_avg.empty:
        col_top, col_bot = st.columns(2)
        with col_top:
            st.markdown(f"<div style='font-size:0.74rem;font-weight:600;color:{PETROL};margin-bottom:4px;'>🏆 Top 10 — Highest Fill Rate</div>", unsafe_allow_html=True)
            top10 = df_sku_avg.nlargest(10,"fill_rate")[["sku","fill_rate","cost_total"]] \
                              .rename(columns={"sku":"SKU","fill_rate":"Fill Rate β (%)","cost_total":"Avg Cost (€)"})
            st.dataframe(top10.style.format({"Fill Rate β (%)":"{:.2f}","Avg Cost (€)":"{:,.2f}"},
                         na_rep="—"), use_container_width=True, height=320, hide_index=True)
        with col_bot:
            st.markdown(f"<div style='font-size:0.74rem;font-weight:600;color:#C0392B;margin-bottom:4px;'>⚠ Bottom 10 — Lowest Fill Rate</div>", unsafe_allow_html=True)
            bot10 = df_sku_avg.nsmallest(10,"fill_rate")[["sku","fill_rate","cost_total"]] \
                              .rename(columns={"sku":"SKU","fill_rate":"Fill Rate β (%)","cost_total":"Avg Cost (€)"})
            st.dataframe(bot10.style.format({"Fill Rate β (%)":"{:.2f}","Avg Cost (€)":"{:,.2f}"},
                         na_rep="—"), use_container_width=True, height=320, hide_index=True)

    # ── Global Best Combination
    st.markdown("<div class='sec-hdr'>◆ Global Best Combination</div>", unsafe_allow_html=True)

    with st.spinner("Evaluating all combinations globally..."):
        # Agregar todos os SKUs de todos os parquets
        global_rows = []
        for meta in parquets_meta:
            try:
                df_g = load_parquet(meta["filepath"])
                m_g = compute_metrics(df_g)
                fr_g = m_g.get("fill_rate", np.nan)
                ct_g = m_g.get("cost_total", np.nan)
                if np.isnan(fr_g) or np.isnan(ct_g) or ct_g == 0:
                    continue
                global_rows.append({
                    "policy": meta["policy"],
                    "ns": meta["ns"],
                    "k": meta["k"],
                    "fill_rate": fr_g,
                    "cost_total": ct_g,
                })
            except Exception:
                continue

    if global_rows:
        df_global = pd.DataFrame(global_rows)
        fill_rate_target_ov = 95.0

        feasible_g = df_global[df_global["fill_rate"] >= fill_rate_target_ov]
        if not feasible_g.empty:
            best_g = feasible_g.sort_values("cost_total").iloc[0]
            met_g = True
        else:
            best_g = df_global.sort_values("fill_rate", ascending=False).iloc[0]
            met_g = False

        # ── 1. Caixa melhor combinação global
        col_bg, col_tg = st.columns([1, 2])
        with col_bg:
            if met_g:
                badge_g = f"<span class='best-badge' style='background:#2E8B57;'>✓ Fill Rate ≥ {fill_rate_target_ov}%</span>"
                criterion_g = f"Fill Rate ≥ {fill_rate_target_ov}% satisfied → lowest cost selected"
            else:
                badge_g = f"<span class='best-badge' style='background:#C9850A;'>⚠ Target not met</span>"
                criterion_g = f"No combination reaches {fill_rate_target_ov}% — best available shown"
            st.markdown(f"""
            <div class="bestbox">
              <div class="bestbox-ttl">🏆 Best Global Combination</div>
              <div class="best-combo">
                {policy_label(best_g['policy'])} · SL {best_g['ns']}% · k={best_g['k']}
                {badge_g}
              </div>
              <div class="best-detail">
                Fill Rate: <b style='color:{PETROL};'>{best_g['fill_rate']:.2f}%</b>
                &nbsp;|&nbsp;
                Total Cost: <b style='color:{ORANGE};'>€{best_g['cost_total']:,.2f}</b><br>
                <i>{criterion_g}</i>
              </div>
            </div>""", unsafe_allow_html=True)

        with col_tg:
            # ── 2. Tabela de todas as combinações
            df_show_g = df_global.copy()
            df_show_g["Policy"] = df_show_g["policy"].apply(policy_label)
            df_show_g["SL (%)"] = df_show_g["ns"]
            df_show_g["Fill Rate β (%)"] = df_show_g["fill_rate"].map("{:.2f}".format)
            df_show_g["Total Cost (€)"] = df_show_g["cost_total"].map("{:,.2f}".format)
            df_show_g["Meets Target"] = df_show_g["fill_rate"].apply(
                lambda x: "✓" if x >= fill_rate_target_ov else "✗"
            )
            df_show_g = df_show_g[["Policy", "SL (%)", "k", "Fill Rate β (%)", "Total Cost (€)", "Meets Target"]] \
                                  .sort_values("Fill Rate β (%)", ascending=False)
            st.dataframe(df_show_g, use_container_width=True, height=200, hide_index=True)

        # ── 3. Scatter plot Fill Rate vs Custo
        st.markdown("<div class='sec-hdr'>◆ Fill Rate vs Cost — All Combinations</div>",
                    unsafe_allow_html=True)

        fig_sc = go.Figure()

        # Pontos que não atingem o target
        df_inf = df_global[df_global["fill_rate"] < fill_rate_target_ov]
        if not df_inf.empty:
            fig_sc.add_trace(go.Scatter(
                x=df_inf["cost_total"], y=df_inf["fill_rate"],
                mode="markers",
                name="Below Target",
                marker=dict(color="#C0392B", size=8, opacity=0.7),
                text=df_inf.apply(lambda r: f"{policy_label(r['policy'])} · SL {r['ns']}% · k={r['k']}", axis=1),
                hovertemplate="<b>%{text}</b><br>Cost: €%{x:,.0f}<br>Fill Rate: %{y:.2f}%<extra></extra>",
            ))

        # Pontos que atingem o target
        df_feas = df_global[df_global["fill_rate"] >= fill_rate_target_ov]
        if not df_feas.empty:
            fig_sc.add_trace(go.Scatter(
                x=df_feas["cost_total"], y=df_feas["fill_rate"],
                mode="markers",
                name="Above Target",
                marker=dict(color=PETROL, size=8, opacity=0.8),
                text=df_feas.apply(lambda r: f"{policy_label(r['policy'])} · SL {r['ns']}% · k={r['k']}", axis=1),
                hovertemplate="<b>%{text}</b><br>Cost: €%{x:,.0f}<br>Fill Rate: %{y:.2f}%<extra></extra>",
            ))

        # Ponto ótimo destacado
        fig_sc.add_trace(go.Scatter(
            x=[best_g["cost_total"]], y=[best_g["fill_rate"]],
            mode="markers",
            name="Best Combination",
            marker=dict(color=ORANGE, size=14, symbol="star",
                        line=dict(color=PETROL_D, width=1.5)),
            text=[f"{policy_label(best_g['policy'])} · SL {best_g['ns']}% · k={best_g['k']}"],
            hovertemplate="<b>%{text}</b><br>Cost: €%{x:,.0f}<br>Fill Rate: %{y:.2f}%<extra></extra>",
        ))

        # Linha vertical do target
        fig_sc.add_hline(
            y=fill_rate_target_ov,
            line_dash="dash", line_color="#C0392B", line_width=1.5,
            annotation_text=f"Target {fill_rate_target_ov}%",
            annotation_position="right",
        )

        fig_sc.update_layout(
            **PLOT, height=350, margin=dict(l=10, r=10, t=20, b=10),
            xaxis=dict(title="Total Cost (€)", gridcolor=GREY_BDR),
            yaxis=dict(title="Fill Rate β (%)", gridcolor=GREY_BDR),
            legend=dict(orientation="h", yanchor="bottom", y=1.02,
                        bgcolor="rgba(0,0,0,0)"),
            hovermode="closest",
        )
        st.plotly_chart(fig_sc, use_container_width=True)

    st.markdown("---")
    st.caption("📦 Stock Management Simulator · Group 3 – MEGI · Supply Chain Management")
    st.stop()

# ═════════════════════════════════════════════
# SKU / CLASS MODE
# ═════════════════════════════════════════════

df_raw = load_parquet(selected_file)

if mode == "By SKU":
    df_filtered = df_raw[df_raw["sku"] == sku_sel].copy()
    sel_label   = f"SKU {sku_sel}"
    sku_or_class = sku_sel
    bc_mode      = "SKU"
else:
    df_filtered  = df_raw[df_raw["sku"].isin(skus_in_class)].copy()
    sel_label    = f"Class {class_sel}"
    sku_or_class = class_sel
    bc_mode      = "CLASS"

if df_filtered.empty:
    st.warning("No data for the current selection.")
    st.stop()

n_days = df_filtered["date"].nunique() if "date" in df_filtered.columns else len(df_filtered)
n_skus = df_filtered["sku"].nunique()  if "sku"  in df_filtered.columns else 1


# ── Policy Description
Policy_Descriptions = {
    "min_max": {
        "icon": "🔄",
        "title": "Min-Max (R, s, S)",
        "text": "Every R units of time we check the inventory position. If it is at or below the reorder point s, we order enough to raise it to S.",
        "params": ["R — Review period", "s — Reorder point", "S — Order-up-to level"],
    },
    "order_cycle": {
        "icon": "📅",
        "title": "Order Cycle (R, S)",
        "text": "Every R units of time (i.e., at each review instant) enough is ordered to raise the inventory position to the level S.",
        "params": ["R — Review period", "S — Order-up-to level"],
    },
    "order_level": {
        "icon": "📦",
        "title": "Order Level (s, Q)",
        "text": "A fixed quantity Q is ordered whenever the inventory position drops to the reorder point s or lower.",
        "params": ["s — Reorder point", "Q — Fixed order quantity"],
    },
}

pol_key = policy_sel.lower().replace("-","_")
pol_info = Policy_Descriptions.get(pol_key)

col_policy, col_kpi = st.columns([3, 1])

with col_policy:
    if pol_info:
        params_html = "".join(
            f"<span style='display:inline-block;background:{PETROL_D};color:white;"
            f"font-family:IBM Plex Mono,monospace;font-size:0.68rem;padding:2px 10px;"
            f"border-radius:20px;margin:2px 4px 2px 0;'>{p}</span>"
            for p in pol_info["params"]
        )
        st.markdown(f"""
        <div style='background:#FEF3E8;border:1.5px solid #F5C49A;border-left:4px solid {ORANGE};
                    border-radius:8px;padding:14px 18px;margin-bottom:1rem;'>
          <div style='font-family:IBM Plex Mono,monospace;font-size:0.65rem;font-weight:600;
                      color:{ORANGE};text-transform:uppercase;letter-spacing:0.12em;margin-bottom:6px;'>
            {pol_info["icon"]} &nbsp;Active Policy
          </div>
          <div style='font-size:1.0rem;font-weight:600;color:#B85A0D;margin-bottom:6px;'>
            {pol_info["title"]}
          </div>
          <div style='font-size:0.85rem;color:#7C3D0A;line-height:1.7;margin-bottom:10px;
                      font-style:italic;'>
            "{pol_info["text"]}"
          </div>
          <div>{params_html}</div>
        </div>
        """, unsafe_allow_html=True)

with col_kpi:
    st.markdown(f"""
    <div style='text-align:right;padding-top:4px;'>
      <div style='font-family:IBM Plex Mono,monospace;font-size:1.4rem;
                  font-weight:600;color:{PETROL_D};'>{n_days:,}</div>
      <div style='font-size:0.65rem;color:{GREY_MID};text-transform:uppercase;
                  letter-spacing:0.08em;'>Simulated Days</div>
      <div style='font-family:IBM Plex Mono,monospace;font-size:1rem;
                  font-weight:600;color:{ORANGE};margin-top:4px;'>{n_skus}</div>
      <div style='font-size:0.65rem;color:{GREY_MID};text-transform:uppercase;
                  letter-spacing:0.08em;'>SKUs</div>
    </div>""", unsafe_allow_html=True)
    

# ── SOH Chart
st.markdown("<div class='sec-hdr'>◆ Stock Evolution </div>", unsafe_allow_html=True)

if "date" in df_filtered.columns and "soh_final" in df_filtered.columns:
    if mode == "By SKU":
        df_plot = df_filtered.sort_values("date")
        x_min, x_max = df_plot["date"].min(), df_plot["date"].max()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_plot["date"], y=df_plot["soh_final"],
            mode="lines", name="SOH Final",
            line=dict(color=PETROL, width=2),
            fill="tozeroy", fillcolor="rgba(46,110,126,0.10)",
        ))
        if "demand" in df_plot.columns:
            fig.add_trace(go.Scatter(
                x=df_plot["date"], y=df_plot["demand"],
                mode="lines", name="Demand",
                line=dict(color=ORANGE, width=1.5, dash="dash"),
            ))
        if "forecast" in df_plot.columns:
            fig.add_trace(go.Scatter(
                x=df_plot["date"], y=df_plot["forecast"],
                mode="lines", name="Forecast",
                line=dict(color="#9B59B6", width=1.5, dash="dot"),
            ))
        if "stockout" in df_plot.columns:
            so = df_plot[df_plot["stockout"] > 0]
            if not so.empty:
                fig.add_trace(go.Scatter(
                    x=df_plot["date"],
                    y=df_plot["soh_final"],
                    mode="markers",
                    name="Stockout",
                    marker=dict(
                        color=df_plot["stockout"].apply(lambda x: "#C0392B" if x > 0 else "rgba(0,0,0,0)"),
                        size=df_plot["stockout"].apply(lambda x: 8 if x > 0 else 0),
                        symbol="x"
                    ),
                    customdata=df_plot["stockout"],
                    hovertemplate=(
                        "Stockout: %{customdata:.0f}<extra></extra>"
                    )
                ))
    else:
        df_agg = df_filtered.groupby("date")["soh_final"].sum().reset_index().sort_values("date")
        x_min, x_max = df_agg["date"].min(), df_agg["date"].max()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_agg["date"], y=df_agg["soh_final"],
            mode="lines", name="Total SOH (Class)",
            line=dict(color=PETROL, width=2),
            fill="tozeroy", fillcolor="rgba(46,110,126,0.10)",
        ))
   
    fig.update_layout(
        **PLOT, height=310, margin=dict(l=10,r=10,t=20,b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="right", x=1, bgcolor="rgba(0,0,0,0)"),
        yaxis=dict(gridcolor=GREY_BDR, title="Units", showgrid=True),
        xaxis=dict(gridcolor=GREY_BDR, showgrid=True,
                   range=[x_min-pd.Timedelta(days=1), x_max+pd.Timedelta(days=1)],
                   dtick="M1", tickformat="%b %Y", hoverformat="%d %b %Y"),
        hovermode="x unified",
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Columns 'date' or 'soh_final' not found in parquet file.")

# ── Cost Charts
cs_c = next((c for c in ["custo_stock_diario","custo_stock","stock_cost"] if c in df_filtered.columns), None)
ct_c = next((c for c in ["custo_transporte","transport_cost","custo_transporte_diario"] if c in df_filtered.columns), None)

if cs_c and ct_c and "date" in df_filtered.columns:
    st.markdown("<div class='sec-hdr'>◆ Monthly Cost Breakdown</div>", unsafe_allow_html=True)
    df_mes = df_filtered.copy()
    df_mes["month_label"] = df_mes["date"].dt.strftime("%b %Y")   # "Jan 2026"
    df_mes["month_sort"]  = df_mes["date"].dt.to_period("M").astype(str)  # para ordenar
    df_agg_m = df_mes.groupby(["month_sort", "month_label"])[[cs_c, ct_c]].sum().reset_index()
    df_agg_m = df_agg_m.sort_values("month_sort")
    col_bar, col_pie = st.columns([2,1])
    with col_bar:
        fig_b = go.Figure()
        fig_b.add_trace(go.Bar(x=df_agg_m["month_label"], y=df_agg_m[cs_c],
                               name="Stock Cost", marker_color=PETROL))
        fig_b.add_trace(go.Bar(x=df_agg_m["month_label"], y=df_agg_m[ct_c],
                               name="Transport Cost", marker_color=ORANGE))
        fig_b.update_layout(**PLOT, barmode="stack", height=260,
                            margin=dict(l=10,r=10,t=20,b=10),
                            yaxis=dict(gridcolor=GREY_BDR, title="€"),
                            legend=dict(orientation="h", yanchor="bottom", y=1.02,
                                        bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig_b, use_container_width=True)
    with col_pie:
        fig_p = go.Figure(go.Pie(
            labels=["Stock Cost","Transport Cost"],
            values=[df_agg_m[cs_c].sum(), df_agg_m[ct_c].sum()],
            hole=0.55, marker=dict(colors=["#5BA3B5", "#F0A868"]),
        ))
        fig_p.update_layout(**PLOT, height=260, margin=dict(l=10,r=10,t=10,b=10))
        st.plotly_chart(fig_p, use_container_width=True)

# ── Performance Metrics
metrics = compute_metrics(df_filtered)

# Inject MOQ from params file (SKU mode only — not shown for class)
if mode == "By SKU" and moq_map:
    moq_val = moq_map.get(sku_sel, np.nan)
    metrics["moq"] = moq_val if pd.notna(moq_val) else np.nan

st.markdown("<div class='sec-hdr'>◆ Performance Metrics</div>", unsafe_allow_html=True)

defs = [
    ("fill_rate",    "Fill Rate β",           ",.2f", "%",      ""),
    ("stockout_rate", "Stockout Rate",        ",.2f", "%", ""),
    ("csl",          "CSL α (Cycle Service)",  ",.2f", "%",      ""),
    ("stockout_days","Stockout Days",          ",.0f", " days",  ""),
    ("pct_zero",     "% Days Stock = 0",       ",.2f", "%",      ""),
    ("stock_medio",  "Average Stock",          ",.2f", " units", ""),
    ("stock_minimo", "Minimum Stock",          ",.0f", " units", ""),
    ("stock_maximo", "Maximum Stock",          ",.0f", " units", ""),
    ("ss_medio",     "Avg Safety Stock",       ",.2f", " units", ""),
    ("cobertura",    "Average Coverage",       ",.0f", " days",  ""),
    ("num_orders",   "Number of Orders",       ",.0f", "",       ""),
]

# MOQ only shown in By SKU mode
if mode == "By SKU":
    defs.append(("moq", "MOQ ", ",.0f", " units", ""))

defs += [
    ("cost_stock",    "Stock Cost",      ",.2f", "", "€"),
    ("cost_transport","Transport Cost",  ",.2f", "", "€"),
    ("cost_total",    "Total Cost",      ",.2f", "", "€"),
]

for row in [defs[i:i+4] for i in range(0, len(defs), 4)]:
    cols = st.columns(4)
    for idx, (key, lbl, fmt, suf, pre) in enumerate(row):
        val = metrics.get(key)
        c_card, c_val = mcss(key, val)
        with cols[idx]:
            st.markdown(f"""
            <div class="kcard {c_card}">
              <div class="klbl">{lbl}</div>
              <div class="kval {c_val}">{fv(val, fmt, suf, pre)}</div>
            </div>""", unsafe_allow_html=True)

# ── SKU list (class mode only) — just show which SKUs are in this class
if mode == "By ABC/XYZ Class":
    st.markdown("<div class='sec-hdr'>◆ SKUs in this Class</div>", unsafe_allow_html=True)
    sku_list = sorted(df_filtered["sku"].unique()) if "sku" in df_filtered.columns else []
    if sku_list:
        # Build a simple table: SKU | ABC/XYZ Class
        df_sku_tbl = pd.DataFrame({"SKU": sku_list})
        df_sku_tbl["ABC/XYZ Class"] = class_sel
        # Add MOQ if available
        if moq_map:
            df_sku_tbl["MOQ "] = df_sku_tbl["SKU"].map(
                lambda s: f"{int(moq_map[s]):,}" if s in moq_map and pd.notna(moq_map[s]) else "—"
            )
        st.dataframe(df_sku_tbl, use_container_width=True, height=min(400, 40 + 35 * len(sku_list)), hide_index=True)
    else:
        st.info("No SKUs found for this class in the selected parquet file.")

# ── Best Combination
st.markdown("<div class='sec-hdr'>◆ Best Combination Finder</div>", unsafe_allow_html=True)
with st.spinner("Evaluating all combinations..."):
    res = find_best(parquets_meta, df_abc, bc_mode, sku_or_class, fill_rate_target)

if res:
    best, df_combos, met_target = res
    col_b, col_t = st.columns([1,2])
    with col_b:
        if met_target:
            badge_html = f"<span class='best-badge' style='background:#2E8B57;'>✓ Fill Rate ≥ {fill_rate_target}%</span>"
            criterion_txt = f"Fill Rate ≥ {fill_rate_target}% satisfied → lowest cost selected"
        else:
            badge_html = f"<span class='best-badge' style='background:#C9850A;'>⚠ Target not met</span>"
            criterion_txt = f"No combination reaches {fill_rate_target}% — best available fill rate shown"
        st.markdown(f"""
        <div class="bestbox">
          <div class="bestbox-ttl">🏆 Recommended Combination</div>
          <div class="best-combo">
            {policy_label(best['policy'])} · SL {best['ns']}% · k={best['k']}
            {badge_html}
          </div>
          <div class="best-detail">
            Fill Rate: <b style='color:{PETROL};'>{best['fill_rate']:.2f}%</b>
            &nbsp;|&nbsp;
            Total Cost: <b style='color:{ORANGE};'>€{best['cost_total']:,.2f}</b><br>
            <i>{criterion_txt}</i>
          </div>
        </div>""", unsafe_allow_html=True)
    with col_t:
        df_show = df_combos.copy()
        df_show["Policy"]          = df_show["policy"].apply(policy_label)
        df_show["SL (%)"]          = df_show["ns"]
        df_show["Fill Rate β (%)"] = df_show["fill_rate"].map("{:.2f}".format)
        df_show["Total Cost (€)"]  = df_show["cost_total"].map("{:,.2f}".format)
        df_show["Meets Target"]    = df_show["fill_rate"].apply(
            lambda x: "✓" if x >= fill_rate_target else "✗"
        )
        df_show = df_show[["Policy","SL (%)","k","Fill Rate β (%)","Total Cost (€)","Meets Target"]] \
                          .sort_values("Fill Rate β (%)", ascending=False)
        st.dataframe(df_show, use_container_width=True, height=150, hide_index=True)
else:
    total_demand = df_filtered["demand"].sum() if "demand" in df_filtered.columns else 0
    total_forecast = df_filtered["forecast"].sum() if "forecast" in df_filtered.columns else 0
    if total_demand == 0 and total_forecast == 0:
        st.info("Demand and forecast are both 0 throughout the simulated period — it was not possible to evaluate the best parameter combination for this SKU.")
    else:
        st.warning("Could not evaluate combinations — check that parquet files contain cost and fill rate columns.")


st.markdown("---")
st.caption("📦 Stock Management Simulator · Group 3 – MEGI · Supply Chain Management")