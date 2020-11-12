from flask import Blueprint


posts = Blueprint('posts', __name__, template_folder='templates', url_prefix='/posts')


from app.posts import routes