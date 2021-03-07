from . import app, db
from flask import request
from .models import Users, Messages, Chats, usersInChats
from sqlalchemy import exc, and_


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


def verify_user_data(username, psw, email='line'):
    """Проверка корректности вводимых данных"""
    err_log = {'psw_err': False, 'username_err': False, 'msg': ''}
    if is_field_incorrect(username):
        err_log['msg'] += 'Username ' + is_field_incorrect(username)
        err_log['username_err'] = True
    if is_field_incorrect(email):
        err_log['msg'] += 'Email ' + is_field_incorrect(email)
        err_log['email_err'] = True
    if is_field_incorrect(psw):
        err_log['msg'] += 'Password ' + is_field_incorrect(psw)
        err_log['psw_err'] = True
    return err_log


@app.route('/corporate_chat', methods=['POST'])
def login():
    """Вход пользователя."""
    err_log = verify_user_data(request.form['username'], request.form['psw'])
    if err_log['msg']:
        return err_log
    user = Users.find_by_name(request.form['username'])
    if user is None:
        err_log['msg'] = 'no such user'
        return err_log
    elif user.check_password(request.form['psw']):
        err_log['user_id'] = user.id
        return err_log
    else:
        err_log['msg'] = 'incorrect psw'
        return err_log


@app.route('/corporate_chat/register', methods=['POST'])
def register():
    """Регистрация пользователей."""
    err_log = {'email_err': False}
    err_log.update(verify_user_data(request.form['username'], request.form['psw'], request.form['email']))
    print(err_log)
    if err_log['msg']:
        return err_log
    try:
        user = Users(request.form['username'], request.form['email'])
        user.set_password(request.form['psw'])
        db.session.add(user)
        db.session.commit()
        return err_log
    except exc.IntegrityError:
        err_log['msg'] = 'user with this name exists'
        return err_log


@app.route('/corporate_chat/send_message', methods=['POST'])
def send_message():
    """Отправка сообщений от пользователя к пользователю."""
    msg = Messages(request.form['sender'], request.form['to_chat'], request.form['msg'])
    db.session.add(msg)

    chat = Chats.find_by_id(request.form['to_chat'])
    chat.set_last_ativity(msg.time_stamp)
    db.session.commit()
    return {'send_time': msg.time_stamp}


@app.route('/corporate_chat/receive_messages', methods=['POST'])
def receive_messages():
    """Получение сообщений одного конкретного пользователя."""
    chat = Chats.find_by_id(request.form['chat_id'])
    msgs = [
        {'sender': msg.sender,
         'msg_text': msg.msg,
         'send_time': msg.time_stamp
         }
        for msg in chat.messages
    ]
    return {'msgs': msgs}


@app.route('/corporate_chat/receive_user_chats', methods=['POST'])
def receive_user_chats():
    """Получение списка всех чатов пользователя."""
    user = Users.find_by_name(request.form['username'])
    user_chats = user.find_user_chats()
    chats_info = [
        {'chat_name': chat.chat_name,
         'chat_id': chat.id,
         'last_msg': chat.last_activity,
         }
        for chat in user_chats
    ]
    print(chats_info)
    return {'chats': chats_info}


@app.route('/corporate_chat/find_user_by_name', methods=['POST'])
def find_user_by_name():
    """Получение списка подходящих по запросу пользователей."""
    user = Users.find_by_id(request.form['current_user_id'])
    suitable_users = Users.suitable_users(request.form['example_username'])
    return {'suitable_users': {user.id: user.username for user in suitable_users}}

    # print(user_chats, suitable_users)
    # chats_info = []
    # for user_id, chat_id in user_chats.items():
    #     if user_id in suitable_users:
    #         del suitable_users[user_id]
    #
    #         chats_info += [
    #             {'chat_name': chat.chat.chat_name,
    #              'chat_id': chat.chat.id,
    #              'last_msg': chat.chat.last_activity,
    #              }
    #             for chat in UserChats.query.filter
    #             (and_(UserChats.chat_ids == chat_id,
    #                   UserChats.user_ids == user_id))
    #         ]
    #
    # chats = sorted(chats_info, key=lambda x: x['last_msg'], reverse=True)
    # print(chats, suitable_users)
    # return {'suitable_chats': chats,
    #         'suitable_users': suitable_users}


@app.route('/corporate_chat/start_new_chat', methods=['POST'])
def start_new_chat():
    """Создание чата."""
    chat = Chats(request.form['users'])
    db.session.add(chat)
    db.session.commit()

    users_ids = list(request.form['users_ids'])
    for user_id in users_ids:
        user = Users.find_by_id(int(user_id))
        user.add_to_chat(chat)
        db.session.commit()

    return {'chat_id': chat.id, 'users': chat.chat_name}
