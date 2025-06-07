import pyautogui
import cv2
import numpy as np
import time
import os

import itertools

# --- Configuration ---

# 1. DEFINE YOUR 8 DECK CARD TEMPLATES
#    Use the filenames of your resized and cropped card images that worked before.
#    Replace the example paths with your actual paths.
#    The keys (e.g., "Archers") are for your reference and output.
DECK_CARD_TEMPLATES = {
    "Witch": r"C:\gitsync\jan_projects\clash_royale_ai\all_cards_small_cropped2\WitchCard.png.resized.png",
    "Wizard": r"C:\gitsync\jan_projects\clash_royale_ai\all_cards_small_cropped2\WizardCard.png.resized.png",
    "Graveyard": r"C:\gitsync\jan_projects\clash_royale_ai\all_cards_small_cropped2\GraveyardCard.png.resized.png",
    "Ram Rider": r"C:\gitsync\jan_projects\clash_royale_ai\all_cards_small_cropped2\RamRiderCard.png.resized.png",
    "X-Bow": r"C:\gitsync\jan_projects\clash_royale_ai\all_cards_small_cropped2\X-BowCard.png.resized.png",
    "Lumberjack": r"C:\gitsync\jan_projects\clash_royale_ai\all_cards_small_cropped2\LumberjackCard.png.resized.png",
    "Magic Archer": r"C:\gitsync\jan_projects\clash_royale_ai\all_cards_small_cropped2\MagicArcherCard.png.resized.png",
    "Royal Hogs": r"C:\gitsync\jan_projects\clash_royale_ai\all_cards_small_cropped2\RoyalHogsCard.png.resized.png",
    # Add all 8 of your chosen deck cards. Ensure paths are correct!
}

# DECK_CARD_TEMPLATES = {
# "BabyDragonCard": r"C:\gitsync\jan_projects\clash_royale_ai\all_cards_small_cropped2\BabyDragonCard.png.resized.png",
# "GoblinBarrelCard": r"C:\gitsync\jan_projects\clash_royale_ai\all_cards_small_cropped2\GoblinBarrelCard.png.resized.png",
# "MinerCard": r"C:\gitsync\jan_projects\clash_royale_ai\all_cards_small_cropped2\MinerCard.png.resized.png",
# "MusketeerCard": r"C:\gitsync\jan_projects\clash_royale_ai\all_cards_small_cropped2\MusketeerCard.png.resized.png",
# "RamRiderCard": r"C:\gitsync\jan_projects\clash_royale_ai\all_cards_small_cropped2\RamRiderCard.png.resized.png",
# "SkeletonArmyCard": r"C:\gitsync\jan_projects\clash_royale_ai\all_cards_small_cropped2\SkeletonArmyCard.png.resized.png",
# "SpearGoblinsCard": r"C:\gitsync\jan_projects\clash_royale_ai\all_cards_small_cropped2\SpearGoblinsCard.png.resized.png",
# "WitchCard": r"C:\gitsync\jan_projects\clash_royale_ai\all_cards_small_cropped2\WitchCard.png.resized.png",
# # "None": r"C:\gitsync\jan_projects\clash_royale_ai\all_cards_small_cropped2\none.png",
# }

# DECK_CARD_TEMPLATES = {
# "WitchCard.png.resized": r"C:\gitsync\jan_projects\clash_royale_ai\all_cards_small_cropped2\WitchCard.png.resized.png",
# "WizardCard.png.resized": r"C:\gitsync\jan_projects\clash_royale_ai\all_cards_small_cropped2\WizardCard.png.resized.png",
# "GraveyardCard.png.resized": r"C:\gitsync\jan_projects\clash_royale_ai\all_cards_small_cropped2\GraveyardCard.png.resized.png",
# "RamRiderCard.png.resized": r"C:\gitsync\jan_projects\clash_royale_ai\all_cards_small_cropped2\RamRiderCard.png.resized.png",
# "X-BowCard.png.resized": r"C:\gitsync\jan_projects\clash_royale_ai\all_cards_small_cropped2\X-BowCard.png.resized.png",
# "LumberjackCard.png.resized": r"C:\gitsync\jan_projects\clash_royale_ai\all_cards_small_cropped2\LumberjackCard.png.resized.png",
# "MagicArcherCard.png.resized": r"C:\gitsync\jan_projects\clash_royale_ai\all_cards_small_cropped2\MagicArcherCard.png.resized.png",
# "RoyalHogsCard.png.resized": r"C:\gitsync\jan_projects\clash_royale_ai\all_cards_small_cropped2\RoyalHogsCard.png.resized.png",
# "None": r"C:\gitsync\jan_projects\clash_royale_ai\all_cards_small_cropped2\none.png",

