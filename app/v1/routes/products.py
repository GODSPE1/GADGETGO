from flask import Blueprint, jsonify, request
from app.v1 import db
from app.v1.models import Product
from app.v1.utils.token_manager import token_required


product = Blueprint(import_name=__name__, name="product", url_prefix="/products")

# Route to add new products (admin only)
@product.route('/', methods=['POST'])
@token_required
def add_product(current_user):
    """Create a new product (Admin only)
    ---
    tags:
      - Products
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - title
            - description
            - price
            - category_id
          properties:
            title:
              type: string
              example: "Laptop"
            description:
              type: string
              example: "High-performance laptop"
            price:
              type: number
              example: 999.99
            image:
              type: string
              example: "image_url"
            category_id:
              type: integer
              example: 1
    responses:
      201:
        description: Product added successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Product added successfully!"
      400:
        description: Bad request - missing fields or product already exists
      403:
        description: Unauthorized - admin access required
      500:
        description: Server error
    """

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
    """Fetch all products
    ---
    tags:
      - Products
    responses:
      200:
        description: List of all products retrieved successfully
        schema:
          type: object
          properties:
            products:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  title:
                    type: string
                    example: "Laptop"
                  price:
                    type: number
                    example: 999.99
      404:
        description: No products found
      500:
        description: Server error
    """
    # Query the database for all products
    products = Product.query.all()
    output = [{'id': product.id, 'title': product.title, 'price': product.price} for product in products]

    # Check if there is no product
    if not output:
        return jsonify({'message': 'No product found'}), 404

    return jsonify({'products': output}), 200


# Route to fetch a single product by ID
@product.route('/<id>', methods=['GET'])
def get_one_product(id):
    """Fetch a single product by ID
    ---
    tags:
      - Products
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: Product ID
    responses:
      200:
        description: Product retrieved successfully
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            title:
              type: string
              example: "Laptop"
            description:
              type: string
              example: "High-performance laptop"
            price:
              type: number
              example: 999.99
      404:
        description: Product not found
      500:
        description: Server error
    """
    # Query the database for a product by its id
    my_product = Product.query.filter(Product.id == id).first()

    if not my_product:
        return jsonify({'message': 'Product not found'}), 404

    return jsonify({
        'id': my_product.id,
        'title': my_product.title,
        'description': my_product.description,
        'price': my_product.price,
    }), 200


# Route to edit a product (admin only)
@product.route('/<id>', methods=['PUT'])
@token_required
def edit_product(current_user, id):
    """Edit a product (Admin only)
    ---
    tags:
      - Products
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: Product ID
      - in: body
        name: body
        schema:
          type: object
          properties:
            title:
              type: string
              example: "Updated Laptop"
            description:
              type: string
              example: "Updated description"
            price:
              type: number
              example: 1099.99
    responses:
      200:
        description: Product updated successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Product updated successfully!"
      403:
        description: Unauthorized - admin access required
      404:
        description: Product not found
      500:
        description: Server error
    """

    # Check for admin privileges
    if not current_user.admin:
        return jsonify({'message': 'Unauthorized to perform this function!'}), 403

    try:
        # Query the database
        data = request.get_json()
        my_product = Product.query.filter_by(id=id).first()

        # Check if product is found
        if not my_product:
            return jsonify({'message': 'Product not found'}), 404

        # Check fields that were provided
        if 'title' in data:
            my_product.title = data.get('title', my_product.title)

        if 'description' in data:
            my_product.description = data.get('description', my_product.description)

        if 'price' in data:
            my_product.price = data.get('price', my_product.price)

        # Save to the database
        db.session.commit()

        return jsonify({'message': 'Product updated successfully!'}), 200

    except Exception as e:
        return jsonify({'message': 'Error editing products'}), 500


# Route to delete a product (admin only)
@product.route('/<id>', methods=['DELETE'])
@token_required
def delete_products(current_user, id):
    """Delete a product (Admin only)
    ---
    tags:
      - Products
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: Product ID
    responses:
      200:
        description: Product deleted successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Product deleted successfully!"
      403:
        description: Unauthorized - admin access required
      404:
        description: Product not found
      500:
        description: Server error
    """
    
    # Check for admin privilege
    if not current_user.admin:
        return jsonify({'message': 'Unauthorized to perform this function!'}), 403

    try:
        # Query the database for products
        my_product = Product.query.get(id)

        # Check if product is found
        if not my_product:
            return jsonify({'message': 'Product not found'}), 404

        # Delete a product and save to the database
        db.session.delete(my_product)
        db.session.commit()

        return jsonify({'message': 'Product deleted successfully!'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Could not delete the product, try again', 'error': str(e)}), 500