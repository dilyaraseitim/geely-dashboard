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

SKIP_STATUSES = ["stock dlr", "tranzit to dlr", "stock kz"]

MODEL_EQUIVALENTS = {
    ("coolray new", "coolray"),
    ("monjaro new", "monjaro"),
    ("emgrand", "emgrand"),
    ("atlas", "atlas 4wd"),
    ("atlas", "atlas 2wd"),
    ("okavango", "okavango"),
    ("coolray", "coolray"),
    ("monjaro", "monjaro"),
    ("atlas skd", "atlas 4wd"),
    ("tugella", "tugella"),
    ("azkarra", "azkarra"),
}

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


def get_value(row, col, suffix=None):
    if suffix:
        suffixed_col = f"{col}_{suffix}"
        if suffixed_col in row.index:
            return row.get(suffixed_col)
    if col in row.index:
        return row.get(col)
    return ""


def models_match(base_model, dealer_model):
    base = normalize_text(base_model)
    dealer = normalize_text(dealer_model)
    return base == dealer or (base, dealer) in MODEL_EQUIVALENTS


def dates_match_for_rules(base_date, dealer_date):
    if pd.isna(base_date) or pd.isna(dealer_date):
        return False

    base_date = pd.to_datetime(base_date, errors="coerce")
    dealer_date = pd.to_datetime(dealer_date, errors="coerce")

    if pd.isna(base_date) or pd.isna(dealer_date):
        return False

    if base_date.date() == dealer_date.date():
        return True

    if base_date.year == 2025 and dealer_date.year == 2025:
        return base_date.month == dealer_date.month

    return False


def canonical_vin(value, vin_map):
    vin = normalize_vin(value)
    return vin_map.get(vin, vin)


def add_issue(issues, level, category, problem, action):
    priority = {"Критично": 3, "Проверить": 2, "OK": 0}
    issues.append({
        "level": level,
        "category": category,
        "problem": problem,
        "action": action,
        "priority": priority[level],
    })


@st.cache_data(ttl=300)
def load_main_data():
    df = pd.read_csv(MAIN_SHEET_URL)
    return clean_columns(df)


@st.cache_data(ttl=300)
def load_dealer_data(url):
    df = pd.read_csv(url)
    return clean_columns(df)


def build_vin_map(vin_file):
    if vin_file is None:
        return {}, set()

    vin_df = pd.read_excel(vin_file)
    vin_df = clean_columns(vin_df)

    cols = vin_df.columns.tolist()
    if len(cols) < 2:
        return {}, set()

    kaz_col = None
    china_col = None

    for col in cols:
        name = normalize_text(col)
        if "каз" in name or "kz" in name or "казахстан" in name:
            kaz_col = col
        if "кит" in name or "china" in name or "chinese" in name or "cn" in name:
            china_col = col

    if kaz_col is None:
        kaz_col = cols[0]
    if china_col is None:
        china_col = cols[1]

    vin_map = {}
    china_vins = set()

    for _, row in vin_df.iterrows():
        kaz_vin = normalize_vin(row.get(kaz_col))
        china_vin = normalize_vin(row.get(china_col))

        if kaz_vin:
            vin_map[kaz_vin] = kaz_vin
        if china_vin and kaz_vin:
            vin_map[china_vin] = kaz_vin
            china_vins.add(china_vin)

    return vin_map, china_vins


@st.cache_data(ttl=300)
def build_dealer_options(dealer_sheets):
    options = {}

    for fallback_name, sheet_url in dealer_sheets.items():
        try:
            dealer_df = load_dealer_data(sheet_url)
            dealer_name = detect_dealer_name(dealer_df, fallback_name)

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


def match_main_dealer_name(detected_name, main_dealer_values):
    for value in main_dealer_values:
        if normalize_text(value) == normalize_text(detected_name):
            return value
    return detected_name


def prepare_loaded_dealer(sheet_name, sheet_url, main_dealer_values):
    dealer_df = load_dealer_data(sheet_url)
    detected_name = detect_dealer_name(dealer_df, sheet_name)
    matched_main_name = match_main_dealer_name(detected_name, main_dealer_values)

    return {
        "sheet_name": sheet_name,
        "dealer_name": matched_main_name,
        "dealer_df": dealer_df,
        "error": None,
    }


