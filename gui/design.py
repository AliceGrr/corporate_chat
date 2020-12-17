import sys
from PyQt5 import QtWidgets

from gui import login


class LoginWindow(QtWidgets.QMainWindow, login.Ui_LoginWindow):
    """Класс дизайна формы входа."""
    def __init__(self):
        super().__init__()
        self.ui = login.Ui_LoginWindow()
        self.ui.setupUi(self)

        # точки для ввода пароля
        self.ui.password_in.setEchoMode(QtWidgets.QLineEdit.Password)


def main():
    """Показ окна и запуск приложения."""
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
