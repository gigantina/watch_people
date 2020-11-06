import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import *


class QRegDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('reg.ui', self)  # Загружаем дизайн
        self.setWindowTitle('Регистрация')
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.lineEdit_3.setEchoMode(QLineEdit.Password)

        # Обратите внимание: имя элемента такое же как в QTDesigner

    def get_res(self):
        if self.exec_() == QDialog.Accepted:
            login = self.lineEdit.text()
            password = self.lineEdit_2.text()
            password_new = self.lineEdit_3.text()
            return login, password, password_new
        else:
            return None


class ChangePasswordDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('change.ui', self)  # Загружаем дизайн
        self.setWindowTitle('Смена пароля')
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.lineEdit_3.setEchoMode(QLineEdit.Password)

        # Обратите внимание: имя элемента такое же как в QTDesigner

    def get_res(self):
        if self.exec_() == QDialog.Accepted:
            login = self.lineEdit.text()
            password = self.lineEdit_2.text()
            password_new = self.lineEdit_3.text()
            if login and password and password_new:
                return login, password, password_new
            else:
                return [None, None, None]
        else:
            return [None, None, None]


class ChangeLoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('change.ui', self)  # Загружаем дизайн
        self.setWindowTitle('Смена логина')
        self.label_2.setText('Новый логин')
        self.label_3.setText('Пароль')
        self.lineEdit_3.setEchoMode(QLineEdit.Password)

    def get_res(self):
        if self.exec_() == QDialog.Accepted:
            login = self.lineEdit.text()
            new_login = self.lineEdit_2.text()
            password = self.lineEdit_3.text()
            return login, new_login, password
        else:
            return None


class Info(QDialog):
    def __init__(self, information):
        super().__init__()
        uic.loadUi('info.ui', self)
        self.info = information
        self.setWindowTitle('Информация')
        self.textEdit.setText(self.info)

    def show_message(self):
        if self.exec_() == QDialog.Accepted:
            return True
        else:
            return None
