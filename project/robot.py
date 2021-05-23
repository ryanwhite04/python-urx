
import urx
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper as Gripper
from sys import argv
from time import sleep
from clean import *
from math import pi

def getRobot(ip):
    rob = urx.Robot(ip, use_rt=True, urFirm=5.1)
    rob.set_tcp((0, 0, 0.1, 0, 0, 0))
    rob.set_payload(2, (0, 0, 0.1))
    sleep(0.2)
    return rob

def main(num, speed=0.1):
    acceleration = speed
    ip = f'192.168.1.{num}'
    robot = getRobot(ip)
    gripper = Gripper(robot)
    buckets = {}
    start = [0, -pi/2, -pi/2, -2, pi/2, pi]
    try:
        input("Move tool over the RED bucket, then press Enter: ")
        buckets["RED"] = robot.get_pose()
        input("Move tool over the GREEN bucket, then press Enter: ")
        buckets["GREEN"] = robot.get_pose()
        input("Move tool over the YELLOW bucket, then press Enter: ")
        buckets["YELLOW"] = robot.get_pose()
        robot.movej(start, vel=speed, acc=acceleration, wait=True)
        clean(num, robot, gripper, buckets, speed)
    # except Exception as e:
    #     print('Something went wrong', e)
    finally:
        robot.close()
    return robot, gripper

if __name__ == "__main__":
    print(argv)
    main(argv[1], float(argv[2]))
