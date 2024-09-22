from flask import Flask, request, jsonify, make_response, abort
import json
import uuid
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import app
import jwt
from app.models import User, Product, Order, OrderProduct, Category
from functools import wraps
from app import db
from sqlalchemy import or_

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
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(username=data['username']).first()
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated



@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    """test function"""
    return jsonify({'message': "Welcome to our home page now"})




# Route to get user details
@app.route('/user/<username>', methods=['GET'])
@token_required
def get_one_user(current_user, username):
    if not current_user.admin:
        return jsonify({'message': 'Unauthorized to perform this function!'}), 403

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'message': 'No user found!'}), 404

    return jsonify({'username': user.username, 'email': user.email, 'admin': user.admin}), 200




# Route to get all users
@app.route('/users', methods=['GET'])
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
@app.route('/user/create', methods=['POST'])
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
@app.route('/user/delete/<username>', methods=['DELETE'])
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



# Route to register a new user (public access)
@app.route('/register', methods=['POST'])
def register():
    try:
        # Extract the data from the request body
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')
        admin = data.get('admin', False)  # Default to False if not provided

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
@app.route('/login', methods=['POST'])
def login():
    # auth = request.authorization


    # if not auth or not auth.username or not auth.password:
    #     return make_response('Could not verify password', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    
    data = request.get_json()
    password = data.get('password')
    username = data.get('username')
    print(password)
    print(username)
    print

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return make_response('Could not verify username', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    try:
        token = jwt.encode(
        {'username': user.username, 'exp': datetime.datetime.now() + datetime.timedelta(minutes=30)},
        app.config['SECRET_KEY']
        )
    except Exception as e:
        return jsonify({'message': 'Error in tokenization'}), 403

    if isinstance(token, bytes):
        token = token.decode('utf-8')
    token_type = (type(token))
    return jsonify({
        'token-type': token_type
        'token': token
        }), 200


# Route to fetch all products
@app.route('/products', methods=['GET'])
def get_products():
    """Function to fetch all the products

    Return: the list of all products in a json format
    """
    #Query the database for all products
    try:

        products = Product.query.all()
        output = [{'title': product.title, 'price': product.price} for product in products]

        return jsonify({'products': output}), 200
    
    except Exception as e:
        return jsonify({'message': 'Couldn\'t  finish this operation! try again'}), 500




# Route to fetch a single product by name
@app.route('/products/<product_name>', methods=['GET'])
def get_one_product(product_name):
    product = Product.query.filter_by(title=product_name).first()

    if not product:
        return jsonify({'message': 'Product not found'}), 404

    return jsonify({
        'title': product.title,
        'description': product.description,
        'price': product.price,
        'category': product.category
    }), 200




# Route to add new products (admin only)
@app.route('/products', methods=['POST'])
@token_required
def add_product(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Unauthorized to perform this function!'}), 403

    data = request.get_json()

    # Check if product already exists
    existing_product = Product.query.filter_by(title=data['title']).first()
    if existing_product:
        return jsonify({'message': 'Product already exists'}), 409

    new_product = Product(
        prod_id=str(uuid.uuid4()), 
        category=data['category'], 
        title=data['title'], 
        description=data['description'], 
        price=data['price'],
        image=data['image']
    )
    db.session.add(new_product)
    db.session.commit()

    return jsonify({'message': 'Product added successfully!'}), 201




# Route to edit a product (admin only)
@app.route('/products/<product_name>', methods=['PUT'])
@token_required
def edit_product(current_user, product_name):
    if not current_user.admin:
        return jsonify({'message': 'Unauthorized to perform this function!'}), 403

    data = request.get_json()
    product = Product.query.filter_by(title=product_name).first()

    if not product:
        return jsonify({'message': 'Product not found'}), 404

    product.title = data.get('title', product.title)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.image = data.get('image', product.image)

    db.session.commit()

    return jsonify({'message': 'Product updated successfully!'}), 200




# Route to delete a product (admin only)
@app.route('/products/<product_name>', methods=['DELETE'])
@token_required
def delete_products(current_user, product_name):
    if not current_user.admin:
        return jsonify({'message': 'Unauthorized to perform this function!'}), 403

    product = Product.query.filter_by(title=product_name).first()

    if not product:
        return jsonify({'message': 'Product not found'}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({'message': 'Product deleted successfully!'}), 200




# Retrieve a list of orders
@token_required
def all_order(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Unauthorized to perform this function!'}), 403

    orders = Order.query.all()  # Fetch all orders
    output = [{'orderId': order.id, 'userId': order.user_id} for order in orders]
    
    return jsonify({'List of orders': output})



# Fetch user orders
@app.route('/orders/<id>', methods=['GET'])
@token_required
def get_one_order(current_user):
    """get a specfic oder for the user"""
    if not current_user:
        return jsonify({ 'message': 'User does not exit'})
    
    current_user_oder = current_user.order

    if not current_user_oder:
        return jsonify({ 'message': 'order doesn\'t exist'})
    
    return jsonify({'user orders': current_user_oder})



@app.route('/orders', methods=['POST'])
@token_required
def create_order(current_user):
    """Create a new order for the user"""

    data = request.get_json() 

    if request.method == 'POST':

        #check if data is present
        if not data or 'product_id' not in data or 'quantity' not in data:
            return jsonify({'message': 'Missing required fields'}), 400

        # Create a new order associated with the current user
        new_order = Order(
            user_id=current_user.id,
            product_id=data['product_id'],
            quantity=data['quantity'],
            status=data['status']
        )

        # Add the new order to the session
        db.session.add(new_order)
        db.session.commit()

        return jsonify({'message': 'Order created successfully'}), 201



@app.route('/orders/<id>', methods=['PUT'])
@token_required
def update_order(current_user, id):
    """Update an order associated with a user"""
    if not current_user:
        return jsonify({'message': 'Unauthorized'}), 401
    
    data = request.get_json()

    # Find the order by its ID.
    # check if it belongs to the current user
    existing_order = Order.query.filter_by(id=id, user_id=current_user.id).first()
    
    if not existing_order:
        return jsonify({'message': 'Order does not exist or does not belong to the current user'}), 404

    if 'quantity' in data:
        existing_order.quantity = data['quantity']
    if 'product_id' in data:
        existing_order.product_id = data['product_id']
    
    # Commit the changes to the database
    db.session.commit()
    
    return jsonify({'message': 'Order has been updated successfully'}), 200



@app.route('/orders/<id>/', methods=['DELETE'])
@token_required
def delete_an_order(current_user, id):
    """delete an order associated with a user"""
    
    if not current_user:
        return jsonify({'message': 'Unauthorized'}), 401

    # Query a specific order based on ID
    user_order = Order.query.filter_by(id=id, user_id=current_user.id).first()

    if not user_order:
        return jsonify({'message': 'Order does not exist or does not belong to the current user'}), 404

    # Delete the order
    db.session.delete(user_order)
    db.session.commit()

    return jsonify({'message': 'Order has been deleted successfully'}), 200




@app.route('/categry', methods=['POST'])
@token_required
def create_category(current_user):
    """create a category"""
    if not current_user.admin:
        return jsonify({ 'message' : 'Unauthorized'}), 403
     
    data = request.get_json()

    existing_category = Category.query.filter(name=data['name'].lower().strip()).first()
    if existing_category:
        return jsonify({'message': 'Category already exist'}), 400
    
    try:
        new_category = Category(
            name = data['name'],
            description = data['description']
        )

        db.session.add(new_category)
        db.session.commit()
        return jsonify({
            'message': 'Category created Successfully',
            'name': new_category.name,
            'description': new_category.description

        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error creating Category', 'error': str(e)}), 500



@app.route('/categories', methods=['GET'])
@token_required
def get_all_categories(current_user):
    """Retrieve a list of categories."""
    if not current_user.admin:
        return jsonify({'message': 'Unauthorized'}), 403
    
    # Query the database
    category_list = Category.query.all()

    if not category_list:
        return jsonify({'message': 'No categories found'}), 404
    
    output = []

    # Prepare the output list with category details
    for category in category_list:
        category_data = {
            'id': category.id,
            'name': category.name,
            'description': category.description
        }
        output.append(category_data)

    # Return the entire list of categories
    return jsonify({'categories': output}), 200




@app.route('/categories/<id>', methods=['GET'])
@token_required
def get_one_category(current_user, id):
    """Retrieve a specific category by its ID"""

    if not current_user:
        return jsonify({'message': 'Unauthorized'}), 403
    
    # Query for a specific category using id
    category = Category.query.filter_by(id=id).first()

    if not category:
        return jsonify({'message': 'Category not found'}), 404
    
    # Format the category data for the response
    try:
        category_data = {
            'id': category.id,
            'name': category.name,
            'image': category.description
        }
        return jsonify({'category': category_data}), 200
    except Exception as e:
        return jsonify({'message': 'An error occurred while processing the category'}), 500



@app.route('/categories/<id>', methods=['PUT'])
@token_required
def update_category(current_user, id):
    """Update an existing category"""
    if not current_user.admin:
        return jsonify({'message': 'Unauthorised'}), 403
    

    data = request.get_json()

    existing_category = Category.query.filter_by(id=id).first()
    
    if not existing_category:
        return jsonify({'message': 'Category Not Found'}), 404
    
    try:
        existing_category.id = data.get('name', existing_category.id)
        existing_category.name = data.get('name', existing_category.name)
        existing_category.description = data('description', existing_category.description)

        db.session.commit()

        return jsonify({
            'message': 'Category Succesfully updated',
            'id': existing_category.id,
            'name': existing_category.name,
            'description': existing_category.description
        })
    except Exception as e:
        return jsonify({'message': 'Error updating the category'})


@app.route('/categories/<id>', methods=['DELETE'])
@token_required
def delete_category(current_user, id):
    """Delete a category"""
    
    if not current_user.admin:
        return jsonify({'message': 'Unauthorised'}), 403
    
    category = Category.query.filter_by(id=id).first()

    if not category:
        return jsonify({'message': 'Category not found'}), 403
    try:
        db.session.delete(category)
        db.session.commit()

        return jsonify({'message': 'Succesfully deleted categry'}), 200
    
    except Exception as e:
        return jsonify({'message': 'Error while deleting category'}), 500


@app.route('/payment_callback', methods=['GET'])
def paymentCallback():
    """handles payment"""

    reference = request.args.get('reference')

    if not reference:
        return jsonify({"No reference provided"}), 400

    # Verify User payment
    response = request.get(f'https://api.paystack.co/transaction/verify/{reference}', 
                            headers={'Authorization': f"Bearer {os.getenv('PAYSTACK_SECRET_KEY')}"})

    if response.status_code == 200:

        data = response.json().get('data', {})
        status = data.get('status')
        if status == 'success':
            customer = data.get('customer', {})
            email = customer.get('email')
            if email:

                # Update user's payment status in the database
                #user = PaymentStatus.query.filter_by(email=email).first()
                if user:
                    user.is_paid = True
                    db.session.commit()
                    return redirect(url_for('pages.register_applicant'))
                else:
                    return "User not found", 400
            else:
                return "Email not found in Paystack response", 400
        else:
            return f"Payment verification failed: {status}", 400
    else:
        return "Failed to verify payment with Paystack", 400
