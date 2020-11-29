import cv2
import numpy as np


class TextImg:
    __textImage: np.ndarray
    __sizes: tuple
    __img_height: int
    __img_width: int

    __srcPoint: np.ndarray
    __dstPoint: np.ndarray

    originalWidth: int  # 이미지 확장 전 너비
    originalHeight: int  # 이미지 확장 전 높이
    expandedWidth: int  # 확장 후 너비
    expandedHeight: int  # 확장 후 너비

    leftLineAngle: float
    topLineAngle: float
    rightLineAngle: float
    bottomLineAngle: float

    def setThetas(self, edgeThetas: list):
        print('edgeThetas in Function : ', edgeThetas)
        self.leftLineAngle, self.topLineAngle, self.rightLineAngle, self.bottomLineAngle = edgeThetas

    def generate(self, text: str = '50mph', font=cv2.FONT_HERSHEY_SIMPLEX, scale=1, thickness=1,
                 color=(255, 255, 255, 255)) -> np.ndarray:
        sizes = cv2.getTextSize(text, font, scale, thickness)
        width, height = sizes[0]
        self.__img_height = height + 20
        self.__img_width = width
        self.originalHeight = height + 20
        self.originalWidth = width
        print(sizes, "텍스트 이미지 높이 %d 너비 %d" % (height, width), sep='')

        self.__srcPoint: np.ndarray = np.float32([
            [0, 0],  # 좌상단
            [0, self.originalHeight],  # 좌하단
            [self.originalWidth, 0],  # 우상단
            [self.originalWidth, self.originalHeight]  # 우하단
        ])  # [x,y]
        self.expandedWidth = self.originalWidth
        self.expandedHeight = self.originalHeight

        # generate png File
        self.__textImage = np.zeros((self.__img_height, self.__img_width, 4), dtype=np.uint8)
        # putText
        cv2.putText(self.__textImage, text, (0, self.__img_height - 10), font, scale, color=color, thickness=thickness,
                    lineType=cv2.LINE_AA)
        # for debug
        # cv2.rectangle(self.__textImage, (0, 0), (self.__img_width, self.__img_height), (255, 255, 255, 255),
        #               thickness=4, lineType=cv2.LINE_AA)
        cv2.imshow('basic Img', self.__textImage)
        return self.perspectiveProject()

    def perspectiveProject(self):

        #  for road 222
        #  가로선에 대한 정보는 없는 이미지임
        # dstPoint = np.float32([
        #     [self.originalHeight * np.tan(np.pi + (0.17453292)), 0],  # 좌상단
        #     [0, self.originalHeight],  # 좌하단
        #     [self.originalWidth - (self.originalHeight * np.tan(np.pi - 2.111848)), 0],  # 우상단
        #     [self.originalWidth, self.originalHeight]  # 우하단
        # ])

        # for signAlone.jpg
        # 네모칸이 왼쪽 위에서 오른쪽 아래로 하락하는 이미지지만, 오른쪽 가장자리가 특이한 형태( 전체적으로 사다리꼴 비스무리한 형태)
        '''
        dstPoint = np.float32([
            # np.pi/2 + theta , # -np.pi + theta
            [self.originalHeight * np.tan(np.pi / 2 + (-1.2217304865506033)),  # 3번 Edge
             0],  # 좌상단 #

            # 여기를 기준점으로 잡아 고정
            [0,
             self.originalHeight],  # 좌하단.

            # np.pi/2+ theta(단 theta 값은 음수. x축 기준 각도는 예각)
            [self.originalWidth + self.originalHeight * np.tan(np.pi / 2 + (1.239183827242579 - np.pi)),  # 7번 Edge
             self.originalWidth * np.tan(np.pi/2-1.239183827242579)],  # 우상단 7번 edge

            # np.tan(theta) 단, 예각일 때
            [self.originalWidth,
             self.originalHeight + (self.originalWidth * np.tan(0.2967060049388071))]  # 우하단 1번 Edge
        ])
        '''

        # for Cargo Image
        # 네모칸이 왼쪽 아래에서 오른쪽 위로 상승
        # edges (top,bottom,left,right) = (0,1,6,6)
        # theta 가 음수 일대 np.tan(theta)
        # dstPoint = np.float32([
        #     [0 + self.originalHeight * np.tan(np.pi / 2 + (-1.5009831572559218)),  # 여기는 쓸게 없어서 갖다 부인거니 의미는 없음
        #      0],
        #
        #     [0, self.originalHeight],  # 좌하단. 여기를 기준으로 해보기
        #
        #     [self.originalWidth + self.originalHeight * np.tan(np.pi / 2 + (-1.5009831572559218)),
        #      (self.originalWidth * np.tan(-0.2268927852299551))],  # 우상단
        #
        #     [self.originalWidth,
        #      (self.originalWidth * np.tan(-0.26179941097763576)) + self.originalHeight]  # 우하단
        # ])

        '''
            for 내리막길 주의 표지판 사진(ROAD WarningSign.jpg) Edge: 6 7 10 12 <--이게 최종임
            네모칸이 왼쪽 아래로 하락
            dstPoint = np.float32([
                # np.pi/2 + theta , # -np.pi + theta
                [self.originalHeight * np.tan(np.pi / 2 + (-1.5533430344101529)),
                 0 - self.originalWidth * np.tan(np.pi + 0.017453237375940907)],  # 좌상단 #-41도임
    
                # 여기를 기준점으로 잡아 고정
                [0, self.originalHeight],  # 좌하단.
    
                # np.pi/2+ theta(단 theta 값은 음수. x축 기준 각도는 예각)
                [self.originalWidth + self.originalHeight * np.tan(np.pi / 2 + (-1.5184364477780203)),
                 0],  # 우상단
    
                # np.tan(theta) 단, 예각일 때
                [self.originalWidth,
                 (self.originalWidth * np.tan(0.0698131759974619)) + self.originalHeight]  # 우하단
            ])
        '''

        # 모든 이미지에 대해 일반화한 버전
        dstPoint = np.float32([
            [0 + self.originalHeight * np.tan(np.pi / 2 + self.leftLineAngle),
             0],  # 좌상단
            [0, self.originalHeight],  # 좌하단. 기준점
            [self.originalWidth + self.originalHeight * np.tan(np.pi / 2 + self.rightLineAngle),
             self.originalWidth * np.tan(self.topLineAngle)],
            [self.originalWidth,
             (self.originalWidth * np.tan(self.bottomLineAngle)) + self.originalHeight],
        ])

        # 이동할 영역이 이미지 밖을 벗어나는지 확인
        minimumX, minimumY = np.min(dstPoint, axis=0)
        maximumX, maximumY = np.max(dstPoint, axis=0)

        expandLength = self.__getExpandLength((minimumX, minimumY), (maximumX, maximumY))
        # 이미지 영역을 벗어나는 목적지 좌표가 있다면 이미지를 확장 시켜준다
        if np.any(expandLength):
            expandAndMoveDone = self.__moveLittle(expandLength)
        else:
            expandAndMoveDone = self.__textImage

        matrixForPerspective = cv2.getPerspectiveTransform(self.__srcPoint, dstPoint)
        perspectiveDone = cv2.warpPerspective(expandAndMoveDone, matrixForPerspective,
                                              (self.expandedWidth, self.expandedHeight))
        cv2.imshow('perspective done!', perspectiveDone)
        cv2.waitKey(0)
        return perspectiveDone

    # 확장할 이미지의 크기에 대한 정보를 반환하는 함수
    def __getExpandLength(self, minimums: tuple, maximums: tuple) -> list:
        miniX, miniY = minimums
        maxiX, maxiY = maximums
        expandLengths = [0, 0, 0, 0]  # top,bottom,left,right

        if miniY < 0:
            expandLengths[0] = abs(miniY)
        if maxiY > self.__img_height:
            expandLengths[1] = maxiY - self.__img_height
        if miniX < 0:
            expandLengths[2] = abs(miniX)
        if maxiX > self.__img_width:
            expandLengths[3] = maxiX - self.__img_width
        return expandLengths

    def __moveLittle(self, expandInfo: list):
        top, bottom, left, right = expandInfo
        expandBottom: int = int(abs(top) + abs(bottom) + 0.5)
        expandRight: int = int(abs(left) + abs(right) + 0.5)

        # 이미지 확장하기
        expanded = cv2.copyMakeBorder(self.__textImage, 0, expandBottom, 0, expandRight,
                                      cv2.BORDER_CONSTANT,
                                      value=[0, 0, 0, 0])
        cv2.imshow('expanded', expanded)

        dx: int = int(abs(left))
        dy: int = int(abs(top))
        matrixForMove = np.float32([[1, 0, dx],
                                    [0, 1, dy]])
        expandAndMoved = cv2.warpAffine(expanded, matrixForMove,
                                        (self.originalWidth + expandRight, self.originalHeight + expandBottom), None,
                                        cv2.INTER_LINEAR)
        self.expandedHeight = self.__img_height + expandBottom
        self.expandedWidth = self.__img_width + expandRight
        cv2.imshow('moved and expand', expandAndMoved)
        return expandAndMoved
