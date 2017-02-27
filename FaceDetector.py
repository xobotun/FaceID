import cv2
import numpy as np
from CameraHAL import CameraHAL

class FaceDetector:
	def __init__(self, camera):
		self.camera = camera
	
	def detect_faces(self):
		frame = self.camera.frame
		frame = self.cut_non_body_color(frame)
		return frame
	
	def cut_non_body_color(self, image):
		height, width, channels = image.shape
		mask = np.zeros((height,width), np.uint8)
		for range in FaceDetector.von_Luschan:
			lower = self.make_lower_range(range)
			upper = self.make_upper_range(range)
			mask += cv2.inRange(image, lower, upper)
		cv2.imshow('tmp', mask)
		return image
	
	def make_lower_range(self, range):
		range[0] += FaceDetector.delta_blue[0]
		range[1] += FaceDetector.delta_green[0]
		range[2] += FaceDetector.delta_red[0]
		return np.array(range, dtype = "uint8")
		
	def make_upper_range(self, range):
		range[0] += FaceDetector.delta_blue[1]
		range[1] += FaceDetector.delta_green[1]
		range[2] += FaceDetector.delta_red[1]
		return np.array(range, dtype = "uint8")
	
	def get_faces(self):
		pass
	
	delta_blue = [-20, 50]
	delta_green = [-20, 50]
	delta_red = [-30, 50]
	
	# BGR
	von_Luschan = [
		#1-9
		[245, 242, 244],
		[233, 235, 236],
		[247, 249, 250],
		[230, 251, 253],
		[230, 246, 252],
		[229, 248, 253],
		[239, 240, 250],
		[229, 234, 243],
		[234, 241, 244],
		#10-18
		[242, 253, 251],
		[235, 247, 251],
		[225, 246, 254],
		[223, 250, 254],
		[223, 250, 254],
		[195, 231, 241],
		[173, 226, 239],
		[147, 210, 224],
		[151, 226, 242],
		#19-27
		[157, 214, 235],
		[133, 217, 235],
		[103, 197, 226],
		[104, 194, 224],
		[123, 193, 223],
		[119, 184, 222],
		[100, 164, 198],
		[98,  151, 188],
		[67,  107, 156],
		#28-36
		[60,  88,  142],
		[48,  77,  121],
		[20,  49,  100],
		[32,  48,  101],
		[33,  49,  96 ],
		[41,  50,  87 ],
		[21,  32,  64 ],
		[41,  37,  49 ],
		[46,  28,  27 ],
	]