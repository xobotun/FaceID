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
		pass
		#mask = cv2.inRange(hsv, lower_range, upper_range)
		
	def get_faces(self):
		pass
	
	delta_blue = [-10, 10]
	delta_green = [-10, 10]
	delta_red = [-20, 20]
	
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