from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'


from app.auth import auth
from app.posts import posts
app.register_blueprint(auth)
app.register_blueprint(posts)


# Отправка ошибки на почту
if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    mail_handler = SMTPHandler(mailhost=(app.config['SERVER'], app.config['MAIL_PORT']),
                               fromaddr=app.config['MAIL_SERVER'],
                               toaddrs=app.config['ADMINS'],
                               subject='Your App Failed')
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

from app import models
from app import routes
from app.models import User, Post, Tag


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'app': app, 'User': User, 'Post': Post, 'Tag': Tag}