import cv2
import numpy as np
from CameraHAL import CameraHAL
from FaceDetector import FaceDetector
from FaceIdentifier import *
import time



class Camera:
    def __init__(self, camera_source=0, mirror=False, resize_scale=1, should_draw_faces=True):
        self.camera = CameraHAL(camera_source, mirror, resize_scale)
        if not self.camera.is_open():
            print "Camera #{} cannot be open!".format(camera_source)
        self.detector = FaceDetector(self.camera)
        self._last_fps_timestamp = self.get_milliseconds()
        self._fps_counter = 0
        self.fps = 0
        self.should_draw_faces = True
        self.excluded_persons = []

    def refresh(self):
        self.camera.refresh()
        self.detector.refresh()

        identify_faces(self.detector.faces)
        self.add_identified_persons_to_exclude_list()

        self.draw_faces()
        self.count_fps()

    def count_fps(self):
        self._fps_counter += 1
        if self.get_milliseconds() - self._last_fps_timestamp > 1000:
            self.fps = self._fps_counter
            self._fps_counter = 0
            self._last_fps_timestamp = self.get_milliseconds()
            print "Camera #{} fps is {}".format(self.camera.camera_source, self.fps)

    def add_identified_persons_to_exclude_list(self):
        self.excluded_persons = []
        for face in self.detector.faces:
            if face.identified:
                self.excluded_persons.append(face)


    def draw_faces(self):
        if self.should_draw_faces:
            for face in self.detector.faces:
                face.draw(self.camera.get_frame())

    def get_faces(self):
        pass

    def get_milliseconds(self):
        return int(round(time.time() * 1000))
