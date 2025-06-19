# app/main.py
import sys
from PyQt6.QtWidgets import QApplication
from db import initialize_db
from gui import MainApp  # предположим, позже GUI вынесем в отдельный модуль

if __name__ == "__main__":
    initialize_db()  # автоматическая инициализация базы

    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
