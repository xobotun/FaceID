import cv2
import numpy as np
import time
from CameraHAL import CameraHAL
from Face import Face


class FaceDetector:
    def __init__(self, camera, convolution_resolution=16, skin_erode_factor=2, skin_dilate_factor=10, rescan_every_nth_frame=16):
        self.camera = camera
        self.convolution_resolution = convolution_resolution
        self.skin_erode_factor = skin_erode_factor
        self.skin_dilate_factor = skin_dilate_factor
        self.previous_mask = None
        self.rescan_every_nth_frame = rescan_every_nth_frame
        self.faces = []
        self.current_frame = 0
        self.face_cascade = cv2.CascadeClassifier("E:/opencv/build/etc/haarcascades/haarcascade_frontalface_default.xml")
        self.face_tracking_margin = 32

    def should_fully_rescan(self):
        return self.current_frame % self.rescan_every_nth_frame == 0

    def detect_faces(self):
        frame = self.camera.frame
        #begin = self.get_milliseconds()
        if self.should_fully_rescan():
            frame = self.cut_non_body_color(frame)

        self.get_faces(frame)
        self.draw_faces(frame)
        #print "recognition took {} milliseconds".format(self.get_milliseconds() - begin)
        self.current_frame += 1
        return frame

    def cut_non_body_color(self, image):
        height, width, channels = image.shape
        mask = np.zeros((height, width), np.uint8)
        resolution = self.convolution_resolution # In px. Greater the lower.

        for i in np.arange(0, width, resolution):
            for j in np.arange(0, height, resolution):
                if self.check_is_within_ellipse(image[j,i]):
                    mask[j, i] = 255

       #cv2.imshow('mask', mask)

        mask = cv2.dilate(mask, np.ones((resolution, resolution), np.uint8))    # stretch points into regions.
        mask = cv2.erode(mask,  np.ones((resolution * self.skin_erode_factor + 1, resolution * self.skin_erode_factor + 1), np.uint8))    # if there are less than <self.skin_erode_factor> points nearby, remove them and contract regions into points again.
        mask = cv2.dilate(mask, np.ones((resolution * self.skin_dilate_factor + 1, resolution * self.skin_dilate_factor + 1), np.uint8))    # stretch remaining points <self.skin_dilate_factor> times.

        if self.previous_mask is None:
            self.previous_mask = mask
        full_mask = cv2.bitwise_or(mask, self.previous_mask)
        self.previous_mask = np.copy(mask)

        masked_image = cv2.bitwise_and(image, image, mask=full_mask)
        #cv2.imshow('masked_image', masked_image)
        return masked_image

    def get_faces(self, image):
        if self.should_fully_rescan():
            self.faces = []
            self.get_faces_on_image(image)
        else:
            self.filter_faces(image)

    def get_faces_on_image(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        for coordinate in faces:
            self.faces.append(Face(coordinate))

    def filter_faces(self, image):
        for face in self.faces:
            face.crop_frame(image, self.face_tracking_margin)
            gray = cv2.cvtColor(face.image, cv2.COLOR_BGR2GRAY)
            detected = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            if len(detected) != 1:
                face.should_be_deleted = True
            else:
                x, y, w, h = detected[0]
                x -= self.face_tracking_margin
                y -= self.face_tracking_margin
                old_face_coords = face.coordinates
                face.coordinates = (old_face_coords[0] + x, old_face_coords[1] + y, w, h)

    def draw_faces(self, frame):
        for face in self.faces:
            x, y, w, h = face.coordinates
            if not face.should_be_deleted:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.imshow('frame', frame)

    def check_is_within_ellipse(self, point):
        a = 149.456258494
        focus_1 = np.array([201.738200082, 224.099463072, 275.804410926])
        focus_2 = np.array([43.5045978443, 60.5293119777, 94.7957947733])
        dist_1 = np.linalg.norm(focus_1 - point)
        dist_2 = np.linalg.norm(focus_2 - point)
        return (dist_1 + dist_2) < (2 * a)

    def get_milliseconds(self):
        return int(round(time.time() * 1000))
