import sys
from PyQt5 import QtWidgets
import requests
from gui import login, registration, chat


def clear_form(self):
    """Очистка формы от введеных значений и маркеров ошибок."""
    self.ui.login_in.setText('')
    self.ui.password_in.setText('')
    self.ui.error_label.setText('')
    self.ui.login_in.setStyleSheet('''''')
    self.ui.login_in.setStyleSheet('''''')


def show_input_errors(self, err_log):
    """Выделение ошибок ввода данных."""
    if err_log['username_err']:
        self.ui.login_in.setStyleSheet(
            '''
            border: 2px solid rgb(255, 55, 118);
            '''
        )
    else:
        self.ui.login_in.setStyleSheet('''''')
    if err_log['psw_err']:
        self.ui.password_in.setStyleSheet(
            '''
            border: 2px solid rgb(255, 55, 118);
            '''
        )
    else:
        self.ui.login_in.setStyleSheet('''''')
    answer = err_log['msg']
    self.ui.error_label.setText(answer)


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

    def to_chat_form(self):
        """Переход на форму чата."""
        chat_window.show()
        self.close()

    def login(self):
        """Вход пользователя в систему."""
        username = self.ui.login_in.text()
        psw = self.ui.password_in.text()
        response = requests.post('http://127.0.0.1:5000/corporate_chat',
                                 data={'username': username, 'psw': psw})
        print(response)
        err_log = response.json()
        if err_log['msg']:
            show_input_errors(self, err_log)
        else:
            clear_form(self)
            chat_window.current_user = username
            # Переход на форму чата
            self.to_chat_form()


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

    def to_login_form(self):
        """Переход на форму логина."""
        login_window.show()
        self.close()

    def register(self):
        """Регистрация пользователя."""
        username = self.ui.login_in.text()
        psw = self.ui.password_in.text()
        response = requests.post('http://127.0.0.1:5000/corporate_chat/register',
                                 data={'username': username, 'psw': psw})
        err_log = response.json()
        if err_log['msg']:
            show_input_errors(self, err_log)
        else:
            clear_form(self)
            # Переход на форму логина
            self.to_login_form()


class ChatForm(QtWidgets.QMainWindow, chat.Ui_ChatForm):
    """Класс формы чата."""

    def __init__(self):
        super().__init__()
        self.ui = chat.Ui_ChatForm()
        self.ui.setupUi(self)
        self.current_user = ''

        # Список всех чатов
        response = requests.get('http://127.0.0.1:5000/corporate_chat/receive_user_list')
        data = response.json()
        self.ui.chats.addItems(data['users'])

        self.ui.send_message.clicked.connect(self.send_message)

    def send_message(self):
        msg_text = self.ui.message_text.toPlainText()
        from_user = self.current_user
        to_user = 'Mur'
        response = requests.post('http://127.0.0.1:5000/corporate_chat/send_message',
                                 data={'from_user': from_user, 'to_user': to_user, 'msg': msg_text})
        self.ui.messages.addItem(f'{from_user}: {msg_text}')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    chat_window = ChatForm()
    registration_window = RegistrationForm()
    login_window = LoginForm()
    login_window.show()
    app.exec_()
