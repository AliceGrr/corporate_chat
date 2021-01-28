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
    to_user = db.Column(db.String(50))
    time_stamp = db.Column(db.DateTime())

    def __init__(self, from_user, to_user, msg):
        self.from_user = from_user
        self.to_user = to_user
        self.msg = msg
        self.time_stamp = datetime.datetime.now()

    def __repr__(self):
        return f'<from: {self.from_user}, to: {self.to_user}, msg: {self.msg}, date/time: {self.time_stamp}>'


