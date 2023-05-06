import yahooquery as yq
import pandas as pd

def Load_symbol_name():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header = 0)
    df = html[0]
    return tuple(df['Symbol'].values.tolist())

class Financial_statement_analysis():
    def __init__(self,symbol,frequency="a"):
        self.tickerData = yq.Ticker(symbol)
        self.financial_statement_df = self.tickerData.all_financial_data(frequency=frequency)
        self.price = self.tickerData.price[symbol]
        self.symbol = symbol
        self.preprocess()
        self.extract_metrics()
    
    def preprocess(self):
        def format_year(year):
            return '{:.0f}'.format(year)
        df = self.financial_statement_df
        df['year_quarter'] = df['asOfDate'].dt.strftime('%Y-Q') + df['asOfDate'].dt.quarter.astype(str)
        df['year'] = df['asOfDate'].dt.year
        df['year'] = df['year'].apply(format_year)
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

if __name__ == '__main__':
    ticker = Financial_statement_analysis('MMM')
    df = ticker.financial_statement_df


