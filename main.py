import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import *
import traceback
from dialogs import QRegDialog
from profile import Profile, authorization, get_id
from session import Session_Window

from func import *

sys.excepthook = log_uncaught_exceptions


class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('first_window.ui', self)  # Загружаем дизайн
        self.pushButton_2.clicked.connect(self.registrate)
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.setWindowTitle('Вход')
        self.pushButton.clicked.connect(self.authorizate)

        # Обратите внимание: имя элемента такое же как в QTDesigner

    def authorizate(self):
        login = self.lineEdit.text()
        password = self.lineEdit_2.text()
        try:
            profile_id = authorization(login, password)
        except Exception as E:
            show_exception(E)
        self.sw = Session_Window(login)
        self.sw.show()
        self.close()

    def registrate(self):
        reg = QRegDialog()
        login, password, password_ok = reg.get_res()
        profile = Profile(login, password, password_ok)
        try:
            profile.check_password()
            profile.add_to_base()

        except Exception as E:
            show_exception(E)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main_Window()
    ex.show()
    sys.exit(app.exec_())
