import cv2
import numpy as np

TYPE_FACE_APPEARED = "f+"
TYPE_FACE_LEFT_FRAME = "f-"

class Event:
    def __init__(self, camera, event_type, face):
        self.camera = camera
        self.type = event_type
        self.face = face