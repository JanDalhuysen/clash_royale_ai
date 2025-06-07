# Clash Royale AI

This project contains scripts for automating and analyzing Clash Royale gameplay:

## Main Scripts

1. **get_data.py**  
   Captures game screenshots at regular intervals

2. **get_data_on_touch.py**  
   Intercepts ADB touch events to convert screen coordinates to images and save touch points

3. **labler.py**  
   Image labeling tool for creating YOLO training data with custom class groupings

4. **train.py**  
   Trains YOLO model using collected training data

5. **predict_video.py**  
   Live screen detector using YOLO model on screen capture

## Legacy/Utility Scripts

1. **by_elixir.py**  
   Parses HTML to extract Clash Royale cards grouped by elixir cost

2. **adb_event_to_xy.py**  
   Converts ADB touch events to x y and displays them as red dots on a white image using OpenCV.

3. **old_labler.py**  
   Legacy version of the image labeling tool

4. **predict.py**  
   Runs YOLO inference on static images and displays results

5. **main.py**  
   Contains various experimental utilities including OCR and button detection

6. **card_counter.py**  
   Tracks card usage by matching on-screen cards using template matching

## Usage

For capturing game data at regular intervals:

```bash
python get_data.py
```

For capturing game data only when a card is placed:

```bash
adb shell getevent | python adb_event_to_xy.py
```

For labeling:

```bash
python labler.py
```

For live prediction:

```bash
python predict_video.py
```

## Todo

- [ ] Maybe seperate model for cards and troops

![Results](results.png)
