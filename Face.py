import cv2
import numpy as np


class Face:
    def __init__(self, coordinates=(0,0,0,0), owner_id=0, owner_name="???"):
        self.coordinates = coordinates
        self.image = None
        self.owner_id = owner_id
        self.owner_name = owner_name
        self.should_be_deleted = False

    def crop_frame(self, frame, additional_margin=0):
        x, y, w, h = self.coordinates
        x1 = x - additional_margin
        x2 = x + w + additional_margin
        y1 = y - additional_margin
        y2 = y + h + additional_margin
        self.image = frame[y1:y2 + 1, x1:x2 + 1]
        pass
