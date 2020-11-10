import cv2

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from datetime import datetime
from profile import *

import face_recognition as fr
from time import sleep
from random import randint
from vision import *


# поток с камерой
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
