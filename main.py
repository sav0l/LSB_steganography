#!/usr/bin/python3
import sys

from PyQt5.QtWidgets import QApplication

from MainWindow import MainWindow


def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
