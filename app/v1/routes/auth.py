from flask import Blueprint
from flask import request, jsonify, make_response, current_app
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
import jwt

from app.v1.models import User
from app.v1 import db

auth = Blueprint(name="auth", import_name=__name__)

# Route to register a new user (public access)
@auth.route('/register', methods=['POST'])
def register():
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
            return jsonify({'message': 'Invalid credentials. Email, password, and username are required.'}), 400

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

    # check if content type is application/json
    if request.headers.get("Content-Type") != "application/json":
            return jsonify({"message": "content-type is not application/json", "status_code": 415}), 415
    
    # Extract the data from the request body
    data = request.get_json()
    password = data.get('password')
    username = data.get('username')
    print(password)
    print(username)

    user: User | None = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return make_response('Could not verify username', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    try:
        now = datetime.datetime.now()
        payload = {
            'username': user.username,
            'exp': now + datetime.timedelta(minutes=30)
        }
        token = jwt.encode(payload=payload, key=current_app.config['SECRET_KEY'], algorithm='HS256')
        
        if isinstance(token, bytes):
            token = token.decode('utf-8')
            
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error in tokenization'}), 403

    return jsonify({
        'token-type': "bearer",
        'token': token
        }), 200
