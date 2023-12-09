import cv2
import numpy as np
from glob import glob

image_list = glob('./raw_images/*.png')

for i in range(len(image_list)):
    image = cv2.imread(image_list[i], cv2.IMREAD_GRAYSCALE)
    ret, thr = cv2.threshold(image, 60, 255, cv2.THRESH_BINARY)
    cv2.imwrite('./thr_images/{}.png'.format(i), thr)

