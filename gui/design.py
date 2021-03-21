import os
import sys
from PyQt5 import QtWidgets
import requests
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
from gui.gui_classes import login, registration, chat

PASSWORD_IN_STYLE = '''QLineEdit {padding: 5; border-radius: 10px; border: 1px solid #CCCCCC; font: 25 8pt "Yu Gothic UI Light";}'''
ERR_STYLE = '''border: 2px solid rgb(255, 55, 118);'''
USERNAMES_STYLE = '''font: 63 10pt "Yu Gothic UI Semibold";'''
TEXT_STYLE = '''font: 10pt "Yu Gothic UI Semilight";'''


def change_windows(self, window_to_open, login_in_filed=None):
    """Переход на другое окно."""
    self.clear_form()
    if login_in_filed:
        window_to_open.ui.login_in.setFocus()
    window_to_open.show()
    self.close()


def show_input_errors(self, err_log):
    """Выделение ошибок ввода данных."""
    if err_log['username_err']:
        self.ui.login_in.setStyleSheet(ERR_STYLE)
    else:
        self.ui.login_in.setStyleSheet('''''')
    if err_log['psw_err']:
        self.ui.password_in.setStyleSheet(ERR_STYLE)
    else:
        self.ui.password_in.setStyleSheet(PASSWORD_IN_STYLE)
    if 'email_err' in err_log:
        if err_log['email_err']:
            self.ui.email_in.setStyleSheet(ERR_STYLE)
        else:
            self.ui.email_in.setStyleSheet('''''')
    answer = err_log['msg']
    self.ui.error_label.setText(answer)


def download_avatar(user_id, icon_path):
    response = requests.post('http://127.0.0.1:5000/corporate_chat/load_avatar',
                             data={'id': user_id},
                             stream=True)
    with open(icon_path, 'wb') as f:
        for block in response.iter_content(1024):
            if not block:
                f.close()
                break
            f.write(block)


class LoginForm(QtWidgets.QMainWindow, login.Ui_LoginForm):
    """Класс формы входа."""

    def __init__(self):
        super().__init__()
        self.ui = login.Ui_LoginForm()
        self.ui.setupUi(self)

        # связки кнопок и функций
        self.ui.to_sign_up_button.clicked.connect(self.to_registration_form)

        # по нажатию Enter в password_in вызывает login
        self.ui.sign_in_button.clicked.connect(self.login)
        self.ui.sign_in_button.setAutoDefault(True)
        self.ui.password_in.returnPressed.connect(self.login)

        # по нажатию Enter в login_in переводит фокус на password_in
        self.ui.login_in.returnPressed.connect(self.ui.password_in.setFocus)

        self.ui.login_in.setFocus()

    def clear_form(self):
        """Очистка формы от введенных значений и маркеров ошибок."""
        self.ui.login_in.clear()
        self.ui.password_in.clear()
        self.ui.error_label.clear()
        self.ui.login_in.setStyleSheet('''''')
        self.ui.password_in.setStyleSheet(PASSWORD_IN_STYLE)

    def to_registration_form(self):
        """Переход на форму регистрации."""
        change_windows(self, registration_window, login_in_filed=True)

    def to_chat_form(self, username, user_id, avatar):
        """Переход на форму чата."""
        change_windows(self, chat_window)
        chat_window.load_user_data(username, user_id, avatar)

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
            self.to_chat_form(username, err_log['user_id'], err_log['avatar'])


