# app.py
from flask import Flask, render_template, request
from services.menu_service import get_menu_data

app = Flask(__name__)  # Utworzenie instancji Flask

# import i rejestracja blueprintów po utworzeniu `app`
from routes.order_routes import order_routes
app.register_blueprint(order_routes)

from routes.history_routes import history_routes
app.register_blueprint(history_routes)

from routes.stats_routes import stats_routes
app.register_blueprint(stats_routes)

@app.route('/')
def index():
    return render_template('menu.html', menu=get_menu_data())

@app.route('/menu')
def menu_page():
    menu = get_menu_data()
    return render_template('menu.html', menu=menu)

@app.route('/order')
def order_page():
    return render_template('order.html')

@app.route('/clients')
def clients_page():
    return render_template('clients.html')

@app.route('/stats')
def stats_page():
    return render_template('stats.html')

@app.route('/tables')
def tables_page():
    return render_template('tables.html')

if __name__ == '__main__':
    app.run(debug=True)