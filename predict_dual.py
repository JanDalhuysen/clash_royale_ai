import cv2
import numpy as np
from ultralytics import YOLO
import mss
import time

# --- Configuration ---
# You should train two separate models:
# 1. cards.pt: Trained on CARD images (cropped from UI or downloaded)
# 2. troops.pt: Trained on TROOP sprites/gameplay
# NOTE: Changing this to a DETECTION model ('yolo11n.pt') because the code below expects bounding boxes.
# If you want to use classification ('-cls.pt'), you must modify the code to crop 4 fixed slots.
CARD_MODEL_PATH = 'best.pt'     # Changed from -cls.pt to .pt for detection demo
TROOP_MODEL_PATH = 'best.pt'    # Example: Detection model for troops

# Define the region for the Card Hand (approximate, adjust to your screen)
# Left, Top, Width, Height
# Assuming 1080x2400 resolution or similar ratio
HAND_REGION_Y_START = 0.8 # Start at 80% of screen height
# Exact coordinates depend on your resolution. 
# For the script, we will dynamic crop based on frame size.

def run_dual_inference():
    # 1. Load the two specialized models
    # Note: Using YOLOv11 is recommended for speed/accuracy balance.
    print("Loading models...")
    try:
        # We use a placeholder here. In reality, load your trained 'cards.pt' and 'troops.pt'
        model_troops = YOLO(TROOP_MODEL_PATH) 
        model_cards = YOLO(CARD_MODEL_PATH) 
    except Exception as e:
        print(f"Error loading models: {e}")
        print("Please ensure you have trained models. Using generic yolov8n as fallback for demo.")
        model_troops = YOLO('best.pt')
        model_cards = YOLO('best.pt')

    # 2. Setup Screen Capture - Left Third Only
    with mss.mss() as sct:
        full_monitor = sct.monitors[1] # Main monitor
        
        # Calculate left third region
        monitor = {
            "top": full_monitor["top"],
            "left": full_monitor["left"],
            "width": full_monitor["width"] // 3,
            "height": full_monitor["height"]
        }
        
        while True:
            # Capture Frame (left third only)
            t0 = time.time()
            sct_img = sct.grab(monitor)
            frame = np.array(sct_img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            h = frame.shape[0]

            # --- CARD DETECTION (Hand) ---
            # Crop the bottom area where cards always live
            # This makes inference faster and easier for the model
            hand_y_start = int(h * 0.78) 
            hand_img = frame[hand_y_start:h, :]
            
            # Predict Cards
            # specific config for cards (confidence can be high since UI is clear)
            card_results = model_cards.predict(hand_img, conf=0.55, verbose=False)
            
            # --- TROOP DETECTION (Arena) ---
            # Crop the arena (exclude top bar and bottom hand if desired to save pixels)
            # Or just run on full frame if troops can be anywhere.
            # Usually better to run on full frame effectively or just the play area.
            arena_img = frame[0:hand_y_start, :] 
            
            # Predict Troops
            troop_results = model_troops.predict(arena_img, conf=0.55, verbose=False)

            # --- VISUALIZATION ---
            
            # Draw Card Results (Offset y coordinates back to original frame)
            for r in card_results:
                boxes = r.boxes
                if boxes is None:
                    # Handle Classification Model Output (Top-1 class)
                    # This implies the user used a -cls model on the whole hand strip, which isn't ideal but we shouldn't crash.
                    if r.probs is not None:
                        top1 = r.probs.top1
                        conf = r.probs.top1conf
                        label = f"Class: {r.names[top1]} {conf:.2f}"
                        cv2.putText(frame, label, (10, int(hand_y_start) + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    continue

                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    label = f"Card: {r.names[cls]} {conf:.2f}"
                    
                    # Offset y by hand_y_start
                    abs_y1 = int(y1 + hand_y_start)
                    abs_y2 = int(y2 + hand_y_start)
                    
                    cv2.rectangle(frame, (int(x1), abs_y1), (int(x2), abs_y2), (255, 0, 0), 2)
                    cv2.putText(frame, label, (int(x1), abs_y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            # Draw Troop Results
            for r in troop_results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    label = f"Troop: {r.names[cls]} {conf:.2f}"
                    
                    # Arena img starts at 0,0 so no offset needed for y (unless you cropped top)
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    cv2.putText(frame, label, (int(x1), int(y1) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            fps = 1 / (time.time() - t0)
            cv2.putText(frame, f"FPS: {fps:.1f}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            
            cv2.imshow("Dual Model Clash AI", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_dual_inference()
