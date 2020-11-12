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


from app import models
from app import routes
from app.models import User, Post


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'app': app, 'User': User, 'Post': Post}