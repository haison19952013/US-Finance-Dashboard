import streamlit as st
from .utils import Price_plot, Bullet_plot, Gauge_plot, Make_grid

def Overview_tab(tab_obj,data_obj,from_date,to_date):
    with tab_obj:
        symbol = data_obj.symbol
        tickerData = data_obj.tickerData
        financial_statement_df = data_obj.financial_statement_df
        # plot using column in streamlit
        fig = Price_plot(symbol, tickerData, start_date = from_date,end_date = to_date)
        st.plotly_chart(fig,use_container_width=True)
        fig = Bullet_plot(financial_statement_df,y = 'Z_score',ylabel = 'Altman Z-Score', ref_value = 3.0)
        st.plotly_chart(fig,use_container_width=True)
        mygrid = Make_grid(2,2)
        fig = Gauge_plot(financial_statement_df,y = 'Debt_2_equity',ylabel = 'Debt-to-Equity', ref_value = 1.0)
        mygrid[0][0].plotly_chart(fig,use_container_width=True)
        fig = Gauge_plot(financial_statement_df,y = 'Current_ratio',ylabel = 'Current Ratio', ref_value = 1.0)
        mygrid[0][1].plotly_chart(fig,use_container_width=True)
        fig = Gauge_plot(financial_statement_df,y = 'Asset_turnover_rate',ylabel = 'Asset Turnover Rate', ref_value= 1.0)
        mygrid[1][0].plotly_chart(fig,use_container_width=True)
        fig = Gauge_plot(financial_statement_df,y = 'Inventory_turnover_rate',ylabel = 'Inventory Turnover Rate',ref_value = 1.0)
        mygrid[1][1].plotly_chart(fig,use_container_width=True)

