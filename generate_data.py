# generate_data.py
import cv2
import numpy as np
import os
import random


def overlay_transparent(background, overlay, x, y):
    """
    Overlays a transparent BGRA image onto a BGR image.
    """
    bg_h, bg_w, _ = background.shape
    h, w, _ = overlay.shape

    # Get the alpha channel from the overlay
    alpha = overlay[:, :, 3] / 255.0

    # Get the BGR channels from the overlay
    overlay_bgr = overlay[:, :, :3]

    # Perform the overlay
    for c in range(0, 3):
        background[y : y + h, x : x + w, c] = alpha * overlay_bgr[:, :, c] + (1 - alpha) * background[y : y + h, x : x + w, c]
    return background


def generate_synthetic_data(num_images, class_map):
    """
    Generates synthetic images and YOLO labels.
    """
    SPRITE_DIR = "ig_extracted_sprites"
    BACKGROUND_DIR = "ig_backgrounds"
    OUTPUT_IMG_DIR = "ig_synthetic_output/images"
    OUTPUT_LABEL_DIR = "ig_synthetic_output/labels"

    os.makedirs(OUTPUT_IMG_DIR, exist_ok=True)
    os.makedirs(OUTPUT_LABEL_DIR, exist_ok=True)

    background_files = [os.path.join(BACKGROUND_DIR, f) for f in os.listdir(BACKGROUND_DIR) if f.lower().endswith((".png", ".jpg"))]
    all_sprites = []
    for char_name, class_id in class_map.items():
        char_dir = os.path.join(SPRITE_DIR, char_name)
        print(f"Loading sprites for character '{char_name}' (class ID: {class_id}) from '{char_dir}'")
        if os.path.isdir(char_dir):
            for f in os.listdir(char_dir):
                all_sprites.append({"class_id": class_id, "path": os.path.join(char_dir, f)})

    if not all_sprites:
        print("Error: No sprites found. Did you run extract_sprites.py?")
        return

    for i in range(num_images):
        print(f"Generating image {i + 1}/{num_images}...")

        # 1. Load a random background
        bg_path = random.choice(background_files)
        background = cv2.imread(bg_path)
        bg_h, bg_w, _ = background.shape

        yolo_labels = []
        # num_sprites_to_place = random.randint(5, 20) # Place 5 to 20 sprites per image
        num_sprites_to_place = 1

        for _ in range(num_sprites_to_place):
            # 2. Select a random sprite
            sprite_info = random.choice(all_sprites)
            sprite_img = cv2.imread(sprite_info["path"], cv2.IMREAD_UNCHANGED)  # Read with alpha channel

            # --- 3. Augment the sprite ---
            # Randomly resize
            # scale = random.uniform(0.5, 1.2) # Scale between 50% and 120%
            scale = 0.5
            new_w = int(sprite_img.shape[1] * scale)
            new_h = int(sprite_img.shape[0] * scale)
            sprite_resized = cv2.resize(sprite_img, (new_w, new_h))

            # (Optional: Add more augmentations like rotation, brightness, etc.)

            # 4. Choose a random placement location
            # max_x = bg_w - new_w
            # max_y = bg_h - new_h
            # if max_x <= 0 or max_y <= 0: continue # Skip if sprite is too big for background

            # x_pos = random.randint(0, max_x)
            # y_pos = random.randint(0, max_y)

            # x y w h
            # (133, 279, 195, 312)
            x_pos = random.randint(133, 133 + 195)
            y_pos = random.randint(279, 279 + 312)

            # 5. Overlay the sprite onto the background
            background = overlay_transparent(background, sprite_resized, x_pos, y_pos)
            # background = overlay_transparent(background, sprite_img, x_pos, y_pos)

            # 6. Calculate and store YOLO label
            class_id = sprite_info["class_id"]
            # Bounding box of the placed sprite
            x_center = (x_pos + new_w / 2) / bg_w
            y_center = (y_pos + new_h / 2) / bg_h
            width_norm = new_w / bg_w
            height_norm = new_h / bg_h

            yolo_labels.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width_norm:.6f} {height_norm:.6f}")

        # 7. Save the final image and labels
        output_img_path = os.path.join(OUTPUT_IMG_DIR, f"synth_{i}.jpg")
        output_label_path = os.path.join(OUTPUT_LABEL_DIR, f"synth_{i}.txt")

        cv2.imwrite(output_img_path, background)
        with open(output_label_path, "w") as f:
            f.write("\n".join(yolo_labels))

    print(f"Done! Generated {num_images} synthetic images and labels in 'synthetic_output/'")


