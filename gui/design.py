import os
import sys
from urllib import request
from PyQt5 import QtWidgets
import requests
from PyQt5.QtGui import QIcon, QPixmap

from gui import login, registration, chat


def clear_form(self):
    """Очистка формы от введенных значений и маркеров ошибок."""
    self.ui.login_in.setText('')
    self.ui.password_in.setText('')
    self.ui.error_label.setText('')
    self.ui.login_in.setStyleSheet('''''')
    self.ui.password_in.setStyleSheet('''''')


def change_windows(self, window_to_open):
    """Переход на другое окно."""
    clear_form(self)
    window_to_open.show()
    self.close()


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
        self.ui.password_in.setStyleSheet('''''')
    if 'email_err' in err_log:
        if err_log['email_err']:
            self.ui.email_in.setStyleSheet(
                '''
                border: 2px solid rgb(255, 55, 118);
                '''
            )
        else:
            self.ui.email_in.setStyleSheet('''''')
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
        change_windows(self, registration_window)

    def to_chat_form(self):
        """Переход на форму чата."""
        change_windows(self, chat_window)
        chat_window.view_chats()

    def login(self):
        """Вход пользователя в систему."""
        username = self.ui.login_in.text()
        psw = self.ui.password_in.text()
        response = requests.post('http://127.0.0.1:5000/corporate_chat',
                                 data={'username': username, 'psw': psw})
        err_log = response.json()
        if err_log['msg']:
            show_input_errors(self, err_log)
        else:
            chat_window.current_user = username
            chat_window.current_user_id = err_log['user_id']
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
        self.ui.to_login_button.clicked.connect(self.to_login_form)

    def to_login_form(self):
        """Переход на форму логина."""
        self.ui.email_in.setText('')
        self.ui.email_in.setStyleSheet('''''')
        change_windows(self, login_window)

    def register(self):
        """Регистрация пользователя."""
        username = self.ui.login_in.text()
        psw = self.ui.password_in.text()
        email = self.ui.email_in.text()
        response = requests.post('http://127.0.0.1:5000/corporate_chat/register',
                                 data={'username': username, 'psw': psw, 'email': email})
        err_log = response.json()
        if err_log['msg']:
            show_input_errors(self, err_log)
        else:
            # переход на форму логина
            self.to_login_form()


class MessageItemForm(QtWidgets.QWidget):
    """Форма одного сообщения."""

    def __init__(self, msg_text, msg_time, sender):
        super().__init__()

        self.msg = QtWidgets.QLabel(f'{sender}: {msg_text}')
        self.time = QtWidgets.QLabel(msg_time)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.msg)
        layout.addWidget(self.time)

        self.setLayout(layout)


class ChatItemForm(QtWidgets.QWidget):
    """Форма одного чата в списке доступных."""

    def __init__(self, chat_name, last_msg=''):
        super().__init__()

        self.chat_name = QtWidgets.QLabel(chat_name)
        self.last_msg = QtWidgets.QLabel(last_msg)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.chat_name)
        if last_msg != '':
            layout.addWidget(self.last_msg)
        self.setLayout(layout)


