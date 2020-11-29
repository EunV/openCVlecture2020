import cv2

from Project.ImageMerger import ImageMerger
from Project.LineDetection import LineDetector
from Project.TextImageMaker import TextImg

if __name__ == '__main__':
    textImgMaker = TextImg()
    imageMerger = ImageMerger()
    lineDetector = LineDetector()
    userSelectedEdges: list

    # img = cv2.imread("img/signAloneWithBG.jpg")
    # img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    # for 180 :  307~693 --> Canny | Points : 42
    # edgeNum : (left,top,right,bottom) = (5 1 7 0)

    img = cv2.imread("img/road222.jpg")
    img = cv2.resize(img, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)

    print('원하시는 기능을 선택하세요')
    selection = int(input('틸트-쉬프트 : 0 , 원근변환 글자 : 1 -->'))

    if selection == 0:
        print('test')
    elif selection == 1:
        print('test')

    # for 180 :  260~520 --> Canny | Points : 91

    # img = cv2.imread("img/signAlone.jpg")
    # for 180 :  630~693 --> Canny | Points : 81
    # edgeNum : (left,top,right,bottom) = (3 0 7 1)

    # img = cv2.imread("img/cargo-640.jpg")
    # for 180 : (cannyLower,cannyUpper, HoughPoints) = (300,693,81)
    # edgeNum : (left,top,right,bottom) = (5 0 5 1)

    # img = cv2.imread("img/WarningSign.jpg")
    # for 180 : (cannyLower,cannyUpper, HoughPoints) = (755,900,78)
    # edgeNum : (left,top,right,bottom) = (8,11,12,15)
    # img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

    # img = cv2.imread("img/roadSign2222.jpg")
    # for 180 : (cannyLower,cannyUpper, HoughPoints) = (800,90,100)

    # img = cv2.imread("img/roadSing_BigFlipped.jpg")
    # img = cv2.resize(img, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)
    # for 180 : (cannyLower,cannyUpper, HoughPoints) = (800,90,100)
    # edgeNum : (left,top,right,bottom) = (0,1또는2,10,5)

    # img = cv2.imread("img/stop.jpg")
    # for 180 : (cannyLower,cannyUpper, HoughPoints) = (250,500,80)

    # img = cv2.imread("img/board_1280.jpg")
    # img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    # for 180 : (cannyLower,cannyUpper, HoughPoints) = (250,500,80)
    # edgeNum : (left,top,right,bottom) = (7,0,3,1)

    edgeAngleList, edgeAngleList_theta = lineDetector.makeLines(img, 260, 520, 91)

    userSelectedEdges = list(map(int, input('사용하고자 하는 엣지의 번호를 입력해주세요(가로 평행선은 -1) : ').split(' ')[:4]))
    textImgMaker.setThetas(edgeAngleList_theta[userSelectedEdges])

    txtImg = textImgMaker.generate('Busan->', scale=2, thickness=2, color=(255, 255, 255, 255))
    imageMerger.mergeImg(img, img.copy(), txtImg)

    cv2.imshow('TaDa!', txtImg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
