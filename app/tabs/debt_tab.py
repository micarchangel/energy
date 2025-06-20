from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QFileDialog,
    QMessageBox, QLineEdit, QLabel, QHBoxLayout
)
import csv
import pandas as pd
from app.debt import calculate_debts_for_account
from app.logging import log_action
from app.session import current_user_id


class DebtTab(QWidget):
    """
    Вкладка для отображения и экспорта информации о задолженности абонентов.
    Позволяет выполнять поиск по лицевому счёту и экспортировать данные в CSV или Excel.
    """

    def __init__(self):
        """Инициализация элементов интерфейса вкладки задолженности."""
        super().__init__()
        self.layout = QVBoxLayout(self)

        search_layout = QHBoxLayout()
        self.account_input = QLineEdit()
        self.account_input.setPlaceholderText("Введите лицевой счёт")
        self.search_btn = QPushButton("Поиск")
        self.search_btn.clicked.connect(self.search_by_account)
        search_layout.addWidget(QLabel("Поиск по счёту:"))
        search_layout.addWidget(self.account_input)
        search_layout.addWidget(self.search_btn)
        self.layout.addLayout(search_layout)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.export_csv_btn = QPushButton("Экспорт в CSV")
        self.export_csv_btn.clicked.connect(self.export_to_csv)
        self.layout.addWidget(self.export_csv_btn)

        self.export_xlsx_btn = QPushButton("Экспорт в Excel")
        self.export_xlsx_btn.clicked.connect(self.export_to_xlsx)
        self.layout.addWidget(self.export_xlsx_btn)

    def search_by_account(self):
        """
        Выполняет поиск задолженности по введённому лицевому счёту
        и отображает результаты в таблице.
        """
        account_number = self.account_input.text().strip()
        if not account_number:
            QMessageBox.warning(self, "Ошибка", "Введите лицевой счёт.")
            return

        result = calculate_debts_for_account(account_number)
        if not result:
            QMessageBox.information(self, "Информация", "Данные не найдены.")
            self.table.setRowCount(0)
            return

        self.table.setRowCount(1)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Лицевой счёт", "ФИО", "Начислено", "Оплачено", "Задолженность"]
        )

        self.table.setItem(0, 0, QTableWidgetItem(result["account_number"]))
        self.table.setItem(0, 1, QTableWidgetItem(result["full_name"]))
        self.table.setItem(0, 2, QTableWidgetItem(f"{result['total_charge']:.2f}"))
        self.table.setItem(0, 3, QTableWidgetItem(f"{result['total_payment']:.2f}"))
        self.table.setItem(0, 4, QTableWidgetItem(f"{result['debt']:.2f}"))

        log_action(current_user_id, f"Поиск задолженности по счёту {account_number}")

    def export_to_csv(self):
        """Экспортирует содержимое таблицы в CSV-файл."""
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить в CSV", "", "CSV Files (*.csv)")
        if path:
            with open(path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
                writer.writerow(headers)
                for row in range(self.table.rowCount()):
                    writer.writerow([
                        self.table.item(row, col).text() if self.table.item(row, col) else ""
                        for col in range(self.table.columnCount())
                    ])
            QMessageBox.information(self, "Экспорт", "Файл CSV успешно сохранён!")
            log_action(current_user_id, "Экспорт задолженности в CSV")

    def export_to_xlsx(self):
        """Экспортирует содержимое таблицы в Excel-файл."""
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить в Excel", "", "Excel Files (*.xlsx)")
        if path:
            data = []
            for row in range(self.table.rowCount()):
                row_data = [
                    self.table.item(row, col).text() if self.table.item(row, col) else ""
                    for col in range(self.table.columnCount())
                ]
                data.append(row_data)
            df = pd.DataFrame(data, columns=[self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())])
            df.to_excel(path, index=False)
            QMessageBox.information(self, "Экспорт", "Файл Excel успешно сохранён!")
            log_action(current_user_id, "Экспорт задолженности в Excel")
