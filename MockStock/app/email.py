from flask_mail import Message
from app import mail, app
from flask import render_template


def send_email(subject, sender, recipients, text_body, html_body):
    """
    Takes a message, subject, and the email of the sender and the recipient and sends out an email.
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_password_reset_email(user):
    """
    Gets a token from the user who clicked the reset password link then utilizes the
    send_email function to send out the reset password email.
    """
    token = user.get_reset_password_token()
    send_email('[MockStock] Reset Your Password',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, token=token),
               html_body=render_template('email/reset_password.html', user=user, token=token))