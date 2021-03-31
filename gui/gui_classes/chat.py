# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chat.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ChatForm(object):
    def setupUi(self, ChatForm):
        ChatForm.setObjectName("ChatForm")
        ChatForm.resize(1200, 810)
        ChatForm.setMinimumSize(QtCore.QSize(1200, 810))
        ChatForm.setMaximumSize(QtCore.QSize(1200, 810))
        ChatForm.setStyleSheet("QMainWindow {background-color:rgb(249, 249, 249)}\n"
"QPushButton {background-color:rgb(249, 249, 249);  color:rgb(28, 94, 217); border-radius: 10px;border: 1px solid #CCCCCC;}\n"
"QPushButton:hover {background-color:rgb(230, 230, 230);}\n"
"QPushButton:pressed {background-color:rgb(212, 212, 212);}\n"
"QLineEdit {padding: 5; border-radius: 10px;border: 1px solid #CCCCCC;font: 25 14pt \"Yu Gothic UI Light\";}\n"
"QListWidget {background-color:rgb(249, 249, 249); padding: 2; color:rgb(28, 94, 217); border-radius: 10px;border: 1px solid #CCCCCC;}\n"
"QLabel {color: rgb(28, 94, 217);}\n"
"QPlainTextEdit {padding: 2; border-radius: 10px;border: 1px solid #CCCCCC;font: 25 14pt \"Yu Gothic UI Light\";}\n"
"")
        self.centralwidget = QtWidgets.QWidget(ChatForm)
        self.centralwidget.setObjectName("centralwidget")
        self.chats = QtWidgets.QListWidget(self.centralwidget)
        self.chats.setGeometry(QtCore.QRect(10, 70, 320, 730))
        self.chats.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.chats.setIconSize(QtCore.QSize(30, 30))
        self.chats.setObjectName("chats")
        self.find_user = QtWidgets.QLineEdit(self.centralwidget)
        self.find_user.setGeometry(QtCore.QRect(70, 10, 260, 50))
        self.find_user.setStyleSheet("")
        self.find_user.setText("")
        self.find_user.setDragEnabled(False)
        self.find_user.setReadOnly(False)
        self.find_user.setClearButtonEnabled(True)
        self.find_user.setObjectName("find_user")
        self.messages = QtWidgets.QListWidget(self.centralwidget)
        self.messages.setGeometry(QtCore.QRect(340, 70, 851, 650))
        self.messages.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.messages.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.messages.setIconSize(QtCore.QSize(30, 30))
        self.messages.setObjectName("messages")
        self.send_message = QtWidgets.QPushButton(self.centralwidget)
        self.send_message.setGeometry(QtCore.QRect(1110, 730, 80, 70))
        self.send_message.setText("")
        self.send_message.setIconSize(QtCore.QSize(40, 40))
        self.send_message.setObjectName("send_message")
        self.message_text = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.message_text.setGeometry(QtCore.QRect(339, 730, 761, 70))
        self.message_text.setStyleSheet("")
        self.message_text.setObjectName("message_text")
        self.no_user_label = QtWidgets.QLabel(self.centralwidget)
        self.no_user_label.setGeometry(QtCore.QRect(60, 330, 171, 41))
        self.no_user_label.setStyleSheet("font: 25 15pt \"Yu Gothic UI Light\";")
        self.no_user_label.setText("")
        self.no_user_label.setObjectName("no_user_label")
        self.chat_name_lanel = QtWidgets.QLabel(self.centralwidget)
        self.chat_name_lanel.setGeometry(QtCore.QRect(340, 6, 591, 41))
        self.chat_name_lanel.setStyleSheet("font: 63 14pt \"Yu Gothic UI Semibold\";")
        self.chat_name_lanel.setText("")
        self.chat_name_lanel.setObjectName("chat_name_lanel")
        self.last_activite_label = QtWidgets.QLabel(self.centralwidget)
        self.last_activite_label.setGeometry(QtCore.QRect(341, 30, 601, 41))
        self.last_activite_label.setStyleSheet("font: 10pt \"Yu Gothic UI Semilight\";")
        self.last_activite_label.setText("")
        self.last_activite_label.setObjectName("last_activite_label")
        self.chat_settings = QtWidgets.QPushButton(self.centralwidget)
        self.chat_settings.setGeometry(QtCore.QRect(1140, 10, 50, 50))
        self.chat_settings.setText("")
        self.chat_settings.setIconSize(QtCore.QSize(30, 30))
        self.chat_settings.setObjectName("chat_settings")
        self.menu_button = QtWidgets.QPushButton(self.centralwidget)
        self.menu_button.setGeometry(QtCore.QRect(10, 10, 50, 50))
        self.menu_button.setText("")
        self.menu_button.setIconSize(QtCore.QSize(30, 30))
        self.menu_button.setObjectName("menu_button")
        self.user_menu = QtWidgets.QWidget(self.centralwidget)
        self.user_menu.setEnabled(True)
        self.user_menu.setGeometry(QtCore.QRect(0, 0, 330, 800))
        self.user_menu.setStyleSheet("QWidget {background-color:rgb(249, 249, 249); border-radius: 10px; border: 1px solid #CCCCCC;}")
        self.user_menu.setObjectName("user_menu")
        self.log_out = QtWidgets.QPushButton(self.user_menu)
        self.log_out.setGeometry(QtCore.QRect(10, 90, 50, 50))
        self.log_out.setStyleSheet("QPushButton {background-color:rgb(249, 249, 249);  color:rgb(28, 94, 217); border-radius: 10px;border: 1px solid #CCCCCC;}\n"
"QPushButton:hover {background-color:rgb(230, 230, 230);}\n"
"QPushButton:pressed {background-color:rgb(212, 212, 212);}")
        self.log_out.setText("")
        self.log_out.setIconSize(QtCore.QSize(30, 30))
        self.log_out.setObjectName("log_out")
        self.username_label = QtWidgets.QLabel(self.user_menu)
        self.username_label.setGeometry(QtCore.QRect(130, 10, 191, 50))
        self.username_label.setStyleSheet("font: 63 14pt \"Yu Gothic UI Semibold\"; background-color:rgb(143, 169, 255); color:rgb(249, 249, 249); border-radius: 0px; border: 0px solid #CCCCCC")
        self.username_label.setText("")
        self.username_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.username_label.setObjectName("username_label")
        self.avatar = QtWidgets.QPushButton(self.user_menu)
        self.avatar.setGeometry(QtCore.QRect(70, 10, 50, 50))
        self.avatar.setStyleSheet("")
        self.avatar.setText("")
        self.avatar.setIconSize(QtCore.QSize(40, 40))
        self.avatar.setObjectName("avatar")
        self.menu_button_2 = QtWidgets.QPushButton(self.user_menu)
        self.menu_button_2.setGeometry(QtCore.QRect(10, 10, 50, 50))
        self.menu_button_2.setStyleSheet("QPushButton {background-color:rgb(249, 249, 249);  color:rgb(28, 94, 217); border-radius: 10px;border: 1px solid #CCCCCC;}\n"
"QPushButton:hover {background-color:rgb(230, 230, 230);}\n"
"QPushButton:pressed {background-color:rgb(212, 212, 212);}")
        self.menu_button_2.setText("")
        self.menu_button_2.setIconSize(QtCore.QSize(30, 30))
        self.menu_button_2.setObjectName("menu_button_2")
        self.log_out_label = QtWidgets.QLabel(self.user_menu)
        self.log_out_label.setGeometry(QtCore.QRect(70, 90, 171, 50))
        self.log_out_label.setStyleSheet("font: 63 14pt \"Yu Gothic UI Semibold\"; border-radius: 0px; border: 0px solid #CCCCCC")
        self.log_out_label.setObjectName("log_out_label")
        self.label = QtWidgets.QLabel(self.user_menu)
        self.label.setGeometry(QtCore.QRect(0, 0, 331, 71))
        self.label.setStyleSheet("background-color:rgb(143, 169, 255);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label.raise_()
        self.log_out.raise_()
        self.username_label.raise_()
        self.avatar.raise_()
        self.menu_button_2.raise_()
        self.log_out_label.raise_()
        self.chat_menu = QtWidgets.QWidget(self.centralwidget)
        self.chat_menu.setGeometry(QtCore.QRect(10, 10, 321, 51))
        self.chat_menu.setStyleSheet("background-color:rgb(249, 249, 249)")
        self.chat_menu.setObjectName("chat_menu")
        self.add_or_delete_button = QtWidgets.QPushButton(self.chat_menu)
        self.add_or_delete_button.setGeometry(QtCore.QRect(209, 0, 110, 50))
        self.add_or_delete_button.setStyleSheet("QPushButton {font: 12pt \"Yu Gothic UI Semilight\"; background-color:rgb(249, 249, 249);  color:rgb(28, 94, 217); border-radius: 10px;border: 1px solid #CCCCCC;}\n"
"QPushButton:hover {background-color:rgb(230, 230, 230);}\n"
"QPushButton:pressed {background-color:rgb(212, 212, 212);}")
        self.add_or_delete_button.setIconSize(QtCore.QSize(30, 30))
        self.add_or_delete_button.setObjectName("add_or_delete_button")
        self.find_user_2 = QtWidgets.QLineEdit(self.chat_menu)
        self.find_user_2.setGeometry(QtCore.QRect(0, 0, 200, 50))
        self.find_user_2.setStyleSheet("")
        self.find_user_2.setText("")
        self.find_user_2.setDragEnabled(False)
        self.find_user_2.setReadOnly(False)
        self.find_user_2.setClearButtonEnabled(True)
        self.find_user_2.setObjectName("find_user_2")
        self.chat_name_lanel_2 = QtWidgets.QLabel(self.centralwidget)
        self.chat_name_lanel_2.setGeometry(QtCore.QRect(1020, 20, 112, 25))
        self.chat_name_lanel_2.setStyleSheet("font: 63 14pt \"Yu Gothic UI Semibold\";")
        self.chat_name_lanel_2.setObjectName("chat_name_lanel_2")
        self.chats.raise_()
        self.find_user.raise_()
        self.messages.raise_()
        self.send_message.raise_()
        self.message_text.raise_()
        self.no_user_label.raise_()
        self.chat_name_lanel.raise_()
        self.last_activite_label.raise_()
        self.chat_settings.raise_()
        self.menu_button.raise_()
        self.chat_menu.raise_()
        self.user_menu.raise_()
        self.chat_name_lanel_2.raise_()
        ChatForm.setCentralWidget(self.centralwidget)

        self.retranslateUi(ChatForm)
        QtCore.QMetaObject.connectSlotsByName(ChatForm)

    def retranslateUi(self, ChatForm):
        _translate = QtCore.QCoreApplication.translate
        ChatForm.setWindowTitle(_translate("ChatForm", "MainWindow"))
        self.log_out_label.setText(_translate("ChatForm", "Log out"))
        self.add_or_delete_button.setText(_translate("ChatForm", "Add users"))
        self.chat_name_lanel_2.setText(_translate("ChatForm", "Chat settings"))
