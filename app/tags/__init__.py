from flask import Blueprint


tags = Blueprint('tags', __name__, template_folder='templates', url_prefix='/tags')


from app.tags import routes