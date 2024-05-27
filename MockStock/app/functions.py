import yfinance as yf
from app import app, db
from app.models import Transaction, Stock, UserFavorites
import yfinance as yf
from app.user import User
from app import app , db
from app.models import Transaction, Stock, User, UserStock, BalanceHistory
from datetime import date


def tickerExist(ticker):
    """
    tickerExist takes a ticker and sees if that ticker has a matching stock in the database
    Parameters: ticker - String
    Return: result - stock model or false
    """
    result= False
    stocks = Stock.query.all()
    for i in stocks:
        if i.ticker == ticker:
            result= i
            return result
    return result


def buy(ticker: str, user: User, amount, price):
    """
      Function buy() allows the user to buy a stock at a given price
      Parameters: stock ticker, user, amount bought, and price
      Returns: String
    """
    # check that stock is in the database
    stock = tickerExist(ticker)
    if not stock:
        return "Stock not found"


    action = "buy"

    # Calculate the total cost of the purchase
    total_cost = amount * price


    transaction = Transaction(user_id= user.id, stock_id=stock.id, action=action, amount=amount, price=price)

    # Add the Transaction object to the database
    db.session.add(transaction)
    db.session.commit()

    user_stock = UserStock.query.filter_by(user_id=user.id, stock_id=stock.id).first()
    if user_stock:
        user_stock.quantity += amount

    else:
        userStock = UserStock(user_id= user.id, stock_id=stock.id,quantity=amount)
        db.session.add(userStock)

    # Update the user's balance
    current_user = User.query.filter_by(id=user.id).first()
    current_user.balance -= round(total_cost,2)

    db.session.commit()

    return "You just bought "+ str(amount)+ " shares of "+ str(ticker) + " for $"+ str(total_cost)


def sell(ticker: str , user: User, amount,price):
    """
      Function sell() allows the user to sell a stock at a given price
      Parameters: SStock ticker, user, and the amount sold
      Returns: New transaction object
    """

    #check if stock exist then get the stock
    stock= tickerExist(ticker)
    if not stock:
        return "Stock not found"

    # Set price
    action = "sell"

    total_cost = amount * price

    #update amount
    user_stock = UserStock.query.filter_by(user_id=user.id, stock_id= stock.id).first()
    user_stock.quantity -= amount
    # Commit Changes
    db.session.commit()

    transaction = Transaction(user_id=user.id, stock_id=stock.id, action=action, amount=amount, price=price)

    #Add the Transaction object to the database
    db.session.add(transaction)
    db.session.commit()

    #Update the user's balance
    current_user = User.query.filter_by(id=user.id).first()
    current_user.balance +=  round(total_cost,2)
    db.session.commit()

    return "You just sold "+ str(amount)+ " shares of "+ str(ticker) + " for $"+ str(total_cost)


def transactionList(user):
    """
    transactionList takes a user and returns a list of all of there transaction
    Parameters: user - User
    Return result - List<Transactions>
    """
    result= Transaction.query.filter_by(user_id=user.id).order_by(Transaction.timestamp.desc()).all()

    return result


def getQuantity(stock,user):
    """
    getquantity take a stock and user and return the amount of that stock the user owns
    Parameters: stock - Stock , user- User
    Return: quantity owned - Int
    """
    user_stock = UserStock.query.filter_by(user_id=user.id, stock_id=stock.id).first()

    if user_stock:
        return user_stock.quantity
    return 0

    # Update the user's balance
    # user.balance += total_cost
    # db.session.commit()


def get_favorites(user):
    """
    :param user: The current user logged into the system
    :return: Either the list of the user's current favorited stocks or none
    """
    favorites = []
    user_favs = UserFavorites.query.filter_by(user_id=user.id).all()
    if user_favs is not None:
        for stock in user_favs:
            if stock.favorited is True:
                favorites.append(stock)
        return favorites

    else:
        return None