if __name__ == "__main__":
    # IMPORTANT: Create a mapping from your character folder names to the class IDs
    # These IDs must match the 'names' list in your YOLOv8 data.yaml file.
    CLASS_MAP = {
        # 'chr_baby_dragon_tex': 0,
        # 'goblin': 2,
        # ... and so on for all your characters
        "chr_skeleton_tex": 0,
        "ElectroSpirit": 1,
        "FireSpirit": 2,
        "chr_ice_spirits_tex": 3,
        "HealSpirit": 4,
        "chr_goblin_tex": 5,
        "SpearGoblins": 6,
        "chr_bomber_tex": 7,
        "chr_bats_tex": 8,
        "Zap": 9,
        "GiantSnowball": 10,
        "chr_berserker_tex": 11,
        "IceGolem": 12,
        "SuspiciousBush": 13,
        "BarbarianBarrel": 14,
        "WallBreakers": 15,
        "GoblinCurse": 16,
        "Rage": 17,
        "TheLog": 18,
        "chr_archer_tex": 19,
        "Arrows": 20,
        "chr_knight_tex": 21,
        "chr_minion_tex": 22,
        "Cannon": 23,
        "GoblinGang": 24,
        "SkeletonBarrel": 25,
        "Firecracker": 26,
        "RoyalDelivery": 27,
        "Tombstone": 28,
        "chr_mega_minion_tex": 29,
        "DartGoblin": 30,
        "Earthquake": 31,
        "ElixirGolem": 32,
        "GoblinBarrel": 33,
        "Guards": 34,
        "chr_skeleton_tex": 35,
        "Clone": 36,
        "Tornado": 37,
        "Void": 38,
        "chr_miner_tex": 39,
        "chr_princess_tex": 40,
        "chr_ice_wizard_tex": 41,
        "RoyalGhost": 42,
        "chr_bandit_tex": 43,
        "Fisherman": 44,
        "LittlePrince": 45,
        "SkeletonDragons": 46,
        "Mortar": 47,
        "Tesla": 48,
        "Fireball": 49,
        "MiniPEKKA": 50,
        "chr_musketeer_tex": 51,
        "GoblinCage": 52,
        "GoblinHut": 53,
        "chr_valkyrie_tex": 54,
        "chr_battle_ram_tex": 55,
        "BombTower": 56,
        "chr_flying_machine_tex": 57,
        "chr_hog_rider_tex": 58,
        "BattleHealer": 59,
        "Furnace": 60,
        "Zappies": 61,
        "chr_goblin_demolisher_tex": 62,
        "chr_baby_dragon_tex": 63,
        "DarkPrince": 64,
        "Freeze": 65,
        "Poison": 66,
        "RuneGiant": 67,
        "Hunter": 68,
        "GoblinDrill": 69,
        "chr_electro_wizard_tex": 70,
        "InfernoDragon": 71,
        "Phoenix": 72,
        "chr_archer_tex": 73,
        "Lumberjack": 74,
        "NightWitch": 75,
        "MotherWitch": 76,
        "GoldenKnight": 77,
        "chr_skeleton_tex": 78,
        "MightyMiner": 79,
        "chr_barbarian_tex": 80,
        "MinionHorde": 81,
        "Rascals": 82,
        "chr_giant_tex": 83,
        "InfernoTower": 84,
        "chr_wizard_tex": 85,
        "RoyalHogs": 86,
        "chr_witch_tex": 87,
        "chr_balloon_tex": 88,
        "chr_prince_tex": 89,
        "ElectroDragon": 90,
        "chr_bowler_tex": 91,
        "Executioner": 92,
        "Cannon": 93,
        "CannonCart": 94,
        "RamRider": 95,
        "Graveyard": 96,
        "chr_goblin_machine_tex": 97,
        "ArcherQueen": 98,
        "Goblinstein": 99,
        "Monk": 100,
        "chr_royal_giant_tex": 101,
        "EliteBarbarians": 102,
        "chr_RockerA_tex": 103,
        "chr_barbarian_tex": 104,
        "ElixirCollector": 105,
        "chr_giant_skeleton_tex": 106,
        "Lightning": 107,
        "GoblinGiant": 108,
        "X-Bow": 109,
        "Sparky": 110,
        "chr_boss_bandit_tex": 111,
        "RoyalRecruits": 112,
        "PEKKA": 113,
        "ElectroGiant": 114,
        "chr_mega_knight_tex": 115,
        "chr_lava_hound_tex": 116,
        "Golem": 117,
        "ThreeMusketeers": 118,
    }

    # Number of synthetic images to generate
    NUM_IMAGES_TO_GENERATE = 999

    generate_synthetic_data(NUM_IMAGES_TO_GENERATE, CLASS_MAP)
