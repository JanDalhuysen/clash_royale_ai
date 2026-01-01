import cv2
import numpy as np
import os
import glob

# --- Configuration ---
IMAGE_FOLDER = 'images_to_label'  # Folder containing your game screenshots/images
OUTPUT_LABEL_FOLDER = 'labels'    # Folder where YOLO .txt label files will be saved
# IMAGE_FOLDER = 'ig_synthetic_output/images'
# OUTPUT_LABEL_FOLDER = 'ig_synthetic_output/labels'

troop_e_1 = ['Skeletons', 'ElectroSpirit', 'FireSpirit', 'IceSpirit', 'HealSpirit']
troop_e_2 = ['Goblins', 'SpearGoblins', 'Bomber', 'Bats', 'Zap', 'GiantSnowball', 'Berserker', 'IceGolem', 'SuspiciousBush', 'BarbarianBarrel', 'WallBreakers', 'GoblinCurse', 'Rage', 'TheLog']
troop_e_3 = ['Archers', 'Arrows', 'Knight', 'Minions', 'Cannon', 'GoblinGang', 'SkeletonBarrel', 'Firecracker', 'RoyalDelivery', 'Tombstone', 'MegaMinion', 'DartGoblin', 'Earthquake', 'ElixirGolem', 'GoblinBarrel', 'Guards', 'SkeletonArmy', 'Clone', 'Tornado', 'Void', 'Miner', 'Princess', 'IceWizard', 'RoyalGhost', 'Bandit', 'Fisherman', 'LittlePrince']
troop_e_4 = ['SkeletonDragons', 'Mortar', 'Tesla', 'Fireball', 'MiniPEKKA', 'Musketeer', 'GoblinCage', 'GoblinHut', 'Valkyrie', 'BattleRam', 'BombTower', 'FlyingMachine', 'HogRider', 'BattleHealer', 'Furnace', 'Zappies', 'GoblinDemolisher', 'BabyDragon', 'DarkPrince', 'Freeze', 'Poison', 'RuneGiant', 'Hunter', 'GoblinDrill', 'ElectroWizard', 'InfernoDragon', 'Phoenix', 'MagicArcher', 'Lumberjack', 'NightWitch', 'MotherWitch', 'GoldenKnight', 'SkeletonKing', 'MightyMiner']
troop_e_5 = ['Barbarians', 'MinionHorde', 'Rascals', 'Giant', 'InfernoTower', 'Wizard', 'RoyalHogs', 'Witch', 'Balloon', 'Prince', 'ElectroDragon', 'Bowler', 'Executioner', 'Cannon', 'CannonCart', 'RamRider', 'Graveyard', 'GoblinMachine', 'ArcherQueen', 'Goblinstein', 'Monk']
troop_e_6 = ['RoyalGiant', 'EliteBarbarians', 'Rocket', 'BarbarianHut', 'ElixirCollector', 'GiantSkeleton', 'Lightning', 'GoblinGiant', 'X-Bow', 'Sparky', 'BossBandit']
troop_e_7 = ['RoyalRecruits', 'PEKKA', 'ElectroGiant', 'MegaKnight', 'LavaHound']
troop_e_8 = ['Golem']
troop_e_9 = ['ThreeMusketeers']

