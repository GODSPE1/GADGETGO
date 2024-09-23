from flask import Blueprint

version_one = Blueprint(import_name=__name__, name="version_one")

from app.v1.routes.auth import auth
from app.v1.routes.products import product
from app.v1.routes.category import category
from app.v1.routes.orders import order
from app.v1.routes.payments import payment
from app.v1.routes.users import user

version_one.register_blueprint(auth)
version_one.register_blueprint(product)
version_one.register_blueprint(category)
version_one.register_blueprint(order)
version_one.register_blueprint(payment)
version_one.register_blueprint(user)
