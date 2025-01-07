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

# Блок с данными ставки ЦБ РФ
st.header("Курс рубля, ЦБ РФ")

# Получаем данные о курсах валют
exchange_rates = get_exchange_rates()

if exchange_rates is not None:
    usd_last = exchange_rates['CBRF_USD_LAST'].values[0]
    usd_change = exchange_rates['CBRF_USD_LASTCHANGEPRCNT'].values[0]
    usd_trade_date = pd.to_datetime(exchange_rates['CBRF_USD_TRADEDATE']).dt.date.values[0]
    
    eur_last = exchange_rates['CBRF_EUR_LAST'].values[0]
    eur_change = exchange_rates['CBRF_EUR_LASTCHANGEPRCNT'].values[0]
    eur_trade_date = pd.to_datetime(exchange_rates['CBRF_EUR_TRADEDATE']).dt.date.values[0]
    
    # Выводим данные о долларах
    st.subheader("Доллар США")
    st.write(f"Курс: ${usd_last:.2f}")
    st.write(f"Изменение: {usd_change:.2f}%")
    st.write(f"Дата обновления: {usd_trade_date}")
    
    # Выводим данные о евро
    st.subheader("Евро")
    st.write(f"Курс: €{eur_last:.2f}")
    st.write(f"Изменение: {eur_change:.2f}%")
    st.write(f"Дата обновления: {eur_trade_date}")

# Блок с графиками кривых свопов
st.header("Графики кривых свопов")

# Автоматический запрос данных
curves_data = get_swap_curves()

if curves_data is not None:
    # Убедитесь, что столбец 'swap_curve' существует
    if 'swap_curve' in curves_data.columns:
        swap_curve_filter = st.selectbox('Выберите кривую:', options=curves_data['swap_curve'].unique())
        filtered_data = curves_data.query(f"swap_curve == '{swap_curve_filter}'")
        
        # Получение даты выгрузки
        trade_date_str = filtered_data['tradedate'].values[0]
        trade_date = datetime.strptime(trade_date_str, '%Y-%m-%d').strftime('%d.%m.%Y')  # Преобразуем формат даты
        
        # Выводим дату выгрузки
        st.write(f"Дата выгрузки: {trade_date}")
        
        # Строим график
        fig = px.line(filtered_data, x='tenor', y='swap_rate', title=f"Кривая '{swap_curve_filter}'",
                     labels={'tenor': 'Срок', 'swap_rate': 'Ставка'},
                     template='plotly_dark')
        
        # Отображаем график
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Столбец 'swap_curve' отсутствует в данных.")
else:
    st.warning("Не удалось получить данные.")
