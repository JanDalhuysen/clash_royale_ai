import cv2
import numpy as np
from ultralytics import YOLO
import mss
import requests

model = YOLO('best.pt')

# 250, 26, 250+456, 1010
def show_preds_live_screen(region={'top': 1, 'left': 1, 'width': 860, 'height': 1400}):
    with mss.mss() as sct:
        monitor = sct.monitors[1] if region is None else region
        while True:
            sct_img = sct.grab(monitor)
            frame = np.array(sct_img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            outputs = model.predict(source=frame, conf=0.15, verbose=True)
            boxes = outputs[0].boxes.xyxy.cpu().numpy() if outputs[0].boxes.xyxy.numel() > 0 else []
            scores = outputs[0].boxes.conf.cpu().numpy() if outputs[0].boxes.conf.numel() > 0 else []
            classes = outputs[0].boxes.cls.cpu().numpy() if outputs[0].boxes.cls.numel() > 0 else []
            names = outputs[0].names

            for i, det in enumerate(boxes):
                class_id = int(classes[i]) if len(classes) > i else -1
                label = f"{names[class_id]}: {scores[i]:.2f}" if class_id in names else f"ID {class_id}: {scores[i]:.2f}"
                # Draw rectangle
                cv2.rectangle(
                    frame,
                    (int(det[0]), int(det[1])),
                    (int(det[2]), int(det[3])),
                    color=(0, 0, 255),
                    thickness=2,
                    lineType=cv2.LINE_AA
                )
                # Draw label
                cv2.putText(
                    frame,
                    label,
                    (int(det[0]), int(det[1]) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2,
                    cv2.LINE_AA
                )

            cv2.imshow("Live Screen Predictions", frame)
            # Send detection results to Flask API
            detection_data = {
                "hand": [
                    {"card_name": names[class_id], "elixir": int(scores[i] * 10) // 2 + 1}  # Mock elixir based on confidence
                    for i, det in enumerate(boxes)
                ],
                "my_troops": [],
                "enemy_troops": []
            }
            
            # try:
            #     response = requests.post("http://localhost:5000/update_detections", json=detection_data)
            #     if response.status_code != 200:
            #         print("Failed to update detections:", response.text)
            # except Exception as e:
            #     print("Error sending detections to API:", e)
                
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

if __name__ == "__main__":
    show_preds_live_screen()


# conda install -c conda-forge python-mss
import requests
