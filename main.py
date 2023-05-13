import streamlit as st
from src import Financial_statement_analysis, Side, Overview_tab, FS_tab, Top, Price_history_tab, News_tab

if __name__ == '__main__':
    st.set_page_config(layout='wide')
    tickerSymbol, start_date, end_date = Side()
    data_obj = Financial_statement_analysis(tickerSymbol)
    Top(data_obj)
    overview_tab, FS_analysis_tab, News_analysis_tab, Price_history_analysis_tab = st.tabs(["Overview",
                            "Financial Statement Analysis",
                            "News and Events",
                            "Price History"])
    Overview_tab(overview_tab,data_obj,start_date, end_date)
    FS_tab(FS_analysis_tab,data_obj)
    Price_history_tab(Price_history_analysis_tab,data_obj,start_date, end_date)
    News_tab(News_analysis_tab,data_obj)
    