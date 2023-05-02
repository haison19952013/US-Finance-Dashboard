import yfinance as yf
import streamlit as st
import yahooquery as yq
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.graph_objects as go

class financial_statement_analysis():
    def __init__(self,tickerData, frequency="a"):
        self.financial_statement_df = tickerData.all_financial_data(frequency=frequency)
        self.preprocess()
    
    def preprocess(self):
        def format_year(year):
            return '{:.0f}'.format(year)
        df = self.financial_statement_df
        df['asOfDate'] = df['asOfDate'].dt.year
        df['asOfDate'] = df['asOfDate'].apply(format_year)
        self.financial_statement_df = df
    
    def extract_metrics(self):
        df  = self.financial_statement_df
        # Calculate Debt-to-equity = Total Liabilities / Total Shareholders Equity (Stockholders Equity)
        Total_liabilities = df['TotalLiabilitiesNetMinorityInterest'].values # Total_liabilities = df['TotalAssets'].values - df['StockholdersEquity'].values
        Debt_2_equity = Total_liabilities / df['StockholdersEquity'].values
        df['Debt_2_equity'] = Debt_2_equity.tolist()

        # Calculate current ratio = Current asset/ Current debt
        df['Current_ratio'] = df['CurrentAssets'].values / df['CurrentDebt'].values

        # Asset Turnover Rate = Total Sales / (Beginning Assets + Ending Assets)/2
        df['TotalSales'] = df['TotalRevenue'].values
        df['BeginningAssets'] = df['TotalAssets'].shift(1).values
        df['EndingAssets'] = df['TotalAssets'].values
        df['Asset_turnover_rate'] = df['TotalSales'].values / ((df['BeginningAssets'].values + df['EndingAssets'].values)/2)

        # Inventory Turnover Rate = Costs of goods solds / (Beginning Inventory + Ending Inventory)/2
        df['CostsOfGoodsAndServicesSold'] = df['CostOfRevenue'].values
        df['BeginningInventory'] = df['Inventory'].shift(1).values
        df['EndingInventory'] = df['Inventory'].values
        df['Inventory_turnover_rate'] = df['CostsOfGoodsAndServicesSold'].values / ((df['BeginningInventory'].values + df['EndingInventory'].values)/2)

        # Assets Growth = Total Assets (year) -  Total Assets (year - 1) / Total Assets (year) * 100%
        df['Assets_growth'] = df['TotalAssets'].pct_change() * 100

        # Stockholders Equity Growth = Stockholders Equity (year) -  Stockholders Equity (year - 1) / Stockholders Equity (year) * 100%
        df['StockholdersEquity_growth'] = df['StockholdersEquity'].pct_change() * 100

        self.financial_statement_df = df
    
    def time_series_plot(self,x,y,xlabel,ylabel,kind = 'line'):
        df = self.financial_statement_df
        # Plot data
        (fig, ax) = plt.subplots(1, 1, figsize=(10, 8))
        # Create a plot
        df.plot(x = x, y = y, kind = kind,ax = ax,legend = None)
        ax.set_xlabel(xlabel, fontsize=16)
        ax.set_ylabel(ylabel, fontsize=16)
        ax.tick_params(labelsize=12, labelrotation = 0)
        ax.grid(True)
        return fig
    
    def gauge_plot(self,y,ylabel):
        # gauge chart using plotly
        df = self.financial_statement_df
        # Filter data to take the latest year
        df = df[df['asOfDate'] == df['asOfDate'].max()]
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = df[[y]].values.tolist()[0][0],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': ylabel}))
        return fig



def load_symbol_name():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header = 0)
    df = html[0]
    return tuple(df['Symbol'].values.tolist())


# define the ticker symbol
symbol_tuple = load_symbol_name()
tickerSymbol = st.selectbox(label = 'Ticker Symbol of the analyzed company', options = symbol_tuple)
# tickerSymbol = 'XOM'
longname = yf.Ticker(tickerSymbol).info["longName"]
st.title('Finanicial Statement Analsysis For %s (%s)' % (longname, tickerSymbol))

# Get data and extract metrics
tickerData = yq.Ticker(tickerSymbol)
financial_statement = financial_statement_analysis(tickerData)
financial_statement_df = financial_statement.financial_statement_df
financial_statement.extract_metrics()

# Ask for displaying raw data
with st.container():
    show_data = st.checkbox("Do you want to see the full table of financial statement data?")
    if show_data:
        financial_statement_df

st.header('1. Balance Sheet Analysis')
st.subheader('1.2 Overview')
fig = financial_statement.gauge_plot(y = 'Debt_2_equity',ylabel = 'Debt-to-Equity')
st.plotly_chart(fig, use_container_width=True)
# plot using column


# Analyze financial health
st.subheader('1.2 Financial Health')
st.write('- Debt-to-Equity = Total Liabilities / Total Shareholders Equity (Stockholders Equity)')
fig = financial_statement.time_series_plot(x = 'asOfDate', y = 'Debt_2_equity', xlabel='Year',ylabel='Debt-to-Equity',kind = 'bar')
st.pyplot(fig)

st.write('- Current Ratio = Current Assets / Current Debt')
fig = financial_statement.time_series_plot(x = 'asOfDate', y = 'Current_ratio', xlabel='Year',ylabel='Current Ratio',kind = 'bar')
st.pyplot(fig)

# Analyze asset utilization
st.subheader('1.3 Asset Utilization')
st.write('- Asset Turnover Rate = Total Sales / (Beginning Assets + Ending Assets)/2')
fig = financial_statement.time_series_plot(x = 'asOfDate', y = 'Asset_turnover_rate', xlabel='Year',ylabel='Asset Turnover Rate',kind = 'bar')
st.pyplot(fig)

st.write('- Inventory Turnover Rate = Costs of goods solds / (Beginning Inventory + Ending Inventory)/2')
fig = financial_statement.time_series_plot(x = 'asOfDate', y = 'Inventory_turnover_rate', xlabel='Year',ylabel='Inventory Turnover Rate',kind = 'bar')
st.pyplot(fig)

# Analyze bussiness growth
st.subheader('1.4 Bussiness Growth')
st.write('- Assets Growth = Total Assets (year) -  Total Assets (year - 1) / Total Assets (year) * 100%')
fig = financial_statement.time_series_plot(x = 'asOfDate', y = 'Assets_growth', xlabel='Year',ylabel='Assets Growth (%)',kind = 'bar')
st.pyplot(fig)

st.write('- Stockholders Equity Growth = Stockholders Equity (year) -  Stockholders Equity (year - 1) / Stockholders Equity (year) * 100%')
fig = financial_statement.time_series_plot(x = 'asOfDate', y = 'StockholdersEquity_growth', xlabel='Year',ylabel='Stockholders Equity Growth  (%)',kind = 'bar')
st.pyplot(fig)

st.header('2. Income Statement')
st.header('3. Cash Flow')


