from .data_loader import Load_symbol_name
import streamlit as st

def Side():
    # define the ticker symbol
    symbol_tuple = Load_symbol_name()
    with st.sidebar:
        tickerSymbol = st.selectbox(label='Please choose your company', 
                                options=symbol_tuple)
    return tickerSymbol
