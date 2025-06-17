# app/db.py
import os
import psycopg2
import bcrypt
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime

DB_NAME = "energy"
DB_USER = "postgres"
DB_PASSWORD = "1Wizard1"
DB_HOST = "localhost"
DB_PORT = 5432

def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def create_database_if_not_exists():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}';")
        exists = cur.fetchone()

        if not exists:
            print(f"Создаётся база данных '{DB_NAME}'...")
            cur.execute(f"CREATE DATABASE {DB_NAME};")
        else:
            print(f"База данных '{DB_NAME}' уже существует.")

        cur.close()
        conn.close()
    except Exception as e:
        print("Ошибка при создании базы данных:", e)

def write_log(action, user_id=None):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO logs (user_id, action, timestamp) VALUES (%s, %s, %s);",
            (user_id, action, datetime.now())
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("Ошибка при записи в лог:", e)

def initialize_db():
    create_database_if_not_exists()

    try:
        conn = get_connection()
        cur = conn.cursor()

        # Проверка, инициализирована ли БД
        cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'abonents');")
        exists = cur.fetchone()[0]

        if exists:
            print("Таблицы уже существуют. Инициализация не требуется.")
        else:
            print("Создаются таблицы и начальные данные...")

            schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
            with open(schema_path, "r", encoding="utf-8") as f:
                cur.execute(f.read())
            conn.commit()
            print("База данных успешно инициализирована.")

            write_log("Инициализация базы данных и создание таблиц", user_id=None)

        cur.close()
        conn.close()

    except Exception as e:
        print("Ошибка при инициализации базы данных:", e)


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def get_user_by_login(login: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, login, password_hash, role FROM users WHERE login = %s", (login,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user  # tuple (id, login, password_hash, role)