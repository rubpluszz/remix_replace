from app.email import send_email
from flask import render_template, current_app
from flask_babel import _


def send_password_reset_email(user):
    """Відправка листа для скидання паролю"""
    token = user.get_reset_password_token()
    send_email(
                _('[MultManiak] Reset Your Password'), 
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[user.email], 
                text_body=render_template('email/reset_password.txt', user=user, token=token),
                html_body=render_template('email/reset_password.html', user=user, token=token)
              )

