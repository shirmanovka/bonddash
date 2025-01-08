import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime


# Заголовок приложения
st.title("Финансовые инструменты")


# Функция для получения данных ставки ЦБ РФ
def get_exchange_rates():
    moex_url_cbrf = 'https://iss.moex.com//iss/statistics/engines/currency/markets/selt/rates.json'
    
    try:
        response = requests.get(moex_url_cbrf)
        if response.status_code == 200:
            result = response.json()
            col_names = result['cbrf']['columns']
            df = pd.DataFrame(result['cbrf']['data'], columns=col_names)
            
            selected_columns = [
                'CBRF_USD_LAST',
                'CBRF_USD_LASTCHANGEPRCNT',
                'CBRF_USD_TRADEDATE',
                'CBRF_EUR_LAST',
                'CBRF_EUR_LASTCHANGEPRCNT',
                'CBRF_EUR_TRADEDATE'
            ]
            filtered_df = df[selected_columns]
            return filtered_df
        else:
            st.error(f'Ошибка при получении данных. Код состояния: {response.status_code}')
    except Exception as e:
        st.error(f'Произошла ошибка при запросе данных: {e}')


# Блок с данными ставки ЦБ РФ
st.header("Курс рубля, ЦБ РФ")

# Получаем данные о курсах валют
exchange_rates = get_exchange_rates()

if exchange_rates is not None:
    usd_last = exchange_rates['CBRF_USD_LAST'].values[0]
    usd_change = float(exchange_rates['CBRF_USD_LASTCHANGEPRCNT'].values[0]
    usd_trade_date = pd.to_datetime(exchange_rates['CBRF_USD_TRADEDATE']).dt.date.values[0]
    
    eur_last = exchange_rates['CBRF_EUR_LAST'].values[0]
    eur_change = float(exchange_rates['CBRF_EUR_LASTCHANGEPRCNT'].values[0]
    eur_trade_date = pd.to_datetime(exchange_rates['CBRF_EUR_TRADEDATE']).dt.date.values[0]
    
    # Размещаем курсы валют в колонках
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"USD: {usd_last}")
        change_color = "green" if usd_change >= 0 else "red"
        st.markdown(f"Изменение к закрытию: <span style='color:{change_color}; font-weight:bold; font-size:16px;'>{usd_change:.2f}%</span>", unsafe_allow_html=True)
        st.text(f"Дата обновления: {usd_trade_date}")
    
    with col2:
        st.subheader(f"EUR: {eur_last}")
        change_color = "green" if eur_change >= 0 else "red"
        st.markdown(f"Изменение к закрытию: <span style='color:{change_color}; font-weight:bold; font-size:16px;'>{eur_change:.2f}%</span>", unsafe_allow_html=True)
        st.text(f"Дата обновления: {eur_trade_date}")

# Индексы RGBI и IMOEX
st.header("Индексы")
left_column, right_column = st.columns(2)

with left_column:
    st.subheader(f"RGBI: {load_rgbi()['CURRENTVALUE'].values[0]}")
    
    rgbi_df = load_rgbi()
    
    last_change = float(rgbi_df['LASTCHANGEPRC'].values[0])
    change_color = "green" if last_change >= 0 else "red"
    st.markdown(f"Изменение к закрытию: <span style='color:{change_color}; font-weight:bold; font-size:16px;'>{last_change:.2f}%</span>", unsafe_allow_html=True)
    st.text(f"Дата обновления: {rgbi_df['SYSTIME'].values[0]}")

with right_column:
    st.subheader(f"IMOEX: {load_imoex()['CURRENTVALUE'].values[0]}")
    
    imoex_df = load_imoex()
    
    last_change = float(imoex_df['LASTCHANGEPRC'].values[0])
    change_color = "green" if last_change >= 0 else "red"
    st.markdown(f"Изменение к закрытию: <span style='color:{change_color}; font-weight:bold; font-size:16px;'>{last_change:.2f}%</span>", unsafe_allow_html=True)
    st.text(f"Дата обновления: {imoex_df['SYSTIME'].values[0]}")

# Блок с графиками кривых свопов
st.header("Графики кривых свопов")

# Автоматический запрос данных
curves_data = get_swap_curves()

if curves_data is not None:
    # Убедимся, что столбец 'swap_curve' существует
    if 'swap_curve' in curves_data.columns:
        swap_curve_filter = st.selectbox('Выберите кривую:', options=curves_data['swap_curve'].unique())
        filtered_data = curves_data.query(f"swap_curve == '{swap_curve_filter}'")
        
        # Получение даты выгрузки
        trade_date_str = filtered_data['tradedate'].values[0]
        trade_date = datetime.strptime(trade_date_str, '%Y-%m-%d').strftime('%d.%m.%Y')  # Преобразуем формат даты
        
        # Выводим дату выгрузки
        st.write(f"Дата выгрузки: {trade_date}")
        
        # Строим график
        fig = px.line(filtered_data, x='tenor', y='swap_rate', title=f'Кривая свопа "{swap_curve_filter}"')
        st.plotly_chart(fig, use_container_width=True)

if st.button('Обновить данные', key='refresh'):
    st.script_runner.rerun()
