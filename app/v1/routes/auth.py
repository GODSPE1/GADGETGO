#!/usr/bin/env python3
from flask import Blueprint
from flask import request, jsonify, make_response, current_app
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
import jwt
from app.v1.utils.token_manager import token_required, request_token
from app.v1.utils.is_logout import log_out_token

from app.v1.models import User
from app.v1 import db

auth = Blueprint(name="auth", import_name=__name__)

# Route to register a new user (public access)
@auth.route('/register', methods=['POST'])
def register():
    """
    Register a new user with email, username, and password
    ---
    tags:
      - Authentication
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - username
            - password
          properties:
            email:
              type: string
              format: email
              example: "user@example.com"
            username:
              type: string
              minLength: 1
              example: "john_doe"
            password:
              type: string
              format: password
              minLength: 6
              example: "securePassword123"
            admin:
              type: boolean
              default: false
              example: false
    responses:
      201:
        description: User registered successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User registered successfully"
            user_id:
              type: integer
              example: 1
      400:
        description: Bad request - missing required fields
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Invalid credentials. Email, password, and username are required."
      409:
        description: Conflict - username or email already exists
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Username already exists"
      415:
        description: Unsupported Media Type - Content-Type must be application/json
        schema:
          type: object
          properties:
            message:
              type: string
              example: "content-type is not application/json"
            status_code:
              type: integer
              example: 415
      500:
        description: Internal server error during registration
        schema:
          type: object
          properties:
            error:
              type: string
              example: "An error occurred during registration. Please try again later."
    """
    try:
        # check if content type is application/json
        if request.headers.get("Content-Type") != "application/json":
            return jsonify({"message": "content-type is not application/json", "status_code": 415}), 415
        
        # Extract the data from the request body
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')
        admin = data.get('admin', False)

        # Validate the input fields
        if not email or not password or not username:
            return jsonify({'message': 'Username, email, and password are required.'}), 400

        # Check if the user already exists
        existing_user = User.query.filter(
            or_(User.email == email, User.username == username)
        ).first()
        
        if existing_user:
            if existing_user.username == username:
                return jsonify({'error': 'Username already exists'}), 409
            
            if existing_user.email == email:
                return jsonify({'error': 'Email already exists'}), 409

        # Hash the password securely
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Create a new user instance
        new_user = User(username=username, email=email, password=hashed_password, admin=bool(admin))

        # Add the new user to the session and commit
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully', 'user_id': new_user.id}), 201

    except Exception as e:
        # Log the error for debugging
        print(f"Error during registration: {str(e)}")
        return jsonify({'error': 'An error occurred during registration. Please try again later.'}), 500



# Route to login and receive token
@auth.route('/login', methods=['POST'])
def login():
    """
    User login endpoint - authenticates user and returns JWT token
    ---
    tags:
      - Authentication
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              minLength: 1
              example: "john_doe"
            password:
              type: string
              format: password
              minLength: 6
              example: "securePassword123"
    responses:
      200:
        description: Login successful - returns Bearer token
        schema:
          type: object
          properties:
            token-type:
              type: string
              example: "bearer"
            token:
              type: string
              example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
      401:
        description: Unauthorized - invalid username or password
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Could not verify username"
      403:
        description: Forbidden - error in tokenization
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Error in tokenization"
      415:
        description: Unsupported Media Type - Content-Type must be application/json
        schema:
          type: object
          properties:
            message:
              type: string
              example: "content-type is not application/json"
            status_code:
              type: integer
              example: 415
    """

    # check if content type is application/json
    if request.headers.get("Content-Type") != "application/json":
            return jsonify({"message": "content-type is not application/json", "status_code": 415}), 415
    
    # Extract the data from the request body
    data = request.get_json()
    password = data.get('password')
    username = data.get('username')

    user: User | None = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return make_response('Username and password are Required', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    try:
        # Give expiry date to the token
        now = datetime.datetime.utcnow()
        payload = {
            'username': user.id,
            'exp': now + datetime.timedelta(hours=1)
        }

        # Generate a token for registered and login
        token = jwt.encode(payload=payload, key=current_app.config['SECRET_KEY'], algorithm='HS256')
        
        # Check for token is bytes and decode to string
        if isinstance(token, bytes):
            token = token.decode('utf-8')

        return jsonify({'token': token})
            
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error in tokenization'}), 403

    # return token and token type
    return jsonify({
        'token-type': "bearer",
        'token': token
        }), 200


@auth.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    """
    User logout endpoint - invalidates the user's JWT token
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    responses:
      200:
        description: Successfully logged out
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Successfully logged out"
      401:
        description: Unauthorized - missing or invalid token
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Token is missing or invalid"
      500:
        description: Internal server error during logout
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Error during logout"
    """
    token = request_token()
    log_out_token(token)
    return jsonify({'message': 'Successfully logged out'}), 200
