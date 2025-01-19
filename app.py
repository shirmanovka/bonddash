import streamlit as st
import requests
import pandas as pd

# Заголовки для запроса
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Функция для скачивания файла и чтения данных
def download_data():
    url = 'https://web.moex.com/moex-web-icdb-api/api/v1/export/listing-applications/xlsx'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        with open('listing_applications.xlsx', 'wb') as f:
            f.write(response.content)
        return pd.read_excel('listing_applications.xlsx')
    else:
        st.error("Ошибка при скачивании данных.")
        return None

# Заголовок приложения
st.title("Скачивание данных о заявках на листинг")

# Кнопка для скачивания данных
if st.button("Скачать данные"):
    df = download_data()
    if df is not None:
        columns_to_keep = [
        'Наименование эмитента',
        'ИНН эмитента',
        'Категория(тип) ценной бумаги',
        'Идентификатор выпуска*',
        'Уровень листинга',
        'Дата получения заявления',
        'Дата раскрытия информации'
    ]
        df = df[columns_to_keep]
        abbreviation = {
       'Общество с ограниченной ответственностью': 'OOO',
       'Публичное акционерное общество': 'ПAO',
       'Акционерное общество': 'AO'
        }

   # Замена полных названий на аббревиатуры
        df['Наименование эмитента'] = df['Наименование эмитента'].replace(abbreviation)
        
        def highlight_rows(row):
            return ['background-color: lightgreen' if row['Идентификатор выпуска*'] == "Не присвоен" else '' for _ in row]

        df = df.tail(5)
        
        styled_df = df.style.apply(highlight_rows, axis=1)
        
        for full_name, abbreviation in abbreviations.items():
            df['Наименование эмитента'] = df['Наименование эмитента'].replace(full_name, abbreviation, regex=True)
        
        styled_df = df.style.apply(highlight_rows, axis=1)    
            # Вывод последних 5 строк DataFrame с примененной стилизацией
        st.dataframe(styled_df.format({'ИНН эмитента': '{:.0f}'}))
    
