from app import db
from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from app.register.forms import RegistrationForm, AcceptOrderForm
from flask_babel import _, get_locale
from guess_language import guess_language
from app.translate import translate
from app.models import User
from app.register import bp
from app.register.email import send_password_reset_email

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
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Дякуємо за реєстрацію. На вказану вами адресу було відправлене електронне повідомлення з інструкціями щодо активації вашого рахунку. Якщо ви не отримали цього повідомлення, зверніться до адміністратора форуму за адресою leo@astyle.org.ua.')
        return redirect(url_for('register.endregister'))
    return render_template("register/register.html", title='Реєстрація', form=form)


