import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, timedelta
import re

st.set_page_config(page_title="GEELY Sales Dashboard", layout="wide", initial_sidebar_state="expanded")

MAIN_SHEET_URL = "https://docs.google.com/spreadsheets/d/1ezLtX2FMnPSFVvyFQ9mdNyiAgw17xvL0XwPeuWC5u80/export?format=csv&gid=1265787437"

DEALER_SHEETS = {
    "Aktau": "https://docs.google.com/spreadsheets/d/1EJRyBfDhz98tsZwMveyPlidGSFBDlcm-J0AK0UXHwd0/export?format=csv&gid=1077962440",
    "Dealer 02": "https://docs.google.com/spreadsheets/d/1vw6TOlN6n8Wcp23WpuGt1uYAmt2cBBTSEs1Ap4tILaw/export?format=csv&gid=1077962440",
    "Dealer 03": "https://docs.google.com/spreadsheets/d/1Wiql53qEcO-Qxdd9Ev2NkeRoV808jKkNFNiOeDzM3rE/export?format=csv&gid=1077962440",
    "Dealer 04": "https://docs.google.com/spreadsheets/d/1YHhYj9O4tcc9aaI1tnj2a8T6MAiini6u358pcvyr_MA/export?format=csv&gid=1077962440",
    "Dealer 05": "https://docs.google.com/spreadsheets/d/1xJD6aSbd1PjeR32YAVioSSlBywXeKAvdOVF7mwQmMyw/export?format=csv&gid=1077962440",
    "Dealer 06": "https://docs.google.com/spreadsheets/d/1TSM6sCKF9Wmk1vKecKcYq9zDoOG84hFTkuOC8eF7jPc/export?format=csv&gid=1077962440",
    "Dealer 07": "https://docs.google.com/spreadsheets/d/1TjqZWqMIbtMpeIJX2ie8NRlBbr-6Fn5b89-sSwKbmnI/export?format=csv&gid=1077962440",
    "Dealer 08": "https://docs.google.com/spreadsheets/d/1HmWFn0-DHyqx8yvR-NN2bwubX-WVr4sfBdZSwIVmDpI/export?format=csv&gid=1077962440",
    "Dealer 09": "https://docs.google.com/spreadsheets/d/1ZWZB8DQg6ZLxWMbO3x6-oylph5_K1rlTzcKNLhYgV8Q/export?format=csv&gid=1077962440",
    "Dealer 10": "https://docs.google.com/spreadsheets/d/1eurtgsR32wFrpKgk9Vbfrlwoo4qQuNh_DZKgKwV053Q/export?format=csv&gid=1077962440",
    "Dealer 11": "https://docs.google.com/spreadsheets/d/1Nmzns3SHlt-D87rYGGATXM3tj7WRFzL7DGpLCErTo6M/export?format=csv&gid=1077962440",
    "Dealer 12": "https://docs.google.com/spreadsheets/d/1FLf5xbPdRrYiOuSKODio2YxkWKcCe0LlF9SaeBRNiGw/export?format=csv&gid=1077962440",
    "Dealer 13": "https://docs.google.com/spreadsheets/d/1wMCv_E4uRyycqLRu3BcmMpy0Uku_LYJ_RySirMHqWWM/export?format=csv&gid=1077962440",
    "Dealer 14": "https://docs.google.com/spreadsheets/d/10GlX9hhjAUPSQ838QkF9ilPUF3L0NWU5837eBVFEfyw/export?format=csv&gid=1077962440",
    "Dealer 15": "https://docs.google.com/spreadsheets/d/1qyuscUVpMmBzQmtllOzFgkB7ZZfcGBxJjsLeraO9JmU/export?format=csv&gid=1077962440",
    "Dealer 16": "https://docs.google.com/spreadsheets/d/1CTBHlE6_8zcPWjsdzhW9e2h6kLv26mqRc1fHEo1uC_M/export?format=csv&gid=1077962440",
    "Dealer 17": "https://docs.google.com/spreadsheets/d/1QI9VPyBvt17M_MH7ycA3WLvBiMKULs7b8woAq-iQ5oA/export?format=csv&gid=1077962440",
    "Dealer 18": "https://docs.google.com/spreadsheets/d/1EvRcSM7Z19_uZrwykc8dRB9AqNLTn7yg7afUi9QgwSk/export?format=csv&gid=1077962440",
    "Dealer 19": "https://docs.google.com/spreadsheets/d/1nEAUrzLxZelIBJDMgxmQOfYV0XvOvC6A1PkHlOQy_IE/export?format=csv&gid=1077962440",
    "Dealer 20": "https://docs.google.com/spreadsheets/d/1ezDMETw-Od7E87vJAPo1jOfX3sdVRppig3S1ZQiVpfA/export?format=csv&gid=1077962440",
    "Dealer 21": "https://docs.google.com/spreadsheets/d/1uDY9TV5cAqyCrEAWY_krZA0J_r8JH-9zNyoP3XsV2rk/export?format=csv&gid=1077962440",
    "Dealer 22": "https://docs.google.com/spreadsheets/d/1FZk-oTRBqrwuJAFkI63l-o0tGKKNlqjrHxj2GiDu7j8/export?format=csv&gid=1077962440",
    "Dealer 23": "https://docs.google.com/spreadsheets/d/1fOlimW-a6sqeinlWC9ULO3rFZEHS8fmkhS3yOcZoWks/export?format=csv&gid=1077962440",
    "Dealer 24": "https://docs.google.com/spreadsheets/d/1a7GFeKeEt30xGQFmdzxBo1Qno84kD8ge8WLnL6jVqcE/export?format=csv&gid=1077962440",
    "Dealer 25": "https://docs.google.com/spreadsheets/d/1hdfMr_L431efl1fbC09HqKodziY0Jj23xbmly6yz6P4/export?format=csv&gid=1077962440",
}

