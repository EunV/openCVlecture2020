import cv2
import numpy as np


def onChange(k):
    global img
    mini = cv2.getTrackbarPos('mini', 'origin')
    maxi = cv2.getTrackbarPos('maxi', 'origin')
    points = cv2.getTrackbarPos('points', 'origin')

    canny = cv2.Canny(gray, mini, maxi)
    cv2.imshow("canny", canny)

    lines = cv2.HoughLines(canny, 1, np.pi / 180, points, srn=100, stn=200, min_theta=0, max_theta=np.pi)
    dst = img.copy()
    cnt = 0
    cv2.imshow("dst", dst)
    if lines is None:
        print("lines Not found")
        exit(0)

    for i in lines:
        cnt = cnt + 1
        rho, theta = i[0][0], i[0][1]
        a, b = np.cos(theta), np.sin(theta)
        x0, y0 = a * rho, b * rho

        scale = img.shape[0] + img.shape[1]

        x1 = int(x0 + scale * -b)
        y1 = int(y0 + scale * a)
        x2 = int(x0 - scale * -b)
        y2 = int(y0 - scale * a)

        # print("번호 : %d , 기울기 :  %s , theta :  %s, 360도 중 %s" % (
        #     cnt, str(theta * 180 / np.pi), str(theta), str(theta * 180 / np.pi)))
        cv2.line(dst, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.circle(dst, (x0, y0), 3, (255, 0, 0), 5, cv2.FILLED)
        cv2.putText(dst, '%d' % mini, (100, 100), cv2.FONT_ITALIC, 1.5, (255, 0, 0))

    cv2.imshow("dst", dst)
