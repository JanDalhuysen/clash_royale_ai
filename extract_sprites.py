# extract_sprites.py
import cv2
import numpy as np
import os

def extract_sprites_from_sheet(sheet_path, output_dir, character_name):
    """
    Extracts individual sprites from a sprite sheet and saves them as transparent PNGs.
    """
    # Create character-specific output directory
    char_output_dir = os.path.join(output_dir, character_name)
    os.makedirs(char_output_dir, exist_ok=True)

    # Load the image with unchanged flag to preserve alpha channel if present
    img = cv2.imread(sheet_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"Error: Could not load image at {sheet_path}")
        return

    # --- Step 1: Create a mask to separate sprites from background ---
    if img.shape[2] == 4:  # PNG with alpha channel
        # Use the alpha channel as the mask
        alpha = img[:, :, 3]
        _, mask = cv2.threshold(alpha, 0, 255, cv2.THRESH_BINARY)
        img_bgr = img[:, :, :3]
    else:
        # Fallback for images without alpha channel (original method)
        img_bgr = img
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    # --- Step 2: Find contours of each sprite ---
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    print(f"Found {len(contours)} potential sprites for '{character_name}'.")
    
    sprite_count = 0
    for i, contour in enumerate(contours):
        # --- Step 3: Filter out small noise or giant contours ---
        area = cv2.contourArea(contour)
        # if area < 400 or area > (img.shape[0] * img.shape[1] * 0.9): # Ignore tiny noise and huge areas
        if area < 2500 or area > 3500: # Ignore tiny noise and huge areas
            continue

        x, y, w, h = cv2.boundingRect(contour)
        cropped_bgr = img_bgr[y:y+h, x:x+w]
        cropped_mask = mask[y:y+h, x:x+w]

        # Create a blank mask for the cropped region
        contour_mask = np.zeros((h, w), dtype=np.uint8)
        # Shift contour coordinates to the cropped region
        shifted_contour = contour - [x, y]
        cv2.drawContours(contour_mask, [shifted_contour], -1, 255, thickness=cv2.FILLED)

        # Combine with alpha if needed
        cropped_bgra = cv2.cvtColor(cropped_bgr, cv2.COLOR_BGR2BGRA)
        cropped_bgra[:, :, 3] = contour_mask

        output_path = os.path.join(char_output_dir, f"{sprite_count}.png")
        cv2.imwrite(output_path, cropped_bgra)
        sprite_count += 1
        
    print(f"Successfully extracted and saved {sprite_count} sprites to '{char_output_dir}'")

if __name__ == '__main__':
    SPRITE_SHEET_DIR = 'ig_sprite_sheets'
    OUTPUT_SPRITE_DIR = 'ig_extracted_sprites'

    # Process all images in the sprite sheet directory
    for filename in os.listdir(SPRITE_SHEET_DIR):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            character_name = os.path.splitext(filename)[0]
            sheet_path = os.path.join(SPRITE_SHEET_DIR, filename)
            print(f"\nProcessing {sheet_path}...")
            extract_sprites_from_sheet(sheet_path, OUTPUT_SPRITE_DIR, character_name)
