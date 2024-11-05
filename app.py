import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Читаем файл xlsx
df = pd.read_excel(('Карта рынка.xlsx'), skiprows=1)

df['Объем, млн'] = pd.to_numeric(df['Объем, млн'], errors='coerce')  # Преобразует в NaN некорректные значения

# Формируем расчетные столбцы
df['spread'] = (df['Спред, пп'] * 100)
df['Yield'] = ((100 - df['Цена, пп']) * 100) / df['Срок  до погашения / оферты, лет']
df['Cupon'] = df['spread'] / df['Цена, пп'] * 100 - df['spread']
df['Cspread'] = round(df['spread'] + df['Cupon'] + df['Yield'])
df['deltaS'] = round(df['Cspread'] - df['spread'])
df['Name_rating_gap'] = df.apply(lambda row: f"{row['Тикер']},{row['Рейтинг']},{row['deltaS']}", axis=1)
df['Размещениеt'] = pd.to_datetime(df['Размещение'], dayfirst=True)
df = df.sort_values(by='Размещениеt', ascending=True)  # Сортируем от малых к большим

# Создаем Streamlit интерфейс
st.title('Карта рынка флоутеров')

# Фильтры для столбцов
tickers = df['Тикер'].unique()
selected_tickers = st.multiselect('Выберите тикер:', tickers)

ratings = df['Рейтинг'].unique()
selected_ratings = st.multiselect('Выберите рейтинг:', ratings)

# Фильтр по диапазону дат
min_date = df['Размещениеt'].min().date()  # Конвертируем в формат date
max_date = df['Размещениеt'].max().date()  # Конвертируем в формат date
selected_date_range = st.date_input("Выберите диапазон дат", [min_date, max_date])

# Конвертируем в datetime, чтобы избежать ошибок с типами
selected_date_range[0] = pd.to_datetime(selected_date_range[0])
selected_date_range[1] = pd.to_datetime(selected_date_range[1])

# Фильтрация данных
f_df = df[(df['Тикер'].isin(selected_tickers) | (len(selected_tickers) == 0)) &
            (df['Рейтинг'].isin(selected_ratings) | (len(selected_ratings) == 0)) &
            (df['Размещениеt'] >= selected_date_range[0]) &
            (df['Размещениеt'] <= selected_date_range[1])]

# Отображение отфильтрованного DataFrame
st.dataframe(f_df)

# Построение графика
if not f_df.empty:
    plt.figure(figsize=(12, 6))

    plt.scatter(f_df['Размещениеt'], f_df['Cspread'], color='darkred', marker='o', s=80, label='Текущий спред')
    plt.scatter(f_df['Размещениеt'], f_df['spread'], color='tan', marker='o', s=80, label='Спред при размещении')

    for i, row in f_df.iterrows():
        plt.text(row['Размещениеt'], row['spread'] + 4, row['Name_rating_gap'], ha='left', fontsize=10)

    for i in range(len(f_df)):
        for j in range(len(f_df)): 
            if f_df['Размещениеt'].iloc[i] == f_df['Размещениеt'].iloc[j]:
                plt.annotate('', xy=(f_df['Размещениеt'].iloc[j], f_df['Cspread'].iloc[j]),
                             xytext=(f_df['Размещениеt'].iloc[i], f_df['spread'].iloc[i]),
                             arrowprops=dict(arrowstyle='->', color='goldenrod', linewidth=2, shrinkA=7, shrinkB=7))

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
