import pandas as pd
import requests
import streamlit as st
import plotly.express as px
from datetime import datetime


def get_data(url):
    response = requests.get(url)
    result = response.json()
    col_names = result['marketdata']['columns']
    data = pd.DataFrame(result['marketdata']['data'], columns=col_names)
    return data


def load_rgbi():
    moex_url = 'https://iss.moex.com/iss/engines/stock/markets/index/securities/RGBI.json'
    df = get_data(moex_url)
    return df


def load_imoex():
    moex_url = 'https://iss.moex.com/iss/engines/stock/markets/index/securities/IMOEX.json'
    df = get_data(moex_url)
    return df


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


def main():
    st.title("Финансовые инструменты")

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
    
    if st.button('Обновить данные', key='refresh'):
        pass

    # Курс рубля, ЦБ РФ
    st.header("Курс рубля, ЦБ РФ")

    # Получаем данные о курсах валют
    exchange_rates = get_exchange_rates()

    if exchange_rates is not None:
        usd_last = exchange_rates['CBRF_USD_LAST'].values[0]
        usd_change = exchange_rates['CBRF_USD_LASTCHANGEPRCNT'].values[0]
        usd_trade_date = pd.to_datetime(exchange_rates['CBRF_USD_TRADEDATE'].values[0], format='%Y%m%d')
        eur_last = exchange_rates['CBRF_EUR_LAST'].values[0]
        eur_change = exchange_rates['CBRF_EUR_LASTCHANGEPRCNT'].values[0]
        eur_trade_date = pd.to_datetime(exchange_rates['CBRF_EUR_TRADEDATE'].values[0], format='%Y%m%d')

        st.write(f"USD: {usd_last}, Изменение: {usd_change:.2f}%, Дата: {usd_trade_date.strftime('%d-%m-%Y')}")
        st.write(f"EUR: {eur_last}, Изменение: {eur_change:.2f}%, Дата: {eur_trade_date.strftime('%d-%m-%Y')}")

    # Кривые свопов
    st.header("Кривые свопов")

    swap_curves = get_swap_curves()

    if swap_curves is not None:
        st.dataframe(swap_curves)


if __name__ == "__main__":
    main()
