import streamlit as st
from .utils import Time_series_plot

def IS_tab(tab_obj,data_obj):
    with tab_obj:
        st.header('1. Income Statement')

