import os
import psycopg2
import bcrypt
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app.logging import log_action

DB_NAME = "energy"
DB_USER = "postgres"
DB_PASSWORD = "1Wizard1"
DB_HOST = "localhost"
DB_PORT = 5432

def get_connection():
    """
    Создаёт и возвращает подключение к базе данных energy.
    """
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def create_database_if_not_exists():
    """
    Проверяет наличие базы данных energy и создаёт её, если не существует.
    """
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

def initialize_db():
    """
    Проверяет инициализирована ли база данных, создаёт таблицы из schema.sql при необходимости.
    """
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

            log_action(None, "Инициализация базы данных и создание таблиц")

        cur.close()
        conn.close()

    except Exception as e:
        print("Ошибка при инициализации базы данных:", e)

def hash_password(password: str) -> str:
    """
    Хеширует пароль с помощью bcrypt.

    :param password: Пароль в открытом виде
    :return: Хешированный пароль
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def check_password(password: str, hashed: str) -> bool:
    """
    Проверяет соответствие пароля его хешу.

    :param password: Пароль в открытом виде
    :param hashed: Хеш пароля
    :return: True, если пароли совпадают
    """
    return bcrypt.checkpw(password.encode(), hashed.encode())

def get_user_by_login(login: str):
    """
    Получает пользователя по логину.

    :param login: Логин пользователя
    :return: Кортеж (id, login, password_hash, role) или None
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, login, password_hash, role FROM users WHERE login = %s", (login,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user
