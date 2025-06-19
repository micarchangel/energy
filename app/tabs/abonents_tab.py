from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox,
    QDialog, QFormLayout, QLineEdit
)
from app.abonents import get_all_abonents, add_abonent, update_abonent, delete_abonent
from app.session import current_user_id
from logging import log_action


class AbonentsTab(QWidget):
    """
    Класс представляет вкладку 'Абоненты' с возможностью
    добавления, редактирования и удаления абонентов.
    """

    def __init__(self):
        """
        Инициализирует интерфейс вкладки и кнопки управления.
        """
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Добавить")
        self.edit_button = QPushButton("Редактировать")
        self.delete_button = QPushButton("Удалить")

        self.add_button.clicked.connect(self.add_abonent)
        self.edit_button.clicked.connect(self.edit_abonent)
        self.delete_button.clicked.connect(self.delete_abonent)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        self.layout.addLayout(button_layout)

        self.load_abonents()

    def load_abonents(self):
        """
        Загружает список абонентов из базы данных и отображает в таблице.
        """
        self.table.clear()
        abonents = get_all_abonents()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "ФИО", "Адрес", "Лицевой счет"])
        self.table.setRowCount(len(abonents))
        for row, abonent in enumerate(abonents):
            for col, item in enumerate(abonent):
                self.table.setItem(row, col, QTableWidgetItem(str(item)))

    def add_abonent(self):
        """
        Открывает диалог добавления нового абонента и сохраняет его в БД.
        """
        dialog = AddAbonentDialog()
        if dialog.exec():
            full_name, address, account_number = dialog.get_data()
            if full_name and address and account_number:
                try:
                    add_abonent(full_name, address, account_number)
                    self.load_abonents()
                    log_action(current_user_id, f"Добавлен абонент: {account_number}")
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось добавить абонента:\n{e}")
            else:
                QMessageBox.warning(self, "Внимание", "Все поля должны быть заполнены.")

    def edit_abonent(self):
        """
        Открывает диалог редактирования выбранного абонента.
        """
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Выбор", "Выберите абонента для редактирования.")
            return

        abonent_id = int(self.table.item(row, 0).text())
        current_name = self.table.item(row, 1).text()
        current_address = self.table.item(row, 2).text()
        current_account = self.table.item(row, 3).text()

        dialog = AddAbonentDialog(full_name=current_name, address=current_address, account_number=current_account)
        if dialog.exec():
            full_name, address, account_number = dialog.get_data()
            if full_name and address and account_number:
                try:
                    update_abonent(abonent_id, full_name, address, account_number)
                    self.load_abonents()
                    log_action(current_user_id, f"Изменён абонент: ID={abonent_id}")
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось обновить абонента:\n{e}")
            else:
                QMessageBox.warning(self, "Внимание", "Все поля должны быть заполнены.")

    def delete_abonent(self):
        """
        Удаляет выбранного абонента после подтверждения.
        """
        row = self.table.currentRow()
        if row < 0:
            return
        abonent_id = int(self.table.item(row, 0).text())
        confirm = QMessageBox.question(self, "Удаление", "Удалить абонента?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            delete_abonent(abonent_id)
            self.load_abonents()
            log_action(current_user_id, f"Удалён абонент ID={abonent_id}")


class AddAbonentDialog(QDialog):
    """
    Диалоговое окно добавления/редактирования абонента.
    """

    def __init__(self, full_name="", address="", account_number=""):
        """
        Инициализация полей формы с передачей значений по умолчанию.
        """
        super().__init__()
        self.setWindowTitle("Добавить / редактировать абонента")

        self.layout = QFormLayout(self)

        self.name_input = QLineEdit(full_name)
        self.address_input = QLineEdit(address)
        self.account_input = QLineEdit(account_number)

        self.layout.addRow("ФИО:", self.name_input)
        self.layout.addRow("Адрес:", self.address_input)
        self.layout.addRow("Лицевой счёт:", self.account_input)

        buttons_layout = QHBoxLayout()
        self.ok_button = QPushButton("Сохранить")
        self.cancel_button = QPushButton("Отмена")
        buttons_layout.addWidget(self.ok_button)
        buttons_layout.addWidget(self.cancel_button)

        self.layout.addRow(buttons_layout)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_data(self):
        """
        Возвращает введённые пользователем данные.

        :return: Кортеж (ФИО, адрес, лицевой счёт)
        """
        return (
            self.name_input.text().strip(),
            self.address_input.text().strip(),
            self.account_input.text().strip()
        )
