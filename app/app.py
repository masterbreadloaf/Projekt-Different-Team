# app.py
from flask import Flask, render_template
from services.menu_service import get_menu_data

app = Flask(__name__)

@app.route('/menu')
def menu_page():
    menu = get_menu_data()
    return render_template('menu.html', menu=menu)

if __name__ == '__main__':
    app.run(debug=True)