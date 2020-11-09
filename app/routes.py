from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, logout_user, login_user
from werkzeug.urls import url_parse

from app import app, db
from app.forms import Registration, Login
from app.models import User


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
    return render_template('profile.html', user=user)
