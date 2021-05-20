from requests import get
from search import search
import cv2 as cv
from filter import filterImage
from livefeed import getCoordinates
from robot import *

ROBOT = False
GRIPPER = False
BUCKETS = {}
    
def mainClean(num, robot, gripper, buckets):
    global ROBOT
    global GRIPPER
    ROBOT = robot
    GRIPPER = gripper
    BUCKETS = buckets
    clean(num)

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

def set_height(height):
    r = ROBOT
    pose = r.get_pose()
    pose.pos[2] = height
    r.set_pose(pose)

def clean(num):
    angle = pi/4
    delta = 0.1
    for color in ["red", "green", "yellow"]:
        sort(num, color, delta, angle, 0.2)
        angle *= -1
        delta *= -1

def sort(num, color, delta, angle, speed=0.1):
    r = ROBOT
    j = r.getj()
    j[0] = -angle
    r.movej(j, speed, speed/2)
    while r.getj()[0] < angle:
        found, image = search(num, color)
        while not found:
            j = r.getj()
            j[0] += delta
            r.movej(j, speed, speed/2)
            found, image = search(num, color)
        deposit(num, color, image)

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

def deposit(num, color, image, height=0.1):
    threshold = 30
    robot = ROBOT
    gripper = GRIPPER
    pose = robot.get_pose()
    centre(num, color, threshold)
    gripper.open_gripper()
    # toolDown(robot)
    set_height(height)
    gripper.close_gripper()
    robot.set_pose(pose)
    robot.set_pose(BUCKETS[color])
    gripper.open_gripper()
    robot.set_pose(pose)

def centre(num, color, threshold, dimensions):
    res, x, y = getCoordinates(color)
    # x = x * scaling factor
    # y = y * scaling factor
    if res == True:
        if abs(x-dimensions[0]) < threshold:
            if abs(y-dimensions[1]) < threshold:
                return 1
            else:
                moveUp(y-dimensions[1])
                return centre(color, threshold, dimensions)
        else:
            moveRight(x-dimensions[0])
            return centre(color, threshold, dimensions)
