import authorization, hidden, func, session, camthread, dialogs, profile, vision
from PyQt5.QtWidgets import *
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = authorization.Main_Window()
    ex.show()
    sys.exit(app.exec_())
