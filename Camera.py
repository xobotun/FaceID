import cv2
import numpy as np
from CameraHAL import CameraHAL
from FaceDetector import FaceDetector

class Camera:
	def __init__(self, cameraID=0, mirror=False):
		self.camera = CameraHAL(cameraID, mirror)
		#if not camera.is_open()
		#	pass
		self.detector = FaceDetector(self.camera)
	
	def refresh(self):
		self.camera.refresh()
		self.detector.detect_faces()
		
	def get_faces(self):
		pass