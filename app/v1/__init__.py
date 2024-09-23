from flask import Flask
from config import Config

from app.v1.models import *
from app.v1.routes import version_one


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(version_one)


with app.app_context():
    db.create_all()
    print('Database successfully created')
