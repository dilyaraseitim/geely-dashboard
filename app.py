import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="GEELY BI Dashboard", layout="wide")
st.title("📊 GEELY Sales Dashboard")

# ----------------------------
# LOAD DATA
# ----------------------------
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ezLtX2FMnPSFVvyFQ9mdNyiAgw17xvL0XwPeuWC5u80/export?format=csv&gid=1265787437"

@st.cache_data(ttl=300)
def load_data():
    df = pd.read_csv(SHEET_URL)
    df.columns = df.columns.astype(str).str.strip()
    return df

df = load_data()
st.write(df.columns.tolist())

# ----------------------------
# PREP
# ----------------------------
date_col = "Дата продажи"
model_col = "Model 2"

df[date_col] = pd.to_datetime(df[date_col], dayfirst=True, errors="coerce")
df = df.dropna(subset=[date_col])
df["Месяц"] = df[date_col].dt.to_period("M").astype(str)

# ----------------------------
# FILTERS
# ----------------------------
st.sidebar.header("Фильтры")

min_date = df[date_col].min()
max_date = df[date_col].max()

date_from = st.sidebar.date_input("С", value=min_date, min_value=min_date, max_value=max_date)
date_to = st.sidebar.date_input("По", value=max_date, min_value=min_date, max_value=max_date)

df = df[
    (df[date_col] >= pd.to_datetime(date_from)) &
    (df[date_col] <= pd.to_datetime(date_to))
]

if "Dealer" in df.columns:
    dealers = ["Все"] + sorted(df["Dealer"].dropna().unique().tolist())
    selected_dealer = st.sidebar.selectbox("Дилер", dealers)
    if selected_dealer != "Все":
        df = df[df["Dealer"] == selected_dealer]

models = ["Все"] + sorted(df[model_col].dropna().unique().tolist())
selected_model = st.sidebar.selectbox("Модель", models)
if selected_model != "Все":
    df = df[df[model_col] == selected_model]

# ----------------------------
# KPI
# ----------------------------
st.subheader("📌 KPI")

total_sales = len(df)
monthly_counts = df.groupby("Месяц").size()
avg_monthly = round(monthly_counts.mean(), 1) if len(monthly_counts) > 0 else 0

col1, col2 = st.columns(2)
col1.metric("Всего продаж", total_sales)
col2.metric("Среднее в месяц", avg_monthly)

# ----------------------------
# 1. ПРОДАЖИ ПО МЕСЯЦАМ
# ----------------------------
st.subheader("📅 Продажи по месяцам")

monthly_sales = df.groupby("Месяц").size().reset_index(name="Продажи")

fig1 = px.bar(
    monthly_sales,
    x="Месяц",
    y="Продажи",
    text="Продажи",
    title="Продажи по месяцам"
)
fig1.update_traces(textposition="outside")
st.plotly_chart(fig1, use_container_width=True)

# ----------------------------
# 2. ПРОДАЖИ ПО МОДЕЛЯМ
# ----------------------------
st.subheader("🚗 Продажи по моделям")

model_sales = df.groupby(model_col).size().reset_index(name="Продажи")
model_sales = model_sales.sort_values("Продажи", ascending=False)

fig2 = px.bar(
    model_sales,
    x=model_col,
    y="Продажи",
    text="Продажи",
    title="Продажи по моделям"
)
fig2.update_traces(textposition="outside")
st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# 3. ПРОДАЖИ ПО ДИЛЕРАМ
# ----------------------------
if "Dealer" in df.columns:
    st.subheader("🏢 Продажи по дилерам")

    dealer_sales = df.groupby("Dealer").size().reset_index(name="Продажи")
    dealer_sales = dealer_sales.sort_values("Продажи", ascending=False)

    fig3 = px.bar(
        dealer_sales,
        x="Dealer",
        y="Продажи",
        text="Продажи",
        title="Продажи по дилерам"
    )
    fig3.update_traces(textposition="outside")
    st.plotly_chart(fig3, use_container_width=True)

# ----------------------------
# 4. МОДЕЛЬ × МЕСЯЦ (тепловая карта)
# ----------------------------
st.subheader("🗓️ Модель по месяцам")

pivot = df.groupby(["Месяц", model_col]).size().reset_index(name="Продажи")

fig4 = px.density_heatmap(
    pivot,
    x="Месяц",
    y=model_col,
    z="Продажи",
    color_continuous_scale="Blues",
    title="Продажи: модель × месяц"
)
st.plotly_chart(fig4, use_container_width=True)

# ----------------------------
# 5. ТАБЛИЦА
# ----------------------------
st.subheader("📋 Данные")
st.dataframe(df, use_container_width=True)
