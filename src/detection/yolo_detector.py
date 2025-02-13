import cv2
import numpy as np
from ultralytics import YOLO

class YOLODetector:
    def __init__(self, model_path='yolov8n.pt'):
        
        self.model = YOLO(model_path)

    def detect(self, frame):
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = self.model(frame_rgb, conf=0.2, iou=0.4, augment=True)[0]
        detections = []
        if results.boxes is not None and len(results.boxes) > 0:
            boxes = results.boxes.xyxy.cpu().numpy()
            classes = results.boxes.cls.cpu().numpy()
            confidences = results.boxes.conf.cpu().numpy()
            
            print("Detections:", boxes, classes, confidences)
            for i, cls in enumerate(classes):
                
                if confidences[i] >= 0.5:
                    x1, y1, x2, y2 = boxes[i]
                    detections.append((int(x1), int(y1), int(x2), int(y2), int(cls), float(confidences[i])))
        print("Detected boxes:", detections)
        return detections
