import cv2


class Lock:
    def __init__(self):
        self.h = True
        self.s = True
        self.v = True


img = cv2.imread("img/myCity.jpg")
result2 = img.copy()
window_name = 'Tilt-Shift'

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lock = Lock()

# x, y, width, height = cv2.selectROI('origin', img, False)
# roi = None
# if width and height:
#     roi = img[y:y + height, x:x + width].copy()

img_height, img_width = img.shape[:2]
cv2.imshow('origin', img)
cv2.imshow(window_name, result2)


def onChange(k):
    global img, result2
    global img_height, img_width

    hue = cv2.getTrackbarPos('Hue', window_name) - 180
    sat = cv2.getTrackbarPos('Saturation', window_name) - 255
    val = cv2.getTrackbarPos('Value', window_name) - 255

    bll = cv2.getTrackbarPos('BlurLevel', window_name) * 2 - 1
    bly = cv2.getTrackbarPos('BlurY', window_name)
    blh = cv2.getTrackbarPos('BlurHeight', window_name)

    if bll > 0:
        print('yes')
        makeBlur(img[bly:bly + blh, :], bll, bly, blh)

    h, s, v = cv2.split(hsv)
    if not lock.h:
        h[:] = hue
    if not lock.s:
        s[:] = s[:] + sat
    if not lock.v:
        v[:] = v[:] + val

    hsv_result = cv2.merge((h, s, v))
    result2 = cv2.cvtColor(hsv_result, cv2.COLOR_HSV2BGR)

    cv2.imshow(window_name, result2)


cv2.createTrackbar('Hue', window_name, 180, 360, onChange)
cv2.createTrackbar('Saturation', window_name, 255, 510, onChange)
cv2.createTrackbar('Value', window_name, 255, 510, onChange)
cv2.createTrackbar('BlurLevel', window_name, 0, 90, onChange)
cv2.createTrackbar('BlurY', window_name, 20, img_height, onChange)
cv2.createTrackbar('BlurHeight', window_name, 20, 50, onChange)


def makeBlur(roi_input, bll, bly, blh):
    global img
    blurResult = img.copy()
    blurZone = cv2.GaussianBlur(roi_input, (bll, bll), 0)

    result2[bly:bly + blh, :] = blurZone[0:blh, :]
    cv2.imshow('blur Result', result2)


class KeyEventProcessor:
    def __init__(self):
        print('test')


while True:
    '''
    esc : 종료
    r   : 사진 원래대로
    h   : Hue 값 고정/해제
    s   : Sat 값 고정/해제
    v   : Val 값 고정/해제
    b   : 블러 효과
    '''
    key = cv2.waitKey(0) & 0xFF
    if key == 27:
        break

    elif key == ord('r'):
        print('사진 원래대로')

    elif key == ord('h'):
        if lock.h:
            lock.h = False
            print('잠금해제 완료')
        else:
            lock.h = True
            print('잠금 완료')

    elif key == ord('s'):
        if lock.s:
            lock.s = False
        else:
            lock.s = True

    elif key == ord('v'):
        if lock.v:
            lock.v = False
        else:
            lock.v = True

    elif key == ord('b'):
        print('대기중')

cv2.destroyAllWindows()
