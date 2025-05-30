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

Dane poniżej dotyczą katalogu app\

[nie trzeba] Tworzenie wirtualnego środowiska python:
python -m venv venv | Jeśli chcemy stworzyć nowe. Jest dodane przeze mnie do folderu

venv\Scripts\activate

[od tego punktu i dalej trzeba] Instalacja bibliotek:
pip install -r requirements.txt | Jeśli nie chcecie instalować z szablonu, w pliku requirements są wymagane wersje bibliotek.

Jeśli nie mamy, pobieramy ODBC w wersji 17 ze strony. Jeśli mamy, wystarczy skonfigurować.
https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16#download-for-windows

Konfiguracja ODBC:
1. Wchodzimy w ODBC 64bit
2. Systemowe DSN (2 zakładka)
3. Dodaj
4. ODBC Driver 2017 for SQL Server
5. Name: restauracjadb
   SQL Server: localhost | może być nazwa urządzenia w Windowsie 
6. Integrated Windows authentication 
7. Change default database to: restauracjadb (reszta domyślnie)
8. Test Data Source (u mnie wyskoczyło okno 
		"Microsoft ODBC Driver for SQL Server Version 17.10.0006

		Running connectivity tests...

		Attempting connection
		Connection established
		Verifying option settings
		Disconnecting from server

		TESTS COMPLETED SUCCESSFULLY!"

Sprawdzamy połączenie uruchamiając skrypt test.py z katalogu /app. Jeśli wszystko działa, to komunikat == "Połączono z bazą danych!"

Instalujemy bibliotekę python-dotenv-1.1.0
pip install python-dotenv

Instalujemy Flaska
pip install Flask

uruchamiamy serwer Flask poprzez
python app.py

aplikacja będzie dostępna w przeglądarce pod adresem 127.0.0.1:5000 lub localhost:5000

-----------------------------------------
Struktura plików:

app/
│
├── app.py                 # Główna aplikacja Flask — inicjalizacja aplikacji i rejestracja blueprintów
├── db.py                  # Łączenie z bazą danych MSSQL (przez pyodbc, .env)
├── .env                   # Zmienne środowiskowe (połączenie do bazy - DRIVER, Server, Database, Trusted Connections)
├── requirements.txt       # Lista zależności
├── README.md              # Dokumentacja projektu
├── test.py                # Test połączenia z bazą
├── testapp.py             # Alternatywny / testowy punkt wejścia
│
├── routes/                # Endpointy HTTP – logika tras
│   ├── auth_routes.py         # Logowanie i wylogowanie użytkowników, sesje
│   ├── history_routes.py      # Historia zamówień
│   ├── menu_routes.py         # Wyświetlanie i zarządzanie pozycjami menu
│   ├── order_routes.py        # Obsługa zamówień (dodawanie, modyfikacja, statusy)
│   ├── stats_routes.py        # API i widok dla statystyk
│   └── users_routes.py        # Zarządzanie użytkownikami (CRUD)
│
├── services/              # Logika oddzielona od warstwy tras
│   ├── history_service.py     # Pobieranie i filtrowanie historii zamówień
│   ├── menu_service.py        # Operacje na pozycjach menu
│   ├── order_service.py       # Obsługa logiki zamówień i płatności
│   ├── stats_service.py       # Generowanie danych do wykresów/statystyk
│   └── users_service.py       # Operacje na użytkownikach (rejestracja, lista, edycja)
│
├── templates/             # Szablony HTML renderowane przez Flask
│   ├── add_user.html          # Formularz dodawania nowego użytkownika
│   ├── edit_users.html        # Formularz edycji danych użytkownika
│   ├── history.html           # Widok historii zamówień
│   ├── login.html             # Formularz logowania
│   ├── menu.html              # Widok pozycji z menu
│   ├── order.html             # Widok zamówień z podziałem na stoliki i kategorie
│   ├── register.html          # Formularz rejestracyjny
│   ├── stats.html             # Panel statystyk restauracyjnych
│   └── users.html             # Lista użytkowników (widok admina)
│
├── static/                # Pliki statyczne (style, JS, obrazki)
│   ├── css/
│   │   └── css.css            # Globalny arkusz stylów css
│   ├── favicon/               # Favicon
│   └── images/                # Obrazy potraw, UI itp.

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