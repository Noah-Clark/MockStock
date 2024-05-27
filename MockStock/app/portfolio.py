# Need the user class to be made before this can be merged since it needs to pull email, etc.

from app.user import User, sample_users
from app.stock import stock_set


class Portfolio(User):
    """
    This class represents a user's individual portfolio.
    """
    def __init__(self, user: User, balance: float, fav_stocks: list, profit: float, num_stocks_pur: int):
        """
        Initializes the portfolio data class
        :param user: The user that is connected to the portfolio
        :param balance: The user's active balance
        :param fav_stocks: The list of the user's favorite stocks
        :param profit: The user's profit (can be both positive or negative)
        :param num_stocks_pur: The amount of stocks that the user has purchased
        """
        super().__init__(user.get_profileName(), user.get_email(), user.get_username(), user.get_password())
        self.balance = balance
        self.fav_stocks = fav_stocks
        self.profit = profit
        self.num_stocks_pur = num_stocks_pur


# Sample Data
user_portfolios = [
    # Tests basic account
    Portfolio(sample_users[0], 29000, [stock_set[0], stock_set[1], stock_set[2]], 400, 9),
    # Tests no favorites
    Portfolio(sample_users[1], 23000, [], 4500, 3),
    # Tests negative profit
    Portfolio(sample_users[2], 67000, [stock_set[3], stock_set[4]], -200, 5),
]
