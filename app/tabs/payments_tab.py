from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QFormLayout, QLineEdit, QDateEdit
from PyQt6.QtCore import QDate
import psycopg2

from app.payments import get_payments, add_payment, delete_payment
from app.logging import log_action
from app.session import current_user_id


class PaymentsTab(QWidget):
    """
    Вкладка управления оплатами.
    Позволяет добавлять и удалять записи об оплате, а также просматривать список всех оплат.
    """

    def __init__(self):
        """Инициализация вкладки"""
        super().__init__()
        self.conn = psycopg2.connect(
            dbname="energy", user="postgres", password="1Wizard1", host="localhost", port="5432"
        )
        self.init_ui()

    def init_ui(self):
        """Создание пользовательского интерфейса"""
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "ID абонента", "Сумма", "Дата оплаты"])
        layout.addWidget(self.table)

        self.abonent_input = QLineEdit()
        self.amount_input = QLineEdit()
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)

        form_layout = QFormLayout()
        form_layout.addRow("ID абонента:", self.abonent_input)
        form_layout.addRow("Сумма:", self.amount_input)
        form_layout.addRow("Дата оплаты:", self.date_input)
        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        add_button = QPushButton("Добавить")
        add_button.clicked.connect(self.add_payment)
        delete_button = QPushButton("Удалить")
        delete_button.clicked.connect(self.delete_payment)
        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        """Загружает все оплаты в таблицу"""
        self.table.setRowCount(0)
        for row_data in get_payments(self.conn):
            row_pos = self.table.rowCount()
            self.table.insertRow(row_pos)
            for col, value in enumerate(row_data):
                self.table.setItem(row_pos, col, QTableWidgetItem(str(value)))

    def add_payment(self):
        """Добавляет новую запись об оплате"""
        try:
            abonent_id = int(self.abonent_input.text())
            amount = float(self.amount_input.text())
            payment_date = self.date_input.date().toPyDate()
            add_payment(self.conn, abonent_id, amount, payment_date)
            log_action(current_user_id, f"Добавлена оплата: Абонент {abonent_id}, {amount} руб.")
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить оплату: {e}")

    def delete_payment(self):
        """Удаляет выбранную запись об оплате"""
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            try:
                payment_id = int(self.table.item(selected_row, 0).text())
                delete_payment(self.conn, payment_id)
                log_action(current_user_id, f"Удалена оплата ID {payment_id}")
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить оплату: {e}")
