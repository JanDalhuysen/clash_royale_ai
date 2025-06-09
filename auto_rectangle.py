import cv2
import os

def create_yolo_label(image_path, template_path, class_id, output_dir):
    # Load image and template
    img = cv2.imread(image_path)
    template = cv2.imread(template_path)
    h, w = template.shape[:2]

    # Template matching
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    # Get bounding box coordinates
    x, y = top_left
    width = bottom_right[0] - top_left[0]
    height = bottom_right[1] - top_left[1]

    # Normalize coordinates
    img_h, img_w = img.shape[:2]
    x_center = (x + width / 2) / img_w
    y_center = (y + height / 2) / img_h
    norm_width = width / img_w
    norm_height = height / img_h

    # Create label file
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    label_path = os.path.join(output_dir, base_name + ".txt")
    with open(label_path, "w") as f:
        f.write(f"{class_id} {x_center} {y_center} {norm_width} {norm_height}")

# Example usage:
image_path = "1234.png" # Replace with first sys.argv
template_path = "5678.png" # Replace with second sys.argv
class_id = 0 # Class ID of the object
output_dir = "labels"
os.makedirs(output_dir, exist_ok=True)
create_yolo_label(image_path, template_path, class_id, output_dir)
