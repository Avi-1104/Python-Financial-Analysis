import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go

# ============================================================
# PAGE SETUP
# ============================================================
st.set_page_config(page_title="Financial Intelligence", layout="wide")

# ============================================================
# THEME TOGGLE
# ============================================================
theme_choice = st.sidebar.radio("Theme", ["Dark", "Light"], horizontal=True)

if theme_choice == "Dark":
    T = {
        "bg": "#0B0E14", "card": "#141821", "border": "#1F2530",
        "border_hover": "#2B3340", "title": "#FFFFFF", "text": "#B4BAC4",
        "muted": "#6B7280", "section": "#9CA3AF", "grid": "#161B24",
        "accent": "#3B82F6", "up": "#16B981", "down": "#EF5350",
        "table_bg": "rgba(0,0,0,0)"
    }
else:
    T = {
        "bg": "#F7F8FA", "card": "#FFFFFF", "border": "#E3E7ED",
        "border_hover": "#C7CDD6", "title": "#0B0E14", "text": "#3F4654",
        "muted": "#8A92A0", "section": "#6B7280", "grid": "#E8EBEF",
        "accent": "#2563EB", "up": "#059669", "down": "#DC2626",
        "table_bg": "rgba(0,0,0,0)"
    }

# ============================================================
# STYLING (theme-aware)
# ============================================================
st.markdown(f"""
<style>
    #MainMenu, footer, header {{visibility: hidden;}}

    .stApp {{ background: {T['bg']}; }}

    .main-title {{
        font-size: 1.9rem; font-weight: 600; color: {T['title']};
        letter-spacing: -0.4px; margin-bottom: 2px;
    }}
    .main-sub {{
        font-size: 0.9rem; color: {T['muted']}; margin-top: 0;
        margin-bottom: 1.8rem; font-weight: 400;
    }}

    .kpi-card {{
        background: {T['card']}; border: 1px solid {T['border']};
        border-radius: 10px; padding: 18px 20px;
        transition: border-color 0.2s ease;
    }}
    .kpi-card:hover {{ border-color: {T['border_hover']}; }}
    .kpi-label {{
        font-size: 0.72rem; color: {T['muted']}; text-transform: uppercase;
        letter-spacing: 0.8px; margin-bottom: 8px; font-weight: 500;
    }}
    .kpi-value {{
        font-size: 1.6rem; font-weight: 600; color: {T['title']}; line-height: 1.1;
    }}
    .kpi-delta {{ font-size: 0.85rem; font-weight: 500; margin-top: 6px; }}
    .pos {{ color: {T['up']}; }}
    .neg {{ color: {T['down']}; }}

    .section-h {{
        font-size: 0.8rem; font-weight: 600; color: {T['section']};
        text-transform: uppercase; letter-spacing: 0.8px;
        margin: 2rem 0 0.8rem 0; padding-bottom: 8px;
        border-bottom: 1px solid {T['border']};
    }}

    .insight-box {{
        background: {T['card']}; border-left: 2px solid {T['accent']};
        border-radius: 6px; padding: 14px 18px; margin-bottom: 10px;
        color: {T['text']}; font-size: 0.92rem; line-height: 1.55;
    }}
    .insight-box b {{ color: {T['title']}; font-weight: 600; }}

    .disclaimer {{
        font-size: 0.8rem; color: {T['muted']}; margin-top: 8px; line-height: 1.5;
    }}
    /* Sidebar container */
    section[data-testid="stSidebar"] {{
        background: {T['card']};
        border-right: 1px solid {T['border']};
    }}

    /* Sidebar text — title, labels, captions */
    section[data-testid="stSidebar"] * {{
        color: {T['text']} !important;
    }}
    section[data-testid="stSidebar"] h1 {{
        color: {T['title']} !important;
    }}

    /* Sidebar dropdown / multiselect boxes */
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {{
        background: {T['bg']} !important;
        border-color: {T['border']} !important;
    }}

    /* Sidebar divider lines */
    section[data-testid="stSidebar"] hr {{
        border-color: {T['border']};
    }}
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# ============================================================
prices = pd.read_csv("data/close_prices.csv", index_col=0, parse_dates=True)

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.title("Controls")
st.sidebar.markdown("---")

all_stocks = list(prices.columns)
selected = st.sidebar.multiselect("Select stocks", all_stocks, default=all_stocks)

if not selected:
    st.warning("Please select at least one stock from the sidebar.")
    st.stop()

prices = prices[selected]
ticker = st.sidebar.selectbox("Focus stock", selected)
st.sidebar.markdown("---")
st.sidebar.caption("Built with Python and Streamlit")

# ============================================================
# CALCULATIONS
# ============================================================
daily_returns = prices.pct_change()
total_return = (prices.iloc[-1] / prices.iloc[0] - 1) * 100
volatility = daily_returns.std() * (252 ** 0.5) * 100
sharpe = (daily_returns.mean() * 252 * 100) / volatility

best_stock, best_value = total_return.idxmax(), total_return.max()
riskiest, riskiest_val = volatility.idxmax(), volatility.max()

# ============================================================
# INSIGHT GENERATOR
# ============================================================
def generate_insights():
    notes = []
    notes.append(
        f"<b>{best_stock}</b> leads the group with a <b>{best_value:.1f}%</b> return "
        f"over the period, marking it the strongest performer."
    )
    best_sharpe_stock = sharpe.idxmax()
    notes.append(
        f"On a risk-adjusted basis, <b>{best_sharpe_stock}</b> stands out with a "
        f"Sharpe ratio of <b>{sharpe.max():.2f}</b>, the most efficient return per unit of risk."
    )
    notes.append(
        f"<b>{riskiest}</b> is the most volatile at <b>{riskiest_val:.1f}%</b> annualized risk, "
        f"suitable only for risk-tolerant investors."
    )
    worst_stock = total_return.idxmin()
    worst_val = total_return.min()
    if worst_val < 0:
        notes.append(
            f"<b>{worst_stock}</b> underperformed with a <b>{worst_val:.1f}%</b> loss, "
            f"warranting caution."
        )
    else:
        notes.append(
            f"<b>{worst_stock}</b> showed the weakest growth at <b>{worst_val:.1f}%</b>, "
            f"lagging the group."
        )
    return notes

# ============================================================
# HEADER
# ============================================================
st.markdown('<div class="main-title">Financial Intelligence Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="main-sub">Stock performance, risk analysis, and market insights</div>', unsafe_allow_html=True)

# ============================================================
# KPI CARDS
# ============================================================
def kpi(col, label, value, delta=None, positive=True):
    delta_html = ""
    if delta is not None:
        cls = "pos" if positive else "neg"
        arrow = "+" if positive else "-"
        delta_html = f'<div class="kpi-delta {cls}">{arrow}{delta}</div>'
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
kpi(c1, "Best Performer", best_stock, f"{abs(best_value):.1f}%", positive=best_value >= 0)
kpi(c2, "Most Volatile", riskiest, f"{riskiest_val:.1f}% risk", positive=False)
kpi(c3, "Stocks Tracked", str(len(selected)))
kpi(c4, "Trading Days", str(len(prices)))

# ============================================================
# MARKET INTELLIGENCE
# ============================================================
st.markdown('<div class="section-h">Market Intelligence</div>', unsafe_allow_html=True)
for note in generate_insights():
    st.markdown(f'<div class="insight-box">{note}</div>', unsafe_allow_html=True)

# ============================================================
# CANDLESTICK
# ============================================================
st.markdown(f'<div class="section-h">{ticker} — Price Action</div>', unsafe_allow_html=True)

data = yf.download(ticker, period="6mo")
data.columns = [c[0] if isinstance(c, tuple) else c for c in data.columns]

fig = go.Figure(data=[go.Candlestick(
    x=data.index, open=data["Open"], high=data["High"],
    low=data["Low"], close=data["Close"],
    increasing_line_color=T["up"], decreasing_line_color=T["down"]
)])
fig.update_layout(
    xaxis_rangeslider_visible=False, height=380,
    margin=dict(t=10, b=10, l=10, r=10),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=T["muted"]),
    xaxis=dict(gridcolor=T["grid"]), yaxis=dict(gridcolor=T["grid"])
)
st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TWO-COLUMN GRID
# ============================================================
left, right = st.columns(2)
with left:
    st.markdown('<div class="section-h">Price Trends</div>', unsafe_allow_html=True)
    st.line_chart(prices, height=280)
with right:
    st.markdown('<div class="section-h">Relative Performance</div>', unsafe_allow_html=True)
    st.line_chart(prices / prices.iloc[0] * 100, height=280)

# ============================================================
# PRICE FORECAST
# ============================================================
st.markdown(f'<div class="section-h">{ticker} — 30-Day Trend Projection</div>', unsafe_allow_html=True)

series = prices[ticker].dropna()
x = np.arange(len(series))
slope, intercept = np.polyfit(x, series.values, 1)

future_x = np.arange(len(series), len(series) + 30)
future_prices = slope * future_x + intercept
future_dates = pd.bdate_range(series.index[-1], periods=31)[1:]

fig_fc = go.Figure()
fig_fc.add_trace(go.Scatter(
    x=series.index, y=series.values,
    name="Historical", line=dict(color=T["accent"], width=2)
))
fig_fc.add_trace(go.Scatter(
    x=future_dates, y=future_prices,
    name="Projected", line=dict(color=T["up"], width=2, dash="dash")
))
fig_fc.update_layout(
    height=340, margin=dict(t=10, b=10, l=10, r=10),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=T["muted"]), legend=dict(orientation="h", y=1.12),
    xaxis=dict(gridcolor=T["grid"]), yaxis=dict(gridcolor=T["grid"])
)
st.plotly_chart(fig_fc, use_container_width=True)

direction = "upward" if slope > 0 else "downward"
st.markdown(
    f'<div class="disclaimer">Based on the recent trend, {ticker} shows a {direction} '
    f'trajectory. This is a simple statistical projection, not financial advice. '
    f'Markets are influenced by many unpredictable factors.</div>',
    unsafe_allow_html=True
)

# ============================================================
# ANALYST SUMMARY
# ============================================================
st.markdown('<div class="section-h">Analyst Summary</div>', unsafe_allow_html=True)
summary = pd.DataFrame({
    "Total Return (%)": total_return.round(2),
    "Volatility (%)": volatility.round(2),
    "Sharpe Ratio": sharpe.round(2)
})
st.dataframe(summary, use_container_width=True)