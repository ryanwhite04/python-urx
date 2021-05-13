from requests import get
from filter import *

def getCoordinates(ip, color):
    result, mask = filterImage(cv.imread('clustered.jpg'), GREEN)
    circles = cv.HoughCircles(mask, cv.HOUGH_GRADIENT, 2.5, 100, 200)
    

def getImage(ip, path="camera.jpg"):
    content = get(f'http://{ip}:4242/current.jpg?annotations=off').content
    array = np.asarray(bytearray(content), dtype=np.uint8)
    return cv.imdecode(array, -1)

def showCamera(ip):
    path = getImage(ip)
    image = cv.imread(path)
    filtered = filterImage(image, RED)
    cv.imshow('camera', image)
    cv.imshow('red', filtered)
    cv.waitKey(0)
    cv.destroyAllWindows()

def liveFeed(ip, color=GREEN):
    while True:
        try:
            result, mask = filterImage(getImage(ip), color)
            circles = cv.HoughCircles(mask, cv.HOUGH_GRADIENT, 2.5, 100, 200)
            for c in circles[0]:
                cv.circle(result, (c[0], c[1]), 10, (255, 0, 0), 3)
            cv.imshow(f'live {color}', result)
            cv.waitKey(1)
        except Exception as e:
            print(e)
            break

