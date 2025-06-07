# Clash Royale AI

This project contains scripts for automating and analyzing Clash Royale gameplay through computer vision and machine learning:

## Main Scripts

1. **get_data.py**  
   Captures game screenshots at fixed intervals (default 5 seconds) for building training datasets

2. **get_data_on_touch.py**  
   Intercepts ADB touch events to capture screenshots + touch coordinates when cards are played (requires ADB device connection)

3. **labler.py**  
   Image labeling tool for creating YOLO training data with card+troop classes grouped by elixir cost for faster labeling

4. **train.py**  
   Trains custom YOLOv8 model using collected training data with grouped class weights

5. **predict_video.py**  
   Real-time screen detector that uses trained YOLO model to identify cards and troops during gameplay

## Legacy/Utility Scripts

1. **by_elixir.py**  
   Scrapes Clash Royale card data from HTML widgets and groups cards by elixir cost

2. **adb_event_to_xy.py**  
   Converts binary ADB touch events to (x,y) coordinates and overlays them on a display image

3. **old_labler.py**  
   Original labeling tool without elixir-based class grouping (unused in current workflow)

4. **predict.py**  
   Runs YOLO inference on static image files and displays detection results

5. **main.py**  
   Experiments for OCR, template matching and UI detection (core logic moved to card_counter.py)

6. **card_counter.py**  
   Tracks active cards using template matching with adjustable confidence thresholds

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

![Results](results.png)