def remove_favorites(current_user, stock_index):
    """
    :param current_user: The current user logged into the system
    :param stock_index: The index of the selected stock in the current favorites list
    :return: none
    """
    index = int(stock_index)
    user_favorites = get_favorites(current_user)

    remove_stock = user_favorites[index]
    remove_stock.favorited = False
    
    db.session.commit()


def find_favorite(user, stock_ticker):
    user_favs = UserFavorites.query.filter_by(user_id=user.id).all()
    if user_favs is not None:
        for stock in user_favs:
            if stock.ticker == stock_ticker:
                return stock


def add_favorite(user, stock_ticker):
    stock = UserFavorites.query.filter_by(user_id=user.id, stock_ticker=stock_ticker).first()
    if stock is not None:
        stock.favorited = True
        db.session.commit()


def stock_instantiation():
    """
    In case you need to instantiate all the stocks in the database
    :return: None
    """

    stocks = [Stock(name='Apple Inc.', ticker='AAPL'), Stock(name='Microsoft Corporation', ticker='MSFT'),
              Stock(name='Alphabet Inc. Class A', ticker='GOOGL'), Stock(name='Amazon.com Inc.', ticker='AMZN'),
              Stock(name='Tesla Inc.', ticker='TSLA'),
              Stock(name='Visa Inc. Class A', ticker='V'), Stock(name='Johnson & Johnson', ticker='JNJ'),
              Stock(name='JPMorgan Chase & Co.', ticker='JPM'), Stock(name='Procter & Gamble Co.', ticker='PG'),
              Stock(name='NVIDIA Corporation', ticker='NVDA'),
              Stock(name='UnitedHealth Group Incorporated', ticker='UNH'), Stock(name='Walt Disney Co.', ticker='DIS'),
              Stock(name='Mastercard Incorporated Class A', ticker='MA'), Stock(name='Adobe Inc.', ticker='ADBE'),
              Stock(name='Home Depot Inc.', ticker='HD'), Stock(name='PayPal Holdings Inc.', ticker='PYPL'),
              Stock(name='Netflix Inc.', ticker='NFLX'), Stock(name='Merck & Co. Inc.', ticker='MRK'),
              Stock(name='Verizon Communications Inc.', ticker='VZ'), Stock(name='AT&T Inc.', ticker='T'),
              Stock(name='McDonalds Corporation', ticker='MCD'),
              Stock(name='Comcast Corporation Class A', ticker='CMCSA'),
              Stock(name='Salesforce.com Inc.', ticker='CRM'), Stock(name='Cisco Systems Inc.', ticker='CSCO'),
              Stock(name='Pfizer Inc.', ticker='PFE'), Stock(name='Abbott Laboratories', ticker='ABT'),
              Stock(name='AbbVie Inc.', ticker='ABBV'), Stock(name='Intel Corporation', ticker='INTC'),
              Stock(name='Goldman Sachs Group Inc.', ticker='GS'), Stock(name='Oracle Corporation', ticker='ORCL'),
              Stock(name='PepsiCo Inc.', ticker='PEP'), Stock(name='Bristol-Myers Squibb Company', ticker='BMY'),
              Stock(name='Accenture plc Class A', ticker='ACN'), Stock(name='Broadcom Inc.', ticker='AVGO'),
              Stock(name='United Parcel Service Inc. Class B', ticker='UPS'), Stock(name='Morgan Stanley', ticker='MS'),
              Stock(name='Exxon Mobil Corporation', ticker='XOM'), Stock(name='Walmart Inc.', ticker='WMT'),
              Stock(name='Baidu Inc. ADR Class A', ticker='BIDU'), Stock(name='Boeing Company', ticker='BA'),
              Stock(name='3M Company', ticker='MMM'), Stock(name='Citigroup Inc.', ticker='C'),
              Stock(name='Ford Motor Company', ticker='F'), Stock(name='General Electric Company', ticker='GE'),
              Stock(name='The Coca-Cola Company', ticker='KO'),
              Stock(name='Caterpillar Inc. Common Stock', ticker='CAT'),
              Stock(name='Chevron Corporation', ticker='CVX'), Stock(name='IBM Common Stock', ticker='IBM'),
              Stock(name='NIKE Inc. Common Stock', ticker='NKE')]

    for stock in stocks:
        db.session.add(stock)

    db.session.commit()


