import eventlet

eventlet.monkey_patch()
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import make_config
import os


try:
    os.remove("storage.db")
except Exception:
    pass

app = Flask(__name__)
make_config(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from .controller import observer_controller

db.create_all()
