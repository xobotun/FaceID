import cv2
import numpy as np


class CameraHAL:
    def __init__(self, cameraID=0, mirror=False):
        self.cameraID = cameraID
        self.camera = cv2.VideoCapture(cameraID)
        self.mirror = mirror
        self.frame = None

    def refresh(self):
        ret_val, self.frame = self.camera.read()
        if self.mirror:
            self.frame = cv2.flip(self.frame, 1)
        cv2.imshow('tmp2', self.frame)

    def get_frame(self):
        if self.frame is None:
            self.refresh()
        return self.frame

    def is_open(self):
        return self.camera is not None
