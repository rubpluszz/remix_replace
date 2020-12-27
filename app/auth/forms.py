from flask_wtf import FlaskForm
from wtforms import  StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User
from flask_babel import _, lazy_gettext as _l


class LoginForm(FlaskForm):

    """docstring for LoginForm(FlaskForm"""

    username = StringField('Ім`я користувача' , validators = [DataRequired()])
    password = PasswordField('Пароль', validators = [DataRequired()])
    remember_me = BooleanField('Запам`ятай мене')
    submit = SubmitField('Увійти')


class AcceptOrderForm(FlaskForm):
    """docstring for AcceptOrderForm"""
    accept_order = BooleanField('Я погоджуюсь з правилами форуму та бажаю зареєструватися')
    accept_language = BooleanField('Я буду спілкуватись українською мовою.')
    submit = SubmitField('Погоджуюсь')   
    cancel = SubmitField('Скасувати')

class RegistrationForm(FlaskForm):

    """Когда вы добавляете какие-либо методы, соответствующие 
    шаблону validate_<имя_поля>, WTForms принимает их 
    как пользовательские валидаторы и вызывает их в дополнение к 
    стандартным валидаторам."""

    username = StringField(_l('Username'), validators = [DataRequired()])
    email = StringField(_l('Email'), validators = [DataRequired(), Email()])#Для поля электронной почты email я добавил второй валидатор после DataRequired, называемый Email. Это еще один валидатор (в оригинале «stock validator», т.е. правильнее это перевести как встроенный, стандартный), который поставляется с WTForms, который гарантирует, что то, что пользователь вводит в этом поле, соответствует структуре адреса электронной почты.
    password = PasswordField(_l('Password'), validators = [DataRequired()])
    password2 = PasswordField(_l('Repeat Password'), validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Register'))


    def validate_username(self, username):
        """Провірка поданого імені користувача 
            вільне воно чи зайняте"""
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different username'))


    def validate_email(self, email):
        """ Провірка чи невикористовується поданий емаіл іншим користувачем"""
        user = User.query.filter_by(email = email.data).first()
        if user is not None :
            raise ValidationError(_('Please use a different email'))



class ResetPasswordRequestForm(FlaskForm):

    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))



class ResetPasswordForm(FlaskForm):

    """Form to reset user password"""

    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(_l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Request Password Reset'))
