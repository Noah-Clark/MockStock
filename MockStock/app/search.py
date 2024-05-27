import app.models
import app.stock
import app.functions
import operator


class Search:

    # app.stock.Stock.getPrice(stock)
    # Use the above later in place of the zeros when stocks are all sorted out

    @classmethod
    def exact_search(cls, stock, string):
        """
        Does an exact search of the stock names and ticker symbols
        :param stock: The stock that is being compared to the user's search
        :param string: The string that the user searched
        :return: boolean (True if stock and string match)
        """

        if stock.name == string:

            return True

        elif stock.ticker == string:

            return True

        else:

            return False

    @classmethod
    def parser(cls, stock, string):
        """
        Searches through the stock to see if the string is found within it
        :param stock: The stock that is being compared to the user's search
        :param string: The string that the user searched
        :return: boolean (True if string is within stock)
        """

        name = stock.name.lower()
        string = string.lower()
        word = ""
        word_list = []

        for index in range(0, len(stock.name)):

            if name[index] == " ":
                word_list.append(word)
                word = ""

            else:
                word += name[index]

        string_index = 0
        word = ""

        for index in range(0, len(stock.name)):

            if word == string:
                return True

            elif name[index] == string[string_index]:
                word += name[index]
                string_index += 1
                continue

            else:
                word = ""
                string_index = 0

        for word in word_list:

            if word == string:
                return True

        return False

    @classmethod
    def relative_name_search(cls, string):
        """
        Does a fuzzy search of the stock names
        :param string: The string that the user searched
        :return: A series of stocks similar or exact to what the user wanted
        """

        new_list = []
        stock_set = []
        stock_list = app.models.Stock.query.all()
        for stock in stock_list:
            stock_set.append(app.stock.Stock(stock.name, stock.price, stock.ticker, 0))

        for stock in stock_set:

            if cls.exact_search(stock, string) is True:
                new_list.append(stock)
                continue

            elif cls.parser(stock, string) is True:
                new_list.append(stock)
                continue

            for index in range(0, len(string) - 1):

                if index < len(stock.name):

                    if stock.name[index] != string[index]:

                        adjuster = 100 / len(string)
                        new_score = int(stock.stock_score - adjuster)
                        stock.set_stock_score(new_score)
                index += 1

            new_list.append(stock)

        sorted_list = sorted(new_list, key=operator.attrgetter('stock_score'), reverse=True)

        for stock in stock_set:

            stock.set_stock_score(100)

        final_list = []
        index = 0

        for stock in sorted_list:

            if index < 15:
                final_list.append(stock)

            index += 1

        return final_list

    @classmethod
    def relative_ticker_search(cls, string):
        """
        Does a fuzzy search of the stock ticker symbols
        :param string: The string that the user searched
        :return: A series of stocks similar or exact to what the user wanted
        """

        new_list = []
        stock_set = []
        stock_list = app.models.Stock.query.all()
        for stock in stock_list:
            stock_set.append(app.stock.Stock(stock.name, stock.price, stock.ticker, 0))

        for stock in stock_set:

            if cls.exact_search(stock, string) is True:
                new_list.append(stock)
                continue

            elif cls.parser(stock, string) is True:
                new_list.append(stock)
                continue

            for index in range(0, len(string) - 1):

                if index < len(stock.ticker):

                    if stock.ticker[index] != string[index]:
                        adjuster = 100 / len(string)
                        new_score = int(stock.stock_score - adjuster)
                        stock.set_stock_score(new_score)
                index += 1

            new_list.append(stock)

        sorted_list = sorted(new_list, key=operator.attrgetter('stock_score'), reverse=True)

        for stock in stock_set:

            stock.set_stock_score(100)

        final_list = []
        index = 0

        for stock in sorted_list:

            if index < 15:

                final_list.append(stock)

            index += 1

        return final_list
