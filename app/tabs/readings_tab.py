
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox, QInputDialog
from PyQt6.QtCore import Qt
from app.readings import get_all_readings, add_reading, delete_reading
from app.logging import log_action
from app.session import current_user_id


class ReadingsTab(QWidget):
    """
    Вкладка управления показаниями счётчиков.
    Позволяет добавлять, просматривать и удалять показания.
    """
    def __init__(self):
        """
        Инициализация интерфейса вкладки показаний.
        """
        super().__init__()
        layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Дата", "Показание", "Счётчик", "Абонент"])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()

        add_btn = QPushButton("Добавить")
        add_btn.clicked.connect(self.add_reading)
        btn_layout.addWidget(add_btn)

        del_btn = QPushButton("Удалить")
        del_btn.clicked.connect(self.delete_reading)
        btn_layout.addWidget(del_btn)

        layout.addLayout(btn_layout)
        self.load_data()

    def load_data(self):
        """
        Загружает данные показаний из базы данных в таблицу.
        """
        self.table.setRowCount(0)
        for row_data in get_all_readings():
            row = self.table.rowCount()
            self.table.insertRow(row)
            for col, item in enumerate(row_data):
                self.table.setItem(row, col, QTableWidgetItem(str(item)))

    def add_reading(self):
        """
        Добавляет новое показание счётчика.
        """
        date, ok = QInputDialog.getText(self, "Добавить показание", "Введите дату (ГГГГ-ММ-ДД):")
        if not ok or not date:
            return
        value, ok = QInputDialog.getInt(self, "Добавить показание", "Введите значение:")
        if not ok:
            return
        meter_id, ok = QInputDialog.getInt(self, "Добавить показание", "Введите ID счётчика:")
        if not ok:
            return
        try:
            add_reading(date, value, meter_id)
            log_action(current_user_id, f"Добавлено показание: {value} на счётчик {meter_id} ({date})")
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить показание: {e}")

    def delete_reading(self):
        """
        Удаляет выбранное показание.
        """
        selected = self.table.currentRow()
        if selected >= 0:
            reading_id = int(self.table.item(selected, 0).text())
            confirm = QMessageBox.question(
                self, "Подтверждение удаления",
                f"Удалить показание с ID {reading_id}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirm == QMessageBox.StandardButton.Yes:
                delete_reading(reading_id)
                log_action(current_user_id, f"Удалено показание ID {reading_id}")
                self.load_data()
