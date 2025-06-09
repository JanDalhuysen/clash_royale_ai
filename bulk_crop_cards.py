import cv2
import numpy as np
from PIL import Image
import os

# import pytesseract
# import pyautogui
# import requests
# import base64
# import json
# import time
# from translate import Translator
# import difflib
# import contractions

print("Choose folder with images to crop")
exit()

# crop all images to only keep the middle third in images folder
images_folder = "testing2"
if os.path.exists(images_folder):
    for image_to_find in os.listdir(images_folder):
        image_path = os.path.join(images_folder, image_to_find)
        if os.path.isfile(image_path):
            # Load the image
            img = cv2.imread(image_path)

            # Get the dimensions of the image
            height, width = img.shape[:2]

            # Calculate the coordinates for cropping

            print("Choose cropping method:")
            print("1. Crop top and bottom")
            print("2. Crop left and right")
            exit()

            # For cropping top and bottom
            # start_x = 0
            # end_x = width
            # start_y = int(height / 8)
            # end_y = int(height * 7 / 8)

            # For cropping left and right
            # start_x = int(width / 8)
            # end_x = int(width * 7 / 8)
            # start_y = 0
            # end_y = height

            # Crop the image
            cropped_img = img[start_y:end_y, start_x:end_x]

            # Save the cropped image
            cv2.imwrite(image_path, cropped_img)

exit()
