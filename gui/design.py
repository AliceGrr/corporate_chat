import sys
import time
from datetime import datetime, timezone
from pathlib import Path
import requests
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QObject, QThread, pyqtSignal

from gui.gui_classes import login, registration, chat

PASSWORD_IN_STYLE = '''padding: 5; border-radius: 10px; border: 1px solid #CCCCCC; font: 25 8pt "Yu Gothic UI Light";'''
PASSWORD_ERR_STYLE = '''padding: 5; border-radius: 10px; border: 2px solid rgb(255, 55, 118); font: 25 8pt "Yu Gothic UI Light";'''
ERR_STYLE = '''border: 2px solid rgb(255, 55, 118);'''
USERNAMES_STYLE = '''font: 63 10pt "Yu Gothic UI Semibold";'''
TEXT_STYLE = '''font: 10pt "Yu Gothic UI Semilight";'''
INFORMATION_ITEM_STYLE = '''font: 63 10pt "Yu Gothic UI Semibold"; background-color:rgb(143, 169, 255); color:rgb(249, 249, 249);'''
SERVER = 'https://corporate--chat.herokuapp.com'


def show_connection_error(self):
    """Выводит сообщение об ошибке соединения."""
    self.ui.connection_error.setText('Connection lost')


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
        self.ui.password_in.setStyleSheet(PASSWORD_ERR_STYLE)
    else:
        self.ui.password_in.setStyleSheet(PASSWORD_IN_STYLE)
    if 'email_err' in err_log:
        if err_log['email_err']:
            self.ui.email_in.setStyleSheet(ERR_STYLE)
        else:
            self.ui.email_in.setStyleSheet('''''')
    answer = err_log['msg']
    self.ui.error_label.setText(answer)
    self.ui.login_in.setFocus()


def hide_input_errors(self, mail=False):
    """Отключение ошибок ввода данных."""
    self.ui.login_in.setStyleSheet('''''')
    self.ui.password_in.setStyleSheet(PASSWORD_IN_STYLE)
    self.ui.connection_error.clear()
    if mail:
        self.ui.email_in.setStyleSheet('''''')
    self.ui.error_label.clear()


def download_avatar(icon_path, user_id=0, chat_id=0):
    chat_window.ui.connection_error.clear()
    try:
        response = requests.post(f'http://{SERVER}/corporate_chat/load_avatar',
                                 data={'user_id': user_id,
                                       'chat_id': chat_id},
                                 stream=True)
    except:
        show_connection_error(chat_window)
    else:
        with open(icon_path, 'wb') as f:
            for block in response.iter_content(1024):
                if not block:
                    f.close()
                    break
                f.write(block)


def delete_avatar(icon_path):
    """Удаляет ненужный файл аватара."""
    p = Path(icon_path)
    p.unlink(icon_path)


def load_icon(icon_name):
    """Загрузка изображения."""
    icon = QIcon()
    icon_path = Path('resources', icon_name)
    icon.addPixmap(QPixmap(str(icon_path)))
    return icon


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

        # по нажатию Enter в login_in переводит фокус на password_in
        self.ui.login_in.returnPressed.connect(self.ui.password_in.setFocus)

        # при изменении текста прячет ошибки
        self.ui.login_in.textChanged.connect(lambda: hide_input_errors(self))
        self.ui.password_in.textChanged.connect(lambda: hide_input_errors(self))

        self.create_worker_thread()

        self.ui.login_in.setFocus()

    def create_worker_thread(self):
        self.worker = LoginWorker()
        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)

        self.sing_in_button_actions()

        self.ui.sign_in_button.pressed.connect(lambda: self.ui.sign_in_button.setEnabled(True))
        self.ui.password_in.returnPressed.connect(lambda: self.ui.sign_in_button.setEnabled(True))
        self.worker.login_log.connect(self.login)
        self.worker.login_log.connect(self.worker_thread.quit)
        self.worker.login_log.connect(self.worker.deleteLater)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)

    def sing_in_button_actions(self):
        self.ui.sign_in_button.pressed.connect(lambda: self.ui.sign_in_button.setDisabled(True))
        self.ui.password_in.returnPressed.connect(lambda: self.ui.sign_in_button.setDisabled(True))

        self.ui.sign_in_button.pressed.connect(lambda: self.worker.login(username=self.ui.login_in.text(),
                                                                         psw=self.ui.password_in.text()))
        self.ui.password_in.returnPressed.connect(lambda: self.worker.login(username=self.ui.login_in.text(),
                                                                            psw=self.ui.password_in.text()))

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

    def login(self, response):
        """Вход пользователя в систему."""
        self.ui.connection_error.clear()
        if len(response) == 1:
            show_connection_error(self)
        else:
            if response['msg']:
                show_input_errors(self, response)
            else:
                self.to_chat_form(response['username'], response['user_id'], response['avatar'])