class ChatForm(QtWidgets.QMainWindow, chat.Ui_ChatForm):
    """Класс формы чата."""

    def __init__(self):
        super().__init__()
        self.ui = chat.Ui_ChatForm()
        self.ui.setupUi(self)
        self.current_user = ''
        self.current_user_id = 0
        self.current_chat = 0
        self.current_user_avatar = ''
        self.temp_chat = None

        self.ui.send_message.setEnabled(False)

        # связки кнопок и функций
        self.ui.send_message.clicked.connect(self.send_message)
        self.ui.find_user_button.clicked.connect(self.find_user)

        # связка списка чатов с функцией
        self.ui.chats.itemClicked.connect(self.open_chat)

    def view_avatar(self, filename=''):
        """Загрузка изображения для аватара."""
        icon = QIcon()
        icon_path = os.getcwd() + "\\gui\\images\\" + filename
        print(icon_path)
        loaded_icon = QPixmap(icon_path)
        if loaded_icon.isNull():
            response = requests.post('http://127.0.0.1:5000/corporate_chat/load_avatar',
                                     data={'id': self.current_user_id},
                                     stream=True)
            with open(icon_path, 'wb') as f:
                for block in response.iter_content(1024):
                    if not block:
                        break
                    f.write(block)
        icon.addPixmap(loaded_icon)
        return icon

    def add_msg_item(self, msg_text, msg_time, sender, url=''):
        """Добавление нового msg_item объекта в QListWidget."""
        item = QtWidgets.QListWidgetItem(self.ui.messages)
        msg = MessageItemForm(msg_text, msg_time, sender)

        item.setIcon(self.view_avatar(url))
        item.setSizeHint(msg.sizeHint())
        self.ui.messages.addItem(item)
        self.ui.messages.setItemWidget(item, msg)
        self.ui.messages.scrollToItem(item)

        self.ui.message_text.clear()

    def add_chat_item(self, chat_name, url='', last_msg='', chat_id=None, user_id=None):
        """Добавление нового chat_item объекта в QListWidget."""
        chat_name = chat_name.replace(self.current_user, '')
        chat_name = chat_name.replace(',', '')

        item = QtWidgets.QListWidgetItem()
        chat = ChatItemForm(chat_name, last_msg)

        item.chat_name = chat_name

        item.user_id = user_id
        item.chat_id = chat_id

        item.setIcon(self.view_avatar(url))
        item.setSizeHint(chat.sizeHint())
        self.ui.chats.addItem(item)
        self.ui.chats.setItemWidget(item, chat)

    def view_chats(self):
        response = requests.post('http://127.0.0.1:5000/corporate_chat/receive_user_chats',
                                 data={'username': self.current_user})
        chats = (response.json())['chats']
        self.ui.chats.clear()
        if len(chats) > 0:
            self.ui.no_user_label.setText('')
            for chat in chats:
                self.add_chat_item(chat_name=chat['chat_name'],
                                   last_msg=chat['last_msg'],
                                   chat_id=chat['chat_id'],
                                   url=chat['avatar'])
        else:
            self.ui.no_user_label.setText('no chats yet')

    def view_msgs(self):
        """Выводит сообщения данного чата."""
        self.ui.messages.clear()
        response = requests.post('http://127.0.0.1:5000/corporate_chat/receive_messages',
                                 data={'chat_id': self.current_chat})
        msgs = response.json()
        for msg in msgs['msgs']:
            self.add_msg_item(msg['msg_text'], msg['send_time'], msg['sender'], msg['avatar'])

    def send_message(self):
        """Отправка сообщения в чате."""
        msg_text = self.ui.message_text.toPlainText()
        if msg_text:
            if self.temp_chat:
                self.create_new_chat(self.temp_chat.chat_name, self.temp_chat.user_id)
                self.temp_chat = None
            response = requests.post('http://127.0.0.1:5000/corporate_chat/send_message',
                                     data={'sender': self.current_user, 'to_chat': self.current_chat, 'msg': msg_text})
            msg_time = response.json()['send_time']
            self.add_msg_item(msg_text, msg_time['send_time'], self.current_user)
            self.view_chats()

    def find_user(self):
        """Поиск пользователя по введенному значению."""
        example_username = self.ui.find_user.text()
        if example_username:
            response = requests.post('http://127.0.0.1:5000/corporate_chat/find_user_by_name',
                                     data={'example_username': example_username,
                                           'current_user_id': self.current_user_id})
            user_list = response.json()

            if len(user_list['suitable_chats']) > 0 or len(user_list['suitable_users']) > 0:
                self.ui.chats.clear()
                self.ui.no_user_label.setText('')

                if len(user_list['suitable_chats']) > 0:
                    self.ui.chats.addItem('~~chats~~')
                    for suitable_chat in user_list['suitable_chats']:
                        self.add_chat_item(chat_name=suitable_chat['chat_name'],
                                           last_msg=suitable_chat['last_msg'],
                                           chat_id=suitable_chat['chat_id'],
                                           url=suitable_chat['avatar'])

                if len(user_list['suitable_users']) > 0:
                    self.ui.chats.addItem('~~users~~')
                    for suitable_user in user_list['suitable_users']:
                        self.add_chat_item(chat_name=suitable_user['username'],
                                           user_id=suitable_user['user_id'],
                                           url=suitable_user['avatar'])

            else:
                self.ui.chats.clear()
                self.ui.no_user_label.setText('no such user')
        else:
            self.ui.chat_name.setText('')
            self.view_chats()

    def create_new_chat(self, companion, companion_id):
        """Создает новый чат."""
        user_ids = ''.join(str(id) for id in [self.current_user_id, companion_id])
        response = requests.post('http://127.0.0.1:5000/corporate_chat/start_new_chat',
                                 data={'users': f'{companion},{self.current_user}',
                                       'users_ids': user_ids})
        chat_info = response.json()
        self.current_chat = chat_info['chat_id']
        self.view_chats()

    def open_chat(self, chat):
        """Открытие конкретного чата."""
        self.ui.send_message.setEnabled(True)
        companion = chat.chat_name
        self.ui.chat_name.setText(companion)
        if chat.chat_id is None:
            self.temp_chat = chat
        else:
            self.current_chat = chat.chat_id
            self.view_msgs()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    chat_window = ChatForm()
    # chat_window.current_user = 'Alice'
    # chat_window.current_user_id = 1
    # chat_window.view_chats()
    # chat_window.show()
    # Спрятано до введения отслеживания авторизации
    registration_window = RegistrationForm()
    login_window = LoginForm()
    login_window.show()
    app.exec_()
