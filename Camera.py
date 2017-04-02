import cv2
import numpy as np
from CameraHAL import CameraHAL
from FaceDetector import FaceDetector
from FaceIdentifier import *
from Events import Event
import Events
import time



class Camera:
    def __init__(self, camera_source=0, mirror=False, resize_scale=1, should_draw_faces=True):
        self.camera_hal = CameraHAL(camera_source, mirror, resize_scale)
        if not self.camera_hal.is_open():
            #print "Camera #{} cannot be open!".format(camera_source)
            raise NameError("Camera #{} cannot be open!".format(camera_source))
        self.detector = FaceDetector(self.camera_hal, self)
        self._last_fps_timestamp = self.get_milliseconds()
        self._fps_counter = 0
        self.fps = 0
        self.should_draw_faces = True
        self.excluded_persons = []
        self.is_active = False
        self.notifiers = []
        self.new_faces = []
        self.faces_disappeared = []

    def __str__(self):
        if isinstance(self.camera_hal.camera_source, int):
            return "Camera #{}".format(self.camera_hal.camera_source)
        if isinstance(self.camera_hal.camera_source, str):
            return self.camera_hal.camera_source
        return "Some weird camera @{}".format(hex(id(self)))

    def refresh(self):
        self.camera_hal.refresh()
        self.detector.refresh()

        identify_faces(self.detector.faces)
        self.add_identified_persons_to_exclude_list()
        self.compare_faces_now_and_then(self.detector.faces)

        self.draw_faces()
        #self.count_fps()

    def count_fps(self):
        self._fps_counter += 1
        if self.get_milliseconds() - self._last_fps_timestamp > 1000:
            self.fps = self._fps_counter
            self._fps_counter = 0
            self._last_fps_timestamp = self.get_milliseconds()
            print "Camera #{} fps is {}".format(self.camera_hal.camera_source, self.fps)

    def add_identified_persons_to_exclude_list(self):
        self.excluded_persons = []
        for face in self.detector.faces:
            if face.identified:
                self.excluded_persons.append(face)

    def draw_faces(self):
        if self.should_draw_faces:
            for face in self.detector.faces:
                face.draw(self.camera_hal.get_frame())

    def get_faces(self):
        pass

    def get_milliseconds(self):
        return int(round(time.time() * 1000))

    def get_frame(self):
        return self.camera_hal.get_frame()

    def add_notifier(self, notifier):
        self.notifiers.append(notifier)

    def remove_notifier(self, notifier):
        self.notifiers.remove(notifier)

    def compare_faces_now_and_then(self, faces):
        for face in self.new_faces:
            for notifier in self.notifiers:
                notifier.add_event(Event(self, Events.TYPE_FACE_APPEARED, face))

        for face in self.faces_disappeared:
            for notifier in self.notifiers:
                notifier.add_event(Event(self, Events.TYPE_FACE_LEFT_FRAME, face))

        self.new_faces = []
        self.faces_disappeared = []