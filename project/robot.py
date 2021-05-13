
import urx
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper as Gripper
from sys import argv
from time import sleep
from clean import clean
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
        BASE_POSITION = robot.get_pose()
        print("Moving to red bucket...")
        robot.set_pose(buckets["Red"], speed, acceleration)
        sleep(10)
        print("Moving to green bucket...")
        robot.set_pose(buckets["Green"], speed, acceleration)
        sleep(10)
        print("Moving to yellow bucket...")
        robot.set_pose(buckets["Yellow"], speed, acceleration)
        sleep(10)
        print("Moving to start position...")
        robot.set_pose(BASE_POSITION, speed, acceleration)
        print("Done")
        clean(robot, gripper, BASE_POSITION, buckets)
    except:
        print('Something went wrong')
    finally:
        robot.close()
    return robot, gripper

if __name__ == "__main__":
    main(argv[1], float(argv[2]))
