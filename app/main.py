from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("АИС Учёт электроэнергии")
        self.setGeometry(100, 100, 800, 600)

        tabs = QTabWidget()
        tabs.addTab(self.create_abonent_tab(), "Абоненты")
        tabs.addTab(self.create_reading_tab(), "Показания")
        tabs.addTab(self.create_payment_tab(), "Оплаты")
        tabs.addTab(self.create_report_tab(), "Отчёты")

        self.setCentralWidget(tabs)

    def create_abonent_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Здесь будет таблица абонентов"))
        layout.addWidget(QPushButton("Добавить абонента"))
        widget.setLayout(layout)
        return widget

    def create_reading_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Ввод показаний"))
        layout.addWidget(QPushButton("Сохранить показание"))
        widget.setLayout(layout)
        return widget

    def create_payment_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Журнал оплат"))
        layout.addWidget(QPushButton("Добавить оплату"))
        widget.setLayout(layout)
        return widget

    def create_report_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Отчёты"))
        layout.addWidget(QPushButton("Сформировать отчёт"))
        widget.setLayout(layout)
        return widget

if __name__ == "__main__":
    app = QApplication([])
    window = MainApp()
    window.show()
    app.exec()