from werkzeug.security import generate_password_hash, check_password_hash
from app import login, db
from flask_login import UserMixin
import app.models


class User(UserMixin):
    """A class representing a User."""

    # profile_name: str
    # email: str
    # username: str
    # password: str
    password_hash: str
    id_counter = 0

    def __init__(self, profile_name: str, email: str, username: str, balance: float = 0, password: str = None):
        """
        Constructor for the User class
        :param profile_name: str
        :param email: str
        :param username: str
        :param password: str
        """
        self.profile_name = profile_name
        self.email = email
        self.username = username
        self.id = User.id_counter
        self.balance = balance
        self.password = None
        self.password_hash = None
        User.id_counter += 1

    # ----------------------------------------------------------------------------
    # Had to add the getters so that the portfolio file would run DO NOT DELETE!!!

    def get_profileName(self):
        """
        Gets the profile name from the user class
        :return: profile_name: str
        """
        return self.profile_name

    def get_email(self):
        """
        Gets the email from the user class
        :return: email: str
        """
        return self.email

    def get_username(self):
        """
        Gets the username from the user class
        :return: username: str
        """
        return self.username

    def get_password(self):
        """
        Gets the password from the user class
        :return: password: str
        """
        return self.password_hash

    # ----------------------------------------------------------------------------

    def get_id(self):
        """
        Return: id
        Necessary function for flask_login, gets and returns the unique id of the user
        """
        return self.id

    def set_password(self, password):
        """
        param: passward
        Generates a hash for the given password and sets that as the User's new password
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        param: password
        Checks the hash of the given password and returns True or False if it matches
        """
        return check_password_hash(self.password_hash, password)


# @login.user_loader
# def load_user(id):
#     """
#     Loads the current user into the system using their unique ID when redirecting to a new page.
#     """

    # def load_user(id):
    #     with app.app_context():
    #         return User.query.get(int(id))


sample_users = [
    User("Noah", "fake_email@gmail.com", "test1", 1000, "pass1"),
    User("Witten", "this_email@gmail.com", "test2", 10000, "pass2"),
    User("Anthony", "that_email@gmail.com", "test3", 30000, "pass3")
]
