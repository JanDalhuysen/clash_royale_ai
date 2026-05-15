import cv2
import numpy as np
import os
import glob
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# --- Configuration ---
IMAGE_FOLDER = "images_to_label"  # Folder containing your game screenshots/images
OUTPUT_LABEL_FOLDER = "labels"  # Folder where YOLO .txt label files will be saved
TEMPLATES_FOLDER = "templates"  # Folder with card images
# IMAGE_FOLDER = 'ig_synthetic_output/images'
# OUTPUT_LABEL_FOLDER = 'ig_synthetic_output/labels'

troop_e_1 = [
    "Skeletons",
    "ElectroSpirit",
    "FireSpirit",
    "IceSpirit",
    "HealSpirit",
]
troop_e_2 = [
    "Goblins",
    "SpearGoblins",
    "Bomber",
    "Bats",
    "Zap",
    "GiantSnowball",
    "Berserker",
    "IceGolem",
    "SuspiciousBush",
    "BarbarianBarrel",
    "WallBreakers",
    "GoblinCurse",
    "Rage",
    "TheLog",
]
troop_e_3 = [
    "Archers",
    "Arrows",
    "Knight",
    "Minions",
    "Cannon",
    "GoblinGang",
    "SkeletonBarrel",
    "Firecracker",
    "RoyalDelivery",
    "Tombstone",
    "MegaMinion",
    "DartGoblin",
    "Earthquake",
    "ElixirGolem",
    "GoblinBarrel",
    "Guards",
    "SkeletonArmy",
    "Clone",
    "Tornado",
    "Void",
    "Miner",
    "Princess",
    "IceWizard",
    "RoyalGhost",
    "Bandit",
    "Fisherman",
    "LittlePrince",
]
troop_e_4 = [
    "SkeletonDragons",
    "Mortar",
    "Tesla",
    "Fireball",
    "MiniPEKKA",
    "Musketeer",
    "GoblinCage",
    "GoblinHut",
    "Valkyrie",
    "BattleRam",
    "BombTower",
    "FlyingMachine",
    "HogRider",
    "BattleHealer",
    "Furnace",
    "Zappies",
    "GoblinDemolisher",
    "BabyDragon",
    "DarkPrince",
    "Freeze",
    "Poison",
    "RuneGiant",
    "Hunter",
    "GoblinDrill",
    "ElectroWizard",
    "InfernoDragon",
    "Phoenix",
    "MagicArcher",
    "Lumberjack",
    "NightWitch",
    "MotherWitch",
    "GoldenKnight",
    "SkeletonKing",
    "MightyMiner",
]
troop_e_5 = [
    "Barbarians",
    "MinionHorde",
    "Rascals",
    "Giant",
    "InfernoTower",
    "Wizard",
    "RoyalHogs",
    "Witch",
    "Balloon",
    "Prince",
    "ElectroDragon",
    "Bowler",
    "Executioner",
    "Cannon",
    "CannonCart",
    "RamRider",
    "Graveyard",
    "GoblinMachine",
    "ArcherQueen",
    "Goblinstein",
    "Monk",
]
troop_e_6 = [
    "RoyalGiant",
    "EliteBarbarians",
    "Rocket",
    "BarbarianHut",
    "ElixirCollector",
    "GiantSkeleton",
    "Lightning",
    "GoblinGiant",
    "X-Bow",
    "Sparky",
    "BossBandit",
]
troop_e_7 = [
    "RoyalRecruits",
    "PEKKA",
    "ElectroGiant",
    "MegaKnight",
    "LavaHound",
]
troop_e_8 = ["Golem"]
troop_e_9 = ["ThreeMusketeers"]

