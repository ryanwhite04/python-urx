from request import get

ROBOT
GRIPPER

def main(num, robot, gripper, buckets):
    global ROBOT = robot
    global GRIPPER = gripper
    clean(num, buckets)

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

def set_height(height):
    r = ROBOT
    pose = r.get_pose()
    pose.pos[2] = height
    r.set_pose(pose)

def clean(num, buckets):
    angle = pi/4, delta = 0.1
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
        deposit(color, image)

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
    robot = ROBOT
    gripper = GRIPPER
    pose = robot.get_pose()
    centre(num, color, threshold)
    gripper.open_gripper()
    cameraDown(robot)
    set_height(height)
    gripper.close_gripper()
    robot.set_pose(pose)
    robot.set_pose(buckets[color])
    gripper.open_gripper()
    robot.set_pose(pose)

def centre(num, color, threshold, dimensions)
    x, y = getCoordinates(color)
    if abs(x-dimensions[0]) < threshold:
        if abs(y-dimensions[1]) < threshold:
            return
        else:
            moveUp(y-dimensions[1])
            centre(color, threshold, dimensions)
    else:
        moveRight(x-dimensions[0])
        centre(color, threshold, dimensions)
