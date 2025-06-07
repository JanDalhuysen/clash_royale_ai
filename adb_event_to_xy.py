import sys
import cv2
import numpy as np

# adb shell getevent | python adb_event_to_xy.py

# This program reads touch event data from stdin,
# extracts (x, y) coordinates,and displays them
#  as red dots on a white image using OpenCV.

img = np.ones((2400, 1080, 3), dtype=np.uint8) * 255

x, y = -1, -1
gotX, gotY = False, False

cv2.namedWindow("Points", cv2.WINDOW_NORMAL)

for line in sys.stdin:
    line = line.strip()
    if "0000 0000 00000000" in line:
        if gotX and gotY:
            if 0 <= x < 1080 and 0 <= y < 2400:
                cv2.circle(img, (x, y), 10, (0, 0, 255), -1)  # Red dot
                cv2.imshow("Points", img)
                if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
                    break
        gotX = gotY = False
        x = y = -1
        continue

    if "0003 0035" in line:
        parts = line.split()
        if len(parts) >= 4:
            x = int(parts[3], 16)
            gotX = True

    if "0003 0036" in line:
        parts = line.split()
        if len(parts) >= 4:
            y = int(parts[3], 16)
            gotY = True

cv2.destroyAllWindows()
