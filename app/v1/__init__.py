from flask import Flask
from config import Config
from flasgger import Swagger
from app.v1.models import db
from app.v1.routes import version_one

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Register your Blueprint(s)
app.register_blueprint(version_one)

# Initialize Flasgger
swagger = Swagger(app)

with app.app_context():
    db.create_all()
    print('Database successfully created')

