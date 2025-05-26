# app.py
from flask import Flask, render_template, request, redirect, session
from services.menu_service import get_menu_data

#sesja
from datetime import timedelta

app = Flask(__name__) # Utworzenie instancji Flask
app.secret_key = 'supersekretnyklucz'
app.permanent_session_lifetime = timedelta(hours=2)
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False

from routes.auth_routes import auth_routes
app.register_blueprint(auth_routes)

# import i rejestracja blueprintów po utworzeniu `app`
from routes.order_routes import order_routes
app.register_blueprint(order_routes)

from routes.history_routes import history_routes
app.register_blueprint(history_routes)

from routes.stats_routes import stats_routes
app.register_blueprint(stats_routes)

from routes.users_routes import users_routes
app.register_blueprint(users_routes)

@app.route('/')
def index():
    return render_template('menu.html', menu=get_menu_data())

@app.route('/login')
@app.route('/login.html')
def login_page():
    return render_template('login.html')

@app.route('/register')
@app.route('/register.html')
def register_page():
    return render_template('register.html')

@app.route('/menu')
def menu_page():
    menu = get_menu_data()
    return render_template('menu.html', menu=menu)

@app.route('/order')
def order_page():
    return render_template('order.html')

@app.route('/users')
def users_page():
    return render_template('users.html')

@app.route('/stats')
def stats_page():
    return render_template('stats.html')

@app.route('/users/edit/<int:client_id>')
def edit_client_page(client_id):
    return render_template('edit_users.html')

@app.route('/users/add')
def add_user_page():
    return render_template('add_user.html')

@app.before_request
def restrict_access():
    public_paths = ['/login', '/login.html', '/register', '/register.html', '/api/login', '/api/register']
    static_extensions = ('.js', '.css', '.png', '.jpg', '.ico', '.html')

    if request.path in public_paths or request.path.endswith(static_extensions):
        return

    user = session.get('user')
    if not user:
        return redirect('/login.html')

    role = user.get('role')

    # Ogranicz dostęp na podstawie roli
    if role == 'Klient':
        if request.path not in ['/menu', '/']:
            return "Brak dostępu", 403
    elif role == 'Kelner':
        if request.path.startswith('/users'):
            return "Brak dostępu", 403
    # Admin ma dostęp do wszystkiego

if __name__ == '__main__':
    app.run(debug=True)