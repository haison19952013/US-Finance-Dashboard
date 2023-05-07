import streamlit as st
from src import Financial_statement_analysis, Side, Overview_tab, BS_tab, IS_tab, CF_tab, Top

if __name__ == '__main__':
    st.set_page_config(layout='wide')
    tickerSymbol, from_date, to_date = Side()
    data_obj = Financial_statement_analysis(tickerSymbol)
    Top(data_obj)
    overview_tab, BS_analysis, IS_analysis, CF_analysis, NE_analysis= st.tabs(["Overview",
                            "Balance Sheet Analysis", 
                            "Income Statement Analysis", 
                            "Cash Flow Analsysis",
                            "News and Events"])
    Overview_tab(overview_tab,data_obj,from_date, to_date)
    BS_tab(BS_analysis,data_obj)
    IS_tab(IS_analysis,data_obj)
    CF_tab(CF_analysis,data_obj)
    