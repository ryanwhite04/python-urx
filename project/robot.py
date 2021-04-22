import urx
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper as Gripper
from time import sleep
from filter import filterImage

def getRobot(ip):
    rob = urx.Robot(ip)
    rob.set_tcp((0, 0, 0.1, 0, 0, 0))
    rob.set_payload(2, (0, 0, 0.1))
    sleep(0.2)
    return rob



def main(ip="192.168.1.6"):
    robot = getRobot(ip)
    gripper = Gripper(robot)
    return robot, gripper

if __name__ == "__main__":
    main()
