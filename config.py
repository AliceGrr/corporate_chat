import os
from pathlib import Path


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'lil secret key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///chat.db'
    ALLOWED_EXTENSIONS = {'png'}
