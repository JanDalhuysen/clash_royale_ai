import pyautogui
import numpy as np
import time
import os
import cv2


# Save the screenshot in data folder with name i.png
def save_screenshot(i):
    # Take a screenshot of the screen
    my_screenshot_image = pyautogui.screenshot()

    # Only save region of interest
    # def show_preds_live_screen(region={'top': 1, 'left': 1, 'width': 860, 'height': 1400}):
    my_screenshot_image = my_screenshot_image.crop((0, 50, 1000, 1045))
    # my_screenshot_image = my_screenshot_image.crop((250, 26, 250+456, 1010))
    # my_screenshot_image.save(os.path.join("data", f"{i}.png"))
    # print(f"Screenshot {i} saved.")

    # Make the left most 100 and right most 100 pixel black

    img_array = np.array(my_screenshot_image)
    img_array[:, :100] = 0
    img_array[:, -100:] = 0
    # Remove the top 30 pixels
    img_array[:30, :] = 0
    # Save the modified image with opencv
    modified_image = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    # Get current timestamp in milliseconds
    timestamp = int(time.time() * 1000)
    cv2.imwrite(os.path.join("data", f"{timestamp}.png"), modified_image)
    print(f"Screenshot {i} saved.")

    # Get current timestamp in milliseconds
    # timestamp = int(time.time() * 1000)
    # Save the screenshot with the timestamp in the filename
    # my_screenshot_image.save(os.path.join("data", f"{timestamp}.png"))
    # print(f"Screenshot {timestamp} saved.")


# Create data folder if it doesn't exist
if not os.path.exists("data"):
    os.makedirs("data")

# Find the highest existing image number in the data folder
existing_files = [f for f in os.listdir("data") if f.endswith(".png") and f[:-4].isdigit()]
if existing_files:
    max_index = max(int(f[:-4]) for f in existing_files)
else:
    max_index = -1

# Take screenshot every x seconds, continuing numbering
for i in range(max_index + 1, max_index + 1 + 100):
    save_screenshot(i)
    # Wait for x seconds before taking the next screenshot
    wait_time = 5
    time.sleep(wait_time)
