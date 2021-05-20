from requests import get
from filter import filterImage
import cv2 as cv
from livefeed import getImage, getCoordinates

BLUE = (105, 135) # HSV range for blue
GREEN = (55, 80) # HSV range for green
RED = (150, 179) # HSV range for red
YELLOW = (15, 45) # HSV range for yellow


# THRESHOLD
THRESH = 1000


def showCamera(num, color):
    image = getImage(num)
    filtered, mask = filterImage(image, color)
    return mask

def checkForColour(mask):
    columnVals = []
    for column in mask:
        count = 0
        for px in column:
            if px:
                count += 1
        columnVals.append(count)
    
    return sum(columnVals) > THRESH and getCoordinates(mask)[0]

def search(num, color):
    print('search', color, num)
    mask = showCamera(num, color)
    return checkForColour(mask), mask

