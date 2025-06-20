"""
Модуль работы с тарифами (tariffs) в базе данных energy.

Содержит функции для получения, добавления и удаления тарифов.
"""

from db import get_connection

def get_tariffs():
    """
    Получает список всех тарифов, отсортированных по дате начала действия (в порядке убывания).

    :return: список кортежей с данными тарифов
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tariffs ORDER BY start_date DESC;")
            return cur.fetchall()

def add_tariff(zone, value, start_date):
    """
    Добавляет новый тариф в базу данных.

    :param zone: зона действия тарифа (например, дневной, ночной)
    :param value: стоимость тарифа (в рублях)
    :param start_date: дата начала действия тарифа
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO tariffs (zone, value, start_date) VALUES (%s, %s, %s);",
                (zone, value, start_date)
            )
            conn.commit()

def delete_tariff(tariff_id):
    """
    Удаляет тариф по его ID.

    :param tariff_id: ID тарифа для удаления
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM tariffs WHERE id = %s;", (tariff_id,))
            conn.commit()
