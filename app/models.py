from app import db

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer(), primary_key=True)  # Unique identifier for each product
    title = db.Column(db.String(100), nullable=False)  # Product title, required field
    description = db.Column(db.String(1024), nullable=False)  # Product description, required field
    price = db.Column(db.Float(), nullable=False)  # Product price, required field
    image = db.Column(db.String(255), nullable=True)  # Optional image URL
    orders = db.relationship('Order', backref='product')  # Relationship with Order model

    def __repr__(self) -> str:
        return f"<Product {self.title}>"  # String representation of the object
    
    def save(self):
        """Save changes made to the product instance to the database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete a specific product from the database"""
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        """Update the product with new data passed as keyword arguments"""
        for key, value in kwargs.items():
            setattr(self, key, value)  # Dynamically update attributes
        db.session.commit()

# User Model
class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)  # Unique identifier for each user
    username = db.Column(db.String(150), unique=True, nullable=False)  # Username, required and unique
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email, required and unique
    password = db.Column(db.String(60), nullable=False)  # Password, required but not unique
    phone_no = db.Column(db.String(20), unique=True, nullable=False)  # Phone number, stored as a string
    orders = db.relationship('Order', backref='user', lazy='dynamic')  # Relationship with Order model

    def __repr__(self):
        """Return a string representation of the user object"""
        return f"<User {self.username}>"

    def save(self):
        """Save the user to the database"""
        db.session.add(self)
        db.session.commit()

"""
Order Model
    Attributes:
        id (primary key)
        user_id (foreign key referencing the User model)
        cart_id (foreign key referencing the Cart model)
        status (e.g. "pending", "shipped", "delivered")
        payment_method
        payment_status
        shipping_address
        shipping_cost
    Methods:
        update_status(status)
        update_payment_status(status)
        update_shipping_address(address)
    get_total_cost()
"""
# Order Model
class Order(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    
    # ForeignKey to Product model
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    # ForeignKey to User model
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # foreign key referencing the Cart model
    cart_id = db.Column(db.Integer, db.ForeignKey('cart'))

    status = db.Column(db.Text, nullable=True)

    payment_method = db.Column(db.String(), unique=False)

    shipping_address = db.Column(db.Text, unique=False)

    shipping_cost = db.Column(db.Integer)

    def user_order(self):
        """Fetch a user and their oders"""
        user = User.query.get(1)
        for order in user.order.all():
            return order
        
    def update_status(status):
        """"""

    def update_payment_status(status):
        """"""

    def update_shipping_address(address):
        """"""

    def get_total_cost():
        """"""
        

"""

Cart Model

Attributes:
id (primary key)
user_id (foreign key referencing the User model)
items (relationship with CartItem model)
Methods:
add_item(product_id, quantity)
remove_item(product_id)
update_quantity(product_id, quantity)
get_total_price()
checkout()

"""


class Cart(db.model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_id'), nullable=False)
    items = db.relationship('CartItem', backref='cart', lazy=True)

    def add_item(product_id, quantity):
        """"""
    def remove_item(product_id):
        """"""
    def update_quantity(product_id, quantity):
        """"""

    def get_total_price():
        """"""
    def checkout():
        """"""

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    Product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity =db.Column(db.Integer, nullable=False, default=1)

    product = db.relationship('Product')

    def get_total_price(self):
        """Calculates the total price for this cart item"""
        return self.quantity * self.product.price


"""
Relationships:

A Cart has many CartItems.
A CartItem belongs to one Cart.
An Order belongs to one Cart.
An Order has one User.
A User has many Orders.

"""