import unittest
from flask_testing import TestCase
from flask import Flask
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import time


class Tests(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    # US: 32, Sign up successful:
    def test_sign_up_success(self):
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())

        driver.get('http://127.0.0.1:5000/sign_up')
        driver.maximize_window()
        element = driver.find_element(By.ID, 'username')
        element.send_keys('NewUser')
        time.sleep(2)
        element = driver.find_element(By.ID, 'email')
        element.send_keys('NewUser@gmail.com')
        time.sleep(2)
        element = driver.find_element(By.ID, 'profile_name')
        element.send_keys('New User')
        time.sleep(2)
        element = driver.find_element(By.ID, 'password')
        element.send_keys('NewPass')
        time.sleep(2)
        element = driver.find_element(By.ID, 'password2')
        element.send_keys('NewPass')
        element = driver.find_element(By.ID, 'balance')
        element.send_keys('30000')
        time.sleep(2)
        driver.find_element(By.ID, 'submit').click()
        #time.sleep(2)
        current_url = driver.current_url
        driver.quit()
        assert current_url == 'http://127.0.0.1:5000/login'

    # US: 32, Sign up fails:
    def test_sign_up_failure(self):
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())

        driver.get('http://127.0.0.1:5000/sign_up')
        driver.maximize_window()
        element = driver.find_element(By.ID, 'username')
        element.send_keys('')
        time.sleep(2)
        element = driver.find_element(By.ID, 'email')
        element.send_keys('')
        time.sleep(2)
        element = driver.find_element(By.ID, 'profile_name')
        element.send_keys('')
        time.sleep(2)
        element = driver.find_element(By.ID, 'password')
        element.send_keys('')
        time.sleep(2)
        element = driver.find_element(By.ID, 'password2')
        element.send_keys('')
        element = driver.find_element(By.ID, 'balance')
        element.send_keys('')
        time.sleep(2)
        driver.find_element(By.ID, 'submit').click()
        time.sleep(2)
        current_url = driver.current_url
        driver.quit()
        assert current_url == 'http://127.0.0.1:5000/sign_up'

    # US: 8, Acceptance Criteria: Correct login, can access homepage
    def test_login_success(self):
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())

        driver.get('http://127.0.0.1:5000/login')
        driver.maximize_window()
        element = driver.find_element(By.ID, 'username')
        element.send_keys('test1')
        element = driver.find_element(By.ID, 'password')
        element.send_keys('pass1')
        driver.find_element(By.ID, 'submit').click()
        current_url = driver.current_url
        driver.quit()
        assert current_url == 'http://127.0.0.1:5000/home'

    # US: 8, Acceptance Criteria: Wrong login, no access to homepage
    def test_login_failure(self):
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())

        driver.get('http://127.0.0.1:5000/login')
        driver.maximize_window()
        element = driver.find_element(By.ID, 'username')
        element.send_keys('hello')
        element = driver.find_element(By.ID, 'password')
        element.send_keys('world')
        driver.find_element(By.ID, 'submit').click()
        current_url = driver.current_url
        driver.quit()
        assert current_url == 'http://127.0.0.1:5000/login'