date_col = "Дата продажи"
model_col = "Model 2 车型"
dealer_col = "Dealer"
vin_col = "VIN"
status_col = "logistics status"

dealer_city_col = "City"
dealer_model_col = "Модель автомобиля"
dealer_contract_date_col = "Дата контракта"
dealer_cancel_date_col = "Дата отмены контракта"
dealer_delivery_date_col = "Дата выдачи автомобиля"
dealer_vin_col = "VIN"

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


def clean_columns(df):
    df = df.copy()
    df.columns = df.columns.astype(str).str.replace("\n", " ").str.strip()
    return df


def normalize_text(value):
    if pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value)).strip().casefold()


def normalize_vin(value):
    if pd.isna(value):
        return ""
    return re.sub(r"[^A-Z0-9]", "", str(value).upper().strip())


@st.cache_data(ttl=300)
def load_main_data():
    df = pd.read_csv(MAIN_SHEET_URL)
    return clean_columns(df)


@st.cache_data(ttl=300)
def load_dealer_data(url):
    df = pd.read_csv(url)
    return clean_columns(df)


@st.cache_data(ttl=300)
def build_dealer_options(dealer_sheets):
    options = {}

    for fallback_name, sheet_url in dealer_sheets.items():
        try:
            dealer_df = load_dealer_data(sheet_url)

            dealer_name = fallback_name
            if dealer_city_col in dealer_df.columns:
                cities = dealer_df[dealer_city_col].dropna().astype(str).str.strip()
                cities = cities[cities != ""]
                if len(cities) > 0:
                    dealer_name = cities.value_counts().index[0]

            if dealer_name in options:
                dealer_name = f"{dealer_name} ({fallback_name})"

            options[dealer_name] = sheet_url

        except Exception:
            options[fallback_name] = sheet_url

    return options


