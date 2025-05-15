from flask import Blueprint, request, jsonify
from services.history_service import get_orders_by_filters

history_routes = Blueprint('history_routes', __name__)

@history_routes.route('/api/history')
def api_history():
    filters = {
        'start': request.args.get('start'),
        'end': request.args.get('end'),
        'table': request.args.get('table'),
        'paid': request.args.get('paid'),
        'min': request.args.get('min'),
        'max': request.args.get('max')
    }
    orders = get_orders_by_filters(filters)
    return jsonify(orders)