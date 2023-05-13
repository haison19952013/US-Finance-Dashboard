import streamlit as st
import pandas as pd
from .utils import Create_download_link

def Downloads_tab(tab_obj,data_obj,start_date,end_date):
    with tab_obj:
        symbol = data_obj.symbol
        tickerData = data_obj.tickerData
        # Show history price
        st.markdown(f"# {symbol} Stock Price ({start_date} - {end_date})")
        price_data = tickerData.history(start=start_date, end=end_date, period='ytd', interval= '1d')
        price_data = price_data.reset_index()
        price_data = price_data.drop('symbol', axis=1)
        st.dataframe(price_data)
        if st.button('Generate price history file',key='button_price_history'):
            tmp_download_link = Create_download_link(price_data , 'price_history')
            st.markdown(tmp_download_link, unsafe_allow_html=True)
        
        # Show history balance sheet
        st.markdown(f"# {symbol} Balance Sheet")
        balancesheet_data = tickerData.balance_sheet(trailing=False)
        balancesheet_data = balancesheet_data.reset_index()
        balancesheet_data = balancesheet_data.drop('symbol', axis=1)
        st.dataframe(balancesheet_data)
        if st.button('Generate balance sheet file',key='balance_sheet'):
            tmp_download_link = Create_download_link(balancesheet_data , 'balance_sheet')
            st.markdown(tmp_download_link, unsafe_allow_html=True)
        
        # Show history income statement
        st.markdown(f"# {symbol} Income Statement")
        income_data = tickerData.income_statement(trailing=False)
        income_data = income_data.reset_index()
        income_data = income_data.drop('symbol', axis=1)
        st.dataframe(balancesheet_data)
        if st.button('Generate income statement file',key='income_statement'):
            tmp_download_link = Create_download_link(balancesheet_data , 'income_statement')
            st.markdown(tmp_download_link, unsafe_allow_html=True)
        
        # Show history cashflow statement
        st.markdown(f"# {symbol} Cashflow Statement")
        cashflow_data = tickerData.cash_flow(trailing=False)
        cashflow_data = cashflow_data.reset_index()
        cashflow_data = cashflow_data.drop('symbol', axis=1)
        st.dataframe(cashflow_data)
        if st.button('Generate cash flow file',key='cash_flow_statement'):
            tmp_download_link = Create_download_link(cashflow_data , 'cashflow_statement')
            st.markdown(tmp_download_link, unsafe_allow_html=True)

