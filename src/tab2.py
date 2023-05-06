import streamlit as st
from .utils import Time_series_plot

def Tab2(tab2_obj,data_obj):
    with tab2_obj:
        financial_statement_df = data_obj.financial_statement_df
        # Analyze financial health
        st.subheader('1. Financial Health')
        st.write('- Debt-to-Equity = Total Liabilities / Total Shareholders Equity (Stockholders Equity)')
        fig = Time_series_plot(financial_statement_df,x = 'year', y = 'Debt_2_equity', xlabel='Year',ylabel='Debt-to-Equity',kind = 'bar')
        st.pyplot(fig,use_container_width=True)

        st.write('- Current Ratio = Current Assets / Current Debt')
        fig = Time_series_plot(financial_statement_df,x = 'year', y = 'Current_ratio', xlabel='Year',ylabel='Current Ratio',kind = 'bar')
        st.pyplot(fig)

        # Analyze asset utilization
        st.subheader('2. Asset Utilization')
        st.write('- Asset Turnover Rate = Total Sales / (Beginning Assets + Ending Assets)/2')
        fig = Time_series_plot(financial_statement_df,x = 'year', y = 'Asset_turnover_rate', xlabel='Year',ylabel='Asset Turnover Rate',kind = 'bar')
        st.pyplot(fig)

        st.write('- Inventory Turnover Rate = Costs of goods solds / (Beginning Inventory + Ending Inventory)/2')
        fig = Time_series_plot(financial_statement_df,x = 'year', y = 'Inventory_turnover_rate', xlabel='Year',ylabel='Inventory Turnover Rate',kind = 'bar')
        st.pyplot(fig)

        # Analyze bussiness growth
        st.subheader('3. Bussiness Growth')
        st.write('- Assets Growth = Total Assets (year) -  Total Assets (year - 1) / Total Assets (year) * 100%')
        fig = Time_series_plot(financial_statement_df,x = 'asOfDate', y = 'Assets_growth', xlabel='Year',ylabel='Assets Growth (%)',kind = 'bar')
        st.pyplot(fig)

        st.write('- Stockholders Equity Growth = Stockholders Equity (year) -  Stockholders Equity (year - 1) / Stockholders Equity (year) * 100%')
        fig = Time_series_plot(financial_statement_df,x = 'asOfDate', y = 'StockholdersEquity_growth', xlabel='Year',ylabel='Stockholders Equity Growth  (%)',kind = 'bar')
        st.pyplot(fig)

