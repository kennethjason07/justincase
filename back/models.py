from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    garment_type = db.Column(db.String(50))
    pant_options = db.Column(db.String(200))
    shirt_options = db.Column(db.String(200))
    quantity = db.Column(db.Integer)
    order_date = db.Column(db.Date)
    delivery_date = db.Column(db.Date)
    worker_name = db.Column(db.String(100))
    customer_name = db.Column(db.String(100))
    mobile_number = db.Column(db.String(20))

class Worker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    completed_orders = db.Column(db.Integer)
    pending_orders = db.Column(db.Integer)
