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
        
        # Создаем функцию для применения стилей к ячейкам таблицы
        def highlight_change(s):
            color = 'green' if s > 0 else 'red'
            return f'color: {color}'
        
        # Применяем стили к столбцам с изменениями
        styled_df = exchange_rates.style.applymap(highlight_change, subset=['CBRF_USD_LASTCHANGEPRCNT', 'CBRF_EUR_LASTCHANGEPRCNT'])
        
        # Формируем HTML-код для отображения валютных иконок
        usd_icon_html = '<img src="https://www.countryflags.io/us/flat/64.png" alt="USD">'
        eur_icon_html = '<img src="https://www.countryflags.io/eu/flat/64.png" alt="EUR">'
        
        # Добавляем иконки перед значениями курсов
        exchange_rates['CBRF_USD_LAST'] = usd_icon_html + ' ' + exchange_rates['CBRF_USD_LAST'].astype(str)
        exchange_rates['CBRF_EUR_LAST'] = eur_icon_html + ' ' + exchange_rates['CBRF_EUR_LAST'].astype(str)
        
        # Конвертируем DataFrame в HTML и рендерим его
        html_table = styled_df.to_html(escape=False, index=False)
        st.write(html_table, unsafe_allow_html=True)
