from flask import Blueprint
from flask import jsonify
from app.v1.models import User
from app.v1 import db
from app.v1.utils.token_manager import token_required
from app.v1.routes.auth import register


user = Blueprint(import_name=__name__, name="user", url_prefix="/users")

# Route to get user details
@user.route('/<username>', methods=['GET'])
@token_required
def get_one_user(current_user, username):
    if not current_user.admin:
        return jsonify({'message': 'Unauthorized to perform this function!'}), 403

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'message': 'No user found!'}), 404

    return jsonify({'username': user.username, 'email': user.email, 'admin': user.admin}), 200




# Route to get all users
@user.route('/', methods=['GET'])
@token_required
def get_all_users(current_user):

    # check if user is an admin
    if not current_user.admin:
        return jsonify({'message': 'Unauthorized to perform this function!'}), 403

    # queey the database
    users = User.query.all()
    output = []
    for user in users:
        user_data = {
            'username': user.username,
            'email': user.email,
            'admin': user.admin
        }
        output.append(user_data)

    return jsonify({'users': output}), 200



# Route to create a new user
@user.route('/create', methods=['POST'])
@token_required
def create_user(current_user):
    # Check if the current user is an admin
        if not current_user.admin:
            return jsonify({'message': 'Unauthorized to perform this function!'}), 403
    

    # Register a user using try exception
        try:
            register()
        
            return jsonify({'message': 'New user created!'}), 201

        except Exception as e:
            return jsonify({'message': 'Failed to create user', 'error': str(e)}), 400



# Route to delete a user
@user.route('/delete/<username>', methods=['DELETE'])
@token_required
def delete_user(current_user, username):
    # check if current user is admin
    if not current_user.admin:
        return jsonify({'message': 'Unauthorized to perform this function!'}), 403

    try: 
        # Query the database to find user
        user = User.query.filter_by(username=username).first()

        if not user:
            return jsonify({'message': 'No user found!'}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User deleted!'}), 200
    
    except Exception as e:
        return jsonify({'message' 'Internal server error'}), 500
