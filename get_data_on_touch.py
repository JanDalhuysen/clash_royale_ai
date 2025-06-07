import sys
import cv2
import numpy as np
import time
import os
import pyautogui

# adb shell getevent | python get_data_on_touch.py

# This program listens for touch events from stdin,
# saves a screenshot and touch coordinates to files
# when a touch is detected, and organizes the data into separate folders.

# Save the screenshot in data folder with name i.png
def save_screenshot(i):
    # Take a screenshot of the screen
    my_screenshot_image = pyautogui.screenshot()

    # Only save region of interest
    my_screenshot_image = my_screenshot_image.crop((250, 26, 250+456, 1010))
    my_screenshot_image.save(os.path.join("data", f"{i}.png"))
    print(f"Screenshot {i} saved.")
    time.sleep(0.5)  # Add a small delay to avoid overwhelming the system

# Create data folder if it doesn't exist
if not os.path.exists("data"):
    os.makedirs("data")

# Create touch_events folder if it doesn't exist
if not os.path.exists("touch_events"):
    os.makedirs("touch_events")

# Find the highest existing image number in the data folder
existing_files = [f for f in os.listdir("data") if f.endswith(".png") and f[:-4].isdigit()]
if existing_files:
    max_index = max(int(f[:-4]) for f in existing_files)
else:
    max_index = -1


img = np.ones((2400, 1080, 3), dtype=np.uint8) * 255

x, y = -1, -1
gotX, gotY = False, False

# cv2.namedWindow("Points", cv2.WINDOW_NORMAL)

for line in sys.stdin:
    line = line.strip()
    if "0000 0000 00000000" in line:
        if gotX and gotY:
            if 0 <= x < 1080 and 0 <= y < 2400:
                # Log the event: timestamp and coordinates
                # if y < 2000:
                    # wait 3.6 seconds before taking the screenshot
                    # time.sleep(3.6)

                touch_timestamp = time.time()
                save_screenshot(touch_timestamp)

                # Create the touch event file in the touch_events folder
                with open(os.path.join('touch_events', f"{touch_timestamp}.txt"), 'w') as touch_file:
                    touch_file.write(f"{x},{y}\n")
            # cv2.circle(img, (x, y), 10, (0, 0, 255), -1)  # Red dot
            # cv2.imshow("Points", img)
        gotX = gotY = False
        x = y = -1
        continue

    if "0003 0035" in line:
        parts = line.split()
        if len(parts) >= 4:
            x = int(parts[3], 16)
            print(f"X: {x}")
            gotX = True

    if "0003 0036" in line:
        parts = line.split()
        if len(parts) >= 4:
            y = int(parts[3], 16)
            print(f"Y: {y}")
            gotY = True

# cv2.destroyAllWindows()
