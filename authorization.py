import sys

from PyQt5 import uic
from PyQt5.QtWidgets import *
import traceback
from dialogs import QRegDialog
from profile import Profile, authorization
from session import Session_Window

from func import *

sys.excepthook = log_uncaught_exceptions
# основное окно, с входом и регистрацией
class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        path = resource_path('first_window.ui')
        uic.loadUi(path, self)
        self.setFixedSize(self.size().width(), self.size().height())
        self.pushButton_2.clicked.connect(self.registrate)
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.setWindowTitle('Вход')
        self.pushButton.clicked.connect(self.authorizate)


    def authorizate(self):
        login = self.lineEdit.text()
        password = self.lineEdit_2.text()
        try:
            authorization(login, password)
            self.sw = Session_Window(login)
            self.sw.show()
            self.close()
        except Exception as E:
            show_exception(E)

    def registrate(self):
        try:
            reg = QRegDialog()
            login, password, password_ok = reg.get_res()
            profile = Profile(login, password, password_ok)
            profile.check_password()
            profile.check_login()
            profile.add_to_base()
        except TypeError:
            pass

        except Exception as E:
            show_exception(E)
