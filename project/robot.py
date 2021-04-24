import urx
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper as Gripper
from time import sleep
from filter import *
from requests import get

def getImage(ip, path="camera.jpg"):
    content = get(f'http://{ip}:4242/current.jpg?annotations=off').content
    with open(path, 'wb') as f:
        f.write(content)
    return path

def showCamera(ip):
    path = getImage(ip)
    image = cv.imread(path)
    filtered = filterImage(image, RED)
    cv.imshow('camera', image)
    cv.imshow('red', filtered)
    cv.waitKey(0)
    cv.destroyAllWindows()

def getRobot(ip):
    rob = urx.Robot(ip, use_rt=True, urFirm=5.1)
    rob.set_tcp((0, 0, 0.1, 0, 0, 0))
    rob.set_payload(2, (0, 0, 0.1))
    sleep(0.2)
    return rob

def main(ip="192.168.1.6"):
    robot = getRobot(ip)
    gripper = Gripper(robot)
    # while 1:
    #     j_temp = robot.get_joint_temperature()
    #     print(j_temp)
    # position = (0.56597, 0.10704, 0.40409)
    # robot.set_pos(position)
    #     sleep(0.1)
    while 1:
        showCamera(ip)
    return robot, gripper, position

if __name__ == "__main__":
    main()
