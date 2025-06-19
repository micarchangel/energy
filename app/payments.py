"""
Модуль работы с таблицей оплат (payments) в базе данных energy.

Предоставляет функции для получения, добавления и удаления записей об оплатах абонентов.
"""

import psycopg2

def get_payments(conn):
    """
    Получает все записи об оплатах из базы данных.

    :param conn: активное соединение с базой данных
    :return: список кортежей с данными об оплатах
    """
    with conn.cursor() as cur:
        cur.execute("SELECT id, abonent_id, amount, pay_date FROM payments ORDER BY pay_date DESC")
        return cur.fetchall()

def add_payment(conn, abonent_id, amount, payment_date):
    """
    Добавляет новую оплату в базу данных.

    :param conn: активное соединение с базой данных
    :param abonent_id: ID абонента, сделавшего оплату
    :param amount: сумма оплаты
    :param payment_date: дата оплаты
    """
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO payments (abonent_id, amount, pay_date) VALUES (%s, %s, %s)",
            (abonent_id, amount, payment_date)
        )
    conn.commit()

def delete_payment(conn, payment_id):
    """
    Удаляет оплату по её ID.

    :param conn: активное соединение с базой данных
    :param payment_id: ID записи об оплате
    """
    with conn.cursor() as cur:
        cur.execute("DELETE FROM payments WHERE id = %s", (payment_id,))
    conn.commit()
