import pyautogui
import numpy as np
import time
import os

# Save the screenshot in data folder with name i.png
def save_screenshot(i):
    # Take a screenshot of the screen
    my_screenshot_image = pyautogui.screenshot()

    # Only save region of interest
    my_screenshot_image = my_screenshot_image.crop((250, 26, 250+456, 1010))
    my_screenshot_image.save(os.path.join("data", f"{i}.png"))
    print(f"Screenshot {i} saved.")

# Create data folder if it doesn't exist
if not os.path.exists("data"):
    os.makedirs("data")

# Find the highest existing image number in the data folder
existing_files = [f for f in os.listdir("data") if f.endswith(".png") and f[:-4].isdigit()]
if existing_files:
    max_index = max(int(f[:-4]) for f in existing_files)
else:
    max_index = -1

# Take screenshot every 5 seconds, continuing numbering
for i in range(max_index + 1, max_index + 1 + 100):
    save_screenshot(i)
    # Wait for 4 seconds before taking the next screenshot
    time.sleep(10)
