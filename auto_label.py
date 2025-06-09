import os
import cv2
from pathlib import Path

# class IDs
card_e_1 = ['SkeletonsCard', 'ElectroSpiritCard', 'FireSpiritCard', 'IceSpiritCard', 'HealSpiritCard']
card_e_2 = ['GoblinsCard', 'SpearGoblinsCard', 'BomberCard', 'BatsCard', 'ZapCard', 'GiantSnowballCard', 'BerserkerCard', 'IceGolemCard', 'SuspiciousBushCard', 'BarbarianBarrelCard', 'WallBreakersCard', 'GoblinCurseCard', 'RageCard', 'TheLogCard']
card_e_3 = ['ArchersCard', 'ArrowsCard', 'KnightCard', 'MinionsCard', 'CannonCard', 'GoblinGangCard', 'SkeletonBarrelCard', 'FirecrackerCard', 'RoyalDeliveryCard', 'TombstoneCard', 'MegaMinionCard', 'DartGoblinCard', 'EarthquakeCard', 'ElixirGolemCard', 'GoblinBarrelCard', 'GuardsCard', 'SkeletonArmyCard', 'CloneCard', 'TornadoCard', 'VoidCard', 'MinerCard', 'PrincessCard', 'IceWizardCard', 'RoyalGhostCard', 'BanditCard', 'FishermanCard', 'LittlePrinceCard']
card_e_4 = ['SkeletonDragonsCard', 'MortarCard', 'TeslaCard', 'FireballCard', 'MiniPEKKACard', 'MusketeerCard', 'GoblinCageCard', 'GoblinHutCard', 'ValkyrieCard', 'BattleRamCard', 'BombTowerCard', 'FlyingMachineCard', 'HogRiderCard', 'BattleHealerCard', 'FurnaceCard', 'ZappiesCard', 'GoblinDemolisherCard', 'BabyDragonCard', 'DarkPrinceCard', 'FreezeCard', 'PoisonCard', 'RuneGiantCard', 'HunterCard', 'GoblinDrillCard', 'ElectroWizardCard', 'InfernoDragonCard', 'PhoenixCard', 'MagicArcherCard', 'LumberjackCard', 'NightWitchCard', 'MotherWitchCard', 'GoldenKnightCard', 'SkeletonKingCard', 'MightyMinerCard']
card_e_5 = ['BarbariansCard', 'MinionHordeCard', 'RascalsCard', 'GiantCard', 'InfernoTowerCard', 'WizardCard', 'RoyalHogsCard', 'WitchCard', 'BalloonCard', 'PrinceCard', 'ElectroDragonCard', 'BowlerCard', 'ExecutionerCard', 'CannonCard', 'CannonCartCard', 'RamRiderCard', 'GraveyardCard', 'GoblinMachineCard', 'ArcherQueenCard', 'GoblinsteinCard', 'MonkCard']
card_e_6 = ['RoyalGiantCard', 'EliteBarbariansCard', 'RocketCard', 'BarbarianHutCard', 'ElixirCollectorCard', 'GiantSkeletonCard', 'LightningCard', 'GoblinGiantCard', 'X-BowCard', 'SparkyCard', 'BossBanditCard']
card_e_7 = ['RoyalRecruitsCard', 'PEKKACard', 'ElectroGiantCard', 'MegaKnightCard', 'LavaHoundCard']
card_e_8 = ['GolemCard']
card_e_9 = ['ThreeMusketeersCard']


# Function to get all class IDs in the correct order
def get_ordered_class_ids():
    """Get all class IDs in the correct order from card_e_* lists."""
    all_class_ids = []
    
    # Add cards in order from elixir cost 1 to 9
    all_class_ids.extend(card_e_1)
    all_class_ids.extend(card_e_2)
    all_class_ids.extend(card_e_3)
    all_class_ids.extend(card_e_4)
    all_class_ids.extend(card_e_5)
    all_class_ids.extend(card_e_6)
    all_class_ids.extend(card_e_7)
    all_class_ids.extend(card_e_8)
    all_class_ids.extend(card_e_9)
    
    return all_class_ids

