from flask import render_template

from app import app
from app.models import User


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/profile/<id>')
def profile(id):
    user = User.query.filter_by(id=id).first_or_404()
    posts = user.posts
    return render_template('profile.html', user=user, posts=posts)
