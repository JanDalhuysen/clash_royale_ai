import os
import cv2
import argparse
from pathlib import Path

crop_dir = "cropped_matches"
Path(crop_dir).mkdir(exist_ok=True)

# Make a set to store the deck of player 1 and player 2
player_1_deck = set()
player_2_deck = set()

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


def create_yolo_label(
    img,
    template_path,
    class_id,
    output_dir,
    confidence_threshold=0.6,
    scale_steps=10,
    box_scale_factor=0.55,
    max_detections=1,
):
    """Create YOLO label file using multi-scale template matching.

    Args:
        img: The image to process
        template_path: Path to the template image
        class_id: Class ID for the label
        output_dir: Output directory for labels
        confidence_threshold: Minimum confidence for a valid match
        scale_steps: Number of different scales to try
        box_scale_factor: Factor to scale the final bounding box (default 0.55 = 55% of original size)
        max_detections: Maximum number of detections to return for this template
    """
    template = cv2.imread(template_path)
    if template is None:
        print(f"Error: Could not load template {template_path}")
        return []

    # Busy with processing screenshot img

    # Get original template dimensions
    h, w = template.shape[:2]

    # scale_steps = 10

    detections = []
    working_img = img.copy()

    # Keep searching for additional instances when replay mode allows it.
    for _ in range(max_detections):
        best_match = None
        best_max_val = -1

        for scale in range(1, scale_steps + 1):
            # Calculate current scale factor
            # start_scale = 0.91
            # end_scale = 0.60
            # scale_factor = start_scale + (scale - 1) * (end_scale - start_scale) / (scale_steps - 1)
            # scale_factor = 2
            # scale_factor = 1.59
            # scale_factor = 1.98
            scale_factor = 0.82  # TV Royale Replay mode (in game)
            # scale_factor = 0.65 # TV Royale Replay mode (match selection screen)
            resized_template = cv2.resize(template, None, fx=scale_factor, fy=scale_factor)
            th, tw = resized_template.shape[:2]

            # Skip if template is larger than image
            if tw > working_img.shape[1] or th > working_img.shape[0]:
                continue

            # Template matching
            result = cv2.matchTemplate(working_img, resized_template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            # Keep track of best match across all scales
            if max_val > best_max_val:
                best_max_val = max_val
                best_match = (max_loc, tw, th, scale_factor)

        # Stop if no more valid matches are found.
        if not best_match or best_max_val < confidence_threshold:
            break

        top_left, tw, th, scale_factor = best_match

        # If the match is not in the top or bottom of the image, discard it and keep searching.
        # if top_left[1] > 200 and top_left[1] < img.shape[0] - 200:
        # print(f"Discarded {os.path.basename(template_path)} with confidence {best_max_val:.2f} at scale {scale_factor:.2f} because it is not in the top or bottom of the image")
        # cv2.rectangle(working_img, top_left, (top_left[0] + tw, top_left[1] + th), (0, 0, 0), thickness=-1)
        # continue

        print(f"Matched {os.path.basename(template_path)} with confidence {best_max_val:.2f} at scale {scale_factor:.2f}")
        bottom_right = (top_left[0] + tw, top_left[1] + th)

        # Get bounding box coordinates
        x, y = top_left
        width = bottom_right[0] - top_left[0]
        height = bottom_right[1] - top_left[1]

        # If the matched card is in the top half of the image add it to the player 1 set
        if y + height / 2 < img.shape[0] / 2:
            player_1_deck.add(class_id)
        else:
            player_2_deck.add(class_id)

        # Get current timestamp in milliseconds for unique filename (normal Python time)
        import time

        timestamp = int(time.time() * 1000)

        # Crop the matched region from the original image
        matched_region = img[y : y + height, x : x + width]
        # Save the matched region for debugging
        matched_region_path = os.path.join(crop_dir, f"{best_max_val:.2f}_matched_{class_id}_{timestamp}_{os.path.basename(template_path)}")
        cv2.imwrite(matched_region_path, matched_region)

        # Calculate center of the bounding box
        center_x = x + width / 2
        center_y = y + height / 2

        # Apply the box scale factor to make the box smaller
        scaled_width = width  # * (box_scale_factor+0.2)
        scaled_height = height * box_scale_factor

        # Normalize coordinates
        img_h, img_w = img.shape[:2]
        x_center = center_x / img_w
        y_center = center_y / img_h
        norm_width = scaled_width / img_w
        norm_height = scaled_height / img_h

        detections.append((class_id, x_center, y_center, norm_width, norm_height))

        # Mask out the matched region so replay mode can find a second copy of the same card.
        cv2.rectangle(working_img, top_left, bottom_right, (0, 0, 0), thickness=-1)

    return detections


def main():
    """Main function to process images and generate labels."""
    images_dir = "images_to_label"
    templates_dir = "templates"
    output_dir = "labels"

    # parser = argparse.ArgumentParser(description="Generate YOLO labels from Clash Royale screenshots using template matching.")
    # parser.add_argument(
    #     "--mode",
    #     choices=["live", "replay"],
    #     default="live",
    #     help="live allows one detection per card per image; replay allows up to two detections per card",
    # )
    # args = parser.parse_args()

    # Configuration parameters

    # Minimum confidence for a valid match
    confidence_threshold = 0.75

    # Number of different scales to try for template matching
    scale_steps = 1

    # 55% of the original bounding box size
    box_scale_factor = 0.55

    # Maximum number of detections to return for each card
    # set to 1 for live mode
    # 2 for replay mode / TV Royale
    max_detections_per_card = 2

    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(exist_ok=True)

    # Get ordered list of all class IDs
    ordered_class_ids = get_ordered_class_ids()

    # Get all template files from the templates directory
    template_files = [f for f in os.listdir(templates_dir) if f.endswith((".png", ".jpg", ".jpeg"))]

    # Process each image
    for image_file in os.listdir(images_dir):
        if not image_file.endswith((".png", ".jpg", ".jpeg")):
            continue

        image_path = os.path.join(images_dir, image_file)
        print(f"Processing {image_file}")
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
                boxes = create_yolo_label(
                    img,
                    template_path,
                    class_id,
                    output_dir,
                    confidence_threshold=confidence_threshold,
                    scale_steps=scale_steps,
                    box_scale_factor=box_scale_factor,
                    max_detections=max_detections_per_card,
                )
                all_boxes.extend(boxes)
            # else:
            # print(f"Warning: Card name {card_name} not found in class IDs list")

        # Write all boxes to label file
        base_name = os.path.splitext(image_file)[0]
        label_path = os.path.join(output_dir, base_name + ".txt")

        with open(label_path, "w") as f:
            for box in all_boxes:
                f.write(" ".join(map(str, box)) + "\n")

        print(f"Player 1 deck: {len(player_1_deck)} {[get_ordered_class_ids()[i] for i in player_1_deck]}")
        print(f"Player 2 deck: {len(player_2_deck)} {[get_ordered_class_ids()[i] for i in player_2_deck]}")

        print(f"*******\nProcessed {image_file}, found {len(all_boxes)} cards\n\n")


if __name__ == "__main__":
    main()