# }


# 2. DEFINE REGIONS OF INTEREST (ROIs) FOR THE 4 CARD SLOTS IN YOUR HAND
#    These are (x, y, width, height) tuples for each slot.
#    IMPORTANT:
#        - 'x' and 'y' are the top-left coordinates of the slot on your screen.
#        - 'width' and 'height' MUST BE VERY CLOSE to the dimensions of your template images.
#    You'll need to measure these on your screen.
#    A utility function `get_rois_for_slots_utility()` is provided below to help you find these.
CARD_SLOT_ROIS = [
    (362, 907, 66, 62),  # Slot 1
    (442, 910, 74, 58),  # Slot 2
    (529, 911, 70, 58),  # Slot 3
    (611, 907, 75, 62),  # Slot 4
]

# CARD_SLOT_ROIS = [
#     (607, 885, 85, 114),  # Slot 1
#     (521, 888, 85, 114),  # Slot 2
#     (435, 888, 86, 107),  # Slot 3
#     (347, 886, 86, 114),  # Slot 4
# ]

# CARD_SLOT_ROIS = [
#     (345, 882, 91, 126),  # Slot 4
#     (435, 881, 87, 127),  # Slot 3
#     (520, 882, 87, 125),  # Slot 2
#     (598, 885, 96, 120),  # Slot 1
# ]

# Normal
# CARD_SLOT_ROIS = [
#     (362, 907, 66, 62),  # Slot 1
#     (442, 910, 74, 58),  # Slot 2
#     (529, 911, 70, 58),  # Slot 3
#     (611, 907, 75, 62),  # Slot 4
# ]

#Spectate
# CARD_SLOT_ROIS = [
#     (314, 925, 56, 71),  # Slot 1
#     (372, 927, 58, 71),  # Slot 2
#     (432, 927, 59, 70),  # Slot 3
#     (490, 927, 59, 70),  # Slot 4
# ]


# 3. MATCHING CONFIDENCE
#    Use the confidence level that worked well for you (e.g., 0.80).
MATCH_CONFIDENCE = 0.10

# 4. POLLING RATE (seconds)
#    How often to check the hand. Too fast can be CPU intensive or catch animations.
#    Too slow might miss quick plays. Clash Royale has ~1 sec global cooldown.
POLL_INTERVAL = 0.75 # seconds
POLL_INTERVAL = 0.5 # seconds

# --- Load Template Images ---
loaded_templates = {}
print("Loading card templates...")
for card_name, card_path in DECK_CARD_TEMPLATES.items():
    if not os.path.exists(card_path):
        print(f"ERROR: Template image not found at {card_path} for {card_name}")
        continue
    img = cv2.imread(card_path)
    if img is None:
        print(f"ERROR: Could not load template for {card_name} from {card_path}")
    else:
        loaded_templates[card_name] = img
        print(f"  ✓ Loaded template for {card_name} (Dimensions: {img.shape[1]}w x {img.shape[0]}h)")

if not loaded_templates:
    print("CRITICAL ERROR: No templates were successfully loaded. Exiting.")
    print("Please check the paths in DECK_CARD_TEMPLATES and ensure card images exist.")
    exit()

if len(loaded_templates) != 8:
    print(f"WARNING: Expected 8 deck templates, but only {len(loaded_templates)} were loaded.")
    print("The tracker will only work with the loaded cards.")


# --- Helper Functions ---

def pick_unique_cards(slot_matches):
    """
    slot_matches: List[List[(name,conf)]] of length n_slots, each inner list has exactly 2 tuples.
    Returns List[str] of length n_slots with one name per slot, maximizing total confidence
    and ensuring each name is used at most once.
    """
    best_score = -1.0
    best_choice = None

    # try every way of picking either match 0 or match 1 for each slot
    for choice in itertools.product([0, 1], repeat=len(slot_matches)):
        names = [slot_matches[i][choice[i]][0] for i in range(len(slot_matches))]
        # skip if duplicate names
        if len(set(names)) != len(names):
            continue
        score = sum(slot_matches[i][choice[i]][1] for i in range(len(slot_matches)))
        if score > best_score:
            best_score = score
            best_choice = choice

    if best_choice is None:
        # fallback: just pick the top‐confidence for each slot (may have duplicates)
        return [matches[0][0] for matches in slot_matches]

    # return the chosen names
    return [slot_matches[i][best_choice[i]][0] for i in range(len(slot_matches))]

