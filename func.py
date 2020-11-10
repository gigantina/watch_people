import traceback
from PyQt5.QtWidgets import *
import sys, os


# показ ошибки в диалоговом окне
def show_exception(E):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)

    msg.setWindowTitle("Ошибка!")
    msg.setText("Ошибка")
    msg.setDetailedText(str(E))

    msg.addButton('Закрыть', QMessageBox.RejectRole)

    msg.exec()


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)

    text += ''.join(traceback.format_tb(tb))

    print(text)

    sys.exit()
