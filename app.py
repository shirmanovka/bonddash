import streamlit as st
import requests
import pandas as pd
import smtplib
import schedule
import time
from email.mime.text import MIMEText
from threading import Thread
from datetime import datetime, timedelta

# Установка параметров отображения для pandas
pd.set_option('display.float_format', '{:.0f}'.format)

# Заголовки для запроса
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Глобальная переменная для хранения предыдущего состояния таблицы
last_df = pd.DataFrame()

# Функция для отправки email
def send_email(new_row):
    msg = MIMEText(new_row.to_string())
    msg['Subject'] = 'Новая облигация с идентификатором "Не присвоен"'
    msg['From'] = 'k9819722707@gmail.com'
    msg['To'] = 'Shirman7@bk.ru'

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('k9819722707gmail.com', '1qaz2wsx#EDC')  # Замените на свои учетные данные
        server.send_message(msg)

# Функция для скачивания файла и чтения данных
def download_data():
    global last_df
    url = 'https://web.moex.com/moex-web-icdb-api/api/v1/export/listing-applications/xlsx'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        with open('listing_applications.xlsx', 'wb') as f:
            f.write(response.content)
        df = pd.read_excel('listing_applications.xlsx')
        return df
    else:
        st.error("Ошибка при скачивании данных.")
        return None

# Функция для обновления данных
def update_data():
    global last_df
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

        # Преобразование столбца даты в datetime формат
        df['Дата получения заявления'] = pd.to_datetime(df['Дата получения заявления'], errors='coerce')

        # Вычисление пределов дат
        today = datetime.now()
        five_days_ago = today - timedelta(days=5)

        # Фильтрация новых строк с "Не присвоен" и не старше 5 дней
        new_rows = df[(df['Идентификатор выпуска*'] == "Не присвоен") &
                       (~df.isin(last_df)).any(axis=1) &
                       (df['Дата получения заявления'] >= five_days_ago)]
        
        if not new_rows.empty:
            for idx in new_rows.index:
                send_email(new_rows.loc[idx])

        # Обновить last_df для следующего сравнения
        last_df = df

# Запланировать обновление данных
def schedule_updates():
    schedule.every().day.at("08:00").do(update_data)
    schedule.every().day.at("12:00").do(update_data)
    schedule.every().day.at("16:00").do(update_data)

    while True:
        schedule.run_pending()
        time.sleep(1)

# Запуск планировщика в отдельном потоке
thread = Thread(target=schedule_updates)
thread.start()

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
        st.write(df.tail(5))  # Вывод последних 5 строк DataFrame