card_e_1 = [
    "SkeletonsCard",
    "ElectroSpiritCard",
    "FireSpiritCard",
    "IceSpiritCard",
    "HealSpiritCard",
]
card_e_2 = [
    "GoblinsCard",
    "SpearGoblinsCard",
    "BomberCard",
    "BatsCard",
    "ZapCard",
    "GiantSnowballCard",
    "BerserkerCard",
    "IceGolemCard",
    "SuspiciousBushCard",
    "BarbarianBarrelCard",
    "WallBreakersCard",
    "GoblinCurseCard",
    "RageCard",
    "TheLogCard",
]
card_e_3 = [
    "ArchersCard",
    "ArrowsCard",
    "KnightCard",
    "MinionsCard",
    "CannonCard",
    "GoblinGangCard",
    "SkeletonBarrelCard",
    "FirecrackerCard",
    "RoyalDeliveryCard",
    "TombstoneCard",
    "MegaMinionCard",
    "DartGoblinCard",
    "EarthquakeCard",
    "ElixirGolemCard",
    "GoblinBarrelCard",
    "GuardsCard",
    "SkeletonArmyCard",
    "CloneCard",
    "TornadoCard",
    "VoidCard",
    "MinerCard",
    "PrincessCard",
    "IceWizardCard",
    "RoyalGhostCard",
    "BanditCard",
    "FishermanCard",
    "LittlePrinceCard",
]
card_e_4 = [
    "SkeletonDragonsCard",
    "MortarCard",
    "TeslaCard",
    "FireballCard",
    "MiniPEKKACard",
    "MusketeerCard",
    "GoblinCageCard",
    "GoblinHutCard",
    "ValkyrieCard",
    "BattleRamCard",
    "BombTowerCard",
    "FlyingMachineCard",
    "HogRiderCard",
    "BattleHealerCard",
    "FurnaceCard",
    "ZappiesCard",
    "GoblinDemolisherCard",
    "BabyDragonCard",
    "DarkPrinceCard",
    "FreezeCard",
    "PoisonCard",
    "RuneGiantCard",
    "HunterCard",
    "GoblinDrillCard",
    "ElectroWizardCard",
    "InfernoDragonCard",
    "PhoenixCard",
    "MagicArcherCard",
    "LumberjackCard",
    "NightWitchCard",
    "MotherWitchCard",
    "GoldenKnightCard",
    "SkeletonKingCard",
    "MightyMinerCard",
]
card_e_5 = [
    "BarbariansCard",
    "MinionHordeCard",
    "RascalsCard",
    "GiantCard",
    "InfernoTowerCard",
    "WizardCard",
    "RoyalHogsCard",
    "WitchCard",
    "BalloonCard",
    "PrinceCard",
    "ElectroDragonCard",
    "BowlerCard",
    "ExecutionerCard",
    "CannonCard",
    "CannonCartCard",
    "RamRiderCard",
    "GraveyardCard",
    "GoblinMachineCard",
    "ArcherQueenCard",
    "GoblinsteinCard",
    "MonkCard",
]
card_e_6 = [
    "RoyalGiantCard",
    "EliteBarbariansCard",
    "RocketCard",
    "BarbarianHutCard",
    "ElixirCollectorCard",
    "GiantSkeletonCard",
    "LightningCard",
    "GoblinGiantCard",
    "X-BowCard",
    "SparkyCard",
    "BossBanditCard",
]
card_e_7 = [
    "RoyalRecruitsCard",
    "PEKKACard",
    "ElectroGiantCard",
    "MegaKnightCard",
    "LavaHoundCard",
]
card_e_8 = ["GolemCard"]
card_e_9 = ["ThreeMusketeersCard"]

WINDOW_NAME = "YOLO Labeling Tool"
BOX_COLOR = (0, 255, 0)  # Green for current box
# SAVED_BOX_COLOR = (255, 100, 0)  # Blue for saved boxes
SAVED_BOX_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)  # Black for text
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.5
LINE_THICKNESS = 2

# Folder for touch events
TOUCH_EVENTS_FOLDER = "touch_events"  # Folder containing the touch event files

# --- Global Variables ---
image_files = []
current_touch_points = []  # List of (x, y) for the current image
current_image_index = 0
current_image = None
display_image = None  # Image to draw on (a copy)
current_bboxes = []  # List of {'class_id': int, 'bbox': [x_min, y_min, x_max, y_max]}
drawing = False
ref_point = []  # Stores (x1, y1) of the current drawing box
selected_class_id = 0  # Currently selected class ID for labeling

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
    card_e_9,
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
    troop_e_9,
]

