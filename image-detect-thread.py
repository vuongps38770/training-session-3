import threading
import queue
from ultralytics import YOLO
import cv2
import time

model = YOLO("best.pt")

image_queue = queue.Queue()

def yolo_worker():
    while True:
        image_path = image_queue.get()
        if image_path is None:
            break  

        results = model(image_path)

        for result in results:
            for box in result.boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                xyxy = box.xyxy[0].tolist()
                print(f"[{image_path}] Class: {model.names[cls]}, Confidence: {conf:.2f}, Box: {xyxy}")

        image_queue.task_done()

threading.Thread(target=yolo_worker, daemon=True).start()

def receive_image_simulation():
    for i in range(100):
        path = f"images/frame_{i}.jpg"
        image_queue.put(path)
        time.sleep(0.1)

receive_image_simulation()
