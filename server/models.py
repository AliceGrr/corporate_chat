import os
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import datetime
from hashlib import md5

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
    avatar = db.Column(db.String(128))
    chats = db.relationship(
        'Chats', secondary=usersInChats,
        primaryjoin=(usersInChats.c.user_id == id),
        backref=db.backref('chats', lazy='dynamic'), lazy='dynamic')

    def load_avatar(self, url):
        filename = f'{self.username}_offline.png'
        filepath = os.getcwd() + '/server/images/' + filename
        with open(filepath, 'wb') as f:
            response = requests.get(url, stream=True)
            for block in response.iter_content(1024):
                if not block:
                    break
                f.write(block)
        return filename

    def set_avatar(self):
        url = self.get_avatar_url(128)
        self.avatar = self.load_avatar(url)

    def get_avatar_url(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.set_avatar()

    def get_suitable_chats(self, example_username):
        return db.session.query(Chats, Users.avatar, Users.username) \
            .join(usersInChats, (usersInChats.c.chat_id == Chats.id)) \
            .join(Users, (usersInChats.c.user_id == Users.id)) \
            .filter(Users.username.startswith(example_username),
                    Chats.id.in_([chat.id for chat in self.find_user_chats()]),
                    Users.id != self.id) \
            .order_by(Chats.last_activity.desc())

    def get_suitable_users(self, example_username):
        return Users.query \
            .filter(Users.username.startswith(example_username),
                    Users.id != self.id)

    def find_user_chats(self):
        return Chats.query \
            .join(usersInChats) \
            .filter(usersInChats.c.user_id == self.id) \
            .order_by(Chats.last_activity.desc())

    def find_users_in_chats(self, chat_id):
        return Users.query \
            .join(usersInChats) \
            .filter(Users.id != self.id, usersInChats.c.chat_id == chat_id)

    def set_password(self, password):
        self.psw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.psw_hash, password)

    @staticmethod
    def find_by_name(username):
        return Users.query \
            .filter(Users.username == username) \
            .first()

    @staticmethod
    def find_by_id(user_id):
        return Users.query.get(user_id)

    def add_to_chat(self, chat):
        if not self.is_in_chat(chat):
            self.chats.append(chat)

    def remove_from_chat(self, chat):
        if self.is_in_chat(chat):
            self.chats.remove(chat)

    def is_in_chat(self, chat):
        return self.chats \
                   .filter(usersInChats.c.chat_id == chat.id) \
                   .count() > 0

    def __repr__(self):
        return f'{self.username}'


class Messages(db.Model):
    """Класс сообщений для БД."""
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Integer)
    msg = db.Column(db.String(200))
    chat = db.Column(db.Integer, db.ForeignKey('chats.id'))
    time_stamp = db.Column(db.DateTime())

    def __init__(self, sender, chat, msg):
        self.sender = sender
        self.chat = chat
        self.msg = msg
        self.time_stamp = datetime.datetime.now()


class Chats(db.Model):
    """Класс чата для БД."""
    id = db.Column(db.Integer, primary_key=True)
    messages = db.relationship('Messages', backref='chats')
    users = db.relationship(
        'Users', secondary=usersInChats,
        primaryjoin=(usersInChats.c.chat_id == id),
        backref=db.backref('users', lazy='dynamic'), lazy='dynamic')
    chat_name = db.Column(db.String(100))
    owner = db.Column(db.Integer)
    last_activity = db.Column(db.DateTime())

    @staticmethod
    def find_by_id(chat_id):
        return Chats.query.get(chat_id)

    def get_last_msg(self):
        last_msg = Messages.query \
            .filter(Messages.chat == self.id) \
            .order_by(Messages.time_stamp.desc()).first()
        if last_msg:
            return last_msg.msg
        else:
            return ''

    def __init__(self, users):
        self.chat_name = users
