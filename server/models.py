from . import db
import datetime


class Users(db.Model):
    """Класс пользователей для БД."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    psw = db.Column(db.String(128))
    chats = db.relationship('UserChats', backref='user')

    def __init__(self, username, psw):
        self.username = username
        self.psw = psw

    def __repr__(self):
        return f'{self.username}'


class Messages(db.Model):
    """Класс сообщений для БД."""
    id = db.Column(db.Integer, primary_key=True)
    from_user = db.Column(db.String(50))
    msg = db.Column(db.String(200))
    chat = db.Column(db.Integer, db.ForeignKey('chats.id'))
    time_stamp = db.Column(db.DateTime())

    def __init__(self, from_user, chat, msg):
        self.from_user = from_user
        self.chat = chat
        self.msg = msg
        self.time_stamp = datetime.datetime.now()

    def __repr__(self):
        return f'{self.from_user}: {self.msg}'


class Chats(db.Model):
    """Класс чата для БД."""
    id = db.Column(db.Integer, primary_key=True)
    messages = db.relationship('Messages', backref='chatm')
    users = db.relationship('UserChats', backref='chat')
    chat_name = db.Column(db.String(100))
    last_activity = db.Column(db.DateTime())

    def __init__(self, users):
        self.chat_name = users
        self.last_activity = datetime.datetime.now()


class UserChats(db.Model):
    """Класс таблицы для связки пользователей и чатов."""
    id = db.Column(db.Integer, primary_key=True)
    user_ids = db.Column(db.Integer, db.ForeignKey('users.id'))
    chat_ids = db.Column(db.Integer, db.ForeignKey('chats.id'))

    def __init__(self, user_id, chat_id):
        self.user_ids = user_id
        self.chat_ids = chat_id
