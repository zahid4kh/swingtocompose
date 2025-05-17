from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox


class ApiKeyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Enter Gemini API Key")
        self.resize(400, 100)

        layout = QFormLayout(self)

        self.api_key_field = QLineEdit()
        self.api_key_field.setPlaceholderText(
            "Paste your Gemini API key here...")
        self.api_key_field.setMinimumWidth(300)

        layout.addRow("API Key:", self.api_key_field)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout.addWidget(self.button_box)

        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #CCCCCC;
            }
            QLineEdit {
                border: 1px solid #555;
                border-radius: 4px;
                padding: 4px;
                background-color: #2D2D2D;
                color: #EEEEEE;
                selection-background-color: #3E7BFA;
            }
            QPushButton {
                background-color: transparent;
                color: #CCCCCC;
                border: 1px solid #666666;
                padding: 8px 16px;
                border-radius: 7px;
                font-weight: bold;
                text-align: center;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid #888888;
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.2);
                border: 1px solid #AAAAAA;
            }
        """)
