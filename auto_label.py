import os
import cv2
from pathlib import Path

def create_yolo_label(img, template_path, class_id, output_path, confidence_threshold=0.2, scale_steps=10):
    """Create YOLO label file using multi-scale template matching."""
    template = cv2.imread(template_path)
    if template is None:
        print(f"Error: Could not load template {template_path}")
        return []
    
    # Get original template dimensions
    h, w = template.shape[:2]
    
    # Try different scales
    best_match = None
    best_max_val = -1
    for scale in range(scale_steps + 1):
        # Calculate current scale factor
        scale_factor = 1.5 - (scale * (1.0 / scale_steps))  # Try scales from 150% down to 50%
        # Resize template
        resized_template = cv2.resize(template, None, fx=scale_factor, fy=scale_factor)
        th, tw = resized_template.shape[:2]
        
        # Skip if template is larger than image
        if tw > img.shape[1] or th > img.shape[0]:
            continue
            
        # Template matching
        result = cv2.matchTemplate(img, resized_template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        # Keep track of best match across all scales
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
        img_h, img_w = img.shape[:2]
        x_center = (x + width / 2) / img_w
        y_center = (y + height / 2) / img_h
        norm_width = width / img_w
        norm_height = height / img_h
        
        return [(class_id, x_center, y_center, norm_width, norm_height)]
    
    return []

def main():
    """Main function to process images and generate labels."""
    images_dir = "images_to_label"
    templates_dir = "templates"
    output_dir = "labels"
    
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(exist_ok=True)
    
    # Get list of all template files
    template_files = [f for f in os.listdir(templates_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    # Sort files for consistent class IDs
    template_files.sort()
    
    # Process each image
    for image_file in os.listdir(images_dir):
        if not image_file.endswith(('.png', '.jpg', '.jpeg')):
            continue
            
        image_path = os.path.join(images_dir, image_file)
        img = cv2.imread(image_path)
        
        if img is None:
            print(f"Error: Could not load image {image_path}")
            continue
            
        all_boxes = []
        
        # Match against all templates
        for class_id, template_file in enumerate(template_files):
            template_path = os.path.join(templates_dir, template_file)
            boxes = create_yolo_label(img, template_path, class_id, output_dir)
            all_boxes.extend(boxes)
        
        # Write all boxes to label file
        base_name = os.path.splitext(image_file)[0]
        label_path = os.path.join(output_dir, base_name + ".txt")
        
        with open(label_path, "w") as f:
            for box in all_boxes:
                f.write(" ".join(map(str, box)) + "\n")
                
        print(f"Processed {image_file}, found {len(all_boxes)} cards")

if __name__ == "__main__":
    main()
