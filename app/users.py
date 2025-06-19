"""
Модуль users.py предназначен для управления пользователями системы.

Содержит функции для добавления, редактирования, удаления и получения информации о пользователях.
"""

from db import get_connection, hash_password


def add_user(login, password, role):
    """
    Добавляет нового пользователя в базу данных.

    :param login: Логин пользователя
    :param password: Пароль (в чистом виде)
    :param role: Роль пользователя (admin, operator, inspector, cashier)
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (login, password_hash, role)
                VALUES ( %s, %s, %s)
            """, (login, hash_password(password), role))

def update_user(user_id, login, role):
    """
    Обновляет логин и роль существующего пользователя.

    :param user_id: ID пользователя
    :param login: Новый логин
    :param role: Новая роль
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE users SET login=%s, role=%s WHERE id=%s
            """, (login, role, user_id))

def delete_user(user_id):
    """
    Удаляет пользователя по ID.

    :param user_id: ID пользователя
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id=%s", (user_id,))

def get_users():
    """
    Возвращает список всех пользователей (id, login, role).

    :return: Список кортежей
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, login, role FROM users ORDER BY id")
            return cur.fetchall()

def get_user_by_login(login):
    """
    Возвращает пользователя по логину: (id, login, hashed_password, role)
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, login, password_hash, role FROM users WHERE login=%s", (login,))
            return cur.fetchone()
