import streamlit as st
import requests
import pandas as pd
import plotly.express as px

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

# Автоматический запрос данных
curves_data = get_swap_curves()

if curves_data is not None:
    # Убедитесь, что столбец 'swap_curve' существует
    if 'swap_curve' in curves_data.columns:
        swap_curve_filter = st.selectbox('Выберите кривую:', options=curves_data['swap_curve'].unique())
        filtered_data = curves_data.query(f"swap_curve == '{swap_curve_filter}'")
        
        # Строим график
        fig = px.line(filtered_data, x='tenor', y='swap_rate', title=f"Кривая '{swap_curve_filter}'",
                     labels={'tenor': 'Срок', 'swap_rate': 'Ставка'},
                     template='plotly_dark',
                     color='darkred')
        
        # Отображаем график
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Столбец 'swap_curve' отсутствует в данных.")
else:
    st.warning("Не удалось получить данные.")