def build_dealer_vin_locations(loaded_dealers, vin_map, china_vins):
    locations = {}

    for item in loaded_dealers:
        dealer_df = item["dealer_df"].copy()
        dealer_name = item["dealer_name"]

        if dealer_vin_col not in dealer_df.columns:
            continue

        dealer_df[dealer_delivery_date_col] = pd.to_datetime(
            dealer_df.get(dealer_delivery_date_col),
            dayfirst=True,
            errors="coerce",
        )

        for _, row in dealer_df.iterrows():
            original_vin = normalize_vin(row.get(dealer_vin_col))
            canonical = canonical_vin(original_vin, vin_map)

            if not canonical:
                continue

            delivery_date = row.get(dealer_delivery_date_col)
            if pd.isna(delivery_date):
                continue

            locations.setdefault(canonical, []).append({
                "dealer": dealer_name,
                "original_vin": original_vin,
                "used_china_vin": original_vin in china_vins,
                "delivery_date": delivery_date,
            })

    return locations


def compare_dealer(main_df, dealer_df, selected_dealer_value, vin_map, china_vins, dealer_vin_locations):
    main = main_df.copy()
    dealer = dealer_df.copy()

    main[date_col] = pd.to_datetime(main[date_col], dayfirst=True, errors="coerce")
    dealer[dealer_delivery_date_col] = pd.to_datetime(dealer[dealer_delivery_date_col], dayfirst=True, errors="coerce")

    main["_original_vin"] = main[vin_col].map(normalize_vin)
    dealer["_original_vin"] = dealer[dealer_vin_col].map(normalize_vin)

    main["_vin"] = main["_original_vin"].apply(lambda x: canonical_vin(x, vin_map))
    dealer["_vin"] = dealer["_original_vin"].apply(lambda x: canonical_vin(x, vin_map))

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

        base_model = get_value(row, model_col, "base")
        dealer_model = get_value(row, dealer_model_col, "dealer")

        base_status = get_value(row, status_col, "base")
        base_status_norm = normalize_text(base_status)

        base_sale_date = get_value(row, date_col, "base")
        dealer_delivery_date = get_value(row, dealer_delivery_date_col, "dealer")
        dealer_contract_date = get_value(row, dealer_contract_date_col, "dealer")
        dealer_cancel_date = get_value(row, dealer_cancel_date_col, "dealer")
        dealer_original_vin = get_value(row, "_original_vin", "dealer")

        issues = []

        if dealer_original_vin in china_vins:
            add_issue(
                issues,
                "Проверить",
                "VIN",
                "Дилер указал китайский VIN вместо казахстанского VIN",
                "Попросить дилера заменить VIN в отчете на казахстанский",
            )

        if source == "left_only":
            if base_status_norm == "sales":
                other_dealers = [
                    x for x in dealer_vin_locations.get(vin, [])
                    if normalize_text(x["dealer"]) != normalize_text(selected_dealer_value)
                ]

                if other_dealers:
                    names = sorted(set(x["dealer"] for x in other_dealers))
                    add_issue(
                        issues,
                        "Критично",
                        "Дилер",
                        f"В общем файле продажа указана за {selected_dealer_value}, но в отчете продажу показывает: {', '.join(names)}",
                        "Проверить, какой дилер фактически продал автомобиль, и исправить Dealer в общем файле",
                    )
                else:
                    add_issue(
                        issues,
                        "Критично",
                        "Продажа",
                        "В общем файле статус Sales, но VIN отсутствует в файле контрактов дилера",
                        "Проверить, почему дилер не отразил контракт/выдачу по проданной машине",
                    )

            elif base_status_norm in SKIP_STATUSES:
                continue

            elif base_status_norm == "":
                add_issue(
                    issues,
                    "Проверить",
                    "Статус",
                    "VIN есть в общем файле, но не заполнен или не прочитан logistics status",
                    "Проверить точное название и значение столбца logistics status в общем файле",
                )
            else:
                add_issue(
                    issues,
                    "Проверить",
                    "Статус",
                    f"VIN есть в общем файле со статусом {base_status}, но нет в контрактах дилера",
                    "Проверить, нужно ли учитывать этот статус в правилах",
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
            if base_status_norm in SKIP_STATUSES and pd.isna(dealer_delivery_date):
                continue

            if base_status_norm in SKIP_STATUSES and not pd.isna(dealer_delivery_date):
                add_issue(
                    issues,
                    "Критично",
                    "Статус",
                    f"У дилера есть дата выдачи, но в общем файле статус {base_status}",
                    "Проверить logistics status: если машина выдана, в общем файле должен быть Sales",
                )

            if base_status_norm == "sales":
                if normalize_text(base_model) and normalize_text(dealer_model):
                    if not models_match(base_model, dealer_model):
                        add_issue(
                            issues,
                            "Проверить",
                            "Модель",
                            "Модель в общем файле отличается от модели в файле дилера",
                            "Сверить модель по VIN и исправить название в одном из файлов",
                        )

                if pd.isna(dealer_delivery_date):
                    add_issue(
                        issues,
                        "Критично",
                        "Статус",
                        "В общем файле статус Sales, но у дилера нет даты выдачи автомобиля",
                        "Попросить дилера заполнить дату выдачи или проверить статус Sales в общем файле",
                    )
                elif not dates_match_for_rules(base_sale_date, dealer_delivery_date):
                    add_issue(
                        issues,
                        "Проверить",
                        "Дата",
                        "Дата продажи в общем файле отличается от даты выдачи у дилера",
                        "За 2025 год допускается совпадение месяца, за 2026 год дата должна совпадать точно",
                    )

            if base_status_norm not in ["sales"] + SKIP_STATUSES:
                add_issue(
                    issues,
                    "Проверить",
                    "Статус",
                    f"VIN найден в обоих файлах, но logistics status = {base_status}",
                    "Проверить, нужно ли добавить этот статус в правила проверки",
                )

        if not issues:
            add_issue(
                issues,
                "OK",
                "OK",
                "Продажа совпадает по текущим правилам",
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
            "VIN для сверки": vin,
            "VIN дилера исходный": dealer_original_vin,
            "Dealer в общем файле": get_value(row, dealer_col, "base"),
            "City у дилера": get_value(row, dealer_city_col, "dealer"),
            "logistics status": base_status,
            "Модель в общем файле": base_model,
            "Модель у дилера": dealer_model,
            "Дата продажи": base_sale_date,
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
    st.subheader("Проверка продаж дилеров")

    vin_mapping_file = st.file_uploader(
        "Файл соответствия казахстанского и китайского VIN",
        type=["xlsx"],
    )

    vin_map, china_vins = build_vin_map(vin_mapping_file)

    dealer_options = build_dealer_options(DEALER_SHEETS)

    dealer_choice = st.selectbox(
        "Дилер",
        ["Все дилеры"] + list(dealer_options.keys())
    )

    main_dealer_values = sorted(df[dealer_col].dropna().unique().tolist())

    all_loaded_dealers = []
    load_errors = []

    with st.spinner("Загружаю дилерские файлы..."):
        for sheet_name, sheet_url in dealer_options.items():
            try:
                all_loaded_dealers.append(prepare_loaded_dealer(sheet_name, sheet_url, main_dealer_values))
            except Exception as exc:
                load_errors.append({
                    "sheet_name": sheet_name,
                    "error": str(exc),
                })

    dealer_vin_locations = build_dealer_vin_locations(all_loaded_dealers, vin_map, china_vins)

    if dealer_choice == "Все дилеры":
        selected_loaded_dealers = all_loaded_dealers
    else:
        selected_loaded_dealers = [
            item for item in all_loaded_dealers
            if normalize_text(item["sheet_name"]) == normalize_text(dealer_choice)
            or normalize_text(item["dealer_name"]) == normalize_text(dealer_choice)
        ]

    checks = []

    with st.spinner("Сверяю продажи..."):
        for item in selected_loaded_dealers:
            try:
                result_df, status_view, main_dealer_df, dealer_contracts_df = compare_dealer(
                    df,
                    item["dealer_df"],
                    item["dealer_name"],
                    vin_map,
                    china_vins,
                    dealer_vin_locations,
                )

                if not result_df.empty:
                    result_df["Дилер"] = item["dealer_name"]

                if not status_view.empty:
                    status_view["Дилер"] = item["dealer_name"]

                checks.append({
                    "sheet_name": item["sheet_name"],
                    "dealer_name": item["dealer_name"],
                    "error": None,
                    "result_df": result_df,
                    "status_view": status_view,
                    "main_df": main_dealer_df,
                    "dealer_df": dealer_contracts_df,
                })

            except Exception as exc:
                checks.append({
                    "sheet_name": item["sheet_name"],
                    "dealer_name": item["dealer_name"],
                    "error": str(exc),
                    "result_df": pd.DataFrame(),
                    "status_view": pd.DataFrame(),
                    "main_df": pd.DataFrame(),
                    "dealer_df": pd.DataFrame(),
                })

    skipped_checks = [x for x in checks if x["error"]]
    valid_checks = [x for x in checks if not x["error"]]

    if load_errors or skipped_checks:
        with st.expander("Пропущенные дилеры", expanded=False):
            for item in load_errors:
                st.warning(f"{item['sheet_name']}: файл не прочитан, дилер пропущен")
            for item in skipped_checks:
                st.warning(f"{item['sheet_name']}: ошибка при сверке, дилер пропущен")

    if not valid_checks:
        st.stop()

    result_frames = [x["result_df"] for x in valid_checks if not x["result_df"].empty]
    status_frames = [x["status_view"] for x in valid_checks if not x["status_view"].empty]

    all_results = pd.concat(result_frames, ignore_index=True) if result_frames else pd.DataFrame()
    all_statuses = pd.concat(status_frames, ignore_index=True) if status_frames else pd.DataFrame()

    if all_results.empty:
        st.success("По выбранным дилерам нет ошибок продаж. Stock DLR / Tranzit to DLR / Stock KZ скрыты из проверки.")
        st.stop()

    critical_count = len(all_results[all_results["Уровень"] == "Критично"])
    check_count = len(all_results[all_results["Уровень"] == "Проверить"])
    ok_count = len(all_results[all_results["Уровень"] == "OK"])

    sales_count = len(all_statuses[all_statuses[status_col].map(normalize_text) == "sales"]) if not all_statuses.empty else 0
    stock_dlr_count = len(all_statuses[all_statuses[status_col].map(normalize_text) == "stock dlr"]) if not all_statuses.empty else 0
    transit_count = len(all_statuses[all_statuses[status_col].map(normalize_text) == "tranzit to dlr"]) if not all_statuses.empty else 0
    stock_kz_count = len(all_statuses[all_statuses[status_col].map(normalize_text) == "stock kz"]) if not all_statuses.empty else 0

    k1, k2, k3 = st.columns(3)
    k1.metric("Критично", critical_count)
    k2.metric("Проверить", check_count)
    k3.metric("OK по Sales", ok_count)

    k4, k5, k6, k7 = st.columns(4)
    k4.metric("Sales в общем файле", sales_count)
    k5.metric("Stock DLR скрыто", stock_dlr_count)
    k6.metric("Tranzit to DLR скрыто", transit_count)
    k7.metric("Stock KZ скрыто", stock_kz_count)

    st.divider()

    summary_rows = []

    for item in valid_checks:
        result_df = item["result_df"]
        status_view = item["status_view"]

        summary_rows.append({
            "Дилер": item["dealer_name"],
            "Критично": len(result_df[result_df["Уровень"] == "Критично"]) if not result_df.empty else 0,
            "Проверить": len(result_df[result_df["Уровень"] == "Проверить"]) if not result_df.empty else 0,
            "OK по Sales": len(result_df[result_df["Уровень"] == "OK"]) if not result_df.empty else 0,
            "Всего строк в проверке": len(result_df),
            "Sales": len(status_view[status_view[status_col].map(normalize_text) == "sales"]) if not status_view.empty else 0,
            "Stock DLR скрыто": len(status_view[status_view[status_col].map(normalize_text) == "stock dlr"]) if not status_view.empty else 0,
            "Tranzit to DLR скрыто": len(status_view[status_view[status_col].map(normalize_text) == "tranzit to dlr"]) if not status_view.empty else 0,
            "Stock KZ скрыто": len(status_view[status_view[status_col].map(normalize_text) == "stock kz"]) if not status_view.empty else 0,
        })

    summary_df = pd.DataFrame(summary_rows).sort_values(["Критично", "Проверить"], ascending=False)

    fig_summary = px.bar(
        summary_df,
        x="Дилер",
        y=["Критично", "Проверить", "OK по Sales"],
        barmode="group",
        text_auto=True,
        color_discrete_map={
            "Критично": "#B42318",
            "Проверить": "#B54708",
            "OK по Sales": "#067647",
        },
    )
    fig_summary.update_layout(height=380, margin=dict(t=10, b=10), xaxis_tickangle=-30)
    st.plotly_chart(fig_summary, use_container_width=True)

    critical_df = all_results[all_results["Уровень"] == "Критично"].copy()
    check_df = all_results[all_results["Уровень"] == "Проверить"].copy()
    ok_df = all_results[all_results["Уровень"] == "OK"].copy()

    tab_action, tab_critical, tab_check_rows, tab_ok, tab_total, tab_status, tab_raw = st.tabs([
        "Требует действия",
        "Критично",
        "Проверить",
        "OK по Sales",
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

    with tab_ok:
        st.dataframe(ok_df, use_container_width=True, hide_index=True)

    with tab_total:
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

    with tab_status:
        st.caption("Справка по статусам. Stock DLR / Tranzit to DLR / Stock KZ скрыты из проверки контрактов.")
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
