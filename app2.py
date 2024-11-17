import requests
import pandas as pd
import json
import streamlit as st

# Получаем данные о бондах с MOEX
moex_url = 'https://iss.moex.com/iss/engines/stock/markets/bonds/boards/TQCB/securities.json' 
response = requests.get(moex_url) 
result = json.loads(response.text)
col_name1 = result['marketdata']['columns']

# Заполняем DataFrame с данными о бондах
resp_date = result['marketdata']['data']
market_data_bonds = pd.DataFrame(resp_date, columns=col_name1)

# Создаем интерфейс Streamlit
st.title('Анализ бондов')

# Фильтры для столбцов
for col in col_name1:
    if col != 'TRADESTATUS':  # Исключаем столбцы, которые не являются фильтрами
        unique_values = market_data_bonds[col].unique()
        selected_values = st.multiselect(f'Выберите значение для {col}:', unique_values, default=unique_values.tolist())
        # Фильтруем данные
        market_data_bonds = market_data_bonds[market_data_bonds[col].isin(selected_values)]

# Отображаем отфильтрованный DataFrame
st.dataframe(market_data_bonds)
