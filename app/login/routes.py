from app import db
from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from app.login.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, AcceptOrderForm
from flask_babel import _, get_locale
from guess_language import guess_language
from app.translate import translate
from app.models import User
from app.login import bp
from app.login.email import send_password_reset_email


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Відображення сторінки впровадження нового пароля"""

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('login.login'))
    return render_template('login/reset_password.html', form=form, title='Ресетування паролю')


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    """Відновлення пароля через електронну почту""" 
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(_('Check your email for the instructions to reset your password'))
        return redirect(url_for('login.login'))
    return render_template('login/reset_password_request.html', title='Запит на ресетування паролю'
        , form=form)


@bp.route('/login', methods = ['GET', 'POST'])
def  login():
    """Login view function logic"""
    if current_user.is_authenticated:#Якщо користувач залогований ...
        return redirect(url_for('main.index'))#...return index
    form = LoginForm()
    if form.validate_on_submit():#Якщо натиснуто SUBMIT
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):#Провірка ауторизаційних данних
            flash(_('Invalid username or password'))
            return redirect(url_for('login.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')#Redirect to next page
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login/login.html', title='Вхід',  form=form)


@bp.route('/logout')
def logout():
    """Logout view function"""
    logout_user()
    return redirect(url_for('main.index'))


