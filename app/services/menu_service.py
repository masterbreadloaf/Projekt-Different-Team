# services/menu_service.py
from db import get_connection

def get_menu_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            m.MEN_Nazwa,
            m.MEN_Opis,
            m.MEN_Cena,
            m.MEN_CzasPrzygotowania,
            m.MEN_Kategoria,
            z.ZDJ_Sciezka
        FROM menu m
        LEFT JOIN zdjeciamenu z 
            ON m.MEN_IdPozycji = z.MEN_IdPozycji AND z.ZDJ_Glowne = 1
        WHERE m.MEN_Dostepnosc = 1
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    categories = {}
    for row in rows:
        category = row[4].strip().lower()
        item = {
            'name': row[0],
            'description': row[1],
            'price': row[2],
            'prep_time': row[3],
            'image': row[5] or '/static/images/default.jpg'
        }
        if category not in categories:
            categories[category] = []
        categories[category].append(item)

    return categories