import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="GEELY Sales Dashboard", layout="wide")
st.title("📊 GEELY Sales Dashboard")

# ----------------------------
# LOAD DATA
# ----------------------------
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ezLtX2FMnPSFVvyFQ9mdNyiAgw17xvL0XwPeuWC5u80/export?format=csv&gid=1265787437"

@st.cache_data(ttl=300)
def load_data():
    df = pd.read_csv(SHEET_URL)
    # убираем переносы строк и пробелы из названий колонок
    df.columns = df.columns.astype(str).str.replace("\n", " ").str.strip()
    return df

df = load_data()

date_col = "Дата продажи"
model_col = "Model 2 车型"
dealer_col = "Dealer"

df[date_col] = pd.to_datetime(df[date_col], dayfirst=True, errors="coerce")
df = df.dropna(subset=[date_col])
df["Месяц"] = df[date_col].dt.to_period("M").astype(str)

# ----------------------------
# ФИЛЬТРЫ — компактно в одну строку
# ----------------------------
col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    min_date = df[date_col].min().date()
    max_date = df[date_col].max().date()
    date_range = st.date_input("📅 Период", value=(min_date, max_date), min_value=min_date, max_value=max_date)

with col_f2:
    dealers = ["Все"] + sorted(df[dealer_col].dropna().unique().tolist())
    selected_dealer = st.selectbox("🏢 Дилер", dealers)

with col_f3:
    models = ["Все"] + sorted(df[model_col].dropna().unique().tolist())
    selected_model = st.selectbox("🚗 Модель", models)

# применяем фильтры
if len(date_range) == 2:
    df = df[
        (df[date_col] >= pd.to_datetime(date_range[0])) &
        (df[date_col] <= pd.to_datetime(date_range[1]))
    ]

if selected_dealer != "Все":
    df = df[df[dealer_col] == selected_dealer]

if selected_model != "Все":
    df = df[df[model_col] == selected_model]

st.divider()

# ----------------------------
# KPI
# ----------------------------
total_sales = len(df)
monthly_counts = df.groupby("Месяц").size()
avg_monthly = round(monthly_counts.mean(), 1) if len(monthly_counts) > 0 else 0
top_model = df[model_col].value_counts().idxmax() if len(df) > 0 else "—"
top_dealer = df[dealer_col].value_counts().idxmax() if len(df) > 0 else "—"

k1, k2, k3, k4 = st.columns(4)
k1.metric("Всего продаж", total_sales)
k2.metric("Среднее в месяц", avg_monthly)
k3.metric("Топ модель", top_model)
k4.metric("Топ дилер", top_dealer)

st.divider()

# ----------------------------
# 1. ПРОДАЖИ ПО МЕСЯЦАМ
# ----------------------------
st.subheader("📅 Продажи по месяцам")

monthly_sales = df.groupby("Месяц").size().reset_index(name="Продажи")
fig1 = px.bar(monthly_sales, x="Месяц", y="Продажи", text="Продажи")
fig1.update_traces(textposition="outside")
fig1.update_layout(margin=dict(t=30))
st.plotly_chart(fig1, use_container_width=True)

# ----------------------------
# 2. ПРОДАЖИ ПО МОДЕЛЯМ
# ----------------------------
st.subheader("🚗 Продажи по моделям")

model_sales = df.groupby(model_col).size().reset_index(name="Продажи")
model_sales = model_sales.sort_values("Продажи", ascending=False)
fig2 = px.bar(model_sales, x=model_col, y="Продажи", text="Продажи")
fig2.update_traces(textposition="outside")
fig2.update_layout(margin=dict(t=30))
st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# 3. ПРОДАЖИ ПО ДИЛЕРАМ
# ----------------------------
st.subheader("🏢 Продажи по дилерам")

dealer_sales = df.groupby(dealer_col).size().reset_index(name="Продажи")
dealer_sales = dealer_sales.sort_values("Продажи", ascending=False)
fig3 = px.bar(dealer_sales, x=dealer_col, y="Продажи", text="Продажи")
fig3.update_traces(textposition="outside")
fig3.update_layout(margin=dict(t=30))
st.plotly_chart(fig3, use_container_width=True)

# ----------------------------
# 4. ТЕПЛОВАЯ КАРТА МОДЕЛЬ × МЕСЯЦ
# ----------------------------
st.subheader("🗓️ Модель по месяцам")

pivot = df.groupby(["Месяц", model_col]).size().reset_index(name="Продажи")
fig4 = px.density_heatmap(pivot, x="Месяц", y=model_col, z="Продажи", color_continuous_scale="Blues")
fig4.update_layout(margin=dict(t=30))
st.plotly_chart(fig4, use_container_width=True)

# ----------------------------
# 5. ТАБЛИЦА
# ----------------------------
with st.expander("📋 Показать таблицу данных"):
    st.dataframe(df, use_container_width=True)
