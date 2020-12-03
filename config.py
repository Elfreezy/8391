import os
from os import environ
from dotenv import load_dotenv


load_dotenv('.env')
basedir = os.path.dirname(__file__)


class Config(object):
    DEBUG = environ.get('DEBUG') or True
    SECRET_KEY = environ.get('SECRET_KEY') or 'secret_key'
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SERVER = environ.get('SERVER') or '127.0.0.1'
    MAIL_PORT = int(environ.get('MAIL_PORT') or 25)
    MAIL_SERVER = environ.get('MAIL_SERVER')
    ADMINS = ['alicapolice@yandex.ru']