from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFormLayout,
    QLineEdit, QGroupBox, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt
import os


class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())

        self.layout().addWidget(QLabel("<h2>Настройки приложения</h2>"))

        # Группа: Параметры подключения к БД
        self.db_group = QGroupBox("Параметры базы данных")
        db_layout = QFormLayout()

        self.db_host_input = QLineEdit("localhost")
        self.db_port_input = QLineEdit("5432")
        self.db_name_input = QLineEdit("energy")
        self.db_user_input = QLineEdit("postgres")
        self.db_password_input = QLineEdit()
        self.db_password_input.setEchoMode(QLineEdit.EchoMode.Password)

        db_layout.addRow("Хост:", self.db_host_input)
        db_layout.addRow("Порт:", self.db_port_input)
        db_layout.addRow("База данных:", self.db_name_input)
        db_layout.addRow("Пользователь:", self.db_user_input)
        db_layout.addRow("Пароль:", self.db_password_input)

        self.save_db_button = QPushButton("Сохранить настройки БД")
        self.save_db_button.clicked.connect(self.save_db_settings)

        db_layout.addRow(self.save_db_button)
        self.db_group.setLayout(db_layout)
        self.layout().addWidget(self.db_group)

        # Группа: Резервное копирование
        self.backup_group = QGroupBox("Резервное копирование и восстановление")
        backup_layout = QVBoxLayout()

        self.backup_button = QPushButton("Создать резервную копию")
        self.restore_button = QPushButton("Восстановить из резервной копии")

        self.backup_button.clicked.connect(self.backup_database)
        self.restore_button.clicked.connect(self.restore_database)

        backup_layout.addWidget(self.backup_button)
        backup_layout.addWidget(self.restore_button)
        self.backup_group.setLayout(backup_layout)

        self.layout().addWidget(self.backup_group)
        self.layout().addStretch()

    def save_db_settings(self):
        QMessageBox.information(self, "Сохранение", "Настройки подключения к базе данных сохранены (пока не реализовано).")

    def backup_database(self):
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить резервную копию", "", "SQL Files (*.sql)")
        if path:
            try:
                os.system(f'pg_dump -U postgres -d energy -f "{path}"')
                QMessageBox.information(self, "Резервное копирование", "Резервная копия успешно создана.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при создании резервной копии: {e}")

    def restore_database(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выбрать файл резервной копии", "", "SQL Files (*.sql)")
        if path:
            try:
                os.system(f'psql -U postgres -d energy -f "{path}"')
                QMessageBox.information(self, "Восстановление", "База данных успешно восстановлена.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при восстановлении: {e}")
