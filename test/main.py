import sys
from PyQt6.QtWidgets import QApplication, QTabWidget
from gui import MainApp
from auth import LoginDialog
from PyQt6.QtWidgets import QDialog

def main():
    app = QApplication(sys.argv)

    login_dialog = LoginDialog()
    if login_dialog.exec() != QDialog.DialogCode.Accepted:
        sys.exit(0)

    user_login = login_dialog.login_input.text()
    user_role = login_dialog.role

    main_window = MainApp(current_user=user_login, role=user_role)
    main_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