def detect_dealer_name(dealer_df, fallback_name):
    if dealer_city_col in dealer_df.columns:
        cities = dealer_df[dealer_city_col].dropna().astype(str).str.strip()
        cities = cities[cities != ""]
        if len(cities) > 0:
            return cities.value_counts().index[0]
    return fallback_name


def add_issue(issues, level, category, problem, action):
    priority = {"Критично": 3, "Проверить": 2, "Информация": 1, "OK": 0}
    issues.append({
        "level": level,
        "category": category,
        "problem": problem,
        "action": action,
        "priority": priority[level],
    })


def compare_dealer(main_df, dealer_df, selected_dealer_value):
    main = main_df.copy()
    dealer = dealer_df.copy()

    main[date_col] = pd.to_datetime(main[date_col], dayfirst=True, errors="coerce")
    dealer[dealer_delivery_date_col] = pd.to_datetime(dealer[dealer_delivery_date_col], dayfirst=True, errors="coerce")

    main["_vin"] = main[vin_col].map(normalize_vin)
    dealer["_vin"] = dealer[dealer_vin_col].map(normalize_vin)

    main_dealer = main[
        (main[dealer_col].map(normalize_text) == normalize_text(selected_dealer_value)) &
        (main["_vin"] != "")
    ].copy()

    dealer_contracts = dealer[dealer["_vin"] != ""].copy()

    main_dealer = main_dealer.drop_duplicates("_vin", keep="last")
    dealer_contracts = dealer_contracts.drop_duplicates("_vin", keep="last")

    merged = main_dealer.merge(
        dealer_contracts,
        on="_vin",
        how="outer",
        suffixes=("_base", "_dealer"),
        indicator=True,
    )

    rows = []

    for _, row in merged.iterrows():
        vin = row["_vin"]
        source = row["_merge"]

        base_model = row.get(f"{model_col}_base", "")
        dealer_model = row.get(f"{dealer_model_col}_dealer", "")
        base_status = row.get(f"{status_col}_base", "")
        base_status_norm = normalize_text(base_status)

        base_sale_date = row.get(f"{date_col}_base", pd.NaT)
        dealer_delivery_date = row.get(f"{dealer_delivery_date_col}_dealer", pd.NaT)
        dealer_contract_date = row.get(f"{dealer_contract_date_col}_dealer", pd.NaT)
        dealer_cancel_date = row.get(f"{dealer_cancel_date_col}_dealer", pd.NaT)

        issues = []

        if source == "left_only":
            if base_status_norm == "sales":
                add_issue(
                    issues,
                    "Критично",
                    "Продажа",
                    "В общем файле статус Sales, но VIN отсутствует в файле контрактов дилера",
                    "Проверить, почему дилер не отразил контракт/выдачу по проданной машине",
                )

            elif base_status_norm == "stock dlr":
                add_issue(
                    issues,
                    "Информация",
                    "Сток дилера",
                    "VIN есть в общем файле со статусом Stock DLR и отсутствует в контрактах дилера",
                    "Это нормально: машина стоит на стоке у дилера, продажи по ней пока не должно быть",
                )

            elif base_status_norm == "tranzit to dlr":
                add_issue(
                    issues,
                    "Информация",
                    "Транзит",
                    "VIN есть в общем файле со статусом Tranzit to DLR и отсутствует в контрактах дилера",
                    "Это нормально: машина еще в пути к дилеру, продажи по ней пока не должно быть",
                )

            elif base_status_norm == "stock kz":
                add_issue(
                    issues,
                    "Информация",
                    "Сток KZ",
                    "VIN есть в общем файле со статусом Stock KZ и отсутствует в контрактах дилера",
                    "Это нормально: машина еще на складе KZ, у дилера по ней не должно быть продажи",
                )

            elif base_status_norm == "":
                add_issue(
                    issues,
                    "Проверить",
                    "Статус",
                    "VIN есть в общем файле, но отсутствует в контрактах дилера и нет logistics status",
                    "Заполнить или проверить logistics status в общем файле",
                )

            else:
                add_issue(
                    issues,
                    "Проверить",
                    "Статус",
                    f"VIN есть в общем файле со статусом {base_status}, но отсутствует в контрактах дилера",
                    "Проверить, является ли этот статус нормальным для отсутствия контракта",
                )

        elif source == "right_only":
            if not pd.isna(dealer_delivery_date):
                add_issue(
                    issues,
                    "Критично",
                    "VIN",
                    "VIN есть у дилера с датой выдачи, но нет в общем файле по этому дилеру",
                    "Проверить VIN, дилера в общем файле и факт продажи",
                )
            else:
                add_issue(
                    issues,
                    "Проверить",
                    "VIN",
                    "VIN есть в файле дилера, но нет в общем файле по этому дилеру",
                    "Проверить, не ошибся ли дилер в VIN или City",
                )

        if source == "both":
            if normalize_text(base_model) and normalize_text(dealer_model):
                if normalize_text(base_model) != normalize_text(dealer_model):
                    add_issue(
                        issues,
                        "Проверить",
                        "Модель",
                        "Модель в общем файле отличается от модели в файле дилера",
                        "Сверить модель по VIN и исправить название в одном из файлов",
                    )

            if base_status_norm == "sales":
                if pd.isna(dealer_delivery_date):
                    add_issue(
                        issues,
                        "Критично",
                        "Статус",
                        "В общем файле статус Sales, но у дилера нет даты выдачи автомобиля",
                        "Попросить дилера заполнить дату выдачи или проверить статус Sales в общем файле",
                    )
                elif not pd.isna(base_sale_date) and base_sale_date.date() != dealer_delivery_date.date():
                    add_issue(
                        issues,
                        "Проверить",
                        "Дата",
                        "Дата продажи в общем файле отличается от даты выдачи у дилера",
                        "Сверить правильную дату продажи/выдачи и исправить один из файлов",
                    )

            if base_status_norm in ["stock dlr", "tranzit to dlr", "stock kz"] and not pd.isna(dealer_delivery_date):
                add_issue(
                    issues,
                    "Критично",
                    "Статус",
                    f"У дилера есть дата выдачи, но в общем файле статус {base_status}",
                    "Проверить logistics status в общем файле: возможно машину нужно перевести в Sales",
                )

            if base_status_norm == "stock dlr":
                add_issue(
                    issues,
                    "Информация",
                    "Сток",
                    "Машина числится как Stock DLR",
                    "Позже сверить с отдельным файлом актуального стока дилера",
                )

            if base_status_norm == "tranzit to dlr":
                add_issue(
                    issues,
                    "Информация",
                    "Логистика",
                    "Машина в статусе Tranzit to DLR",
                    "Проверить после поступления к дилеру",
                )

            if base_status_norm == "stock kz":
                add_issue(
                    issues,
                    "Информация",
                    "Сток",
                    "Машина в статусе Stock KZ",
                    "У дилера по ней обычно не должно быть выдачи",
                )

        if not issues:
            add_issue(
                issues,
                "OK",
                "OK",
                "Данные совпадают по текущим правилам",
                "Действий не требуется",
            )

        main_issue = sorted(issues, key=lambda x: x["priority"], reverse=True)[0]

        rows.append({
            "Уровень": main_issue["level"],
            "Категория": main_issue["category"],
            "Проблема": main_issue["problem"],
            "Что сделать": main_issue["action"],
            "Все замечания": " | ".join([x["problem"] for x in issues if x["level"] != "OK"]),
            "Дилер": selected_dealer_value,
            "VIN": vin,
            "Dealer в общем файле": row.get(f"{dealer_col}_base", ""),
            "City у дилера": row.get(f"{dealer_city_col}_dealer", ""),
            "logistics status": base_status,
            "Модель в общем файле": base_model,
            "Модель у дилера": dealer_model,
            "Дата продажи": row.get(f"{date_col}_base", ""),
            "Дата выдачи дилера": dealer_delivery_date,
            "Дата контракта": dealer_contract_date,
            "Дата отмены контракта": dealer_cancel_date,
        })

    result_df = pd.DataFrame(rows)
    status_view = main_dealer[[vin_col, dealer_col, model_col, status_col, date_col]].copy()

    return result_df, status_view, main_dealer, dealer_contracts


