import pandas as pd
import requests
import streamlit as st

def get_data(url):
    response = requests.get(url)
    result = response.json()
    col_names = result['marketdata']['columns']
    data = pd.DataFrame(result['marketdata']['data'], columns=col_names)
    return data

def load_rgbi():
    moex_url = 'https://iss.moex.com/iss/engines/stock/markets/index/securities/RGBI.json'
    df = get_data(moex_url)
    return df

def load_imoex():
    moex_url = 'https://iss.moex.com/iss/engines/stock/markets/index/securities/IMOEX.json'
    df = get_data(moex_url)
    return df

def main():
    st.title("Индексы")
    
    left_column, right_column = st.columns(2)
    
    with left_column:
        st.subheader(f"RGBI: {load_rgbi()['CURRENTVALUE'].values[0]}")
        
        rgbi_df = load_rgbi()
        
        last_change = float(rgbi_df['LASTCHANGEPRC'].values[0])
        change_color = "green" if last_change >= 0 else "red"
        st.markdown(f"Изменение к закрытию: <span style='color:{change_color}; font-weight:bold; font-size:16px;'>{last_change:.2f}%</span>", unsafe_allow_html=True)
        st.text(f"Дата обновления: {rgbi_df['SYSTIME'].values[0]")
    
    with right_column:
        st.subheader(f"IMOEX: {load_imoex()['CURRENTVALUE'].values[0]")
        
        imoex_df = load_imoex()
        
        last_change = float(imoex_df['LASTCHANGEPRC'].values[0])
        change_color = "green" if last_change >= 0 else "red"
        st.markdown(f"Изменение к закрытию: <span style='color:{change_color}; font-weight:bold; font-size:16px;'>{last_change:.2f}%</span>", unsafe_allow_html=True)
        st.text(f"Дата обновления: {imoex_df['SYSTIME'].values[0]")
    
    if st.button('Обновить данные', key='refresh'):
        pass

if __name__ == "__main__":
    main()
