from app.v1.models.base_model import db

# Order Model
class Order(db.Model):
    """Order Model class"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<Order {self.id}>"


# OrderProduct Model
class OrderProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False, default=1)

    order = db.relationship('Order', backref='orderproducts', cascade="all, delete")
    product = db.relationship('Product', backref='orderproducts', cascade="all, delete")
       
    def __repr__(self):
        return f"OrderProduct {self.order_id} {self.product_id}"
    