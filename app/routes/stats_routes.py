from flask import Blueprint, request, jsonify
from services.stats_service import get_statistics

stats_routes = Blueprint('stats_routes', __name__)

@stats_routes.route('/api/stats')
def api_stats():
    start = request.args.get('start')
    end = request.args.get('end')
    if not start or not end:
        return jsonify({'error': 'Brak zakresu dat'}), 400

    stats = get_statistics(start, end)
    return jsonify(stats)