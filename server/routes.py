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


def verify_user_data(psw, username='user', email='line@mail.com'):
    """Проверка корректности вводимых данных"""
    err_log = {'psw_err': False, 'username_err': False, 'msg': ''}
    check_login(username, err_log)
    check_password(psw, err_log)
    check_email(email, err_log)
    return err_log


@app.route('/corporate_chat', methods=['POST'])
def login():
    """Вход пользователя."""
    if verify_email(request.form['username']):
        err_log, user = login_by_mail()
    else:
        err_log, user = login_by_name()
    if err_log['msg']:
        return err_log
    if user is None:
        err_log['msg'] = 'No such user'
        return err_log
    elif user.check_password(request.form['psw']):
        err_log.update({'user_id': user.id,
                        'username': user.username,
                        'avatar': user.avatar,
                        })
        user.update_activity()
        db.session.commit()
        return err_log
    else:
        err_log['msg'] = 'Incorrect psw'
        return err_log


def login_by_name():
    err_log = verify_user_data(username=request.form['username'],
                               psw=request.form['psw'])
    if err_log['msg']:
        return err_log, None
    user = Users.find_by_name(request.form['username'])
    return err_log, user


def login_by_mail():
    err_log = verify_user_data(email=request.form['username'],
                               psw=request.form['psw'])
    if err_log['msg']:
        return err_log, None
    user = Users.find_by_mail(request.form['username'])
    return err_log, user


@app.route('/corporate_chat/register', methods=['POST'])
def register():
    """Регистрация пользователей."""
    err_log = verify_user_data(username=request.form['username'],
                               psw=request.form['psw'],
                               email=request.form['email'])
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
    chat.update_activity()

    user = Users.find_by_id(request.form['sender'])
    user.update_activity()
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


@app.route('/corporate_chat/receive_current_chat_info', methods=['POST'])
def receive_current_chat_info():
    current_user = Users.find_by_id(request.form['current_user_id'])
    current_chat = Chats.find_by_id(request.form['chat_id'])
    if current_chat.is_public:
        answer = {'chat_info': current_chat.amount_of_users(),
                  'is_public': current_chat.is_public}
    else:
        companion = current_user.find_companion(current_chat.id)
        answer = {'chat_info': companion.last_activity,
                  'is_public': current_chat.is_public}
    return answer


@app.route('/corporate_chat/receive_user_chats', methods=['POST'])
def receive_user_chats():
    """Получение списка всех чатов пользователя."""
    current_user = Users.find_by_name(request.form['username'])
    user_chats = current_user.find_user_chats()

    chats_info = []
    for chat in user_chats:
        if chat.is_public:
            chats_info.append(public_chat_info(chat, current_user))
        else:
            companion = current_user.find_companion(chat.id)
            chats_info.append(private_chat_info(chat, current_user, companion))
    return {'chats': chats_info}


def private_chat_info(chat, current_user, companion):
    """Словарь с информацией о личном чате."""
    return {'chat_name': chat.get_chat_name(current_user.username),
            'chat_id': chat.id,
            'avatar': companion.avatar_name,
            'companion_id': companion.id,
            'last_msg': chat.get_last_msg(),
            'last_activity': chat.last_activity,
            'is_public': chat.is_public,
            'chat_info': companion.last_activity,
            }


def public_chat_info(chat, current_user):
    """Словарь с информацией о публичном чате."""
    return {'chat_name': chat.get_chat_name(current_user.username),
            'chat_id': chat.id,
            'avatar': chat.avatar,
            'companion_id': 0,
            'last_msg': chat.get_last_msg(),
            'last_activity': chat.last_activity,
            'is_public': chat.is_public,
            'chat_info': chat.amount_of_users()
            }


def user_info(user):
    """Словарь с информацией о пользователе."""
    return {'user_id': user.id,
            'username': user.username,
            'avatar': user.avatar_name,
            }


