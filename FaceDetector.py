import cv2
import numpy as np
import time
from CameraHAL import CameraHAL


class FaceDetector:
    def __init__(self, camera, convolution_resolution=16, skin_erode_factor=2, skin_dilate_factor=10):
        self.camera = camera
        self.convolution_resolution = convolution_resolution
        self.skin_erode_factor = skin_erode_factor
        self.skin_dilate_factor = skin_dilate_factor
        self.previous_mask = None

    def detect_faces(self):
        frame = self.camera.frame
        begin = self.get_milliseconds()
        frame = self.cut_non_body_color(frame)
        self.get_faces(frame)
        print "recognition took {} milliseconds".format(self.get_milliseconds() - begin)
        return frame

    def cut_non_body_color(self, image):
        height, width, channels = image.shape
        mask = np.zeros((height, width), np.uint8)
        resolution = self.convolution_resolution # In px. Greater the lower.

        for i in np.arange(0, width, resolution):
            for j in np.arange(0, height, resolution):
                if self.check_is_within_ellipse(image[j,i]):
                    mask[j, i] = 255

        cv2.imshow('mask', mask)

        mask = cv2.dilate(mask, np.ones((resolution, resolution), np.uint8))    # stretch points into regions.
        mask = cv2.erode(mask,  np.ones((resolution * self.skin_erode_factor + 1, resolution * self.skin_erode_factor + 1), np.uint8))    # if there are less than <self.skin_erode_factor> points nearby, remove them and contract regions into points again.
        mask = cv2.dilate(mask, np.ones((resolution * self.skin_dilate_factor + 1, resolution * self.skin_dilate_factor + 1), np.uint8))    # stretch remaining points <self.skin_dilate_factor> times.

        if self.previous_mask is None:
            self.previous_mask = mask
        full_mask = cv2.bitwise_or(mask, self.previous_mask)
        self.previous_mask = np.copy(mask)

        masked_image = cv2.bitwise_and(image, image, mask=full_mask)
        cv2.imshow('masked_image', masked_image)
        return masked_image

    def get_faces(self, image):
        face_cascade = cv2.CascadeClassifier("E:/opencv/build/etc/haarcascades/haarcascade_frontalface_default.xml")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow('img', image)

    def check_is_within_ellipse(self, point):
        a = 149.456258494
        focus_1 = np.array([201.738200082, 224.099463072, 275.804410926])
        focus_2 = np.array([43.5045978443, 60.5293119777, 94.7957947733])
        dist_1 = np.linalg.norm(focus_1 - point)
        dist_2 = np.linalg.norm(focus_2 - point)
        return (dist_1 + dist_2) < (2 * a)

    def get_milliseconds(self):
        return int(round(time.time() * 1000))
