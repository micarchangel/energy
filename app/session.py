"""
Модуль session.py

Хранит идентификатор текущего авторизованного пользователя
для использования в логировании и других модулях системы.
"""

current_user_id: int = None

def set_current_user(user_id: int):
    """
    Устанавливает ID текущего пользователя.

    :param user_id: Идентификатор пользователя (из таблицы users)
    """
    global current_user_id
    current_user_id = user_id
