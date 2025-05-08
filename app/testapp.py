from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    # Przekierowanie do strony głównej (menu)
    return render_template('menu.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/order')
def order():
    # Pobierz numer stolika, jeśli został przekazany
    table = request.args.get('table', default=None, type=int)
    return render_template('order.html', table=table)

@app.route('/clients')
def clients():
    # Placeholder dla strony klientów
    return "Strona klientów - w przygotowaniu"

@app.route('/statistics')
def statistics():
    # Placeholder dla strony statystyk
    return "Strona statystyk - w przygotowaniu"

@app.route('/tables')
def tables():
    return render_template('tables.html')

if __name__ == '__main__':
    app.run(debug=True)