def favorites_instantiation(user):
    favorites = []
    for stock in Stock.query.all():
        favorites.append(UserFavorites(user_id=user.id, stock_ticker=stock.ticker, favorited=False,
                                       price=yf.Ticker(stock.ticker).history(period="1d")["Close"][0],
                                       start_price=yf.Ticker(stock.ticker).history(period="1d")["Open"][0]))
    for favorite in favorites:
        db.session.add(favorite)

    db.session.commit()

def stock_deletion():
    """
    In case you need to delete all stocks in the database
    :return: None
    """
    stocks = Stock.query.all()

    for stock in stocks:
        db.session.delete(stock)
    
    db.session.commit()


def get_balance(current_user):
    """
    :param current_user: The current user logged into the system
    :return: The derived balance
    """
    balance = current_user.balance
    transaction_list = transactionList(current_user)
    if transaction_list is not None:
        for transaction in transaction_list:
            if transaction.action == "buy":
                amount = transaction.amount
                transaction_price = transaction.price * amount
                ticker = transaction.stock.ticker
                stock_price = yf.Ticker(ticker).history(period="1d")["Close"][0]
                curr_price = stock_price * amount

                transact_value = transaction_price - curr_price
                balance += transact_value

    return round(balance,2)

def get_price(ticker):
    """
    Price finds the price out of a list of popular tickers #update list to check with stocks in database in the future
    Parameters: Null
    Returns: Either the price of the given ticker or "Not Valid Ticker"
    """
    tickerData = yf.Ticker(ticker)
    data = tickerData.history()
    price = round(data['Close'].iloc[-1], 2)

    return price


def get_start_price(ticker):
    """
    Price finds the price out of a list of popular tickers #update list to check with stocks in database in the future
    Parameters: Null
    Returns: Either the price of the given ticker or "Not Valid Ticker"
    """
    tickerData = yf.Ticker(ticker)
    data = tickerData.history()
    price = round(data['Open'].iloc[-1], 2)

    return price


def update_balance_hist(user):
    """
    :param user: The current user logged into the system
    :return: none
    """
    today = date.today()

    curr_bal = get_balance(user)

    in_sys = False
    for balance in BalanceHistory.query.filter_by(user_id=user.id).all():
        if balance.date == today:
            balance.day_balance = curr_bal
            db.session.commit()

            return

    if in_sys is False:
        db.session.add(BalanceHistory(user_id=user.id, date=date.today(), day_balance=curr_bal))
        db.session.commit()

    return


def transaction_deletion(user):

    transactions_history = Transaction.query.filter_by(user_id=user.id).order_by(Transaction.timestamp.desc()).all()

    for transaction in transactions_history:
        db.session.delete(transaction)

    db.session.commit()


def stock_quantity_deletion(user):

    stocks = Stock.query.all()

    for stock in stocks:
        user_stock = UserStock.query.filter_by(user_id=user.id, stock_id=stock.id).first()
        if user_stock:
            user_stock.quantity = 0

    db.session.commit()


def balance_reset(balance, user):

    user = User.query.filter_by(id=user.id).first()
    user.balance = balance

    db.session.commit()


def graph_reset(user):

    day_data = BalanceHistory.query.filter_by(user_id=user.id).all()

    for day in day_data:
        db.session.delete(day)

    db.session.commit()


def change_username(username, user):

    current_user = User.query.filter_by(id=user.id).first()
    current_user.username = username

    db.session.commit()