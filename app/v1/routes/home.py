from flask import jsonify
from app.v1 import app

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    """test function"""
    return jsonify({'message': "Welcome to our api feel free use our service"})
