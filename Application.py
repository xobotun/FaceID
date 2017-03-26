import cv2
import numpy as np
from Camera import Camera


class Application:
    def __init__(self):
        self.print_lib_data()
        self.test_camera_init()

        while True:
            self.camera.refresh()
            if cv2.waitKey(1) == 27:  # ESC
                break

    def print_lib_data(self):
        print "OpenCV version : {0}".format(cv2.__version__)
        print "Numpy version : {0}".format(np.__version__)

    def test_camera_init(self):
        self.camera = Camera(camera_source="vid2.mp4", mirror=True, resize_scale=1)
