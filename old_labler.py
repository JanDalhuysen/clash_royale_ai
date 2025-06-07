import cv2
import numpy as np
import os
import glob

# --- Configuration ---
IMAGE_FOLDER = 'images_to_label'  # Folder containing your game screenshots/images
OUTPUT_LABEL_FOLDER = 'labels'    # Folder where YOLO .txt label files will be saved

# Card: card in current hand
# Troop: troop that has been placed

# Current deck
CLASS_NAMES = [
"BabyDragonCard",
"GoblinBarrelCard",
"MinerCard",
"MusketeerCard",
"RamRiderCard",
"SkeletonArmyCard",
"SpearGoblinsCard",
"WitchCard",
"BabyDragon",
"GoblinBarrel",
"Miner",
"Musketeer",
"RamRider",
"SkeletonArmy",
"SpearGoblins",
"Witch"
]

WINDOW_NAME = 'YOLO Labeling Tool'
BOX_COLOR = (0, 255, 0)  # Green for current box
SAVED_BOX_COLOR = (255, 100, 0) # Blue for saved boxes
TEXT_COLOR = (0, 0, 0) # Black for text
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.7
LINE_THICKNESS = 2

# --- Global Variables ---
image_files = []
current_image_index = 0
current_image = None
display_image = None # Image to draw on (a copy)
current_bboxes = []  # List of {'class_id': int, 'bbox': [x_min, y_min, x_max, y_max]}
drawing = False
ref_point = [] # Stores (x1, y1) of the current drawing box
current_class_id = 0

def get_image_paths(folder):
    """Gets all jpg, png, jpeg image paths from a folder."""
    patterns = ['*.jpg', '*.jpeg', '*.png']
    paths = []
    for pattern in patterns:
        paths.extend(glob.glob(os.path.join(folder, pattern)))
    return sorted(paths)

def yolo_format(class_id, bbox, img_width, img_height):
    """Converts bbox [x_min, y_min, x_max, y_max] to YOLO format."""
    x_min, y_min, x_max, y_max = bbox
    dw = 1. / img_width
    dh = 1. / img_height
    x_center = (x_min + x_max) / 2.0
    y_center = (y_min + y_max) / 2.0
    w = x_max - x_min
    h = y_max - y_min

    x_center_norm = x_center * dw
    y_center_norm = y_center * dh
    w_norm = w * dw
    h_norm = h * dh
    return f"{class_id} {x_center_norm:.6f} {y_center_norm:.6f} {w_norm:.6f} {h_norm:.6f}\n"

def save_labels():
    """Saves current_bboxes to a .txt file in YOLO format."""
    global current_image_index, image_files, current_bboxes, OUTPUT_LABEL_FOLDER
    if not current_bboxes or current_image_index >= len(image_files):
        print("No bounding boxes to save or no image loaded.")
        return

    img_path = image_files[current_image_index]
    img_filename = os.path.basename(img_path)
    label_filename = os.path.splitext(img_filename)[0] + '.txt'
    label_filepath = os.path.join(OUTPUT_LABEL_FOLDER, label_filename)

    if current_image is None:
        print("Error: current_image is not loaded. Cannot get dimensions.")
        return
        
    img_height, img_width = current_image.shape[:2]

    with open(label_filepath, 'w') as f:
        for item in current_bboxes:
            yolo_line = yolo_format(item['class_id'], item['bbox'], img_width, img_height)
            f.write(yolo_line)
    print(f"Labels saved to: {label_filepath}")

