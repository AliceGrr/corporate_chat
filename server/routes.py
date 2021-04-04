from pathlib import Path

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


def verify_email(email):
    """Проверка email по шаблону."""
    email_regex = re.compile(r'[^@]+@[^@]+\.[^@]+')
    if email_regex.match(email):
        return True
    return False


def check_login(username, err_log):
    """Проверка на корректность логина."""
    if is_field_incorrect(username):
        err_log['msg'] += 'Username ' + is_field_incorrect(username)
        err_log['username_err'] = True


def check_password(psw, err_log):
    """Проверка на корректность пароля."""
    if is_field_incorrect(psw):
        err_log['msg'] += 'Password ' + is_field_incorrect(psw)
        err_log['psw_err'] = True


def check_email(email, err_log):
    """Проверка на корректность почты."""
    if is_field_incorrect(email):
        err_log['msg'] += 'Email ' + is_field_incorrect(email)
        err_log['email_err'] = True
    elif not verify_email(email):
        err_log['msg'] += 'Invalid email\n'
        err_log['email_err'] = True


def verify_user_data(username, psw, email='line@mail.com'):
    """Проверка корректности вводимых данных"""
    err_log = {'psw_err': False, 'username_err': False, 'msg': ''}
    check_login(username, err_log)
    check_password(psw, err_log)
    check_email(email, err_log)
    print(err_log)
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
    chat.update_activity(msg.time_stamp)

    user = Users.find_by_id(request.form['sender'])
    user.update_activity(msg.time_stamp)
    db.session.commit()
    return {'send_time': msg.time_stamp}


@app.route('/corporate_chat/receive_messages', methods=['POST'])
def receive_messages():
    """Получение сообщений одного конкретного пользователя."""
    chat = Chats.find_by_id(request.form['chat_id'])
    limit = int(request.form['limit']) * 10
    msgs = []
    for msg in chat.get_msgs(limit)[::-1]:
        if msg.sender == -1:
            msgs.append(
                {'sender': msg.sender,
                 'msg_text': msg.msg,
                 })
        else:
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
        if chat.is_public:
            last_msg = chat.get_last_msg()
            chats_info.append(
                {'chat_name': chat.get_chat_name(current_user.username),
                 'chat_id': chat.id,
                 'avatar': chat.avatar,
                 'companion_id': 0,
                 'last_msg': last_msg,
                 'last_activity': chat.last_activity,
                 'is_public': chat.is_public,
                 }
            )
        else:
            user = current_user.find_companion(chat.id)
            last_msg = chat.get_last_msg()
            chats_info.append(
                {'chat_name': chat.get_chat_name(current_user.username),
                 'chat_id': chat.id,
                 'avatar': user.avatar,
                 'companion_id': user.id,
                 'last_msg': last_msg,
                 'last_activity': chat.last_activity,
                 'is_public': chat.is_public,
                 }
            )
    return {'chats': chats_info}


@app.route('/corporate_chat/find_user_by_name', methods=['POST'])
def find_user_by_name():
    """Получение списка подходящих по запросу пользователей."""
    current_user = Users.find_by_id(request.form['current_user_id'])
    users = current_user.get_suitable_users(request.form['requested_username'])
    chats = current_user.get_suitable_chats(request.form['requested_username'])

    suitable_chats = []
    for chat in chats:
        if not chat.Chats.is_public:
            suitable_chats.append({'chat_name': chat.Chats.get_chat_name(current_user.username),
                                   'chat_id': chat.Chats.id,
                                   'last_msg': chat.Chats.get_last_msg(),
                                   'avatar': chat.avatar,
                                   'last_activity': chat.Chats.last_activity,
                                   'is_public': chat.Chats.is_public,
                                   'companion_id': -1, })
        elif chat.Chats.is_public and chat.Chats.id not in [chat['chat_id'] for chat in suitable_chats]:
            suitable_chats.append({'chat_name': chat.Chats.get_chat_name(current_user.username),
                                   'chat_id': chat.Chats.id,
                                   'last_msg': chat.Chats.get_last_msg(),
                                   'avatar': chat.Chats.avatar,
                                   'last_activity': chat.Chats.last_activity,
                                   'is_public': chat.Chats.is_public,
                                   'companion_id': -1, })

    suitable_users = []
    for user in users:
        for chat in chats:
            if not chat.Chats.is_public and user.username in chat.Chats.chat_name:
                break
        else:
            suitable_users.append({'user_id': user.id,
                                   'username': user.username,
                                   'avatar': user.avatar,
                                   })

    return {'suitable_users': suitable_users,
            'suitable_chats': suitable_chats}


@app.route('/corporate_chat/start_new_chat', methods=['POST'])
def start_new_chat():
    """Создание чата."""
    current_user = Users.find_by_id(request.form['current_user_id'])
    users_ids_str = request.form['users_ids']
    users_ids = users_ids_str.split(',')
    answer = create_new_chat(current_user=current_user,
                             users_ids=[int(user_id) for user_id in users_ids], )
    return answer


