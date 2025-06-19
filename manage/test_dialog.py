from PyQt6.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QPushButton

class TestDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Dialog")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Это тестовое окно"))
        self.setLayout(layout)

app = QApplication([])
dlg = TestDialog()
dlg.exec()