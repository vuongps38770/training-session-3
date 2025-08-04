import cv2
from ultralytics import YOLO

# Load model
model = YOLO("best.pt")

# Camera
cap = cv2.VideoCapture(1)
# greenLight/green_E

# Thông số vật thể và tiêu cự
KNOWN_WIDTH = 1.0  # cm
KNOWN_DISTANCE = 5.0 # cm
REFERENCE_WIDTH = 100  # pixel (box_width tại khoảng cách 50cm)
FOCAL_LENGTH = (REFERENCE_WIDTH * KNOWN_DISTANCE) / KNOWN_WIDTH  # tính tiêu cự

def estimate_distance(box_width_px):
    if box_width_px == 0:
        return -1
    return (KNOWN_WIDTH * FOCAL_LENGTH) / box_width_px

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)
    annotated_frame = frame.copy()

    for r in results:
        for box in r.boxes:
            if box.conf > 0.5:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                box_width = x2 - x1
                distance_cm = estimate_distance(box_width)

                conf = float(box.conf)
                cls = int(box.cls)
                label = f"{model.names[cls]} {conf:.2f} - {distance_cm:.1f}cm"

                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(annotated_frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow("Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
