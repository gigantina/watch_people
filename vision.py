import cv2
import numpy as np
from datetime import datetime
from profile import Session
import os
from PIL import Image
import imagehash
import face_recognition as fr
import numpy as np
import imagehash


class ImageCount(Exception):
    pass


def compare_faces(img1, img2, dist=35):
    img1 = Image.open(img1)
    img2 = Image.open(img2)
    hash1 = imagehash.average_hash(img1)
    hash2 = imagehash.average_hash(img2)
    if (hash1 - hash2) > dist:
        return False
    else:
        return True


def delete_not_unique_faces(path, faces):
    files = get_photos(path)
    for i in range(len(files)):
        if not i in faces:
            file = f'{path}/{files[i]}'
            os.remove(file)


def get_photos(path):
    return os.listdir(path)


# new_session(1, 2, 0)
def get_unique_faces(path):
    try:
        files = get_photos(path)
        faces = [0]
        for i in range(1, len(files)):
            for j in range(len(faces)):
                pos = 0
                res = compare_faces(f'{path}/{files[i]}', f'{path}/{files[j]}')
                if not res:
                    pos += 1
            if pos == len(faces):
                faces.append(i)

    except IndexError:
        raise ImageCount('Изображений слишком мало!')

    return faces


# new_session(1, 1)
delete_not_unique_faces('C:/Users/User/yandex1/lop', get_unique_faces('C:/Users/User/yandex1/lop'))