@app.route('/corporate_chat/find_user_by_name', methods=['POST'])
def find_user_by_name():
    """Получение списка подходящих по запросу пользователей."""
    current_user = Users.find_by_id(request.form['current_user_id'])
    users = current_user.get_suitable_users(request.form['requested_username'])
    chats = current_user.get_suitable_chats(request.form['requested_username'])

    suitable_chats = select_suitable_chats(chats, current_user)
    suitable_users = select_suitable_users(users, chats)

    current_user.update_activity()
    return {'suitable_users': suitable_users,
            'suitable_chats': suitable_chats}


def select_suitable_users(users, chats):
    """Выбирает подходящих запросу пользователей из списка."""
    suitable_users = []
    if len(chats) > 0:
        private_chats = [chat for chat in chats if not chat.Chats.is_public]
        for user in users:
            if any([user.username in chat.Chats.chat_name for chat in private_chats]):
                continue
            else:
                suitable_users.append({
                    'user_id': user.id,
                    'username': user.username,
                    'avatar': user.avatar_name,
                    'chat_info': user.last_activity,
                })
    else:
        for user in users:
            suitable_users.append({
                'user_id': user.id,
                'username': user.username,
                'avatar': user.avatar_name,
                'chat_info': user.last_activity,
            })
    return suitable_users


def select_suitable_chats(chats, current_user):
    """Выбирает подходящие запросу чаты из списка"""
    suitable_chats = []
    for chat in chats:
        if not chat.Chats.is_public:
            companion = current_user.find_companion(chat.Chats.id)
            suitable_chats.append(private_chat_info(chat.Chats, current_user, companion))
        elif chat.Chats.is_public and chat.Chats.id not in [chat['chat_id'] for chat in suitable_chats]:
            suitable_chats.append(public_chat_info(chat.Chats, current_user))
    return suitable_chats


@app.route('/corporate_chat/start_new_chat', methods=['POST'])
def start_new_chat():
    """Создание чата."""
    current_user = Users.find_by_id(request.form['current_user_id'])
    users_ids_str = request.form['users_ids']
    users_ids = users_ids_str.split(',')
    answer = create_new_chat(current_user=current_user,
                             users_ids=[int(user_id) for user_id in users_ids], )
    current_user.update_activity()
    return answer


def create_new_chat(users_ids=None, current_user=None):
    """Создание чата."""
    chat_name = ''
    for user_id in users_ids:
        user = Users.find_by_id(user_id)
        chat_name += user.username + ', '

    chat = Chats(chat_name)
    db.session.add(chat)
    db.session.commit()

    for user_id in users_ids:
        user = Users.find_by_id(user_id)
        user.add_to_chat(chat)

    chat.is_public = False if chat.amount_of_users() == 2 else True
    if chat.is_public:
        chat.get_chat_avatar(current_user)
    db.session.add(chat)
    db.session.commit()
    return {'chat_id': chat.id,
            'chat_name': chat.get_chat_name(current_user.username),
            'is_public': chat.is_public,
            'filename': chat.avatar}


@app.route('/corporate_chat/load_avatar', methods=['POST'])
def load_avatar():
    """Отправка аватаров клиенту."""
    user = Users.find_by_id(request.form['user_id'])
    current_chat = Chats.find_by_id(request.form['chat_id'])
    if current_chat is None:
        if user.avatar_name is None:
            user.set_avatar()
        path = Path('images', user.avatar_name)
        if not Path.exists(path):
            user.set_avatar()
    else:
        path = Path('images', current_chat.avatar)
        if not Path.exists(path):
            current_chat.get_chat_avatar(user)

    return send_file(path)


@app.route('/corporate_chat/users_in_chat', methods=['POST'])
def users_in_chat():
    """Список пользователей чата."""
    current_chat = Chats.find_by_id(request.form['chat_id'])
    users = current_chat.find_users_in_chat()
    return {'users': [user_info(user) for user in users]}


@app.route('/corporate_chat/users_in_chat_by_name', methods=['POST'])
def users_in_chat_by_name():
    """Список пользователей чата по запрошенному имени."""
    current_chat = Chats.find_by_id(request.form['chat_id'])
    users = current_chat.find_users_in_chat().filter(
        Users.username.startswith(request.form['requested_username'].lower()))
    return {'users': [user_info(user) for user in users]}


