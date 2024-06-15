import cv2
import numpy as np
import sys

# Oeffne das Bild
img = cv2.imread('robocup.png')

# convert to hsv
hsv  = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# gray scale image
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.imshow('image',img)
#cv2.imshow('gray',gray)


# define range of blue color in HSV
h = 320/2
lower = np.array([h-20, 102, 153])
upper = np.array([h+20, 204, 255])

#lower = np.array([80, 120, 150])
#upper = np.array([100, 150, 200])

print(f"h = {h}")
print(f"lower = [{lower[0]}, {lower[1]}, {lower[2]}]")
print(f"upper = [{upper[0]}, {upper[1]}, {upper[2]}]")

# mask color
mask = cv2.inRange(hsv, lower, upper)
cv2.imshow('color mask',mask)


###################################################################

# adapt the mask
kernel = np.ones((3,3),np.uint8)
mask = cv2.erode(mask,kernel,iterations = 1)
mask = cv2.dilate(mask,kernel,iterations = 1)

# cv2.MORPH_OPEN:
# 1) Erosion: Entfernt (erodiert) kleine Objekte aus dem Bild.
# 2) Dilatation: Füllt (dilatiert) die verbliebenen Objekte wieder auf.

# cv2.MORPH_CLOSE:
# 1) Dilatation
# 2) Erosion
opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

cv2.imshow('color mask + morphological operations',mask)

cv2.imshow('openung mask',opening)


# show all images
#cv2.waitKey(0)
#cv2.destroyAllWindows()
# exit code
#sys.exit(0)

###################################################################

# Diese Zeile führt eine bitweise UND-Operation zwischen dem Originalbild (img) und sich selbst durch,
# aber nur an den Positionen, die durch die Maske (mask) angegeben sind. Die Maske ist ein binäres Bild,
# bei dem die Bereiche von Interesse (z.B. bestimmte Farben oder Formen) weiß sind und der Rest schwarz ist.
# Das Ergebnis (blob) enthält nur die Teile des Bildes, die innerhalb der Maske liegen.

# Bitwise-AND mask and original image
blob = cv2.bitwise_and(img,img, mask= mask)

#cv2.imshow('blob',blob)

# detect contours
contours, hierarchy = cv2.findContours(image=mask, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
#print(contours)
#print(hierarchy)

cv2.drawContours(img, contours, -1, (0,255,0), 3)
cv2.imshow('image',img)

# show all images
cv2.waitKey(0)
cv2.destroyAllWindows()
