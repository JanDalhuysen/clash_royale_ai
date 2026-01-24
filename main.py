import cv2
import numpy as np
from PIL import Image
import pytesseract
import os

import pyautogui
import requests
import base64
import json
import time

# from translate import Translator

import difflib

# import contractions

im1 = pyautogui.screenshot()
im1.save(r"in.png")
im1.save(r"original.png")

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

            # For cropping top and bottom
            start_x = 0
            end_x = width
            start_y = int(height / 8)
            end_y = int(height * 7 / 8)

            # For cropping left and right
            # start_x = int(width / 9)
            # end_x = int(width * 8 / 9)
            # start_y = 0
            # end_y = height

            # Crop the image
            cropped_img = img[start_y:end_y, start_x:end_x]

            # Save the cropped image
            cv2.imwrite(image_path, cropped_img)

exit()


def find_button_coordinates_opencv_multiscale(screenshot_path, button_image_path, confidence=0.8, scales=None):
    if scales is None:
        # Try 3 scales from 90% down to 70%
        scales = np.linspace(0.7, 0.9, 3)[::-1]

    screenshot = cv2.imread(screenshot_path)
    original_button_img = cv2.imread(button_image_path)

    if screenshot is None:
        # ... (error handling)
        return None
    if original_button_img is None:
        # ... (error handling)
        return None

    (sH, sW) = screenshot.shape[:2]
    (oBH, oBW) = original_button_img.shape[:2]

    found = None

    for scale in scales:
        # Resize the template
        new_width = int(oBW * scale)
        new_height = int(oBH * scale)

        # Ensure the template is not larger than the screenshot after resizing
        if new_width == 0 or new_height == 0 or new_width > sW or new_height > sH:
            continue

        resized_button_img = cv2.resize(original_button_img, (new_width, new_height))

        # Perform template matching
        result = cv2.matchTemplate(screenshot, resized_button_img, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if found is None or max_val > found[0]:
            found = (
                max_val,
                max_loc,
                scale,
                resized_button_img.shape[1],
                resized_button_img.shape[0],
            )

    if found and found[0] >= confidence:
        max_val, max_loc, scale_used, btn_w, btn_h = found
        print(f"Match found with scale {scale_used:.2f} and confidence {max_val:.2f}")
        top_left = max_loc
        center_x = top_left[0] + btn_w // 2
        center_y = top_left[1] + btn_h // 2
        return center_x, center_y
    # else:
    # if found:
    # print(f"Button '{os.path.basename(button_image_path)}' not found with sufficient confidence (best: {found[0]:.2f} < {confidence})")
    # else:
    # print(f"Button '{os.path.basename(button_image_path)}' not found (no potential matches).")
    # return None


def find_button_coordinates_opencv(screenshot_path, button_image_path, confidence=0.8):
    try:
        # --- Load the screenshot and the button image ---
        screenshot = cv2.imread(screenshot_path)
        button_img = cv2.imread(button_image_path)

        if screenshot is None:
            raise FileNotFoundError(f"Could not open or find the image at: {screenshot_path}")
        if button_img is None:
            raise FileNotFoundError(f"Could not open or find the image at: {button_image_path}")

        # --- Perform template matching ---
        result = cv2.matchTemplate(screenshot, button_img, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # --- Check if the match is good enough ---
        if max_val >= confidence:
            # --- Calculate the center coordinates of the matched button ---
            button_width = button_img.shape[1]
            button_height = button_img.shape[0]
            top_left = max_loc
            center_x = top_left[0] + button_width // 2
            center_y = top_left[1] + button_height // 2
            return center_x, center_y
        else:
            print(f"Button '{os.path.basename(button_image_path)}' not found with sufficient confidence ({max_val:.2f} < {confidence})")
            return None

    except Exception as e:
        print(f"Error during OpenCV image matching for '{os.path.basename(button_image_path)}': {e}")
        return None


# Loop through all images in the 'images' folder and try to find them in 'original.png'
images_folder = "all_cards_small_cropped"
if os.path.exists(images_folder):
    for image_to_find in os.listdir(images_folder):
        image_path = os.path.join(images_folder, image_to_find)
        if os.path.isfile(image_path):
            # button_coordinates = find_button_coordinates_opencv("original.png", image_path, confidence=0.3)
            button_coordinates = find_button_coordinates_opencv_multiscale("original.png", image_path, confidence=0.8)  # Adjust confidence
            screenshot = cv2.imread("original.png")
            button_img = cv2.imread(image_path)
            # if screenshot is not None:
            # print(f"Screenshot dimensions: {screenshot.shape}")
            # if button_img is not None:
            # print(f"Button image dimensions: {button_img.shape}")

            if button_coordinates:
                x, y = button_coordinates
                print(f"Moving mouse to coordinates of the {image_to_find}: x={x}, y={y}")
                # Draw a red rectangle around the found area
                screenshot = cv2.imread("original.png")
                button_img = cv2.imread(image_path)
                if screenshot is not None and button_img is not None:
                    button_w, button_h = (
                        button_img.shape[1],
                        button_img.shape[0],
                    )
                    # Calculate top-left corner from center
                    top_left_x = int(x - button_w // 2)
                    top_left_y = int(y - button_h // 2)
                    bottom_right_x = int(top_left_x + button_w)
                    bottom_right_y = int(top_left_y + button_h)
                    cv2.rectangle(
                        screenshot,
                        (top_left_x, top_left_y),
                        (bottom_right_x, bottom_right_y),
                        (0, 0, 255),
                        2,
                    )
                    # Save or show the image with the rectangle
                    out_path = f"found_{os.path.splitext(image_to_find)[0]}.png"
                    cv2.imwrite(out_path, screenshot)
                    print(f"Red box drawn and saved to {out_path}")
                pyautogui.moveTo(x, y, duration=1)
                # pyautogui.click()
                time.sleep(0.25)
else:
    print(f"Folder '{images_folder}' does not exist.")


exit()

words_to_choose_from = []

words_to_choose_from.append("i")
words_to_choose_from.append("I")

im1 = pyautogui.screenshot()
im1.save(r"in.png")
im1.save(r"original.png")

# Path to the uploaded image
image_path = "in.png"

try:
    # --- Load the image with OpenCV ---
    img_cv = cv2.imread(image_path)
    if img_cv is None:
        raise FileNotFoundError(f"Could not open or find the image at: {image_path}")

    # --- Convert to grayscale ---
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

    # --- Apply Canny edge detection ---
    # Adjust these thresholds based on your image
    edges = cv2.Canny(gray, 100, 200)  # Try higher thresholds

    # --- Dilate the edges (Optional but often helpful) ---
    kernel = np.ones((3, 3), np.uint8)  # Adjust kernel size as needed
    dilated_edges = cv2.dilate(edges, kernel, iterations=1)  # Adjust iterations as needed

    # --- Find contours ---
    contours, _ = cv2.findContours(dilated_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # --- Filter contours to identify button-like shapes ---
    button_count = 0

    for contour in contours:
        # Get the bounding box of the contour
        x, y, w, h = cv2.boundingRect(contour)

        # Filter based on area and aspect ratio to consider it a button
        # check if the button is in the lower half of the image
        if (y > img_cv.shape[0] / 2) and (y < img_cv.shape[0] - 80) and (w > 10) and (h > 10):
            # if min_button_area < w * h < max_button_area and 1.5 <= aspect_ratio <= 5.0: # Adjust aspect ratio as needed
            # --- Crop the button using PIL for easier text extraction ---
            img_pil = Image.open(image_path).convert("RGB")
            cropped_button = img_pil.crop((x, y, x + w, y + h))

            # --- Perform OCR to get the text from the button ---
            try:
                button_text = pytesseract.image_to_string(cropped_button, config="--psm 6")
                button_text = button_text.strip().lower()
                # replace special characters with space
                button_text = "".join(e if e.isalnum() else " " for e in button_text)

                words_to_choose_from.append(button_text)

                if button_text:
                    filename = f"{button_text.replace(' ', '_')}.png"
                    # filepath = os.path.join(output_directory, filename)
                    # save image in the current directory
                    filepath = filename
                    # only save if the filename is not already taken
                    if os.path.exists(filepath):
                        print(f"File '{filename}' already exists. Skipping...")
                    else:
                        # Save the cropped button image
                        cropped_button.save(filepath)
                        print(f"Cropped and saved: {filename}")
                        button_count += 1
            except pytesseract.TesseractNotFoundError:
                print("Error: Tesseract is not installed or not in your PATH.")
                break
        else:
            # Optionally, you can draw the rejected contours for debugging
            # cv2.rectangle(img_cv, (x, y), (x + w, y + h), (0, 0, 255), 2)
            pass

    # --- Optional: Draw the detected button contours on the original image for visualization ---
    cv2.drawContours(img_cv, contours, -1, (0, 255, 0), 2)
    cv2.imwrite("detected_buttons.png", img_cv)
    print(f"Detected button contours saved to 'detected_buttons.png'")

    print(f"Successfully cropped and saved {button_count} word buttons.")

except FileNotFoundError as e:
    print(f"Error: {e}")
except pytesseract.TesseractNotFoundError:
    print("Error: Tesseract is not installed or not in your PATH.")
except Exception as e:
    print(f"An error occurred: {e}")

time.sleep(1)

# # --- Ollama Configuration ---
# ollama_url = "http://localhost:11434/api/generate"
# model_name = "llama3.2:3b"
# image_path = "in.png"

# img_cv = cv2.imread(image_path)
# if img_cv is None:
#     raise FileNotFoundError(f"Could not open or find the image at: {image_path}")

# # Convert to grayscale
# gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

# # Crop the image to only keep the top half
# height = img_cv.shape[0] // 2
# cropped_img = img_cv[0:height, 0:img_cv.shape[1]]
# cv2.imwrite(image_path, cropped_img)

# # Crop the image to only keep the bottom half of the cropped image
# height = cropped_img.shape[0] // 2
# cropped_img = cropped_img[height:cropped_img.shape[0], 0:cropped_img.shape[1]]
# cv2.imwrite(image_path, cropped_img)

# # Extract text from the cropped image using Tesseract OCR
# extracted_text = pytesseract.image_to_string(cropped_img, config='--psm 6')

# # Remove everything up to the first ")"
# extracted_text = extracted_text.split(")", 1)[-1] if ")" in extracted_text else extracted_text

# print(" ")
# print("Extracted text:")
# print(extracted_text.strip())

# def get_translation_from_ollama(image_path, prompt, model):
#     try:
#         with open(image_path, "rb") as image_file:
#             image_data = image_file.read()
#             base64_image = base64.b64encode(image_data).decode('utf-8')

#         payload = {
#             "model": model,
#             "prompt": prompt,
#             # "images": [base64_image]
#         }

#         response = requests.post(ollama_url, json=payload, stream=True)
#         response.raise_for_status()

#         translated_text = ""
#         for line in response.iter_lines():
#             if line:
#                 try:
#                     data = json.loads(line.decode('utf-8'))
#                     if 'response' in data:
#                         translated_text += data['response']
#                     if data.get('done'):
#                         break
#                 except json.JSONDecodeError:
#                     print(f"Error decoding JSON: {line}")
#                     continue
#         return translated_text.strip()

#     except FileNotFoundError:
#         print(f"Error: Image not found at '{image_path}'")
#         return None
#     except requests.exceptions.RequestException as e:
#         print(f"Error communicating with Ollama: {e}")
#         return None

# use_ollama = False

# # get the translation Python Translator library

# translator = Translator(to_lang="en", from_lang="nl")
# translation = translator.translate(extracted_text.strip())

# print(" ")
# print("Python Translator library:")
# print(translation)

# # convert the translation to an array of words
# words = translation.split()
# # remove commas and periods from the words
# words = [word.replace(",", "").replace(".", "").replace("?", "").replace("!", "") for word in words]

# # Check is any word contains a contraction
# for word in words:
#     if "'" in word:
#         # Expand the contraction using the contractions library
#         expanded_word = contractions.fix(word)
#         words[words.index(word)] = expanded_word
#         print(f"Expanded contraction: '{word}' to '{expanded_word}'")

# # join the words back into a string
# translation = " ".join(words)

# print(" ")
# print("Translation after expanding contractions:")
# print(translation)

# # check if translation contains words that are not in the allowed words list
# for word in translation.split():
#     # remove commas and periods from the words
#     word = word.replace(",", "").replace(".", "").replace("?", "").replace("!", "")

#     if word.lower() not in words_to_choose_from:
#         print(f"Word '{word}' not in allowed words list")
#         print("Trying to find a close match...")
#         # Find close matches using difflib
#         try_fix = difflib.get_close_matches(word, words_to_choose_from)

#         # Check if try_fix is in the allowed words list
#         try:
#             if try_fix[0].lower() in words_to_choose_from:
#                 print(f"Found close match: '{try_fix[0]}'")
#                 translation = translation.replace(word, try_fix[0])
#                 print(f"Replaced '{word}' with '{try_fix[0]}'")
#         except IndexError:
#             print(f"No close match found for '{word}'")
#             use_ollama = True
#             print("translation failed, using Ollama instead")
#             break

# if use_ollama == False:
#     print(" ")
#     print("Final translation:")
#     print(translation)

# # get the translation from Ollama

# if use_ollama == True:

#     prompt_template = (
#         "Translate the following Dutch text into English, output only the answer, nothing else and no explanation, "
#         "only using the words provided below. "
#         "Do not use any words outside this list.\n\n"
#         "Dutch text: \n\n```\n{text}\n```\n\n"
#         "Allowed words: \n\n```\n{allowed_words}\n```\n\n"
#     )

#     allowed_words_str = ", ".join(words_to_choose_from)

#     prompt = prompt_template.format(text=extracted_text, allowed_words=allowed_words_str)

#     print(f"Prompt: '{prompt}'")

#     translation = get_translation_from_ollama(image_path, prompt, model_name)

# print(" ")
# print("Final translation:")
# print(translation)

# def find_button_coordinates_opencv(screenshot_path, button_image_path, confidence=0.8):
#     try:
#         # --- Load the screenshot and the button image ---
#         screenshot = cv2.imread(screenshot_path)
#         button_img = cv2.imread(button_image_path)

#         if screenshot is None:
#             raise FileNotFoundError(f"Could not open or find the image at: {screenshot_path}")
#         if button_img is None:
#             raise FileNotFoundError(f"Could not open or find the image at: {button_image_path}")

#         # --- Perform template matching ---
#         result = cv2.matchTemplate(screenshot, button_img, cv2.TM_CCOEFF_NORMED)
#         min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

#         # --- Check if the match is good enough ---
#         if max_val >= confidence:
#             # --- Calculate the center coordinates of the matched button ---
#             button_width = button_img.shape[1]
#             button_height = button_img.shape[0]
#             top_left = max_loc
#             center_x = top_left[0] + button_width // 2
#             center_y = top_left[1] + button_height // 2
#             return center_x, center_y
#         else:
#             print(f"Button '{os.path.basename(button_image_path)}' not found with sufficient confidence ({max_val:.2f} < {confidence})")
#             return None

#     except Exception as e:
#         print(f"Error during OpenCV image matching for '{os.path.basename(button_image_path)}': {e}")
#         return None

# if translation:
#     # process the translation to click the buttons
#     words = translation.split()
#     # remove commas, periods, question marks and exclamation marks from the words
#     words = [word.replace(",", "").replace(".", "").replace("?", "").replace("!", "") for word in words]

#     print(" ")
#     print(f"Words to click: {words}")
#     print(" ")

#     for i in range(len(words)):
#         word = words[i]
#         # Path to the button image
#         button_image_path = f'{word.lower()}.png'

#         # use OpenCV to find button coordinates
#         button_coordinates = find_button_coordinates_opencv("original.png", button_image_path, confidence=0.8)

#         if button_coordinates:
#             x, y = button_coordinates
#             print(f"Moving mouse to coordinates of the button '{word}': x={x}, y={y}")
#             pyautogui.moveTo(x, y, duration=1)
#             pyautogui.click()
#             time.sleep(0.5)

#     # Check
#     pyautogui.moveTo(1433, 936, duration=2)
#     pyautogui.click()
#     time.sleep(0.5)
#     # Continue
#     pyautogui.moveTo(1433, 936, duration=2)
#     pyautogui.click()
#     time.sleep(0.5)
