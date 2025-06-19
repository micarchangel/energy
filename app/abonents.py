import psycopg2

DB_PARAMS = {
    'dbname': 'energy',
    'user': 'postgres',
    'password': '1Wizard1',
    'host': 'localhost',
    'port': '5432',
}

def get_all_abonents():
    """
    Получает список всех абонентов из базы данных.

    :return: Список кортежей с данными абонентов (id, full_name, address, account_number)
    """
    with psycopg2.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, full_name, address, account_number FROM abonents ORDER BY id;")
            return cur.fetchall()

def add_abonent(full_name, address, account_number):
    """
    Добавляет нового абонента в таблицу abonents.

    :param full_name: Полное имя абонента
    :param address: Адрес абонента
    :param account_number: Лицевой счёт (уникальный идентификатор)
    """
    with psycopg2.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO abonents (full_name, address, account_number) VALUES (%s, %s, %s);",
                (full_name, address, account_number)
            )

def update_abonent(abonent_id, full_name, address, account_number):
    """
    Обновляет информацию об абоненте по заданному ID.

    :param abonent_id: ID абонента
    :param full_name: Новое имя
    :param address: Новый адрес
    :param account_number: Новый лицевой счёт
    """
    with psycopg2.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE abonents SET full_name=%s, address=%s, account_number=%s WHERE id=%s;",
                (full_name, address, account_number, abonent_id)
            )

def delete_abonent(abonent_id):
    """
    Удаляет абонента из базы данных по ID.

    :param abonent_id: Идентификатор абонента
    """
    with psycopg2.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM abonents WHERE id=%s;", (abonent_id,))
