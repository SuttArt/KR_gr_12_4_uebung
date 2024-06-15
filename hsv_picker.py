import cv2
import numpy as np

# Funktion, die beim Klicken aufgerufen wird
def get_hsv_color(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # Linke Maustaste gedrückt
        # Pixelwerte an der angeklickten Position erhalten
        bgr_color = img[y, x]
        # Umwandlung der BGR-Farbe in HSV
        hsv_color = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)[0][0]
        print(f"Position (x={x}, y={y}): BGR={bgr_color}, HSV={hsv_color}")

# Bild laden !!!!!!!!!!!!!!!!!!!!!!!!!!
img = cv2.imread('imgs/1.png')
#img = cv2.imread('robocup.png')
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

cv2.namedWindow('image')
cv2.setMouseCallback('image', get_hsv_color)

while True:
    cv2.imshow('image', img)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC zum Beenden
        break

cv2.destroyAllWindows()
