import os
from os import environ
from dotenv import load_dotenv


load_dotenv('.env')
basedir = os.path.dirname(__file__)


class Config(object):
    DEBUG = environ.get('DEBUG') or True
    SECRET_KEY = environ.get('SECRET_KEY') or 'secret_key'
