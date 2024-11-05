import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Читаем файл xlsx
df = pd.read_excel('Карта рынка.xlsx', skiprows=1)

# Преобразуем колонки
df['Объем, млн'] = pd.to_numeric(df['Объем, млн'], errors='coerce')

# Формируем расчетные столбцы
df['spread'] = (df['Спред, пп'] * 100)
df['Yield'] = ((100 - df['Цена, пп']) * 100) / df['Срок  до погашения / оферты, лет']
df['Cupon'] = df['spread'] / df['Цена, пп'] * 100 - df['spread']
df['Cspread'] = round(df['spread'] + df['Cupon'] + df['Yield'])
df['deltaS'] = round(df['Cspread'] - df['spread'])
df['Name_rating_gap'] = df.apply(lambda row: f"{row['Тикер']},{row['Рейтинг']},{row['deltaS']}", axis=1)
df['Размещениеt'] = pd.to_datetime(df['Размещение'], dayfirst=True)
df = df.sort_values(by='Размещениеt', ascending=True)

# Инициализация состояния сессии для хранения индексов
if 'selected_indices' not in st.session_state:
    st.session_state.selected_indices = []

# Создаем Streamlit интерфейс
st.title('Карта рынка флоутеров')

# Фильтры для столбцов
tickers = df['Тикер'].unique()
selected_tickers = st.multiselect('Выберите тикер:', tickers)

ratings = df['Рейтинг'].unique()
selected_ratings = st.multiselect('Выберите рейтинг:', ratings)

# Фильтрация данных
f_df = df[
    (df['Тикер'].isin(selected_tickers) | (len(selected_tickers) == 0)) &
    (df['Рейтинг'].isin(selected_ratings) | (len(selected_ratings) == 0))
]

# Отображение отфильтрованного DataFrame
st.dataframe(f_df)

# Позволяем пользователям выбирать строки для удаления
selected_indices = st.multiselect('Выберите строки для удаления:', f_df.index.tolist(), default=st.session_state.selected_indices)

if st.button('Удалить выбранные строки'):
    if selected_indices:
        # Удаляем выбранные строки из DataFrame
        f_df = f_df.drop(index=selected_indices)
        f_df.reset_index(drop=True, inplace=True)  # Сбрасываем индекс после удаления

        # Обновляем состояние сессии для будущих выборов
        st.session_state.selected_indices = f_df.index.tolist()  # Обновляем список индексов
        st.success("Выбранные строки удалены.")
    else:
        st.warning("Не выбраны строки для удаления.")

# Построение графика
if not f_df.empty:
    plt.figure(figsize=(12, 6))
    plt.scatter(f_df['Размещениеt'], f_df['Cspread'], color='darkred', marker='o', s=80, label='Текущий спред')
    plt.scatter(f_df['Размещениеt'], f_df['spread'], color='tan', marker='o', s=80, label='Спред при размещении')

    for i, row in f_df.iterrows():
        plt.text(row['Размещениеt'], row['spread'] + 4, row['Name_rating_gap'], ha='left', fontsize=10)

    plt.title('Карта рынка', fontsize=18)
    plt.xlabel('Дата размещения', fontsize=16)
    plt.ylabel('Спред к КС', fontsize=16)
    plt.legend()
    plt.grid()
    plt.xticks(rotation=45)

    # Показываем график в Streamlit
    st.pyplot(plt)
else:
    st.write("Нет данных для отображения.")
