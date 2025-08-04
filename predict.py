from ultralytics import YOLO
import cv2

# Các tham số đã biết
KNOWN_WIDTH = 20.0  # cm (vật thể thật)
FOCAL_LENGTH = 800  # phải tính trước từ ảnh chuẩn

# Load model
model = YOLO("runs/detect/train3/weights/best.pt")  

# Đọc ảnh
img_path = "img.jpg"
image = cv2.imread(img_path)

# Dự đoán
results = model(img_path)

for result in results:
    for box in result.boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        box_width = x2 - x1

        # Tính khoảng cách
        if box_width > 0:
            distance_cm = (KNOWN_WIDTH * FOCAL_LENGTH) / box_width
        else:
            distance_cm = -1  # lỗi nếu box_width = 0

        print(f"Class: {model.names[cls]}, Confidence: {conf:.2f}, Box: {[x1, y1, x2, y2]}, Distance: {distance_cm:.2f} cm")

        # Hiển thị lên ảnh
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, f"{distance_cm:.1f} cm", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

cv2.imshow("Result", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
