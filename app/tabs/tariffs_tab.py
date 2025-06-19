
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QDateEdit, QMessageBox
from PyQt6.QtCore import QDate
from app.tariffs import get_tariffs, add_tariff, delete_tariff

class TariffsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Зона", "Тариф", "Дата начала"])
        self.layout().addWidget(QLabel("Тарифы"))
        self.layout().addWidget(self.table)

        form_layout = QHBoxLayout()
        self.zone_input = QLineEdit()
        self.zone_input.setPlaceholderText("Зона")
        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText("Тариф")
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())

        form_layout.addWidget(self.zone_input)
        form_layout.addWidget(self.value_input)
        form_layout.addWidget(self.date_input)

        self.layout().addLayout(form_layout)

        button_layout = QHBoxLayout()
        add_button = QPushButton("Добавить")
        add_button.clicked.connect(self.add_tariff)
        del_button = QPushButton("Удалить")
        del_button.clicked.connect(self.delete_selected_tariff)

        button_layout.addWidget(add_button)
        button_layout.addWidget(del_button)
        self.layout().addLayout(button_layout)

        self.load_tariffs()

    def load_tariffs(self):
        self.table.setRowCount(0)
        for row_data in get_tariffs():
            row = self.table.rowCount()
            self.table.insertRow(row)
            for col, data in enumerate(row_data):
                self.table.setItem(row, col, QTableWidgetItem(str(data)))

    def add_tariff(self):
        zone = self.zone_input.text()
        value = self.value_input.text()
        date = self.date_input.date().toPyDate()
        try:
            add_tariff(zone, float(value), date)
            self.zone_input.clear()
            self.value_input.clear()
            self.date_input.setDate(QDate.currentDate())
            self.load_tariffs()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def delete_selected_tariff(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Внимание", "Выберите тариф для удаления.")
            return
        tariff_id = self.table.item(row, 0).text()
        delete_tariff(tariff_id)
        self.load_tariffs()