def identify_card_in_slot(slot_screenshot_cv, templates_dict):
    """Attempts to identify the two best matching cards in a given slot image."""
    matches = []
    slot_h, slot_w = slot_screenshot_cv.shape[:2]

    for card_name, template_img in templates_dict.items():
        temp_img = template_img
        temp_h, temp_w = temp_img.shape[:2]

        # Resize template if it's larger than the slot in any dimension
        if temp_h > slot_h or temp_w > slot_w:
            scale = min(slot_h / temp_h, slot_w / temp_w)
            new_size = (max(1, int(temp_w * scale)), max(1, int(temp_h * scale)))
            temp_img = cv2.resize(temp_img, new_size)
            temp_h, temp_w = temp_img.shape[:2]

        # Skip if still too big
        if slot_h < temp_h or slot_w < temp_w:
            continue

        try:
            result = cv2.matchTemplate(slot_screenshot_cv, temp_img, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)
            matches.append((card_name, max_val))
        except cv2.error as e:
            print(f"OpenCV error matching {card_name}: {e}. Slot shape: {slot_screenshot_cv.shape}, Template shape: {temp_img.shape}")
            continue

    # Sort matches by confidence descending
    matches.sort(key=lambda x: x[1], reverse=True)
    # Return the two best matches above threshold (if any)
    best_matches = [(name, conf) for name, conf in matches if conf >= MATCH_CONFIDENCE][:2]
    # Pad with None if less than 2 found
    while len(best_matches) < 2:
        best_matches.append((None, -1.0))
    return best_matches

def load_all_templates_from_folder(folder_path):
    """
    Loads all PNG images from the given folder into a dictionary.
    Key: filename without extension, Value: loaded cv2 image.
    """
    templates = {}
    for fname in os.listdir(folder_path):
        if fname.lower().endswith(".png"):
            card_name = os.path.splitext(fname)[0]
            img_path = os.path.join(folder_path, fname)
            img = cv2.imread(img_path)
            if img is not None:
                templates[card_name] = img
            else:
                print(f"Warning: Could not load {img_path}")
    return templates

