import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, timedelta
import calendar

st.set_page_config(page_title="GEELY Sales Dashboard", layout="wide", initial_sidebar_state="expanded")

SHEET_URL = "https://docs.google.com/spreadsheets/d/1ezLtX2FMnPSFVvyFQ9mdNyiAgw17xvL0XwPeuWC5u80/export?format=csv&gid=1265787437"

st.markdown("""
<style>
[data-testid="stSidebar"] { min-width: 200px !important; max-width: 200px !important; }
[data-testid="stSidebar"] .block-container { padding: 1rem 0.5rem; }
div[data-testid="metric-container"] { background: var(--background-secondary-color, #f8f9fa); border-radius: 8px; padding: 0.75rem 1rem; }
.geely-logo { display: flex; align-items: center; gap: 10px; padding: 0.5rem 0.5rem 1rem; border-bottom: 1px solid rgba(128,128,128,0.2); margin-bottom: 0.75rem; }
.geely-logo img { width: 36px; height: 36px; object-fit: contain; }
.geely-title { font-size: 14px; font-weight: 600; line-height: 1.2; }
.geely-sub { font-size: 10px; opacity: 0.5; }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)
def load_data():
    df = pd.read_csv(SHEET_URL)
    df.columns = df.columns.astype(str).str.replace("\n", " ").str.strip()
    return df

df = load_data()

date_col   = "Дата продажи"
model_col  = "Model 2 车型"
dealer_col = "Dealer"

df[date_col] = pd.to_datetime(df[date_col], dayfirst=True, errors="coerce")
df = df.dropna(subset=[date_col])
df["Месяц"] = df[date_col].dt.to_period("M").astype(str)

# ----------------------------
# SIDEBAR
# ----------------------------
with st.sidebar:
    st.markdown("""
    <div class="geely-logo">
      <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Geely_logo.svg/240px-Geely_logo.svg.png"/>
      <div>
        <div class="geely-title">Geely KZ</div>
        <div class="geely-sub">Sales Dashboard</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.caption("ДИЛЕРЫ")
    dealers_list = ["Все"] + sorted(df[dealer_col].dropna().unique().tolist())
    selected_dealer = st.radio("", dealers_list, label_visibility="collapsed")

# ----------------------------
# PERIOD FILTER
# ----------------------------
today = date.today()
first_this_month  = today.replace(day=1)
first_last_month  = (first_this_month - timedelta(days=1)).replace(day=1)
last_last_month   = first_this_month - timedelta(days=1)
first_this_year   = today.replace(month=1, day=1)

col_p1, col_p2, col_p3, col_m = st.columns([1, 1, 1, 2])

with col_p1:
    btn1 = st.button("Этот месяц", use_container_width=True)
with col_p2:
    btn2 = st.button("Прошлый месяц", use_container_width=True)
with col_p3:
    btn3 = st.button("Этот год", use_container_width=True)
with col_m:
    models_list = ["Все модели"] + sorted(df[model_col].dropna().unique().tolist())
    selected_model = st.selectbox("", models_list, label_visibility="collapsed")

if "period_start" not in st.session_state:
    st.session_state.period_start = first_this_month
    st.session_state.period_end   = today

if btn1:
    st.session_state.period_start = first_this_month
    st.session_state.period_end   = today
if btn2:
    st.session_state.period_start = first_last_month
    st.session_state.period_end   = last_last_month
if btn3:
    st.session_state.period_start = first_this_year
    st.session_state.period_end   = today

period_start = st.session_state.period_start
period_end   = st.session_state.period_end

# ----------------------------
# APPLY FILTERS
# ----------------------------
mask = (
    (df[date_col].dt.date >= period_start) &
    (df[date_col].dt.date <= period_end)
)
dff = df[mask].copy()

if selected_dealer != "Все":
    dff = dff[dff[dealer_col] == selected_dealer]
if selected_model != "Все модели":
    dff = dff[dff[model_col] == selected_model]

today_df = dff[dff[date_col].dt.date == today]

st.divider()

# ----------------------------
# KPI
# ----------------------------
k1, k2, k3, k4 = st.columns(4)

total_sales = len(dff)
top_model   = dff[model_col].value_counts().index[0] if len(dff) > 0 else "—"
top_model_n = dff[model_col].value_counts().iloc[0]  if len(dff) > 0 else 0
top_dealer  = dff[dealer_col].value_counts().index[0] if len(dff) > 0 else "—"
top_dealer_n= dff[dealer_col].value_counts().iloc[0]  if len(dff) > 0 else 0

k1.metric("Продажи за период", total_sales)
k2.metric("Топ модель", top_model, f"{top_model_n} шт.")
k3.metric("Топ дилер", top_dealer, f"{top_dealer_n} шт.")
k4.metric("Контракты", "—", "данные скоро", delta_color="off")

st.divider()

# ----------------------------
# CHARTS
# ----------------------------
st.subheader("Продажи по месяцам")
monthly = dff.groupby("Месяц").size().reset_index(name="Продажи")
fig1 = px.bar(monthly, x="Месяц", y="Продажи", text="Продажи", color_discrete_sequence=["#1B4F9B"])
fig1.update_traces(textposition="outside")
fig1.update_layout(margin=dict(t=10, b=10), height=260, showlegend=False)
st.plotly_chart(fig1, use_container_width=True)

c1, c2 = st.columns(2)

with c1:
    st.subheader("По моделям")
    ms = dff.groupby(model_col).size().reset_index(name="Продажи").sort_values("Продажи", ascending=False)
    fig2 = px.bar(ms, x=model_col, y="Продажи", text="Продажи", color_discrete_sequence=["#1B4F9B"])
    fig2.update_traces(textposition="outside")
    fig2.update_layout(margin=dict(t=10, b=10), height=240, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

with c2:
    st.subheader("По дилерам")
    ds = dff.groupby(dealer_col).size().reset_index(name="Продажи").sort_values("Продажи", ascending=False)
    fig3 = px.bar(ds, x=dealer_col, y="Продажи", text="Продажи", color_discrete_sequence=["#1B4F9B"])
    fig3.update_traces(textposition="outside")
    fig3.update_layout(margin=dict(t=10, b=10), height=240, showlegend=False, xaxis_tickangle=-30)
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ----------------------------
# СЕГОДНЯ + КОНТРАКТЫ
# ----------------------------
t1, t2 = st.columns(2)

with t1:
    st.subheader(f"Продажи сегодня — {today.strftime('%d.%m.%Y')}")
    if len(today_df) == 0:
        st.info("Сегодня продаж пока нет")
    else:
        today_by_model = today_df.groupby(model_col).size().reset_index(name="Шт.").sort_values("Шт.", ascending=False)
        st.dataframe(today_by_model, use_container_width=True, hide_index=True)

with t2:
    st.subheader("Контракты")
    st.info("Данные по контрактам подключатся позже — место зарезервировано")

with st.expander("Таблица данных"):
    st.dataframe(dff, use_container_width=True, hide_index=True)
