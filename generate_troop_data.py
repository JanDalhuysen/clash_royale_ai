# generate_troop_data.py
import cv2
import numpy as np
import os
import random

# --- CONFIGURATION ---
# This generator is specifically for TROOPS (Gameplay).
# Ensure your 'data_troops.yaml' has class names corresponding to TROOPS (e.g., 'SkeletonsTroop', 'GiantTroop').
# NOT cards.

SPRITE_DIR = 'extracted_sprites'
BACKGROUND_DIR = 'backgrounds'      # Ensure these are ARENA backgrounds
OUTPUT_IMG_DIR = 'data/troops_dataset/images'
OUTPUT_LABEL_DIR = 'data/troops_dataset/labels'
NUM_IMAGES_TO_GENERATE = 500

def overlay_transparent(background, overlay, x, y):
    bg_h, bg_w, _ = background.shape
    h, w, _ = overlay.shape

    if x >= bg_w or y >= bg_h: return background

    # Clip if out of bounds
    w = min(w, bg_w - x)
    h = min(h, bg_h - y)
    if w <= 0 or h <= 0: return background

    overlay = overlay[:h, :w]
    
    alpha = overlay[:, :, 3] / 255.0
    overlay_bgr = overlay[:, :, :3]

    for c in range(0, 3):
        background[y:y+h, x:x+w, c] = (
            alpha * overlay_bgr[:, :, c] +
            (1 - alpha) * background[y:y+h, x:x+w, c]
        )
    return background

def generate_synthetic_data(num_images, class_map):
    os.makedirs(OUTPUT_IMG_DIR, exist_ok=True)
    os.makedirs(OUTPUT_LABEL_DIR, exist_ok=True)

    background_files = [os.path.join(BACKGROUND_DIR, f) for f in os.listdir(BACKGROUND_DIR) if f.lower().endswith(('.png', '.jpg'))]
    if not background_files:
        print(f"Error: No backgrounds found in {BACKGROUND_DIR}")
        return

    all_sprites = []
    for char_name, class_id in class_map.items():
        char_dir = os.path.join(SPRITE_DIR, char_name)
        if os.path.isdir(char_dir):
            files = [f for f in os.listdir(char_dir) if f.endswith('.png')]
            for f in files:
                all_sprites.append({'class_id': class_id, 'path': os.path.join(char_dir, f)})
        else:
             print(f"Warning: Sprite directory not found: {char_dir}")

    if not all_sprites:
        print("Error: No sprites found to generate data.")
        return
        
    for i in range(num_images):
        bg_path = random.choice(background_files)
        background = cv2.imread(bg_path)
        if background is None: continue
        bg_h, bg_w, _ = background.shape

        yolo_labels = []
        num_sprites = random.randint(3, 9) # Realistic crowd

        for _ in range(num_sprites):
            sprite_info = random.choice(all_sprites)
            sprite_img = cv2.imread(sprite_info['path'], cv2.IMREAD_UNCHANGED)
            if sprite_img is None: continue
            
            # Random scale (troops vary slightly or by effect)
            scale = random.uniform(0.6, 0.7) 
            new_w = int(sprite_img.shape[1] * scale)
            new_h = int(sprite_img.shape[0] * scale)
            sprite_resized = cv2.resize(sprite_img, (new_w, new_h))

            # Random placement (limit to arena area preferably)
            # Assuming full frame for now
            max_x = bg_w - new_w
            max_y = bg_h - new_h
            if max_x <= 0 or max_y <= 0: continue
            
            x_pos = random.randint(100, max_x - 100)
            y_pos = random.randint(300, max_y - 500) # Avoid extreme top/bottom UI areas roughly

            background = overlay_transparent(background, sprite_resized, x_pos, y_pos)

            # Labels
            class_id = sprite_info['class_id']
            x_center = (x_pos + new_w / 2) / bg_w
            y_center = (y_pos + new_h / 2) / bg_h
            width_norm = new_w / bg_w
            height_norm = new_h / bg_h
            
            yolo_labels.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width_norm:.6f} {height_norm:.6f}")

        output_img_path = os.path.join(OUTPUT_IMG_DIR, f"synth_troop_{i}.jpg")
        output_label_path = os.path.join(OUTPUT_LABEL_DIR, f"synth_troop_{i}.txt")
        
        cv2.imwrite(output_img_path, background)
        with open(output_label_path, 'w') as f:
            f.write("\n".join(yolo_labels))

    print(f"Generated {num_images} images in {OUTPUT_IMG_DIR}")

