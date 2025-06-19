from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QMessageBox, QInputDialog
)
from app.meters import get_all_meters, add_meter, update_meter, delete_meter

class MetersTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Добавить счётчик")
        self.edit_btn = QPushButton("Редактировать")
        self.del_btn = QPushButton("Удалить")
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.del_btn)
        self.layout.addLayout(btn_layout)

        self.add_btn.clicked.connect(self.add_meter)
        self.edit_btn.clicked.connect(self.edit_meter)
        self.del_btn.clicked.connect(self.delete_meter)

        self.load_meters()

    def load_meters(self):
        meters = get_all_meters()
        self.table.setRowCount(len(meters))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Серийный номер", "Тип", "Дата установки", "Абонент"])
        for row, meter in enumerate(meters):
            self.table.setItem(row, 0, QTableWidgetItem(str(meter["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(meter["serial_number"]))
            self.table.setItem(row, 2, QTableWidgetItem(meter["type"]))
            self.table.setItem(row, 3, QTableWidgetItem(str(meter["install_date"])))
            self.table.setItem(row, 4, QTableWidgetItem(meter["full_name"] or ""))

    def add_meter(self):
        serial, ok1 = QInputDialog.getText(self, "Серийный номер", "Введите серийный номер:")
        if not ok1: return
        type_, ok2 = QInputDialog.getText(self, "Тип", "Введите тип счётчика:")
        if not ok2: return
        date, ok3 = QInputDialog.getText(self, "Дата установки", "Введите дату (ГГГГ-ММ-ДД):")
        if not ok3: return
        abonent_id, ok4 = QInputDialog.getInt(self, "ID абонента", "Введите ID абонента:")
        if not ok4: return
        try:
            add_meter(serial, type_, date, abonent_id)
            self.load_meters()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def edit_meter(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Внимание", "Выберите строку для редактирования.")
            return
        meter_id = int(self.table.item(row, 0).text())
        serial, ok1 = QInputDialog.getText(self, "Серийный номер", "Введите серийный номер:", text=self.table.item(row, 1).text())
        if not ok1: return
        type_, ok2 = QInputDialog.getText(self, "Тип", "Введите тип:", text=self.table.item(row, 2).text())
        if not ok2: return
        date, ok3 = QInputDialog.getText(self, "Дата", "Введите дату:", text=self.table.item(row, 3).text())
        if not ok3: return
        abonent_id, ok4 = QInputDialog.getInt(self, "Абонент", "Введите ID абонента:")
        if not ok4: return
        update_meter(meter_id, serial, type_, date, abonent_id)
        self.load_meters()

    def delete_meter(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Внимание", "Выберите строку для удаления.")
            return
        meter_id = int(self.table.item(row, 0).text())
        confirm = QMessageBox.question(self, "Подтверждение", "Удалить этот счётчик?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            delete_meter(meter_id)
            self.load_meters()