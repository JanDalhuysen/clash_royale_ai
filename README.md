# Clash Royale AI

This project contains scripts for automating and analyzing Clash Royale gameplay through computer vision and machine learning:

## Main Scripts

1. **get_data.py**  
   Captures game screenshots at fixed intervals (default 5 seconds) for building training datasets. This script is useful for collecting a broad range of gameplay scenarios. It saves the screenshots to the `data` folder, naming them sequentially.

2. **get_data_on_touch.py**  
   Intercepts ADB touch events to capture screenshots + touch coordinates when cards are played (requires ADB device connection). This is ideal for creating a dataset focused on card placements. It also saves screenshots to the `data` folder, triggered by touch events, and saves touch event data to corresponding `.txt` files in the `touch_events` folder.

3. **labler.py**  
   Image labeling tool for creating YOLO training data with card+troop classes grouped by elixir cost for faster labeling. This script provides a GUI for annotating images with bounding boxes and class labels. It saves the labels in YOLO format to the `labels` folder, making it easier to train a detection model.

4. **train.py**  
   Trains custom YOLOv8 model using collected training data with grouped class weights. This script uses the YOLOv8 framework to train a model on your labeled dataset. It requires a `data.yaml` file to configure the dataset paths and class names, and outputs training metrics and model weights to the `runs/detect` directory.

5. **predict_video.py**  
   Real-time screen detector that uses trained YOLO model to identify cards and troops during gameplay. This script uses the trained YOLO model to detect cards and troops in real-time from a screen capture. It displays the results with bounding boxes and class labels, providing a live view of the game state.

## Legacy/Utility Scripts

1. **by_elixir.py**  
   Scrapes Clash Royale card data from HTML widgets and groups cards by elixir cost. This script extracts card names and elixir costs from a static HTML page. It's useful for creating a mapping between card names and their elixir costs, which can be used for data analysis or model training.

2. **by_category.py**  
   Scrapes Clash Royale card data from HTML widgets and groups cards by category (e.g., air, building, etc.). Similar to `by_elixir.py`, this script extracts card names and categories from a static HTML page. It helps in organizing cards based on their roles, providing insights into deck compositions.

3. **adb_event_to_xy.py**  
   Converts binary ADB touch events to (x,y) coordinates and overlays them on a display image. This script takes ADB touch event data and converts it into screen coordinates. It's useful for visualizing touch inputs on the screen, helping to understand user interactions.

4. **old_labler.py**  
   Original labeling tool without elixir-based class grouping (unused in current workflow). This is a legacy labeling tool that doesn't group classes by elixir cost. It's kept for historical purposes but is not used in the current workflow, as `labler.py` provides more advanced features.

5. **predict.py**  
   Runs YOLO inference on static image files and displays detection results. This script runs the YOLO model on a single image and displays the detected objects. It's useful for testing the model on individual images and verifying its performance.

6. **main.py**  
   Experiments for OCR, template matching and UI detection (core logic moved to card_counter.py). This script contains various experiments with OCR, template matching, and UI detection. The core logic has been moved to `card_counter.py` for better organization and maintainability.

7. **card_counter.py**  
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

![Results](results.png)
