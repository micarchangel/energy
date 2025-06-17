from db import get_connection, hash_password

def create_user(login: str, password: str, role: str = "operator"):
    """Создание нового пользователя"""
    hashed = hash_password(password)
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (login, password_hash, role) VALUES (%s, %s, %s)",
            (login, hashed, role)
        )
        conn.commit()
        print(f"Пользователь '{login}' успешно добавлен.")
    except Exception as e:
        print(f"Ошибка при добавлении пользователя: {e}")
    finally:
        cur.close()
        conn.close()

def delete_user(login: str):
    """Удаление пользователя по логину"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM users WHERE login = %s", (login,))
        if cur.rowcount > 0:
            print(f"Пользователь '{login}' удалён.")
        else:
            print(f"Пользователь '{login}' не найден.")
        conn.commit()
    except Exception as e:
        print(f"Ошибка при удалении пользователя: {e}")
    finally:
        cur.close()
        conn.close()
