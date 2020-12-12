import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

from gui import login


class ExampleApp(QtWidgets.QMainWindow, login.Ui_LoginWindow):
    """Класс дизайна формы входа."""
    def __init__(self):
        super().__init__()
        self.setupUi(self)


def main():
    """Показ окна и запуск приложения."""
    app = QApplication([])
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
