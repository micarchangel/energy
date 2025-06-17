from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QMainWindow, QTabWidget, QPushButton, QScrollArea
)
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

class MainApp(QMainWindow):
    def __init__(self, current_user=None, role=None):
        super().__init__()
        self.current_user = current_user
        self.role = role

        self.setWindowTitle(f"АИС Учёт электроэнергии — {self.current_user} ({self.role})")
        self.resize(1280, 720)
        self.setMinimumSize(1280, 720)
        self.setMaximumSize(3840, 2160)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.apply_styles()

        self.tabs.addTab(self.create_user_tab(), "Пользователи")
        self.tabs.addTab(self.create_clients_tab(), "Абоненты")
        self.tabs.addTab(self.create_meters_tab(), "Счетчики")
        self.tabs.addTab(self.create_meter_readings_tab(), "Показания")
        self.tabs.addTab(self.create_payments_tab(), "Оплаты")
        self.tabs.addTab(self.create_reports_tab(), "Отчёты")

        if self.role == "admin":
            self.tabs.addTab(self.create_admin_tab(), "Настройки")

    def apply_styles(self):
        self.setStyleSheet("""
            QPushButton {
                background-color: #0073e6;
                color: white;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #005BAA;
            }
            QLabel {
                font-size: 16px;
            }
            QMainWindow {
                background-color: white;
            }
        """)

    def create_tab(self, title, elements):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(title))
        for text in elements:
            layout.addWidget(QPushButton(text))
        layout.addStretch()
        scroll = QScrollArea()
        container = QWidget()
        container.setLayout(layout)
        scroll.setWidget(container)
        scroll.setWidgetResizable(True)
        wrapper = QVBoxLayout()
        wrapper.addWidget(scroll)
        tab.setLayout(wrapper)
        return tab

    def create_user_tab(self):
        return self.create_tab("Управление пользователями", [
            "Добавить пользователя",
            "Редактировать пользователя",
            "Удалить пользователя"
        ])

    def create_clients_tab(self):
        return self.create_tab("Работа с абонентами", [
            "Добавить абонента",
            "Редактировать абонента",
            "Удалить абонента",
            "Поиск по ИНН/ФИО"
        ])

    def create_meters_tab(self):
        return self.create_tab("Устройства учета", [
            "Добавить счетчик",
            "Привязать к абоненту",
            "Редактировать / удалить"
        ])

    def create_meter_readings_tab(self):
        return self.create_tab("Учёт показаний", [
            "Ввести показания",
            "Просмотреть историю",
            "Автоматическая проверка и расчёт"
        ])

    def create_payments_tab(self):
        return self.create_tab("Учёт оплат", [
            "Ввести оплату",
            "Просмотр по периоду",
            "Фильтрация должников"
        ])

    def create_reports_tab(self):
        return self.create_tab("Отчётность", [
            "Сформировать квитанцию",
            "Сводный отчёт по оплатам",
            "Экспорт в Excel / PDF"
        ])

    def create_admin_tab(self):
        return self.create_tab("Администрирование", [
            "Резервное копирование",
            "Восстановление из копии",
            "Управление базой данных"
        ])
