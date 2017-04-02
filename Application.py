import cv2
import numpy as np
from Camera import Camera
import Events
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QFrame, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont, QImage, QPainter, QPaintEvent, QPixmap
from PyQt5.QtCore import QThread, QTimer
from threading import Thread
from Notifiers import Notifier
import traceback

cameras = []

class Application:
    def __init__(self):
        self.print_lib_data()
        self.show_trump()
        self.open_all_webcameras()
        self.app = QApplication(sys.argv)

        w = CameraWindow(cameras[0])
        w.show()

        work = WorkingThread()
        work.start()

        retval = self.app.exec_()
        print('\n'.join(repr(w) for w in self.app.allWidgets()))

        work.running = False
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


# Windows

class FaceList:
    def __init__(self, parent):
        self.layout = QVBoxLayout(parent)
        self.init_ui()
        self.face_to_widget = {}

    def init_ui(self):
        self.label = QLabel("No faces detected")
        self.layout.addWidget(self.label)
        self.spacer = QSpacerItem(1, 9999, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(self.spacer)

    def add_face(self, face):
        self.layout.removeItem(self.spacer)
        face_widget = PersonOnCameraWidget(face)
        self.face_to_widget[face] = face_widget
        self.layout.addWidget(face_widget)
        #self.label.setVisible(False)
        self.label.setText("{} faces detected:".format(len(self.face_to_widget)))
        self.layout.addItem(self.spacer)

    def remove_face(self, face):
        if self.face_to_widget.has_key(face):
            widget = self.face_to_widget.pop(face)
            widget.deleteLater()
            self.layout.removeWidget(widget)
        if len(self.face_to_widget) == 0:
            #self.label.setVisible(True)
            self.label.setText("No faces detected")

class FaceAdder:
    def __init__(self, face_list):
        self.face_list = face_list

    def do(self, event):
        if event.type == Events.TYPE_FACE_APPEARED:
            self.face_list.add_face(event.face)

class FaceRemover:
    def __init__(self, face_list):
        self.face_list = face_list

    def do(self, event):
        if event.type == Events.TYPE_FACE_LEFT_FRAME:
            self.face_list.remove_face(event.face)

class CameraWindow(QWidget):
    def __init__(self, camera):
        super(QWidget, self).__init__()
        self.camera = camera
        self.init_ui()
        self.init_notifier()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_notifier)
        self.timer.start(30)

    def init_ui(self):
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(8)

        self.camera_container = QWidget()
        self.camera_widget = CameraImageWidget(self.camera_container, self.camera)
        self.layout.addWidget(self.camera_container)
        self.layout.addWidget(VLine())

        self.face_list_container = QWidget()
        self.face_list = FaceList(self.face_list_container)
        self.face_list_container.setMaximumWidth(256 + 2 * 8)
        self.face_list_container.setMinimumWidth(64 + 2 * 8)

        #self.face_list_layout.addWidget(HLine())

        self.layout.addWidget(self.face_list_container)

        self.setLayout(self.layout)
        self.setGeometry(300, 300, 640 + 256, 480)
        self.setWindowTitle(self.camera.__str__())

    def init_notifier(self):
        self.notifier = Notifier()
        self.notifier.subscribe(FaceAdder(self.face_list))
        self.notifier.subscribe(FaceRemover(self.face_list))
        self.camera.add_notifier(self.notifier)

    def update_notifier(self):
        self.notifier.refresh()

def HLine():
    toto = QFrame()
    toto.setFrameShape(QFrame.HLine)
    toto.setFrameShadow(QFrame.Sunken)
    return toto

def VLine():
    toto = QFrame()
    toto.setFrameShape(QFrame.VLine)
    toto.setFrameShadow(QFrame.Sunken)
    return toto

class PersonOnCameraWidget(QWidget):
    def __init__(self, face):
        super(QWidget, self).__init__()
        self.face = face
        self.init_ui()
        #self.setStyleSheet("border:1px solid rgb(200, 200, 200); ")

    def init_ui(self):
        self.animated_face = CameraImageWidget(None, self.face)
        self.animated_face.setMinimumWidth(64)
        self.animated_face.setMinimumHeight(64)
        self.animated_face.setMaximumWidth(64)
        self.animated_face.setMaximumHeight(64)

        self.name_label = QLabel(self.face.owner_name)#self.face.owner_name)
        self.proof_label = QLabel(str(self.face.probability) + "%")

        self.layout = QHBoxLayout(self)
        #self.layout.setSpacing(8)

        self.layout.addWidget(self.animated_face)

        self.inner_layout = QVBoxLayout(self)
        self.inner_layout.setSpacing(8)

        self.inner_layout.addWidget(self.name_label)
        self.inner_layout.addWidget(self.proof_label)

        self.layout.addLayout(self.inner_layout)

        self.setMinimumWidth(128)
        self.setMinimumHeight(64 + 8*2)
        self.setMaximumHeight(64 + 8*2)

        self.setLayout(self.layout)


class CameraImageWidget(QWidget):
    def __init__(self, parent, camera=None):
        super(QWidget, self).__init__(parent)
        self.camera = camera
        self.updating = True

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def prepare_image(self, frame):
        parent_width = self.parent().width()
        parent_height = self.parent().height()

        if parent_width < 4 or parent_height < 4:
            return QImage()

        height, width, channels = frame.shape
        bytesPerLine = width * channels

        if not frame.flags["C_CONTIGUOUS"]:
            frame = np.ascontiguousarray(frame)

        image = QImage(frame, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()

        if parent_width < 64:
            parent_width = 64
        if parent_height < 64:
            parent_height = 64

        image = QPixmap.fromImage(image).scaled(parent_width, parent_height, 1).toImage()
        self.resize(parent_width, parent_height)

        return image

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        if self.camera is not None:
            frame = self.camera.get_frame()
            image_to_be_drawn = self.prepare_image(frame)
            painter.drawImage(0, 0, image_to_be_drawn)

        painter.end()

    def update_frame(self):
        if self.updating:
            self.update()
