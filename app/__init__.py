from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from collections import deque

from config import Config

flask_app = Flask(__name__)
flask_app.config.from_object(Config)
db = SQLAlchemy(flask_app)
migrate = Migrate(flask_app, db)

ROOMS = {}
EMPTY_ROOMS = deque()


from app import routes, models

