
import psycopg2
from psycopg2 import sql
from db import get_connection

def get_tariffs():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tariffs ORDER BY start_date DESC;")
            return cur.fetchall()

def add_tariff(zone, value, start_date):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO tariffs (zone, value, start_date) VALUES (%s, %s, %s);",
                (zone, value, start_date)
            )
            conn.commit()

def delete_tariff(tariff_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM tariffs WHERE id = %s;", (tariff_id,))
            conn.commit()
