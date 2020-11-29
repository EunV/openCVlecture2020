import cv2
import numpy as np


class TiltShiftMaker:
    __originalImg: np.ndarray
    __resultWindowName: str = 'TiltShiftResult'
    __previewWinName: str = 'Preview'
    __previewImage: np.ndarray
    __rotateAngle: float
    __center: int = 0  # 중심 직선의 y절편
    __slope: float
    __imgSize: tuple
    __mask: np.ndarray
    __maskOriginal: np.ndarray
    __previewImageBlur: np.ndarray
    __sign: int = 1

    def __init__(self):
        self.__originalImg = cv2.imread("img/myCity.jpg")
        self.__originalImg = cv2.resize(self.__originalImg, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        self.__maskOriginal = np.zeros_like(self.__originalImg)

        self.height, self.width = self.__originalImg.shape[:2]
        self.__imgSize = self.__originalImg.shape[:2]

        print(self.__originalImg.shape)

        self.__center = self.__originalImg.shape[1] // 2
        self.__rotateAngle = np.arctan(self.width / self.height)
        self.__slope = np.tan(self.__rotateAngle)
        print(self.height, self.width, self.height / self.width, self.__rotateAngle, self.__slope)

    def __generateTrackbars(self):
        cv2.createTrackbar('Distance', self.__previewWinName, 0, 255, self.onChange)
        cv2.createTrackbar('Angle', self.__previewWinName, 1, 89, self.onChange)
        cv2.setTrackbarMin('Angle', self.__previewWinName, 1)
        cv2.createTrackbar('Center', self.__previewWinName, 0, self.__imgSize[0], self.onChange)

    def __generateTrackbars2(self):
        cv2.createTrackbar('Saturation', 'maskResult', 100, 150, self.onChange2)
        cv2.setTrackbarMin('Saturation', 'maskResult', 80)
        cv2.createTrackbar('Value', 'maskResult', 100, 150, self.onChange2)
        cv2.setTrackbarMin('Value', 'maskResult', 80)

    def onChange2(self, k):
        satGain = cv2.getTrackbarPos('Saturation', 'maskResult') / 10
        valGain = cv2.getTrackbarPos('Value', 'maskResult') / 10

    def makeTiltShift(self, original: np.ndarray):
        self.__originalImg = original

        # preview 창 띄우기
        self.__previewImage = original.copy()
        cv2.imshow(self.__previewWinName, self.__originalImg)
        self.__generateTrackbars()

        while True:
            key = cv2.waitKey(10) & 0xFF
            if key == ord('m'):  # 마스크 보여주기
                cv2.imshow('mask', self.__mask)
                mask_inv = cv2.bitwise_not(self.__mask)
                cv2.imshow('mask_inv', mask_inv)

                maskBG = cv2.bitwise_and(mask_inv, self.__previewImageBlur)
                maskResult = cv2.bitwise_and(self.__mask, self.__originalImg)
                realResult = cv2.bitwise_or(maskBG, maskResult)
                cv2.imshow('maskResult', maskResult)
                self.__generateTrackbars2()
                cv2.imshow('maskBG', maskBG)
                cv2.imshow('realResult', realResult)
            elif key == ord('c'):  # 마스크 창 닫기
                cv2.destroyWindow('mask')
            elif key == ord('q') or key == 27:  # esc 또는 q 버튼으로 프로그램 종료
                print('프로그램을 종료합니다')
                cv2.destroyAllWindows()
                exit(0)
            elif key == ord('s'):  # 이미지 저장하기
                print('test')
            elif key == ord('n'):  # negativeMode
                if self.__sign == 1:
                    self.__sign = -1
                    print('음수 모드')
                elif self.__sign == -1:
                    self.__sign = 1
                    print('양수모드')

    def onChange(self, k):
        self.__mask = self.__maskOriginal.copy()
        self.__previewImage = self.__originalImg.copy()
        self.__previewImageBlur = cv2.GaussianBlur(self.__previewImage, (11, 11), 0)
        cv2.imshow('previewBlur', self.__previewImageBlur)
        distance: int = cv2.getTrackbarPos('Distance', self.__previewWinName)
        angle: int = cv2.getTrackbarPos('Angle', self.__previewWinName)
        angle_theta: float = angle * np.pi / 180
        self.__center = cv2.getTrackbarPos('Center', self.__previewWinName)

        pts1_x = int(-self.__center / np.tan(angle_theta))
        pts1_y = int(0)
        pts2_x = int(self.width)
        pts2_y = int(self.width * np.tan(angle_theta) + self.__center)
        print(pts1_x, pts1_y, pts2_x, pts2_y)
        cv2.line(self.__previewImage, (pts1_x, pts1_y), (pts2_x, pts2_y), (255, 255, 0))  # center

        # upper Line
        pts1u_x = int(-self.__center / np.tan(angle_theta))
        pts1u_y = int(0) - distance
        pts2u_x = int(self.width)
        pts2u_y = int(self.width * np.tan(angle_theta) + self.__center) - distance
        cv2.line(self.__previewImage, (pts1u_x, pts1u_y), (pts2u_x, pts2u_y), (255, 0, 0))  # upper

        # lower Line
        pts1d_x = int(-self.__center / np.tan(angle_theta))
        pts1d_y = int(0) + distance
        pts2d_x = int(self.width)
        pts2d_y = int(self.width * np.tan(angle_theta) + self.__center) + distance
        cv2.line(self.__previewImage, (pts1d_x, pts1d_y), (pts2d_x, pts2d_y), (0, 0, 255))  # lower

        points = np.array([[pts1u_x, pts1u_y], [pts1d_x, pts1d_y], [pts2d_x, pts2d_y], [pts2u_x, pts2u_y]],
                          dtype=np.int32)
        cv2.fillPoly(self.__mask, [points], (255, 255, 255), lineType=cv2.LINE_AA)
        cv2.imshow(self.__previewWinName, self.__previewImage)


img = cv2.imread("img/myCity.jpg")
img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
tsm = TiltShiftMaker()
tsm.makeTiltShift(img)
