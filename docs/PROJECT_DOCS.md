# Clash Royale AI Project Documentation

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
