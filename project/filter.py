from time import sleep
from sys import argv
from requests import get
import cv2 as cv
import numpy as np

# Global colour ranges
def addCircles(result, mask):
    circles = cv.HoughCircles(mask, cv.HOUGH_GRADIENT,
        4, 100,
        # param1=50, param2=30,
        minRadius=0, maxRadius=150)
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

def showCamera(num, color):
    print('showCamera', num)
    path = getImage(num)
    image = cv.imread(path)
    filtered = filterImage(image, color)
    cv.imshow('camera', image)
    cv.imshow('red', filtered)
    cv.waitKey(0)
    cv.destroyAllWindows()

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

def main(num=6, color="GREEN"):
    liveFeed(num, color)

def getCoordinates(mask):
    circles = cv.HoughCircles(mask, cv.HOUGH_GRADIENT, 4, 100, minRadius=0, maxRadius=150)
    try:
        if circles.ndim == 3:
            circles = np.uint16(np.around(circles))
            for c in circles[0,:]:
                return True, c[0], c[1] # return x and y centre of the first circle identified
            return False, False, False
    except AttributeError:
        return False, False, False

def filterImage(image, color, iter=3):
    print('filterImage', 'color', color)
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
