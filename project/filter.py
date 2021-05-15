import cv2 as cv
import numpy as np

# Global colour ranges
# Upper limit first, then lower limit, in HSV format
BLUE = (105, 135) # HSV range for blue
GREEN = (55, 80) # HSV range for green
RED = (150, 179) # HSV range for red
YELLOW = (15, 45) # HSV range for yellow
# Current colour to look for
COLOUR = YELLOW

def filterImage(image, color, iter=3):

    # Convert BGR to HSV
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    # define range of red color in HSV
    lower = np.array([color[0],50,30])
    upper = np.array([color[1],255,255])

    # Threshold the HSV image to get only red colors
    mask = cv.inRange(hsv, lower, upper)

    kernel = np.ones((3,3), np.uint8)
    
    mask = cv.dilate(mask, kernel, iterations=iter)
    mask = cv.erode(mask, kernel, iterations=iter)
    
    # Bitwise--AND mask and the original image
    res = cv.bitwise_and(image, image, mask=mask)
    return res, mask
    
def main(color=GREEN, path='images/current-2.jpg'):
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
