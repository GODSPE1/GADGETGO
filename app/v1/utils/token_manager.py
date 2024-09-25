#!/usr/bin/env python3
import os
from flask import request, jsonify
import jwt
from app.v1.models import User
from functools import wraps
from app.v1.utils.is_logout import log_out_token


secret = os.getenv("SECRET_KEY", default="strong_secret")


def request_token():
    """Get the token from header authorization"""
    auth_header = request.headers.get('Authorization')

    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(" ")[1]  # Extract token from the header
        return token
    return None


# Decorator to require token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request_token()
        # token = None

        # auth_headers = request.headers.get('Authorization')
        
        # if not auth_headers:
        #     return jsonify({'message': 'Authourization header is missing'})
        
        # token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Authorization token is missing!'}), 401

        try:
            if log_out_token(token):
                return jsonify({'message': 'Token has been blacklisted. Please log in again.'}), 403
            
            data = jwt.decode(token, key=secret, algorithms=["HS256"])
            current_user = User.query.filter_by(username=data['username']).first()
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated


