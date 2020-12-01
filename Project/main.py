import cv2

from Project.ImageMerger import ImageMerger
from Project.LineDetection import LineDetector
from Project.TextImageMaker import TextImg
from Project.TiltShift import TiltShiftMaker

if __name__ == '__main__':
    textImgMaker = TextImg()
    imageMerger = ImageMerger()
    lineDetector = LineDetector()
    userSelectedEdges: list

    print('원하시는 기능을 선택하세요')
    selection = int(input('틸트-쉬프트 : 0 , 원근변환 글자 : 1 -->'))

    fName = input('img 폴더 내부에 있는 파일의 이름을 입력하세요  : ')
    folder = "img/"
    fName = folder + fName
    img = cv2.imread(fName)

    if selection == 0:
        print('Tilt-Shift 기능을 실행합니다.')
        tiltShiftMaker = TiltShiftMaker(img)
        tiltShiftMaker.makeTiltShift(img)

    elif selection == 1:
        print('원근변환 글자 기능을 실행합니다.')
        cannyLower, cannyUpper, points = list(
            map(int, (input('이미지의 cannyLower, cannyUpper, HoughLine_Points 값을 입력하세요 ')).split(' ')[:4])
        )

        text = input('원하는 글자를 입력하세요! (가능한 한 6자 이내)')
        edgeAngleList, edgeAngleList_theta = lineDetector.makeLines(img, cannyLower, cannyUpper, points)
        userSelectedEdges = list(map(int, input('사용하고자 하는 엣지의 번호를 입력해주세요.: ').split(' ')[:4]))
        textImgMaker.setThetas(edgeAngleList_theta[userSelectedEdges])
        txtImg = textImgMaker.generate(text, scale=2, thickness=2, color=(255, 255, 255, 255))
        imageMerger.mergeImg(img, img.copy(), txtImg)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
