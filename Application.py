import cv2
import numpy as np
from Camera import Camera


class Application:
    def __init__(self):
        self.print_lib_data()
        self.test_camera_init()

        while True:
            self.camera.refresh()
            self.camera1.refresh()
            self.camera2.refresh()
            if cv2.waitKey(1) == 27:  # ESC
                break

    def print_lib_data(self):
        print "OpenCV version : {0}".format(cv2.__version__)
        print "Numpy version : {0}".format(np.__version__)

    def test_camera_init(self):
        self.camera = Camera(camera_source=0, mirror=True, resize_scale=2)
        self.camera1 = Camera(camera_source=1, mirror=True, resize_scale=2)
        self.camera2 = Camera(camera_source=2, mirror=True, resize_scale=2)