from app.email import send_email
from flask import render_template, current_app


def send_password_confirmation_email(user):
    """Відправка листа для підтвердження пошти 
        та установки користувацького паролю"""
    
    token = user.get_set_password_token()
    print('/n token',token)
    send_email(
                'Створення паролю новим користувачем', 
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[user.email],
                text_body=render_template('email/set_password.txt', user=user, token=token),
                html_body=render_template('email/set_password.html', user=user, token=token)
              )

