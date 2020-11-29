- 이미지 프리셋 정보
- 디렉토의 이미지에 대한 cannyLower,cannyUpper,houghLines_threshold 값
    
    
| 이미지 이름 | cannyLower | cannyUpper | houghPoint | Edges(left,top,right,bottom)|
|-----------|------------|------------|------------|-----------------------------|
|signAloneWithBG|307|693|42|(5,1,7,0)|
    
    
    - img = cv2.imread("img/signAloneWithBG.jpg")
    - img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    - for 180 :  307~693 --> Canny | Points : 42
    - edgeNum : (left,top,right,bottom) = (5 1 7 0)

    - img = cv2.imread("img/road222.jpg")
    - for 180 :  260~520 --> Canny | Points : 91

    - img = cv2.imread("img/signAlone.jpg")
    - for 180 :  630~693 --> Canny | Points : 81
    - edgeNum : (left,top,right,bottom) = (3 0 7 1)

    - img = cv2.imread("img/cargo-640.jpg")
    - for 180 : (cannyLower,cannyUpper, HoughPoints) = (300,693,81)
    - edgeNum : (left,top,right,bottom) = (5 0 5 1)

    - img = cv2.imread("img/WarningSign.jpg")
    - for 180 : (cannyLower,cannyUpper, HoughPoints) = (755,900,78)
    - edgeNum : (left,top,right,bottom) = (8,11,12,15)
    - img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

    - img = cv2.imread("img/roadSign2222.jpg")
    - for 180 : (cannyLower,cannyUpper, HoughPoints) = (800,90,100)

    - img = cv2.imread("img/roadSing_BigFlipped.jpg")
    - img = cv2.resize(img, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)
    - for 180 : (cannyLower,cannyUpper, HoughPoints) = (800,90,100)
    - edgeNum : (left,top,right,bottom) = (0,1또는2,10,5)

    - img = cv2.imread("img/stop.jpg")
    - for 180 : (cannyLower,cannyUpper, HoughPoints) = (250,500,80)
    
    -img = cv2.imread("img/board_1280.jpg")
    -img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    - for 180 : (cannyLower,cannyUpper, HoughPoints) = (250,500,80)
    - edgeNum : (left,top,right,bottom) = (7,0,3,1)