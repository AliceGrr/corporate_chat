from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config.update(
    SQLALCHEMY_DATABASE_URI='sqlite:///chat.db',
    SECRET_KEY='lil secret key',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

db = SQLAlchemy(app)


from server import routes


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
