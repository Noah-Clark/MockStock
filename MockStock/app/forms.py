from app import app
from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, StringField, PasswordField, IntegerField
from app.portfolio import user_portfolios  # Using fake data for now (will be replaced by the database later)
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange
from app.models import User


class FavoritesForm(FlaskForm):
    # favorites_list = user_portfolios[0].fav_stocks

    # unfavorite_buttons = []
    # for stock in range(len(favorites_list)):
    #     unfavorite_buttons.append(BooleanField('Unfavorite', default=True))

    submit_changes = SubmitField(
        'Submit Changes')  # Submit button for when the toggle button's functionality is fully realized


class SearchForm(FlaskForm):
    search = StringField()
    submit = SubmitField('Search')


class ProfileForm(FlaskForm):
    balance = IntegerField('Reset Your balance ($5,000-$50,000):', validators=[DataRequired()])
    reset = SubmitField('Reset')


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    profile_name = StringField('Profile Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    balance = IntegerField('Starting Balance ($5,000-$50,000):', validators=[DataRequired(), NumberRange(min=5000, max=50000)])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        """
        Checks to see if a username is already taken and raises an error if it is.
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        """
        Checks to see if an email is already in use on an account and raises an error if it is.
        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')


class ChangeUsernameForm(FlaskForm):
    old_username = StringField('Old Username', validators=[DataRequired()])
    username = StringField('New Username', validators=[DataRequired()])
    submit = SubmitField('Change Username')

