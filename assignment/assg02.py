# 2018301044 윤웅상 02번 과제
import cv2
import numpy as np

img = cv2.imread('img/blank_500.jpg')
# img = np.zeros((500, 500, 3), dtype=np.uint8)
# img[::] = [255, 255, 255]

#직선 3개 그리기
cv2.putText(img, "Lines", (20, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
cv2.line(img, (50, 30), (150, 30), (255, 0, 0))
cv2.line(img, (200, 30), (300, 30), (0, 255, 0))
cv2.line(img, (350, 30), (450, 30), (0, 0, 255))

#직사각형 3개 그리기
cv2.putText(img, "Rectangle", (20, 80), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0))
cv2.rectangle(img, (50, 100), (100, 150), (255, 0, 0))
cv2.rectangle(img, (200, 100), (250, 150), (0, 255, 0), thickness=10)
cv2.rectangle(img, (350, 100), (400, 150), (0, 0, 255), thickness=-1)

#다각형 4개 그리기
cv2.putText(img, "PolyLine", (20, 180), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0))
#1
pts1 = np.array([[50, 200], [100, 250], [60, 250], [120, 280]] , dtype = np.int32)
cv2.polylines(img, [pts1], False, (255, 0, 0))
#2
pts2 = np.array([[200, 200], [150, 280], [250, 280]], dtype = np.int32)
cv2.polylines(img, [pts2], False, (0, 0, 0), thickness=10)
#3
pts3 = np.array([[330, 200], [280, 280], [380, 280]], dtype = np.int32)
cv2.polylines(img, [pts3], True, (0, 0, 255), thickness=10)
#4
pts4 = np.array([[425, 180], [475, 220], [450, 260], [400, 260], [375, 220]], dtype = np.int32)
cv2.polylines(img, [pts4], True, (0, 0, 0))

#타원과 원, 호 그리기
cv2.putText(img, "Circle", (20, 300), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1, (200, 100, 50))
cv2.circle(img, (50, 350), 50, (255, 0, 0)) #얇은 큰 원
cv2.circle(img, (50, 420), 40, (0, 255, 0), thickness=5) #두꺼운 중간 원
cv2.circle(img, (50, 460), 35, (0, 0, 255), thickness=-1) #채워진 작은 원

cv2.ellipse(img, (150, 350), (50, 50), 0, 0, 180, (255, 0, 0)) #아랫 반원
cv2.ellipse(img, (200, 350), (50, 50), 0, 181, 360, (0, 0, 255)) #윗 반원
cv2.ellipse(img, (325, 350), (75, 50), 0, 0, 360, (0, 255, 0)) #납작한 타원
cv2.ellipse(img, (450, 350), (50, 75), 0, 0, 360, (255, 0, 255)) #홀쭉한 타원

cv2.ellipse(img, (150, 450), (40, 50), 45, 0, 360, (0, 0, 0)) #기울어진 타원
cv2.ellipse(img, (300, 450), (40, 50), 45, 0, 180, (0, 0, 255)) #기울어진 아랫 호
cv2.ellipse(img, (350, 450), (40, 50), 45, 181, 360, (255, 0, 0)) #기울어진 윗 호

#이미지 저장하기
# cv2.imwrite('img/blank_500.jpg' , img)

#이미지 윈도우 창에서 자주 쓰이는 것들
cv2.imshow('Draw All', img)
cv2.waitKey(0)
cv2.destroyAllWindows()