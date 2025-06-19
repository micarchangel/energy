"""
Модуль работы с таблицей показаний (readings) в базе данных energy.

Предоставляет функции для получения, добавления и удаления записей о показаниях счётчиков.
"""

import psycopg2
from psycopg2 import sql
from db import get_connection

def get_all_readings():
    """
    Получает все записи о показаниях с данными счётчиков и абонентов.

    :return: список кортежей с показаниями и сопутствующей информацией
    """
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
    """
    Добавляет новое показание в базу данных.

    :param reading_date: дата показания
    :param value: значение показания
    :param meter_id: ID счётчика
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO readings (reading_date, value, meter_id) VALUES (%s, %s, %s)",
                (reading_date, value, meter_id),
            )
        conn.commit()

def delete_reading(reading_id):
    """
    Удаляет запись о показании по её ID.

    :param reading_id: ID записи о показании
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM readings WHERE id = %s", (reading_id,))
        conn.commit()
