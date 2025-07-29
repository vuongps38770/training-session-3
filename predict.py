from ultralytics import YOLO

model = YOLO("best.pt")  
results = model("image.png")  


for result in results:
    for box in result.boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        xyxy = box.xyxy[0].tolist()
        print(f"Class: {model.names[cls]}, Confidence: {conf:.2f}, Box: {xyxy}")
