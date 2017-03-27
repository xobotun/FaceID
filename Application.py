import cv2
import numpy as np
from Camera import Camera
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton
from PyQt5.QtGui import QFont, QImage, QPainter, QPaintEvent, QPixmap
from PyQt5.QtCore import QThread, QTimer
from threading import Thread

cameras = []

class Application:
    def __init__(self):
        self.print_lib_data()
        self.show_trump()
        self.open_all_webcameras()
        self.app = QApplication(sys.argv)

        w = BasicWindow()
        w.show()

        work = WorkingThread()
        work.start()

        retval = self.app.exec_()
        print('\n'.join(repr(w) for w in self.app.allWidgets()))
        sys.exit(retval)

    def print_lib_data(self):
        print "OpenCV version : {0}".format(cv2.__version__)
        print "Numpy version : {0}".format(np.__version__)

    def show_trump(self):
        self.camera = Camera(camera_source="vid2.mp4", mirror=True, resize_scale=1)

    def open_all_webcameras(self):
        for i in range(100):
            try:
                camera = Camera(camera_source=i, mirror=True)
            except NameError:
                return
            else:
                cameras.append(camera)

class WorkingThread(QThread):
    def __init__(self):
        super(QThread, self).__init__()
        self.running = True

    def __del__(self):
        self.running = False

    def run(self):
        while self.running:
            for camera in cameras:
                camera.refresh()
                if cv2.waitKey(1) == 27:  # ESC
                    break

class BasicWindow(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.init_ui()

    def init_ui(self):
        #QToolTip.setFont(QFont('SansSerif', 10))

        #self.setToolTip('This is a <b>QWidget</b> widget')

        tmp = CameraImageWidget(self, cameras[0])

        #btn = QPushButton('Button', self)
        #btn.setToolTip('This is a <b>QPushButton</b> widget')
        #btn.resize(btn.sizeHint())
        #btn.move(0, 0)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Tooltips')

class CameraImageWidget(QWidget):
    def __init__(self, parent, camera=None):
        super(QWidget, self).__init__(parent)
        self.camera = camera
        self.updating = True

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def prepare_image(self, frame):
        height, width, channels = frame.shape
        bytesPerLine = width * channels

        image = QImage(frame, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        parent_width = self.parent().width()
        parent_height = self.parent().height()
        image = QPixmap.fromImage(image).scaled(parent_width, parent_height).toImage()

        self.resize(parent_width, parent_height)

        return image

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        if self.camera is not None:
            frame = self.camera.camera_hal.get_frame()
            image_to_be_drawn = self.prepare_image(frame)
            painter.drawImage(0, 0, image_to_be_drawn)

        painter.end()

    def update_frame(self):
        if self.updating:
            self.update()
