import sys
from coolstyle import CoolStyle
from mainwindow import MainWindow
from PyQt6.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)

    app.setApplicationName("SwingToCompose")
    app.setApplicationDisplayName("Swing to Compose")
    app.setDesktopFileName("swingtocompose")

    if hasattr(app, 'setWindowClass'):
        app.setWindowClass("SwingToCompose")

    CoolStyle.apply_to_application(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
