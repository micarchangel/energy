from db import get_connection
import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(login, password, role):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (login, password_hash, role)
                VALUES ( %s, %s, %s)
            """, (login, hash_password(password), role))

def update_user(user_id, login, role):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE users SET login=%s, role=%s WHERE id=%s
            """, (login, role, user_id))

def delete_user(user_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id=%s", (user_id,))

def get_users():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, login, role FROM users ORDER BY id")
            return cur.fetchall()

def get_user_by_login(login):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE login=%s", (login,))
            return cur.fetchone()