@app.route('/corporate_chat/users_not_in_chat_by_name', methods=['POST'])
def users_not_in_chat_by_name():
    """Список пользователей вне чата по запрошенному имени."""
    current_chat = Chats.find_by_id(request.form['chat_id'])
    users_in = [user.id for user in current_chat.find_users_in_chat()]
    users = Users.find_users_not_in_chat(users_in).filter(
        Users.username.startswith(request.form['requested_username'].lower()))
    return {'users': [user_info(user) for user in users]}


@app.route('/corporate_chat/users_not_in_chat', methods=['POST'])
def users_not_in_chat():
    """Список пользователей вне чата."""
    current_chat = Chats.find_by_id(request.form['chat_id'])
    users_in = [user.id for user in current_chat.find_users_in_chat()]
    users = Users.find_users_not_in_chat(users_in)
    return {'users': [user_info(user) for user in users]}


@app.route('/corporate_chat/add_to_chat', methods=['POST'])
def add_to_chat():
    """Добавление пользователя в чат."""
    answer = {'new': False}
    msg_text = ''

    current_user = Users.find_by_id(request.form['current_user_id'])
    user_to_add = Users.find_by_id(request.form['user_id'])
    current_chat = Chats.find_by_id(request.form['chat_id'])

    if current_chat.amount_of_users() == 2 and not current_chat.is_public:
        users_ids = [user.id for user in current_chat.find_users_in_chat()]
        users_ids.append(user_to_add.id)
        answer = create_new_chat(users_ids=users_ids,
                                 current_user=current_user)

        current_chat = Chats.find_by_id(answer['chat_id'])
        answer['new'] = True
        msg_text += f"{current_user.username} create chat <{current_chat.get_chat_name(current_user.username)}>. "
    else:
        user_to_add.add_to_chat(current_chat)
        current_chat.chat_name += user_to_add.username + ', '
    msg_text += f'{current_user.username} add {user_to_add.username}'

    add_inf_msg(current_chat, msg_text)
    answer.update(add_chat_info_to_answer(current_chat=current_chat,
                                          current_user=current_user,
                                          msg_text=msg_text))
    current_user.update_activity()
    return answer


def add_inf_msg(current_chat, text):
    """Добавление информационного сообщения."""
    msg = Messages(-1, current_chat.id, text)
    current_chat.last_activity = msg.time_stamp

    db.session.add(msg)
    db.session.commit()
    return msg.msg


def add_chat_info_to_answer(current_chat, current_user, msg_text):
    """Добавление информации о чате в словарь с ответом."""
    return {'chat_name': current_chat.chat_name,
            'msg': msg_text,
            'filename': current_chat.get_chat_avatar(current_user)}


@app.route('/corporate_chat/remove_from_chat', methods=['POST'])
def delete_from_chat():
    """Удаление пользователя из чата."""
    current_user = Users.find_by_id(request.form['current_user_id'])
    user_to_delete = Users.find_by_id(request.form['user_id'])
    current_chat = Chats.find_by_id(request.form['chat_id'])

    answer = {'del_chat': False, 'leave': False, 'filename': current_chat.avatar}
    msg_text = ''

    if current_chat.amount_of_users() == 2:
        current_chat.delete_chat()
        answer['del_chat'] = True
    else:
        if current_user.id == user_to_delete.id:
            msg_text += f'{current_user.username} leave chat'
            answer['leave'] = True
        else:
            msg_text += f'{current_user.username} delete {user_to_delete.username}'

        user_to_delete.remove_from_chat(current_chat)

        current_chat.chat_name = current_chat.chat_name.replace(user_to_delete.username + ', ', '')
        add_inf_msg(current_chat, msg_text)
        answer.update(add_chat_info_to_answer(current_chat=current_chat,
                                              current_user=current_user,
                                              msg_text=msg_text))
    current_user.update_activity()
    return answer