def create_new_chat(users_ids=None, current_user=None):
    """Создание чата."""
    chat_name = ''
    for user_id in users_ids:
        user = Users.find_by_id(user_id)
        chat_name += user.username + ', '

    chat = Chats(chat_name)
    chat.is_public = False if chat.amount_of_users() == 2 else True
    db.session.add(chat)
    db.session.commit()

    for user_id in users_ids:
        user = Users.find_by_id(user_id)
        user.add_to_chat(chat)

    chat.is_public = False if chat.amount_of_users() == 2 else True
    if chat.avatar is None:
        chat.get_chat_avatar(current_user.id)
    db.session.add(chat)
    db.session.commit()
    return {'chat_id': chat.id,
            'chat_name': chat.get_chat_name(current_user.username),
            'is_public': chat.is_public,
            'filename': chat.avatar}


@app.route('/corporate_chat/load_avatar', methods=['POST'])
def load_user_avatar():
    """Отправка аватаров клиенту."""
    user = Users.find_by_id(request.form['user_id'])
    current_chat = Chats.find_by_id(request.form['chat_id'])
    if current_chat is None:
        path = Path('images', user.avatar)
        if not Path.exists(path):
            user.set_avatar()
    else:
        path = Path('images', current_chat.avatar)
        if not Path.exists(path):
            current_chat.get_chat_avatar(user.id)

    return send_file(path)


@app.route('/corporate_chat/users_in_chat', methods=['POST'])
def users_in_chat():
    """Список пользователей чата."""
    current_chat = Chats.find_by_id(request.form['chat_id'])
    users = current_chat.find_users_in_chat()
    if request.form['requested_username']:
        suitable_users = [{
            'user_id': user.id,
            'username': user.username,
            'avatar': user.avatar,
        } for user in users if user.username.lower().startswith(request.form['requested_username'].lower())]
        return {'users': suitable_users}
    return {'users': [{
        'user_id': user.id,
        'username': user.username,
        'avatar': user.avatar,
    } for user in users]}


@app.route('/corporate_chat/users_not_in_chat', methods=['POST'])
def users_not_in_chat():
    """Список пользователей вне чата."""
    current_chat = Chats.find_by_id(request.form['chat_id'])
    users_in = [user.id for user in current_chat.find_users_in_chat()]
    users = Users.find_users_not_in_chat(users_in)
    if request.form['requested_username']:
        suitable_users = [{
            'user_id': user.id,
            'username': user.username,
            'avatar': user.avatar,
        } for user in users if user.username.lower().startswith(request.form['requested_username'].lower())]
        return {'users': suitable_users}
    return {'users': [{
        'user_id': user.id,
        'username': user.username,
        'avatar': user.avatar,
    } for user in users]}


@app.route('/corporate_chat/add_to_chat', methods=['POST'])
def add_to_chat():
    """Добавление пользователя в чат."""
    answer = {}
    current_user = Users.find_by_id(request.form['current_user_id'])
    user_to_add = Users.find_by_id(request.form['user_id'])
    current_chat = Chats.find_by_id(request.form['chat_id'])
    if current_chat.amount_of_users() == 2 and not current_chat.is_public:
        users = [user.id for user in current_chat.find_users_in_chat()]
        users.append(user_to_add.id)

        answer = create_new_chat(users_ids=users,
                                 current_user=current_user)

        current_chat = Chats.find_by_id(answer['chat_id'])
        answer['new'] = True

        msg = Messages(-1, current_chat.id,
                       f"{current_user.username} create chat <{current_chat.get_chat_name(current_user.username)}>")
        db.session.add(msg)
    else:
        user_to_add.add_to_chat(current_chat)
        current_chat.chat_name += user_to_add.username + ', '
        answer['chat_name'] = current_chat.chat_name
        answer['new'] = False
    # add information msg
    msg = Messages(-1, current_chat.id, f'{current_user.username} add {user_to_add.username}')
    current_chat.last_activity = msg.time_stamp

    db.session.add(msg)
    db.session.commit()

    answer['filename'] = current_chat.get_chat_avatar(current_user.id)
    answer['msg'] = msg.msg
    return answer


@app.route('/corporate_chat/remove_from_chat', methods=['POST'])
def delete_from_chat():
    """Удаление пользователя из чата."""
    answer = {'del_chat': False, 'leave': False}
    current_user = Users.find_by_id(request.form['current_user_id'])
    user_to_delete = Users.find_by_id(request.form['user_id'])
    current_chat = Chats.find_by_id(request.form['chat_id'])
    if current_chat.amount_of_users() == 2:
        current_chat.delete_chat()
        answer['del_chat'] = True
    else:
        # add information msg
        if current_user.id == user_to_delete.id:
            msg = Messages(-1, current_chat.id, f'{current_user.username} leave chat')
            answer['leave'] = True
        else:
            msg = Messages(-1, current_chat.id, f'{current_user.username} delete {user_to_delete.username}')

        user_to_delete.remove_from_chat(current_chat)
        current_chat.chat_name = current_chat.chat_name.replace(user_to_delete.username + ', ', '')

        current_chat.last_activity = msg.time_stamp

        db.session.add(msg)
        db.session.commit()
        answer['msg'] = msg.msg
    answer['filename'] = current_chat.get_chat_avatar(current_user.id)
    return answer