# US: #82, Acceptance Criteria: The graph is displayed on the Home Page
    def test_balance_graph_success(self):
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())

        driver.get('http://127.0.0.1:5000/login')
        driver.maximize_window()
        element = driver.find_element(By.ID, 'username')
        element.send_keys('hello')
        # time.sleep(2)
        element = driver.find_element(By.ID, 'password')
        element.send_keys('world')
        # time.sleep(2)
        driver.find_element(By.ID, 'submit').click()

        elem = driver.find_element(By.ID, "plot")

        assert elem.is_displayed()

    # US: #21, Acceptance Criteria: The user can see the balance of their account on the homepage
    def test_balance_visibility(self):

        driver = webdriver.Edge(EdgeChromiumDriverManager().install())

        driver.get('http://127.0.0.1:5000/login')
        driver.maximize_window()
        element = driver.find_element(By.ID, 'username')
        element.send_keys('hello')
        # time.sleep(2)
        element = driver.find_element(By.ID, 'password')
        element.send_keys('world')
        # time.sleep(2)
        driver.find_element(By.ID, 'submit').click()

        element = driver.find_element(By.ID, 'balance')

        assert element == "Balance: 150000"

    # US: #21, Acceptance Criteria: The balance is updated after every purchase
    # Meant to succeed, currently fails because it keeps failing to find the id being searched for
    def test_balance_change(self):
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())

        driver.get('http://127.0.0.1:5000/login')
        driver.maximize_window()
        element = driver.find_element(By.ID, 'username')
        element.send_keys('hello')
        # time.sleep(2)
        element = driver.find_element(By.ID, 'password')
        element.send_keys('world')
        # time.sleep(2)
        driver.find_element(By.ID, 'submit').click()

        old_bal = driver.find_element(By.ID, 'balance')
        # time.sleep(2)
        driver.find_element(By.ID, "more-info-AAPL").click()
        # time.sleep(2)
        element = driver.find_element(By.ID, 'shares')
        element.send_keys(1)
        # time.sleep(2)
        driver.find_element(By.ID, "buy-button").click()
        # time.sleep(2)
        alert = Alert(driver)
        alert.accept()
        # time.sleep(2)
        new_bal = driver.find_element(By.ID, 'balance')

        driver.quit()

        assert old_bal != new_bal

    # US: 11 Acceptance Criteria: Shows up the stock the user wanted
    # US: 39 (Since that was to interact with a search button) Acceptance Criteria: Allows the user
    # to see the results for their searched string
    def test_search_success(self):

        driver = webdriver.Edge(EdgeChromiumDriverManager().install())
        expected_result = 'Walt Disney Co. DIS'

        driver.get('http://127.0.0.1:5000/search')
        driver.maximize_window()
        element = driver.find_element(By.NAME, 'search')
        element.send_keys('DIS')
        driver.find_element(By.NAME, 'submit').click()
        result = driver.find_element(By.ID, 'DIS')
        driver.quit()

        assert result.text == expected_result

    # US: 11 Acceptance Criteria: Does not show up the stock the user wanted since it doesn't exist

    def test_search_fail(self):

        driver = webdriver.Edge(EdgeChromiumDriverManager().install())
        expected_result = 'ASFASFG'

        driver.get('http://127.0.0.1:5000/search')
        driver.maximize_window()
        element = driver.find_element(By.NAME, 'search')
        element.send_keys('ASFASFG')
        driver.find_element(By.NAME, 'submit').click()

        try:
            result = driver.find_element(By.ID, 'ASFASFG')

        # This means that the test successfully showed that it isn't there
        except Exception:
            driver.quit()
            assert True

    # US: 24 Acceptance Criteria: Switches between the home and search page (can be applied to all pages)
    def test_page_switch(self):

        driver = webdriver.Edge(EdgeChromiumDriverManager().install())
        expected_url = 'http://127.0.0.1:5000/search'

        driver.get('http://127.0.0.1:5000/login')
        driver.maximize_window()
        element = driver.find_element(By.ID, 'username')
        element.send_keys('test1')
        element = driver.find_element(By.ID, 'password')
        element.send_keys('pass1')
        driver.find_element(By.ID, 'submit').click()
        time.sleep(2)
        driver.find_element(By.LINK_TEXT, 'Search').click()
        current_url = driver.current_url
        time.sleep(2)
        driver.quit()

        assert current_url == expected_url

 # US: #60, Acceptance Criteria: The user sets their balance to $35,000 successfully.
    def test_account_reset_success(self):

        driver = webdriver.Edge(EdgeChromiumDriverManager().install())

        driver.get('http://127.0.0.1:5000/login')
        driver.maximize_window()
        element = driver.find_element(By.ID, 'username')
        element.send_keys('test1')
        time.sleep(2)
        element = driver.find_element(By.ID, 'password')
        element.send_keys('pass1')
        time.sleep(2)
        driver.find_element(By.ID, 'submit').click()
        time.sleep(2)
        driver.get('http://127.0.0.1:5000/profile')
        driver.maximize_window()
        time.sleep(2)
        element = driver.find_element(By.ID, 'balance')
        element.send_keys('35000')
        time.sleep(2)
        driver.find_element(By.ID, 'reset').click()
        time.sleep(2)
        alert = Alert(driver)
        currenttext = alert.text
        time.sleep(2)
        alert.accept()
        driver.quit()
        assert currenttext == 'Are you sure you want to reset your account to $35000?'

    # US: #60, Acceptance criteria: User sets an invalid number and fails to reset their balance.
    def test_account_reset_failure(self):
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())
        driver.get('http://127.0.0.1:5000/login')
        driver.maximize_window()
        element = driver.find_element(By.ID, 'username')
        element.send_keys('test1')
        time.sleep(2)
        element = driver.find_element(By.ID, 'password')
        element.send_keys('pass1')
        time.sleep(2)
        driver.find_element(By.ID, 'submit').click()
        time.sleep(2)
        driver.get('http://127.0.0.1:5000/profile')
        element = driver.find_element(By.ID, 'balance')
        element.send_keys('0')
        time.sleep(2)
        driver.find_element(By.ID, 'reset').click()
        alert = Alert(driver)
        currenttext = alert.text
        time.sleep(2)
        alert.dismiss()
        driver.quit()
        assert currenttext == 'You have to choose a balance within the range $20,000 - $50,000'

    # US: 34 Acceptance criteria: The user enters an amount of shares to buy and clicks the buy button and has the corresponding currency subtracted from their balance and shares added to their portfolio.
    # US: 70 Acceptance criteria: The user enters an amount of shares to buy or sell and the system displays the cost based off of the current stock price.
    def test_buy_success(self):
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())

        # Login
        driver.get('http://127.0.0.1:5000/login')
        driver.maximize_window()
        element = driver.find_element(By.ID, 'username')
        element.send_keys('WittenJoplin')
        element = driver.find_element(By.ID, 'password')
        element.send_keys('pass1')
        driver.find_element(By.ID, 'submit').click()

        # Search for stocks
        driver.find_element(By.ID, "search").click()
        driver.find_element(By.ID, 'submit').click()
        #time.sleep(2)

        # Click on more info button for the stock
        driver.find_element(By.ID, "more-info-AAPL").click()

        # Click the buy button
        element = driver.find_element(By.ID, 'shares')
        element.send_keys(1)
        driver.find_element(By.ID, "buy-button").click()

        # Accept confirmation message
        alert = Alert(driver)
        alert.accept()

        # Check if the user was redirected to the buy page
        current_url = driver.current_url
        driver.quit()
        assert current_url == 'http://127.0.0.1:5000/buy'

    # US: 65 Acceptance criteria: The user enters an amount of shares in a stock to sell and clicks the sell button, and the corresponding shares are removed from their portfolio and currency is added to their balance.
    # US: 70 Acceptance criteria: The user enters an amount of shares to buy or sell and the system displays the cost based off of the current stock price.
    def test_sell_success(self):
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())

        # Login
        driver.get('http://127.0.0.1:5000/login')
        driver.maximize_window()
        element = driver.find_element(By.ID, 'username')
        element.send_keys('WittenJoplin')
        element = driver.find_element(By.ID, 'password')
        element.send_keys('pass1')
        driver.find_element(By.ID, 'submit').click()

        # Search for stock
        driver.find_element(By.ID, "search").click()
        driver.find_element(By.ID, 'submit').click()

        # Click on more info button for the stock
        driver.find_element(By.ID, "more-info-AAPL").click()

        # Click the sell button
        element = driver.find_element(By.ID, 'shares2')
        element.send_keys(1)
        driver.find_element(By.ID, "sell-button").click()

        # Accept confirmation message
        alert = Alert(driver)
        alert.accept()

        # Check if the user was redirected to the sell page
        current_url = driver.current_url
        driver.quit()
        assert current_url == 'http://127.0.0.1:5000/sell'

    # US: 70 Acceptance criteria: The user enters an amount of shares to buy or sell and the system displays the cost based off of the current stock price.
    def test_buy_cancel(self):
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())

        # Login
        driver.get('http://127.0.0.1:5000/login')
        driver.maximize_window()
        element = driver.find_element(By.ID, 'username')
        element.send_keys('WittenJoplin')
        element = driver.find_element(By.ID, 'password')
        element.send_keys('pass1')
        driver.find_element(By.ID, 'submit').click()

        # Search for stock
        driver.find_element(By.ID, "search").click()
        driver.find_element(By.ID, 'submit').click()

        # Click on more info button for the stock
        driver.find_element(By.ID, "more-info-AAPL").click()

        # Click the buy button
        element = driver.find_element(By.ID, 'shares')
        element.send_keys(1)
        driver.find_element(By.ID, "buy-button").click()

        # Cancel confirmation message
        alert = Alert(driver)
        alert.dismiss()

        # Check if the user stayed on the same page
        current_url = driver.current_url
        driver.quit()
        assert current_url == 'http://127.0.0.1:5000/stock_temp'

    # US: 70 Acceptance criteria: The user enters an amount of shares to buy or sell and the system displays the cost based off of the current stock price.
    def test_sell_cancel(self):
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())

        # Login
        driver.get('http://127.0.0.1:5000/login')
        driver.maximize_window()
        element = driver.find_element(By.ID, 'username')
        element.send_keys('WittenJoplin')
        element = driver.find_element(By.ID, 'password')
        element.send_keys('pass1')
        driver.find_element(By.ID, 'submit').click()

        # Search for stocks
        driver.find_element(By.ID, "search").click()
        driver.find_element(By.ID, 'submit').click()

        # Click on more info button for the stock
        driver.find_element(By.ID, "more-info-AAPL").click()

        # Click the sell button
        element = driver.find_element(By.ID, 'shares2')
        element.send_keys(1)
        driver.find_element(By.ID, "sell-button").click()

        # Cancel confirmation message
        alert = Alert(driver)
        alert.dismiss()

        # Check if the user stayed on the same page
        current_url = driver.current_url
        driver.quit()
        assert current_url == 'http://127.0.0.1:5000/stock_temp'

   # US: 70 Acceptance criteria: The user enters an invalid entry (negative number, wrong data type, etc) and receives an error message.
    def test_sell_negative_error(self):
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())

        # Login
        driver.get('http://127.0.0.1:5000/login')
        driver.maximize_window()
        element = driver.find_element(By.ID, 'username')
        element.send_keys('WittenJoplin')
        element = driver.find_element(By.ID, 'password')
        element.send_keys('pass1')
        driver.find_element(By.ID, 'submit').click()

        # Search for stock
        driver.find_element(By.ID, "search").click()
        driver.find_element(By.ID, 'submit').click()

        # Click on more info button for the stock
        driver.find_element(By.ID, "more-info-AAPL").click()

        # Click the sell button with negative shares
        element = driver.find_element(By.ID, 'shares2')
        element.send_keys(-1)
        driver.find_element(By.ID, "sell-button").click()

        # Get error Message
        error_message = element.get_attribute("validationMessage")

        driver.quit()

        assert error_message == "Value must be greater than or equal to 1."

    # US: 70 Acceptance criteria: The user enters an invalid entry (negative number, wrong data type, etc) and receives an error message.
    def test_buy_negative_error(self):
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())

        # Login
        driver.get('http://127.0.0.1:5000/login')
        driver.maximize_window()
        element = driver.find_element(By.ID, 'username')
        element.send_keys('WittenJoplin')
        element = driver.find_element(By.ID, 'password')
        element.send_keys('pass1')
        driver.find_element(By.ID, 'submit').click()

        # Search for stock
        driver.find_element(By.ID, "search").click()
        driver.find_element(By.ID, 'submit').click()

        # Click on more info button for the stock
        driver.find_element(By.ID, "more-info-AAPL").click()

        # Click the buy button with negative number
        element = driver.find_element(By.ID, 'shares')
        element.send_keys(-1)
        driver.find_element(By.ID, "buy-button").click()
        # Get error Message
        error_message = element.get_attribute("validationMessage")

        driver.quit()
        assert error_message == "Value must be greater than or equal to 1."

    # US: 70 Acceptance criteria: The user enters an invalid entry (negative number, wrong data type, etc) and receives an error message.
    def test_sell_zero_error(self):
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())

        # Login
        driver.get('http://127.0.0.1:5000/login')
        driver.maximize_window()
        element = driver.find_element(By.ID, 'username')
        element.send_keys('WittenJoplin')
        element = driver.find_element(By.ID, 'password')
        element.send_keys('pass1')
        driver.find_element(By.ID, 'submit').click()

        # Search for stock
        driver.find_element(By.ID, "search").click()
        driver.find_element(By.ID, 'submit').click()

        # Click on more info button for the stock
        driver.find_element(By.ID, "more-info-AAPL").click()

        # Click the sell button with 0 shares
        element = driver.find_element(By.ID, 'shares2')
        element.send_keys(0)
        driver.find_element(By.ID, "sell-button").click()

        # Get error message
        error_message = element.get_attribute("validationMessage")

        driver.quit()

        assert error_message == "Value must be greater than or equal to 1."

    # US: 70 Acceptance criteria: The user enters an invalid entry (negative number, wrong data type, etc) and receives an error message.
    def test_buy_zero_error(self):
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())

        # Login
        driver.get('http://127.0.0.1:5000/login')
        driver.maximize_window()
        element = driver.find_element(By.ID, 'username')
        element.send_keys('WittenJoplin')
        element = driver.find_element(By.ID, 'password')
        element.send_keys('pass1')
        driver.find_element(By.ID, 'submit').click()

        # Search for stock
        driver.find_element(By.ID, "search").click()
        driver.find_element(By.ID, 'submit').click()

        # Click on more info button for the stock
        driver.find_element(By.ID, "more-info-AAPL").click()

        # Click the buy button with zero
        element = driver.find_element(By.ID, 'shares')
        element.send_keys(0)
        driver.find_element(By.ID, "buy-button").click()

        # Get error message
        error_message= element.get_attribute("validationMessage")

        driver.quit()

        assert error_message == "Value must be greater than or equal to 1."

    # US: 65 Acceptance criteria: The user clicks the sell button after entering an invalid amount (more shares than they own) and receives an error message.
    def test_sell_large_number_error(self):
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())

        # Login
        driver.get('http://127.0.0.1:5000/login')
        driver.maximize_window()
        element = driver.find_element(By.ID, 'username')
        element.send_keys('WittenJoplin')
        element = driver.find_element(By.ID, 'password')
        element.send_keys('pass1')
        driver.find_element(By.ID, 'submit').click()

        # Search for stock
        driver.find_element(By.ID, "search").click()
        driver.find_element(By.ID, 'submit').click()

        # Click on more info button for the stock
        driver.find_element(By.ID, "more-info-AAPL").click()

        # Click the sell button with a large number
        element = driver.find_element(By.ID, 'shares2')
        element.send_keys(99999999)
        driver.find_element(By.ID, "sell-button").click()

        # Accept confirmation message
        alert = Alert(driver)
        alert.accept()

        # locate the element containing the message
        message_element = driver.find_element(By.ID,"message")

        # extract the message text from the element
        message = message_element.text
        error_message = ' '.join(message.split()[:2])


        # close the WebDriver
        driver.quit()

        assert error_message == "Insufficient shares:"

    # US: 34 Acceptance criteria: The user enters an invalid amount of shares to buy(not enough currency) and receives an error message.
    def test_buy_large_number_error(self):
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())

        # Login
        driver.get('http://127.0.0.1:5000/login')
        driver.maximize_window()
        element = driver.find_element(By.ID, 'username')
        element.send_keys('WittenJoplin')
        element = driver.find_element(By.ID, 'password')
        element.send_keys('pass1')
        driver.find_element(By.ID, 'submit').click()

        # Search for stock
        driver.find_element(By.ID, "search").click()

        driver.find_element(By.ID, 'submit').click()

        # Click on more info button for the stock
        driver.find_element(By.ID, "more-info-AAPL").click()

        # Click the buy button with large number
        element = driver.find_element(By.ID, 'shares')
        element.send_keys(999999999)

        driver.find_element(By.ID, "buy-button").click()

        # Accept confirmation message
        alert = Alert(driver)
        alert.accept()

        # locate the element containing the message
        message_element = driver.find_element(By.ID,"message")

        # extract the message text from the element
        message = message_element.text
        error_message = ' '.join(message.split()[:3])


        # close the WebDriver
        driver.quit()
        assert error_message == "Not enough funds:"

    # US: 70 Acceptance criteria: The user enters an invalid entry (negative number, wrong data type, etc) and receives an error message.
    def test_sell_decimal_error(self):
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())

        # Login
        driver.get('http://127.0.0.1:5000/login')
        driver.maximize_window()
        element = driver.find_element(By.ID, 'username')
        element.send_keys('WittenJoplin')
        element = driver.find_element(By.ID, 'password')
        element.send_keys('pass1')
        driver.find_element(By.ID, 'submit').click()

        # Search for stock
        driver.find_element(By.ID, "search").click()
        driver.find_element(By.ID, 'submit').click()


        # Click on more info button for the stock
        driver.find_element(By.ID, "more-info-AAPL").click()
        #time.sleep(2)

        # Click the sell button with 1.1 shares
        element = driver.find_element(By.ID, 'shares2')
        element.send_keys(1.1)

        driver.find_element(By.ID, "sell-button").click()

        # Get error Message
        error_message = element.get_attribute("validationMessage")


        driver.quit()

        assert error_message == "Please enter a valid value. The two nearest valid values are 1 and 2."

    # US: 70 Acceptance criteria: The user enters an invalid entry (negative number, wrong data type, etc) and receives an error message.
    def test_buy_decimal_error(self):
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())

        # Login
        driver.get('http://127.0.0.1:5000/login')
        driver.maximize_window()
        element = driver.find_element(By.ID, 'username')
        element.send_keys('WittenJoplin')
        element = driver.find_element(By.ID, 'password')
        element.send_keys('pass1')
        driver.find_element(By.ID, 'submit').click()

        # Search for stock
        driver.find_element(By.ID, "search").click()
        driver.find_element(By.ID, 'submit').click()

        # Click on more info button for the stock
        driver.find_element(By.ID, "more-info-AAPL").click()

        # Click the buy button
        element = driver.find_element(By.ID, 'shares')
        element.send_keys(1.1)
        driver.find_element(By.ID, "buy-button").click()

        # Get error Message
        error_message = element.get_attribute("validationMessage")

        driver.quit()
        assert error_message == "Please enter a valid value. The two nearest valid values are 1 and 2."

    # US: 70 Acceptance criteria: The user enters an invalid entry (negative number, wrong data type, etc) and receives an error message.
    def test_sell_null_error(self):
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())

        # Login
        driver.get('http://127.0.0.1:5000/login')
        driver.maximize_window()
        element = driver.find_element(By.ID, 'username')
        element.send_keys('WittenJoplin')
        element = driver.find_element(By.ID, 'password')
        element.send_keys('pass1')
        driver.find_element(By.ID, 'submit').click()

        # Search for stock
        driver.find_element(By.ID, "search").click()
        driver.find_element(By.ID, 'submit').click()


        # Click on more info button for the stock
        driver.find_element(By.ID, "more-info-AAPL").click()
        #time.sleep(2)

        # Click the sell button with no shares
        element = driver.find_element(By.ID, 'shares2')

        driver.find_element(By.ID, "sell-button").click()

        # Get error Message
        error_message = element.get_attribute("validationMessage")


        driver.quit()

        assert error_message == "Please fill out this field."

    # US: 70 Acceptance criteria: The user enters an invalid entry (negative number, wrong data type, etc) and receives an error message.
    def test_buy_null_error(self):
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())

        # Login
        driver.get('http://127.0.0.1:5000/login')
        driver.maximize_window()
        element = driver.find_element(By.ID, 'username')
        element.send_keys('WittenJoplin')
        element = driver.find_element(By.ID, 'password')
        element.send_keys('pass1')
        driver.find_element(By.ID, 'submit').click()

        # Search for stock
        driver.find_element(By.ID, "search").click()
        driver.find_element(By.ID, 'submit').click()

        # Click on more info button for the stock
        driver.find_element(By.ID, "more-info-AAPL").click()

        # Click the buy button
        element = driver.find_element(By.ID, 'shares')

        driver.find_element(By.ID, "buy-button").click()

        # Get error Message
        error_message = element.get_attribute("validationMessage")

        driver.quit()

        assert error_message == "Please fill out this field."



if __name__ == '__main__':
    unittest.main()
