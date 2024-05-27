# This file will hold transaction objects for each time a user buys or sells a stock




class Transaction:

    def __init__(self, userID: int, stockID: int, action: str, amount: int, price: float):
        self.userID = userID
        self.stockID = stockID
        self.action = action
        self.amount = amount
        self.price = price



