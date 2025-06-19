import psycopg2

def get_payments(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT id, abonent_id, amount, pay_date FROM payments ORDER BY pay_date DESC")
        return cur.fetchall()

def add_payment(conn, abonent_id, amount, payment_date):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO payments (abonent_id, amount, pay_date) VALUES (%s, %s, %s)",
            (abonent_id, amount, payment_date)
        )
    conn.commit()

def delete_payment(conn, payment_id):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM payments WHERE id = %s", (payment_id,))
    conn.commit()
