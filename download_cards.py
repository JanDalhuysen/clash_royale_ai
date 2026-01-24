import os
import requests
import re

# Read links from the markdown file
LINKS_FILE = "all_cards_links.md"
OUTPUT_DIR = "data/cards_dataset/images"
LABELS_DIR = "data/cards_dataset/labels"  # For if we want to make classification folders or detection labels

# We will create a Classification Dataset structure for YOLOv8/11 Cls
# structure: data/cards_dataset/train/class_name/image.png
TRAIN_DIR = "data/cards_dataset/train"
VAL_DIR = "data/cards_dataset/val"


def download_cards():
    if not os.path.exists(LINKS_FILE):
        print(f"Error: {LINKS_FILE} not found.")
        return

    os.makedirs(TRAIN_DIR, exist_ok=True)
    os.makedirs(VAL_DIR, exist_ok=True)

    with open(LINKS_FILE, "r") as f:
        lines = f.readlines()

    print(f"Found {len(lines)} links.")

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        # Extract filename from URL
        filename = line.split("/")[-1]
        # Remove extension to get class name
        class_name = os.path.splitext(filename)[0]

        # Determine paths
        # We put everything in train first. You should manually move some to val or split programmatically.
        class_dir = os.path.join(TRAIN_DIR, class_name)
        os.makedirs(class_dir, exist_ok=True)

        save_path = os.path.join(class_dir, filename)

        if os.path.exists(save_path):
            print(f"Skipping {class_name} (already exists)")
            continue

        print(f"Downloading {class_name}...")
        try:
            response = requests.get(line)
            if response.status_code == 200:
                with open(save_path, "wb") as f:
                    f.write(response.content)
            else:
                print(f"Failed to download {line}")
        except Exception as e:
            print(f"Error downloading {line}: {e}")

    print("\nDownload complete.")
    print("For Classification Training: Ensure you split some images into the 'val' folder.")
    print("For Detection Training: You will need to take these images and paste them onto backgrounds to create synthetic detection data.")


if __name__ == "__main__":
    download_cards()
