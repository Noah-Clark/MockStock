class FavoriteStock:

    def __init__(self, user_id: int, stock_id: str, favorited: bool, price: float, start_price: float):
        self.user_id = user_id
        self.stock_id = stock_id
        self.favorited = favorited
        self.price = price
        self.start_price = start_price
