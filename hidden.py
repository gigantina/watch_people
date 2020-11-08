import sys
import traceback

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import requests
from googletrans import Translator
from profile import get_id
from func import log_uncaught_exceptions

sys.excepthook = log_uncaught_exceptions


# генерация шуток с помощью API от Чака Норриса
def generate_joke(name, surname=None):
    while True:
        try:
            if surname:
                res = requests.get(f'http://api.icndb.com/jokes/random?firstName={name}&lastName={surname}')
            else:
                res = requests.get(f'http://api.icndb.com/jokes/random?firstName={name}')
            joke = res.json()['value']['joke']
            res = translate_joke(joke)
            if '&quot' in res:
                continue
            break
        except AttributeError:
            continue
    return res


# машинный перевод шутки
def translate_joke(joke):
    translator = Translator()
    res = translator.translate(joke, src='en', dest='ru')
    return res.text


# окно режима скрытности
class Hidden_Window(QDialog):
    def __init__(self, password, parent):
        super().__init__(parent)
        uic.loadUi('hidden.ui', self)
        self.setWindowTitle('Генератор шуток')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.password = password
        self.pushButton.clicked.connect(self.run)

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Подтвердите действие', "Вы уверены, что хотите выйти",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def run(self):
        text = str(self.lineEdit.text())
        if text != self.password:
            text = text.split()
            if len(text) < 2:
                res = generate_joke(text[0])
            else:
                res = generate_joke(text[0], text[1])
            self.textBrowser.setText(res)
        else:
            self.close()
            self.parent().show()
