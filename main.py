import yfinance as yf
import streamlit as st
import yahooquery as yq
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.graph_objects as go

class financial_statement_analysis():
    def __init__(self,symbol,tickerData, frequency="a"):
        self.tickerData = tickerData
        self.financial_statement_df = tickerData.all_financial_data(frequency=frequency)
        self.price = tickerData.price[symbol]
        self.symbol = symbol
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

        # Compute Altman Z-Score 
        # Z-Score = 1.2A + 1.4B + 3.3C + 0.6D + 1.0E
        # A = Working Capital / Total Assets
        # B = Retained Earnings / Total Assets
        # C = Earnings Before Interest and Taxes (EBIT) / Total Assets             
        # D = Market Value of Equity / Book Value of Total Liabilities
        # E = Sales / Total Assets
        A = df['WorkingCapital'].values / df['TotalAssets'].values
        B = df['RetainedEarnings'].values / df['TotalAssets'].values
        C = df['EBIT'].values / df['TotalAssets'].values
        D = self.price['marketCap'] / df['TotalLiabilitiesNetMinorityInterest'].values
        E = df['TotalRevenue'].values / df['TotalAssets'].values
        df['Z_score'] = 1.2 * A + 1.4 * B + 3.3 * C + 0.6 * D + 1.0 * E
        self.financial_statement_df = df
    
    def price_plot(self,start_date = '2022-01-01',end_date = '2022-05-05', interval = '1d'):
        price_data = self.tickerData.history(start=start_date, end=end_date, period='ytd', interval= interval)
        price_data = price_data.reset_index()

        # Create the candlestick chart using plotly
        fig = go.Figure(data=[go.Candlestick(x=price_data.date,
                                            open=price_data['open'],
                                            high=price_data['high'],
                                            low=price_data['low'],
                                            close=price_data['close'])])

        fig.update_layout(
            title={
                'text': f"{self.symbol} Stock Price ({start_date} - {end_date})",
                'font': {'family': "Arial", 'size': 18, 'color': "#7f7f7f"},
                'x': 0.25, # Set to 0.5 for center position or to a value >0.5 for right alignment
                'y': 0.9, # Set to 1.0 for top alignment or to a smaller value for lower position
            },
            xaxis_title="Date",
            yaxis_title="Price ($)",
        )
        return fig

    def time_series_plot(self,x,y,xlabel,ylabel,kind = 'line'):
        df = self.financial_statement_df
        # Plot data
        (fig, ax) = plt.subplots(1, 1, figsize=(6, 4))
        # Create a plot
        df.plot(x = x, y = y, kind = kind,ax = ax,legend = None)
        ax.set_xlabel(xlabel, fontsize=16)
        ax.set_ylabel(ylabel, fontsize=16)
        ax.tick_params(labelsize=12, labelrotation = 0)
        ax.grid(True)
        return fig
    
    def gauge_plot(self,y,ylabel,ref_value = 1.0):
        # gauge chart using plotly
        df = self.financial_statement_df
        # Filter data to take the latest year
        df = df[df['asOfDate'] == df['asOfDate'].max()]
        fig = go.Figure(go.Indicator(delta = {'reference': ref_value},
            mode = "gauge+number+delta",
            value = df[[y]].values.tolist()[0][0],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': ylabel}))
        fig.update_layout(font=dict(size=20))
        return fig

    def bullet_plot(self, y, ylabel, ref_value=1.0, min=-4, max=8):
        # bullet chart using plotly
        df = self.financial_statement_df
        # Filter data to take the latest year
        df = df[df['asOfDate'] == df['asOfDate'].max()]
        fig = go.Figure(go.Indicator(
            mode="number+gauge+delta", value=df[[y]].values.tolist()[0][0],
            domain={'x': [0.25, 1], 'y': [0, 1]},
            title={'text': "<b>%s</b>" % ylabel, 'align': "center"},
            delta={'reference': ref_value},
            gauge={
                'shape': "bullet",
                'axis': {
                    'range': [min, max],
                    'tickmode': 'linear',
                    'dtick': 2.0
                },
                'threshold': {
                    'line': {'color': "black", 'width': 3.5},
                    'thickness': 1.,
                    'value': df[[y]].values.tolist()[0][0]
                },
                'steps': [{'range': [min, ref_value-1], 'color': 'lightgray'},
                    {'range': [ref_value-1, ref_value+1], 'color': 'gray'},
                    {'range': [ref_value+1, max], 'color': 'lightgray'}],
                'bar': {'color': "black", 'thickness': 0}
            }
        ))

        fig.update_layout(height=250, font=dict(size=20))
        return fig



# make any grid with a function
def make_grid(cols,rows):
    grid = [0]*cols
    for i in range(cols):
        with st.container():
            grid[i] = st.columns(rows)
    return grid

def load_symbol_name():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header = 0)
    df = html[0]
    return tuple(df['Symbol'].values.tolist())


# define the ticker symbol
symbol_tuple = load_symbol_name()

with st.sidebar:
    tickerSymbol = st.selectbox(label='Please choose your company', 
                            options=symbol_tuple)
    tickerData = yq.Ticker(tickerSymbol)

longname = tickerData.quote_type[tickerSymbol]['longName']
st.markdown('<h1 style="text-align: center;">Finance Analysis Dashboard</h1>', unsafe_allow_html=True)
col1, col2 = st.columns([1,2.5])
# Column 1
company_profile = tickerData.summary_profile[tickerSymbol]
with col1:
    st.markdown('**{}**'.format(tickerSymbol))
    st.markdown(longname)
    st.markdown(' `%s` `%s` ' % ( company_profile['sector'], company_profile['industry']))


# Column 2
summary_detail = tickerData.summary_detail[tickerSymbol]
financial_data = tickerData.financial_data[tickerSymbol]
with col2:
    col21, col22 = st.columns(2)
    with col21:
        price_delta = round(financial_data["currentPrice"] - summary_detail['previousClose'],2)
        price_relative =  round((price_delta/ summary_detail['previousClose'])*100,2)
        # st.markdown('Current price')
        st.metric(label="Price", value='%s %s ' % ( summary_detail['previousClose'], summary_detail['currency']), 
                  delta="{} {} ({}%)".format(price_delta, summary_detail['currency'],price_relative),
                  label_visibility = "collapsed")
    with col22:
        st.markdown(' Highest price:  %s (%s) ' % ( round(summary_detail['dayHigh'],2), summary_detail['currency']))
        st.markdown(' Lowest price:  %s (%s) ' % ( round(summary_detail['dayLow'],2), summary_detail['currency']))
    st.markdown("Le Hai Son")

   
with st.expander("Company profile"):
        st.write(company_profile['longBusinessSummary'])

tab1, tab2, tab3, tab4 = st.tabs(["Overview",
                            "Balance Sheet Analysis", 
                            "Income Statement Analysis", 
                            "Cash Flow Analsysis"])

# Get data and extract metrics
financial_statement = financial_statement_analysis(tickerSymbol, tickerData)
financial_statement_df = financial_statement.financial_statement_df
financial_statement.extract_metrics()

# Ask for displaying raw data
with st.container():
    show_data = st.checkbox("Do you want to see the full table of financial statement data?")
    if show_data:
        financial_statement_df


with tab1:
    # plot using column in streamlit
    fig = financial_statement.price_plot(start_date = '2022-01-01',end_date = '2022-05-05')
    st.plotly_chart(fig,use_container_width=True)
    fig = financial_statement.bullet_plot(y = 'Z_score',ylabel = 'Altman Z-Score', ref_value = 3.0)
    st.plotly_chart(fig,use_container_width=True)
    mygrid = make_grid(2,2)
    fig = financial_statement.gauge_plot(y = 'Debt_2_equity',ylabel = 'Debt-to-Equity', ref_value = 1.0)
    mygrid[0][0].plotly_chart(fig,use_container_width=True)
    fig = financial_statement.gauge_plot(y = 'Current_ratio',ylabel = 'Current Ratio', ref_value = 1.0)
    mygrid[0][1].plotly_chart(fig,use_container_width=True)
    fig = financial_statement.gauge_plot(y = 'Asset_turnover_rate',ylabel = 'Asset Turnover Rate', ref_value= 1.0)
    mygrid[1][0].plotly_chart(fig,use_container_width=True)
    fig = financial_statement.gauge_plot(y = 'Inventory_turnover_rate',ylabel = 'Inventory Turnover Rate',ref_value = 1.0)
    mygrid[1][1].plotly_chart(fig,use_container_width=True)


with tab2:
    # Analyze financial health
    st.subheader('1. Financial Health')
    st.write('- Debt-to-Equity = Total Liabilities / Total Shareholders Equity (Stockholders Equity)')
    fig = financial_statement.time_series_plot(x = 'asOfDate', y = 'Debt_2_equity', xlabel='Year',ylabel='Debt-to-Equity',kind = 'bar')
    st.pyplot(fig,use_container_width=True)

    st.write('- Current Ratio = Current Assets / Current Debt')
    fig = financial_statement.time_series_plot(x = 'asOfDate', y = 'Current_ratio', xlabel='Year',ylabel='Current Ratio',kind = 'bar')
    st.pyplot(fig)

    # Analyze asset utilization
    st.subheader('2. Asset Utilization')
    st.write('- Asset Turnover Rate = Total Sales / (Beginning Assets + Ending Assets)/2')
    fig = financial_statement.time_series_plot(x = 'asOfDate', y = 'Asset_turnover_rate', xlabel='Year',ylabel='Asset Turnover Rate',kind = 'bar')
    st.pyplot(fig)

    st.write('- Inventory Turnover Rate = Costs of goods solds / (Beginning Inventory + Ending Inventory)/2')
    fig = financial_statement.time_series_plot(x = 'asOfDate', y = 'Inventory_turnover_rate', xlabel='Year',ylabel='Inventory Turnover Rate',kind = 'bar')
    st.pyplot(fig)

    # Analyze bussiness growth
    st.subheader('3. Bussiness Growth')
    st.write('- Assets Growth = Total Assets (year) -  Total Assets (year - 1) / Total Assets (year) * 100%')
    fig = financial_statement.time_series_plot(x = 'asOfDate', y = 'Assets_growth', xlabel='Year',ylabel='Assets Growth (%)',kind = 'bar')
    st.pyplot(fig)

    st.write('- Stockholders Equity Growth = Stockholders Equity (year) -  Stockholders Equity (year - 1) / Stockholders Equity (year) * 100%')
    fig = financial_statement.time_series_plot(x = 'asOfDate', y = 'StockholdersEquity_growth', xlabel='Year',ylabel='Stockholders Equity Growth  (%)',kind = 'bar')
    st.pyplot(fig)

with tab3:
    st.header('1. Income Statement')

with tab4:
    st.header('1. Cash Flow')