card_e_1 = ['SkeletonsCard', 'ElectroSpiritCard', 'FireSpiritCard', 'IceSpiritCard', 'HealSpiritCard']
card_e_2 = ['GoblinsCard', 'SpearGoblinsCard', 'BomberCard', 'BatsCard', 'ZapCard', 'GiantSnowballCard', 'BerserkerCard', 'IceGolemCard', 'SuspiciousBushCard', 'BarbarianBarrelCard', 'WallBreakersCard', 'GoblinCurseCard', 'RageCard', 'TheLogCard']
card_e_3 = ['ArchersCard', 'ArrowsCard', 'KnightCard', 'MinionsCard', 'CannonCard', 'GoblinGangCard', 'SkeletonBarrelCard', 'FirecrackerCard', 'RoyalDeliveryCard', 'TombstoneCard', 'MegaMinionCard', 'DartGoblinCard', 'EarthquakeCard', 'ElixirGolemCard', 'GoblinBarrelCard', 'GuardsCard', 'SkeletonArmyCard', 'CloneCard', 'TornadoCard', 'VoidCard', 'MinerCard', 'PrincessCard', 'IceWizardCard', 'RoyalGhostCard', 'BanditCard', 'FishermanCard', 'LittlePrinceCard']
card_e_4 = ['SkeletonDragonsCard', 'MortarCard', 'TeslaCard', 'FireballCard', 'MiniPEKKACard', 'MusketeerCard', 'GoblinCageCard', 'GoblinHutCard', 'ValkyrieCard', 'BattleRamCard', 'BombTowerCard', 'FlyingMachineCard', 'HogRiderCard', 'BattleHealerCard', 'FurnaceCard', 'ZappiesCard', 'GoblinDemolisherCard', 'BabyDragonCard', 'DarkPrinceCard', 'FreezeCard', 'PoisonCard', 'RuneGiantCard', 'HunterCard', 'GoblinDrillCard', 'ElectroWizardCard', 'InfernoDragonCard', 'PhoenixCard', 'MagicArcherCard', 'LumberjackCard', 'NightWitchCard', 'MotherWitchCard', 'GoldenKnightCard', 'SkeletonKingCard', 'MightyMinerCard']
card_e_5 = ['BarbariansCard', 'MinionHordeCard', 'RascalsCard', 'GiantCard', 'InfernoTowerCard', 'WizardCard', 'RoyalHogsCard', 'WitchCard', 'BalloonCard', 'PrinceCard', 'ElectroDragonCard', 'BowlerCard', 'ExecutionerCard', 'CannonCard', 'CannonCartCard', 'RamRiderCard', 'GraveyardCard', 'GoblinMachineCard', 'ArcherQueenCard', 'GoblinsteinCard', 'MonkCard']
card_e_6 = ['RoyalGiantCard', 'EliteBarbariansCard', 'RocketCard', 'BarbarianHutCard', 'ElixirCollectorCard', 'GiantSkeletonCard', 'LightningCard', 'GoblinGiantCard', 'X-BowCard', 'SparkyCard', 'BossBanditCard']
card_e_7 = ['RoyalRecruitsCard', 'PEKKACard', 'ElectroGiantCard', 'MegaKnightCard', 'LavaHoundCard']
card_e_8 = ['GolemCard']
card_e_9 = ['ThreeMusketeersCard']

# Total cards in original list: 123
# Total matched cards: 117
# Total not matched cards: 6
# Unmatched cards: ['PEKKACard', 'CannonCartCard', 'MirrorCard', 'TowerPrincessCard', 'CannoneerCard', 'DaggerDuchessCard', 'RoyalChefCard']

WINDOW_NAME = 'YOLO Labeling Tool'
BOX_COLOR = (0, 255, 0)  # Green for current box
SAVED_BOX_COLOR = (255, 100, 0) # Blue for saved boxes
TEXT_COLOR = (0, 0, 0) # Black for text
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.7
LINE_THICKNESS = 2

# Folder for touch events
TOUCH_EVENTS_FOLDER = 'touch_events'   # Folder containing the touch event files

# --- Global Variables ---
image_files = []
current_touch_points = []   # List of (x, y) for the current image
current_image_index = 0
current_image = None
display_image = None # Image to draw on (a copy)
current_bboxes = []  # List of {'class_id': int, 'bbox': [x_min, y_min, x_max, y_max]}
drawing = False
ref_point = [] # Stores (x1, y1) of the current drawing box
current_label_set = 'card'  # 'card' or 'troop'
current_elixir_group = 0  # 0-based index for elixir group
current_class_index = 0   # 0-based index within selected elixir group

# --- Elixir Class Arrays ---
CARD_CLASSES = [
    card_e_1,
    card_e_2,
    card_e_3,
    card_e_4,
    card_e_5,
    card_e_6,
    card_e_7,
    card_e_8,
    card_e_9
]
TROOP_CLASSES = [
    troop_e_1,
    troop_e_2,
    troop_e_3,
    troop_e_4,
    troop_e_5,
    troop_e_6,
    troop_e_7,
    troop_e_8,
    troop_e_9
]

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

    # Reset touch points for this image
    current_touch_points.clear()

    # Load touch events if any
    base_name = os.path.splitext(os.path.basename(img_path))[0]
    touch_filepath = os.path.join(TOUCH_EVENTS_FOLDER, base_name + '.txt')
    if os.path.exists(touch_filepath):
        with open(touch_filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    if len(parts) >= 2:
                        try:
                            x = int(parts[0])
                            y = int(parts[1])
                            current_touch_points.append((x, y))
                        except ValueError:
                            print(f"Invalid number in touch event file: {line}")

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
                    # Find which set and elixir group/class this class_id belongs to
                    idx = class_id
                    set_name = 'card'
                    total_card = sum(len(g) for g in CARD_CLASSES)
                    if idx >= total_card:
                        set_name = 'troop'
                        idx -= total_card
                        active_classes = TROOP_CLASSES
                    else:
                        active_classes = CARD_CLASSES
                    group = 0
                    for g, arr in enumerate(active_classes):
                        if idx < len(arr):
                            group = g
                            class_idx = idx
                            break
                        idx -= len(arr)
                    # Note: This only affects display, not current selection
                    current_bboxes.append({'class_id': class_id, 'bbox': [x_min, y_min, x_max, y_max]})
    
    redraw_image()
    return True

def redraw_image():
    """Redraws the image with current bboxes and info text."""
    global display_image, current_image, current_bboxes, current_elixir_group, current_class_index, ref_point, drawing
    if current_image is None:
        return
    display_image = current_image.copy()

    # Draw saved bounding boxes
    for item in current_bboxes:
        class_id = item['class_id']
        idx = class_id
        total_card = sum(len(g) for g in CARD_CLASSES)
        if idx >= total_card:
            idx -= total_card
            active_classes = TROOP_CLASSES
            set_label = 'T'
        else:
            active_classes = CARD_CLASSES
            set_label = 'C'
        for g, arr in enumerate(active_classes):
            if idx < len(arr):
                label_text = f"{set_label}:{arr[idx]}"
                break
            idx -= len(arr)
        else:
            label_text = str(class_id)
        x_min, y_min, x_max, y_max = item['bbox']
        cv2.rectangle(display_image, (x_min, y_min), (x_max, y_max), SAVED_BOX_COLOR, LINE_THICKNESS)
        (w, h), _ = cv2.getTextSize(label_text, FONT, FONT_SCALE, LINE_THICKNESS)
        cv2.rectangle(display_image, (x_min, y_min - h - 5), (x_min + w, y_min -5), SAVED_BOX_COLOR, -1)
        cv2.putText(display_image, label_text, (x_min, y_min - 5), FONT, FONT_SCALE, TEXT_COLOR, LINE_THICKNESS)

    # Draw current drawing box if any
    if drawing and len(ref_point) == 2:
        cv2.rectangle(display_image, ref_point[0], ref_point[1], BOX_COLOR, LINE_THICKNESS)

    # Draw current touch points as red circles
    for pt in current_touch_points:
        cv2.circle(display_image, pt, 5, (0, 0, 255), -1)

    # Display current class and image info
    set_label = 'C' if current_label_set == 'card' else 'T'
    info_text_class = f"[{set_label}] Elixir {current_elixir_group+1} ({current_class_index+1}/{len(get_active_classes()[current_elixir_group])}): {get_current_class_name()}"
    info_text_image = f"Image: {os.path.basename(image_files[current_image_index])} ({current_image_index + 1}/{len(image_files)})"
    info_text_controls = "C/T:Card/Troop | 1-9:Elixir | N/P:Class | S:Save | D:Del | Space:Next | Q:Quit | A:Auto"

    cv2.putText(display_image, info_text_class, (10, 30), FONT, FONT_SCALE, (255,255,255), LINE_THICKNESS+1, cv2.LINE_AA)
    cv2.putText(display_image, info_text_class, (10, 30), FONT, FONT_SCALE, TEXT_COLOR, LINE_THICKNESS, cv2.LINE_AA)

    cv2.putText(display_image, info_text_image, (10, 60), FONT, FONT_SCALE, (255,255,255), LINE_THICKNESS+1, cv2.LINE_AA)
    cv2.putText(display_image, info_text_image, (10, 60), FONT, FONT_SCALE, TEXT_COLOR, LINE_THICKNESS, cv2.LINE_AA)
    
    cv2.putText(display_image, info_text_controls, (10, 90), FONT, FONT_SCALE, (255,255,255), LINE_THICKNESS+1, cv2.LINE_AA)
    cv2.putText(display_image, info_text_controls, (10, 90), FONT, FONT_SCALE, TEXT_COLOR, LINE_THICKNESS, cv2.LINE_AA)


    cv2.imshow(WINDOW_NAME, display_image)

def mouse_callback(event, x, y, flags, param):
    """Handles mouse events for drawing bounding boxes."""
    global ref_point, drawing, current_bboxes, current_elixir_group, current_class_index, display_image

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
            current_bboxes.append({'class_id': get_current_class_id(), 'bbox': [x_min, y_min, x_max, y_max]})
        ref_point = []
        redraw_image()

def get_active_classes():
    return CARD_CLASSES if current_label_set == 'card' else TROOP_CLASSES

def get_current_class_name():
    return get_active_classes()[current_elixir_group][current_class_index]

def get_current_class_id():
    # Unique class id across both sets: card classes first, then troop classes
    offset = 0
    if current_label_set == 'troop':
        offset = sum(len(g) for g in CARD_CLASSES)
    offset += sum(len(g) for g in get_active_classes()[:current_elixir_group])
    return offset + current_class_index

def print_class_ids():
    print("ClassID to Name mapping:")
    class_id = 0
    print("[CARD CLASSES]")
    for group_num, arr in enumerate(CARD_CLASSES, 1):
        print(f"Elixir {group_num}:")
        for name in arr:
            print(f"  {class_id:3d}: {name}")
            class_id += 1
    print("[TROOP CLASSES]")
    for group_num, arr in enumerate(TROOP_CLASSES, 1):
        print(f"Elixir {group_num}:")
        for name in arr:
            print(f"  {class_id:3d}: {name}")
            class_id += 1

def main():
    global image_files, current_image_index, current_bboxes, current_elixir_group, current_class_index, current_label_set
    # print_class_ids()

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
        elif key == ord('c'):
            current_label_set = 'card'
            current_elixir_group = 0
            current_class_index = 0
        elif key == ord('t'):
            current_label_set = 'troop'
            current_elixir_group = 0
            current_class_index = 0
        elif key in [ord(str(i)) for i in range(1,10)]: # 1-9 for elixir group
            new_group = key - ord('1')
            if 0 <= new_group < len(get_active_classes()):
                current_elixir_group = new_group
                current_class_index = 0
        elif key == ord('n'): # Next class in group
            current_class_index = (current_class_index + 1) % len(get_active_classes()[current_elixir_group])
        elif key == ord('p'): # Previous class in group
            current_class_index = (current_class_index - 1 + len(get_active_classes()[current_elixir_group])) % len(get_active_classes()[current_elixir_group])
        elif key == ord('s'): # Save labels
            save_labels()
        elif key == ord('d'): # Delete last bounding box
            if current_bboxes:
                current_bboxes.pop()
        elif key == ord('a'): # Auto-add boxes for touch points
            if current_touch_points:
                # BOX_SIZE = 25  # half box size to get 50x50 box
                BOX_SIZE = 40

                # Get current image size
                img_h, img_w = current_image.shape[:2]
                phone_w, phone_h = 1080, 2400
                scale_x = img_w / phone_w
                scale_y = img_h / phone_h

                for pt in current_touch_points:
                    x_phone, y_phone = pt
                    if y_phone > 2000:
                        # Double box size
                        BOX_SIZE = 50
                    # Map phone coordinates to screenshot coordinates
                    x = int(x_phone * scale_x)
                    y = int(y_phone * scale_y)
                    bbox = [x - BOX_SIZE, y - BOX_SIZE, x + BOX_SIZE, y + BOX_SIZE]
                    current_bboxes.append({'class_id': get_current_class_id(), 'bbox': bbox})
                print(f"Added {len(current_touch_points)} boxes at touch points.")
            else:
                print("No touch points for this image.")
        elif key == ord(' ') or key == 13: # Space or Enter for Next image
            save_labels() # Save current before moving to next
            current_image_index = (current_image_index + 1)
            if current_image_index >= len(image_files):
                print("Reached end of images.")
                current_image_index = len(image_files) -1 # Stay on last image or handle as desired
            if not load_image_and_labels(current_image_index):
                if current_image_index >= len(image_files):
                    break
                else:
                    print(f"Skipping problematic image {image_files[current_image_index]}")
                    current_image_index = (current_image_index + 1)
                    if current_image_index >= len(image_files):
                        break
                    load_image_and_labels(current_image_index)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
