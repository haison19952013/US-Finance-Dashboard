import streamlit as st
import pandas as pd
from .utils import Create_download_link

def News_tab(tab_obj,data_obj):
    with tab_obj:
        symbol = data_obj.symbol
        tickerData = data_obj.tickerData
        news_data = tickerData.corporate_events.reset_index().head(10)
        for i, row in news_data.iterrows():
            st.markdown(f"## {row['headline']}")
            st.markdown(f"**{row['description']}**")
            st.markdown(f"{row['date']}")
            st.markdown(f"---")
        
        if len(news_data) == 10:
            if st.button("Read More"):
                news_data = tickerData.corporate_events.reset_index().iloc[10:]
                for i, row in news_data.iterrows():
                    st.markdown(f"## {row['headline']}")
                    st.markdown(f"**{row['description']}**")
                    st.markdown(f"{row['date']}")
                st.markdown(f"---")





