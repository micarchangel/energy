from PyQt6.QtWidgets import QApplication, QMessageBox
import sys
from db import get_connection

def test_connection():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        cur.close()
        conn.close()
        return f"Успешное подключение к PostgreSQL: {version[0]}"
    except Exception as e:
        return f"Ошибка подключения: {e}"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    result = test_connection()
    QMessageBox.information(None, "Результат подключения", result)
    sys.exit(0)