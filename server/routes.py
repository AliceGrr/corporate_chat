import os
from . import app, db
from flask import request, send_file
from .models import Users, Messages, Chats
from sqlalchemy import exc
import re


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


def verify_email(email, err_log):
    """Проверка email по шаблону."""
    email_regex = re.compile(r'[^@]+@[^@]+\.[^@]+')
    if not email_regex.match(email):
        err_log['msg'] += 'Invalid email\n'
        err_log['email_err'] = True
        return False
    return True


def verify_user_data(username, psw, email='line@mail.com'):
    """Проверка корректности вводимых данных"""
    err_log = {'psw_err': False, 'username_err': False, 'msg': ''}
    if is_field_incorrect(username):
        err_log['msg'] += 'Username ' + is_field_incorrect(username)
        err_log['username_err'] = True
    if is_field_incorrect(email):
        err_log['msg'] += 'Email ' + is_field_incorrect(email)
        err_log['email_err'] = True
    elif verify_email(email, err_log):
        pass
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
        err_log['msg'] = 'No such user'
        return err_log
    elif user.check_password(request.form['psw']):
        err_log['user_id'] = user.id
        err_log['avatar'] = user.avatar
        return err_log
    else:
        err_log['msg'] = 'Incorrect psw'
        return err_log


@app.route('/corporate_chat/register', methods=['POST'])
def register():
    """Регистрация пользователей."""
    err_log = {'email_err': False}
    err_log.update(verify_user_data(request.form['username'], request.form['psw'], request.form['email']))
    if err_log['msg']:
        return err_log
    try:
        user = Users(request.form['username'], request.form['email'])
        user.set_password(request.form['psw'])
        db.session.add(user)
        db.session.commit()
        return err_log
    except exc.IntegrityError:
        err_log['msg'] = 'User with this name exists'
        return err_log


@app.route('/corporate_chat/send_message', methods=['POST'])
def send_message():
    """Отправка сообщений от пользователя к пользователю."""
    msg = Messages(request.form['sender'], request.form['to_chat'], request.form['msg'])
    db.session.add(msg)

    chat = Chats.find_by_id(request.form['to_chat'])
    chat.last_activity = msg.time_stamp

    user = Users.find_by_id(request.form['sender'])
    user.last_activity = msg.time_stamp
    db.session.commit()
    return {'send_time': msg.time_stamp}


@app.route('/corporate_chat/receive_messages', methods=['POST'])
def receive_messages():
    """Получение сообщений одного конкретного пользователя."""
    chat = Chats.find_by_id(request.form['chat_id'])
    msgs = []
    for msg in chat.messages:
        user = Users.find_by_id(msg.sender)
        msgs.append(
            {'sender': msg.sender,
             'sender_name': user.username,
             'msg_text': msg.msg,
             'send_time': msg.time_stamp,
             'avatar': user.avatar
             })
    return {'msgs': msgs}


@app.route('/corporate_chat/receive_user_chats', methods=['POST'])
def receive_user_chats():
    """Получение списка всех чатов пользователя."""
    current_user = Users.find_by_name(request.form['username'])
    user_chats = current_user.find_user_chats()

    chats_info = []
    for chat in user_chats:
        amount_of_users = chat.amount_of_users()
        if amount_of_users > 2:
            pass
        else:
            user = current_user.find_companion(chat.id)
            last_msg = chat.get_last_msg()[:30]
            last_msg = last_msg.replace("\n", "")
            chats_info.append(
                {'chat_name': chat.chat_name,
                 'chat_id': chat.id,
                 'avatar': user.avatar,
                 'companion_id': user.id,
                 'last_msg': last_msg,
                 'last_activity': chat.last_activity,
                 'amount_of_users': amount_of_users,
                 }
            )
    return {'chats': chats_info}


@app.route('/corporate_chat/find_user_by_name', methods=['POST'])
def find_user_by_name():
    """Получение списка подходящих по запросу пользователей."""
    current_user = Users.find_by_id(request.form['current_user_id'])
    users = current_user.get_suitable_users(request.form['requested_username'])
    chats = current_user.get_suitable_chats(request.form['requested_username'])

    suitable_chats = [{
        'chat_name': chat.Chats.chat_name,
        'chat_id': chat.Chats.id,
        'last_msg': chat.Chats.get_last_msg(),
        'avatar': chat.avatar,
        'last_activity': chat.Chats.last_activity,
        'amount_of_users': chat.Chats.amount_of_users(),
    } for chat in chats]
    suitable_users = [{'user_id': user.id,
                       'username': user.username,
                       'avatar': user.avatar,
                       } for user in users
                      if user.username not in [chat.username for chat in chats]]

    return {'suitable_users': suitable_users,
            'suitable_chats': suitable_chats}


@app.route('/corporate_chat/start_new_chat', methods=['POST'])
def start_new_chat(owner=None, users_ids=None):
    """Создание чата."""
    owner = request.form['owner']
    users_ids = request.form['users_ids']

    chat_name = ''
    for user_id in users_ids:
        user = Users.find_by_id(int(user_id))
        chat_name += user.username + ', '

    chat = Chats(chat_name)
    db.session.add(chat)
    db.session.commit()

    for user_id in users_ids:
        user = Users.find_by_id(int(user_id))
        user.add_to_chat(chat)
        db.session.commit()

    return {'chat_id': chat.id,
            'users': chat.chat_name,
            'amount_of_users': chat.amount_of_users(), }


@app.route('/corporate_chat/load_avatar', methods=['POST'])
def load_avatar():
    """Отправка аватаров клиенту."""
    user = Users.find_by_id(request.form['id'])
    path = os.getcwd() + app.config['UPLOAD_FOLDER']
    print(path)
    return send_file(f'{path}{user.avatar}')


@app.route('/corporate_chat/users_in_chat', methods=['POST'])
def users_in_chat():
    """Список пользователей чата."""
    users = Users.find_users_in_chat(request.form['chat_id'])
    owner = Chats.find_owner(request.form['chat_id'])
    return {'users': [{
        'user_id': user.id,
        'username': user.username,
        'avatar': user.avatar,
    } for user in users],
        'owner': owner.owner}


@app.route('/corporate_chat/users_not_in_chat', methods=['POST'])
def users_not_in_chat():
    """Список пользователей вне чата."""
    users_in = [user.id for user in Users.find_users_in_chat(request.form['chat_id'])]
    users = Users.find_users_not_in_chat(users_in)
    print(users)
    return {'users': [{
        'user_id': user.id,
        'username': user.username,
        'avatar': user.avatar,
    } for user in users]}


@app.route('/corporate_chat/add_to_chat', methods=['POST'])
def add_to_chat():
    """Добавление пользователя в чат."""
    user_to_add = Users.find_by_id(request.form['user_id'])
    current_chat = Chats.find_by_id(request.form['chat_id'])
    if current_chat.amount_of_users == 2:
        users = Users.find_users_in_chat(request.form['chat_id'])
        start_new_chat()
    user_to_add.add_to_chat(current_chat)
    return {'success'}


@app.route('/corporate_chat/remove_from_chat', methods=['POST'])
def delete_from_chat():
    """Удаление пользователя из чата."""
    user_to_delete = Users.find_by_id(request.form['user_id'])
    current_chat = Chats.find_by_id(request.form['chat_id'])
    if current_chat.amount_of_users == 2:
        pass
    user_to_delete.remove_from_chat(current_chat)
    return {'success'}
