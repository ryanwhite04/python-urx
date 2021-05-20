from math import pi
from requests import get
from search import search
import cv2 as cv
from filter import filterImage
from livefeed import getCoordinates
from robot import *

ROBOT = False
GRIPPER = False
BUCKETS = {}
    
def clean(num, robot, gripper, buckets, speed):
    global ROBOT
    global GRIPPER
    global BUCKETS
    ROBOT = robot
    GRIPPER = gripper
    BUCKETS = buckets
    angle = pi/4
    delta = 0.1
    for color in ["RED", "GREEN", "YELLOW"]:
        sort(num, color, speed, delta, angle)
        angle *= -1
        delta *= -1

def getImage(ip, path="camera.jpg"):
    content = get(f'http://{ip}:4242/current.jpg?annotations=off').content
    array = np.asarray(bytearray(content), dtype=np.uint8)
    return cv.imdecode(array, -1)

def showImage(mask):
    cv.imshow('mask', mask)
    cv.waitKey(0)
    cv.destroyAllWindows()

def showCamera(ip):
    path = getImage(ip)
    image = cv.imread(path)
    filtered = filterImage(image, RED)
    cv.imshow('camera', image)
    cv.imshow('red', filtered)
    cv.waitKey(0)
    cv.destroyAllWindows()

def set_height(height):
    r = ROBOT
    pose = r.get_pose()
    pose.pos[2] = height
    r.set_pose(pose)

def sort(num, color, speed, delta, angle):
    r = ROBOT
    j = r.getj()
    j[0] = -angle
    r.movej(j, speed, speed/2)
    while r.getj()[0] < angle:
        found, mask = search(num, color)
        print('found', found)
        if found:
            showImage(mask)
            input('deposit: press enter to continue: ')
            found = False
            deposit(num, color, speed)
        else:
            j = r.getj()
            j[0] += delta
            r.movej(j, speed, speed/2)

def moveUp(y, speed):
    r = ROBOT
    pose = r.get_pose()
    pose.pos[0] += y*0.1
    pose.pos[1] += y*0.1
    r.set_pose(pose)

def moveRight(x, speed):
    r = ROBOT
    j = r.getj()
    j[0] += x*0.1
    r.movej(j, speed, speed/2)

def deposit(num, color, speed, height=0.1):
    threshold = 30
    robot = ROBOT
    gripper = GRIPPER
    pose = robot.get_pose()
    centre(num, color, threshold, [500, 400], speed)
    gripper.open_gripper()
    set_height(height)
    gripper.close_gripper()
    robot.set_pose(pose)
    robot.set_pose(BUCKETS[color])
    gripper.open_gripper()
    robot.set_pose(pose)

def centre(num, color, threshold, dimensions, speed):
    res, x, y = getCoordinates(num, color)
    print('centre', res, x, y)
    # x = x * scaling factor
    # y = y * scaling factor
    input('press enter to allow: ')
    if res == True:
        if abs(x-dimensions[0]) < threshold:
            if abs(y-dimensions[1]) < threshold:
                return 1
            else:
                moveUp(y-dimensions[1], speed)
                return centre(num, color, threshold, dimensions, speed)
        else:
            moveRight(x-dimensions[0], speed)
            return centre(num, color, threshold, dimensions, speed)
