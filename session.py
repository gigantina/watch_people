from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from profile import *

from func import *
from dialogs import *
import webbrowser
from hidden import Hidden_Window
from camthread import CameraThread
import csv
from vision import *

sys.excepthook = log_uncaught_exceptions


class BinNotFound(Exception):
    pass


# окно с сессиями
class Session_Window(QMainWindow):
    def __init__(self, login):
        super().__init__()
        self.login = login
        path = resource_path('session.ui')
        uic.loadUi(path, self)
        self.id_ = get_profile(self.login)[0][0]
        self.bin = ''
        self.setWindowTitle('Watch the poeople')
        self.isSession = False
        # menu
        self.action_Temp.triggered.connect(self.del_bin)
        self.action_Temp.setShortcut('Ctrl+D')

        self.action_3.triggered.connect(self.change_password_event)
        self.action_3.setShortcut('Ctrl+P')

        self.action_4.triggered.connect(self.change_login_event)
        self.action_4.setShortcut('Ctrl+L')

        self.action_Github.triggered.connect(self.github)
        self.action_Github.setShortcut('Ctrl+G')

        self.action_csv.triggered.connect(self.csv)
        self.action_csv.setShortcut('Ctrl+S')

        self.actionFAQ.triggered.connect(self.faq)
        self.actionFAQ.setShortcut('Ctrl+F')
        # buttons
        self.pushButton.setEnabled(False)
        self.pushButton.clicked.connect(self.hidden_mode)
        self.pushButton_2.clicked.connect(self.run)
        self.pushButton_3.clicked.connect(self.path_bin)
        self.pushButton_4.clicked.connect(self.del_base)

        self.show_the_table()

    def del_base(self):
        del_sessions_from_id(self.id_)
        self.show_the_table()

    def show_the_table(self):
        data = [('session_id', 'Количество объектов в кадре', 'Время')]
        data += get_sessions_from_profile(self.id_)

        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount((len(data)))

        row = 0
        for tup in data:
            col = 0

            for item in tup:
                cellinfo = QTableWidgetItem(str(item))
                self.tableWidget.setItem(row, col, cellinfo)
                col += 1

            row += 1

    def hidden_mode(self):
        profile = get_profile(self.login)[0]
        self.hide()
        Info(
            f'Чтобы безопасно выйти из секретного режима, необходимо ввести свой id вместо имени и фамиилии: {self.id_}').show_message()
        self.hw = Hidden_Window(str(profile[0]), parent=self)
        self.hw.show()

    def path_bin(self):
        fname = QFileDialog.getExistingDirectory(self,
                                                 'Выберите папку для временных файлов. После окончания сессии там останутся только уникальные лица')
        self.bin = resource_path(str(fname))

    def github(self):
        url = 'https://github.com/gigantina/watch_people'
        webbrowser.open_new(url)

    def csv(self):
        fname = resource_path(QFileDialog.getSaveFileName()[0])
        data = [['session_id', 'Количество объектов в кадре', 'Время']]
        data += get_sessions_from_profile(self.id_)
        try:
            with open(fname, "w", newline="") as file:
                writer = csv.writer(file)
                for i in data:
                    writer.writerow(list(i))
        except FileNotFoundError:
            pass

    def faq(self):
        text = open('readme.txt', "r", encoding='utf-8').read()
        self.faq = Info(text).show_message()

    def run(self):
        if self.isSession:
            self.show_the_table()
            self.pushButton_2.setText('Создать новую сессию')
            self.isSession = False
            self.camThread.stop()
            delete_not_unique_faces(self.bin, get_unique_faces(self.bin))
            self.pushButton_2.setEnabled(True)
            self.pushButton.setEnabled(False)

        else:
            try:
                if self.bin == '':
                    raise BinNotFound(
                        'Путь к папке не найден! Пожалуйста, укажите его с помощью кнопки "Сменить папку назначения"!')
                else:
                    self.camThread = CameraThread(get_id(), self.id_, self.bin, 0, 0)
                    self.pushButton.setEnabled(True)
                    self.pushButton_3.setEnabled(False)
                    self.isSession = True
                    self.pushButton_2.setText('Закончить сессию')
                    self.camThread.start()

            except Exception as E:
                show_exception(E)

    def change_password_event(self):
        try:
            chg = ChangePasswordDialog()
            chg.show()
            login, password, new_password = chg.get_res()
            if login:
                change_password(login, password, new_password)
                Info('Пароль успешно изменен!').show_message()
        except TypeError:
            pass
        except Exception as E:
            show_exception(E)

    def change_login_event(self):
        try:
            chg = ChangeLoginDialog()
            chg.show()
            login, new_login, password = chg.get_res()
            if login:
                change_login(login, new_login, password)
                Info('Логин успешно изменен!').show_message()
        except TypeError:
            pass
        except Exception as E:
            show_exception(E)

    def del_bin(self):
        try:
            if self.bin == '':
                raise BinNotFound(
                    'Путь к папке не найден! Пожалуйста, укажите его с помощью кнопки "Сменить папку назначения"!')
            else:
                delete_not_unique_faces(self.bin, get_photos(self.bin))
        except Exception as E:
            show_exception(E)
