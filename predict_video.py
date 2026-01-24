import cv2
import numpy as np
from ultralytics import YOLO
import mss
import requests
import time
from typing import Dict, List, Optional

# Load model once at module level
try:
    model = YOLO("best.pt")
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
    raise


def show_preds_live_screen(
    region: Optional[Dict[str, int]] = None,
    conf_threshold: float = 0.15,
    show_fps: bool = True,
    api_url: Optional[str] = None,
):
    """
    Display live object detection on screen capture.

    Args:
        region: Screen region to capture (default: full primary monitor)
                Format: {"top": y, "left": x, "width": w, "height": h}
        conf_threshold: Confidence threshold for detections (0.0 to 1.0)
        show_fps: Whether to display FPS counter
        api_url: Optional URL to POST detection results
    """
    if region is None:
        region = {"top": 1, "left": 1, "width": 860, "height": 1400}
    with mss.mss() as sct:
        monitor = region
        frame_count = 0
        fps = 0
        fps_start_time = time.time()

        print(f"Starting live detection with confidence threshold: {conf_threshold}")
        print("Press 'q' to quit, 's' to save current frame")

        while True:
            try:
                loop_start = time.time()

                sct_img = sct.grab(monitor)
                frame = np.array(sct_img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

                outputs = model.predict(source=frame, conf=conf_threshold, verbose=False)
                boxes = outputs[0].boxes.xyxy.cpu().numpy() if outputs[0].boxes.xyxy.numel() > 0 else []
                scores = outputs[0].boxes.conf.cpu().numpy() if outputs[0].boxes.conf.numel() > 0 else []
                classes = outputs[0].boxes.cls.cpu().numpy() if outputs[0].boxes.cls.numel() > 0 else []
                names = outputs[0].names

                # Store detections for API
                detections = []

                for i, det in enumerate(boxes):
                    class_id = int(classes[i]) if len(classes) > i else -1
                    confidence = scores[i] if len(scores) > i else 0.0
                    label = f"{names[class_id]}: {confidence:.2f}" if class_id in names else f"ID {class_id}: {confidence:.2f}"

                    # Store detection info
                    detections.append(
                        {
                            "card_name": names.get(class_id, f"Unknown_{class_id}"),
                            "confidence": float(confidence),
                            "bbox": [
                                int(det[0]),
                                int(det[1]),
                                int(det[2]),
                                int(det[3]),
                            ],
                        }
                    )

                    # Draw rectangle
                    cv2.rectangle(
                        frame,
                        (int(det[0]), int(det[1])),
                        (int(det[2]), int(det[3])),
                        color=(0, 0, 255),
                        thickness=2,
                        lineType=cv2.LINE_AA,
                    )
                    # Draw label with background for better visibility
                    label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                    cv2.rectangle(
                        frame,
                        (int(det[0]), int(det[1]) - label_size[1] - 10),
                        (int(det[0]) + label_size[0], int(det[1])),
                        (0, 255, 0),
                        -1,
                    )
                    cv2.putText(
                        frame,
                        label,
                        (int(det[0]), int(det[1]) - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 0, 0),
                        2,
                        cv2.LINE_AA,
                    )

                # Calculate and display FPS
                if show_fps:
                    frame_count += 1
                    if time.time() - fps_start_time >= 1.0:
                        fps = frame_count
                        frame_count = 0
                        fps_start_time = time.time()

                    cv2.putText(
                        frame,
                        f"FPS: {fps}",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0,
                        (0, 255, 0),
                        2,
                        cv2.LINE_AA,
                    )
                    cv2.putText(
                        frame,
                        f"Detections: {len(detections)}",
                        (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0,
                        (0, 255, 0),
                        2,
                        cv2.LINE_AA,
                    )

                cv2.imshow("Live Screen Predictions", frame)

                # Send detection results to API if URL provided
                if api_url and detections:
                    detection_data = {
                        "hand": detections,
                        "my_troops": [],
                        "enemy_troops": [],
                        "timestamp": time.time(),
                    }
                    try:
                        response = requests.post(api_url, json=detection_data, timeout=0.5)
                        if response.status_code != 200:
                            print(f"API error: {response.status_code} - {response.text}")
                    except requests.exceptions.Timeout:
                        print("API request timeout (continuing...)")
                    except Exception as e:
                        print(f"Error sending detections to API: {e}")

                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    print("Quitting...")
                    break
                elif key == ord("s"):
                    filename = f"capture_{int(time.time())}.png"
                    cv2.imwrite(filename, frame)
                    print(f"Saved frame to {filename}")

            except KeyboardInterrupt:
                print("\nInterrupted by user")
                break
            except Exception as e:
                print(f"Error in main loop: {e}")
                continue

        cv2.destroyAllWindows()


if __name__ == "__main__":
    # Example usage with custom configuration
    # Uncomment and modify as needed:

    # Custom region (e.g., for Clash Royale window)
    # custom_region = {"top": 26, "left": 250, "width": 456, "height": 984}

    # With API integration
    # show_preds_live_screen(
    #     region=custom_region,
    #     conf_threshold=0.2,
    #     show_fps=True,
    #     api_url="http://localhost:5000/update_detections"
    # )

    # Default usage
    show_preds_live_screen(conf_threshold=0.09, show_fps=True)
