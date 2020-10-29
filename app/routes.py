from flask import render_template, request, redirect

from app import app
from app.forms import Registration, Login


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/login')
def login():
    forms = Login()
    if forms.validate_on_submit() and request.method == 'POST':
        # Проверка БД
        pass
    return render_template('login.html', forms=forms)


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    forms = Registration()
    if request.method == 'POST':
        # Регистрация в БД
        pass

    return render_template('registration.html', forms=forms)