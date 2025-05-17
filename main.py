import sys
from coolstyle import CoolStyle
from mainwindow import MainWindow
from PyQt6.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)

    CoolStyle.apply_to_application(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
