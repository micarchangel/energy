import psycopg2
from datetime import datetime

def log_action(user_id: int, action: str):
    """
    Записывает действие пользователя в таблицу logs.

    :param user_id: ID пользователя (из таблицы users)
    :param action: Описание действия
    """
    try:
        conn = psycopg2.connect(
            dbname="energy",
            user="postgres",
            password="1Wizard1",
            host="localhost",
            port="5432"
        )
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO logs (user_id, action, timestamp)
                    VALUES (%s, %s, %s)
                """, (user_id, action, datetime.now()))
    except Exception as e:
        print(f"[Ошибка логирования] {e}")
    finally:
        if conn:
            conn.close()