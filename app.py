import streamlit as st
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

# Заголовок приложения
st.title("Корпоративный календарь")

# Запускаем браузер Safari
driver = webdriver.Safari()

# Переход к нужной странице
driver.get("https://www.bondresearch.ru/dashboard/corporate_calendar.html")

# Ждем загрузки страницы
time.sleep(5)

# Получаем HTML-код страницы
html = driver.page_source

# Закрываем браузер
driver.quit()

# Парсим HTML-код
soup = BeautifulSoup(html, 'html.parser')

# Находим таблицу с корпоративным календарем
table = soup.find('table')

# Извлекаем заголовки столбцов
headers = [th.text.strip() for th in table.find_all('th')]

# Извлекаем строки данных
data = []
for row in table.find_all('tr')[1:]:  # Пропускаем заголовки
    cols = row.find_all('td')
    cols = [elem.text.strip() for elem in cols]  # Убираем лишние пробелы
    data.append(cols)

# Создаем DataFrame
df = pd.DataFrame(data, columns=headers)

# Отображаем DataFrame в Streamlit
st.dataframe(df)
