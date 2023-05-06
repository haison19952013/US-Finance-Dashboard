import streamlit as st
from src import Financial_statement_analysis, Side, Tab1, Tab2, Tab3, Tab4, Top

if __name__ == '__main__':
    tickerSymbol = Side()
    data_obj = Financial_statement_analysis(tickerSymbol)
    Top(data_obj)
    tab1, tab2, tab3, tab4 = st.tabs(["Overview",
                            "Balance Sheet Analysis", 
                            "Income Statement Analysis", 
                            "Cash Flow Analsysis"])
    Tab1(tab1,data_obj)
    Tab2(tab1,data_obj)
    Tab3(tab1,data_obj)
    Tab4(tab1,data_obj)
    