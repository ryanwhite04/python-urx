from filter import *
from sys import argv
def segmentObjects(path):
    image = cv.imread(path)
    red, mask = filterImage(image, RED)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
    cv.imshow('result', mask)
    # noise removal
    kernel = np.ones((3,3),np.uint8)
    dilated = cv.dilate(mask, kernel, iterations=4)
    eroded = cv.erode(dilated, kernel, iterations=8)
    # cv.imshow('dilated', dilated)
    # cv.imshow('eroded', eroded)
    opening = cv.morphologyEx(eroded, cv.MORPH_OPEN,kernel, iterations=5)
    cv.imshow('opened', opening)
    # sure background area
    sure_bg = cv.dilate(opening, kernel,iterations=3)
    # cv.imshow('sure_bg', sure_bg)
    # Finding sure foreground area
    dist_transform = cv.distanceTransform(opening,cv.DIST_L2,5)
    ret, sure_fg = cv.threshold(dist_transform,0.7*dist_transform.max(),255,0)
    # cv.imshow('dist_transform', dist_transform)
    # cv.imshow('sure_fg', sure_fg)
    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv.subtract(sure_bg,sure_fg)
    # cv.imshow('unknown', unknown)
    # Marker labelling
    ret, markers = cv.connectedComponents(sure_fg)
    # print(markers)
    # Add one to all labels so that sure background is not 0, but 1
    markers = markers+1
    # Now, mark the region of unknown with zero
    markers[unknown==255] = 0
    
    markers = cv.watershed(image, markers)

    cv.imshow('markers', np.array(markers, dtype=np.uint8)) 
    image[markers == -1] = [255,0,0]
    cv.imshow('camera', image)
    cv.waitKey(0)
    cv.destroyAllWindows()

segmentObjects(argv[1])
