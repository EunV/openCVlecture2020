import cv2
import numpy as np


class ImageMerger:
    mergedImg: np.ndarray

    __previewImage: np.ndarray
    __previewWinName: str = 'preview'

    __resultImage: np.ndarray
    __resultWinName: str = 'result'

    __txtImg: np.ndarray
    __originalImg: np.ndarray
    __bg: np.ndarray

    def __generateTrackbars(self, bgImgSize: tuple, txtImgSize: tuple):
        bgHeight, bgWidth = bgImgSize
        txtHeight, txtWidth = txtImgSize
        cv2.createTrackbar('X', self.__previewWinName, 0, bgWidth - txtWidth, self.onXYchange)
        cv2.createTrackbar('Y', self.__previewWinName, 0, bgHeight - txtHeight, self.onXYchange)

    def mergeImg(self, originalImg: np.ndarray, bg: np.ndarray, txtImg: np.ndarray):
        self.__originalImg = originalImg
        self.__bg = bg.copy()
        self.__txtImg = txtImg.copy()
        y = 0
        x = 0

        # above : initialize
        # preView image 창 띄우기
        self.__previewImage = originalImg.copy()
        cv2.imshow(self.__previewWinName, self.__previewImage)
        self.__generateTrackbars(bg.shape[:2], txtImg.shape[:2])
        # preView image 창 띄우기 End

        _, mask = cv2.threshold(txtImg[:, :, 3], 1, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        height, width = txtImg.shape[:2]

        imgResult = originalImg.copy()
        txtImg = cv2.cvtColor(txtImg, cv2.COLOR_BGRA2BGR)
        roi = imgResult[y:y + height, x:x + width]
        masked_fg = cv2.bitwise_and(txtImg, txtImg, mask=mask)
        masked_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

        result = masked_fg + masked_bg
        bg[y:y + height, x:x + width] = result

        self.mergedImg = originalImg.copy()
        self.mergedImg[y:y + height, x:x + width] = result
        cv2.imshow('merged image', self.mergedImg)

    def onXYchange(self, k) -> None:
        self.__previewImage = self.__originalImg.copy()
        txtImg = self.__txtImg.copy()
        x = cv2.getTrackbarPos('X', self.__previewWinName)
        y = cv2.getTrackbarPos('Y', self.__previewWinName)

        _, mask = cv2.threshold(txtImg[:, :, 3], 1, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        height, width = txtImg.shape[:2]

        imgResult = self.__originalImg.copy()
        txtImg = cv2.cvtColor(txtImg, cv2.COLOR_BGRA2BGR)
        roi = imgResult[y:y + height, x:x + width]
        masked_fg = cv2.bitwise_and(txtImg, txtImg, mask=mask)
        masked_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

        result = masked_fg + masked_bg

        self.__previewImage[y:y + height, x:x + width] = result
        cv2.imshow(self.__previewWinName, self.__previewImage)

    def saveImg(self, img: np.ndarray, fName: str = 'img/done.jpg') -> None:
        cv2.imwrite(fName, img)
