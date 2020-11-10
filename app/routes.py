from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, logout_user, login_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime

from app import app, db
from app.forms import Registration, Login, PostForm
from app.models import User, Post


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    forms = Login()
    if forms.validate_on_submit() and request.method == 'POST':
        # Проверка БД
        user = User.query.filter_by(login=forms.login.data).first()
        if user is None or not user.check_password_hash(forms.password.data):
            flash('Invalid login or password')
            return redirect(url_for('index'))
        login_user(user, remember=forms.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', forms=forms)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    forms = Registration()
    if forms.validate_on_submit() and request.method == 'POST':
        # Регистрация в БД
        user = User(login=forms.login.data, email=forms.email.data)
        user.set_password_hash(forms.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration is success')
        return redirect(url_for('login'))
    return render_template('registration.html', forms=forms)


@app.route('/profile/<id>')
def profile(id):
    user = User.query.filter_by(id=id).first_or_404()
    posts = user.posts
    return render_template('profile.html', user=user, posts=posts)


@app.route('/create_post', methods=['POST', 'GET'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit() and request.method == 'POST':
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts'))
    return render_template('create_post.html', form=form)


@app.route('/posts')
@login_required
def posts():
    posts = Post.query.all()
    return render_template('posts.html', posts=posts)


@app.route('/edit_post/<slug>', methods=['POST', 'GET'])
def edit_post(slug):
    id = request.args.get('id')
    post = Post.query.filter_by(id=id).first_or_404()
    form = PostForm(formdata=request.form, obj=post)
    if form.validate_on_submit() and request.method == 'POST':
        post.title, post.body, post.slug = form.title.data, form.body.data, Post.slugy(form.title.data)
        post.created = datetime.utcnow()
        db.session.add(post)
        db.session.commit()
        flash('Success')
        return redirect(url_for('post', slug=post.slug, id=post.id))
    return render_template('edit_post.html', form=form)


@app.route('/delete/<slug>', methods=['POST', 'GET'])
def delete_post(slug):
    id = request.args.get('id')
    if id and request.method == 'GET':
        print('-----')
        post = Post.query.filter_by(id=id).first()
        db.session.delete(post)
        db.session.commit()
        flash('Delete is success')
        return redirect(url_for('profile', id=current_user.id))
    return redirect(url_for('index'))


@app.route('/post/<slug>')
@login_required
def post(slug):
    id = request.args.get('id')
    post = Post.query.filter_by(id=id).first()
    return render_template('post.html', post=post)