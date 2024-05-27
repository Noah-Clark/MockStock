from app import db, login, app
import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from time import time
import jwt


# from app.search import add_to_index, query_index


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    profile_name = db.Column(db.String(64), index=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    balance = db.Column(db.Float)
    portfolio = db.relationship('Portfolio', backref='Owner', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    with app.app_context():
        return User.query.get(int(id))


class Portfolio(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    profit = db.Column(db.Float)
    num_stocks_pur = db.Column(db.Integer(), index=True)

    def __repr__(self):
        return 'Portfolio {}'.format(self.email)


class Stock(db.Model):
    __searchable__ = ['name', "ticker"]
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(6), nullable=False, unique=True)
    name = db.Column(db.String(120), index=True)
    price = db.Column(db.Float())

    def __repr__(self):
        return 'Stock {}'.format(self.ticker)


class UserFavorites(db.Model):
    __tablename__ = 'user_favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    stock_ticker = db.Column(db.String(6), nullable=False, index=True)
    favorited = db.Column(db.Boolean, default=False, nullable=False)
    price = db.Column(db.Float, nullable=False)
    start_price = db.Column(db.Float, nullable=False)


class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    user = db.relationship('User', backref=db.backref('transactions', lazy=True))
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False, index=True)
    stock = db.relationship('Stock', backref=db.backref('transactions', lazy=True))
    action = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow, index=True)

    def __repr__(self):
        return 'Transaction {}'.format(self.timestamp)


class BalanceHistory(db.Model):
    __tablename__ = 'balance_history'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    date = db.Column(db.Date, default=datetime.date.today, index=True)
    day_balance = db.Column(db.Float)


class UserStock(db.Model):
    __tablename__ = 'user_stock'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), primary_key=True)
    stock = db.relationship('Stock', backref=db.backref('UserStock', lazy=True))
    quantity = db.Column(db.Integer, nullable=False)
