from flask import Flask, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import requests

app = Flask(__name__)

app.config.update(
    SQLALCHEMY_DATABASE_URI='sqlite:///chat.db',
    SECRET_KEY='lil secret key',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

db = SQLAlchemy(app)


class Users(db.Model):
    """ORM класс пользователей для БД."""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True,)
    psw = db.Column(db.String(500))

    def __init__(self, username, psw):
        self.username = username
        self.psw = psw

    def __repr__(self):
        return f'<id: {self.id}, username: {self.username}, psw: {self.psw}>'


@app.route('/corporate_chat', methods=['GET', 'POST'])
def login():
    """Вход пользователя."""
    if request.method == 'POST':
        return 'no enter'


@app.route('/corporate_chat/register', methods=['GET', 'POST'])
def register():
    """Регистрация пользователей."""
    if request.method == 'POST':
        try:
            user = Users(request.form['username'], request.form['psw'])
        except exc.IntegrityError:
            return 'user with this name exist'
        db.session.add(user)
        db.session.commit()
        flash('You were successfully registered')
        return 'success!'
    if request.method == 'GET':
        message = 'users:' + str(Users.query.all())
        return message


@app.route('/test')
def test():
    """попытка регистрации."""
    requests.post('http://127.0.0.1:5000/corporate_chat/register', data={'username': 'Alice', 'psw': 'qwerty'})
    return 'complete'


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
