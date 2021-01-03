from app import db
from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from app.register.forms import RegistrationForm, AcceptOrderForm, SetPasswordForm
from flask_babel import _, get_locale
from guess_language import guess_language
from app.translate import translate
from app.models import User
from app.register import bp
from app.register.email import send_password_confirmation_email
#Для генерації тимчасового паролю
import random
import string


@bp.route('/accept_order', methods=['GET', 'POST'])
def accept_order():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = AcceptOrderForm()
    if form.cancel.data:
       return redirect(url_for('main.index'))
    if form.submit.data:
        if form.accept_order.data and  form.accept_language.data:
            return redirect(url_for('register.register'))
        else:
            flash('Для продовження реєстрації необхідно погодитися з умовами використання сервісу.')
    return render_template('register/accept_order.html', title='Реєстрація',  form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password("".join(random.choice("0123456789ABCDEF") for i in range(16)))
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_confirmation_email(user)
        return redirect(url_for('register.endregister'))
    return render_template('register/register.html', title='Реєстрація', form=form)


@bp.route('/endregister', methods=['GET', 'POST'])
def endregister():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    flash('Дякуємо за реєстрацію. На вказану вами адресу було відправлене електронне повідомлення з інструкціями щодо активації вашого акаунта. Якщо ви не отримали цього повідомлення, зверніться до адміністратора форуму за адресою leo@astyle.org.ua.')
    return render_template('register/endregister.html', title='Дякуємо за реєстрацію')


@bp.route('/set_password/<token>', methods=['GET', 'POST'])
def set_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_set_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = SetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Вам необхідно задати пароль для вашого облікового запису')
        return redirect(url_for('login.login'))
    return render_template('register/set_password.html', form=form, title='Реєстрація')