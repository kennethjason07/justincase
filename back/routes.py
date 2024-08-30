from flask import Blueprint, request, jsonify
from back.models import db, Order, Worker
from datetime import datetime

main = Blueprint('main', __name__)


#Route for order status check
@main.route('/api/orders/<int:order_id>', methods=['PATCH'])
def update_order_status(order_id):
    data = request.json
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    # Update the order status
    order.order_status = data.get('order_status', order.order_status)
    
    # Save the changes to the database
    db.session.commit()
    
    return jsonify(order.as_dict()), 200


# Route to get today's orders
@main.route('/api/todays-orders', methods=['GET'])
def get_todays_orders():
    today = datetime.today().date()
    orders = Order.query.filter_by(delivery_date=today).all()
    return jsonify([order.as_dict() for order in orders])

# Route to create a new bill
@main.route('/api/new-bill', methods=['POST'])
def create_new_bill():
    data = request.json

    # Debugging: Print received data
    print("Received data:", data)

    # Check if data is provided
    if not data:
        return jsonify({"error": "No data provided."}), 400

    # Validate required fields
    required_fields = ['order_date', 'delivery_date']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"'{field}' is a required field."}), 400

    try:
        # Convert dates from string to date objects
        order_date = datetime.strptime(data['order_date'], '%Y-%m-%d').date()
        delivery_date = datetime.strptime(data['delivery_date'], '%Y-%m-%d').date()
    except ValueError as e:
        print(f"Date conversion error: {e}")
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    try:
        # Create a new order instance
        new_order = Order(
            garment_type=data.get('garment_type'),
            pant_options=data.get('pant_options'),
            shirt_options=data.get('shirt_options'),
            quantity=data.get('quantity'),
            order_date=order_date,
            delivery_date=delivery_date,
            worker_name=data.get('worker_name'),
            customer_name=data.get('customer_name'),
            mobile_number=data.get('mobile_number'),
            order_status="Pending"
        )
        db.session.add(new_order)
        db.session.commit()
    except Exception as e:
        print(f"Error saving to database: {e}")
        return jsonify({"error": "Internal server error"}), 500

    return jsonify({"message": "New bill created successfully"}), 201

# Route to get customer info
@main.route('/api/customer-info/<mobile_number>', methods=['GET'])
def get_customer_info(mobile_number):
    customer_orders = Order.query.filter_by(mobile_number=mobile_number).all()

    if not customer_orders:
        return jsonify({"error": "No orders found for this customer"}), 404

    measurements = {
        "garment_type": customer_orders[0].garment_type,
        "pant_options": customer_orders[0].pant_options,
        "shirt_options": customer_orders[0].shirt_options
    }

    order_history = []
    for order in customer_orders:
        order_info = order.as_dict()
        order_info['status'] = "Completed" if order.delivery_date and order.delivery_date <= datetime.today().date() else "Pending"
        order_history.append(order_info)

    customer_info = {
        "measurements": measurements,
        "order_history": order_history
    }

    return jsonify(customer_info), 200

def order_as_dict(order):
    return {
        'id': order.id,
        'garment_type': order.garment_type,
        'pant_options': order.pant_options,
        'shirt_options': order.shirt_options,
        'quantity': order.quantity,
        'order_date': order.order_date.isoformat() if order.order_date else None,
        'delivery_date': order.delivery_date.isoformat() if order.delivery_date else None,
        'customer_name': order.customer_name,
        'mobile_number': order.mobile_number,
        'order_status': order.order_status
    }

@main.route('/api/worker-info/<worker_name>', methods=['GET'])
def get_worker_info(worker_name):
    # Fetch orders for the specific worker by their name
    orders = Order.query.filter_by(worker_name=worker_name).all()
    
    # Convert orders to a list of dictionaries
    orders_list = [order_as_dict(order) for order in orders]
    
    # Prepare the response data
    response = {
        'name': worker_name,
        'orders': orders_list
    }
    
    return jsonify(response), 200


#Sorting Order By Status
@main.route('/api/orders', methods=['GET'])
def get_orders():
    sort_status = request.args.get('status', 'all')

    query = Order.query

    # Apply status filtering
    if sort_status != 'all':
        query = query.filter(Order.order_status == sort_status)

    # Sort by status
    query = query.order_by(Order.order_status.asc())

    orders = query.all()
    return jsonify([order.as_dict() for order in orders]), 200


# Utility method to convert model to dict
def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# Attach the utility method to the models
Order.as_dict = as_dict
Worker.as_dict = as_dict
