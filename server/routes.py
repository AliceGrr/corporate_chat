from . import app, db
from flask import request
from .models import Users, Messages
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import exc


@app.route('/corporate_chat', methods=['POST'])
def login():
    """Вход пользователя."""
    if request.method == 'POST':
        user = db.session.query(Users).get(request.form['username'])
        if user is None:
            return 'no such user'
        elif check_password_hash(user.psw, request.form['psw']):
            return 'you are welcome'
        return 'success'


def check_register_data(username, psw):
    """Проверка корректности вводимых данных"""
    if username == '':
        return 'Username is required'
    elif psw == '':
        return 'Password is required'
    elif username.startswith(' '):
        return "Username can't start with whitespace"
    elif psw.startswith(' '):
        return "Password can't start with whitespace"
    return True


@app.route('/corporate_chat/register', methods=['POST'])
def register():
    """Регистрация пользователей."""
    if request.method == 'POST':
        if check_register_data(request.form['username'], request.form['psw']) is True:
            try:
                user = Users(request.form['username'], generate_password_hash(request.form['psw']))
                db.session.add(user)
                db.session.commit()
            except exc.IntegrityError:
                return 'user with this name exist'
            return 'success!'
        return 'error'


@app.route('/corporate_chat/send_message', methods=['POST'])
def send_message():
    """Отправка сообщений от пользователя к пользователю."""
    if request.method == 'POST':
        receiver = db.session.query(Users).get(request.form['to_user'])
        if receiver is None:
            print('no such user')
        else:
            msg = Messages(request.form['from_user'], request.form['to_user'], request.form['msg'])
            db.session.add(msg)
            db.session.commit()
            return 'success!'


@app.route('/corporate_chat/receive_message')
def receive_message():
    """Получение сообщений одного конкретного пользователя."""
    # TODO: write a receive func
    pass


@app.route('/test_reg')
def test1():
    requests.post('http://127.0.0.1:5000/corporate_chat/register',
                  data={'username': 'username', 'psw': 'psw'})
    return 'success'
