from . import app, db
from flask import request
from .models import Users, Messages, Chats
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
        user = Users.query.filter(Users.username == request.form['username']).first()
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
        msg = Messages(request.form['from_user'], request.form['to_chat'], request.form['msg'])
        db.session.add(msg)
        db.session.commit()
        return 'success'


@app.route('/corporate_chat/receive_messages', methods=['POST'])
def receive_messages():
    """Получение сообщений одного конкретного пользователя."""
    chat = Chats.query.filter(Chats.id == request.form['chat_id']).first()
    msgs = []
    for msg in chat.messages:
        msgs.append(
            {'msg_text': msg.msg,
             'send_time': msg.time_stamp}
        )

    return {'msgs': msgs}


@app.route('/corporate_chat/receive_user_chats', methods=['POST'])
def receive_user_chats():
    """Получение списка всех чатов пользователя."""
    chats = {str(chat): {'chat_id': chat.id, 'last_msg': str(chat)} for chat in Chats.query.order_by(Chats.users.ilike(request.form['username'])).all()}
    return chats


@app.route('/corporate_chat/find_user_by_name', methods=['POST'])
def find_user_by_name():
    """Получение списка подходящих по запросу пользователей."""
    users = [str(user) for user in
             Users.query.filter(Users.username.startswith(request.form['example_username'])).all()]
    return {'users': users}


@app.route('/corporate_chat/start_new_chat', methods=['POST'])
def start_new_chat():
    """Создание чата."""
    chat = Chats(request.form['users'])
    db.session.add(chat)
    db.session.commit()
    return {'chat_id': chat.id, 'users': chat.users}
