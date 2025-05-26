from db import get_connection

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT UZY_IdUzytkownika, UZY_Login, UZY_Haslo, UZY_Email, UZY_Typ, UZY_DataUtworzenia, UZY_Aktywny
        FROM uzytkownicy
    """)
    users = [{
        'id': row[0],
        'login': row[1],
        'password': row[2],
        'email': row[3],
        'type': row[4],
        'created': row[5].isoformat() if row[5] else None,
        'active': bool(row[6])
    } for row in cursor.fetchall()]

    cursor.close()
    conn.close()
    return users

def get_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT UZY_IdUzytkownika, UZY_Login, UZY_Haslo, UZY_Email, UZY_Typ, UZY_Aktywny
        FROM uzytkownicy WHERE UZY_IdUzytkownika = ?
    """, (user_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    return {
        'id': row[0],
        'login': row[1],
        'password': row[2],
        'email': row[3],
        'role': row[4],
        'active': row[5]
    }

def update_user(data):
    conn = get_connection()
    cursor = conn.cursor()

    # sprawdzenie duplikatu loginu (pomijając aktualnego użytkownika)
    cursor.execute("""
        SELECT COUNT(*) FROM uzytkownicy WHERE UZY_Login = ? AND UZY_IdUzytkownika != ?
    """, (data['login'], data['id']))
    if cursor.fetchone()[0] > 0:
        raise ValueError("Login jest już zajęty przez innego użytkownika.")

    # sprawdzenie duplikatu emaila
    cursor.execute("""
        SELECT COUNT(*) FROM uzytkownicy WHERE UZY_Email = ? AND UZY_IdUzytkownika != ?
    """, (data['email'], data['id']))
    if cursor.fetchone()[0] > 0:
        raise ValueError("Email jest już zajęty przez innego użytkownika.")

    # aktualizacja danych
    cursor.execute("""
        UPDATE uzytkownicy
        SET UZY_Login = ?, UZY_Haslo = ?, UZY_Email = ?, UZY_Typ = ?, UZY_Aktywny = ?
        WHERE UZY_IdUzytkownika = ?
    """, (data['login'], data['password'], data['email'], data['role'], data['active'], data['id']))

    conn.commit()
    cursor.close()
    conn.close()

def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM uzytkownicy WHERE UZY_IdUzytkownika = ?", (user_id,))
    conn.commit()
    conn.close()

def create_user(data):
    conn = get_connection()
    cursor = conn.cursor()

    # Sprawdzenie, czy istnieje użytkownik z tym samym loginem lub emailem
    cursor.execute("""
        SELECT COUNT(*) FROM uzytkownicy WHERE UZY_Login = ? OR UZY_Email = ?
    """, (data['login'], data['email']))
    exists = cursor.fetchone()[0]

    if exists > 0:
        raise ValueError("Użytkownik o takim loginie lub emailu już istnieje.")

    cursor.execute("""
        INSERT INTO uzytkownicy (UZY_Login, UZY_Haslo, UZY_Email, UZY_Typ, UZY_Aktywny, UZY_DataUtworzenia, UZY_OstatnieLogowanie)
        VALUES (?, ?, ?, ?, ?, GETDATE(), GETDATE())
    """, (data['login'], data['password'], data['email'], data['role'], data['active']))



    conn.commit()
    cursor.close()
    conn.close()