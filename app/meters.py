import psycopg2
from psycopg2.extras import RealDictCursor

DB_PARAMS = {
    'dbname': 'energy',
    'user': 'postgres',
    'password': '1Wizard1',
    'host': 'localhost',
    'port': 5432
}

def get_connection():
    return psycopg2.connect(**DB_PARAMS)

def get_all_meters():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT meters.*, abonents.full_name 
                FROM meters 
                LEFT JOIN abonents ON meters.abonent_id = abonents.id
                ORDER BY meters.id;
            """)
            return cur.fetchall()

def add_meter(serial_number, type, install_date, abonent_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO meters (serial_number, type, install_date, abonent_id) VALUES (%s, %s, %s, %s);",
                (serial_number, type, install_date, abonent_id)
            )
            conn.commit()

def update_meter(meter_id, serial_number, type, install_date, abonent_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE meters SET serial_number = %s, type = %s, install_date = %s, abonent_id = %s WHERE id = %s;",
                (serial_number, type, install_date, abonent_id, meter_id)
            )
            conn.commit()

def delete_meter(meter_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM meters WHERE id = %s;", (meter_id,))
            conn.commit()