from math import atan

import cv2
import numpy as np


class LineDetector:
    __grayImg: np.ndarray
    __cannyImg: np.ndarray
    __edgeCount: int = 0
    __realCount: int = 0
    __angleList: list = []
    __angleNpArr: np.ndarray

    def __init__(self):
        self.__resetVariables()

    def __resetVariables(self):
        self.__edgeCount = -1
        self.__realCount = -1
        self.__angleNpArr = None
        self.__angleList = []
        self.__angleListTheta = []
        self.__grayImg = None
        self.__cannyImg = None

    def makeLines(self, srcImg: np.ndarray, cannyLower: int, cannyUpper: int, points: int) -> tuple:
        self.__grayImg = cv2.cvtColor(srcImg, cv2.COLOR_BGR2GRAY)
        self.__cannyImg = cv2.Canny(self.__grayImg, cannyLower, cannyUpper)
        cv2.imshow('canny', self.__cannyImg)

        lines = cv2.HoughLines(self.__cannyImg, 1, np.pi / 180, points)
        # Canny 값 또는 Point 값이 적절히 설정되지 않아 직선 검출이 불가능 할 경우 종료
        if lines is None:
            print("No lines Detected! please check canny or threshold value ")
            exit(0)

        dst: np.ndarray = srcImg.copy()
        for line in lines:
            self.__edgeCount += 1
            rho, theta = line[0]

            theta_180 = theta * 180 / np.pi
            if theta_180 in self.__angleList:
                continue
            else:
                self.__realCount += 1
                self.__angleListTheta.append(atan(1 / np.tan(np.pi - theta)))
                self.__angleList.append(theta_180)

            a, b = np.cos(theta), np.sin(theta)
            x0, y0 = a * rho, b * rho

            scale = srcImg.shape[0] + srcImg.shape[1]

            x1 = int(x0 + scale * -b)
            y1 = int(y0 + scale * a)
            x2 = int(x0 - scale * -b)
            y2 = int(y0 - scale * a)

            # cv2.line(dst, (x1, y1), (x2, y2), (255, 255, 255), 1)
            cv2.line(dst, (x1, y1), (x2, y2), (0, 0, 0), 1)
            cv2.circle(dst, (x0, y0), 3, (255, 0, 0), 5, cv2.FILLED)

            # 엣지 번호를 적어놓기 위한 부분
            cv2.putText(dst, '%d' % self.__realCount,
                        ((x1 + x2 + 50) // 2, (y1 + y2 + 50) // 2),
                        cv2.FONT_ITALIC, 1.0, (0, 0, 255), 1)

            print(
                "(%02d) cotTheta(dx/dy) : %s , tanTheta(dy/dx) : %s , theta :  %s(x축 기준 :%s), 180도 중 %s | rho "
                "%f "
                % (self.__realCount, str(np.tan(np.pi - theta)), str(1 / np.tan(np.pi - theta)),
                   str(atan(1 / np.tan(np.pi - theta))),
                   str(theta),
                   str(theta * 180 / np.pi), rho)
            )
            cv2.imshow('lines', dst)
            cv2.waitKey(0)

        print('총 %d개의 에지가 검출되었습니다' % self.__edgeCount)

        self.__angleNpArr = np.array(self.__angleList)
        # 세로 일 수도 있는 선들에 대한 정보
        probablyVerticalIndex = [np.where((self.__angleNpArr > 135) | (self.__angleNpArr < 45))]
        # 세로일수도 있는 선들에 대한 정보
        probablyHorizonIndex = [np.where((self.__angleNpArr <= 135) & (self.__angleNpArr >= 45))]

        print('세로선으로 추정되는 엣지 번호들 : ', probablyVerticalIndex)
        print('가로선으로 추정되는 엣지 번호들 : ', probablyHorizonIndex)

        # self.__getIntersetctions(1.5358897, 0.017453292, 123.0, 158.0, dst2.copy())
        # cv2.imshow('lines', dst)
        return self.__angleNpArr, np.array(self.__angleListTheta)

    def __getIntersetctions(self, theta1: float, theta2: float, rho1: float, rho2: float, img: np.ndarray):
        # r = x * cos(theta) +y * sin(theta)
        x: float = ((rho1 / np.sin(theta1) - rho2 / np.sin(theta2)) / (1 / np.tan(theta1) - 1 / np.tan(theta2)))
        y: float = rho1 - np.cos(theta1) / np.sin(theta1) * x
        x = int(x + 0.5)
        y = int(y + 0.5)
        print('x좌표 교차점 : %f' % x)
        cv2.circle(img, (x, y), 5, (255, 255, 0), thickness=3)
        cv2.imshow('new', img)
