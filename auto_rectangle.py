import cv2
import os


def create_yolo_label(
    image_path,
    template_path,
    class_id,
    output_dir,
    confidence_threshold=0.2,
    scale_steps=10,
):
    # Load image and template
    img = cv2.imread(image_path)
    template = cv2.imread(template_path)
    h, w = template.shape[:2]

    # Get original image dimensions
    img_h, img_w = img.shape[:2]

    best_match = None
    best_max_val = -1

    # Try different scales
    for scale in range(1, scale_steps + 1):
        # Calculate current scale factor
        scale_factor = 1 - (scale * 0.05)  # Try scales from 100% down to 50% (0.05 * 10 = 0.5)

        # Resize template
        resized_template = cv2.resize(template, None, fx=scale_factor, fy=scale_factor)
        th, tw = resized_template.shape[:2]

        # Skip if template is larger than image
        if tw > img_w or th > img_h:
            continue

        # Template matching
        result = cv2.matchTemplate(img, resized_template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Keep track of best match
        if max_val > best_max_val:
            best_max_val = max_val
            best_match = (max_loc, tw, th, scale_factor)

    # If we found a good match
    if best_match and best_max_val >= confidence_threshold:
        top_left, tw, th, scale_factor = best_match
        bottom_right = (top_left[0] + tw, top_left[1] + th)

        # Get bounding box coordinates
        x, y = top_left
        width = bottom_right[0] - top_left[0]
        height = bottom_right[1] - top_left[1]

        # Normalize coordinates
        x_center = (x + width / 2) / img_w
        y_center = (y + height / 2) / img_h
        norm_width = width / img_w
        norm_height = height / img_h

        # Create label file
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        label_path = os.path.join(output_dir, base_name + ".txt")
        with open(label_path, "w") as f:
            f.write(f"{class_id} {x_center} {y_center} {norm_width} {norm_height}")

        print(f"Matched {os.path.basename(template_path)} in {image_path} with confidence {best_max_val:.2f} at scale {scale_factor:.2f}")
        return True

    print(f"No match found for {template_path} in {image_path}")
    return False


# Example usage:
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print("Usage: python auto_rectangle.py <image_path> <template_path> <class_id>")
        sys.exit(1)

    image_path = sys.argv[1]
    template_path = sys.argv[2]
    class_id = int(sys.argv[3])
    output_dir = "labels"
    os.makedirs(output_dir, exist_ok=True)

    success = create_yolo_label(image_path, template_path, class_id, output_dir)
    sys.exit(0 if success else 1)
