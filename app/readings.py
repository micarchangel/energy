import psycopg2
from psycopg2 import sql
from .db import get_connection


def get_all_readings():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT readings.id, readings.reading_date, readings.value,
                       meters.serial_number, abonents.full_name
                FROM readings
                JOIN meters ON readings.meter_id = meters.id
                JOIN abonents ON meters.abonent_id = abonents.id
                ORDER BY readings.reading_date DESC
            """)
            return cur.fetchall()


def add_reading(reading_date, value, meter_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO readings (reading_date, value, meter_id) VALUES (%s, %s, %s)",
                (reading_date, value, meter_id),
            )
        conn.commit()


def delete_reading(reading_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM readings WHERE id = %s", (reading_id,))
        conn.commit()
