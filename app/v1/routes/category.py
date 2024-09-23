from flask import Blueprint
from flask import request, jsonify
from app.v1.models import Category
from app.v1 import db

from app.v1.utils.token_manager import token_required

category = Blueprint(import_name=__name__, name="category", url_prefix="/categories")

@category.route('/', methods=['POST'])
@token_required
def create_category(current_user):
    """create a category"""
    if not current_user.admin:
        return jsonify({ 'message' : 'Unauthorized'}), 403
     
    data = request.get_json()
    
    # check if fields are provided
    if not 'name' and 'description' in data:
        return jsonify({'message': 'Missing fields'}), 400

    # check for existing Category
    existing_category = Category.query.filter(Category.name==data['name'].lower().strip()).first()
    if existing_category:
        return jsonify({'message': 'Category already exist'}), 400
    
    try:
        new_category = Category(
            id = data['id'],
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



@category.route('/', methods=['GET'])
@token_required
def get_all_categories(current_user):
    """Retrieve list of categories."""
    # Check for admin priviledges
    if not current_user.admin:
        return jsonify({'message': 'Unauthorized'}), 403
    
    # Query the database list of Categories
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




@category.route('/<id>', methods=['GET'])
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



@category.route('/<id>', methods=['PUT'])
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
        if 'name' in data:
            existing_category.name = data.get('name', existing_category.name)
        if 'description' in data:
            existing_category.description = data('description', existing_category.description)

        db.session.commit()

        return jsonify({
            'message': 'Category Succesfully updated',
            'id': existing_category.id,
            'name': existing_category.name,
            'description': existing_category.description
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating the category'})


@category.route('/<id>', methods=['DELETE'])
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

