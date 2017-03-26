import cv2
import numpy as np
from CameraHAL import CameraHAL
from FaceDetector import FaceDetector
import time



class Camera:
    def __init__(self, camera_source=0, mirror=False):
        self.camera = CameraHAL(camera_source, mirror)
        if not self.camera.is_open():
            print "Camera #{} cannot be open!".format(camera_source)
        self.detector = FaceDetector(self.camera)
        self._last_fps_timestamp = self.get_milliseconds()
        self._fps_counter = 0
        self.fps = 0

    def refresh(self):
        self.camera.refresh()
        self.detector.detect_faces()

        self._fps_counter += 1
        if self.get_milliseconds() - self._last_fps_timestamp > 1000:
            self.fps = self._fps_counter
            self._fps_counter = 0
            self._last_fps_timestamp = self.get_milliseconds()
            print "Camera #{} fps is {}".format(self.camera.cameraID, self.fps)

    def get_faces(self):
        pass

    def get_milliseconds(self):
        return int(round(time.time() * 1000))
