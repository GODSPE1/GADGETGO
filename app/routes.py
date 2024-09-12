from flask import Flask, request, jsonify, make_response
import uuid
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import app
import jwt
from app.models import User, Product
from functools import wraps


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check if token is present in headers
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        # Return if no token is provided
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Decode the token using the app's secret key
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(username=data['username']).first()

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401

        # Pass the current_user to the wrapped function
        return f(current_user, *args, **kwargs)

    return decorated



@app.route('/user/<username>', methods=['GET'])
def get_one_user(current_user, username):

    if not current_user.admin:
        return jsonify({ 'message' : 'Unauthoriseed to perform this function!'})

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'message' : 'no user'})

    return jsonify({'username': user.username, 'email': user.email, 'admin': user.admin})

@app.route('/user', methods=['GET'])
@token_required
def get_all_user(current_user):
    """get all user"""

    if not current_user.admin:
        return jsonify({ 'message' : 'Unauthoriseed to perform this function!'})

    users = User.query.all()
    output = []

    for user in users:
        user_data = {}
        user.username
        user_data['password'] = user.password
        user_data['email'] = user.email
        user_data['emai'] = user.admin
        output.append(user_data)

    return jsonify({ 'users': output })


@app.route('/user', methods=['POST'])
@token_required
def create_user(current_user):
    """creates a user"""

    if not current_user.admin:
        return jsonify({ 'message' : 'Unauthoriseed to perform this function!'})


    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    new_user = User(username=data['username'], email=data['email'], password=hashed_password, admin=False)
    new_user.save()

    return jsonify({'message': 'New user created' })

@app.route('/user/<user_id>', methods=['PUT'])
def promote_user():
    return ''

@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(current_user, username):

    if not current_user.admin:
        return jsonify({ 'message' : 'Unauthoriseed to perform this function!'})
    
    if not user:
        return jsonify({ 'message' : 'No user found!'})
    delete(username)



@app.route('/register', methods=['GET', 'POST'])
def register():
    email = request.json['email']
    password = request.json['password']


    user_exists = User.query.filter_by(email=email).first() is not None

    if user_exists:
        return jsonify({ 'error': 'User already exists' }), 409

    hashed_password


@app.route("/login", methods=['GET', 'POST'])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return jsonify({'message': 'No user found'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {'token_id': str(uuid.uuid4()), 'exp': datetime.datetime.now() + datetime.timedelta(minutes=2)}, 
            app.config['SECRET_KEY']
        )

        return jsonify({'token': token})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    db.session.delete()
    db.session.commit()

"""
Products: Allow the admin to add new products using the POST /api/products
endpoint. Fetch all available products using GET /api/products.
"""


@app.route('/products', methods=['GET'])
def products():
    """Fetch all available produts"""
    
    #query the database for all products
    products = Product.query.all()

    return ({ 'products' : products})



@app.route('/products', methods=['POST'])
@token_required
def add_products(current_user):
    """Admin to add new products"""

    # Check if the user has admin privileges
    if not current_user.admin:
        return jsonify({'message': 'Unauthorized to perform this function!'})

    # Get the product data from the request
    data = request.get_json()

    # Create a new Product object
    new_product = Product(prod_id=data['prod_id'], category=data['category'],
                          title=data['title'], description=data['description'],
                          price=data['price'], image=data['image'], order=['order'])

    # Fetch all existing products from the database
    all_products = Product.query.all()

    # Check if a similar product already exists
    for product in all_products:
        if (new_product.prod_id == product.prod_id and 
            new_product.category == product.category and 
            new_product.title == product.title):
            return jsonify({'message': 'Product already exists'})

    # If no matching product was found, save the new product
    new_product.save()  # Ensure that save() method correctly handles adding and committing the product

    # Return a success message
    return jsonify({'message': 'Product added successfully'})

    @app.route('/product/<product>')
    