df = load_main_data()

tab_dashboard, tab_check = st.tabs(["Дашборд", "Проверка"])


with tab_dashboard:
    df_sales = df.copy()

    df_sales[date_col] = pd.to_datetime(df_sales[date_col], dayfirst=True, errors="coerce")
    df_sales = df_sales.dropna(subset=[date_col])
    df_sales["Месяц"] = df_sales[date_col].dt.to_period("M").astype(str)

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
        dealers_list = ["Все"] + sorted(df_sales[dealer_col].dropna().unique().tolist())
        selected_dealer = st.radio("", dealers_list, label_visibility="collapsed")

    today = date.today()
    first_this_month = today.replace(day=1)
    first_last_month = (first_this_month - timedelta(days=1)).replace(day=1)
    last_last_month = first_this_month - timedelta(days=1)
    first_this_year = today.replace(month=1, day=1)

    col_p1, col_p2, col_p3, col_m = st.columns([1, 1, 1, 2])

    with col_p1:
        btn1 = st.button("Этот месяц", use_container_width=True)
    with col_p2:
        btn2 = st.button("Прошлый месяц", use_container_width=True)
    with col_p3:
        btn3 = st.button("Этот год", use_container_width=True)
    with col_m:
        models_list = ["Все модели"] + sorted(df_sales[model_col].dropna().unique().tolist())
        selected_model = st.selectbox("", models_list, label_visibility="collapsed")

    if "period_start" not in st.session_state:
        st.session_state.period_start = first_this_month
        st.session_state.period_end = today

    if btn1:
        st.session_state.period_start = first_this_month
        st.session_state.period_end = today
    if btn2:
        st.session_state.period_start = first_last_month
        st.session_state.period_end = last_last_month
    if btn3:
        st.session_state.period_start = first_this_year
        st.session_state.period_end = today

    period_start = st.session_state.period_start
    period_end = st.session_state.period_end

    mask = (
        (df_sales[date_col].dt.date >= period_start) &
        (df_sales[date_col].dt.date <= period_end)
    )
    dff = df_sales[mask].copy()

    if selected_dealer != "Все":
        dff = dff[dff[dealer_col] == selected_dealer]
    if selected_model != "Все модели":
        dff = dff[dff[model_col] == selected_model]

    today_df = dff[dff[date_col].dt.date == today]

    st.divider()

    k1, k2, k3, k4 = st.columns(4)

    total_sales = len(dff)
    top_model = dff[model_col].value_counts().index[0] if len(dff) > 0 else "—"
    top_model_n = dff[model_col].value_counts().iloc[0] if len(dff) > 0 else 0
    top_dealer = dff[dealer_col].value_counts().index[0] if len(dff) > 0 else "—"
    top_dealer_n = dff[dealer_col].value_counts().iloc[0] if len(dff) > 0 else 0

    k1.metric("Продажи за период", total_sales)
    k2.metric("Топ модель", top_model, f"{top_model_n} шт.")
    k3.metric("Топ дилер", top_dealer, f"{top_dealer_n} шт.")
    k4.metric("Контракты", "—", "данные скоро", delta_color="off")

    st.divider()

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


