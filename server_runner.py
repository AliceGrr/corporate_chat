from flask import Flask, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from tables import Users

app = Flask(__name__)

app.config.update(
    SQLALCHEMY_DATABASE_URI='sqlite:///chat.sql',
    SECRET_KEY='lil secret key',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

db = SQLAlchemy(app)


@app.route('/corporate_chat', methods=['GET', 'POST'])
def login():
    """Вход пользователя."""
    if request.method == 'POST':
        pass


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
        return redirect(url_for('jello'))
    if request.method == 'GET':
        message = 'users:' + str(Users.query.all())
        return message


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
