from math import pi
from requests import get
import urx
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper as Gripper
from sys import argv
from time import sleep
from images import *

ROBOT = False
GRIPPER = False
BUCKETS = {}

def is_running(self):
    return True

urx.URRobot.is_running = is_running

def getRobot(ip, firm=False):
    if firm:
        rob = urx.Robot(ip, use_rt=True, urFirm=5.1)
    else:
        rob = urx.Robot(ip, use_rt=True)
    rob.set_tcp((0, 0, 0.1, 0, 0, 0))
    rob.set_payload(2, (0, 0, 0.1))
    sleep(0.2)
    return rob

def set_height(height, speed):
    r = ROBOT
    pose = r.get_pose()
    pose.pos[2] = height
    r.set_pose(pose, speed/2, speed)

def moveUp(y, speed, scalar=2000):
    print('moving up by: ', y, speed, scalar)
    r = ROBOT
    pose = r.get_pose()
    distance = (pose.pos[0]**2+pose.pos[1]**2)**(0.5)
    pose.pos[0] *= (distance + y/scalar)/distance
    pose.pos[1] *= (distance + y/scalar)/distance
    r.set_pose(pose, speed, speed)

def moveRight(x, speed, scalar=0.005):
    print('moving right by: ', x)
    r = ROBOT
    j = r.getj()
    j[0] -= x*scalar*pi/180
    r.movej(j, speed, speed/2, wait=True)

def deposit(num, color, speed, height=0.1):
    acceleration = speed / 2
    threshold = 15
    robot = ROBOT
    gripper = GRIPPER
    pose = robot.get_pose()
    if not centre(num, color, threshold, [640, 480], speed):
        return
    gripper.open_gripper()
    j = robot.getj()
    j[3] = -pi/2 - 0.2
    robot.movej(j, speed, speed/2)
    moveUp(20, speed)
    set_height(height, speed)
    gripper.close_gripper()
    robot.set_pose(pose, acceleration, speed)
    robot.set_pose(BUCKETS[color], acceleration, speed)
    gripper.open_gripper()
    robot.set_pose(pose, acceleration, speed)

def getBestCircle(circles):
    circles = [c for c in circles if any(c)] 
    for i, circle in enumerate(circles):
        matching = 0
        for j in range(1, len(circles)):
            other = circles[(i+j)%len(circles)]
            x = circle[0] - other[0]
            y = circle[1] - other[1]
            r = circle[2] + other[2]
            if any(circle) and (x**2+y**2) < r**2/4:
                matching += 1
            if matching > 1:
                return circle
    return []

def centre(num, color, threshold, dimensions, speed, counter=0):
    mask = showCamera(num, color)
    circle = getBestCircle([getCoordinates(mask) for i in range(5)])
    print('circle', circle)
    # input('press enter to allow: ')
    if any(circle):
        x, y, radius = circle
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
        
def sort(num, color, speed, delta, angle):
    r = ROBOT
    while r.getj()[0] > -angle:
        found, mask = search(num, color)
        print('found', found)
        if found:
            # showImage(mask)
            # input('deposit: press enter to continue: ')
            found = False
            deposit(num, color, speed)
        else:
            j = r.getj()
            j[0] -= delta
            r.movej(j, speed, speed/2, wait=True)

def main(num, speed=0.1, firm=False):
    angle = pi/2
    delta = 0.2
    robot = getRobot(f'192.168.1.{num}', firm)
    gripper = Gripper(robot)
    buckets = {}
    global ROBOT
    global GRIPPER
    global BUCKETS
    ROBOT = robot
    GRIPPER = gripper
    BUCKETS = buckets
    start = [angle, -pi/2, -pi/2 + 0.2, -2.2, pi/2, pi]
    try:
        while True:
            color = input("Which color? [R/G/Y/Q]")
            if color == "Q":
                break
            else:
                colors = {
                    "R": "RED",
                    "Y": "YELLOW",
                    "G": "GREEN"
                }
                color = colors[color]
                input(f"Move over {color} bucket then press Enter: ")
                buckets[color] = robot.get_pose()
                robot.movej(start, speed, speed, wait=True)
                sort(num, color, speed, delta, angle)
    finally:
        robot.close()
    return robot, gripper

if __name__ == "__main__":
    main(argv[1], float(argv[2]), len(argv) > 3)
    
