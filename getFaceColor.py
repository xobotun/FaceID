import cv2
import numpy as np
import os
import sys


def write_raw_pixels():
    dir1 = "E:\YandexDisk\Learning\diplodoc\Code\FaceID\SkinSamples\\"
    colors = set()

    for filename in os.listdir(dir1):
        img = cv2.imread(dir1 + filename)
        height, width, channels = img.shape
        for i in range(0, height):
            for j in range(0, width):
                color = [None] * 3
                for k in range(0, channels):
                    color[k] = img[i, j][k]
                colors.add(tuple(color))

    return colors

somedata = write_raw_pixels()
file1 = open('./colors_raw.py', 'w+')
file1.write(str(somedata))
file1.close()