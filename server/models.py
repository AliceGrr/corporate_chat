from . import db
import datetime


class Users(db.Model):
    """Класс пользователей для БД."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    psw = db.Column(db.String(128))

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
        return f'<from: {self.from_user}, to chat: {self.chat}, msg: {self.msg}, date/time: {self.time_stamp}>'


class Chats(db.Model):
    """Класс чата для БД."""
    id = db.Column(db.Integer, primary_key=True)
    users = db.Column(db.String(200))
    messages = db.relationship('Messages', backref='chats')

    def __init__(self, users):
        self.users = users

    def __repr__(self):
        return f'{self.users}'


