from flask import Blueprint, jsonify, request
from services.users_service import get_all_users, get_user, update_user, delete_user

users_routes = Blueprint('users_routes', __name__)

@users_routes.route('/api/users')
def api_get_users():
    return jsonify(get_all_users())

@users_routes.route('/api/users/<int:user_id>')
def api_get_user(user_id):
    user = get_user(user_id)
    return jsonify(user) if user else ('', 404)

@users_routes.route('/api/users/<int:user_id>', methods=['PUT'])
def api_update_user(user_id):
    data = request.get_json()
    data['id'] = user_id
    update_user(data)
    return jsonify({'status': 'Zaktualizowano'})

@users_routes.route('/api/users/<int:user_id>', methods=['DELETE'])
def api_delete_user(user_id):
    delete_user(user_id)
    return jsonify({'status': 'Usunięto'})