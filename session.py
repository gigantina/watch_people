import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from datetime import datetime
from profile import *
import cv2
import face_recognition as fr
from func import *
from dialogs import *
import webbrowser
from hidden import Hidden_Window
from time import sleep
from random import randint
import csv
from vision import *

sys.excepthook = log_uncaught_exceptions


class BinNotFound(Exception):
    pass


class CameraThread(QThread):
    def __init__(self, id_session, id_profile, path, cam_id=0, type=0):
        super().__init__(parent=None)
        self.id_session = id_session
        self.id_profile = id_profile
        self.cam_id = cam_id
        self.type = type
        self.running = True
        self.path = path

    def run(self):
        start = datetime.now()
        print('ok')
        session = Session(self.id_session, self.id_profile)
        cap = cv2.VideoCapture(self.cam_id)

        while self.running:

            ret, img = cap.read()
            if ret:
                now = datetime.now()
                time = now.strftime('%d.%m.%y--%H-%M-%S')
                faces = fr.face_locations(img)
                for face_location in faces:
                    # Print the location of each face in this image
                    top, right, bottom, left = face_location
                    cropped = img[top:bottom, left:right]
                    file = self.path + '/' + time + '-' + str(randint(0, 100)) + '.jpg'
                    cv2.imwrite(file, cropped)
                    sleep(5)
                session.add_to_base(time, len(faces))

            else:
                break

        cap.release()
        cv2.destroyAllWindows()

    def stop(self):
        self.running = False


class Session_Window(QMainWindow):
    def __init__(self, login):
        super().__init__()
        self.login = login
        uic.loadUi('session.ui', self)  # Загружаем дизайн
        self.id_ = get_profile(self.login)[0][0]
        self.bin = ''
        self.setWindowTitle('Watch the poeople')
        self.isSession = False
        # menu
        self.action_Temp.triggered.connect(self.del_bin)
        self.action_3.triggered.connect(self.change_password_event)
        self.action_4.triggered.connect(self.change_login_event)
        self.action_Github.triggered.connect(self.github)
        self.action_csv.triggered.connect(self.csv)
        self.actionFAQ.triggered.connect(self.faq)
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
        self.bin = str(fname)

    def github(self):
        url = 'https://github.com/gigantina/yandex1'
        webbrowser.open_new(url)

    def csv(self):
        fname = QFileDialog.getSaveFileName()[0]
        data = [['session_id', 'Количество объектов в кадре', 'Время']]
        data += get_sessions_from_profile(self.id_)
        with open(fname, "w", newline="") as file:
            writer = csv.writer(file)
            for i in data:
                writer.writerow(list(i))

    def faq(self):
        pass

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
