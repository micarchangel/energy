# main.py
import sys
from PyQt6.QtWidgets import QApplication
from db import initialize_db, write_log
from gui import MainApp
from auth import LoginWindow

def main():
    initialize_db()

    app = QApplication(sys.argv)
    main_window = {}

    def launch_main(user_id, role):
        write_log("Вход в систему", user_id)
        main_window['window'] = MainApp(user_id=user_id, role=role)
        main_window['window'].show()

    login = LoginWindow(on_success=launch_main)
    login.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
