
def set_height(height):
    pose = r.get_pose()
    pose.pos[2] = height
    r.set_pose(pose)

def clean(robot, gripper, pose, buckets):
    # robot.set_pose(pose)
    angle = pi/4, delta = 0.1
    for color in ["red", "green", "yellow"]:
        sort(color)
        angle *= -1
        delta *= -1

def sort(color, delta, angle, base, speed=0.1):
    j = r.getj()
    j[0] = -angle
    r.movej(j, speed, speed/2)
    while r.getj()[0] < angle:
        found, image = search(color)
        while not found:
            j = r.getj()
            j[0] += delta
            r.movej(j, speed, speed/2)
            found, image = search(color)
        deposit(color, image)

def deposit(color, image, height=0.1):
    pose = robot.get_pose()
    centre(color, threshold)
    gripper.open_gripper()
    set_height(height)
    gripper.close_gripper()
    robot.set_pose(pose)
    robot.set_pose(buckets[color])
    gripper.open_gripper()
    robot.set_pose(pose)

def centre(color, threshold, horizontal=True)
    # TODO

    
