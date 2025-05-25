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
    cursor.execute("""
        UPDATE uzytkownicy
        SET UZY_Login = ?, UZY_Haslo = ?, UZY_Email = ?, UZY_Typ = ?, UZY_Aktywny = ?
        WHERE UZY_IdUzytkownika = ?
    """, (
        data['login'],
        data['password'],  # ← surowe hasło
        data['email'],
        data['role'],
        int(data['active']),
        data['id']
    ))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM uzytkownicy WHERE UZY_IdUzytkownika = ?", (user_id,))
    conn.commit()
    conn.close()