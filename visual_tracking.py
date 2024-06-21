import cv2
import math
import numpy as np
from controller import Robot, Camera

HUE_YELLOW = 60 / 2   # yellow hue value in OpenCV HSV
TRACKING_SPEED = 0.02 # larger values increase the speed of head motors
# Seconds to wait before looking around when loosing track of an object
PANIC_DELAY = 1

# Threshold for the moment's zero area (MM0) in center_of_mass()
MOMENT_ZERO_THRESH = 10

# upper and lower bounds of saturation and value in center_of_mass()
SAT_LOWER = 180
SAT_UPPER = 200
VAL_LOWER = 200
VAL_UPPER = 255

# Calculate the center of mass of the largest contour of a given
# hue in an image
def center_of_mass(img, hue):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img = cv2.medianBlur(img, 9)
    lower = np.array([hue-10, SAT_LOWER, VAL_LOWER])
    upper = np.array([hue+10, SAT_UPPER, VAL_UPPER])
    mask = cv2.inRange(img, lower, upper)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_NONE)
    if len(contours) == 0:
        # No contour within the specified color range found
        return (None, None)

    largest_contour = max(contours, key=cv2.contourArea)
    moments = cv2.moments(largest_contour)
    if moments["m00"] < MOMENT_ZERO_THRESH:
        # Discard as what weve found is too small to be our duck
        return (None, None)

    center_x = int(moments["m10"] / moments["m00"])
    center_y = int(moments["m01"] / moments["m00"])
    return (center_x, center_y)

def move_arms_down(robot):
    lShoulderPitch = robot.getDevice("LShoulderPitch")
    rShoulderPitch = robot.getDevice("RShoulderPitch")
    lShoulderPitch.setPosition( math.radians(90) )
    rShoulderPitch.setPosition( math.radians(90) )

def main():
    robot = Robot()

    # we process each image every 40ms = 25fps
    timestep = int(robot.getBasicTimeStep() * 4)

    # get access to the cameras and enable them
    camera_top    = robot.getDevice("CameraTop")
    camera_top.enable(timestep)

    head_yaw   = robot.getDevice("HeadYaw")
    head_pitch = robot.getDevice("HeadPitch")
    move_arms_down(robot)

    # Last time we saw the duck
    last_time_seen = 0
    while robot.step(timestep) != -1:
        # current time in s
        t = robot.getTime()

        # getImage() returns a byte string, which needs to be converted
        # into a BGR array for center_of_mass() / OpenCV
        img = np.frombuffer(camera_top.getImage(), dtype=np.uint8)
        img = img.reshape((camera_top.getHeight(),
            camera_top.getWidth(), 4))

        (center_x, center_y) = center_of_mass(img, HUE_YELLOW)
        if center_x and center_y:
            last_time_seen = t

            # switch to velocity control mode
            head_yaw.setPosition(float('inf'))
            head_pitch.setPosition(float('inf'))
            
            # set velocity based on how far the center of mass is from
            # the center of the camera view
            error_x = camera_top.getWidth() / 2 - center_x
            error_y = camera_top.getHeight() / 2 - center_y
            head_yaw.setVelocity(error_x * TRACKING_SPEED)
            head_pitch.setVelocity(-error_y * TRACKING_SPEED)
        elif (t - last_time_seen) > PANIC_DELAY:
            # We've lost track of the duck! Look around to find it again.
            # switch to position control mode
            head_yaw.setVelocity(head_yaw.getMaxVelocity())
            head_pitch.setVelocity(head_pitch.getMaxVelocity())
            # calculate the target joints
            target_head_yaw   = math.radians(110) * math.sin(t)
            target_head_pitch = math.radians(10)
            # set joints
            head_yaw.setPosition(target_head_yaw)
            head_pitch.setPosition(target_head_pitch)

if __name__ == "__main__":
    main()