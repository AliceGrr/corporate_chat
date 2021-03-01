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
        ChatForm.resize(1200, 800)
        self.centralwidget = QtWidgets.QWidget(ChatForm)
        self.centralwidget.setObjectName("centralwidget")
        self.chats = QtWidgets.QListWidget(self.centralwidget)
        self.chats.setGeometry(QtCore.QRect(10, 50, 261, 731))
        self.chats.setObjectName("chats")
        self.find_user = QtWidgets.QLineEdit(self.centralwidget)
        self.find_user.setGeometry(QtCore.QRect(10, 10, 221, 31))
        self.find_user.setObjectName("find_user")
        self.messages = QtWidgets.QListWidget(self.centralwidget)
        self.messages.setGeometry(QtCore.QRect(280, 50, 911, 651))
        self.messages.setIconSize(QtCore.QSize(30, 30))
        self.messages.setObjectName("messages")
        self.send_message = QtWidgets.QPushButton(self.centralwidget)
        self.send_message.setGeometry(QtCore.QRect(1110, 710, 81, 71))
        self.send_message.setObjectName("send_message")
        self.message_text = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.message_text.setGeometry(QtCore.QRect(280, 710, 821, 71))
        self.message_text.setObjectName("message_text")
        self.find_user_button = QtWidgets.QPushButton(self.centralwidget)
        self.find_user_button.setGeometry(QtCore.QRect(240, 10, 31, 31))
        self.find_user_button.setText("")
        self.find_user_button.setObjectName("find_user_button")
        self.chat_name = QtWidgets.QLabel(self.centralwidget)
        self.chat_name.setGeometry(QtCore.QRect(280, 10, 331, 31))
        self.chat_name.setText("")
        self.chat_name.setObjectName("chat_name")
        self.no_user_label = QtWidgets.QLabel(self.centralwidget)
        self.no_user_label.setGeometry(QtCore.QRect(60, 330, 171, 41))
        self.no_user_label.setObjectName("no_user_label")
        ChatForm.setCentralWidget(self.centralwidget)

        self.retranslateUi(ChatForm)
        QtCore.QMetaObject.connectSlotsByName(ChatForm)

    def retranslateUi(self, ChatForm):
        _translate = QtCore.QCoreApplication.translate
        ChatForm.setWindowTitle(_translate("ChatForm", "MainWindow"))
        self.send_message.setText(_translate("ChatForm", "PushButton"))
        self.no_user_label.setText(_translate("ChatForm", "TextLabel"))
