from flask import Flask, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.sql'
app.config['SECRET_KEY'] = 'lil secret key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/')
def jello():
    return 'jello'


@app.route('/register', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        user = Users(request.form['username'], request.form['psw'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('jello'))
    return "can't create user"


@app.route('/test')
def test():
    requests.post('http://127.0.0.1:5000/register', data={'username': 'Pavlo', 'psw': 'qwerty2'})
    message = 'users:' + str(Users.query.all())
    return message


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True,)
    psw = db.Column(db.String(500))

    def __init__(self, username, psw):
        self.username = username
        self.psw = psw

    def __repr__(self):
        return f'id: {self.id}, username: {self.username}, psw: {self.psw} '


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
