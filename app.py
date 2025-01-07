import streamlit as st
import requests
import pandas as pd
import json

# Заголовок приложения
st.title("Курс рубля, ЦБ РФ")

# Функция для получения данных
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

# Отображение данных
if st.button('Обновить курс'):
    exchange_rates = get_exchange_rates()
    if exchange_rates is not None:
        st.write(exchange_rates)
