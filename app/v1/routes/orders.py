from flask import request, jsonify
from app.v1.models import Order
from app.v1 import db
from flask import Blueprint

from app.v1.utils.token_manager import token_required


order = Blueprint(import_name=__name__, name="order", url_prefix="/orders")

# Retrieve a list of orders
@token_required
def all_order(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Unauthorized to perform this function!'}), 403

    orders = Order.query.all()  # Fetch all orders
    output = [{'orderId': order.id, 'userId': order.user_id} for order in orders]
    
    return jsonify({'List of orders': output})



# Fetch user orders
@order.route('/<id>', methods=['GET'])
@token_required
def get_one_order(current_user):
    """get a specfic oder for the user"""
    if not current_user:
        return jsonify({ 'message': 'User does not exit'})
    
    current_user_oder = current_user.order

    if not current_user_oder:
        return jsonify({ 'message': 'order doesn\'t exist'})
    
    return jsonify({'user orders': current_user_oder})



@order.route('', methods=['POST'])
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



@order.route('/<id>', methods=['PUT'])
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



@order.route('/<id>/', methods=['DELETE'])
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
