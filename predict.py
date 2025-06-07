import cv2
import sys

from ultralytics import YOLO

model = YOLO('best.pt')

def show_preds_image(image_path):
    print(model.info())
    image = cv2.imread(image_path)
    print("Loaded image shape:", image.shape)

    outputs = model.predict(source=image_path, conf=0.05)
    print(outputs)

    print("***")
    print(outputs[0].names)
    print("***")

    # Get boxes as numpy array
    boxes = outputs[0].boxes.xyxy.cpu().numpy()
    print("boxes:", boxes)

    if boxes.shape[0] == 0:
        print("No detections found.")
    else:
        for det in boxes:
            cv2.rectangle(
                image,
                (int(det[0]), int(det[1])),
                (int(det[2]), int(det[3])),
                color=(0, 0, 255),
                thickness=2,
                lineType=cv2.LINE_AA
            )
    
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

if __name__ == "__main__":
    image_path = sys.argv[1]
    image_with_overlay = show_preds_image(image_path)
    # save image with overlay
    # cv2.imwrite("image_with_overlay.jpg", image_with_overlay)
    cv2.imshow("Image with Overlay", image_with_overlay)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # No need for exit() or sys.exit()
