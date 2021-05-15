from sys import argv
from requests import get
from filter import *

def addCircles(result, mask):
    circles = cv.HoughCircles(mask, cv.HOUGH_GRADIENT, 2.5, 100, 200)
    circles = np.uint16(np.around(circles))
    for c in circles[0,:]:
        if c.size() > 1:
            cv.circle(result, (c[0], c[1]), 10, (255, 0, 0), 3)
    return result
    

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
            cv.imshow(f'live {color}', addCircles(result, mask))
            cv.waitKey(1)
        except Exception as e:
            print(e)
            break

def main(num=6, color="GREEN"):
    print(num, color)
    colors = {
        "GREEN": GREEN,
        "YELLOW": YELLOW,
        "RED": RED
    }
    liveFeed(f'192.168.1.{num}', colors[color])


def getCoordinates(color):
    colors = {
        "GREEN": GREEN,
        "YELLOW": YELLOW,
        "RED": RED
    }
    c = colors[color]
    result, mask = filterImage(getImage(ip), color)
    circles = cv.HoughCircles(mask, cv.HOUGH_GRADIENT, 2.5, 100, 200)
    circles = np.uint16(np.around(circles))
    return circles[0][0], circles[0][1] # return x and y centre of the first circle identified



if __name__ == "__main__":
    main(*argv)
