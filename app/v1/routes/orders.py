#!/usr/bin/env python3
""" This module defines the order route and features
"""


from flask import Blueprint, jsonify, request

from app.v1 import db
from app.v1.models import Order, OrderProduct, Product, User
from app.v1.utils.token_manager import token_required


order = Blueprint(import_name=__name__, name="order", url_prefix="/orders")

# Retrieve a list of orders
@order.route('/all', methods=['GET'])
@token_required
def all_order(current_user):
    """
      Retrieve all orders from the database (Admin only)
      ---
    tags:
      - Orders
    security:
      - Bearer: []
    responses:
      200:
        description: List of all orders retrieved successfully
        schema:
          type: object
          properties:
            List of orders:
              type: array
              items:
                type: object
                properties:
                  orderId:
                    type: integer
                    example: 1
                  userId:
                    type: integer
                    example: 2
      403:
        description: Unauthorized - User is not an admin
      500:
        description: Server error while fetching orders
    """

    # Check for admin privilege
    if not current_user.admin:
        return jsonify({'message': 'Unauthorized to perform this function!'}), 403

    # Fetch all orders
    orders = Order.query.all()
    output = [{'orderId': order.id, 'userId': order.user_id} for order in orders]

    # Check if the order is empty
    if not output:
        return jsonify({'message': 'No placed order'})

    # Return list of orders
    return jsonify({'List of orders': output})


# Fetch user orders
@order.route('/<id>', methods=['GET'])
@token_required
def get_user_orders(current_user, id):
    """
    Retrieve all orders for a specific user
    ---
    tags:
      - Orders
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: User ID
    responses:
      200:
        description: User orders retrieved successfully
        schema:
          type: object
          properties:
            Your orders are:
              type: array
              items:
                type: object
                properties:
                  orderId:
                    type: integer
                    example: 1
                  userId:
                    type: integer
                    example: 2
      404:
        description: User not found or no orders found
      500:
        description: Server error while fetching user orders
    """

    # Check if the user is logged in
    if not current_user:
        return jsonify({'message': 'User does not exist'})

    # Query the user by their id
    user = User.query.get(id)

    # Check if user exists
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Get all the orders associated to the user
    user_orders = user.orders

    output = []
    for order in user_orders:
        order_data = {'orderId': order.id, 'userId': order.user_id}
        output.append(order_data)

    if not output:
        return jsonify({'message': 'Orders not found'}), 404

    return jsonify({'Your orders are': output})


# Fetch user order
@order.route('/<id>', methods=['GET'])
@token_required
def get_one_order(current_user, id):
    """
    Retrieve a specific order by its ID
    ---
    tags:
      - Orders
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: Order ID
    responses:
      200:
        description: Order retrieved successfully
        schema:
          type: object
          properties:
            user orders:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                user_id:
                  type: integer
                  example: 2
      404:
        description: Order not found
      500:
        description: Server error while fetching the order
    """

    # Check if the user is logged in
    if not current_user:
        return jsonify({'message': 'User does not exist'})

    # Query the database for orders
    user_order = Order.query.filter_by(id=id).first()

    # Check if order exists
    if not user_order:
        return jsonify({'message': "Order doesn't exist"})

    order_data = {'orderId': user_order.id, 'userId': user_order.user_id}

    if not order_data:
        return jsonify({'message': 'Order not found'}), 404

    return jsonify({'user orders': order_data}), 200

@order.route('/create', methods=['POST'])
@token_required
def create_order(current_user):
    """
    Create a new order for the authenticated user
    ---
    tags:
      - Orders
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - products
          properties:
            products:
              type: array
              items:
                type: object
                properties:
                  product_id:
                    type: integer
                    example: 1
                  quantity:
                    type: integer
                    example: 2
    responses:
      201:
        description: Order created successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Order created successfully"
            order_id:
              type: integer
              example: 1
      400:
        description: Missing required fields
      404:
        description: Product not found
      500:
        description: Server error while creating order
    """

    try:
        data = request.get_json()

        # Check if data is valid and contains a list of products
        if not data or 'products' not in data:
            return jsonify({'message': 'Missing required fields'}), 400

        new_order = Order(user_id=current_user.id)
        db.session.add(new_order)
        db.session.flush()

        products = data['products']

        for item in products:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 1)

            # Check if the product exists
            product = Product.query.get(product_id)
            if not product:
                return jsonify({'message': f'Product with id {product_id} does not exist'}), 404

            order_product = OrderProduct(
                order_id=new_order.id,
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(order_product)

        db.session.commit()

        return jsonify({'message': 'Order created successfully', 'order_id': new_order.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error creating order: {str(e)}'}), 500


# Adding an order update route
@order.route('/<id>', methods=['PUT'])
@token_required
def update_order(current_user, id):
    """
    Update an order associated with the current user
    ---
    tags:
      - Orders
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: Order ID
      - in: body
        name: body
        schema:
          type: object
          properties:
            quantity:
              type: integer
              example: 5
            product_id:
              type: integer
              example: 2
    responses:
      200:
        description: Order updated successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Order has been updated successfully"
      401:
        description: Authentication failed
      404:
        description: Order not found or does not belong to the current user
      500:
        description: Server error while updating order
    """
    if not current_user:
        return jsonify({'message': 'Authentication failed'}), 401

    try:
        data = request.get_json()

        # Check if it belongs to the current user
        existing_order = Order.query.filter_by(id=id, user_id=current_user.id).first()

        if not existing_order:
            msg = 'Order does not exist or does not belong to the current user'
            return jsonify({'message': msg}), 404

        if 'quantity' in data:
            existing_order.quantity = data['quantity']
        if 'product_id' in data:
            existing_order.product_id = data['product_id']

        # Commit the changes to the database
        db.session.commit()

        return jsonify({'message': 'Order has been updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error updating order: {str(e)}'}), 500



@order.route('/delete/<id>/', methods=['DELETE'])
@token_required
def delete_an_order(current_user, id):
    """
    Delete an order associated with the current user
    ---
    tags:
      - Orders
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: Order ID
    responses:
      200:
        description: Order deleted successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Order has been deleted successfully"
      401:
        description: Unauthorized
      404:
        description: Order not found or does not belong to the current user
      500:
        description: Server error while deleting order
    """

    if not current_user:
        return jsonify({'message': 'Unauthorized'}), 401

    try:
        # Query a specific order based on ID
        user_order = Order.query.filter_by(id=id, user_id=current_user.id).first()

        if not user_order:
            msg = 'Order does not exist or does not belong to the current user'
            return jsonify({'message': msg}), 404

        # Delete the order
        db.session.delete(user_order)
        db.session.commit()

        return jsonify({'message': 'Order has been deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error deleting order: {str(e)}'}), 500