def recognize_deck_cards_from_region(num_cards=8):
    """
    Lets you select a region containing all deck cards, splits it into equal parts,
    recognizes each card using all templates in the folder, and prints the detected card names.
    """
    print("\n--- Deck Card Recognition Utility ---")
    print("1. Make sure your Clash Royale deck is visible on screen.")
    print("2. You will select a region containing ALL deck cards (in a row).")
    input("Press Enter to capture screen and begin selection...")

    # Load all templates from the folder
    folder_path = r"C:\gitsync\jan_projects\clash_royale_ai\all_cards_small_cropped2"
    all_templates = load_all_templates_from_folder(folder_path)
    if not all_templates:
        print(f"ERROR: No templates found in {folder_path}")
        return

    try:
        screenshot = pyautogui.screenshot()
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        return

    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    roi = cv2.selectROI("Select DECK region (all cards)", screenshot_cv, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow("Select DECK region (all cards)")

    if roi == (0, 0, 0, 0):
        print("Selection cancelled.")
        return

    x, y, w, h = roi
    deck_region = screenshot_cv[y:y+h, x:x+w]

    card_width = w // 4
    card_height = h // 2
    card_names = []
    for row in range(2):
        for col in range(4):
            cx = col * card_width
            cy = row * card_height
            card_img = deck_region[cy:cy+card_height, cx:cx+card_width]
            cv2.imshow(f"Card {row*4+col+1}", card_img)
            cv2.waitKey(0)

            matches = identify_card_in_slot(card_img, all_templates)
            best_name = matches[0][0] if matches and matches[0][0] is not None else "Unknown"
            card_names.append(best_name)

    print("\nDetected card names in region (left to right):")
    for idx, name in enumerate(card_names, 1):
        print(f"Card {idx}: {name}")
        print(f"\"{name}\": r\"C:\\gitsync\\jan_projects\\clash_royale_ai\\all_cards_small_cropped2\\{name}\",")

def get_rois_for_slots_utility(num_slots=4):
    """
    A utility to help you select the ROIs for your card slots.
    Run this function once, copy the output, and paste it into the CARD_SLOT_ROIS variable.
    """
    print("\n--- ROI Selection Utility ---")
    print("1. Make sure your Clash Royale game window is open and visible, showing the card hand.")
    print("2. You will be prompted to select a rectangle for each card slot.")
    print("3. Press ENTER in the console to capture the screen for selection.")
    input("Press Enter to capture screen and begin ROI selection...")

    try:
        screenshot = pyautogui.screenshot()
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        print("Make sure pyautogui is working correctly and you have a display server (e.g., not running headless).")
        return

    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    rois = []
    temp_screenshot_cv = screenshot_cv.copy() # Draw on a copy

    for i in range(num_slots):
        # Check if a template is available to suggest size
        example_template = next(iter(loaded_templates.values()), None)
        window_title = f"Select ROI for Slot {i+1}"
        if example_template is not None:
            h, w = example_template.shape[:2]
            window_title += f" (Approx {w}x{h})"

        while True:
            roi = cv2.selectROI(window_title, temp_screenshot_cv, fromCenter=False, showCrosshair=True)
            if roi == (0,0,0,0): # User pressed ESC or closed
                action = input("Selection cancelled for this slot. (s)kip slot, (r)etry, or (q)uit utility? [s/r/q]: ").lower()
                if action == 'q':
                    cv2.destroyAllWindows()
                    print("ROI selection aborted.")
                    return None
                elif action == 'r':
                    continue # Retry selection for this slot
                else: # Skip slot
                    rois.append(None) # Add a placeholder for skipped slot
                    cv2.destroyWindow(window_title)
                    break
            else:
                rois.append(roi)
                x,y,w,h = roi
                # Draw rectangle on the image to show what's been selected so far
                cv2.rectangle(temp_screenshot_cv, (x,y), (x+w, y+h), (0,255,0), 2)
                cv2.putText(temp_screenshot_cv, f"Slot {i+1}", (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
                cv2.destroyWindow(window_title)
                break


    print("\n--- Selected ROIs (x, y, w, h) ---")
    print("Copy the following list into the CARD_SLOT_ROIS variable in your script:")
    print("CARD_SLOT_ROIS = [")
    for i, r in enumerate(rois):
        if r:
            print(f"    ({r[0]}, {r[1]}, {r[2]}, {r[3]}),  # Slot {i+1}")
        else:
            print(f"    None,  # Slot {i+1} (Skipped)")
    print("]")

    cv2.imshow("All Selected ROIs (Press any key to close)", temp_screenshot_cv)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return rois

# --- Main Tracking Logic ---
def run_card_tracker():
    if not loaded_templates:
        print("No templates loaded, cannot start tracker.")
        return

    # Filter out None ROIs if user skipped some during utility
    valid_slot_rois = [roi for roi in CARD_SLOT_ROIS if roi is not None and len(roi) == 4]
    if not valid_slot_rois or len(valid_slot_rois) != 4 : # Check if all 4 are defined
        print(f"ERROR: CARD_SLOT_ROIS is not properly defined. Expected 4 valid slot definitions.")
        print(f"Current CARD_SLOT_ROIS: {CARD_SLOT_ROIS}")
        print("Please run the `get_rois_for_slots_utility()` or manually define them correctly.")
        return


    card_usage_counts = {card_name: 0 for card_name in loaded_templates}
    # Stores card names identified in each slot from the previous frame
    previous_hand_cards_in_slots = [None] * len(valid_slot_rois)

    print("\n--- Starting Card Tracker ---")
    print(f"Monitoring {len(valid_slot_rois)} card slots. Press Ctrl+C to stop.")
    print(f"Deck: {list(loaded_templates.keys())}")
    time.sleep(1) # Give a moment to switch to game window

    try:
        while True:
            current_hand_cards_in_slots = [None] * len(valid_slot_rois)
            # For debugging display
            slot_images_for_debug_view = []

            # Capture a single screenshot for all slots for efficiency
            try:
                overall_screenshot_pil = pyautogui.screenshot()
                # overall_screenshot_pil = cv2.imread("highres.png")
                overall_screenshot_cv = cv2.cvtColor(np.array(overall_screenshot_pil), cv2.COLOR_RGB2BGR)
            except Exception as e:
                print(f"Error taking screenshot: {e}. Skipping this frame.")
                time.sleep(POLL_INTERVAL)
                continue


            # 1. Identify cards in each slot for the current frame
            slot_matches = []
            for i, slot_roi in enumerate(valid_slot_rois):
                x, y, w, h = slot_roi
                # Ensure ROI coordinates are within the screenshot bounds
                if x < 0 or y < 0 or x + w > overall_screenshot_cv.shape[1] or y + h > overall_screenshot_cv.shape[0]:
                    print(f"Warning: Slot {i+1} ROI ({x},{y},{w},{h}) is out of screenshot bounds ({overall_screenshot_cv.shape[1]}x{overall_screenshot_cv.shape[0]}). Skipping slot.")
                    continue

                slot_img_cv = overall_screenshot_cv[y:y+h, x:x+w]
                slot_images_for_debug_view.append(slot_img_cv.copy()) # For debug display

                matches = identify_card_in_slot(slot_img_cv, loaded_templates)
                slot_matches.append(matches)

            # now pick one unique card per slot
            selected = pick_unique_cards(slot_matches)
            for idx, card_name in enumerate(selected, start=1):
                # print(f"Slot {idx}: {card_name}")
                # store for your usage‐count logic:
                current_hand_cards_in_slots[idx-1] = card_name

            # Debug: Display what's seen in slots
            if slot_images_for_debug_view:
                try:
                    # Find the minimum width and height among all slot images
                    min_height = min(img.shape[0] for img in slot_images_for_debug_view)
                    min_width = min(img.shape[1] for img in slot_images_for_debug_view)
                    # Resize all images to the minimum width and height
                    resized_slots = [
                        cv2.resize(img, (min_width, min_height))
                        for img in slot_images_for_debug_view
                    ]
                    combined_slots_img = np.hstack(resized_slots)

                    # --- Make debug window bigger ---
                    scale_factor = 2  # Increase to 2x size
                    display_img = cv2.resize(combined_slots_img, (combined_slots_img.shape[1]*scale_factor, combined_slots_img.shape[0]*scale_factor), interpolation=cv2.INTER_NEAREST)
                    cv2.imshow("Detected Slots", display_img)

                    # --- New: Show predictions overlay ---
                    annotated_slots = []
                    for idx, img in enumerate(resized_slots):
                        annotated = img.copy()
                        card_name = current_hand_cards_in_slots[idx]
                        label = card_name if card_name else "?"
                        cv2.putText(
                            annotated, label, (5, min_height - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA
                        )
                        annotated_slots.append(annotated)
                    combined_annotated = np.hstack(annotated_slots)
                    # --- Make prediction window bigger ---
                    display_annotated = cv2.resize(combined_annotated, (combined_annotated.shape[1]*scale_factor, combined_annotated.shape[0]*scale_factor), interpolation=cv2.INTER_NEAREST)
                    cv2.imshow("Slots with Predictions", display_annotated)
                    # -----------------------------------

                    if cv2.waitKey(1) & 0xFF == ord('q'): # Press 'q' in either window to quit
                        break
                except Exception as e:
                    print(f"Error creating debug view: {e}")

            # 2. Compare with previous hand to detect played cards
            #    A card is considered "played" if it was in the previous hand (set of cards)
            #    and is no longer in the current hand (set of cards).
            prev_hand_set = set(c for c in previous_hand_cards_in_slots if c is not None)
            current_hand_set = set(c for c in current_hand_cards_in_slots if c is not None)

            # Print current hand for debugging
            # print("\nCurrent Hand:")
            # for card_name in current_hand_cards_in_slots:
            #     if card_name is not None:
            #         print(f"  {card_name}")

            played_this_cycle = prev_hand_set - current_hand_set

            if played_this_cycle:
                # print("\n--- Detection ---")
                # print(f"Prev hand slots: {previous_hand_cards_in_slots}")
                # print(f"Curr hand slots: {current_hand_cards_in_slots}")
                for card_name in played_this_cycle:
                    if card_name in card_usage_counts: # Should always be true
                        card_usage_counts[card_name] += 1
                        print(f"  => Card Played: {card_name} \t \t (Total Uses: {card_usage_counts[card_name]})")

                # Display updated counts
                # print("Current Usage Counts:")
                # for name, count in sorted(card_usage_counts.items()):
                #     if count > 0: print(f"  {name}: {count}")
                # print("--------------------")

            # 3. Update previous_hand_state for the next iteration
            previous_hand_cards_in_slots = list(current_hand_cards_in_slots) # Make a copy

            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("\nTracker stopped by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
    finally:
        print("\n--- Final Card Usage Counts ---")
        for name, count in sorted(card_usage_counts.items()):
            print(f"  {name}: {count}")
        cv2.destroyAllWindows()


if __name__ == "__main__":
    # Run this utility to define your CARD_SLOT_ROIS
    # After running, copy the printed list into the CARD_SLOT_ROIS variable above.
    # get_rois_for_slots_utility()

    # Run this utility to recognize deck cards from a selected region
    # After running, copy the printed list into the DECK_CARD_TEMPLATES variable above.
    # recognize_deck_cards_from_region()

    # Run the main card tracker
    run_card_tracker()