class RegistrationForm(QtWidgets.QMainWindow, registration.Ui_RegisterForm):
    """Класс формы регистрации."""

    def __init__(self):
        super().__init__()
        self.ui = registration.Ui_RegisterForm()
        self.ui.setupUi(self)

        # связки кнопок и функций
        self.ui.sign_up_button.clicked.connect(self.register)
        self.ui.to_login_button.clicked.connect(self.to_login_form)

        # по нажатию Enter в password_in вызывает register
        self.ui.sign_up_button.clicked.connect(self.register)
        self.ui.sign_up_button.setAutoDefault(True)
        self.ui.password_in.returnPressed.connect(self.register)

        # по нажатию Enter в login_in переводит фокус на email_in
        self.ui.login_in.returnPressed.connect(self.ui.email_in.setFocus)
        # по нажатию Enter в email_in переводит фокус на password_in
        self.ui.email_in.returnPressed.connect(self.ui.password_in.setFocus)

        self.ui.login_in.setFocus()

    def clear_form(self):
        """Очистка формы от введенных значений и маркеров ошибок."""
        self.ui.login_in.clear()
        self.ui.password_in.clear()
        self.ui.error_label.clear()
        self.ui.email_in.clear()
        self.ui.login_in.setStyleSheet('''''')
        self.ui.password_in.setStyleSheet(PASSWORD_IN_STYLE)
        self.ui.email_in.setStyleSheet('''''')

    def to_login_form(self):
        """Переход на форму логина."""
        change_windows(self, login_window, login_in_filed=True)

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
        layout = QtWidgets.QFormLayout()

        self.sender = QtWidgets.QLabel(sender)
        self.time = QtWidgets.QLabel(msg_time)
        self.text = QtWidgets.QLabel(msg_text)

        self.set_styles()

        layout.addRow(self.sender, self.time)
        layout.addRow(self.text)

        self.setLayout(layout)

    def set_styles(self):
        """Установка стилей."""
        self.sender.setStyleSheet(USERNAMES_STYLE)
        self.time.setStyleSheet(TEXT_STYLE)
        self.text.setStyleSheet(TEXT_STYLE)

        self.time.setAlignment(Qt.AlignRight)


class ChatItemForm(QtWidgets.QWidget):
    """Форма одного чата в списке доступных."""

    def __init__(self, chat_name, last_msg='', last_activity=''):
        super().__init__()
        layout = QtWidgets.QFormLayout()

        self.chat_name = QtWidgets.QLabel(chat_name)
        self.chat_name.setStyleSheet(USERNAMES_STYLE)
        if last_msg == '':
            layout.addRow(self.chat_name)
        if last_msg != '':
            self.last_msg = QtWidgets.QLabel(last_msg)
            self.last_activity = QtWidgets.QLabel(last_activity)

            self.last_msg.setStyleSheet(TEXT_STYLE)
            self.last_activity.setStyleSheet(TEXT_STYLE)
            self.last_activity.setAlignment(Qt.AlignRight)

            layout.addRow(self.chat_name, self.last_activity)
            layout.addRow(self.last_msg)

        self.setLayout(layout)