def create_yolo_label(img, template_path, class_id, output_dir, confidence_threshold=0.6, scale_steps=10, box_scale_factor=0.55):
    """Create YOLO label file using multi-scale template matching.
    
    Args:
        img: The image to process
        template_path: Path to the template image
        class_id: Class ID for the label
        output_dir: Output directory for labels
        confidence_threshold: Minimum confidence for a valid match
        scale_steps: Number of different scales to try
        box_scale_factor: Factor to scale the final bounding box (default 0.55 = 55% of original size)
    """
    template = cv2.imread(template_path)
    if template is None:
        print(f"Error: Could not load template {template_path}")
        return []
    
    # Get original template dimensions
    h, w = template.shape[:2]
    
    # Try different scales
    best_match = None
    best_max_val = -1
    for scale in range(1, scale_steps + 1):
        # Calculate current scale factor
        scale_factor = 1.5 - ((scale - 1) * (0.5 / (scale_steps - 1)))  # Try scales from 150% down to 100%
        
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
        print(f"Matched {os.path.basename(template_path)} with confidence {best_max_val:.2f} at scale {best_match[3]:.2f}")
        top_left, tw, th, scale_factor = best_match
        bottom_right = (top_left[0] + tw, top_left[1] + th)
        
        # Get bounding box coordinates
        x, y = top_left
        width = bottom_right[0] - top_left[0]
        height = bottom_right[1] - top_left[1]
        
        # Calculate center of the bounding box
        center_x = x + width / 2
        center_y = y + height / 2
        
        # Apply the box scale factor to make the box smaller
        scaled_width = width# * (box_scale_factor+0.2)
        scaled_height = height * box_scale_factor
        
        # Normalize coordinates
        img_h, img_w = img.shape[:2]
        x_center = center_x / img_w
        y_center = center_y / img_h
        norm_width = scaled_width / img_w
        norm_height = scaled_height / img_h
        
        return [(class_id, x_center, y_center, norm_width, norm_height)]
    
    return []

def main():
    """Main function to process images and generate labels."""
    images_dir = "images_to_label"
    templates_dir = "templates"
    output_dir = "labels"
    
    # Configuration parameters
    confidence_threshold = 0.65  # Minimum confidence for a valid match
    scale_steps = 5
    box_scale_factor = 0.55  # 55% of the original bounding box size
    
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(exist_ok=True)
    
    # Get ordered list of all class IDs
    ordered_class_ids = get_ordered_class_ids()
    
    # Get all template files from the templates directory
    template_files = [f for f in os.listdir(templates_dir) 
                     if f.endswith(('.png', '.jpg', '.jpeg'))]
    
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
        
        # Match against all templates in the templates directory
        for template_file in template_files:
            template_path = os.path.join(templates_dir, template_file)
            
            # Extract card name from template filename (assuming filename format is CardName.png)
            card_name = os.path.splitext(template_file)[0]
              # Find the class ID for this card in the ordered list
            if card_name in ordered_class_ids:
                class_id = ordered_class_ids.index(card_name)
                
                # Try to match this template
                boxes = create_yolo_label(img, template_path, class_id, output_dir, 
                                         confidence_threshold=confidence_threshold,
                                         scale_steps=scale_steps,
                                         box_scale_factor=box_scale_factor)
                all_boxes.extend(boxes)
            # else:
                # print(f"Warning: Card name {card_name} not found in class IDs list")
        
        # Write all boxes to label file
        base_name = os.path.splitext(image_file)[0]
        label_path = os.path.join(output_dir, base_name + ".txt")
        
        with open(label_path, "w") as f:
            for box in all_boxes:
                f.write(" ".join(map(str, box)) + "\n")
                
        print(f"Processed {image_file}, found {len(all_boxes)} cards")

if __name__ == "__main__":
    main()
