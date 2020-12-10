import sys
from PyQt5 import QtWidgets
from gui import main_design


class ExampleApp(QtWidgets.QMainWindow, main_design.Ui_MainWindow):
    """Класс дизайна основного окна приложения."""
    def __init__(self):
        super().__init__()
        self.setupUi(self)


def main():
    """Показ окна и запуск приложения."""
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()