with tab_check:
    st.subheader("Проверка данных дилеров")

    dealer_options = build_dealer_options(DEALER_SHEETS)

    dealer_choice = st.selectbox(
        "Дилер",
        ["Все дилеры"] + list(dealer_options.keys())
    )

    main_dealer_values = sorted(df[dealer_col].dropna().unique().tolist())

    def run_one_dealer_check(sheet_name, sheet_url):
        dealer_df = load_dealer_data(sheet_url)

        required_main_cols = [dealer_col, model_col, date_col, vin_col, status_col]
        required_dealer_cols = [
            dealer_city_col,
            dealer_model_col,
            dealer_delivery_date_col,
            dealer_vin_col,
        ]

        missing_main = [c for c in required_main_cols if c not in df.columns]
        missing_dealer = [c for c in required_dealer_cols if c not in dealer_df.columns]

        if missing_main or missing_dealer:
            return {
                "sheet_name": sheet_name,
                "dealer_name": sheet_name,
                "error": f"Нет колонок. Общий файл: {missing_main}. Файл дилера: {missing_dealer}",
                "result_df": pd.DataFrame(),
                "status_view": pd.DataFrame(),
                "main_df": pd.DataFrame(),
                "dealer_df": dealer_df,
            }

        detected_name = detect_dealer_name(dealer_df, sheet_name)

        matched_main_name = detected_name
        for value in main_dealer_values:
            if normalize_text(value) == normalize_text(detected_name):
                matched_main_name = value
                break

        result_df, status_view, main_dealer_df, dealer_contracts_df = compare_dealer(
            df,
            dealer_df,
            matched_main_name,
        )

        result_df["Дилер"] = matched_main_name
        status_view["Дилер"] = matched_main_name

        return {
            "sheet_name": sheet_name,
            "dealer_name": matched_main_name,
            "error": None,
            "result_df": result_df,
            "status_view": status_view,
            "main_df": main_dealer_df,
            "dealer_df": dealer_contracts_df,
        }

    selected_items = dealer_options.items()
    if dealer_choice != "Все дилеры":
        selected_items = [(dealer_choice, dealer_options[dealer_choice])]

    checks = []
    with st.spinner("Загружаю и сверяю дилеров..."):
        for sheet_name, sheet_url in selected_items:
            try:
                checks.append(run_one_dealer_check(sheet_name, sheet_url))
            except Exception as exc:
                checks.append({
                    "sheet_name": sheet_name,
                    "dealer_name": sheet_name,
                    "error": str(exc),
                    "result_df": pd.DataFrame(),
                    "status_view": pd.DataFrame(),
                    "main_df": pd.DataFrame(),
                    "dealer_df": pd.DataFrame(),
                })

    load_errors = [x for x in checks if x["error"]]
    valid_checks = [x for x in checks if not x["error"]]

    if load_errors:
        with st.expander("Пропущенные дилеры", expanded=False):
            for item in load_errors:
                st.warning(f"{item['sheet_name']}: файл не прочитан, дилер пропущен")

    if not valid_checks:
        st.stop()

    all_results = pd.concat(
        [x["result_df"] for x in valid_checks if not x["result_df"].empty],
        ignore_index=True
    )

    all_statuses = pd.concat(
        [x["status_view"] for x in valid_checks if not x["status_view"].empty],
        ignore_index=True
    )

    if all_results.empty:
        st.warning("Нет данных для проверки.")
        st.stop()

    critical_count = len(all_results[all_results["Уровень"] == "Критично"])
    check_count = len(all_results[all_results["Уровень"] == "Проверить"])
    info_count = len(all_results[all_results["Уровень"] == "Информация"])
    ok_count = len(all_results[all_results["Уровень"] == "OK"])

    sales_count = len(all_statuses[all_statuses[status_col].map(normalize_text) == "sales"]) if not all_statuses.empty else 0
    stock_dlr_count = len(all_statuses[all_statuses[status_col].map(normalize_text) == "stock dlr"]) if not all_statuses.empty else 0
    transit_count = len(all_statuses[all_statuses[status_col].map(normalize_text) == "tranzit to dlr"]) if not all_statuses.empty else 0
    stock_kz_count = len(all_statuses[all_statuses[status_col].map(normalize_text) == "stock kz"]) if not all_statuses.empty else 0

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Критично", critical_count)
    k2.metric("Проверить", check_count)
    k3.metric("Информация", info_count)
    k4.metric("OK", ok_count)

    k5, k6, k7, k8 = st.columns(4)
    k5.metric("Sales", sales_count)
    k6.metric("Stock DLR", stock_dlr_count)
    k7.metric("Tranzit to DLR", transit_count)
    k8.metric("Stock KZ", stock_kz_count)

    st.divider()

    summary_rows = []
    for item in valid_checks:
        result_df = item["result_df"]
        status_view = item["status_view"]

        summary_rows.append({
            "Дилер": item["dealer_name"],
            "Критично": len(result_df[result_df["Уровень"] == "Критично"]),
            "Проверить": len(result_df[result_df["Уровень"] == "Проверить"]),
            "Информация": len(result_df[result_df["Уровень"] == "Информация"]),
            "OK": len(result_df[result_df["Уровень"] == "OK"]),
            "Всего VIN в проверке": len(result_df),
            "Sales": len(status_view[status_view[status_col].map(normalize_text) == "sales"]) if not status_view.empty else 0,
            "Stock DLR": len(status_view[status_view[status_col].map(normalize_text) == "stock dlr"]) if not status_view.empty else 0,
            "Tranzit to DLR": len(status_view[status_view[status_col].map(normalize_text) == "tranzit to dlr"]) if not status_view.empty else 0,
            "Stock KZ": len(status_view[status_view[status_col].map(normalize_text) == "stock kz"]) if not status_view.empty else 0,
        })

    summary_df = pd.DataFrame(summary_rows).sort_values(["Критично", "Проверить"], ascending=False)

    fig_summary = px.bar(
        summary_df,
        x="Дилер",
        y=["Критично", "Проверить", "Информация", "OK"],
        barmode="group",
        text_auto=True,
        color_discrete_map={
            "Критично": "#B42318",
            "Проверить": "#B54708",
            "Информация": "#175CD3",
            "OK": "#067647",
        },
    )
    fig_summary.update_layout(height=380, margin=dict(t=10, b=10), xaxis_tickangle=-30)
    st.plotly_chart(fig_summary, use_container_width=True)

    critical_df = all_results[all_results["Уровень"] == "Критично"].copy()
    check_df = all_results[all_results["Уровень"] == "Проверить"].copy()
    info_df = all_results[all_results["Уровень"] == "Информация"].copy()
    ok_df = all_results[all_results["Уровень"] == "OK"].copy()

    tab_action, tab_critical, tab_check_rows, tab_info, tab_ok, tab_total, tab_status, tab_raw = st.tabs([
        "Требует действия",
        "Критично",
        "Проверить",
        "Информация",
        "OK",
        "Итог по дилерам",
        "Все статусы",
        "Сырые данные",
    ])

    with tab_action:
        action_df = all_results[all_results["Уровень"].isin(["Критично", "Проверить"])].copy()
        st.dataframe(action_df, use_container_width=True, hide_index=True)

    with tab_critical:
        st.dataframe(critical_df, use_container_width=True, hide_index=True)

    with tab_check_rows:
        st.dataframe(check_df, use_container_width=True, hide_index=True)

    with tab_info:
        st.dataframe(info_df, use_container_width=True, hide_index=True)

    with tab_ok:
        st.dataframe(ok_df, use_container_width=True, hide_index=True)

    with tab_total:
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

    with tab_status:
        st.dataframe(all_statuses, use_container_width=True, hide_index=True)

    with tab_raw:
        for item in valid_checks:
            with st.expander(item["dealer_name"]):
                c1, c2 = st.columns(2)
                with c1:
                    st.caption("Общий файл")
                    st.dataframe(item["main_df"], use_container_width=True, hide_index=True)
                with c2:
                    st.caption("Файл дилера")
                    st.dataframe(item["dealer_df"], use_container_width=True, hide_index=True)

    with st.expander("Все результаты проверки"):
        st.dataframe(all_results, use_container_width=True, hide_index=True)
```
