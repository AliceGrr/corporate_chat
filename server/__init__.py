from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_moment import Moment


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


manager = Manager(app)
manager.add_command('db', MigrateCommand)

from . import routes, models
