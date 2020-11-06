from datetime import datetime
import cv2
import face_recognition as fr
from PIL import Image

def run():
    start = datetime.now()
    print('ok')
    # session = Session(self.id_session, self.id_profile)
    cap = cv2.VideoCapture(0)
    now = datetime.now()
    running = True
    while running:

        ret, img = cap.read()
        if ret:
            if int((now - start).seconds) & 1 == 0:
                time = now.strftime('%d.%m.%y--%H-%M-%S')
                faces = fr.face_locations(img)
                for face_location in faces:
                    # Print the location of each face in this image
                    top, right, bottom, left = face_location
                    print(
                        "A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left,
                                                                                                              bottom,
                                                                                                              right))

                    # You can access the actual face itself like this:
                    cropped = img[top:bottom, left:right]
                    cv2.imwrite(f'temp/{time}.jpg', cropped)
                # session.add_to_base()
                # cv2.imwrite(f'C:/Users/User/yandex1/temp/{time}.jpg', cropped)
        else:
            break


run()
