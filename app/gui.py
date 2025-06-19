import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QMainWindow, QTabWidget, QPushButton, QScrollArea, QApplication,
)

from app.tabs.abonents_tab import AbonentsTab
from app.tabs.debt_tab import DebtTab
from app.tabs.meters_tab import MetersTab
from app.tabs.payments_tab import PaymentsTab
from app.tabs.readings_tab import ReadingsTab
from app.tabs.reports_tab import ReportsTab
from app.tabs.settings_tab import SettingsTab
from app.tabs.tariffs_tab import TariffsTab
from app.tabs.user_tab import UserTab


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

        self.tabs.addTab(AbonentsTab(), "Абоненты")
        self.tabs.addTab(MetersTab(), "Счетчики")
        self.tabs.addTab(ReadingsTab(), "Показания")
        self.tabs.addTab(PaymentsTab(), "Оплаты")
        self.tabs.addTab(ReportsTab(), "Отчёты")
        self.tabs.addTab(DebtTab(), "Задолженность")

        if self.role in ("admin", 'inspector'):
            self.tabs.addTab(TariffsTab(), "Тарифы")

        if self.role == "admin":
            self.tabs.addTab(UserTab(), "Пользователи")
            self.tabs.addTab(SettingsTab(), "Настройки")

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


def main():
    app = QApplication(sys.argv)


    main_window = MainApp(current_user='admin', role='admin')
    main_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()