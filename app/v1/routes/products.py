from flask import request, jsonify, Blueprint
import uuid
from app.v1.models import Product
from app.v1 import db
from app.v1.utils.token_manager import token_required


product = Blueprint(import_name=__name__, name="product", url_prefix="/products")

# Route to add new products (admin only)
@product.route('/', methods=['POST'])
@token_required
def add_product(current_user):
    """Create a product"""

    # Check for admin privileges
    if not current_user.admin:
        return jsonify({'message': 'Unauthorized, admin access is required'}), 403

    data = request.get_json()

    # Check if product already exists
    existing_product = Product.query.filter(Product.title == data['title']).first()

    if existing_product:
        return jsonify({'message': 'Product already exists'}), 400

    # Extract data from request
    title = data.get('title')
    description = data.get('description')
    price = data.get('price')
    image = data.get('image')
    category_id = data.get('category_id')  # Use 'category_id' if that's the expected key

    # Check for missing fields
    if not all([title, description, price, category_id]):
        return jsonify({'message': 'Missing fields'}), 400

    try:
        # Create new product
        new_product = Product(
            title=title,
            description=description,
            price=float(price),
            image=image,
            category_id=int(category_id)
        )    
        
        db.session.add(new_product)
        db.session.commit()

        return jsonify({'message': 'Product added successfully!'}), 201
    except ValueError:
        return jsonify({'message': 'Invalid data format, please check your inputs'}), 400
    except Exception as e:
        db.session.rollback()  # Rollback in case of any other error
        return jsonify({'message': 'An error occurred while adding the product'}), 500

    

# Route to fetch all products
@product.route('/', methods=['GET'])
def get_products():
    """Function to fetch all the products

    Return: the list of all products in a json format
    """
    #Query the database for all products
    try:

        products = Product.query.all()
        output = [{'title': product.title, 'price': product.price} for product in products]

        # check if there is no product
        if not output:
            return jsonify({'message': 'No product found'})

        return jsonify({'products': output}), 200
    
    except Exception as e:
        return jsonify({'message': 'Couldn\'t  finish this operation! try again'}), 500




# Route to fetch a single product by name
@product.route('/<product_name>', methods=['GET'])
def get_one_product(product_name):
    my_product = Product.query.filter_by(title=product_name).first()

    if not product:
        return jsonify({'message': 'Product not found'}), 404

    return jsonify({
        'title': my_product.title,
        'description': my_product.description,
        'price': my_product.price,
        'category': my_product.category
    }), 200


# Route to edit a product (admin only)
@product.route('/<product_name>', methods=['PUT'])
@token_required
def edit_product(current_user, product_name):
    if not current_user.admin:
        return jsonify({'message': 'Unauthorized to perform this function!'}), 403

    data = request.get_json()
    my_product = Product.query.filter_by(title=product_name).first()

    if not product:
        return jsonify({'message': 'Product not found'}), 404

    my_product.title = data.get('title', my_product.title)
    my_product.description = data.get('description', my_product.description)
    my_product.price = data.get('price', my_product.price)
    my_product.image = data.get('image', my_product.image)

    db.session.commit()

    return jsonify({'message': 'Product updated successfully!'}), 200




# Route to delete a product (admin only)
@product.route('/<product_name>', methods=['DELETE'])
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

