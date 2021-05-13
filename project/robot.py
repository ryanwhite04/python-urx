
import urx
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper as Gripper
from sys import argv
from time import sleep
from clean import clean

def getRobot(ip):
    rob = urx.Robot(ip, use_rt=True, urFirm=5.10)
    rob.set_tcp((0, 0, 0.1, 0, 0, 0))
    rob.set_payload(2, (0, 0, 0.1))
    sleep(0.2)
    return rob

def main(num, speed=0.1, acceleration=speed):
    ip = f'192.168.1.{num}'
    robot = getRobot(ip)
    gripper = Gripper(robot)
    buckets = {}
    try:
        input("Move tool over the RED bucket, then press Enter: ")
        buckets["Red"] = robot.get_pose()
        input("Move tool over the GREEN bucket, then press Enter: ")
        buckets["Green"] = robot.get_pose()
        input("Move tool over the YELLOW bucket, then press Enter: ")
        buckets["Yellow"] = robot.get_pose()
        input("Move tool to a good height and press enter: ")
        position = robot.get_pose()
        clean(num, robot, gripper, buckets)
        robot.set_pose(position, speed, acceleration)
    except:
        print('Something went wrong')
    finally:
        robot.close()
    return robot, gripper

if __name__ == "__main__":
    main(argv[1], float(argv[2]))
