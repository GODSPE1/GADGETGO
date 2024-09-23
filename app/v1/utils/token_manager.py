import os
from flask import request, jsonify
import jwt
from app.v1.models import User
from functools import wraps

secret = os.getenv("SECRET_KEY", default="strong_secret")

# Decorator to require token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        auth_headers = request.headers.get('Authorization')
        
        if not auth_headers:
            return jsonify({'message': 'Authourization header is missing'})
        
        token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Authorization token is missing!'}), 401

        try:
            data = jwt.decode(token, key=secret, algorithms=["HS256"])
            current_user = User.query.filter_by(username=data['username']).first()
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated
