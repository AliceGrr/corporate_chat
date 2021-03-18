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
"QLabel {color:rgb(28, 94, 217,);}\n"
"QListWidget {background-color:rgb(249, 249, 249);  color:rgb(28, 94, 217); border-radius: 10px;border: 1px solid #CCCCCC;}\n"
"QPlainTextEdit {padding: 2; border-radius: 10px;border: 1px solid #CCCCCC;font: 25 14pt \"Yu Gothic UI Light\";}\n"
"")
        self.centralwidget = QtWidgets.QWidget(ChatForm)
        self.centralwidget.setObjectName("centralwidget")
        self.chats = QtWidgets.QListWidget(self.centralwidget)
        self.chats.setGeometry(QtCore.QRect(10, 70, 261, 731))
        self.chats.setIconSize(QtCore.QSize(30, 30))
        self.chats.setObjectName("chats")
        self.find_user = QtWidgets.QLineEdit(self.centralwidget)
        self.find_user.setGeometry(QtCore.QRect(10, 20, 221, 31))
        self.find_user.setStyleSheet("")
        self.find_user.setText("")
        self.find_user.setDragEnabled(False)
        self.find_user.setReadOnly(False)
        self.find_user.setClearButtonEnabled(True)
        self.find_user.setObjectName("find_user")
        self.messages = QtWidgets.QListWidget(self.centralwidget)
        self.messages.setGeometry(QtCore.QRect(280, 70, 911, 651))
        self.messages.setIconSize(QtCore.QSize(30, 30))
        self.messages.setObjectName("messages")
        self.send_message = QtWidgets.QPushButton(self.centralwidget)
        self.send_message.setGeometry(QtCore.QRect(1110, 730, 81, 71))
        self.send_message.setText("")
        self.send_message.setObjectName("send_message")
        self.message_text = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.message_text.setGeometry(QtCore.QRect(280, 730, 821, 71))
        self.message_text.setObjectName("message_text")
        self.find_user_button = QtWidgets.QPushButton(self.centralwidget)
        self.find_user_button.setGeometry(QtCore.QRect(240, 20, 31, 31))
        self.find_user_button.setText("")
        self.find_user_button.setObjectName("find_user_button")
        self.no_user_label = QtWidgets.QLabel(self.centralwidget)
        self.no_user_label.setGeometry(QtCore.QRect(60, 330, 171, 41))
        self.no_user_label.setStyleSheet("font: 25 15pt \"Yu Gothic UI Light\";")
        self.no_user_label.setText("")
        self.no_user_label.setObjectName("no_user_label")
        self.chat_name_lanel = QtWidgets.QLabel(self.centralwidget)
        self.chat_name_lanel.setGeometry(QtCore.QRect(270, 10, 281, 41))
        self.chat_name_lanel.setStyleSheet("padding: 8; font: 25 14pt \"Yu Gothic UI Light\";")
        self.chat_name_lanel.setText("")
        self.chat_name_lanel.setObjectName("chat_name_lanel")
        self.username_label = QtWidgets.QLabel(self.centralwidget)
        self.username_label.setGeometry(QtCore.QRect(990, 10, 131, 41))
        self.username_label.setStyleSheet("padding: 8; font: 25 14pt \"Yu Gothic UI Light\";")
        self.username_label.setText("")
        self.username_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.username_label.setObjectName("username_label")
        self.last_activite_label = QtWidgets.QLabel(self.centralwidget)
        self.last_activite_label.setGeometry(QtCore.QRect(274, 30, 281, 41))
        self.last_activite_label.setStyleSheet("padding: 8; font: 25 10pt \"Yu Gothic UI Light\";")
        self.last_activite_label.setText("")
        self.last_activite_label.setObjectName("last_activite_label")
        self.log_out = QtWidgets.QPushButton(self.centralwidget)
        self.log_out.setGeometry(QtCore.QRect(1130, 10, 51, 51))
        self.log_out.setText("")
        self.log_out.setIconSize(QtCore.QSize(30, 30))
        self.log_out.setObjectName("log_out")
        self.chat_settings = QtWidgets.QPushButton(self.centralwidget)
        self.chat_settings.setGeometry(QtCore.QRect(570, 10, 51, 51))
        self.chat_settings.setText("")
        self.chat_settings.setIconSize(QtCore.QSize(30, 30))
        self.chat_settings.setObjectName("chat_settings")
        self.avatar_label = QtWidgets.QLabel(self.centralwidget)
        self.avatar_label.setGeometry(QtCore.QRect(960, 10, 41, 41))
        self.avatar_label.setText("")
        self.avatar_label.setScaledContents(True)
        self.avatar_label.setObjectName("avatar_label")
        ChatForm.setCentralWidget(self.centralwidget)

        self.retranslateUi(ChatForm)
        QtCore.QMetaObject.connectSlotsByName(ChatForm)

    def retranslateUi(self, ChatForm):
        _translate = QtCore.QCoreApplication.translate
        ChatForm.setWindowTitle(_translate("ChatForm", "MainWindow"))
