import cv2
import numpy as np

# Funktion zur Aktualisierung der Farbe basierend auf Trackbar-Werten
def update_color(x):
    h = cv2.getTrackbarPos('Hue', 'Color')
    s = cv2.getTrackbarPos('Saturation', 'Color')
    v = cv2.getTrackbarPos('Value', 'Color')
    show_color_from_hsv(h, s, v)

# Funktion zur Konvertierung von HSV nach BGR und Anzeige der Farbe
def show_color_from_hsv(h, s, v):
    hsv_color = np.uint8([[[h, s, v]]])
    bgr_color = cv2.cvtColor(hsv_color, cv2.COLOR_HSV2BGR)[0][0]
    color_image = np.zeros((300, 300, 3), dtype=np.uint8)
    color_image[:] = bgr_color
    cv2.imshow('Color', color_image)

# Erstellen eines Fensters
cv2.namedWindow('Color')

# Hinzufügen von Trackbars
cv2.createTrackbar('Hue', 'Color', 0, 179, update_color)
cv2.createTrackbar('Saturation', 'Color', 0, 255, update_color)
cv2.createTrackbar('Value', 'Color', 0, 255, update_color)

# Initiale Farbe anzeigen
update_color(0)

# Warten, bis ein Benutzer eine Taste drückt
cv2.waitKey(0)
cv2.destroyAllWindows()
