
import urx
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper as Gripper
from sys import argv
from time import sleep

def getRobot(ip):
    rob = urx.Robot(ip, use_rt=True, urFirm=5.10)
    rob.set_tcp((0, 0, 0.1, 0, 0, 0))
    rob.set_payload(2, (0, 0, 0.1))
    sleep(0.2)
    return rob

def main(num, speed=0.1):
    ip = f'192.168.1.{num}'
    robot = getRobot(ip)
    gripper = Gripper(robot)
    try:
        gripper.open_gripper()
        input("Move tool over object then hit enter: ")
        object_position = robot.get_pose()
        input("Move tool somewhere else and hit enter: ")
        position = robot.get_pose()
        robot.set_pose(object_position, speed, speed)
        gripper.close_gripper()
        robot.set_pose(position, speed, speed)
    except:
        print('something went wrong')
    finally:
        robot.close()
    return robot, gripper

if __name__ == "__main__":
    main(argv[1], float(argv[2]))
