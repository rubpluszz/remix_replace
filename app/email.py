from flask_mail import Message
from app import mail
from threading import Thread
from flask import current_app

"""Функція відправки повідомлееня є асинхронною та реалізована за допомогою Thread"""

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body,
               attachments=None, sync=False):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(current_app._getcurrent_object(), msg)).start()
