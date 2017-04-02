import cv2
import numpy as np


face_id_counter = 0
font = cv2.FONT_HERSHEY_SIMPLEX

class Face:
    def __init__(self, coordinates=(0,0,0,0), owner_id=0, owner_name="???"):
        self.coordinates = coordinates
        self.image = None
        self.owner_id = owner_id
        self.owner_name = owner_name
        self.should_be_deleted = False
        global face_id_counter
        face_id_counter += 1
        self.id = face_id_counter
        self.identified = False
        self.probability = 146

    def crop_frame(self, frame, additional_margin=0):
        x, y, w, h = self.coordinates
        x1 = x - additional_margin
        x2 = x + w + additional_margin
        y1 = y - additional_margin
        y2 = y + h + additional_margin
        self.image = frame[y1:y2 + 1, x1:x2 + 1]

    def intersects_with(self, coordinates):
        x, y, w, h = self.coordinates
        x1, y1, w1, h1 = coordinates
        if (x + w < x1 or x1 + w1 < x or y + h < y1 or y1 + h1 < y):
            return False
        else:
            return True

    def draw(self, frame):
        global font
        x, y, w, h = self.coordinates
        if not self.should_be_deleted:
            # face.crop_frame(frame)
            # cv2.imshow(str(face.id), face.image)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 128, 0), 1)
            cv2.putText(frame, self.owner_name, (x, y + h), font, 0.5, (192, 64, 64), 1, cv2.LINE_AA)

            #
            #
            # face.image[:, :, 0] = cv2.equalizeHist(face.image[:, :, 0])
            # face.image[:, :, 1] = cv2.equalizeHist(face.image[:, :, 1])
            # face.image[:, :, 2] = cv2.equalizeHist(face.image[:, :, 2])

    def get_frame(self):
        return self.image
