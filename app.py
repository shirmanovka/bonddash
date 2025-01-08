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
    if value.startswith('-'):
        return f'<span style="color: red">{value}</span>'
    else:
        return f'<span style="color: green">{value}</span>'

def main():
    st.title("Индексы")
    
    rgbi_df = load_rgbi()
    imoex_df = load_imoex()
    
    # Создаем таблицу для отображения значений
    table_data = {
        "RGBI": [
            f"{rgb_i}" for rgb_i in rgbi_df["CURRENTVALUE"]
        ],
        "Изменение": [
            color_change(change) for change in rgbi_df["LASTCHANGEPRC"]
        ],
        "Дата обновления": [
            f"{date}" for date in rgbi_df["SYSTIME"]
        ]
    }
    
    table_data_imoex = {
        "IMOEX": [
            f"{imoex}" for imoex in imoex_df["CURRENTVALUE"]
        ],
        "Изменение": [
            color_change(change) for change in imoex_df["LASTCHANGEPRC"]
        ],
        "Дата обновления": [
            f"{date}" for date in imoex_df["SYSTIME"]
        ]
    }
    
    st.write("### Индексы:")
    st.markdown(pd.DataFrame(table_data).to_html(escape=False), unsafe_allow_html=True)
    st.write("### IMOEX:")
    st.markdown(pd.DataFrame(table_data_imoex).to_html(escape=False), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