if __name__ == '__main__':
    # UPDATE THIS MAPPING to match your data_troops.yaml exactly!
    # These IDs should define TROOPS (e.g. 0=SkeletonTroop), not Cards.
    # CLASS_MAP = {
    #     'chr_skeleton_tex': 0,
    #     'ElectroSpirit': 1,
    #     'FireSpirit': 2,
    #     'chr_ice_spirits_tex': 3,
    #     'HealSpirit': 4,
    #     # ... Add the rest of your troop mappings here ...
    # }
    CLASS_MAP = {
        # 'chr_baby_dragon_tex': 0,
        # 'goblin': 2,
        # ... and so on for all your characters
        'chr_skeleton_tex': 0,
        'ElectroSpirit': 1,
        'FireSpirit': 2,
        'chr_ice_spirits_tex': 3,
        'HealSpirit': 4,
        'chr_goblin_tex': 5,
        'chr_goblin_archer_tex': 6,
        'chr_bomber_tex': 7,
        'chr_bats_tex': 8,
        'Zap': 9,
        'GiantSnowball': 10,
        'chr_berserker_tex': 11,
        'IceGolem': 12,
        'SuspiciousBush': 13,
        'BarbarianBarrel': 14,
        'WallBreakers': 15,
        'GoblinCurse': 16,
        'Rage': 17,
        'TheLog': 18,
        'chr_archer_tex': 19,
        'Arrows': 20,
        'chr_knight_tex': 21,
        'chr_minion_tex': 22,
        'Cannon': 23,
        'GoblinGang': 24,
        'SkeletonBarrel': 25,
        'Firecracker': 26,
        'RoyalDelivery': 27,
        'Tombstone': 28,
        'chr_mega_minion_tex': 29,
        'DartGoblin': 30,
        'Earthquake': 31,
        'ElixirGolem': 32,
        'GoblinBarrel': 33,
        'Guards': 34,
        'chr_skeleton_tex': 35,
        'Clone': 36,
        'Tornado': 37,
        'Void': 38,
        'chr_miner_tex': 39,
        'chr_princess_tex': 40,
        'chr_ice_wizard_tex': 41,
        'RoyalGhost': 42,
        'chr_bandit_tex': 43,
        'Fisherman': 44,
        'LittlePrince': 45,
        'SkeletonDragons': 46,
        'Mortar': 47,
        'Tesla': 48,
        'Fireball': 49,
        'MiniPEKKA': 50,
        'chr_musketeer_tex': 51,
        'GoblinCage': 52,
        'GoblinHut': 53,
        'chr_valkyrie_tex': 54,
        'chr_battle_ram_tex': 55,
        'BombTower': 56,
        'chr_flying_machine_tex': 57,
        'chr_hog_rider_tex': 58,
        'BattleHealer': 59,
        'Furnace': 60,
        'Zappies': 61,
        'chr_goblin_demolisher_tex': 62,
        'chr_baby_dragon_tex': 63,
        'DarkPrince': 64,
        'Freeze': 65,
        'Poison': 66,
        'RuneGiant': 67,
        'Hunter': 68,
        'GoblinDrill': 69,
        'chr_electro_wizard_tex': 70,
        'InfernoDragon': 71,
        'Phoenix': 72,
        'chr_archer_tex': 73,
        'Lumberjack': 74,
        'NightWitch': 75,
        'MotherWitch': 76,
        'GoldenKnight': 77,
        'chr_skeleton_tex': 78,
        'MightyMiner': 79,
        'chr_barbarian_tex': 80,
        'MinionHorde': 81,
        'Rascals': 82,
        'chr_giant_tex': 83,
        'InfernoTower': 84,
        'chr_wizard_tex': 85,
        'RoyalHogs': 86,
        'chr_witch_tex': 87,
        'chr_balloon_tex': 88,
        'chr_prince_tex': 89,
        'ElectroDragon': 90,
        'chr_bowler_tex': 91,
        'Executioner': 92,
        'Cannon': 93,
        'CannonCart': 94,
        'RamRider': 95,
        'Graveyard': 96,
        'chr_goblin_machine_tex': 97,
        'ArcherQueen': 98,
        'Goblinstein': 99,
        'Monk': 100,
        'chr_royal_giant_tex': 101,
        'EliteBarbarians': 102,
        'chr_RockerA_tex': 103,
        'chr_barbarian_tex': 104,
        'ElixirCollector': 105,
        'chr_giant_skeleton_tex': 106,
        'Lightning': 107,
        'GoblinGiant': 108,
        'X-Bow': 109,
        'Sparky': 110,
        'chr_boss_bandit_tex': 111,
        'RoyalRecruits': 112,
        'PEKKA': 113,
        'ElectroGiant': 114,
        'chr_mega_knight_tex': 115,
        'chr_lava_hound_tex': 116,
        'Golem': 117,
        'ThreeMusketeers': 118,

    }
    
    generate_synthetic_data(NUM_IMAGES_TO_GENERATE, CLASS_MAP)