class RegistrationForm(QtWidgets.QMainWindow, registration.Ui_RegisterForm):
    """Класс формы регистрации."""

    def __init__(self):
        super().__init__()
        self.ui = registration.Ui_RegisterForm()
        self.ui.setupUi(self)

        # связки кнопок и функций
        self.ui.to_login_button.clicked.connect(self.to_login_form)

        # по нажатию Enter в password_in вызывает register
        self.ui.sign_up_button.setAutoDefault(True)

        # по нажатию Enter в login_in переводит фокус на email_in
        self.ui.login_in.returnPressed.connect(self.ui.email_in.setFocus)
        # по нажатию Enter в email_in переводит фокус на password_in
        self.ui.email_in.returnPressed.connect(self.ui.password_in.setFocus)

        # при изменении текста прячет ошибки
        self.ui.login_in.textChanged.connect(lambda: hide_input_errors(self, mail=True))
        self.ui.email_in.textChanged.connect(lambda: hide_input_errors(self, mail=True))
        self.ui.password_in.textChanged.connect(lambda: hide_input_errors(self, mail=True))

        self.create_worker_thread()

        self.ui.login_in.setFocus()

    def create_worker_thread(self):
        self.worker = RegistrationWorker()
        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)

        self.sing_up_button_actions()

        self.ui.sign_up_button.pressed.connect(lambda: self.ui.sign_up_button.setEnabled(True))
        self.ui.password_in.returnPressed.connect(lambda: self.ui.sign_up_button.setEnabled(True))
        self.worker.register_log.connect(self.register)
        self.worker.register_log.connect(self.worker_thread.quit)
        self.worker.register_log.connect(self.worker.deleteLater)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)

    def sing_up_button_actions(self):
        self.ui.sign_up_button.pressed.connect(lambda: self.ui.sign_up_button.setDisabled(True))
        self.ui.password_in.returnPressed.connect(lambda: self.ui.sign_up_button.setDisabled(True))

        self.ui.sign_up_button.pressed.connect(lambda: self.worker.register(username=self.ui.login_in.text(),
                                                                         psw=self.ui.password_in.text(),
                                                                         email=self.ui.email_in.text()))
        self.ui.password_in.returnPressed.connect(lambda: self.worker.register(username=self.ui.login_in.text(),
                                                                            psw=self.ui.password_in.text(),
                                                                            email=self.ui.email_in.text()))

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

    def register(self, response):
        """Регистрация пользователя."""
        self.ui.connection_error.clear()
        if len(response) == 1:
            show_connection_error(self)
        else:
            if response['msg']:
                show_input_errors(self, response)
            else:
                self.to_login_form()


class LoginWorker(QObject):
    """Рабочий класс потока логина."""
    login_log = pyqtSignal(dict)

    def login(self, username, psw):
        try:
            response = requests.post(f'http://{SERVER}/corporate_chat',
                                     data={'username': username, 'psw': psw})
        except Exception as error:
            self.login_log.emit({'error': True})
        else:
            self.login_log.emit(response.json())


class RegistrationWorker(QObject):
    """Рабочий класс потока регистрации."""
    register_log = pyqtSignal(dict)

    def register(self, username, psw, email):
        try:
            response = requests.post(f'http://{SERVER}/corporate_chat/register',
                                     data={'username': username, 'psw': psw, 'email': email})
        except Exception as error:
            self.register_log.emit({'error': True})
        else:
            self.register_log.emit(response.json())


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


def get_local_time(time):
    """Проводит обработку времени"""
    datetime_object = datetime.strptime(time, '%a, %d %b %Y %H:%M:%S %Z')
    local_time = utc_to_local(datetime_object)
    return local_time


def format_chat_and_msg_time(time):
    """Форматирует время в соответствии с разницей от текущего."""
    current_time = datetime.now()

    if current_time.day != time.day:
        local_time = time.strftime('%H:%M, %d %b')
    elif current_time.year != time.year:
        local_time = time.strftime('%H:%M, %d %b %Y')
    else:
        local_time = time.strftime('%H:%M')
    return local_time


