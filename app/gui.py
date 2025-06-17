from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QDialog, QLabel, QLineEdit, QComboBox, QDialogButtonBox, QMainWindow
)
from user_service import get_all_users, create_user, update_user, delete_user, VALID_ROLES

class UserDialog(QDialog):
    def __init__(self, parent=None, mode="add", login="", role="", editable=True):
        super().__init__(parent)
        self.setWindowTitle("Добавить пользователя" if mode == "add" else "Редактировать пользователя")
        self.login_editable = editable
        self.mode = mode

        layout = QVBoxLayout()

        self.login_input = QLineEdit(login)
        self.login_input.setPlaceholderText("Логин")
        self.login_input.setReadOnly(not editable)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.role_combo = QComboBox()
        self.role_combo.addItems(VALID_ROLES)
        if role:
            index = self.role_combo.findText(role)
            if index >= 0:
                self.role_combo.setCurrentIndex(index)

        layout.addWidget(QLabel("Логин:"))
        layout.addWidget(self.login_input)
        layout.addWidget(QLabel("Пароль:"))
        layout.addWidget(self.password_input)
        layout.addWidget(QLabel("Роль:"))
        layout.addWidget(self.role_combo)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_data(self):
        return self.login_input.text(), self.password_input.text(), self.role_combo.currentText()

class MainApp(QMainWindow):  # Пример, если используется QMainWindow
    def create_user_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.user_table = QTableWidget()
        self.user_table.setColumnCount(2)
        self.user_table.setHorizontalHeaderLabels(["Логин", "Роль"])
        layout.addWidget(self.user_table)

        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Добавить")
        edit_btn = QPushButton("Редактировать")
        del_btn = QPushButton("Удалить")

        add_btn.clicked.connect(self.add_user)
        edit_btn.clicked.connect(self.edit_user)
        del_btn.clicked.connect(self.remove_user)

        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(del_btn)

        layout.addLayout(btn_layout)
        tab.setLayout(layout)

        self.load_user_table()
        return tab

    def load_user_table(self):
        users = get_all_users()
        self.user_table.setRowCount(len(users))
        for i, (login, role) in enumerate(users):
            self.user_table.setItem(i, 0, QTableWidgetItem(login))
            self.user_table.setItem(i, 1, QTableWidgetItem(role))

    def add_user(self):
        dialog = UserDialog(self)
        try:
            if dialog.exec():
                login, password, role = dialog.get_data()

                if not login.strip() or not password.strip():
                    QMessageBox.warning(self, "Ошибка", "Логин и пароль не могут быть пустыми.")
                    return

                result = create_user(login.strip(), password, role)
                if result == "ok":
                    self.load_user_table()
                else:
                    QMessageBox.critical(self, "Ошибка создания", result)
        except Exception as e:
            QMessageBox.critical(self, "Сбой", f"Произошла ошибка: {e}")
            print("Ошибка при добавлении пользователя:", e)

    def edit_user(self):
        row = self.user_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Выберите пользователя", "Не выбран пользователь.")
            return

        login = self.user_table.item(row, 0).text()
        role = self.user_table.item(row, 1).text()

        dialog = UserDialog(self, mode="edit", login=login, role=role, editable=False)
        try:
            if dialog.exec():
                _, password, new_role = dialog.get_data()
                result = update_user(login, password, new_role)
                if result == "ok":
                    self.load_user_table()
                else:
                    QMessageBox.critical(self, "Ошибка", result)
        except Exception as e:
            QMessageBox.critical(self, "Сбой", str(e))
            print("Ошибка при редактировании:", e)

    def remove_user(self):
        row = self.user_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Удаление", "Выберите пользователя для удаления.")
            return

        login = self.user_table.item(row, 0).text()
        reply = QMessageBox.question(self, "Удаление", f"Удалить пользователя '{login}'?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            result = delete_user(login)
            if result == "ok":
                self.load_user_table()
            else:
                QMessageBox.critical(self, "Ошибка", result)
