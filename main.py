import streamlit as st
from src import Financial_statement_analysis, Side, Overview_tab, FS_tab, Top, Downloads_tab, News_tab

if __name__ == '__main__':
    st.set_page_config(layout='wide')
    tickerSymbol, start_date, end_date = Side()
    data_obj = Financial_statement_analysis(tickerSymbol)
    Top(data_obj)
    Overview_st_tab, FS_analysis_st_tab, News_st_tab, Download_st_tab = st.tabs(["Overview",
                            "Financial Statement Analysis",
                            "News and Events",
                            "Downloads"])
    Overview_tab(Overview_st_tab,data_obj,start_date, end_date)
    FS_tab(FS_analysis_st_tab,data_obj)
    Downloads_tab(Download_st_tab,data_obj,start_date, end_date)
    News_tab(News_st_tab,data_obj)
    