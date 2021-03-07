from . import app, db
from flask import request
from .models import Users, Messages, Chats
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
    print('err_log create')
    err_log = verify_user_data(request.form['username'], request.form['psw'])
    if err_log['msg']:
        return err_log
    user = Users.query.filter(Users.username == request.form['username']).first()
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
    err_log = verify_user_data(request.form['username'], request.form['psw'], request.form['email'])
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

    chat = Chats.query.filter(Chats.id == request.form['to_chat']).first()
    chat.last_activity = msg.time_stamp
    db.session.add(chat)
    db.session.commit()
    return {'send_time': msg.time_stamp}


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
    user = Users.query.filter(Users.username == request.form['username']).first()
    user_chats = [chat.chat for chat in user.chats]
    chats_info = [
        {'chat_name': chat.chat_name,
         'chat_id': chat.id,
         'last_msg': chat.last_activity,
         }
        for chat in user_chats
    ]
    chats = sorted(chats_info, key=lambda x: x['last_msg'], reverse=True)
    return {'chats': chats}


@app.route('/corporate_chat/find_user_by_name', methods=['POST'])
def find_user_by_name():
    """Получение списка подходящих по запросу пользователей."""
    user = Users.query.filter(Users.id == request.form['current_user_id']).first()
    user_chat_ids = [chat.chat_ids for chat in user.chats]
    print(user_chat_ids)

    user_chats = {}
    for user_chat_id in user_chat_ids:
        user_chats.update({chat.user_ids: chat.chat_ids
                               for chat in UserChats.query.filter
                               (and_(UserChats.chat_ids == user_chat_id),
                                UserChats.user_ids != request.form['current_user_id'])})

    suitable_users = {user.id: str(user) for user in
                      Users.query.filter(and_(
                          Users.username.startswith(request.form['example_username']),
                          Users.id != request.form['current_user_id']))}

    print(user_chats, suitable_users)
    chats_info = []
    for user_id, chat_id in user_chats.items():
        if user_id in suitable_users:
            del suitable_users[user_id]

            chats_info += [
                {'chat_name': chat.chat.chat_name,
                 'chat_id': chat.chat.id,
                 'last_msg': chat.chat.last_activity,
                 }
                for chat in UserChats.query.filter
                (and_(UserChats.chat_ids == chat_id,
                      UserChats.user_ids == user_id))
            ]

    chats = sorted(chats_info, key=lambda x: x['last_msg'], reverse=True)
    print(chats, suitable_users)
    return {'suitable_chats': chats,
            'suitable_users': suitable_users}


@app.route('/corporate_chat/start_new_chat', methods=['POST'])
def start_new_chat():
    """Создание чата."""
    chat = Chats(request.form['users'])
    db.session.add(chat)
    db.session.commit()

    chat_id = chat.id
    users_ids = list(request.form['users_ids'])

    for user_id in users_ids:
        print(user_id, chat_id)
        userchat = UserChats(int(user_id), chat_id)
        db.session.add(userchat)
        db.session.commit()

    return {'chat_id': chat.id, 'users': chat.chat_name}
