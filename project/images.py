from time import sleep
from sys import argv
from requests import get
import cv2 as cv
import numpy as np

def showCamera(num, color):
    image = getImage(num)
    filtered, mask = filterImage(image, color)
    return mask

def checkForColour(mask, threshold=1000):
    columnVals = []
    for column in mask:
        count = 0
        for px in column:
            if px:
                count += 1
        columnVals.append(count)
    
    return sum(columnVals) > threshold and any(getCoordinates(mask))

def search(num, color):
    print('search', color, num)
    mask = showCamera(num, color)
    return checkForColour(mask), mask

def showImage(mask):
    cv.imshow('mask', mask)
    cv.waitKey(0)
    cv.destroyAllWindows()

def addCircles(result, mask, dp=4, minDist=100, param1=100, param2=100, minRadius=50, maxRadius=150):
    circles = cv.HoughCircles(mask, cv.HOUGH_GRADIENT,
        dp=dp, minDist=minDist,
        param1=param1, param2=param2,
        minRadius=minRadius, maxRadius=maxRadius)
    try:
        if circles.ndim == 3:
            circles = np.uint16(np.around(circles))
            for c in circles[0,:]:
                cv.circle(result, (c[0], c[1]), c[2], (255, 0, 0), 3)
    except AttributeError:
        print("err")
    return result

def getImage(num):
    print('getImage', num)
    # sleep(3)
    content = get(f'http://192.168.1.{num}:4242/current.jpg?annotations=off').content
    content = get(f'http://192.168.1.{num}:4242/current.jpg?annotations=off').content
    array = np.asarray(bytearray(content), dtype=np.uint8)
    return cv.imdecode(array, -1)

def liveFeed(num, color="GREEN"):
    print('livefeed', num, color)
    while True:
        try:
            result, mask = filterImage(getImage(num), color, 2)
            cv.imshow(f'live {color}', addCircles(result, mask))
            cv.waitKey(1)
        except KeyboardInterrupt:
            print("close")
            break

def getCoordinates(mask):
    circles = cv.HoughCircles(mask, cv.HOUGH_GRADIENT, 4, 100, minRadius=0, maxRadius=150)
    try:
        if circles.ndim == 3:
            circles = np.uint16(np.around(circles))
            return circles[0,:][0]
    except AttributeError:
        return []

def filterImage(image, color, iter=3):
    # print('filterImage', 'color', color)
    # Upper limit first, then lower limit, in HSV format
    colors = {
            "RED": (150, 179),
            "GREEN": (55, 80),
            "BLUE": (105, 135),
            "YELLOW": (33, 45)
    }
    color = colors[color]
    # Convert BGR to HSV
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    # define range of color in HSV
    lower = np.array([color[0],50,40])
    upper = np.array([color[1],255,255])

    # Threshold the HSV image to get only red colors
    mask = cv.inRange(hsv, lower, upper)
    kernel = np.ones((3,3), np.uint8)
    mask = cv.dilate(mask, kernel, iterations=iter)
    mask = cv.erode(mask, kernel, iterations=iter)
    
    # Bitwise--AND mask and the original image
    result = cv.bitwise_and(image, image, mask=mask)
    return result, mask
    
def record(num, frames, path, name):
    print('recording', num, frames, path, name)
    frame = 0
    while frame < frames:
        print('frame', frame) 
        cv.imwrite(f'{path}/{name}_{frame}.jpg', getImage(num))
        frame += 1

def main(color="GREEN", path='images/current-2.jpg'):
    cv.destroyAllWindows()
    image = cv.imread(path)
    result = filterImage(image, color)
    # cv.imshow('image', image)
    # cv.imshow('mask', mask)
    cv.imshow('res', result)
    # input("press enter to stop")
    # input('press enter to end')
    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