class ChatForm(QtWidgets.QMainWindow, chat.Ui_ChatForm):
    """Класс формы чата."""

    def __init__(self):
        super().__init__()
        self.ui = chat.Ui_ChatForm()
        self.ui.setupUi(self)

        self.temp_chat = None
        self.current_chat_id = 0

        self.current_user = ''
        self.current_user_id = 0
        self.current_user_avatar = ''

        self.chat_edit_mode = False

        self.block_buttons()
        self.load_buttons_icons()
        self.hide_menu()
        self.set_avatars_size()

        # связки кнопок и функций
        self.ui.log_out.clicked.connect(self.log_out)
        self.ui.menu_button.clicked.connect(self.show_menu)
        self.ui.avatar.clicked.connect(self.hide_menu)
        self.ui.chat_settings.clicked.connect(self.open_chat_editor)

        # поиск пользователя по каждому введенному символу
        self.ui.find_user.textChanged.connect(self.find_user)

        self.ui.send_message.clicked.connect(self.send_message)
        # self.ui.message_text..connect(self.ui.send_message.click)

        # связка списка чатов с функцией
        self.ui.chats.itemClicked.connect(self.open_chat)

    def open_chat_editor(self):
        """Открывает окно редактирования чата."""
        pass

    def set_avatars_size(self):
        """Установка размеров аватаров."""
        size = QSize(40, 40)
        self.ui.chats.setIconSize(size)
        self.ui.messages.setIconSize(size)

    def load_buttons_icons(self):
        """Загрузка иконок кнопок."""
        self.ui.chat_settings.setIcon(self.load_icon('settings.png'))
        self.ui.log_out.setIcon(self.load_icon('logout.png'))
        self.ui.send_message.setIcon(self.load_icon('send.png'))
        self.ui.menu_button.setIcon(self.load_icon('menu.png'))

    def block_buttons(self):
        """Блокировка кнопок."""
        self.ui.send_message.setDisabled(True)
        self.ui.chat_settings.setDisabled(True)

    def unblock_buttons(self):
        """Разблокировка кнопок."""
        self.ui.send_message.setEnabled(True)
        self.ui.chat_settings.setEnabled(True)

    def hide_menu(self):
        """Выключение меню."""
        self.ui.menu.hide()
        self.ui.menu.setDisabled(True)

    def show_menu(self):
        """Показ меню."""
        self.ui.find_user.clear()
        self.ui.menu.show()
        self.ui.menu.setEnabled(True)

    def clear_form(self):
        """Очистка формы от введенных значений и маркеров ошибок."""
        self.ui.message_text.clear()
        self.ui.find_user.clear()
        self.ui.username_label.clear()
        self.ui.chat_name_lanel.clear()
        self.ui.last_activite_label.clear()
        self.ui.chats.clear()
        self.ui.messages.clear()

    def to_login_form(self):
        """Переход на форму логина."""
        change_windows(self, login_window, login_in_filed=True)

    def log_out(self):
        """Выход из чата."""
        self.delete_user_data()
        self.block_buttons()
        self.hide_menu()
        self.to_login_form()

    def clear_find_user(self):
        self.ui.find_user.clear()
        self.view_chats()

    def delete_user_data(self):
        """Удаление пользовательских данных."""
        self.current_user = ''
        self.current_user_id = 0
        self.current_chat_id = 0
        self.current_user_avatar = ''
        self.temp_chat = None

    def load_user_data(self, username, user_id, avatar):
        """Получает всю необходимую для работы информацию."""
        self.current_user_avatar = avatar
        self.current_user_id = user_id
        self.current_user = username
        self.view_chats()
        self.ui.username_label.setText(username)
        self.ui.avatar.setIcon(self.load_avatar(avatar, user_id))

    @staticmethod
    def load_icon(icon_name):
        """Загрузка изображения."""
        icon = QIcon()
        icon_path = os.getcwd() + "\\gui\\resourses\\" + icon_name
        icon.addPixmap(QPixmap(icon_path))
        return icon

    @staticmethod
    def load_avatar(filename, user_id=''):
        """Загрузка изображения для аватара."""
        icon = QIcon()
        icon_path = os.getcwd() + "\\gui\\cache\\images\\" + filename
        if QPixmap(icon_path).isNull():
            download_avatar(icon_path=icon_path,
                            user_id=user_id)
        icon.addPixmap(QPixmap(icon_path))
        return icon

    def add_msg_item(self, msg_text, msg_time, sender, sender_name, filename):
        """Добавление нового msg_item объекта в QListWidget."""
        item = QtWidgets.QListWidgetItem(self.ui.messages)
        msg = MessageItemForm(msg_text, msg_time, sender_name)

        item.setIcon(self.load_avatar(filename=filename, user_id=sender))
        item.setSizeHint(msg.sizeHint())
        self.ui.messages.addItem(item)
        self.ui.messages.setItemWidget(item, msg)
        self.ui.messages.scrollToItem(item)

        self.ui.message_text.clear()

    @staticmethod
    def chat_items_size():
        """Установка размеров аватаров."""
        return QSize(320, 55)

    def add_chat_item(self, chat_name, filename, last_msg='', last_activity='', chat_id=None, user_id=None,
                      amount_of_users=0):
        """Добавление нового chat_item объекта в QListWidget."""
        chat_name = chat_name.replace(self.current_user, '')
        chat_name = chat_name.replace(',', '')

        item = QtWidgets.QListWidgetItem()
        chat_item = ChatItemForm(chat_name, last_msg, last_activity)

        item.chat_name = chat_name

        item.user_id = user_id
        item.chat_id = chat_id
        item.amount_of_users = amount_of_users

        item.setIcon(self.load_avatar(filename=filename, user_id=item.user_id))
        item.setSizeHint(self.chat_items_size())
        self.ui.chats.addItem(item)
        self.ui.chats.setItemWidget(item, chat_item)

    def view_chats(self):
        """Показ чатов данного пользователя."""
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
                                   filename=chat['avatar'],
                                   user_id=chat['companion_id'],
                                   last_activity=chat['last_activity'],
                                   amount_of_users=chat['amount_of_users']
                                   )
        else:
            self.ui.no_user_label.setText('no chats yet')

    def view_msgs(self):
        """Выводит сообщения данного чата."""
        self.ui.messages.clear()
        response = requests.post('http://127.0.0.1:5000/corporate_chat/receive_messages',
                                 data={'chat_id': self.current_chat_id})
        msgs = response.json()
        for msg in msgs['msgs']:
            self.add_msg_item(msg_text=msg['msg_text'],
                              msg_time=msg['send_time'],
                              sender_name=msg['sender_name'],
                              sender=msg['sender'],
                              filename=msg['avatar'])

    def send_message(self):
        """Отправка сообщения в чате."""
        msg_text = self.ui.message_text.toPlainText()
        msg_text = msg_text.strip()
        if msg_text:
            if self.temp_chat:
                self.ui.find_user.setText('')
                self.create_new_chat(self.temp_chat.chat_name, self.temp_chat.user_id)
                self.temp_chat = None
            response = requests.post('http://127.0.0.1:5000/corporate_chat/send_message',
                                     data={'sender': self.current_user_id, 'to_chat': self.current_chat_id,
                                           'msg': msg_text})
            msg_time = response.json()['send_time']
            self.add_msg_item(msg_text=msg_text,
                              msg_time=msg_time,
                              sender_name=self.current_user,
                              sender=self.current_user_id,
                              filename=self.current_user_avatar)
            self.view_chats()

    def find_user(self):
        """Поиск пользователя по введенному значению."""
        requested_username = self.ui.find_user.text()
        if requested_username:
            response = requests.post('http://127.0.0.1:5000/corporate_chat/find_user_by_name',
                                     data={'requested_username': requested_username,
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
                                           filename=suitable_chat['avatar'],
                                           last_activity=suitable_chat['last_activity'],
                                           amount_of_users=suitable_chat['amount_of_users']
                                           )

                if len(user_list['suitable_users']) > 0:
                    self.ui.chats.addItem('~~users~~')
                    for suitable_user in user_list['suitable_users']:
                        self.add_chat_item(chat_name=suitable_user['username'],
                                           user_id=suitable_user['user_id'],
                                           filename=suitable_user['avatar'])

            else:
                self.ui.chats.clear()
                self.ui.no_user_label.setText('nothing found')
        else:
            self.ui.chat_name_lanel.setText('')
            self.view_chats()

    def create_new_chat(self, companion, companion_id):
        """Создает новый чат."""
        user_ids = ''.join(str(user_id) for user_id in [self.current_user_id, companion_id])
        response = requests.post('http://127.0.0.1:5000/corporate_chat/start_new_chat',
                                 data={'users': f'{companion},{self.current_user}',
                                       'users_ids': user_ids,
                                       'owner': 0})
        chat_info = response.json()
        self.view_chats()
        self.current_chat_id = chat_info['chat_id']

    def clear_msgs(self):
        self.ui.messages.clear()
        self.ui.message_text.clear()

    def open_chat(self, chat):
        """Открытие конкретного чата."""
        self.unblock_buttons()

        self.ui.chat_name_lanel.setText(chat.chat_name)
        self.ui.last_activite_label.setText('was 1 minute ago')

        if chat.chat_id is None:
            self.temp_chat = chat
            self.clear_msgs()
        else:
            self.current_chat_id = chat.chat_id
            self.view_msgs()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    chat_window = ChatForm()
    registration_window = RegistrationForm()
    login_window = LoginForm()
    login_window.show()
    app.exec_()
