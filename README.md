# Clash Royale AI

<img width="754" height="738" alt="labler" src="https://github.com/user-attachments/assets/330cc99a-a90b-4906-8d82-05c295759fe6" />

- download_cards.py
  extract_sprites.py
  generate_troop_data.py
  predict_dual.py

- auto_label.py
  data.yaml
  get_data.py
  labler.py
  predict_video.py

- train.py

## Key Files Overview

### Data Collection & Labeling

- **`get_data.py`**: Captures screenshots of the game (typically from an emulator like BlueStacks) at set intervals. Used to gather raw images for the dataset.
- **`labler.py`**: A manual labeling tool built with OpenCV. It allows you to draw bounding boxes around cards and troops and assign classes (cards, troops, elixir). It supports loading existing YOLO labels and saving new ones.
- **`auto_label.py`**: Automates labeling for cards using template matching. It compares screenshots against templates in the `templates/` directory to generate initial bounding boxes.
- **`download_cards.py`**: Downloads official card images from links in `all_cards_links.md` to build a base dataset of card assets.

### Synthetic Data Generation

- **`extract_sprites.py`**: Processes sprite sheets (from `sprite_sheets/`) to extract individual character sprites with transparency. These are saved to `extracted_sprites/`.
- **`generate_troop_data.py`**: The core synthetic data generator. It takes extracted sprites and overlays them onto arena backgrounds (`backgrounds/`) to create thousands of training images with perfect YOLO labels (`data/troops_dataset/`). This is crucial for training the object detector to recognize troops in various positions and scales.

### Training & Model

- **`train.py`**: A script to train the YOLOv8/v11 model. It uses the configuration in `data.yaml`.
- **`data.yaml`**: The YOLO configuration file defining the paths to train/val datasets and the list of 119+ class names.
- **`predict_dual.py`**: A real-time inference script that visualizes the model's performance. It runs two models (one for cards, one for troops) on a live screen capture and draws bounding boxes.
- **`predict_video.py`**: Similar to `predict_dual.py`, but designed to send detection data to the game API server.

### Runtime & Agent

- **`game_api.py`**: A Flask server acting as the central state manager. It receives vision data from `predict_video.py` and exposes endpoints (`/get_game_state`, `/place_card`) for the AI agent.
- **`mcp_server.js`**: An MCP (Model Context Protocol) server. It connects an LLM (like Claude or Gemini) to the `game_api.py`. It allows the LLM to query the game state and execute moves.

---

## Example Workflows

### 1. Manual Data Collection and Labeling

Use this workflow to create a high-quality "real" dataset from actual gameplay.

1.  **Capture Images**:
    - Open your game emulator.
    - Run `python get_data.py`.
    - This will save screenshots to the `data/` folder every few seconds. Play a match or watch replays while this runs.
2.  **Label Images**:
    - Run `python labler.py`.
    - **Controls**:
      - `C` / `T`: Switch between **Card** and **Troop** mode.
      - `1-9`: Select Elixir group (classes are grouped by elixir cost).
      - `N` / `P`: Next / Previous class in the group.
      - `Mouse Drag`: Draw a box around an object.
      - `Space`: Save labels and move to the next image.
    - Labels are saved to the `labels/` directory in YOLO format.

### 2. All Synthetic Data Generation

Use this workflow to mass-produce training data without manual labeling.

1.  **Prepare Assets**:
    - Ensure `sprite_sheets/` contains sprite sheets of troops.
    - Ensure `backgrounds/` contains arena images.
    - Run `python extract_sprites.py` to populate `extracted_sprites/`.
2.  **Generate Data**:
    - Edit `generate_troop_data.py`:
      - Check `CLASS_MAP` to ensure sprite folder names map to the correct class IDs (matching `data.yaml`).
      - Set `NUM_IMAGES_TO_GENERATE` (e.g., 5000).
    - Run `python generate_troop_data.py`.
    - This creates images in `data/troops_dataset/images` and labels in `data/troops_dataset/labels`.
3.  **Train**:
    - Update `data.yaml` to point to your new synthetic dataset paths.
    - Run `python train.py` to train the YOLO model.

### 3. Running the Model to Play

Use this workflow to let the AI agent perceive and play the game.

1.  **Start the Game State API**:
    - Run `python game_api.py`.
    - This starts a local server (usually on port 5000) that holds the current game info.
2.  **Start the Vision System**:
    - Ensure you have a trained model (`best.pt`).
    - Edit `predict_video.py` (or `predict_dual.py`) to uncomment the API call section (look for `requests.post`).
    - Run `python predict_video.py`.
    - Position your emulator window so the script captures the correct region. It will now continuously send detection data (cards in hand, troops on board) to the API.
3.  **Start the AI Agent**:
    - Install dependencies: `npm install` (ensure `@modelcontextprotocol/sdk` is installed).
    - Run `node mcp_server.js`.
    - Connect your MCP client (e.g., an LLM interface) to this server.
    - **Agent Loop**: The LLM will now be able to call `get_game_state` to "see" the board and `place_card_at_xy` to play cards via the API.

This project contains scripts for automating and analyzing Clash Royale gameplay through computer vision and machine learning:

## Main Scripts

