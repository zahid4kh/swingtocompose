from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont, QColor, QPalette


class CoolStyle:

    @staticmethod
    def apply_to_application(app: QApplication):
        app.setStyle("Fusion")

        dark_palette = QPalette()

        dark_palette.setColor(QPalette.ColorGroup.All,
                              QPalette.ColorRole.Window, QColor(53, 53, 53))
        dark_palette.setColor(
            QPalette.ColorGroup.All, QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorGroup.All,
                              QPalette.ColorRole.Base, QColor(42, 42, 42))
        dark_palette.setColor(
            QPalette.ColorGroup.All, QPalette.ColorRole.AlternateBase, QColor(66, 66, 66))
        dark_palette.setColor(QPalette.ColorGroup.All,
                              QPalette.ColorRole.ToolTipBase, QColor(25, 25, 25))
        dark_palette.setColor(
            QPalette.ColorGroup.All, QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorGroup.All,
                              QPalette.ColorRole.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorGroup.All,
                              QPalette.ColorRole.Button, QColor(53, 53, 53))
        dark_palette.setColor(
            QPalette.ColorGroup.All, QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorGroup.All,
                              QPalette.ColorRole.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorGroup.All,
                              QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(
            QPalette.ColorGroup.All, QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))

        app.setPalette(dark_palette)

        app.setStyleSheet("""
            QPushButton {
                background-color: #3E7BFA;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #2A68E8;
            }
            
            QPushButton:pressed {
                background-color: #1E59D9;
            }
            
            QTextEdit {
                border: 1px solid #555;
                border-radius: 4px;
                padding: 4px;
                background-color: #2D2D2D;
                color: #EEEEEE;
                selection-background-color: #3E7BFA;
            }
            
            QSplitter::handle {
                background-color: #555;
            }
            
            QProgressBar {
                border: 1px solid #555;
                border-radius: 4px;
                background-color: #2D2D2D;
                text-align: center;
                color: white;
            }
            
            QProgressBar::chunk {
                background-color: #3E7BFA;
                width: 1px;
            }
        """)

    @staticmethod
    def get_code_font() -> QFont:
        font = QFont()
        for font_name in ["Cascadia Code", "Consolas", "DejaVu Sans Mono", "Courier New", "Monospace"]:
            font.setFamily(font_name)
            if font.exactMatch():
                break

        font.setPointSize(10)
        return font
