# 2018301044 윤웅상 03번 과제
import cv2
import numpy as np

img = np.zeros((120, 120, 3), dtype=np.uint8)
img[::] = [255, 255, 255]

img[10:110, :] = [128, 0, 0]

white = (255, 255, 255)
red = (0, 0, 255)

for i in range(100):
    img[i + 10, i:i + 20] = white
    img[i + 10, i + 5:i + 15] = red
    img[109 - i, i: i + 20] = white
    img[109 - i, i + 5:i + 15] = red

img[50:70, ::] = white
img[10:110, 50:70] = white
img[10:110, 55:65] = red
img[55:65, ::] = red

cv2.imwrite("img/myUnion.jpg", img)
cv2.imshow('draw Union', img)
cv2.waitKey(0)
cv2.destroyAllWindows()