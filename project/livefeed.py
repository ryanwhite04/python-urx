from sys import argv
from requests import get
from requests.models import to_key_val_list
from filter import *

def addCircles(result, mask):
    #print('ffff')

    circles = cv.HoughCircles(mask, cv.HOUGH_GRADIENT,
        4, 100,
        # param1=50, param2=30,
        minRadius=0, maxRadius=150)
    try:

        if circles.ndim == 3:
            circles = np.uint16(np.around(circles))
            print("a")
            for c in circles[0,:]:
                print(c)
                cv.circle(result, (c[0], c[1]), c[2], (255, 0, 0), 3)
    except AttributeError:
        print("err")
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
    print(ip, color)
    while True:
        try:
            result, mask = filterImage(getImage(ip), color, 2)
            cv.imshow(f'live {color}', addCircles(result, mask))
            cv.waitKey(1)
        except KeyboardInterrupt:
            print("close")
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
    ''' first arg returns true if circle found '''
    colors = {
        "GREEN": GREEN,
        "YELLOW": YELLOW,
        "RED": RED
    }
    c = colors[color]
    result, mask = filterImage(getImage(ip), color, 2)
    circles = cv.HoughCircles(mask, cv.HOUGH_GRADIENT,
        4, 100,
        # param1=50, param2=30,
        minRadius=0, maxRadius=150)

    try:
        if circles.ndim == 3:
            circles = np.uint16(np.around(circles))
            for c in circles[0,:]:
                return True, c[0], c[1] # return x and y centre of the first circle identified
            return False, False, False

    except AttributeError:
        return False, False, False



if __name__ == "__main__":
    main(*argv[1:])
