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

# Функция для получения данных кривых свопов
def get_swap_curves():
    moex_url = 'https://iss.moex.com//iss/sdfi/curves/securities.json'
    
    try:
        response = requests.get(moex_url)
        if response.status_code == 200:
            result = response.json()
            col_names = result['curves']['columns']
            df = pd.DataFrame(result['curves']['data'], columns=col_names)
            return df
        else:
            st.error(f'Ошибка при получении данных. Код состояния: {response.status_code}')
    except Exception as e:
        st.error(f'Произошла ошибка при запросе данных: {e}')

# Функция для получения данных RGBI
def get_rgbi_data():
    moex_url = 'https://iss.moex.com/iss/engines/stock/markets/index/securities/RGBI.json'
    
    response = requests.get(moex_url)
    result = response.json()
    
    col_name = result['marketdata']['columns']
    data_rgbi = pd.DataFrame(result['marketdata']['data'], columns=col_name)
    
    return data_rgbi

# Блок с данными ставки ЦБ РФ
st.header("Курс рубля, ЦБ РФ")

# Получаем данные о курсах валют
exchange_rates = get_exchange_rates()

rgbi_data = get_rgbi_data()

if exchange_rates is not None:
    usd_last = exchange_rates['CBRF_USD_LAST'].values[0]
    usd_change = exchange_rates['CBRF_USD_LASTCHANGEPRCNT'].values[0]
    usd_trade_date = pd.to_datetime(exchange_rates['CBRF_USD_TRADEDATE']).dt.date.values[0]
    
    eur_last = exchange_rates['CBRF_EUR_LAST'].values[0]
    eur_change = exchange_rates['CBRF_EUR_LASTCHANGEPRCNT'].values[0]
    eur_trade_date = pd.to_datetime(exchange_rates['CBRF_EUR_TRADEDATE']).dt.date.values[rgbix]

    # Создаем три колонки
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Доллар США")
        st.write(f"Курс: ${usd_last:.2f}")
        change_color = "green" if usd_change > 0 else "red"
        st.markdown(f"<p style='color:{change_color}; font-size:20px;'>Изменение: {usd_change:.2f}%</p>", unsafe_allow_html=True)
        st.write(f"Дата обновления: {usd_trade_date}")
    
    with col2:
        st.subheader("Евро")
        st.write(f"Курс: €{eur_last:.2f}")
        change_color = "green" if eur_change > 0 else "red"
        st.markdown(f"<p style='color:{change_color}; font-size:20px;'>Изменение: {eur_change:.2f}%</p>", unsafe_allow_html=True)
        st.write(f"Дата обновления: {eur_trade_date}")

    with col3:
        st.subheader("RGBI")
        rgb_last = rgbi_data['CURRENTVALUE'].values[0]
        rgb_change = rgbi_data['LASTCHANGE'].values[0]
        rgb_trade_date = rgbi_data['TRADEDATE'].values[0]
        change_color = "green" if rgb_change > 0 else "red"
        st.markdown(f"<p style='color:{change_color}; font-size:20px;'>Изменение: {rgb_change:.2f}%</p>", unsafe_allow_html=True)
        st.write(f"Дата обновления: {rgb_trade_date}")

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
        trade_date = datetime.strptime(trade_date_str, '%Y-%m-%d').strftime('%d.%m.%Y') 
