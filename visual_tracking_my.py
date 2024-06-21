"""
 This controller is made by group 12,

 using already prepared functions and hints
 from "Beispiel Code":
 03_opencv.py03_opencv.py
 04_opencv_color_blob.py
 05_opencv_color_blob_extended.py
 mycamera.pymycamera.py
"""

import math
from controller import Robot, Camera

#import for picture detection
import cv2
import numpy as np


robot = Robot()

# we process each image every 40ms = 25fps
timestep = int(robot.getBasicTimeStep() * 4)

# get access to the cameras and enable them
camera_top    = robot.getDevice("CameraTop")
camera_top.enable(timestep)

## enable the bottom camera if necessary
camera_bottom = robot.getDevice("CameraBottom")
camera_bottom.enable(timestep)

head_yaw   = robot.getDevice("HeadYaw")
head_pitch = robot.getDevice("HeadPitch")

# move arms down
lShoulderPitch = robot.getDevice("LShoulderPitch")
rShoulderPitch = robot.getDevice("RShoulderPitch")
lShoulderPitch.setPosition( math.radians(90) )
rShoulderPitch.setPosition( math.radians(90) )

# Get image and convert into a NumPy array
def getImage(camera):
    height = camera.getHeight()
    width = camera.getWidth()
    img = camera.getImage()
    img = np.frombuffer(img, dtype=np.uint8)
    img = img.reshape((height, width, 4))
    img = img[:,:,[0,1,2]] # last channel not needed
    return img

while robot.step(timestep) != -1:
    # current time in s
    t = robot.getTime()

    ###################################################################
    # Find duck block
    #################

    # same as img = cv2.imread('robocup.png')
    img = getImage(camera_top)
    # For debugging:
    cv2.imshow('CameraTop',img)

    # convert to hsv
    hsv  = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    # regular: H \in [0,360]
    # opencv : H \in [0,180]
    h = 320/2
    # lower and upper - define a block, what we are looking for Yellow collor (duck)
    lower = np.array([h-160, 180, 150])
    upper = np.array([h-120, 210, 255])

    # mask color. Find this block in hsv image
    mask = cv2.inRange(hsv, lower, upper)

    # For debugging:
    cv2.imshow('color mask',mask)

    ###################################################################
    # Adapt Mask with morphological operations
    ##########################################

    # adapt the mask
    kernel = np.ones((3,3),np.uint8)
    # Erosion: Removes (erodes) small objects from the image.
    mask = cv2.erode(mask,kernel,iterations = 3)
    # Dilation: Fills (dilates) the remaining objects.
    mask = cv2.dilate(mask,kernel,iterations = 15)
    # 15 - as the duck is sometimes turned at an angle where the torso and
    # nose are visible and there is too large a gap between them to be recognized as a separate object
    mask = cv2.erode(mask,kernel,iterations = 5) # TODO: More precise? We can discuss

    # alternative to erode/dilate opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    # with cv2.MORPH_OPEN or cv2.MORPH_CLOSE

    # For debugging:
    cv2.imshow('color mask + morphological operations',mask)

    ###################################################################
    # Use the mask to find the outline of the duck in the picture
    #############################################################

    # detect contours
    contours, hierarchy = cv2.findContours(image=mask, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

    # For debugging:
    # If you are using/not using img_result -> you will need to enable/disable debugging #1, #2 and #3
    img_result = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    for c in contours:
        # calculate and dra the bounding box :)
        rect = cv2.boundingRect(c)
        x, y, w, h = rect  # unpack

        # For debugging #1:
        cv2.rectangle(img_result, (x, y), (x + w, y + h), (255, 0, 0), 1)

        # calculate moments
        M = cv2.moments(c)

        # moment_{0,0} = Area/ Number of Pixels inside the contour
        a = M["m00"]

        # non empty
        if a > 0:
            # calculate the center of mass (COM)
            cX = int(M["m10"] / a)  # average x-coordinate
            cY = int(M["m01"] / a)  # average y-coordinate

            # For debugging #2:
            cv2.circle(img_result, (cX, cY), 3, (255, 0, 0), -1)

    # For debugging #3:
    center_coordinates = (img.shape[1] // 2, img.shape[0] // 2) # Center of the image
    print((cX, cY))
    print(center_coordinates)
    cv2.circle(img_result, center_coordinates, 2, (0, 0, 255), -1)
    cv2.imshow('Result',img_result)

    ###################################################################

    # save frames (slows down the simulation)
    #camera_top.saveImage('./{}.png'.format(t), 100)

    # calculate the target joints
    target_head_yaw   = math.radians(100) * math.sin(t)
    target_head_pitch = math.radians(10) * math.cos(t)

    # set joints / move head
    # Horizont axis
    #head_yaw.setPosition(target_head_yaw)
    # Vertikal axis
    #head_pitch.setPosition(target_head_pitch)



    # show all images | don't block
    cv2.waitKey(1)

cv2.destroyAllWindows()