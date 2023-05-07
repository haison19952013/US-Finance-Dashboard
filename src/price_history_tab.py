import streamlit as st
import pandas as pd
from .utils import Create_download_link

def Price_history_tab(tab_obj,data_obj,start_date,end_date):
    with tab_obj:
        symbol = data_obj.symbol
        tickerData = data_obj.tickerData
        # plot using column in streamlit
        st.markdown(f"# {symbol} Stock Price ({start_date} - {end_date})")
        price_data = tickerData.history(start=start_date, end=end_date, period='ytd', interval= '1d')
        price_data = price_data.reset_index()
        price_data = price_data.drop('symbol', axis=1)
        st.dataframe(price_data)
        if st.button('Generate CSV file'):
            tmp_download_link = Create_download_link(price_data , 'mydata')
            st.markdown(tmp_download_link, unsafe_allow_html=True)

