from app import db
from flask_login import UserMixin

# Product Model
class Product(db.Model):
    """Product Model class"""
    
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(256))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref='products', lazy=True)

    def __repr__(self) -> str:
        return f"< {self.title}>"

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
            setattr(self, key, value)
        db.session.commit()

# User Model
class User(db.Model):
    """User Model class"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    admin = db.Column(db.Boolean, default=False)
    orders = db.relationship('Order', backref='customer', lazy='dynamic')

    def __repr__(self):
        """Return a string representation of the user object"""
        return f"<User {self.username}>"

    def save(self):
        """Save the user to the database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the user from the database"""
        db.session.delete(self)
        db.session.commit()

# Order Model
class Order(db.Model):
    """Order Model class"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='customer_orders')  # Changed from 'orders' to 'customer_orders'

    def __repr__(self):
        return f"<Order {self.id}>"


# OrderProduct Model
class OrderProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False, default=1)

    order = db.relationship('Order', backref='order_products')
    product = db.relationship('Product', backref='order_products')
       
    def __repr__(self):
        return f"OrderProduct {self.order_id} {self.product_id}"
    
class Category(db.Model):
    """Category Model class"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    db.image = db.Column(db.String(100), nullable=False)