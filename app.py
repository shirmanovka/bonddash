import requests
import pandas as pd
import json
import streamlit as st

# Часть_1 формируем колонки для дата фрейма
moex_url = 'https://iss.moex.com/iss/engines/stock/markets/bonds/boards/TQCB/securities.json' 
response = requests.get(moex_url) #получим овтет от сервера 
result = json.loads(response.text)
col_name1 = result['marketdata']['columns']
data_bonds_marketdata = pd.DataFrame(columns = col_name1)

# Часть_2 заполняем дата фрейм
moex_url_marketdata = 'https://iss.moex.com/iss/engines/stock/markets/bonds/boards/TQCB/securities.json' #TQOB ОФЗ
response = requests.get(moex_url_marketdata)
result = json.loads(response.text)
resp_date = result['marketdata']['data']
market_data_bonds = pd.DataFrame(resp_date, columns = col_name1)
a = len(resp_date)

# Создаем интерфейс Streamlit
st.title('Анализ бондов')
# Фильтры в боковой панели
st.sidebar.header('Фильтры')

# Пример фильтров: спросим у пользователя, какой столбец он хочет фильтровать
# Предположим, у нас есть столбец 'NAME' для примера
if 'NAME' in market_data_bonds.columns:
    selected_name = st.sidebar.selectbox('Выберите название:', market_data_bonds['NAME'].unique())
else:
    selected_name = None

# Фильтрация DataFrame
if selected_name is not None:
    filtered_data = market_data_bonds[market_data_bonds['NAME'] == selected_name]
else:
    filtered_data = market_data_bonds

# Отображаем отфильтрованный DataFrame
st.subheader('Фильтрованные данные')
st.dataframe(filtered_data)

# Отображаем отфильтрованный DataFrame
st.dataframe(market_data_bonds)
