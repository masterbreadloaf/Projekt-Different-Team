from db import get_connection

def get_orders_by_filters(filters):
    conn = get_connection()
    cursor = conn.cursor()

    conditions = []
    params = []

    if filters['start'] and filters['end']:
        conditions.append("CAST(z.ZAM_DataZamowienia AS DATE) BETWEEN ? AND ?")
        params += [filters['start'], filters['end']]

    if filters['table']:
        conditions.append("s.STO_Numer = ?")
        params.append(filters['table'])

    if filters['paid'] == '1':
        conditions.append("z.ZAM_Oplacone = 1")
    elif filters['paid'] == '0':
        conditions.append("z.ZAM_Oplacone = 0")

    if filters['min']:
        conditions.append("z.ZAM_LacznaKwota >= ?")
        params.append(filters['min'])

    if filters['max']:
        conditions.append("z.ZAM_LacznaKwota <= ?")
        params.append(filters['max'])

    where_clause = " AND ".join(conditions) if conditions else "1=1"

    cursor.execute(f"""
        SELECT z.ZAM_IdZamowienia, z.ZAM_DataZamowienia, z.ZAM_LacznaKwota,
               z.ZAM_Status, z.ZAM_Oplacone, s.STO_Numer, ZAM_Komentarz
        FROM zamowienia z
        JOIN stoliki s ON z.STO_IdStolika = s.STO_IdStolika
        WHERE {where_clause}
        ORDER BY z.ZAM_IdZamowienia DESC
    """, params)

    orders = cursor.fetchall()

    result = []
    for order in orders:
        order_id = order[0]
        cursor.execute("""
            SELECT m.MEN_Nazwa, sz.SZAM_Ilosc, sz.SZAM_CenaWZamowieniu
            FROM szczegolyzamowienia sz
            JOIN menu m ON sz.MEN_IdPozycji = m.MEN_IdPozycji
            WHERE sz.ZAM_IdZamowienia = ?
        """, (order_id,))
        items = cursor.fetchall()

        result.append({
            'id': order[0],
            'date': order[1],
            'total': float(order[2]),
            'status': order[3],
            'paid': bool(order[4]),
            'table': order[5],
            'comment': order[6] or "",
            'items': [
                {
                    'name': item[0],
                    'qty': item[1],
                    'total': float(item[2])
                } for item in items
            ]
        })

    cursor.close()
    conn.close()
    return result