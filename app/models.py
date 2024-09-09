from app import db
from datetime import datetime

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer(), primary_key=True)  # Unique identifier for each product
    title = db.Column(db.String(100), nullable=False)  # Product title, required field
    description = db.Column(db.String(1024), nullable=False)  # Product description, required field
    price = db.Column(db.Float(), nullable=False)  # Product price, required field
    image = db.Column(db.String(255), nullable=True)  # Optional image URL

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

    def __repr__(self):
        """Return a string representation of the user object"""
        return f"<User {self.username}>"

    def save(self):
        """Save the user to the database"""
        db.session.add(self)
        db.session.commit()
