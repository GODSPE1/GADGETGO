from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

with app.app_context():
    db.create_all()
    print('Database successfully created')

from app import routes