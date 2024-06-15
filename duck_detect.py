import cv2
import numpy as np
import sys

# Oeffne das Bild
img = cv2.imread('imgs/1.png')

# convert to hsv
hsv  = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Für debugging:
cv2.imshow('image',img)



# define range of blue color in HSV
# regular: H \in [0,360]
# opencv : H \in [0,180]
h = 320/2
lower = np.array([h-160, 180, 150])
upper = np.array([h-120, 210, 255])

# Für debugging:
#print(f"h = {h}")
#print(f"lower = [{lower[0]}, {lower[1]}, {lower[2]}]")
#print(f"upper = [{upper[0]}, {upper[1]}, {upper[2]}]")

# mask color
mask = cv2.inRange(hsv, lower, upper)
cv2.imshow('color mask',mask)

###################################################################

# adapt the mask
kernel = np.ones((3,3),np.uint8)
mask = cv2.erode(mask,kernel,iterations = 1)
mask = cv2.dilate(mask,kernel,iterations = 6)

# Für debugging:
cv2.imshow('color mask + morphological operations',mask)


###################################################################

# detect contours
contours, hierarchy = cv2.findContours(image=mask, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)



# iterate over all contours
for c in contours:

    # calculate and dra the bounding box :)
    rect = cv2.boundingRect(c)
    x, y, w, h = rect  # unpack

    # Für debugging:
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)

    # calculate moments
    M = cv2.moments(c)

    # moment_{0,0} = Area/ Number of Pixels inside the contour
    a = M["m00"]

    # non empty
    if a > 0:
        # calculate the center of mass (COM)
        cX = int(M["m10"] / a)  # average x-coordinate
        cY = int(M["m01"] / a)  # average y-coordinate
        cv2.circle(img, (cX, cY), 7, (255, 0, 0), -1)

# Für debugging:
cv2.imshow('image',img)

# show all images
cv2.waitKey(0)
cv2.destroyAllWindows()
