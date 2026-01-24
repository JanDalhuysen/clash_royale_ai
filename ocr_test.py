import cv2
import pytesseract

# Load the image
image = cv2.imread("16.png")
clone = image.copy()
roi = None


def select_roi(event, x, y, flags, param):
    global roi, start_point, drawing, image

    if event == cv2.EVENT_LBUTTONDOWN:
        start_point = (x, y)
        drawing = True

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        img2 = clone.copy()
        cv2.rectangle(img2, start_point, (x, y), (0, 255, 0), 2)
        cv2.imshow("Select ROI", img2)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        end_point = (x, y)
        roi = (start_point[0], start_point[1], end_point[0], end_point[1])
        cv2.rectangle(image, start_point, end_point, (0, 255, 0), 2)
        cv2.imshow("Select ROI", image)


drawing = False
start_point = (-1, -1)

cv2.namedWindow("Select ROI")
cv2.setMouseCallback("Select ROI", select_roi)
cv2.imshow("Select ROI", image)

print("Draw a rectangle to select the area for OCR, then press any key.")

cv2.waitKey(0)
cv2.destroyAllWindows()

if roi:
    x1, y1, x2, y2 = roi
    x1, x2 = sorted([x1, x2])
    y1, y2 = sorted([y1, y2])
    # Print coordinates of the selected area
    print(f"Selected area coordinates: ({x1}, {y1}), ({x2}, {y2})")

    selected_area = clone[y1:y2, x1:x2]
    text = pytesseract.image_to_string(selected_area, lang="eng")
    print(f"Detected text: {text.strip()}")
    cv2.imshow("Selected Area", selected_area)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No area selected.")
    cv2.destroyAllWindows()


cv2.destroyAllWindows()
