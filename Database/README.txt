Tutaj będą się pojawiały elementy dotyczące bazy danych. Aktualny postęp prac: Wdrażanie CRUD w bazie MS SQL

Baza tworzona na:
-Microsoft SQL Server 2022 Express
-Windows 10 Pro x64

Baza do zaimportowania do SMSS za pomocą pliku restauracjadb_export.bacpac.

Ścieżka importu:
1) Do zainstalowania Microsoft SQL Server 2022 Express
2) Do zainstalowania Microsoft SQL Managment Studio, najlepiej 19 lub 20
3) Przy pierwszej konfiguracji pakietu komputer uruchamiamy ponownie
4) Uruchamiamy SQL Server jeśli jeszcze nie został uruchomiony (domyślnie włączone w autostarcie)
5) Wchodzimy do SMSS, aktualnie Encryption: Optional, klikamy connect
6) Po załadowaniu zawartości serwera bazę importujemy ścieżką:
	-prawy przycisk myszy na Databases
	-Import Data-tier Application
	-Next
	-Wybieramy plik bacpac z dysku, next
	-Nazwa bazy najlepiej żeby została domyślna
	-Lokalizacja bazy może być domyślna, może być customowa. Testowane na niezależnym środowisku i nie robi to różnicy
	-Finish

Po wykonaniu powyższych kroków baza zostanie zaimportowana w całości. Aby usunąć bazę rozwijamy Databases, PPM na naszą bazę i Delete.

-----------------------------------------
Problem z uruchomieniem SQL Server Agent?

PPM > Właściwości/Properties > Service > Start Mode przełączyć z Disabled na Automatic > Zastosuj/Apply

https://www.youtube.com/watch?v=PM-3LiG5rfQ
-----------------------------------------
ROZWÓJ:

Do skonfigurowania:
-ODBC jako źródło danych serwera SQL

Do instalacji i napisania:
-instalacja bibliotek
	sqlalchemy (nmp install sqlalchemy)
	flask, pyodbc, python-dotenv (pip install flask pyodbc python-dotenv)
-do napisania db.py

-----------------------------------------
Proponowana struktura plików:

restaurant_app/ - Główna struktura aplikacji restauracyjnej opartej na Flask, MS SQL Server i Bootstrap.

├── app.py
    - Główna aplikacja Flask, uruchamiana lokalnie.
    - Rejestruje blueprinty (moduły), inicjuje serwer.

├── db.py
    - Zawiera funkcję get_connection() do łączenia się z bazą przez ODBC (pyodbc).
    - Ładuje dane z .env (np. DRIVER, SERVER, UID).

├── .env
    - Plik konfiguracyjny z danymi dostępowymi do bazy danych (MS SQL Server).

├── requirements.txt
    - Lista wymaganych bibliotek (Flask, pyodbc, python-dotenv itd.).

├── README.md
    - Opis projektu, instrukcje uruchomienia, uwagi dla zespołu.

├── auth/
│   ├── auth_routes.py
│   │   - Obsługa tras logowania (/login) i wylogowania (/logout).
│   └── auth_service.py
│       - Walidacja użytkownika, sprawdzanie hasła w bazie.

├── routes/
│   ├── table_routes.py - Trasy do zarządzania stolikami.
│   ├── menu_routes.py - Trasy do zarządzania menu.
│   ├── order_routes.py - Trasy do zamówień.
│   ├── client_routes.py - Trasy do klientów.
│   └── stats_routes.py - Trasy do statystyk.

├── services/
│   ├── table_service.py - Logika dotycząca stolików.
│   ├── menu_service.py - Logika menu.
│   ├── order_service.py - Obsługa operacji zamówień.
│   ├── client_service.py - Obsługa danych klientów.
│   └── stats_service.py - Obliczenia statystyczne.

├── templates/
│   ├── base.html - Główny szablon HTML z menu bocznym.
│   ├── login.html - Formularz logowania.
│   ├── tables.html - Widok zarządzania stolikami.
│   ├── menu.html - Widok menu.
│   ├── orders.html - Widok zamówień.
│   ├── clients.html - Widok klientów.
│   └── stats.html - Widok statystyk.

├── static/
│   ├── css/
│   │   └── styles.css - Własne style (opcjonalnie przy Bootstrapie).
│   └── js/
│       └── scripts.js - Skrypty JavaScript (np. dynamiczne akcje).

Przykładowa trasa dla auth/auth_routes.py:
___________________________________


from flask import Blueprint, render_template, request, redirect, session
from auth.auth_service import verify_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        if verify_user(login, password):
            session['user'] = login
            return redirect('/tables')
        return render_template('login.html', error="Błędne dane logowania")
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

____________________________________

Przykładowy plik auth/auth_service.py

____________________________________


from db import get_connection

def verify_user(login, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT UZY_Haslo FROM uzytkownicy WHERE UZY_Login = ?", (login,))
    row = cursor.fetchone()
    return row and row[0] == password


________________________________

Przykładowy plik templates/login.html

________________________________
<!DOCTYPE html>
<html>
<head>
  <title>Logowanie</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body>
  <div class="container mt-5" style="max-width: 400px;">
    <h3>Zaloguj się</h3>
    {% if error %}
      <div class="alert alert-danger">{{ error }}</div>
    {% endif %}
    <form method="POST">
      <div class="mb-3">
        <label>Login</label>
        <input type="text" name="login" class="form-control" required>
      </div>
      <div class="mb-3">
        <label>Hasło</label>
        <input type="password" name="password" class="form-control" required>
      </div>
      <button class="btn btn-primary">Zaloguj</button>
    </form>
  </div>
</body>
</html>

_____________________________________________

Przykładowy plik app.py

_____________________________________________

from flask import Flask, session, redirect
from auth.auth_routes import auth_bp
from routes.table_routes import table_bp
from routes.menu_routes import menu_bp
from routes.order_routes import order_bp
from routes.client_routes import client_bp
from routes.stats_routes import stats_bp

app = Flask(__name__)
app.secret_key = 'tajny_klucz'

app.register_blueprint(auth_bp)
app.register_blueprint(table_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(order_bp)
app.register_blueprint(client_bp)
app.register_blueprint(stats_bp)

@app.before_request
def require_login():
    if 'user' not in session and not (request.endpoint or "").startswith("auth."):
        return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)

_________________________________

Przykładowy plik db.py (połączenie przez ODBC)

________________________________

import pyodbc
import os
from dotenv import load_dotenv
load_dotenv()

def get_connection():
    conn_str = (
        f"DRIVER={os.getenv('DB_DRIVER')};"
        f"SERVER={os.getenv('DB_SERVER')};"
        f"DATABASE={os.getenv('DB_NAME')};"
        f"UID={os.getenv('DB_USER')};"
        f"PWD={os.getenv('DB_PASS')};"
    )
    return pyodbc.connect(conn_str)

__________________________________
Przykładowy plik .env

__________________________________

DB_DRIVER={ODBC Driver 17 for SQL Server}
DB_SERVER=localhost
DB_NAME=restauracjadb
DB_USER=sa
DB_PASS=TwojeHaslo

-------------------------------------------