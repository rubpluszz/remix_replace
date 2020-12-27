import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    
    """I will use this class in order to save a configuration data"""
    

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')#the path to the file with our database.
    SQLALCHEMY_TRACK_MODIFICATIONS = False #Відключаєм функцію сигналізації))
    POSTS_PER_PAGE = 10
    LANGUAGES = ['ua', 'en', 'pl', 'ru']

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['ruberoidzz@gmail.com']
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')