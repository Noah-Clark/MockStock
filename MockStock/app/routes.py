from flask import Flask, render_template, flash, redirect, url_for, request

from app import app, db
from app.functions import stock_instantiation
from app.login_form import Login_Form
from flask_login import current_user, login_user, logout_user
from app.forms import SearchForm, FavoritesForm, SignUpForm, ProfileForm, ResetPasswordRequestForm, ResetPasswordForm, ChangeUsernameForm
from app.search import Search
from app.models import User
from app.stock import Stock as st
# from app.user import User
from app.portfolio import user_portfolios  # Using fake data until the database is finished
from app import functions
from app.models import Transaction, Stock, UserFavorites, BalanceHistory, UserStock
import datetime
import yfinance as yf
import matplotlib.pyplot as plt
import io
import base64
from app.email import send_password_reset_email
from sqlalchemy import and_
#from app.create import data

# two lines needed to fix threading problem
import matplotlib
matplotlib.use('agg')


def setup_data():
    """Imports stock data into the database if no data is present; for first time initialization."""
    if not Stock.query.all():
        stock_instantiation()
        db.session.commit()


with app.app_context():
    db.create_all()
    db.session.commit()
    setup_data()
    # stocks = Stock.query.all()
    # for stock in stocks:
    #     db.session.delete(stock)
    #
    # user_favs = UserFavorites.query.all()
    # for stock in user_favs:
    #     db.session.delete(stock)
    #
    # db.session.commit()
    #
    # fav_id = 0
    # favorites = []
    # stocks = [Stock(name='Apple Inc.', ticker='AAPL'), Stock(name='Microsoft Corporation', ticker='MSFT'),
    #           Stock(name='Alphabet Inc. Class A', ticker='GOOGL'), Stock(name='Amazon.com Inc.', ticker='AMZN'),
    #           Stock(name='Tesla Inc.', ticker='TSLA'), Stock(name='Meta Platforms Inc.', ticker='META'),
    #           Stock(name='Visa Inc. Class A', ticker='V'), Stock(name='Johnson & Johnson', ticker='JNJ'),
    #           Stock(name='JPMorgan Chase & Co.', ticker='JPM'), Stock(name='Procter & Gamble Co.', ticker='PG'),
    #           Stock(name='NVIDIA Corporation', ticker='NVDA'),
    #           Stock(name='UnitedHealth Group Incorporated', ticker='UNH'), Stock(name='Walt Disney Co.', ticker='DIS'),
    #           Stock(name='Mastercard Incorporated Class A', ticker='MA'), Stock(name='Adobe Inc.', ticker='ADBE'),
    #           Stock(name='Home Depot Inc.', ticker='HD'), Stock(name='PayPal Holdings Inc.', ticker='PYPL'),
    #           Stock(name='Netflix Inc.', ticker='NFLX'), Stock(name='Merck & Co. Inc.', ticker='MRK'),
    #           Stock(name='Verizon Communications Inc.', ticker='VZ'), Stock(name='AT&T Inc.', ticker='T'),
    #           Stock(name='McDonalds Corporation', ticker='MCD'),
    #           Stock(name='Comcast Corporation Class A', ticker='CMCSA'),
    #           Stock(name='Salesforce.com Inc.', ticker='CRM'), Stock(name='Cisco Systems Inc.', ticker='CSCO'),
    #           Stock(name='Pfizer Inc.', ticker='PFE'), Stock(name='Abbott Laboratories', ticker='ABT'),
    #           Stock(name='AbbVie Inc.', ticker='ABBV'), Stock(name='Intel Corporation', ticker='INTC'),
    #           Stock(name='Goldman Sachs Group Inc.', ticker='GS'), Stock(name='Oracle Corporation', ticker='ORCL'),
    #           Stock(name='PepsiCo Inc.', ticker='PEP'), Stock(name='Bristol-Myers Squibb Company', ticker='BMY'),
    #           Stock(name='Accenture plc Class A', ticker='ACN'), Stock(name='Broadcom Inc.', ticker='AVGO'),
    #           Stock(name='United Parcel Service Inc. Class B', ticker='UPS'), Stock(name='Morgan Stanley', ticker='MS'),
    #           Stock(name='Exxon Mobil Corporation', ticker='XOM'), Stock(name='Walmart Inc.', ticker='WMT'),
    #           Stock(name='Baidu Inc. ADR Class A', ticker='BIDU'), Stock(name='Boeing Company', ticker='BA'),
    #           Stock(name='3M Company', ticker='MMM'), Stock(name='Citigroup Inc.', ticker='C'),
    #           Stock(name='Ford Motor Company', ticker='F'), Stock(name='General Electric Company', ticker='GE'),
    #           Stock(name='The Coca-Cola Company', ticker='KO'),
    #           Stock(name='Caterpillar Inc. Common Stock', ticker='CAT'),
    #           Stock(name='Chevron Corporation', ticker='CVX'), Stock(name='IBM Common Stock', ticker='IBM'),
    #           Stock(name='NIKE Inc. Common Stock', ticker='NKE')]
    #
    # # stocks = Stock.query.all()
    # for stock in stocks:
    #     db.session.add(stock)
    #
    #     ticker = stock.ticker
    #     start_price = yf.Ticker(ticker).history(period="1d")["Open"][0]
    #     price = yf.Ticker(ticker).history(period="1d")["Close"][0]
    #     favorite_stock = UserFavorites(id=fav_id, user_id=1, stock_id=stock.id, stock_ticker=ticker, favorited=True,
    #                                    price=price, start_price=start_price)
    #     favorites.append(favorite_stock)
    #     fav_id += 1
    #
    # for favorite in favorites:
    #     print(favorite)
    #     db.session.add(favorite)
    #     db.session.commit()


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Login_Form()
    if form.validate_on_submit():
        with app.app_context():
            user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
                    profile_name=form.profile_name.data, balance=form.balance.data)
        user.set_password(form.password.data)
        db.session.add(user)
        functions.favorites_instantiation(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('sign_up.html', title='Sign Up', form=form)


@app.route('/logout')
def logout():
    """
    Logs the user out of the system and returns to the login screen
    """
    logout_user()
    return redirect(url_for('login'))


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        with app.app_context():
            user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('login'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/home', methods=['GET', 'POST'])
def home():
    user_stock = UserStock.query.filter(and_(UserStock.user_id == current_user.id, UserStock.quantity > 0)).all()
    stocks = Stock.query.all()
    favorites_list = UserFavorites.query.filter_by(user_id=current_user.id).all()
    form = FavoritesForm()

    functions.update_balance_hist(current_user)

    user_bal = functions.get_balance(current_user)

    data = BalanceHistory.query.filter_by(user_id=current_user.id).all()
    bal_data = []
    bal_date = []
    for bal in data:
        bal_data.append(bal.day_balance)
        bal_date.append(bal.date)

    plt.plot(bal_date, bal_data)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()
    plot_html = f'<img src="data:image/png;base64,{plot_url}" />'

    plt.close('all')
    img.close()

    favorites = functions.get_favorites(current_user)
    favorites_len = len(favorites)

    has_favorites = False
    favorites_list_len = []
    curr_change_list = []
    favorites_price_list = []

    for stock in favorites:
        start_price = yf.Ticker(stock.stock_ticker).history(period="1d")["Open"][0]
        if functions.get_price(stock.stock_ticker) < start_price:
            price_diff = functions.get_start_price(stock.stock_ticker) - functions.get_price(stock.stock_ticker)
            curr_change = "▼ " + "{:.2f}".format(price_diff)
            curr_change_list.append(curr_change)
            favorites_price_list.append(functions.get_price(stock.stock_ticker))
        elif stock.price == start_price:
            curr_change = "► " + "0.00"
            curr_change_list.append(curr_change)
            favorites_price_list.append(functions.get_price(stock.stock_ticker))
        else:
            price_diff = functions.get_price(stock.stock_ticker) - functions.get_start_price(stock.stock_ticker)
            curr_change = "▲ " + "{:.2f}".format(price_diff)
            curr_change_list.append(curr_change)
            favorites_price_list.append(functions.get_price(stock.stock_ticker))

    if len(favorites) != 0:
        has_favorites = True

    for num in range(0, favorites_len):
        favorites_list_len.append(num)


    new_favorites = UserFavorites.query.filter_by(user_id=current_user.id).all()


    if request.method == 'POST':
        unfav_list = request.form.getlist('fav_stock')
        for fav in unfav_list:
            for index in range(len(new_favorites) - 1):
                if fav == new_favorites[index].stock_ticker:
                    new_favorites[index].favorited = False
        db.session.commit()
        
        return redirect(url_for('home'))

    return render_template('home.html', balance=user_bal, has_favorites=has_favorites, favorites_data=favorites,
                           curr_change=curr_change_list, favorites_list_len=favorites_list_len,form=form, favorites_price=favorites_price_list, plot=plot_html, stocks=stocks, favorites=favorites_list, user_stock=user_stock)



@app.route('/stockData', methods=['GET', 'POST'])
def stock_data():
    form = FavoritesForm()

    stock_index = int(request.args.get('stock', None))
    favorites = functions.get_favorites(current_user)
    stock = favorites[stock_index]

    symbol = stock.stock_ticker
    price = stock.price
    news_links = yf.Ticker(symbol).news

    if request.method == 'POST':
        favorite = request.args.get('fav_stock', None)
        stocks = UserFavorites.query.filter_by(user_id=current_user.id, stock_ticker=symbol).all()
        for stock in stocks:
            if favorite and stock.favorited is True:
                return redirect(url_for('stock_temp', stock=stock_index, symbol=symbol, favorited=True))
            elif favorite:
                stock.favorited = True
                db.session.commit()
                favorited = True
            else:
                stock.favorited = False
                db.session.commit()
                favorited = False

        return redirect(url_for('stock_temp', stock=stock_index, symbol=symbol, favorited=favorited))

    return render_template('stockPage.html', form=form, symbol=symbol, price=price, news=news_links, favorited=True)


@app.route('/search', methods=['GET', 'POST'])
def search():

    form = SearchForm(request.form)

    if request.method == 'POST':

        name_check = form.search.data
        ticker_check = name_check.upper()
        name_check = Search.relative_name_search(name_check)
        ticker_check = Search.relative_ticker_search(ticker_check)

        if name_check[0].stock_score > ticker_check[0].stock_score:

            stock_found = name_check

        else:

            stock_found = ticker_check

        favorites_list = UserFavorites.query.filter_by(user_id=current_user.id).all()

        return render_template('results.html', title="search_results", stocklist=stock_found, favorites=favorites_list)

    return render_template('search.html', title="search", form=form)


@app.route('/base_stock')
def base_stock():

    return render_template('baseStock.html', title=request.args.get('title', None),
                           stock_name=request.args.get('stock_name', None),
                           stock_ticker=request.args.get('stock_ticker', None),
                           stock_price=request.args.get('stock_price', None),
                           stock_shares=request.args.get('stock_shares', None))


@app.route('/profile', methods=['GET', 'POST'])
def profile():

    form = ProfileForm(request.form)

    if request.method == 'POST':

        balance = form.balance.data
        functions.transaction_deletion(current_user)
        functions.stock_quantity_deletion(current_user)
        functions.balance_reset(balance, current_user)
        functions.graph_reset(current_user)

        return redirect(url_for('home'))

    return render_template('profile.html', title="profile", form=form, balance=current_user.balance)


@app.route('/change_username', methods=['GET', 'POST'])
def change_username():
    form = ChangeUsernameForm()
    if request.method == 'POST':
        if current_user.username == form.old_username.data:
            username = form.username.data
            with app.app_context():
                user = User.query.filter_by(username=form.username.data).first()
            if user is not None:
                flash('Please select a different username')
                return redirect(url_for('change_username'))
            else:
                functions.change_username(username, current_user)
                flash('Username successfully changed')
                return redirect(url_for('change_username'))
        else:
            flash('Wrong old username')
            return redirect(url_for('change_username'))
    return render_template('change_username.html', title="Change Username", form=form)


@app.route('/stock_temp',methods=['GET', 'POST'])
def stock_temp():
    if request.method == 'POST':
        text = request.form['ticker']
        start = request.form['start_date']
        end = request.form['end_date']
        fav = request.form.get('fav_stock')
        stock = functions.tickerExist(text)
        if not stock:
            flash("Not Valid Stock")
            return redirect(url_for('stock_temp'))

        viz_stock = UserFavorites.query.filter_by(user_id=current_user.id, stock_ticker=text).first()
        if fav == 'True':
            viz_stock.favorited = True
            favorited = True
            db.session.commit()
        else:
            viz_stock.favorited = False
            favorited = False
            db.session.commit()

        quantity = functions.getQuantity(stock, current_user)
        stockObject = st(name=stock.name, price=0, ticker=stock.ticker)
        price = stockObject.getPrice()
        today = str(datetime.date.today())
        articles = yf.Ticker(stockObject.ticker).news
        # Checks before attempting to extract data
        # Check if the ticker is valid
        # Check that the start date is before the end date
        # Check if the start date is before today
        if price != "Not Valid Ticker" and start < end and start < today:
            # Generate plot

            data = yf.download(text, start, end)

            data.Close.plot()

            # Convert plot to image
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)

            # Embed image in HTML
            plot_url = base64.b64encode(img.getvalue()).decode()
            plot_html = f'<img src="data:image/png;base64,{plot_url}" />'

            # Close Threads
            plt.close('all')
            img.close()

            return render_template('stockPage.html', enteredText=text, result=price, plot_html=plot_html,
                                   quantity=quantity, news=articles, favorited=favorited)

        return render_template('stockPage.html', enteredText=text, result=price, quantity=quantity,
                               news=articles, favorited=favorited)

    return render_template('stockPage.html', title="stock")


@app.route('/buy', methods=['GET', 'POST'])
def buy():
    user= current_user
    ticker = request.form['ticker2']
    shares = int(request.form['shares'])
    stock = functions.tickerExist(ticker)
    if not stock:
        flash("Not Valid Stock")
        return redirect(url_for('stock_temp',ticker=ticker))
    stockObject= st(stock.name,0, stock.ticker,0)
    price= stockObject.getPrice()
    quantity = functions.getQuantity(stock, user)
    total_cost = shares * price

    # Check if the user has enough balance to make the purchase
    if user.balance < total_cost:
        flash("Not enough funds: your balance is "+str(user.balance)+"$")
        return render_template('stockPage.html', enteredText=ticker, result=price,quantity=quantity)
    functions.buy(ticker, user, shares, price)

    return render_template('buy.html', ticker=ticker,shares= shares)


@app.route('/sell', methods=['GET', 'POST'])
def sell():
    user=current_user
    ticker = request.form['ticker3']
    shares = int(request.form['shares2'])
    stock= functions.tickerExist(ticker)
    if not stock:
        flash("Not Valid Stock")
        return redirect(url_for('stock_temp'))
    stockObject = st(stock.name,0, stock.ticker,0)
    price= stockObject.getPrice()
    sharesOwned= functions.getQuantity(stock,user)
    if sharesOwned < shares:
        flash("Insufficient shares: you own "+ str(sharesOwned)+" shares")
        return render_template('stockPage.html', enteredText=ticker, result=price,quantity=sharesOwned)
    functions.sell(ticker,user,shares,price)

    return render_template('sell.html', ticker=ticker,shares= shares)


@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    transactionList=functions.transactionList(current_user)
    return render_template('transactionPage.html', transactionList=transactionList)
