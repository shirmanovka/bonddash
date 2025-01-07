import requests
import pandas as pd
import json

# Заголовок приложения
st.title("Курс рубля, ЦБ РФ")

# Запрос данных о текущих ценах
moex_url_cbfr = 'https://iss.moex.com//iss/statistics/engines/currency/markets/selt/rates.json'

# Получим ответ от сервера и загрузим данные в DataFrame
response = requests.get(moex_url_cbrf)
result = response.json()  # Выгружаем JSON напрямую
col_name_cbrf = result['cbrf']['columns']  # Получаем названия колонок

# Заполняем DataFrame с данными
data_cbrf = pd.DataFrame(result['cbrf']['data'], columns=col_name)

# Проверка длины данных (если необходима)
data_length = len(data_cbrf)  # Получаем количество строк в DataFrame
selected_columns = [
    'CBRF_USD_LAST',
    'CBRF_USD_LASTCHANGEPRCNT',
    'CBRF_USD_TRADEDATE',
    'CBRF_EUR_LAST',
    'CBRF_EUR_LASTCHANGEPRCNT',
    'CBRF_EUR_TRADEDATE'
]
filtered_data = data_cbrf[selected_columns]

# Выводим DataFrame с выбранными столбцами
display(filtered_data)
