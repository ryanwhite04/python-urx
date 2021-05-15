from requests import get
from filter import filterImage
import cv2 as cv
from livefeed import getImage

BLUE = (105, 135) # HSV range for blue
GREEN = (55, 80) # HSV range for green
RED = (150, 179) # HSV range for red
YELLOW = (15, 45) # HSV range for yellow


# THRESHOLD
THRESH = 30


def showCamera(ip, colour):
    if colour == "RED":
        col = RED
    elif colour == "YELLOW":
        col = YELLOW
    else:
        col = GREEN

    path = getImage(ip)
    image = cv.imread(path)
    #image = cv.imread('images/grass.jpg')
    filtered, mask = filterImage(image, col)
    #cv.imshow('camera', image)
    #cv.imshow('red', filtered)
    #cv.waitKey(0)
    #cv.destroyAllWindows()'''
    return mask

def checkForColour(mask):
    columnVals = []
    for column in mask:
        count = 0
        for px in column:
            if px:
                count += 1
        columnVals.append(count)
    avgVal = sum(columnVals) / len(columnVals)
    return (max(columnVals) - THRESH > avgVal)



def search(colour, ipa=6):
    ip = f'192.168.1.{ipa}'
    mask = showCamera(ip, colour)
    return checkForColour(mask), mask

