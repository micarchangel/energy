from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout
from app.users import add_user, delete_user, get_users

class UserTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.role_input = QComboBox()
        self.role_input.addItems(["admin", "operator", "inspector", "cashier"])

        self.add_button = QPushButton("Добавить пользователя")
        self.add_button.clicked.connect(self.handle_add_user)

        self.delete_button = QPushButton("Удалить выбранного пользователя")
        self.delete_button.clicked.connect(self.handle_delete_user)

        form_layout = QHBoxLayout()
        form_layout.addWidget(self.login_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.role_input)
        form_layout.addWidget(self.add_button)
        form_layout.addWidget(self.delete_button)

        self.layout.addLayout(form_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Логин", "Роль"])
        self.layout.addWidget(self.table)

        self.load_users()

    def handle_add_user(self):
        login = self.login_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_input.currentText()

        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль.")
            return

        try:
            add_user(login, password, role)
            QMessageBox.information(self, "Успех", "Пользователь добавлен.")
            self.load_users()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить пользователя: {e}")

    def handle_delete_user(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя для удаления.")
            return

        row = selected_items[0].row()
        user_id = int(self.table.item(row, 0).text())

        confirm = QMessageBox.question(
            self,
            "Подтвердите удаление",
            f"Удалить пользователя с ID {user_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            try:
                delete_user(user_id)
                QMessageBox.information(self, "Успех", "Пользователь удалён.")
                self.load_users()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить пользователя: {e}")

    def load_users(self):
        self.table.setRowCount(0)
        for user in get_users():
            row_pos = self.table.rowCount()
            self.table.insertRow(row_pos)
            self.table.setItem(row_pos, 0, QTableWidgetItem(str(user[0])))
            self.table.setItem(row_pos, 1, QTableWidgetItem(user[1]))
            self.table.setItem(row_pos, 2, QTableWidgetItem(user[2]))
