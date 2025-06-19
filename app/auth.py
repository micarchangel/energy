from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)

from app.logging import log_action
from db import get_user_by_login, check_password
from session import set_current_user, current_user_id

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход в систему")
        self.resize(300, 150)
        self.role = None
        self.user_id = None

        layout = QVBoxLayout()

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")
        layout.addWidget(QLabel("Логин:"))
        layout.addWidget(self.login_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel("Пароль:"))
        layout.addWidget(self.password_input)

        btn = QPushButton("Войти")
        btn.clicked.connect(self.try_login)
        layout.addWidget(btn)

        self.setLayout(layout)

    def try_login(self):
        login = self.login_input.text()
        password = self.password_input.text()

        user = get_user_by_login(login)
        if not user:
            QMessageBox.warning(self, "Ошибка", "Пользователь не найден")
            return

        user_id, _, hashed_pw, role = user
        if check_password(password, hashed_pw):
            self.role = role
            self.user_id = user_id
            set_current_user(user_id)
            log_action(current_user_id, f"Выполнен вход")
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный пароль")
