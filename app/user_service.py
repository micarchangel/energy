from db import get_connection, hash_password

VALID_ROLES = ('admin', 'operator', 'inspector', 'cashier')

def get_all_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT login, role FROM users ORDER BY login")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users

def create_user(login: str, password: str, role: str) -> str:
    if role not in VALID_ROLES:
        return "Недопустимая роль"
    if not login or not password:
        return "Логин и пароль не могут быть пустыми"

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (login, password_hash, role) VALUES (%s, %s, %s)",
            (login, hash_password(password), role)
        )
        conn.commit()
        return "ok"
    except Exception as e:
        return f"Ошибка: {e}"
    finally:
        cur.close()
        conn.close()

def update_user(login: str, new_password: str, new_role: str) -> str:
    if new_role not in VALID_ROLES:
        return "Недопустимая роль"

    conn = get_connection()
    cur = conn.cursor()
    try:
        if new_password:
            cur.execute(
                "UPDATE users SET password_hash = %s, role = %s WHERE login = %s",
                (hash_password(new_password), new_role, login)
            )
        else:
            cur.execute(
                "UPDATE users SET role = %s WHERE login = %s",
                (new_role, login)
            )
        conn.commit()
        return "ok"
    except Exception as e:
        return f"Ошибка: {e}"
    finally:
        cur.close()
        conn.close()

def delete_user(login: str) -> str:
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM users WHERE login = %s", (login,))
        conn.commit()
        return "ok"
    except Exception as e:
        return f"Ошибка: {e}"
    finally:
        cur.close()
        conn.close()
