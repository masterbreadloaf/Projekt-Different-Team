# routes/order_routes.py
from flask import Blueprint, jsonify, request, render_template
from services.order_service import (
    get_available_menu, get_available_tables, get_alergeny,
    save_order, get_last_order_by_table,
    mark_order_as_paid, update_order, update_table_status,
    get_all_orders_with_details
)
from db import get_connection

order_routes = Blueprint('order_routes', __name__)

@order_routes.route('/order')
def order_page():
    menu = get_available_menu()
    return render_template('order.html', menu=menu)

@order_routes.route('/api/tables')
def get_tables():
    return jsonify(get_available_tables())

@order_routes.route('/api/alergeny')
def get_alergeny_list():
    return jsonify(get_alergeny())

@order_routes.route('/api/order', methods=['POST'])
def submit_order():
    data = request.get_json()
    order_id = save_order(data)
    return jsonify({"order_id": order_id})

@order_routes.route('/api/orders/last/<int:table_id>')
def get_last_order_for_table(table_id):
    order = get_last_order_by_table(table_id)
    return jsonify(order)

@order_routes.route('/api/orders/<int:order_id>', methods=['PATCH'])
def patch_order(order_id):
    data = request.get_json()
    update_order(order_id, data["items"])
    return jsonify({"success": True})

@order_routes.route('/api/orders/pay/<int:order_id>', methods=['POST'])
def pay_order(order_id):
    mark_order_as_paid(order_id)
    return jsonify({"success": True})

@order_routes.route('/api/tables/<int:table_id>/status', methods=['POST'])
def change_table_status(table_id):
    data = request.get_json()
    update_table_status(table_id, data['status'])
    return jsonify({"status": data['status']})

@order_routes.route("/history")
def history_page():
    return render_template("history.html")

@order_routes.route("/api/orders/history")
def api_orders_history():
    orders = get_all_orders_with_details()
    return jsonify(orders)