1. **get_data.py**
   Captures game screenshots at fixed intervals (default 5 seconds) for building training datasets. This script is useful for collecting a broad range of gameplay scenarios. It saves the screenshots to the `data` folder, naming them sequentially.

2. **get_data_on_touch.py**
   Intercepts ADB touch events to capture screenshots + touch coordinates when cards are played (requires ADB device connection). This is ideal for creating a dataset focused on card placements. It also saves screenshots to the `data` folder, triggered by touch events, and saves touch event data to corresponding `.txt` files in the `touch_events` folder.

3. **labler.py**
   Image labeling tool for creating YOLO training data with card+troop classes grouped by elixir cost for faster labeling. This script provides a GUI for annotating images with bounding boxes and class labels. It saves the labels in YOLO format to the `labels` folder, making it easier to train a detection model.

4. **auto_label.py**
   Automated label generator using multi-scale template matching to create YOLO format labels for card images. This script automatically detects cards in images using template matching at various scales, and generates corresponding YOLO label files. It's useful for quickly creating large amounts of training data with minimal manual effort.

5. **train.py**
   Trains custom YOLOv8 model using collected training data with grouped class weights. This script uses the YOLOv8 framework to train a model on your labeled dataset. It requires a `data.yaml` file to configure the dataset paths and class names, and outputs training metrics and model weights to the `runs/detect` directory.

6. **predict_video.py**
   Real-time screen detector that uses trained YOLO model to identify cards and troops during gameplay. This script uses the trained YOLO model to detect cards and troops in real-time from a screen capture. It displays the results with bounding boxes and class labels, providing a live view of the game state.

## Legacy/Utility Scripts

1. **by_elixir.py**
   Scrapes Clash Royale card data from HTML widgets and groups cards by elixir cost. This script extracts card names and elixir costs from a static HTML page. It's useful for creating a mapping between card names and their elixir costs, which can be used for data analysis or model training.

2. **by_category.py**
   Scrapes Clash Royale card data from HTML widgets and groups cards by category (e.g., air, building, etc.). Similar to `by_elixir.py`, this script extracts card names and categories from a static HTML page. It helps in organizing cards based on their roles, providing insights into deck compositions.

3. **adb_event_to_xy.py**
   Converts binary ADB touch events to (x,y) coordinates and overlays them on a display image. This script takes ADB touch event data and converts it into screen coordinates. It's useful for visualizing touch inputs on the screen, helping to understand user interactions.

4. **bulk_crop_cards.py**
   Batch cropping utility that crops images to keep only the middle third of card images. This script can be used to standardize card image dimensions by cropping them to focus on the central portion of the image.

5. **ocr_test.py**
   Interactive test for OCR functionality that lets you select a region of an image to analyze. This script provides a way to test OCR capabilities by allowing users to draw a rectangle on an image to select a specific area for text recognition.

6. **old_labler.py**
   Original labeling tool without elixir-based class grouping (unused in current workflow). This is a legacy labeling tool that doesn't group classes by elixir cost. It's kept for historical purposes but is not used in the current workflow, as `labler.py` provides more advanced features.

7. **predict.py**
   Runs YOLO inference on static image files and displays detection results. This script runs the YOLO model on a single image and displays the detected objects. It's useful for testing the model on individual images and verifying its performance.

8. **main.py**
   Experiments for OCR, template matching and UI detection (core logic moved to card_counter.py). This script contains various experiments with OCR, template matching, and UI detection. The core logic has been moved to `card_counter.py` for better organization and maintainability.

9. **card_counter.py**
   Tracks active cards using template matching with adjustable confidence thresholds. This script uses template matching to identify cards on the screen. It's useful for tracking the cards played by both the player and the opponent, providing insights into game strategy.

## Usage

Capture game screenshots periodically (5s intervals):

```bash
python get_data.py
```

Capture screenshots on card placement (requires ADB):

```bash
adb shell getevent | python get_data_on_touch.py
```

Label collected images with YOLO format:

```bash
python labler.py
```

Train the detection model (uses GPU if available):

```bash
python train.py
```

Run live game detection:

```bash
python predict_video.py
```

## Workflow

The recommended workflow for building and using the detection system:

1. **Data Collection**
   - Use `get_data_on_touch.py` when playing matches to capture card placements with touch events
   - Use `get_data.py` for general gameplay context without ADB

2. **Labeling**
   - Use `labler.py` to annotate card/troop positions in collected images
   - Labels follow YOLOv8 format with elixir-based classes

3. **Training**
   - Configure `data.yaml` with dataset paths and class names
   - Run `train.py` to create detection models
   - Monitor training metrics in runs/detect directory

4. **Deployment**
   - Use `predict_video.py` for real-time detection during gameplay
   - Analyze card placement patterns with detection outputs

## Todo

- [ ] Separate model for cards and troops (improve detection accuracy)
- [ ] Add ADB integration for automated gameplay
- [ ] Collect card deployment positions (location + timing) and game outcome data
- [ ] Train reinforcement learning model for card placement recommendations
- [ ] Implement opponent troop detection using side-of-arena position analysis
- [ ] Collect game state data (elixir counts, tower health) to inform decision-making.
- [ ] Train a model to predict optimal card placements based on game state and opponent actions.
- [ ] Explore methods to differentiate between own troops and opponent troops (e.g., color analysis, position relative to towers).

![Results](results.png)
