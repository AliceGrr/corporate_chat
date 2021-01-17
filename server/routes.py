from . import app, db
from flask import request
from .models import Users, Messages
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import exc


def check_data(username, psw):
    """Проверка корректности вводимых данных"""
    err_msg = ''
    err_log = {'psw_err': False, 'username_err': False}
    if username == '':
        err_msg += 'Username is required\n'
        err_log['username_err'] = True
    if username.find(' ') != -1:
        err_msg += "Username can't contain whitespaces\n"
        err_log['username_err'] = True
    if psw == '':
        err_msg += 'Password is required\n'
        err_log['psw_err'] = True
    if psw.find(' ') != -1:
        err_msg += "Password can't contain whitespaces\n"
        err_log['psw_err'] = True
    err_log['msg'] = err_msg
    print(err_log)
    return err_log


@app.route('/corporate_chat', methods=['POST'])
def login():
    """Вход пользователя."""
    if request.method == 'POST':
        err_log = check_data(request.form['username'], request.form['psw'])
        if err_log['msg']:
            return err_log
        user = db.session.query(Users).get(request.form['username'])
        if user is None:
            err_log['msg'] = 'no such user'
            return err_log
        elif check_password_hash(user.psw, request.form['psw']):
            pass


@app.route('/corporate_chat/register', methods=['POST'])
def register():
    """Регистрация пользователей."""
    if request.method == 'POST':
        try:
            user = Users(request.form['username'], generate_password_hash(request.form['psw']))
            db.session.add(user)
            db.session.commit()
        except exc.IntegrityError:
            return {'msg': 'user with this name exists'}


@app.route('/corporate_chat/send_message', methods=['POST'])
def send_message():
    """Отправка сообщений от пользователя к пользователю."""
    if request.method == 'POST':
        msg = Messages(request.form['from_user'], request.form['to_user'], request.form['msg'])
        db.session.add(msg)
        db.session.commit()


@app.route('/corporate_chat/receive_message')
def receive_message():
    """Получение сообщений одного конкретного пользователя."""
    # TODO: write a receive func
    pass
