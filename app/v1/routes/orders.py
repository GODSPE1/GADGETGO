#!/usr/bin/env python3
""" This module defines the order route and features
"""


from flask import request, jsonify
from app.v1.models import Order, User, Product, OrderProduct
from app.v1 import db
from flask import Blueprint
from app.v1.utils.token_manager import token_required


order = Blueprint(import_name=__name__, name="order", url_prefix="/orders")

# Retrieve a list of orders
@order.route('/all', methods=['GET'])
@token_required
def all_order(current_user):
    """Get all the order in the database"""

    try:
#       Check for admin priviledge
        if not current_user.admin:
            return jsonify({'message': 'Unauthorized to perform this function!'}), 403

        # Fetch all orders
        orders = Order.query.all()
        output = [{'orderId': order.id, 'userId': order.user_id} for order in orders]
        
        # check if the order is empty
        if not output:
            return ({'message': 'No placed order'})
        
        #return list of orders
        return jsonify({'List of orders': output})
    
    except Exception as e:
        return jsonify({'message': 'Error Fetching orders'}), 500


# Fetch user orders
@order.route('/<id>', methods=['GET'])
@token_required
def get_user_orders(current_user, id):
    """Get all orders associated to a specific user"""

    try:
        #check if the user is logged in
        if not current_user:
            return jsonify({ 'message': 'User does not exit'})
        
        #Query the user by their id
        user= User.query.get(id)

        # check if user exist
        if not user:
            return jsonify({ 'message': 'User not found'}), 404
        
        #get all the orders associated to the user
        user_orders = user.orders

        output = []
        for order in  user_orders:
            order_data = {'orderId': order.id, 'userId': order.user_id}
            output.append(order_data)

        if not output:
            return ({'message': 'Orders not found'}), 404
    
        return jsonify({'Your orders are': output})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error fecthing the order'}), 500


# Fetch user order
@order.route('/<id>', methods=['GET'])
@token_required
def get_one_order(current_user, id):
    """get a specfic order for the user"""

    try:
        #check if the user is logged in
        if not current_user:
            return jsonify({ 'message': 'User does not exit'})
        
        #Query the database for orders
        user_oder = Order.query.filter_by(id=id).first()

        # check if user exist
        if not user_oder:
            return jsonify({ 'message': 'order doesn\'t exist'})
        
        order_data = {'orderId': user_oder.id, 'userId': user_oder.user_id}
        
        if not order_data:
            return jsonify({'message': 'Order not found'}), 404
        

        return jsonify({'user orders': user_oder})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error fecthing the order'}), 500


@order.route('/create', methods=['POST'])
@token_required
def create_order(current_user):
    """Create a new order for the user

    Return: the order id
    """

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


@order.route('/<id>', methods=['PUT'])
@token_required
def update_order(current_user, id):
    """Update an order associated with a user"""
    if not current_user:
        return jsonify({'message': 'Authentication failed'}), 401
    
    data = request.get_json()

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



@order.route('/delete/<id>/', methods=['DELETE'])
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
