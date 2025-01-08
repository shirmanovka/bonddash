import pandas as pd
import requests
import streamlit as st

def get_data(url):
    response = requests.get(url)
    result = response.json()
    col_names = result['marketdata']['columns']
    data = pd.DataFrame(result['marketdata']['data'], columns=col_names)
    return data

@st.cache_data
def load_rgbi():
    moex_url = 'https://iss.moex.com/iss/engines/stock/markets/index/securities/RGBI.json'
    df = get_data(moex_url)
    return df

@st.cache_data
def load_imoex():
    moex_url = 'https://iss.moex.com/iss/engines/stock/markets/index/securities/IMOEX.json'
    df = get_data(moex_url)
    return df

def color_change(value):
    value_str = str(value)
    if value_str.startswith('-'):
        return f'<span style="color: red">{value_str}</span>'
    else:
        return f'<span style="color: green">{value_str}</span>'

def main():
    st.title("Индексы")
    
    left_column, right_column = st.columns(2)
    
    with left_column:
        st.subheader(f"RGBI: {load_rgbi()['CURRENTVALUE'].values[0]}")
        
        rgbi_df = load_rgbi()
        
        last_change = rgbi_df['LASTCHANGEPRC'].values[0]
        st.markdown(f"Изменение к закрытию: {color_change(last_change)}")
        st.text(f"Дата обновления: {rgbi_df['SYSTIME'].values[0]}")
    
    with right_column:
        st.subheader(f"IMOEX: {load_imoex()['CURRENTVALUE'].values[0]}")
        
        imoex_df = load_imoex()
        
        last_change = imoex_df['LASTCHANGEPRC'].values[0]
        st.markdown(f"Изменение к закрытию: {color_change(last_change)}")
        st.text(f"Дата обновления: {imoex_df['SYSTIME'].values[0]}")
    
    st.button('Обновить данные', key='refresh')

if __name__ == "__main__":
    main()
