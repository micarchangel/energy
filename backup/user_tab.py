from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit,
    QComboBox, QTableWidget, QTableWidgetItem, QMessageBox
)
from users import get_users, add_user, update_user, delete_user


class UsersTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_users()

    def init_ui(self):
        layout = QVBoxLayout()

        form_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.login_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.role_input = QComboBox()
        self.role_input.addItems(["admin", "operator", "inspector", "cashier"])

        form_layout.addWidget(QLabel("ФИО"))
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(QLabel("Логин"))
        form_layout.addWidget(self.login_input)
        form_layout.addWidget(QLabel("Пароль"))
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(QLabel("Роль"))
        form_layout.addWidget(self.role_input)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "ФИО", "Логин", "Роль"])
        self.table.cellClicked.connect(self.on_cell_clicked)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Добавить")
        self.update_btn = QPushButton("Обновить")
        self.delete_btn = QPushButton("Удалить")
        self.clear_btn = QPushButton("Очистить")

        self.add_btn.clicked.connect(self.add_user)
        self.update_btn.clicked.connect(self.update_user)
        self.delete_btn.clicked.connect(self.delete_user)
        self.clear_btn.clicked.connect(self.clear_fields)

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.clear_btn)

        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.selected_user_id = None

    def load_users(self):
        users = get_users()
        self.table.setRowCount(len(users))
        for row_idx, (user_id, full_name, login, role) in enumerate(users):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(user_id)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(full_name))
            self.table.setItem(row_idx, 2, QTableWidgetItem(login))
            self.table.setItem(row_idx, 3, QTableWidgetItem(role))

    def add_user(self):
        full_name = self.name_input.text()
        login = self.login_input.text()
        password = self.password_input.text()
        role = self.role_input.currentText()
        if not all([full_name, login, password]):
            QMessageBox.warning(self, "Ошибка", "Заполните все поля.")
            return
        try:
            add_user(full_name, login, password, role)
            self.load_users()
            self.clear_fields()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить: {e}")

    def update_user(self):
        if self.selected_user_id is None:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя.")
            return
        try:
            update_user(self.selected_user_id,
                        self.name_input.text(),
                        self.login_input.text(),
                        self.role_input.currentText())
            self.load_users()
            self.clear_fields()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка обновления: {e}")

    def delete_user(self):
        if self.selected_user_id is None:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя.")
            return
        confirm = QMessageBox.question(self, "Удаление",
                                       "Вы уверены, что хотите удалить пользователя?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                delete_user(self.selected_user_id)
                self.load_users()
                self.clear_fields()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка удаления: {e}")

    def clear_fields(self):
        self.name_input.clear()
        self.login_input.clear()
        self.password_input.clear()
        self.role_input.setCurrentIndex(0)
        self.selected_user_id = None

    def on_cell_clicked(self, row, column):
        self.selected_user_id = int(self.table.item(row, 0).text())
        self.name_input.setText(self.table.item(row, 1).text())
        self.login_input.setText(self.table.item(row, 2).text())
        self.password_input.setText("")  # пароль не отображаем
        index = self.role_input.findText(self.table.item(row, 3).text())
        self.role_input.setCurrentIndex(index if index >= 0 else 0)
