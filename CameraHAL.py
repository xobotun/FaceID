import cv2
import numpy as np


class CameraHAL:
    def __init__(self, camera_source=0, mirror=False, resize_scale=1):
        self.camera_source = camera_source
        self.camera = cv2.VideoCapture(camera_source)
        self.mirror = mirror
        self._frame = None
        self.resize_scale = resize_scale

    def refresh(self):
        if self.camera.isOpened():
            ret_val, self._frame = self.camera.read()
            if self.mirror:
                self._frame = cv2.flip(self._frame, 1)
            if self.resize_scale != 1:
                height, width = self._frame.shape[:2]
                self._frame = cv2.resize(self._frame, (width*self.resize_scale, height*self.resize_scale), interpolation=cv2.INTER_CUBIC)

    def get_frame(self):
        if self._frame is None:
            self._frame = np.array([[[0,0,0]]], dtype=np.uint8)
        return self._frame

    def is_open(self):
        return self.camera is not None
