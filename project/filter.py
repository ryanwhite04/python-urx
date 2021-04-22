import cv2 as cv
import numpy as np

def filterImage(image, color):

    # Convert BGR to HSV
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    # define range of red color in HSV
    lower_red = np.array([color-20,50,50])
    upper_red = np.array([color+20,255,255])

    # Threshold the HSV image to get only red colors
    mask = cv.inRange(hsv, lower_red, upper_red)

    # Bitwise--AND mask and the original image
    res = cv.bitwise_and(image, image, mask=mask)
    return mask, res
    
def main(path='images/current-2.jpg'):
    image = cv.imread(path)

    mask, result = filterImage(image, 180)
    # cv.imshow('image', image)
    cv.imshow('mask', mask)
    # cv.imshow('res', res)
    cv.waitKey(0)
    # input('press enter to end')
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
