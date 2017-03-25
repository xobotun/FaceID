import cv2
import numpy as np

face_id_counter = 0

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
