from .data_loader import Load_symbol_name
import streamlit as st
import datetime

def Side():
    # define the ticker symbol
    symbol_tuple = Load_symbol_name()
    with st.sidebar:
        tickerSymbol = st.selectbox(label='Please choose your company', 
                                options=symbol_tuple)
        start_date = st.date_input("From", datetime.date(2022, 1, 1))
        end_date = st.date_input("To", datetime.date(2022, 5, 5))
    return tickerSymbol, start_date, end_date
