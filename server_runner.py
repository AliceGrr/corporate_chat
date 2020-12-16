from flask import Flask, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, select
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
    username = db.Column(db.String(50), primary_key=True)
    psw = db.Column(db.String(500))

    def __init__(self, username, psw):
        self.username = username
        self.psw = psw

    def __repr__(self):
        return f'username: {self.username}, psw: {self.psw}'


@app.route('/corporate_chat', methods=['POST'])
def login():
    """Вход пользователя."""
    if request.method == 'POST':
        # TODO: write a login func
        return 'success'


@app.route('/corporate_chat/register', methods=['POST'])
def register():
    """Регистрация пользователей."""
    if request.method == 'POST':
        if request.form["username"] == '':
            print("Username is required")
        elif request.form["psw"] == '':
            print("Password is required")
        else:
            try:
                user = Users(request.form['username'], request.form['psw'])
                db.session.add(user)
                db.session.commit()
            except exc.IntegrityError:
                print('user with this name exist')
            return 'success!'


@app.route('/register_test')
def test():
    """попытка регистрации."""
    requests.post('http://127.0.0.1:5000/corporate_chat/register', data={'username': 'Alice', 'psw': 'qwerty'})
    return 'complete'


@app.route('/login_test')
def test_2():
    """попытка логина."""
    requests.post('http://127.0.0.1:5000/corporate_chat', data={'username': 'Palvo'})
    return 'complete'


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
