import sys
from PyQt5 import QtWidgets
import requests
from gui import login, registration


class LoginForm(QtWidgets.QMainWindow, login.Ui_LoginForm):
    """Класс формы входа."""

    def __init__(self):
        super().__init__()
        self.ui = login.Ui_LoginForm()
        self.ui.setupUi(self)

        # точки для ввода пароля
        self.ui.password_in.setEchoMode(QtWidgets.QLineEdit.Password)

        # связки кнопок и функций
        self.ui.to_sign_up_button.clicked.connect(self.to_registration_form)
        self.ui.sign_in_button.clicked.connect(self.login)

    def to_registration_form(self):
        """Переход на форму регистрации."""
        registration_window.show()
        self.close()

    def login(self):
        """Вход пользователя в систему."""
        username = self.ui.login_in.text()
        psw = self.ui.password_in.text()
        response = requests.post('http://127.0.0.1:5000/corporate_chat',
                                 data={'username': username, 'psw': psw})
        err_log = response.json()
        if err_log['username_err']:
            self.ui.login_in.setStyleSheet(
                '''
                border: 2px solid rgb(255, 55, 118);
                '''
            )
        else:
            self.ui.login_in.setStyleSheet(
                '''
                '''
            )
        if err_log['psw_err']:
            self.ui.password_in.setStyleSheet(
                '''
                border: 2px solid rgb(255, 55, 118);
                '''
            )
        else:
            self.ui.password_in.setStyleSheet(
                '''
                '''
            )
        answer = err_log['msg']
        self.ui.error_label.setText(answer)
        print(answer)


class RegistrationForm(QtWidgets.QMainWindow, registration.Ui_RegisterForm):
    """Класс формы регистрации."""

    def __init__(self):
        super().__init__()
        self.ui = registration.Ui_RegisterForm()
        self.ui.setupUi(self)

        # точки для ввода пароля
        self.ui.password_in.setEchoMode(QtWidgets.QLineEdit.Password)

        # связки кнопок и функций
        self.ui.sign_up_button.clicked.connect(self.register)

    def register(self):
        """Регистрация пользователя."""
        username = self.ui.login_in.text()
        psw = self.ui.password_in.text()
        response = requests.post('http://127.0.0.1:5000/corporate_chat/register',
                                 data={'username': username, 'psw': psw})
        print(response)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    login_window = LoginForm()
    registration_window = RegistrationForm()
    login_window.show()
    app.exec_()
