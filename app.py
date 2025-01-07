import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Заголовок приложения
st.title("График кривых свопов")

# Функция для получения данных
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

# Отображение данных
if st.button('Загрузить данные'):
    curves_data = get_swap_curves()
    if curves_data is not None:
        # Фильтруем данные по swap_curve
        swap_curve_filter = st.selectbox('Выберите кривую:', options=curves_data['swap_curve'].unique())
        filtered_data = curves_data.query("curveid == @swap_curve_filter")
        
        # Строим график
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(filtered_data['tenor'], filtered_data['swaprate'], color='red')
        ax.set_xlabel('Tenor')
        ax.set_ylabel('Swap Rate')
        ax.set_title(f"Кривая '{swap_curve_filter}'")
        
        # Отображаем график
        st.pyplot(fig)
