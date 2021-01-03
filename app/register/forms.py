from flask_wtf import FlaskForm
from wtforms import  StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User
class AcceptOrderForm(FlaskForm):
    """docstring for AcceptOrderForm"""
    accept_order = BooleanField('Я погоджуюсь з правилами форуму та бажаю зареєструватися')
    accept_language = BooleanField('Я буду спілкуватись українською мовою.')
    submit = SubmitField('Погоджуюсь')   
    cancel = SubmitField('Скасувати')

class RegistrationForm(FlaskForm):

    """Коли  ви додаєте які-небудь методи, котрі відповідають 
    шаблону validate_<им'я_поля>, WTForms приймає їх 
    як користувацькі валідатори s викликає їх в доповнення до 
    стандартних валідаторів."""

    username = StringField('Ім`я користувача', validators = [DataRequired()])
    email = StringField('E-mail', validators = [DataRequired(), Email()])
    protection = StringField('Столиця України')
    submit = SubmitField('Зареєструватися')


    def validate_username(self, username):
        """Провірка поданого імені користувача 
            вільне воно чи зайняте"""
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError('Будьласка використайте відповідне ім`я користувача')


    def validate_email(self, email):
        """ Провірка чи невикористовується поданий емаіл іншим користувачем"""
        user = User.query.filter_by(email = email.data).first()
        if user is not None :
            raise ValidationError('Будьласка використайте відповідну адресу електронної почти')

    def validate_protection(self, protection):
        if protection.data.lower()!='київ' :
            raise ValidationError('Ви неправильно відповіли на контрольне питання')


class SetPasswordForm(FlaskForm):

    """Form to reset user password"""

    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторити пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Встановити пароль')