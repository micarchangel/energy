"""
Модуль работы с таблицей счётчиков (meters) в базе данных energy.

Предоставляет функции для получения, добавления, обновления и удаления данных о счётчиках.
"""

import psycopg2
from psycopg2.extras import RealDictCursor

DB_PARAMS = {
    'dbname': 'energy',
    'user': 'postgres',
    'password': '1Wizard1',
    'host': 'localhost',
    'port': 5432
}

def get_connection():
    """
    Устанавливает соединение с базой данных PostgreSQL.

    :return: объект соединения psycopg2
    """
    return psycopg2.connect(**DB_PARAMS)

def get_all_meters():
    """
    Возвращает список всех счётчиков с данными о связанных абонентах.

    :return: список словарей с данными о счётчиках
    """
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT meters.*, abonents.full_name 
                FROM meters 
                LEFT JOIN abonents ON meters.abonent_id = abonents.id
                ORDER BY meters.id;
            """)
            return cur.fetchall()

def add_meter(serial_number, type, install_date, abonent_id):
    """
    Добавляет новый счётчик в базу данных.

    :param serial_number: серийный номер счётчика
    :param type: тип счётчика
    :param install_date: дата установки
    :param abonent_id: ID абонента
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO meters (serial_number, type, install_date, abonent_id) VALUES (%s, %s, %s, %s);",
                (serial_number, type, install_date, abonent_id)
            )
            conn.commit()

def update_meter(meter_id, serial_number, type, install_date, abonent_id):
    """
    Обновляет данные о счётчике по его ID.

    :param meter_id: ID счётчика
    :param serial_number: новый серийный номер
    :param type: новый тип
    :param install_date: новая дата установки
    :param abonent_id: новый ID абонента
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE meters SET serial_number = %s, type = %s, install_date = %s, abonent_id = %s WHERE id = %s;",
                (serial_number, type, install_date, abonent_id, meter_id)
            )
            conn.commit()

def delete_meter(meter_id):
    """
    Удаляет счётчик по его ID.

    :param meter_id: ID счётчика
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM meters WHERE id = %s;", (meter_id,))
            conn.commit()