def format_user_activity_time(time):
    """Форматирует время в соответствии с разницей от текущего."""
    current_time = datetime.now()
    current_time = current_time.replace(tzinfo=None)
    time = time.replace(tzinfo=None)
    if current_time.day == time.day:
        difference = current_time - time
        if difference.seconds < 15 * 60:
            user_state = 'online'
        else:
            local_time = time.strftime('%H:%M')
            user_state = f'last seen at {local_time}'
    else:
        if current_time.day != time.day:
            local_time = time.strftime('%H:%M, %d %b')
        elif current_time.year != time.year:
            local_time = time.strftime('%H:%M, %d %b %Y')
        user_state = f'last seen at {local_time}'
    return user_state


class MessageItemForm(QtWidgets.QWidget):
    """Форма одного сообщения."""

    def __init__(self, msg_text, msg_time, sender):
        super().__init__()
        layout = QtWidgets.QFormLayout()

        self.sender = QtWidgets.QLabel(sender)
        local_time = format_chat_and_msg_time(get_local_time(msg_time))
        self.time = QtWidgets.QLabel(local_time)
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

        self.chat_name = QtWidgets.QLabel(chat_name[:10])
        self.chat_name.setStyleSheet(USERNAMES_STYLE)
        if last_msg == '':
            layout.addRow(self.chat_name)
        if last_msg != '':
            self.last_msg = QtWidgets.QLabel(last_msg)

            local_time = format_chat_and_msg_time(get_local_time(last_activity))
            if len(local_time) < 6:
                local_time = f'today at {local_time}'
            self.last_activity = QtWidgets.QLabel(local_time)

            self.last_msg.setStyleSheet(TEXT_STYLE)
            self.last_activity.setStyleSheet(TEXT_STYLE)
            self.last_activity.setAlignment(Qt.AlignRight)

            layout.addRow(self.chat_name, self.last_activity)
            layout.addRow(self.last_msg)

        self.setLayout(layout)


class UserItemForm(QtWidgets.QWidget):
    """Форма одного пользователя."""

    def __init__(self, username, action=''):
        super().__init__()
        layout = QtWidgets.QHBoxLayout()

        self.username = QtWidgets.QLabel(username)
        self.username.setStyleSheet(USERNAMES_STYLE)
        layout.addWidget(self.username)

        self.action_button = QtWidgets.QPushButton()
        self.action_button.setFixedSize(40, 40)
        if action == 'add':
            self.action_button.setIcon(load_icon('add.png'))
        elif action == 'leave':
            self.action_button.setIcon(load_icon('logout.png'))
        else:
            self.action_button.setIcon(load_icon('delete.png'))
        layout.addWidget(self.action_button)

        self.setLayout(layout)


class InformationItemForm(QtWidgets.QWidget):
    """Форма информационного поля."""

    def __init__(self, text):
        super().__init__()
        layout = QtWidgets.QHBoxLayout()

        self.text = QtWidgets.QLabel(text)
        self.text.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.text)

        self.setLayout(layout)


class ChatWorker(QObject):
    """Рабочий класс потока обновления информации на клиенте."""
    update_msgs = pyqtSignal(list)
    update_chat_list = pyqtSignal(list)
    update_user_list = pyqtSignal(list)
    update_user_list_while_find = pyqtSignal(list)
    update_chat_list_while_find = pyqtSignal(dict)
    update_chat_info = pyqtSignal(dict)

    def update_client_thread(self):
        """Поток обновления информации на клиенте."""
        while True:
            if chat_window.current_user_id:
                self.update_client()
            time.sleep(5)

    def update_client(self):
        """Обновление информации на клиенте."""
        if chat_window.chat_edit_mode:
            self.update_chat_edit_mode()
        else:
            self.update_main_mode()
        self.update_chat()

    def update_chat(self):
        if chat_window.current_chat_id:
            self.update_msgs.emit(chat_window.msgs_response())
            self.update_chat_info.emit(chat_window.receive_chat_info())

    def update_chat_edit_mode(self):
        requested_username = chat_window.ui.find_user_2.text()
        if requested_username:
            self.update_user_list_while_find.emit(
                chat_window.find_users_in_chat_by_name_response(requested_username))
        else:
            self.update_user_list.emit(chat_window.users_response())

    def update_main_mode(self):
        requested_username = chat_window.ui.find_user.text()
        if requested_username:
            self.update_chat_list_while_find.emit(chat_window.receive_find_user_result(requested_username))
        else:
            self.update_chat_list.emit(chat_window.chats_response())


