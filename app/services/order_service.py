from db import get_connection

def get_available_menu():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.MEN_IdPozycji, m.MEN_Nazwa, m.MEN_Cena, m.MEN_CzasPrzygotowania,
               m.MEN_Kategoria, z.ZDJ_NazwaPliku
        FROM menu m
        LEFT JOIN zdjeciamenu z ON m.MEN_IdPozycji = z.MEN_IdPozycji
        WHERE m.MEN_Dostepnosc = 1
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    menu = {}
    for row in rows:
        category = row[4].lower()
        item = {
            'id': row[0],
            'name': row[1],
            'price': float(row[2]),
            'prep_time': int(row[3]),
            'image': f'static/images/menu/{row[5]}' if row[5] else 'images/placeholder.jpg'
        }
        menu.setdefault(category, []).append(item)
    return menu

def get_available_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT STO_IdStolika, STO_Numer, STO_Status
        FROM stoliki
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [
        {'id': row[0], 'number': row[1], 'status': row[2]}
        for row in rows
    ]

def get_alergeny():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ALR_Nazwa FROM alergeny")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [row[0] for row in rows]

def save_order(order_data):
    conn = get_connection()
    cursor = conn.cursor()

    table_id = order_data.get("table_id")
    if not table_id:
        raise ValueError("Brak numeru stolika")

    total = order_data.get("total")
    prep_time = order_data.get("prep_time")

    cursor.execute("""
        INSERT INTO zamowienia (
            ZAM_DataZamowienia, ZAM_LacznaKwota, ZAM_Oplacone,
            ZAM_Status, STO_IdStolika
        )
        OUTPUT INSERTED.ZAM_IdZamowienia
        VALUES (GETDATE(), ?, 0, 'Złożone', ?)
    """, (total, table_id))

    order_id = cursor.fetchone()[0]

    for item in order_data["items"]:
        cursor.execute("""
            INSERT INTO szczegolyzamowienia (
                ZAM_IdZamowienia, MEN_IdPozycji, SZAM_Ilosc, SZAM_CenaWZamowieniu
            )
            VALUES (?, ?, ?, ?)
        """, (order_id, item["id"], item["qty"], item["total_price"]))

    cursor.execute("""
        INSERT INTO kuchnia (
            ZAM_IdZamowienia, KCH_Status, KCH_CzasPrzygotowania
        )
        VALUES (?, 'Oczekujące', ?)
    """, (order_id, prep_time))

    cursor.execute("""
        UPDATE stoliki
        SET STO_Status = 'OJ'
        WHERE STO_IdStolika = ?
    """, (table_id,))

    cursor.execute("""
        UPDATE rezerwacjestolika
        SET REZ_Status = 'Zrealizowana'
        WHERE STO_IdStolika = ? AND REZ_Status = 'Potwierdzona'
    """, (table_id,))

    conn.commit()
    cursor.close()
    conn.close()

    return order_id

def get_last_order_by_table(table_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT TOP 1 ZAM_IdZamowienia, ZAM_LacznaKwota
        FROM zamowienia
        WHERE STO_IdStolika = ?
        ORDER BY ZAM_IdZamowienia DESC
    """, (table_id,))
    row = cursor.fetchone()

    if not row:
        cursor.close()
        conn.close()
        return {}

    order_id, total = row

    cursor.execute("""
        SELECT m.MEN_Nazwa, s.SZAM_Ilosc, s.SZAM_CenaWZamowieniu, m.MEN_CzasPrzygotowania
        FROM szczegolyzamowienia s
        JOIN menu m ON s.MEN_IdPozycji = m.MEN_IdPozycji
        WHERE s.ZAM_IdZamowienia = ?
    """, (order_id,))
    items = cursor.fetchall()
    cursor.close()
    conn.close()

    return {
        'id': order_id,
        'total': float(total),
        'items': [
            {
                'name': item[0],
                'qty': item[1],
                'total': float(item[2]),
                'prep_time': int(item[3])
            } for item in items
        ]
    }


def mark_order_as_paid(order_id):
    conn = get_connection()
    cursor = conn.cursor()

    # oznaczenie zamówienia jako opłacone
    cursor.execute("""
        UPDATE zamowienia
        SET ZAM_Oplacone = 1
        WHERE ZAM_IdZamowienia = ?
    """, (order_id,))

    # pobranie powiązanego stolika
    cursor.execute("SELECT STO_IdStolika FROM zamowienia WHERE ZAM_IdZamowienia = ?", (order_id,))
    row = cursor.fetchone()
    if row:
        stolik_id = row[0]
        cursor.execute("""
            UPDATE stoliki
            SET STO_Status = 'wolny'
            WHERE STO_IdStolika = ?
        """, (stolik_id,))

    conn.commit()
    cursor.close()
    conn.close()

def update_table_status(table_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE stoliki
        SET STO_Status = ?
        WHERE STO_IdStolika = ?
    """, (status, table_id))
    conn.commit()
    cursor.close()
    conn.close()