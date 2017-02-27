import cv2
from Camera import Camera

camera = Camera()
while True:
    camera.refresh()

    if cv2.waitKey(1) == 27: # ESC
        break

