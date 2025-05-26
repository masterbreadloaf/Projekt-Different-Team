# app/routes/auth_routes.py
from flask import Blueprint, request, jsonify, session
from db import get_connection

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/api/login', methods=['POST'])
def login():
    data = request.json
    login = data['login']
    password = data['password']

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT UZY_IdUzytkownika, UZY_Login, UZY_Email, UZY_Haslo, UZY_Typ, UZY_Aktywny
        FROM uzytkownicy
        WHERE UZY_Login = ?
    """, (login,))

    row = cursor.fetchone()
    if not row:
        return jsonify({'error': 'Nieprawidłowy login lub hasło'}), 401

    if row.UZY_Haslo != password:
        return jsonify({'error': 'Nieprawidłowy login lub hasło'}), 401

    if not row.UZY_Aktywny:
        return jsonify({'error': 'Konto jest nieaktywne'}), 403

    session['user'] = {
        'id': row.UZY_IdUzytkownika,
        'login': row.UZY_Login,
        'email': row.UZY_Email,
        'role': row.UZY_Typ
    }

    conn.close()
    return jsonify({'success': True})

@auth_routes.route('/api/register', methods=['POST'])
def register():
    data = request.json
    login = data['login']
    email = data['email']
    password = data['password']

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM uzytkownicy WHERE UZY_Login = ? OR UZY_Email = ?", (login, email))
    if cursor.fetchone():
        return jsonify({'error': 'Użytkownik z takim loginem lub emailem już istnieje'}), 400

    cursor.execute("""
        INSERT INTO uzytkownicy (UZY_Login, UZY_Email, UZY_Haslo, UZY_Typ, UZY_Aktywny, UZY_DataUtworzenia, UZY_OstatnieLogowanie)
        VALUES (?, ?, ?, 'Klient', 1, GETDATE(), GETDATE())
    """, (login, email, password))

    conn.commit()
    conn.close()
    return jsonify({'success': True})