import streamlit as st
from .utils import Time_series_plot, Make_grid

def FS_tab(tab_obj,data_obj):
    with tab_obj:
        tickerData = data_obj.tickerData
        valuation_measures = tickerData.valuation_measures
        valuation_measures = valuation_measures.query('periodType != "TTM"').copy()
        valuation_measures['year_quarter'] = valuation_measures['asOfDate'].dt.strftime('%Y-Q') + valuation_measures['asOfDate'].dt.quarter.astype(str)
        valuation_measures[['MarketCap','EnterpriseValue']] = valuation_measures[['MarketCap','EnterpriseValue']] / 10**9
        
        metrics = [
                'ForwardPeRatio', 'PsRatio', 'PbRatio',
                  'EnterprisesValueEBITDARatio', 'EnterprisesValueRevenueRatio',
                  'PeRatio', 'MarketCap', 'EnterpriseValue', 'PegRatio'
                ]
        ylabels = [
                'Forward P/E ', 'P/S', 'P/B',
                  'Enterprises Value / EBITDA', 'Enterprises Value / Revenue',
                  'Current P/E', 'Market Cap (BUSD)', 'Enterprise Value (BUSD)', 'PEG'
                ]
        ratio_grid =  Make_grid(3,3)
        for i,metric in enumerate(metrics):
            fig = Time_series_plot(valuation_measures,x = 'year_quarter', y = metric, xlabel='',ylabel=ylabels[i],kind = 'line')
            ratio_grid[i//3][i%3].pyplot(fig,use_container_width=True)
    

        text = '''
        - `Forward P/E`: Forward price-to-earnings (P/E) ratio is a measure of a company's current stock price relative to its predicted earnings per share (EPS) for a future period, usually the next 12 months. It is a valuation metric that helps investors determine whether a stock is overvalued or undervalued.

        - `P?S`: Price-to-sales (P/S) ratio is a valuation metric that compares a company's stock price to its revenue. It is calculated by dividing the current market price of a share of stock by the company's revenue per share. The P/S ratio is a useful tool for comparing the valuations of companies in the same industry.

        - `P/B`: Price-to-book (P/B) ratio is a valuation metric that compares a company's stock price to its book value per share. The book value is the value of a company's assets minus its liabilities. A P/B ratio of less than 1 can indicate that a stock is undervalued.

        - `EnterprisesValue / EBITDA`: Enterprise value-to-EBITDA (EV/EBITDA) ratio is a measure of a company's valuation that compares its enterprise value (EV) to its earnings before interest, taxes, depreciation, and amortization (EBITDA). The EV/EBITDA ratio is a useful tool for comparing the valuations of companies with different levels of debt.

        - `Enterprises Value / Revenue`: Enterprise value-to-revenue (EV/R) ratio is a valuation metric that compares a company's enterprise value (EV) to its revenue. The EV/R ratio is a useful tool for comparing the valuations of companies in the same industry.

        - `Current P/R`: Price-to-earnings (P/E) ratio is a valuation metric that compares a company's stock price to its earnings per share (EPS). The P/E ratio is a useful tool for comparing the valuations of companies in the same industry.

        - `Market Cap`: Market capitalization (market cap) is a measure of the total value of a company's outstanding shares of stock. It is calculated by multiplying the number of outstanding shares by the current market price of a single share.

        - `EnterpriseValue`: Enterprise value (EV) is a measure of a company's total value. It is calculated as market capitalization plus debt minus cash and cash equivalents.

        - `PEG`: Price/earnings-to-growth (PEG) ratio is a valuation metric that compares a company's P/E ratio to its expected earnings growth rate. The PEG ratio can help investors determine whether a stock is overvalued or undervalued based on its earnings growth potential. A PEG ratio of less than 1 can indicate that a stock is undervalued.
        '''
        # Ask for displaying raw data
        with st.container():
            show_data = st.checkbox("Do you want to see the full table of valuation measures?")
            if show_data:
                st.dataframe(valuation_measures)
        
        # Ask for displaying raw data
        with st.container():
            show_explanation = st.checkbox("Do you want to see the explanations of valuation measures?")
            if show_explanation :
                st.markdown(text)

        # Analyze financial health
        # st.subheader('1. Financial Health')
        # st.write('- Debt-to-Equity = Total Liabilities / Total Shareholders Equity (Stockholders Equity)')
        # fig = Time_series_plot(financial_statement_df,x = 'year', y = 'Debt_2_equity', xlabel='Year',ylabel='Debt-to-Equity',kind = 'bar')
        # st.pyplot(fig,use_container_width=True)

        # st.write('- Current Ratio = Current Assets / Current Debt')
        # fig = Time_series_plot(financial_statement_df,x = 'year', y = 'Current_ratio', xlabel='Year',ylabel='Current Ratio',kind = 'bar')
        # st.pyplot(fig)

        # # Analyze asset utilization
        # st.subheader('2. Asset Utilization')
        # st.write('- Asset Turnover Rate = Total Sales / (Beginning Assets + Ending Assets)/2')
        # fig = Time_series_plot(financial_statement_df,x = 'year', y = 'Asset_turnover_rate', xlabel='Year',ylabel='Asset Turnover Rate',kind = 'bar')
        # st.pyplot(fig)

        # st.write('- Inventory Turnover Rate = Costs of goods solds / (Beginning Inventory + Ending Inventory)/2')
        # fig = Time_series_plot(financial_statement_df,x = 'year', y = 'Inventory_turnover_rate', xlabel='Year',ylabel='Inventory Turnover Rate',kind = 'bar')
        # st.pyplot(fig)

        # # Analyze bussiness growth
        # st.subheader('3. Bussiness Growth')
        # st.write('- Assets Growth = Total Assets (year) -  Total Assets (year - 1) / Total Assets (year) * 100%')
        # fig = Time_series_plot(financial_statement_df,x = 'asOfDate', y = 'Assets_growth', xlabel='Year',ylabel='Assets Growth (%)',kind = 'bar')
        # st.pyplot(fig)

        # st.write('- Stockholders Equity Growth = Stockholders Equity (year) -  Stockholders Equity (year - 1) / Stockholders Equity (year) * 100%')
        # fig = Time_series_plot(financial_statement_df,x = 'asOfDate', y = 'StockholdersEquity_growth', xlabel='Year',ylabel='Stockholders Equity Growth  (%)',kind = 'bar')
        # st.pyplot(fig)

