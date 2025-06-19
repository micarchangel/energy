import csv
import xlsxwriter
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt
import psycopg2


class ReportsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.info_label = QLabel("Выберите формат отчета для выгрузки:")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.info_label)

        self.export_csv_button = QPushButton("Выгрузить отчёт (CSV)")
        self.export_csv_button.clicked.connect(self.export_to_csv)
        self.layout.addWidget(self.export_csv_button)

        self.export_xls_button = QPushButton("Выгрузить отчёт (XLSX)")
        self.export_xls_button.clicked.connect(self.export_to_xlsx)
        self.layout.addWidget(self.export_xls_button)

        self.setLayout(self.layout)

    def fetch_data(self):
        try:
            conn = psycopg2.connect(
                dbname="energy",
                user="postgres",
                password="1Wizard1",
                host="localhost",
                port="5432"
            )
            cur = conn.cursor()
            cur.execute("""
                SELECT 
                    a.full_name AS "Абонент",
                    a.account_number AS "Лицевой счёт",
                    m.serial_number AS "Счётчик",
                    r.value AS "Показание",
                    r.reading_date AS "Дата",
                    p.amount AS "Оплата",
                    p.pay_date AS "Дата оплаты"
                FROM abonents a
                LEFT JOIN meters m ON a.id = m.abonent_id
                LEFT JOIN readings r ON m.id = r.meter_id
                LEFT JOIN payments p ON a.id = p.abonent_id
                ORDER BY a.full_name, r.reading_date, p.pay_date;
            """)
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            cur.close()
            conn.close()
            return columns, rows
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка подключения к базе данных: {e}")
            return [], []

    def export_to_csv(self):
        columns, data = self.fetch_data()
        if not data:
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить как", "", "CSV Files (*.csv)")
        if not file_path:
            return

        try:
            with open(file_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(columns)
                writer.writerows(data)
            QMessageBox.information(self, "Успешно", "Отчет успешно выгружен в CSV.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл: {e}")

    def export_to_xlsx(self):
        columns, data = self.fetch_data()
        if not data:
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить как", "", "Excel Files (*.xlsx)")
        if not file_path:
            return

        try:
            workbook = xlsxwriter.Workbook(file_path)
            worksheet = workbook.add_worksheet("Отчет")

            for col_num, header in enumerate(columns):
                worksheet.write(0, col_num, header)

            for row_num, row_data in enumerate(data, start=1):
                for col_num, cell_data in enumerate(row_data):
                    worksheet.write(row_num, col_num, cell_data)

            workbook.close()
            QMessageBox.information(self, "Успешно", "Отчет успешно выгружен в XLSX.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл: {e}")