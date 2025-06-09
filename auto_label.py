import os
import cv2
from pathlib import Path

def create_yolo_label(img, template_path, class_id, output_path, confidence_threshold=0.8):
    """Create YOLO label file using template matching."""
    template = cv2.imread(template_path)
    if template is None:
        print(f"Error: Could not load template {template_path}")
        return []
    
    h, w = template.shape[:2]
    
    # Template matching
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    if max_val >= confidence_threshold:
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
