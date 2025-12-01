from flask import jsonify, Blueprint, render_template
from datetime import datetime
# from app.v1 import app

home_bp = Blueprint('home', __name__)

@home_bp.route('/', methods=['GET'])
@home_bp.route('/home', methods=['GET'])
def home():
    """test function"""
    return render_template("home.html", year=datetime.now().year)
