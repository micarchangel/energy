from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QHBoxLayout,
    QComboBox, QDateEdit, QPushButton
)
from PyQt6.QtCore import QDate
import psycopg2


class LogsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.filter_layout = QHBoxLayout()

        self.user_combo = QComboBox()
        self.user_combo.setPlaceholderText("Все пользователи")

        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDisplayFormat("yyyy-MM-dd")
        self.date_from.setDate(QDate(2000, 1, 1))  # Минимальная дата

        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDisplayFormat("yyyy-MM-dd")
        self.date_to.setDate(QDate.currentDate())  # По умолчанию — сегодня

        self.filter_button = QPushButton("Применить фильтр")
        self.filter_button.clicked.connect(self.load_logs)

        self.filter_layout.addWidget(QLabel("Пользователь:"))
        self.filter_layout.addWidget(self.user_combo)
        self.filter_layout.addWidget(QLabel("С:"))
        self.filter_layout.addWidget(self.date_from)
        self.filter_layout.addWidget(QLabel("По:"))
        self.filter_layout.addWidget(self.date_to)
        self.filter_layout.addWidget(self.filter_button)

        self.layout.addLayout(self.filter_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Пользователь", "Действие", "Время"])
        self.layout.addWidget(self.table)

        self.load_users()
        self.load_logs()

    def load_users(self):
        try:
            conn = psycopg2.connect(
                dbname="energy", user="postgres", password="1Wizard1", host="localhost", port="5432"
            )
            with conn.cursor() as cur:
                cur.execute("SELECT id, login FROM users ORDER BY login")
                self.user_combo.addItem("Все", None)
                for user_id, login in cur.fetchall():
                    self.user_combo.addItem(login, user_id)
        except Exception as e:
            print(f"[Ошибка загрузки пользователей] {e}")
        finally:
            if conn:
                conn.close()

    def load_logs(self):
        self.table.setRowCount(0)
        selected_user = self.user_combo.currentData()
        date_from_str = self.date_from.date().toString("yyyy-MM-dd")
        date_to_str = self.date_to.date().toString("yyyy-MM-dd")

        query = """
            SELECT logs.id, users.login, logs.action, logs.timestamp
            FROM logs
            LEFT JOIN users ON logs.user_id = users.id
            WHERE 1=1
        """
        params = []

        if selected_user:
            query += " AND logs.user_id = %s"
            params.append(selected_user)

        if date_from_str and date_to_str:
            query += " AND DATE(logs.timestamp) BETWEEN %s AND %s"
            params.append(date_from_str)
            params.append(date_to_str)

        query += " ORDER BY logs.timestamp DESC"

        try:
            conn = psycopg2.connect(
                dbname="energy", user="postgres", password="1Wizard1", host="localhost", port="5432"
            )
            with conn.cursor() as cur:
                cur.execute(query, tuple(params))
                rows = cur.fetchall()
                self.table.setRowCount(len(rows))
                for row_idx, row_data in enumerate(rows):
                    for col_idx, value in enumerate(row_data):
                        self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        except Exception as e:
            print(f"[Ошибка загрузки логов] {e}")
        finally:
            if conn:
                conn.close()