# GUI Elements
root = None
card_buttons = {}  # Store references to card buttons
card_frames = {}  # Store references to card frames for highlighting
card_images_tk = {}  # Store PhotoImage references
image_info_label = None


def get_image_paths(folder):
    """Gets all jpg, png, jpeg image paths from a folder."""
    patterns = ["*.jpg", "*.jpeg", "*.png"]
    paths = []
    for pattern in patterns:
        paths.extend(glob.glob(os.path.join(folder, pattern)))
    return sorted(paths)


def yolo_format(class_id, bbox, img_width, img_height):
    """Converts bbox [x_min, y_min, x_max, y_max] to YOLO format."""
    x_min, y_min, x_max, y_max = bbox
    dw = 1.0 / img_width
    dh = 1.0 / img_height
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
    label_filename = os.path.splitext(img_filename)[0] + ".txt"
    label_filepath = os.path.join(OUTPUT_LABEL_FOLDER, label_filename)

    if current_image is None:
        print("Error: current_image is not loaded. Cannot get dimensions.")
        return

    img_height, img_width = current_image.shape[:2]

    with open(label_filepath, "w") as f:
        for item in current_bboxes:
            yolo_line = yolo_format(item["class_id"], item["bbox"], img_width, img_height)
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
    current_bboxes = []  # Reset bboxes for the new image

    # Reset touch points for this image
    current_touch_points.clear()

    # Load touch events if any
    base_name = os.path.splitext(os.path.basename(img_path))[0]
    touch_filepath = os.path.join(TOUCH_EVENTS_FOLDER, base_name + ".txt")
    if os.path.exists(touch_filepath):
        with open(touch_filepath, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(",")
                    if len(parts) >= 2:
                        try:
                            x = int(parts[0])
                            y = int(parts[1])
                            current_touch_points.append((x, y))
                        except ValueError:
                            print(f"Invalid number in touch event file: {line}")

    # Load existing labels for this image if they exist
    img_filename = os.path.basename(img_path)
    label_filename = os.path.splitext(img_filename)[0] + ".txt"
    label_filepath = os.path.join(OUTPUT_LABEL_FOLDER, label_filename)

    if os.path.exists(label_filepath):
        print(f"Loading existing labels from: {label_filepath}")
        img_h, img_w = current_image.shape[:2]
        with open(label_filepath, "r") as f:
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

                    current_bboxes.append(
                        {
                            "class_id": class_id,
                            "bbox": [x_min, y_min, x_max, y_max],
                        }
                    )

    redraw_image()
    update_image_info_label()
    return True


def update_image_info_label():
    """Update the image info label in GUI."""
    if root and image_files:
        info_text = f"Image: {os.path.basename(image_files[current_image_index])} ({current_image_index + 1}/{len(image_files)})"
        image_info_label.config(text=info_text)


def redraw_image():
    """Redraws the image with current bboxes and info text."""
    global display_image, current_image, current_bboxes, ref_point, drawing, selected_class_id
    if current_image is None:
        return
    display_image = current_image.copy()

    # Draw saved bounding boxes
    for item in current_bboxes:
        class_id = item["class_id"]
        label_text = get_class_name_from_id(class_id)
        # remove the words card or troop from the label text
        label_text = label_text.replace("Card", "").replace("Troop", "")
        # only keep the first 10 characters of the label text
        # label_text = label_text[:10]

        x_min, y_min, x_max, y_max = item["bbox"]
        cv2.rectangle(
            display_image,
            (x_min, y_min),
            (x_max, y_max),
            SAVED_BOX_COLOR,
            LINE_THICKNESS,
        )
        (w, h), _ = cv2.getTextSize(label_text, FONT, FONT_SCALE, LINE_THICKNESS)
        cv2.rectangle(
            display_image,
            (x_min, y_min - h - 5),
            (x_min + w, y_min - 5),
            SAVED_BOX_COLOR,
            -1,
        )
        cv2.putText(
            display_image,
            label_text,
            (x_min, y_min - 5),
            FONT,
            FONT_SCALE,
            TEXT_COLOR,
            LINE_THICKNESS,
        )

    # Draw current drawing box if any
    if drawing and len(ref_point) == 2:
        cv2.rectangle(display_image, ref_point[0], ref_point[1], BOX_COLOR, LINE_THICKNESS)

    # Draw current touch points as red circles
    for pt in current_touch_points:
        cv2.circle(display_image, pt, 5, (0, 0, 255), -1)

    # Display current selection and controls
    current_class_name = get_class_name_from_id(selected_class_id)
    info_text_class = f"Selected: {current_class_name} (ID: {selected_class_id})"
    info_text_controls = "S:Save | D:Del | Space:Next | B:Prev | Q:Quit | A:Auto | Click card in panel to select"

    cv2.putText(
        display_image,
        info_text_class,
        (10, 30),
        FONT,
        FONT_SCALE,
        (255, 255, 255),
        LINE_THICKNESS + 1,
        cv2.LINE_AA,
    )
    cv2.putText(
        display_image,
        info_text_class,
        (10, 30),
        FONT,
        FONT_SCALE,
        TEXT_COLOR,
        LINE_THICKNESS,
        cv2.LINE_AA,
    )

    cv2.putText(
        display_image,
        info_text_controls,
        (10, 60),
        FONT,
        FONT_SCALE,
        (255, 255, 255),
        LINE_THICKNESS + 1,
        cv2.LINE_AA,
    )
    cv2.putText(
        display_image,
        info_text_controls,
        (10, 60),
        FONT,
        FONT_SCALE,
        TEXT_COLOR,
        LINE_THICKNESS,
        cv2.LINE_AA,
    )

    cv2.imshow(WINDOW_NAME, display_image)


def mouse_callback(event, x, y, flags, param):
    """Handles mouse events for drawing bounding boxes."""
    global ref_point, drawing, current_bboxes, display_image, selected_class_id

    if event == cv2.EVENT_LBUTTONDOWN:
        ref_point = [(x, y)]
        drawing = True
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            ref_point.append((x, y))  # Store current mouse position as the second point
            temp_display = display_image.copy()  # Use a copy for temporary drawing
            cv2.rectangle(temp_display, ref_point[0], (x, y), BOX_COLOR, LINE_THICKNESS)
            cv2.imshow(WINDOW_NAME, temp_display)
            ref_point.pop()  # Remove the temporary second point
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
            current_bboxes.append(
                {
                    "class_id": selected_class_id,
                    "bbox": [x_min, y_min, x_max, y_max],
                }
            )
        ref_point = []
        redraw_image()


def get_class_name_from_id(class_id):
    """Get class name from class ID."""
    idx = class_id
    total_card = sum(len(g) for g in CARD_CLASSES)
    if idx >= total_card:
        idx -= total_card
        active_classes = TROOP_CLASSES
        prefix = "T"
    else:
        active_classes = CARD_CLASSES
        prefix = "C"

    for g, arr in enumerate(active_classes):
        if idx < len(arr):
            return f"{prefix}:{arr[idx]}"
        idx -= len(arr)
    return f"Unknown:{class_id}"


def get_all_card_info():
    """Get all card information with their class IDs."""
    all_cards = []
    class_id = 0

    # Card classes first
    for elixir_idx, elixir_group in enumerate(CARD_CLASSES):
        for card_name in elixir_group:
            all_cards.append({"class_id": class_id, "name": card_name, "type": "card", "elixir": elixir_idx + 1})
            class_id += 1

    # Then troop classes
    for elixir_idx, elixir_group in enumerate(TROOP_CLASSES):
        for troop_name in elixir_group:
            all_cards.append({"class_id": class_id, "name": troop_name, "type": "troop", "elixir": elixir_idx + 1})
            class_id += 1

    return all_cards


def on_card_button_click(class_id, card_name):
    """Handle card button click."""
    global selected_class_id
    selected_class_id = class_id
    print(f"Selected: {card_name} (ID: {class_id})")

    # Update frame styles to show selection (avoids image loss issues)
    for cid, frame in card_frames.items():
        if cid == class_id:
            frame.config(borderwidth=4, relief=tk.SOLID, style="Selected.TFrame")
        else:
            frame.config(borderwidth=2, relief=tk.GROOVE, style="TFrame")

    redraw_image()


def create_gui():
    """Create the Tkinter GUI for card selection."""
    global root, card_buttons, card_images_tk, image_info_label

    root = tk.Tk()
    root.title("Card Selector")
    root.geometry("900x800")

    # Image info at top
    info_frame = ttk.Frame(root)
    info_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

    image_info_label = ttk.Label(info_frame, text="No image loaded", font=("Arial", 10, "bold"))
    image_info_label.pack()

    # Filter controls
    filter_frame = ttk.Frame(root)
    filter_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

    ttk.Label(filter_frame, text="Filter:").pack(side=tk.LEFT, padx=5)

    filter_var = tk.StringVar(value="all")
    ttk.Radiobutton(filter_frame, text="All", variable=filter_var, value="all", command=lambda: filter_cards(filter_var.get(), search_var.get())).pack(side=tk.LEFT)
    ttk.Radiobutton(filter_frame, text="Cards", variable=filter_var, value="card", command=lambda: filter_cards(filter_var.get(), search_var.get())).pack(side=tk.LEFT)
    ttk.Radiobutton(filter_frame, text="Troops", variable=filter_var, value="troop", command=lambda: filter_cards(filter_var.get(), search_var.get())).pack(side=tk.LEFT)

    # Search box
    ttk.Label(filter_frame, text="Search:").pack(side=tk.LEFT, padx=(20, 5))
    search_var = tk.StringVar()
    search_entry = ttk.Entry(filter_frame, textvariable=search_var, width=20)
    search_entry.pack(side=tk.LEFT)
    search_var.trace("w", lambda *args: filter_cards(filter_var.get(), search_var.get()))

    # Create a canvas with scrollbar
    canvas_frame = ttk.Frame(root)
    canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

    canvas = tk.Canvas(canvas_frame)
    scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Mouse wheel scrolling
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", on_mousewheel)

    # Load all cards and create buttons
    all_cards = get_all_card_info()
    row = 0
    col = 0
    cols_per_row = 4

    for card_info in all_cards:
        class_id = card_info["class_id"]
        card_name = card_info["name"]

        # Try to load image
        img_path = os.path.join(TEMPLATES_FOLDER, f"{card_name}.png")

        # Create frame for each card
        card_frame = ttk.Frame(scrollable_frame, borderwidth=2, relief=tk.GROOVE)
        card_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        # Load and display image
        if os.path.exists(img_path):
            try:
                pil_img = Image.open(img_path)
                pil_img = pil_img.resize((80, 100), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(pil_img)
                card_images_tk[card_name] = photo  # Keep reference

                btn = tk.Button(
                    card_frame,
                    image=photo,
                    command=lambda cid=class_id, cn=card_name: on_card_button_click(cid, cn),
                    compound=tk.TOP,
                    text=card_name.replace("Card", ""),
                    font=("Arial", 8),
                    width=100,
                    height=120,
                )
            except Exception as e:
                print(f"Error loading image for {card_name}: {e}")
                btn = tk.Button(
                    card_frame,
                    text=card_name.replace("Card", ""),
                    command=lambda cid=class_id, cn=card_name: on_card_button_click(cid, cn),
                    width=12,
                    height=6,
                    font=("Arial", 8),
                )
        else:
            btn = tk.Button(
                card_frame,
                text=card_name.replace("Card", ""),
                command=lambda cid=class_id, cn=card_name: on_card_button_click(cid, cn),
                width=12,
                height=6,
                font=("Arial", 8),
            )

        btn.pack(fill=tk.BOTH, expand=True)
        card_buttons[class_id] = btn
        card_frames[class_id] = card_frame

        # Store card info for filtering
        btn.card_info = card_info
        btn.card_frame = card_frame

        col += 1
        if col >= cols_per_row:
            col = 0
            row += 1

    # Select first card by default
    if all_cards:
        on_card_button_click(all_cards[0]["class_id"], all_cards[0]["name"])

    def filter_cards(filter_type, search_text):
        """Filter visible cards based on type and search."""
        search_text = search_text.lower()
        for class_id, btn in card_buttons.items():
            card_info = btn.card_info
            card_frame = btn.card_frame

            # Check type filter
            type_match = filter_type == "all" or card_info["type"] == filter_type

            # Check search filter
            search_match = not search_text or search_text in card_info["name"].lower()

            if type_match and search_match:
                card_frame.grid()
            else:
                card_frame.grid_remove()

    return root


def next_image():
    """Load next image."""
    global current_image_index
    save_labels()
    current_image_index += 1
    if current_image_index >= len(image_files):
        print("Reached end of images.")
        current_image_index = len(image_files) - 1
    else:
        load_image_and_labels(current_image_index)


def prev_image():
    """Load previous image."""
    global current_image_index
    save_labels()
    current_image_index -= 1
    if current_image_index < 0:
        current_image_index = 0
    else:
        load_image_and_labels(current_image_index)


def auto_add_boxes():
    """Auto-add boxes at touch points."""
    global current_touch_points, current_bboxes, selected_class_id, current_image

    if not current_touch_points:
        print("No touch points for this image.")
        return

    BOX_SIZE = 40

    # Get current image size
    img_h, img_w = current_image.shape[:2]
    phone_w, phone_h = 1080, 2400
    scale_x = img_w / phone_w
    scale_y = img_h / phone_h

    for pt in current_touch_points:
        x_phone, y_phone = pt
        box_size = BOX_SIZE
        if y_phone > 2000:
            box_size = 50

        # Map phone coordinates to screenshot coordinates
        x = int(x_phone * scale_x)
        y = int(y_phone * scale_y)
        bbox = [
            x - box_size,
            y - box_size,
            x + box_size,
            y + box_size,
        ]
        current_bboxes.append({"class_id": selected_class_id, "bbox": bbox})

    print(f"Added {len(current_touch_points)} boxes at touch points.")
    redraw_image()


def main():
    global image_files, current_image_index, root

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

    # Create GUI
    root = create_gui()

    # Create OpenCV window
    cv2.namedWindow(WINDOW_NAME)
    cv2.setMouseCallback(WINDOW_NAME, mouse_callback)

    if not load_image_and_labels(current_image_index):
        return  # Exit if first image fails to load

    print("\n=== YOLO Labeling Tool with GUI ===")
    print("Draw boxes on the image by clicking and dragging.")
    print("Click cards in the panel to select them for labeling.")
    print("\nKeyboard shortcuts:")
    print("  S - Save labels")
    print("  D - Delete last box")
    print("  Space/Enter - Next image")
    print("  B - Previous image")
    print("  A - Auto-add boxes at touch points")
    print("  Q - Quit")
    print("=" * 50 + "\n")

    # Main loop
    def check_opencv():
        """Check OpenCV window for events."""
        global current_image_index

        if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
            root.quit()
            return

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):  # Quit
            root.quit()
        elif key == ord("s"):  # Save labels
            save_labels()
        elif key == ord("d"):  # Delete last bounding box
            if current_bboxes:
                current_bboxes.pop()
                redraw_image()
        elif key == ord("a"):  # Auto-add boxes
            auto_add_boxes()
        elif key == ord(" ") or key == 13:  # Space or Enter for Next image
            next_image()
        elif key == ord("b"):  # Previous image
            prev_image()

        # Schedule next check
        root.after(10, check_opencv)

    # Start checking OpenCV
    root.after(10, check_opencv)

    # Start GUI main loop
    root.mainloop()

    # Cleanup
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
