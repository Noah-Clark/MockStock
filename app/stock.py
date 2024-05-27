# This file contains the stock class and its attributes

# import nasdaqdatalink as nasdaq
#from app import app, db
from app import functions
from app.models import UserStock
import yfinance as yf



class Stock:
    """
    Constructor for the stock object
    Parameters: name: str, price: float, symbol: str, shares_owned: int
    Return: Null
    """

    def __init__(self, name: str, price: float, ticker: str, shares_owned=0, start_price=None, stock_score=100):
        self.name = name
        self.price = price
        self.ticker = ticker
        self.shares_owned = shares_owned
        self.start_price = start_price
        self.stock_score = stock_score

    def set_stock_score(self, new_score):
        """
        Adjusts the stock score for the search
        """
        self.stock_score = new_score
        

    def updateStartPrice(self):
        """
        updates the start price
        Parameters: Self
        Return: null
        """
        self.start_price = self.getPrice()

    def getPrice(self):
        """
    Price finds the price out of a list of popular tickers #update list to check with stocks in database in the future
    Parameters: Null
    Returns: Either the price of the given ticker or "Not Valid Ticker"
    """
        ticker = self.ticker
        tickerData = yf.Ticker(ticker)
        data = tickerData.history()
        price = round(data['Close'].iloc[-1], 2)
        return price


# popularTickers = ['DIS', 'PNRA', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'PCAR', 'BRK/A', 'BRK/B', 'TSLA', 'NVDA',
#                     'META', 'V', 'XOM', 'TSM', 'UNH', 'JPM', 'JNJ', 'WMT', 'MA', 'PG', 'NVO', 'CVX', 'HD', 'LLY', 'ABBV',
#                     'BAC', 'MRK', 'AVGO', 'KO', 'GME']


'''
Price finds the price out of a list of popular tickers #update list to check with stocks in database in the future
Parameters: String- ticker
Returns: Either the price of the given ticker or "Not Valid Ticker"
'''
# real data
# stocks = [ Stock('Apple Inc.', 'AAPL'),
#     Stock('Microsoft Corporation', 'MSFT'),
#     Stock('Alphabet Inc. Class A', 'GOOGL'),
#     Stock('Amazon.com Inc.', 'AMZN'),
#     Stock('Tesla Inc.', 'TSLA'),
#     Stock('Facebook Inc. Class A', 'FB')]
#     Stock('Berkshire Hathaway Inc. Class B', 'BRK.B'),
#     Stock('Visa Inc. Class A', 'V'),
#     Stock('Johnson & Johnson', 'JNJ'),
#     Stock('JPMorgan Chase & Co.', 'JPM'),
#     Stock('Procter & Gamble Co.', 'PG'),
#     Stock('NVIDIA Corporation', 'NVDA'),
#     Stock('UnitedHealth Group Incorporated', 'UNH'),
#     Stock(name = 'Walt Disney Co.', ticker= 'DIS'),
#     Stock('Mastercard Incorporated Class A', 'MA'),
#     Stock('Adobe Inc.', 'ADBE'),
#     Stock('Home Depot Inc.', 'HD'),
#     Stock('PayPal Holdings Inc.', 'PYPL'),
#     Stock('Netflix Inc.', 'NFLX'),
#     Stock('Merck & Co. Inc.', 'MRK'),
#     Stock('Verizon Communications Inc.', 'VZ'),
#     Stock('AT&T Inc.', 'T'),
#     Stock('Visa Inc. Class A', 'V'),
#     Stock('McDonalds Corporation', 'MCD'),
#     Stock('Comcast Corporation Class A', 'CMCSA'),
#     Stock('Salesforce.com Inc.', 'CRM'),
#     Stock('Cisco Systems Inc.', 'CSCO'),
#     Stock('Pfizer Inc.', 'PFE'),
#     Stock('Abbott Laboratories', 'ABT'),
#     Stock('AbbVie Inc.', 'ABBV'),
#     Stock('Intel Corporation', 'INTC'),
#     Stock('The Procter & Gamble Company', 'PG'),
#     Stock('Coca-Cola Company', 'KO'),
#     Stock('Goldman Sachs Group Inc.', 'GS'),
#     Stock('Oracle Corporation', 'ORCL'),
#     Stock('PepsiCo Inc.', 'PEP'),
#     Stock('Bristol-Myers Squibb Company', 'BMY'),
#     Stock('Comcast Corporation Class A', 'CMCSA'),
#     Stock('Accenture plc Class A', 'ACN'),
#     Stock('Broadcom Inc.', 'AVGO'),
#     Stock('United Parcel Service Inc. Class B', 'UPS'),
#     Stock('Morgan Stanley', 'MS'),
#     Stock('Exxon Mobil Corporation', 'XOM'),
#     Stock('Walmart Inc.', 'WMT'),
#     Stock('Nike Inc. Class B', 'NKE'),
#     Stock('Baidu Inc. ADR Class A', 'BIDU'),
#     Stock('Boeing Company', 'BA'),
#     Stock('3M Company', 'MMM'),
#     Stock('Citigroup Inc.', 'C'),
#     Stock('Ford Motor Company', 'F'),
#     Stock('General Electric Company', 'GE'),
#     Stock('The Coca-Cola Company', 'KO'),
#     Stock('Caterpillar Inc. Common Stock', 'CAT'),
#     Stock('Chevron Corporation', 'CVX'),
#     Stock('The Home Depot Inc.', 'HD'),
#     Stock('IBM Common Stock', 'IBM'),
#     Stock('Intel Corporation', 'INTC'),
#     Stock('JPMorgan Chase & Co. Common Stock', 'JPM'),
#     Stock('Microsoft Corporation', 'MSFT'),
#     Stock('NIKE Inc. Common Stock', 'NKE'),
#     Stock('Pfizer Inc.', 'PFE')]
# Sample data
stock_set = [

    Stock("Disney", 105.22, "DIS", 22, 46.21),

    Stock("Alphabet Inc Class A", 94.35, "GOOGL", 0, 97.45),

    Stock("Panera", 31.93, "PNRA", 45, 31.93),

    Stock("Warner Bros Discovery", 15.53, "WBD", 64),

    Stock("Nestle ADR", 118.60, "NSRGY", 87)

]


