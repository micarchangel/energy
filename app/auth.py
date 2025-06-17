# app/auth.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from db import get_user_by_login, check_password

class LoginWindow(QWidget):
    def __init__(self, on_success):
        super().__init__()
        self.setWindowTitle("Вход в систему")
        self.resize(300, 150)
        self.on_success = on_success

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
            self.on_success(user_id, role)
            self.hide()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный пароль")