def load_image_and_labels(index):
    """Loads image and its existing labels if any."""
    global current_image, display_image, current_bboxes, image_files, OUTPUT_LABEL_FOLDER
    if index >= len(image_files):
        print("No more images.")
        return False

    img_path = image_files[index]
    current_image = cv2.imread(img_path)
    if current_image is None:
        print(f"Error loading image: {img_path}")
        return False
    
    display_image = current_image.copy()
    current_bboxes = [] # Reset bboxes for the new image

    # Load existing labels for this image if they exist
    img_filename = os.path.basename(img_path)
    label_filename = os.path.splitext(img_filename)[0] + '.txt'
    label_filepath = os.path.join(OUTPUT_LABEL_FOLDER, label_filename)

    if os.path.exists(label_filepath):
        print(f"Loading existing labels from: {label_filepath}")
        img_h, img_w = current_image.shape[:2]
        with open(label_filepath, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 5:
                    class_id = int(parts[0])
                    x_center_norm = float(parts[1])
                    y_center_norm = float(parts[2])
                    w_norm = float(parts[3])
                    h_norm = float(parts[4])

                    # Convert YOLO format back to x_min, y_min, x_max, y_max
                    box_w = w_norm * img_w
                    box_h = h_norm * img_h
                    x_center = x_center_norm * img_w
                    y_center = y_center_norm * img_h

                    x_min = int(x_center - (box_w / 2))
                    y_min = int(y_center - (box_h / 2))
                    x_max = int(x_center + (box_w / 2))
                    y_max = int(y_center + (box_h / 2))
                    
                    current_bboxes.append({'class_id': class_id, 'bbox': [x_min, y_min, x_max, y_max]})
    
    redraw_image()
    return True

def redraw_image():
    """Redraws the image with current bboxes and info text."""
    global display_image, current_image, current_bboxes, current_class_id, ref_point, drawing
    if current_image is None:
        return
    display_image = current_image.copy()

    # Draw saved bounding boxes
    for item in current_bboxes:
        class_id = item['class_id']
        x_min, y_min, x_max, y_max = item['bbox']
        cv2.rectangle(display_image, (x_min, y_min), (x_max, y_max), SAVED_BOX_COLOR, LINE_THICKNESS)
        label_text = CLASS_NAMES[class_id]
        (w, h), _ = cv2.getTextSize(label_text, FONT, FONT_SCALE, LINE_THICKNESS)
        cv2.rectangle(display_image, (x_min, y_min - h - 5), (x_min + w, y_min -5), SAVED_BOX_COLOR, -1)
        cv2.putText(display_image, label_text, (x_min, y_min - 5), FONT, FONT_SCALE, TEXT_COLOR, LINE_THICKNESS)

    # Draw current drawing box if any
    if drawing and len(ref_point) == 2:
        cv2.rectangle(display_image, ref_point[0], ref_point[1], BOX_COLOR, LINE_THICKNESS)

    # Display current class and image info
    info_text_class = f"Current Class ({current_class_id}): {CLASS_NAMES[current_class_id]}"
    info_text_image = f"Image: {os.path.basename(image_files[current_image_index])} ({current_image_index + 1}/{len(image_files)})"
    info_text_controls = "N/P:Class | S:Save | D:Del | Space:Next | Q:Quit"

    cv2.putText(display_image, info_text_class, (10, 30), FONT, FONT_SCALE, (255,255,255), LINE_THICKNESS+1, cv2.LINE_AA)
    cv2.putText(display_image, info_text_class, (10, 30), FONT, FONT_SCALE, TEXT_COLOR, LINE_THICKNESS, cv2.LINE_AA)

    cv2.putText(display_image, info_text_image, (10, 60), FONT, FONT_SCALE, (255,255,255), LINE_THICKNESS+1, cv2.LINE_AA)
    cv2.putText(display_image, info_text_image, (10, 60), FONT, FONT_SCALE, TEXT_COLOR, LINE_THICKNESS, cv2.LINE_AA)
    
    cv2.putText(display_image, info_text_controls, (10, 90), FONT, FONT_SCALE, (255,255,255), LINE_THICKNESS+1, cv2.LINE_AA)
    cv2.putText(display_image, info_text_controls, (10, 90), FONT, FONT_SCALE, TEXT_COLOR, LINE_THICKNESS, cv2.LINE_AA)


    cv2.imshow(WINDOW_NAME, display_image)

def mouse_callback(event, x, y, flags, param):
    """Handles mouse events for drawing bounding boxes."""
    global ref_point, drawing, current_bboxes, current_class_id, display_image

    if event == cv2.EVENT_LBUTTONDOWN:
        ref_point = [(x, y)]
        drawing = True
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            ref_point.append((x, y)) # Store current mouse position as the second point
            temp_display = display_image.copy() # Use a copy for temporary drawing
            cv2.rectangle(temp_display, ref_point[0], (x,y) , BOX_COLOR, LINE_THICKNESS)
            cv2.imshow(WINDOW_NAME, temp_display)
            ref_point.pop() # Remove the temporary second point
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        ref_point.append((x, y))

        # Ensure x_min < x_max and y_min < y_max
        x_min = min(ref_point[0][0], ref_point[1][0])
        y_min = min(ref_point[0][1], ref_point[1][1])
        x_max = max(ref_point[0][0], ref_point[1][0])
        y_max = max(ref_point[0][1], ref_point[1][1])
        
        # Ignore very small boxes
        if (x_max - x_min) > 5 and (y_max - y_min) > 5:
            current_bboxes.append({'class_id': current_class_id, 'bbox': [x_min, y_min, x_max, y_max]})
        ref_point = []
        redraw_image()

def main():
    global image_files, current_image_index, current_class_id, current_bboxes

    # Create output directory if it doesn't exist
    if not os.path.exists(IMAGE_FOLDER):
        print(f"Error: Image folder '{IMAGE_FOLDER}' not found.")
        print("Please create it and add images, or change the IMAGE_FOLDER variable.")
        return
    if not os.path.exists(OUTPUT_LABEL_FOLDER):
        os.makedirs(OUTPUT_LABEL_FOLDER)
        print(f"Created output label folder: {OUTPUT_LABEL_FOLDER}")

    image_files = get_image_paths(IMAGE_FOLDER)
    if not image_files:
        print(f"No images found in {IMAGE_FOLDER}. Exiting.")
        return

    cv2.namedWindow(WINDOW_NAME)
    cv2.setMouseCallback(WINDOW_NAME, mouse_callback)

    if not load_image_and_labels(current_image_index):
        return # Exit if first image fails to load

    while True:
        redraw_image() # Ensure display is up-to-date
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'): # Quit
            break
        elif key == ord('n'): # Next class
            current_class_id = (current_class_id + 1) % len(CLASS_NAMES)
        elif key == ord('p'): # Previous class
            current_class_id = (current_class_id - 1 + len(CLASS_NAMES)) % len(CLASS_NAMES)
        elif key == ord('s'): # Save labels
            save_labels()
        elif key == ord('d'): # Delete last bounding box
            if current_bboxes:
                current_bboxes.pop()
        elif key == ord(' ') or key == 13: # Space or Enter for Next image
            save_labels() # Save current before moving to next
            current_image_index = (current_image_index + 1)
            if current_image_index >= len(image_files):
                print("Reached end of images.")
                current_image_index = len(image_files) -1 # Stay on last image or handle as desired
                # Or break if you want to quit after last image
                # break 
            if not load_image_and_labels(current_image_index):
                if current_image_index >= len(image_files): # If loading failed because it's past the end
                    break
                else: # If loading failed for other reasons, try to go to next valid one
                    print(f"Skipping problematic image {image_files[current_image_index]}")
                    current_image_index = (current_image_index + 1)
                    if current_image_index >= len(image_files):
                        break
                    load_image_and_labels(current_image_index)


    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
