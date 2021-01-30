from . import app, db
from flask import request
from .models import Users, Messages
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import exc


def is_field_empty(data):
    if data == '':
        return 'is required\n'
    return False


def is_field_contains_whitespaces(data):
    if data.find(' ') != -1:
        return "contain whitespaces\n"
    return False


def is_field_incorrect(data):
    return is_field_empty(data) or is_field_contains_whitespaces(data)


def verify_user_data(username, psw):
    """Проверка корректности вводимых данных"""
    err_log = {'psw_err': False, 'username_err': False, 'msg': ''}
    if is_field_incorrect(username):
        err_log['msg'] += 'Username ' + is_field_incorrect(username)
        err_log['username_err'] = True
    if is_field_incorrect(psw):
        err_log['msg'] += 'Password ' + is_field_incorrect(psw)
        err_log['psw_err'] = True
    return err_log


@app.route('/corporate_chat', methods=['POST'])
def login():
    """Вход пользователя."""
    if request.method == 'POST':
        err_log = verify_user_data(request.form['username'], request.form['psw'])
        if err_log['msg']:
            return err_log
        user = Users.query.filter_by(username=request.form['username']).first()
        if user is None:
            err_log['msg'] = 'no such user'
            return err_log
        elif check_password_hash(user.psw, request.form['psw']):
            return err_log
        else:
            err_log['msg'] = 'incorrect psw'
            return err_log


@app.route('/corporate_chat/register', methods=['POST'])
def register():
    """Регистрация пользователей."""
    if request.method == 'POST':
        err_log = verify_user_data(request.form['username'], request.form['psw'])
        if err_log['msg']:
            return err_log
        try:
            user = Users(request.form['username'], generate_password_hash(request.form['psw']))
            db.session.add(user)
            db.session.commit()
            return err_log
        except exc.IntegrityError:
            err_log['msg'] = 'user with this name exists'
            return err_log


@app.route('/corporate_chat/send_message', methods=['POST'])
def send_message():
    """Отправка сообщений от пользователя к пользователю."""
    if request.method == 'POST':
        msg = Messages(request.form['from_user'], request.form['to_user'], request.form['msg'])
        db.session.add(msg)
        db.session.commit()
        return 'success'


@app.route('/corporate_chat/receive_message')
def receive_message():
    """Получение сообщений одного конкретного пользователя."""
    # TODO: write a receive func
    pass


@app.route('/corporate_chat/receive_user_list')
def receive_user_list():
    """Получение списка всех пользователей."""
    users = [str(user) for user in Users.query.order_by(Users.username).all()]
    return {'users': users}


@app.route('/corporate_chat/find_user_by_name', methods=['POST'])
def find_user_by_name():
    """Получение списка подходящих по запросу пользователей."""
    users = [str(user) for user in Users.query.filter(Users.username.startswith(request.form['example_username'])).all()]
    return {'users': users}
