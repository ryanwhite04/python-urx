from math import pi
from requests import get
from search import search, showCamera
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
    delta = 0.2
    for color in ["RED", "GREEN", "YELLOW"]:
        sort(num, color, speed, delta, angle)

def getImage(ip, path="camera.jpg"):
    content = get(f'http://{ip}:4242/current.jpg?annotations=off').content
    array = np.asarray(bytearray(content), dtype=np.uint8)
    return cv.imdecode(array, -1)

def showImage(mask):
    cv.imshow('mask', mask)
    cv.waitKey(0)
    cv.destroyAllWindows()

def set_height(height, speed):
    r = ROBOT
    pose = r.get_pose()
    pose.pos[2] = height
    r.set_pose(pose, speed/2, speed)

def sort(num, color, speed, delta, angle):
    r = ROBOT
    j = r.getj()
    j[0] = -angle
    r.movej(j, speed, speed/2, wait=True)
    while r.getj()[0] < angle:
        found, mask = search(num, color)
        print('found', found)
        if found:
            # showImage(mask)
            # input('deposit: press enter to continue: ')
            found = False
            deposit(num, color, speed)
        else:
            j = r.getj()
            j[0] += delta
            r.movej(j, speed, speed/2, wait=True)

def moveUp(y, speed, scalar=1500):
    print('moving up by: ', y, speed, scalar)
    # j = r.getj()
    r = ROBOT

    pose = r.get_pose()
    distance = (pose.pos[0]**2+pose.pos[1]**2)**(0.5)
    pose.pos[0] *= (distance + y/scalar)/distance
    pose.pos[1] *= (distance + y/scalar)/distance
    # j[1] -= y*scalar*pi/180
    # j[2] += y*scalar*pi/180
    r.set_pose(pose, speed, speed)
    # r.movej(j)

def moveRight(x, speed, scalar=0.01):
    print('moving right by: ', x)
    r = ROBOT
    j = r.getj()
    j[0] -= x*scalar*pi/180
    r.movej(j, speed, speed/2, wait=True)

def deposit(num, color, speed, height=0.1):
    acceleration = speed / 2
    threshold = 30
    robot = ROBOT
    gripper = GRIPPER
    pose = robot.get_pose()
    if not centre(num, color, threshold, [640, 480], speed):
        return
    gripper.open_gripper()
    j = robot.getj()
    j[3] = -pi/2.1
    robot.movej(j, speed, speed/2)
    set_height(height, speed)
    gripper.close_gripper()
    robot.set_pose(pose, acceleration, speed)
    robot.set_pose(BUCKETS[color], acceleration, speed)
    gripper.open_gripper()
    robot.set_pose(pose, acceleration, speed)

def centre(num, color, threshold, dimensions, speed, counter=0):
    mask = showCamera(num, color)
    res, x, y = getCoordinates(mask)
    print('centre', res, x, y)
    # x = x * scaling factor
    # y = y * scaling factor
    # input('press enter to allow: ')
    if res == True:
        if abs(x-dimensions[0]/2) < threshold:
            if abs(y-dimensions[1]/2) < threshold:
                return 1
            else:
                moveUp(dimensions[1]/2-y, speed)
                return centre(num, color, threshold, dimensions, speed)
        else:
            moveRight(x-dimensions[0]/2, speed, 0.03)
            return centre(num, color, threshold, dimensions, speed)
    elif counter < 3:
        centre(num, color, threshold, dimensions, speed, counter+1)
    else:
        print('need to write better code')
