# routes/order_routes.py
from flask import Blueprint, render_template, request, jsonify
from services.order_service import (
    get_available_menu,
    get_available_tables,
    get_alergeny,
    save_order,
    get_last_order_by_table,
    mark_order_as_paid,
    update_table_status
)

order_routes = Blueprint('order_routes', __name__)

@order_routes.route('/order')
def order_page():
    menu = get_available_menu()
    return render_template('order.html', menu=menu)

@order_routes.route('/api/order', methods=['POST'])
def submit_order():
    data = request.get_json()
    try:
        order_id = save_order(data)
        return jsonify({'status': 'success', 'order_id': order_id})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@order_routes.route('/api/tables', methods=['GET'])
def get_tables():
    return jsonify(get_available_tables())

@order_routes.route('/api/alergeny', methods=['GET'])
def get_alergeny_list():
    return jsonify(get_alergeny())

@order_routes.route('/api/orders/last/<int:table_id>', methods=['GET'])
def get_last_order_for_table(table_id):
    order = get_last_order_by_table(table_id)
    if not order:
        return jsonify({'error': 'Brak zamówienia'}), 404
    return jsonify(order)

@order_routes.route('/api/orders/pay/<int:order_id>', methods=['POST'])
def pay_order(order_id):
    mark_order_as_paid(order_id)
    return jsonify({'status': 'ok'})

@order_routes.route('/api/tables/<int:table_id>/status', methods=['POST'])
def update_table_status_route(table_id):
    data = request.get_json()
    update_table_status(table_id, data['status'])
    return jsonify({'status': 'updated'})