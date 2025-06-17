# app/gui.py
from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton,
    QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout
)

class MainApp(QMainWindow):
    def __init__(self, user_id=None, role=None):
        super().__init__()
        self.user_id = user_id
        self.role = role
        self.setWindowTitle("АИС Учёт оплаты электроэнергии")
        self.setGeometry(100, 100, 1100, 700)

        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_abonent_tab(), "Абоненты")
        self.tabs.addTab(self.create_meter_tab(), "Счётчики")
        self.tabs.addTab(self.create_reading_tab(), "Показания")
        self.tabs.addTab(self.create_tariff_tab(), "Тарифы")
        self.tabs.addTab(self.create_payment_tab(), "Оплаты")
        self.tabs.addTab(self.create_report_tab(), "Отчёты")

        # Админ видит вкладку пользователей
        if self.role == "admin":
            self.tabs.addTab(self.create_user_tab(), "Пользователи")

        self.setCentralWidget(self.tabs)

    def create_tab(self, column_names, tab_name):
        tab = QWidget()
        layout = QVBoxLayout()

        table = QTableWidget()
        table.setColumnCount(len(column_names))
        table.setHorizontalHeaderLabels(column_names)
        layout.addWidget(table)

        btn_layout = QHBoxLayout()
        for name in ["Добавить", "Редактировать", "Удалить"]:
            btn_layout.addWidget(QPushButton(name))

        layout.addLayout(btn_layout)
        tab.setLayout(layout)
        return tab

    def create_abonent_tab(self):
        return self.create_tab(["ФИО", "Адрес", "Лицевой счёт"], "Абоненты")

    def create_meter_tab(self):
        return self.create_tab(["Серийный номер", "Тип", "Дата установки", "Абонент"], "Счётчики")

    def create_reading_tab(self):
        return self.create_tab(["Счётчик", "Дата", "Показание", "Абонент"], "Показания")

    def create_tariff_tab(self):
        return self.create_tab(["Зона", "Тариф (руб/кВт·ч)", "Дата ввода"], "Тарифы")

    def create_payment_tab(self):
        return self.create_tab(["Дата оплаты", "Сумма", "Абонент", "Период"], "Оплаты")

    def create_report_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Выберите отчёт:"))

        reports = [
            "Задолженность по абонентам",
            "Потребление за период",
            "Оплаты и начисления",
            "Общий отчёт по району"
        ]

        for r in reports:
            layout.addWidget(QPushButton(r))

        tab.setLayout(layout)
        return tab

    def create_user_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.user_table = QTableWidget()
        self.user_table.setColumnCount(2)
        self.user_table.setHorizontalHeaderLabels(["Логин", "Роль"])
        self.load_user_table()

        layout.addWidget(self.user_table)

        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Добавить")
        edit_btn = QPushButton("Редактировать")
        del_btn = QPushButton("Удалить")

        add_btn.clicked.connect(self.show_add_user_dialog)
        edit_btn.clicked.connect(self.show_edit_user_dialog)
        del_btn.clicked.connect(self.confirm_delete_user)

        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(del_btn)

        layout.addLayout(btn_layout)
        tab.setLayout(layout)
        return tab

