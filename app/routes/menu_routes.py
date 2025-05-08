# routes/menu_routes.py
from flask import Blueprint, jsonify
from services.menu_service import get_menu_data

menu_routes = Blueprint('menu_routes', __name__)

@menu_routes.route('/api/menu', methods=['GET'])
def api_menu():
    menu = get_menu_data()
    return jsonify(menu)