class ChatForm(QtWidgets.QMainWindow, chat.Ui_ChatForm):
    """Класс формы чата."""

    def __init__(self):
        super().__init__()
        self.ui = chat.Ui_ChatForm()
        self.ui.setupUi(self)

        self.temp_chat_id = 0
        self.current_chat_id = 0
        self.current_chat_is_public = False

        self.current_user = ''
        self.current_user_id = 0
        self.current_user_avatar = ''
        self.current_chat_page = 1

        self.chat_edit_mode = False
        self.edit_type = 'del'

        self.block_buttons()
        self.load_buttons_icons()
        self.hide_user_menu()
        self.hide_chat_menu()
        self.set_avatars_size()

        # связки кнопок и функций
        self.ui.log_out.clicked.connect(self.log_out)
        self.ui.menu_button.clicked.connect(self.show_user_menu)
        self.ui.menu_button_2.clicked.connect(self.hide_user_menu)
        self.ui.chat_settings.clicked.connect(self.open_chat_editor)
        self.ui.add_or_delete_button.clicked.connect(self.change_edit_type)
        self.ui.message_text.textChanged.connect(self.is_need_to_send)

        # поиск пользователя по каждому введенному символу
        self.ui.find_user.textChanged.connect(self.find_user)
        self.ui.find_user_2.textChanged.connect(self.find_user_in_chat_editor)

        self.ui.send_message.clicked.connect(self.send_message)

        # связка списка чатов с функцией
        self.ui.chats.itemClicked.connect(self.chat_clicked)
        self.ui.messages.itemClicked.connect(self.load_more_msgs)

        # создание потока обновления данных
        self.thread = QThread()
        self.worker = ChatWorker()
        self.worker.moveToThread(self.thread)
        # соединение сигналов и слотов
        self.thread.started.connect(self.worker.update_client_thread)
        self.worker.update_chat_list.connect(self.view_chats)
        self.worker.update_user_list.connect(self.view_users)
        self.worker.update_msgs.connect(self.view_msgs)
        self.worker.update_chat_list_while_find.connect(self.view_find_user_result)
        self.worker.update_user_list_while_find.connect(self.view_users)
        self.worker.update_chat_info.connect(self.view_dict_chat_info)

        self.thread.start()

    def is_need_to_send(self):
        msg_text = self.ui.message_text.toPlainText()
        if msg_text:
            if msg_text[-1] == '\n':
                self.ui.message_text.clear()
                self.ui.message_text.insertPlainText(msg_text[:-1])
                self.send_message()

    def load_more_msgs(self, chat):
        """Загрузка большего количества сообщений."""
        item_index = self.ui.messages.indexFromItem(chat)
        if chat.chat_id == -2:
            self.current_chat_page += 1
            msgs = self.receive_msgs()
            self.view_msgs(msgs)
            self.ui.messages.scrollToItem(self.ui.messages.itemFromIndex(item_index))
        else:
            pass

    def find_user_in_chat_editor(self):
        """Поиск пользователей в режиме настройки чата."""
        requested_username = self.ui.find_user_2.text()
        if requested_username:
            users = self.find_users_in_chat_by_name(requested_username)
            self.view_users(users)
        else:
            self.view_users(self.receive_users())

    def change_edit_type(self):
        if self.edit_type == 'del':
            self.edit_type = 'add'
            self.ui.add_or_delete_button.setText('Delete users')
        else:
            self.edit_type = 'del'
            self.ui.add_or_delete_button.setText('Add users')
        self.ui.find_user_2.setText('')
        self.view_users(self.receive_users())

    def open_chat_editor(self):
        """Открывает и закрывает окно редактирования чата."""
        if self.chat_edit_mode:
            self.chat_edit_mode = False
            self.ui.chats.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            self.ui.chats.itemClicked.connect(self.chat_clicked)
            self.hide_chat_menu()
            self.view_chats(self.receive_chats())
        else:
            self.chat_edit_mode = True
            self.ui.chats.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
            self.ui.chats.itemClicked.disconnect()
            self.show_chat_menu()
            self.view_users(self.receive_users())

    def add_user_to_chat(self, user_id):
        """Добавление пользователя в чат."""
        self.ui.connection_error.clear()
        try:
            response = requests.post(f'http://{SERVER}/corporate_chat/add_to_chat',
                                     data={'chat_id': self.current_chat_id,
                                           'user_id': user_id,
                                           'current_user_id': self.current_user_id})
        except:
            show_connection_error(self)
        else:
            response = response.json()
            icon_path = Path('cache', 'images', response['filename'])
            if response['new']:
                self.open_new_chat_item(icon_path, response)
            else:
                self.update_chat_info(icon_path, response)

    def update_chat_info(self, icon_path, response):
        """Обновление чата после действия."""
        self.ui.chat_name_lanel.setText(response['chat_name'])
        download_avatar(icon_path,
                        chat_id=self.current_chat_id,
                        user_id=self.current_user_id)
        self.view_users(self.receive_users())
        self.add_inf_item(text=response['msg'], to_list='msgs')

    def open_new_chat_item(self, icon_path, response):
        """Добавление нового чата в список чатов."""
        self.open_chat(chat_id=response['chat_id'],
                       chat_name=response['chat_name'],
                       is_public=response['is_public'],
                       chat_info=response['chat_info'])
        download_avatar(icon_path,
                        chat_id=response['chat_id'],
                        user_id=self.current_user_id)
        self.view_msgs(self.receive_msgs())
        self.view_users(self.receive_users())

    def remove_user_from_chat(self, user_id):
        """Удаление пользователя из чата."""
        self.ui.connection_error.clear()
        try:
            response = requests.post(f'http://{SERVER}/corporate_chat/remove_from_chat',
                                     data={'chat_id': self.current_chat_id,
                                           'user_id': user_id,
                                           'current_user_id': self.current_user_id})
        except:
            show_connection_error(self)
        else:
            response = response.json()

            if response['del_chat'] or response['leave']:
                self.delete_chat(response)
            else:
                self.update_chat_info(Path('cache', 'images', response['filename']),
                                      response)

    def delete_chat(self, response):
        """Удаление чата."""
        delete_avatar(response['filename'])
        self.open_chat_editor()
        self.block_buttons()
        self.ui.messages.clear()

    def set_avatars_size(self):
        """Установка размеров аватаров."""
        size = QSize(40, 40)
        self.ui.chats.setIconSize(size)
        self.ui.messages.setIconSize(size)

    def load_buttons_icons(self):
        """Загрузка иконок кнопок."""
        self.ui.chat_settings.setIcon(load_icon('settings.png'))
        self.ui.log_out.setIcon(load_icon('logout.png'))
        self.ui.send_message.setIcon(load_icon('send.png'))
        self.ui.menu_button.setIcon(load_icon('menu.png'))
        self.ui.menu_button_2.setIcon(load_icon('menu.png'))

    # Button block|unblock

    def block_buttons(self):
        """Блокировка кнопок."""
        self.ui.send_message.setDisabled(True)
        self.ui.chat_settings.setDisabled(True)
        self.ui.message_text.setDisabled(True)

    def unblock_buttons(self):
        """Разблокировка кнопок."""
        self.ui.send_message.setEnabled(True)
        self.ui.chat_settings.setEnabled(True)
        self.ui.message_text.setEnabled(True)

    # Work with menus part

    def hide_chat_menu(self):
        """Выключение меню."""
        self.ui.chat_menu.hide()
        self.ui.chat_menu.setDisabled(True)

    def show_chat_menu(self):
        """Показ меню."""
        self.ui.chat_menu.show()
        self.ui.chat_menu.setEnabled(True)

    def hide_user_menu(self):
        """Выключение меню."""
        self.ui.user_menu.hide()
        self.ui.user_menu.setDisabled(True)

    def show_user_menu(self):
        """Показ меню."""
        self.ui.find_user.clear()
        self.ui.user_menu.show()
        self.ui.user_menu.setEnabled(True)

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
        self.hide_user_menu()
        self.to_login_form()

    def clear_find_user(self):
        self.ui.find_user.clear()
        self.view_chats(self.receive_chats())

    # Work with user data part

    def delete_user_data(self):
        """Удаление пользовательских данных."""
        self.current_user = ''
        self.current_user_id = 0
        self.current_chat_id = 0
        self.current_user_avatar = ''
        self.temp_chat_id = 0

    def load_user_data(self, username, user_id, avatar):
        """Получает всю необходимую для работы информацию."""
        self.current_user_avatar = avatar
        self.current_user_id = user_id
        self.current_user = username

        self.view_chats(self.receive_chats())
        self.ui.username_label.setText(username)
        self.ui.avatar.setIcon(self.load_avatar(avatar, user_id))

    def load_avatar(self, filename, user_id=0, chat_id=0):
        """Загрузка изображения для аватара."""
        icon = QIcon()
        icon_path = Path('cache', 'images', filename)
        if QPixmap(str(icon_path)).isNull():
            if chat_id:
                download_avatar(icon_path=Path(Path.cwd(), 'cache', 'images', filename),
                                user_id=self.current_user_id,
                                chat_id=chat_id)
            else:
                download_avatar(icon_path=Path(Path.cwd(), 'cache', 'images', filename),
                                user_id=user_id)
        icon.addPixmap(QPixmap(str(icon_path)))
        return icon

    # Add some item part

    def add_user_item(self, username, user_id, filename, action=''):
        """Добавление нового msg_item объекта в QListWidget."""
        item = QtWidgets.QListWidgetItem(self.ui.chats)
        user = UserItemForm(username, action=action)
        if action == 'add':
            user.action_button.clicked.connect(lambda: self.add_user_to_chat(user_id))
        else:
            user.action_button.clicked.connect(lambda: self.remove_user_from_chat(user_id))

        item.setIcon(self.load_avatar(filename=filename, user_id=user_id))
        item.setSizeHint(self.chat_items_size())
        self.ui.chats.addItem(item)
        self.ui.chats.setItemWidget(item, user)

    def add_msg_item(self, msg_text, msg_time, sender, sender_name, filename):
        """Добавление нового msg_item объекта в QListWidget."""
        item = QtWidgets.QListWidgetItem(self.ui.messages)
        msg = MessageItemForm(msg_text, msg_time, sender_name)

        item.chat_id = 0

        item.setIcon(self.load_avatar(filename=filename, user_id=sender))
        item.setSizeHint(msg.sizeHint())
        self.ui.messages.addItem(item)
        self.ui.messages.setItemWidget(item, msg)
        self.ui.messages.scrollToItem(item)

    def add_inf_item(self, text, to_list):
        """Добавление нового inf_item объекта в QListWidget."""
        item = QtWidgets.QListWidgetItem()
        inf = InformationItemForm(text)
        inf.setStyleSheet(INFORMATION_ITEM_STYLE)

        item.chat_id = 0

        if to_list == 'chats':
            item.setSizeHint(QSize(320, 40))
            self.ui.chats.addItem(item)
            self.ui.chats.setItemWidget(item, inf)
        elif to_list == 'msgs':
            item.setSizeHint(QSize(320, 40))
            self.ui.messages.addItem(item)
            self.ui.messages.setItemWidget(item, inf)

    def add_more_item(self, text, to_list):
        """Добавление нового more_item объекта в QListWidget."""
        item = QtWidgets.QListWidgetItem()
        inf = InformationItemForm(text)
        inf.setStyleSheet(INFORMATION_ITEM_STYLE)

        item.chat_id = -2

        if to_list == 'chats':
            item.setSizeHint(QSize(320, 40))
            self.ui.chats.addItem(item)
            self.ui.chats.setItemWidget(item, inf)
        elif to_list == 'msgs':
            item.setSizeHint(QSize(320, 40))
            self.ui.messages.addItem(item)
            self.ui.messages.setItemWidget(item, inf)

    @staticmethod
    def chat_items_size():
        """Установка размеров аватаров."""
        return QSize(320, 55)

    def add_chat_item(self, chat_name, filename, chat_info, last_msg='', last_activity='', chat_id=None, user_id=None,
                      is_public=False):
        """Добавление нового chat_item объекта в QListWidget."""
        item = QtWidgets.QListWidgetItem(self.ui.chats)
        chat_item = ChatItemForm(chat_name, last_msg, last_activity)

        item.chat_name = chat_name

        item.user_id = user_id
        item.chat_id = chat_id
        item.is_public = is_public
        item.chat_info = chat_info

        if is_public:
            item.setIcon(self.load_avatar(filename=filename, chat_id=chat_id))
        else:
            item.setIcon(self.load_avatar(filename=filename, user_id=item.user_id))
        item.setSizeHint(self.chat_items_size())
        self.ui.chats.addItem(item)
        self.ui.chats.setItemWidget(item, chat_item)

    # Receive part

    def users_response(self):
        try:
            if self.edit_type == 'add':
                response = requests.post(f'http://{SERVER}/corporate_chat/users_not_in_chat',
                                         data={'chat_id': self.current_chat_id})
            else:
                response = requests.post(f'http://{SERVER}/corporate_chat/users_in_chat',
                                         data={'chat_id': self.current_chat_id})
        except Exception as error:
            print('Caught this error: ' + repr(error))
            raise Exception
        else:
            return response.json()['users']

    def receive_users(self):
        self.ui.connection_error.clear()
        try:
            users = self.users_response()
        except:
            show_connection_error(self)
        else:
            return users

    def msgs_response(self):
        try:
            response = requests.post(f'http://{SERVER}/corporate_chat/receive_messages',
                                     data={'chat_id': self.current_chat_id,
                                           'limit': self.current_chat_page})
        except Exception as error:
            print('Caught this error: ' + repr(error))
            raise Exception
        else:
            return response.json()['msgs']

    def receive_msgs(self):
        """Получение сообщений данного чата."""
        self.ui.connection_error.clear()
        try:
            msgs = self.msgs_response()
        except:
            show_connection_error(self)
        else:
            return msgs

    def chats_response(self):
        try:
            response = requests.post(f'http://{SERVER}/corporate_chat/receive_user_chats',
                                     data={'username': self.current_user})
        except Exception as error:
            print('Caught this error: ' + repr(error))
            raise Exception
        else:
            return (response.json())['chats']

    def receive_chats(self):
        """Получение чатов данного пользователя."""
        self.ui.connection_error.clear()
        try:
            chats = self.chats_response()
        except:
            show_connection_error(self)
        else:
            return chats

    def receive_find_user_result(self, requested_username):
        try:
            response = requests.post(f'http://{SERVER}/corporate_chat/find_user_by_name',
                                     data={'requested_username': requested_username,
                                           'current_user_id': self.current_user_id})
        except:
            show_connection_error(self)
        else:
            return response.json()

    def find_users_in_chat_by_name_response(self, requested_username):
        try:
            if self.edit_type == 'add':
                response = requests.post(f'http://{SERVER}/corporate_chat/users_not_in_chat_by_name',
                                         data={'chat_id': self.current_chat_id,
                                               'requested_username': requested_username})
            else:
                response = requests.post(f'http://{SERVER}/corporate_chat/users_in_chat_by_name',
                                         data={'chat_id': self.current_chat_id,
                                               'requested_username': requested_username})
        except Exception as error:
            print('Caught this error: ' + repr(error))
            raise Exception
        else:
            return response.json()['users']

    def find_users_in_chat_by_name(self, requested_username):
        self.ui.connection_error.clear()
        try:
            users = self.find_users_in_chat_by_name_response(requested_username)
        except:
            show_connection_error(self)
        else:
            return users

    def receive_chat_info(self):
        try:
            response = requests.post(f'http://{SERVER}/corporate_chat/receive_current_chat_info',
                                     data={'current_user_id': self.current_user_id,
                                           'chat_id': self.current_chat_id})
        except Exception as error:
            print('Caught this error: ' + repr(error))
            raise Exception
        else:
            return response.json()

    # View part

    def view_chats(self, chats):
        """Показ чатов данного пользователя."""
        self.ui.chats.clear()
        if chats:
            self.ui.no_user_label.setText('')
            for chat in chats:
                self.add_chat_item(chat_name=chat['chat_name'],
                                   last_msg=chat['last_msg'],
                                   chat_id=chat['chat_id'],
                                   filename=chat['avatar'],
                                   user_id=chat['companion_id'],
                                   last_activity=chat['last_activity'],
                                   is_public=chat['is_public'],
                                   chat_info=chat['chat_info'],
                                   )
        else:
            self.ui.no_user_label.setText('no chats yet')

    def view_msgs(self, msgs):
        """Выводит сообщения данного чата."""
        self.ui.messages.clear()
        if msgs:
            if len(msgs) == 10:
                self.add_more_item('add more messages', to_list='msgs')
            for msg in msgs:
                if msg['sender'] == -1:
                    self.add_inf_item(text=msg['msg_text'], to_list='msgs')
                else:
                    self.add_msg_item(msg_text=msg['msg_text'],
                                      msg_time=msg['send_time'],
                                      sender_name=msg['sender_name'],
                                      sender=msg['sender'],
                                      filename=msg['avatar'])
        else:
            self.ui.no_msgs_label.setText('nothing found')

    def view_users(self, users):
        self.ui.chats.clear()
        if users:
            if self.edit_type == 'add':
                self.add_inf_item('~~users not in chat~~', to_list='chats')
            else:
                self.add_inf_item('~~users in chat~~', to_list='chats')
            for user in users:
                if user['user_id'] == self.current_user_id:
                    self.add_user_item(username=user['username'],
                                       user_id=user['user_id'],
                                       filename=user['avatar'],
                                       action='leave')
                else:
                    self.add_user_item(username=user['username'],
                                       user_id=user['user_id'],
                                       filename=user['avatar'],
                                       action=self.edit_type)
        else:
            self.ui.no_user_label.setText('nothing found')

    def view_find_user_result(self, user_list):
        if len(user_list['suitable_chats']) > 0 or len(user_list['suitable_users']) > 0:
            self.ui.chats.clear()
            self.ui.no_user_label.setText('')

            if len(user_list['suitable_chats']) > 0:
                self.add_inf_item('~~chats~~', to_list='chats')
                for chat in user_list['suitable_chats']:
                    self.add_chat_item(chat_name=chat['chat_name'],
                                       last_msg=chat['last_msg'],
                                       chat_id=chat['chat_id'],
                                       filename=chat['avatar'],
                                       user_id=chat['companion_id'],
                                       last_activity=chat['last_activity'],
                                       is_public=chat['is_public'],
                                       chat_info=chat['chat_info'],
                                       )

            if len(user_list['suitable_users']) > 0:
                self.add_inf_item('~~users~~', to_list='chats')
                for user in user_list['suitable_users']:
                    self.add_chat_item(user_id=user['user_id'],
                                       chat_name=user['username'],
                                       filename=user['avatar'],
                                       chat_info=user['chat_info'],
                                       )
        else:
            self.ui.chats.clear()
            self.ui.no_user_label.setText('Nothing found')

    def no_chat_yet_view(self, chat_name, chat_info, user_id):
        self.temp_chat_id = user_id
        self.current_chat_id = 0

        self.ui.chat_name_lanel.setText(chat_name)
        self.ui.last_activite_label.setText(format_user_activity_time(get_local_time(chat_info)))
        self.clear_msgs()
        self.ui.no_msgs_label.setText('No messages yet')
        self.ui.chat_settings.setDisabled(True)

    def view_dict_chat_info(self, dict_chat_info):
        self.view_chat_info(chat_info=dict_chat_info['chat_info'],
                            is_public=dict_chat_info['is_public'])

    def view_chat_info(self, chat_info, is_public):
        if is_public:
            self.ui.last_activite_label.setText(f'{chat_info} members')
        elif chat_info == '':
            pass
        else:
            self.ui.last_activite_label.setText(format_user_activity_time(get_local_time(chat_info)))

    def send_message(self):
        """Отправка сообщения в чате."""
        msg_text = self.ui.message_text.toPlainText()
        msg_text = msg_text.strip()

        self.ui.connection_error.clear()
        if msg_text:
            if self.temp_chat_id:
                self.create_new_chat(self.temp_chat_id, self.current_user_id)
                self.temp_chat_id = 0
                self.ui.no_msgs_label.clear()
            try:
                response = requests.post(f'http://{SERVER}/corporate_chat/send_message',
                                         data={'sender': self.current_user_id, 'to_chat': self.current_chat_id,
                                               'msg': msg_text})
            except:
                show_connection_error(self)
            else:
                msg_time = response.json()['send_time']
                self.add_msg_item(msg_text=msg_text,
                                  msg_time=msg_time,
                                  sender_name=self.current_user,
                                  sender=self.current_user_id,
                                  filename=self.current_user_avatar)
                self.view_chats(self.receive_chats())
                self.ui.message_text.setFocus()
        self.ui.message_text.clear()
        self.ui.find_user.clear()

    def find_user(self):
        """Поиск пользователя по введенному значению."""
        requested_username = self.ui.find_user.text()
        self.ui.connection_error.clear()
        if requested_username:
            user_list = self.receive_find_user_result(requested_username)
            self.view_find_user_result(user_list)
        else:
            self.view_chats(self.receive_chats())

    def create_new_chat(self, *user_ids):
        """Создает новый чат."""
        self.unblock_buttons()
        self.ui.connection_error.clear()
        try:
            response = requests.post(f'http://{SERVER}/corporate_chat/start_new_chat',
                                     data={'users_ids': ','.join(str(user_id) for user_id in user_ids),
                                           'current_user_id': self.current_user_id})
        except:
            show_connection_error(self)
        else:
            chat_info = response.json()

            self.set_chat_info(chat_id=chat_info['chat_id'],
                               chat_name=chat_info['chat_name'],
                               is_public=chat_info['is_public'],
                               chat_info='')

    def clear_msgs(self):
        self.ui.messages.clear()
        self.ui.message_text.clear()

    def chat_clicked(self, chat):
        """Открытие конкретного чата."""
        if chat.chat_id is None:
            self.no_chat_yet_view(chat_name=chat.chat_name,
                                  chat_info=chat.chat_info,
                                  user_id=chat.user_id)
        elif chat.chat_id == 0 or chat.chat_id == self.current_chat_id:
            pass
        else:
            self.open_chat(chat_id=chat.chat_id,
                           chat_name=chat.chat_name,
                           is_public=chat.is_public,
                           chat_info=chat.chat_info)

    def set_chat_info(self, chat_id, chat_name, is_public, chat_info):
        self.current_chat_id = chat_id
        self.current_chat_is_public = is_public
        self.current_chat_page = 1
        self.ui.chat_name_lanel.setText(chat_name)
        self.view_chat_info(chat_info, is_public)

    def open_chat(self, chat_id, chat_name, is_public, chat_info):
        self.set_chat_info(chat_id, chat_name, is_public, chat_info)
        self.unblock_buttons()
        self.view_msgs(self.receive_msgs())
        self.ui.message_text.setFocus()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    chat_window = ChatForm()
    registration_window = RegistrationForm()
    login_window = LoginForm()
    login_window.show()
    app.exec_()
