from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import datetime

usersInChats = db.Table('usersInChats',
                        db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                        db.Column('chat_id', db.Integer, db.ForeignKey('chats.id'))
                        )


class Users(db.Model):
    """Класс пользователей для БД."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    psw_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), index=True, unique=True)
    last_activity = db.Column(db.DateTime())
    chats = db.relationship(
        'Chats', secondary=usersInChats,
        primaryjoin=(usersInChats.c.user_id == id),
        backref=db.backref('chats', lazy='dynamic'), lazy='dynamic')

    @staticmethod
    def suitable_users(example_username):
        return Users.query.filter(
            Users.username.startswith(example_username))

    def find_user_chats(self):
        return Chats.query.join(
            usersInChats, (usersInChats.c.user_id == self.id)).order_by(Chats.last_activity.desc())

    def set_password(self, password):
        self.psw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.psw_hash, password)

    @staticmethod
    def find_by_name(username):
        return Users.query.filter(
            Users.username == username).first()

    @staticmethod
    def find_by_id(id):
        return Users.query.filter(
            Users.id == id).first()

    def add_to_chat(self, chat):
        if not self.is_in_chat(self):
            self.chats.append(chat)

    def remove_from_chat(self, chat):
        if self.is_in_chat(self):
            self.chats.remove(chat)

    def is_in_chat(self, user):
        return self.chats.filter(
            usersInChats.c.user_id == user.id).count() > 0

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return f'{self.username}'


class Messages(db.Model):
    """Класс сообщений для БД."""
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(50))
    msg = db.Column(db.String(200))
    chat = db.Column(db.Integer, db.ForeignKey('chats.id'))
    time_stamp = db.Column(db.DateTime())

    def __init__(self, sender, chat, msg):
        self.sender = sender
        self.chat = chat
        self.msg = msg
        self.time_stamp = datetime.datetime.now()

    def __repr__(self):
        return f'{self.from_user}: {self.msg}'


class Chats(db.Model):
    """Класс чата для БД."""
    id = db.Column(db.Integer, primary_key=True)
    messages = db.relationship('Messages', backref='chats')
    users = db.relationship(
        'Users', secondary=usersInChats,
        primaryjoin=(usersInChats.c.chat_id == id),
        backref=db.backref('users', lazy='dynamic'))
    chat_name = db.Column(db.String(100))
    last_activity = db.Column(db.DateTime())

    @staticmethod
    def find_by_id(id):
        return Chats.query.filter(
            Chats.id == id).first()

    def __init__(self, users):
        self.chat_name = users
