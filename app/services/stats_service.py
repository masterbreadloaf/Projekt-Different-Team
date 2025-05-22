# app/services/stats_service.py

from db import get_connection

def get_statistics(start_date, end_date):
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Podstawowe statystyki
    cursor.execute("""
        SELECT COUNT(*), 
               COALESCE(SUM(ZAM_LacznaKwota), 0), 
               COALESCE(AVG(ZAM_LacznaKwota), 0)
        FROM zamowienia
        WHERE CAST(ZAM_DataZamowienia AS DATE) BETWEEN ? AND ?
    """, (start_date, end_date))
    row = cursor.fetchone()
    count = row[0] or 0
    total = float(row[1]) if row[1] is not None else 0.0
    avg = float(row[2]) if row[2] is not None else 0.0

    # 2. Przychód godzinowy
    cursor.execute("""
        SELECT DATEPART(HOUR, ZAM_DataZamowienia) AS godzina,
               SUM(ZAM_LacznaKwota)
        FROM zamowienia
        WHERE CAST(ZAM_DataZamowienia AS DATE) BETWEEN ? AND ?
        GROUP BY DATEPART(HOUR, ZAM_DataZamowienia)
        ORDER BY godzina
    """, (start_date, end_date))
    revenue = [{'hour': r[0], 'total': float(r[1])} for r in cursor.fetchall()]

    # 3. Zajętość stolików godzinowo
    cursor.execute("""
        SELECT DATEPART(HOUR, ZAM_DataZamowienia) AS godzina,
               COUNT(DISTINCT STO_IdStolika)
        FROM zamowienia
        WHERE CAST(ZAM_DataZamowienia AS DATE) BETWEEN ? AND ?
        GROUP BY DATEPART(HOUR, ZAM_DataZamowienia)
        ORDER BY godzina
    """, (start_date, end_date))
    occupancy = [{'hour': r[0], 'count': r[1]} for r in cursor.fetchall()]

    # 4. Popularność kategorii (tekstowo z kolumny menu.MEN_Kategoria)
    cursor.execute("""
        SELECT m.MEN_Kategoria, COUNT(*)
        FROM szczegolyzamowienia sz
        JOIN menu m ON m.MEN_IdPozycji = sz.MEN_IdPozycji
        JOIN zamowienia z ON z.ZAM_IdZamowienia = sz.ZAM_IdZamowienia
        WHERE CAST(z.ZAM_DataZamowienia AS DATE) BETWEEN ? AND ?
        GROUP BY m.MEN_Kategoria
        ORDER BY COUNT(*) DESC
    """, (start_date, end_date))
    categories = [{'category': r[0], 'count': r[1]} for r in cursor.fetchall()]

    # 5. Top dania
    cursor.execute("""
        SELECT m.MEN_Nazwa, COUNT(*) AS liczba
        FROM szczegolyzamowienia sz
        JOIN menu m ON m.MEN_IdPozycji = sz.MEN_IdPozycji
        JOIN zamowienia z ON z.ZAM_IdZamowienia = sz.ZAM_IdZamowienia
        WHERE CAST(z.ZAM_DataZamowienia AS DATE) BETWEEN ? AND ?
        GROUP BY m.MEN_Nazwa
        ORDER BY liczba DESC
        OFFSET 0 ROWS FETCH NEXT 5 ROWS ONLY
    """, (start_date, end_date))
    top_items = [{'name': r[0], 'count': r[1]} for r in cursor.fetchall()]

    # 6. Heatmapa: dzień tygodnia × godzina
    cursor.execute("""
        SELECT 
            DATEPART(WEEKDAY, ZAM_DataZamowienia) AS dzien,
            DATEPART(HOUR, ZAM_DataZamowienia) AS godzina,
            COUNT(*) AS liczba
        FROM zamowienia
        WHERE CAST(ZAM_DataZamowienia AS DATE) BETWEEN ? AND ?
        GROUP BY DATEPART(WEEKDAY, ZAM_DataZamowienia), DATEPART(HOUR, ZAM_DataZamowienia)
        ORDER BY dzien, godzina
    """, (start_date, end_date))
    heatmap = [{'day': r[0], 'hour': r[1], 'count': r[2]} for r in cursor.fetchall()]

    cursor.close()
    conn.close()

    return {
        'ordersCount': count,
        'totalRevenue': total,
        'avgOrderValue': avg,
        'revenueOverTime': revenue,
        'tableOccupancyOverTime': occupancy,
        'categoryPopularity': categories,
        'topItems': top_items,
        'heatmapData': heatmap

    }

    