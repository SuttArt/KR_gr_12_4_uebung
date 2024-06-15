#
# Installation
#
#   pip install opencv-python
#
# Tutorials
#  
#   https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html
#   https://www.geeksforgeeks.org/opencv-python-tutorial/
#

import cv2
import numpy as np
from matplotlib import pyplot as plt

# Oeffne das Bild
img = cv2.imread('robocup.png') # BGR

# nutze matplotlib um das Bild anzuzeigen
plt.imshow(img)
# plotte die Farben der 100-ten Zeile
plt.plot(img[100,:,:])
plt.show()

# nutze opencv um das Bild anzuzeigen
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()