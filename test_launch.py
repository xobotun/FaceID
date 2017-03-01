import cv2
from Camera import Camera

camera = Camera(mirror=True)
while True:
    camera.refresh()

    if cv2.waitKey(1) == 27: # ESC
        break

