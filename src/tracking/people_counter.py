# src/tracking/people_counter.py
import cv2
import time
import threading
import numpy as np
from src.detection.yolo_detector import YOLODetector
from src.tracking.centroid_tracker import CentroidTracker
from src.config.config import INITIAL_POLYGON

class PeopleCounter:
    def __init__(self, video_source=0, polygon=INITIAL_POLYGON):
        self.video_source = video_source  
        self.polygon = np.array(polygon, np.int32)
        self.running = False
        self.detector = YOLODetector()  
        # Naikkan distanceThreshold agar tracker lebih akurat (disini diset ke 100)
        self.tracker = CentroidTracker(distanceThreshold=150)
        self.count_in = 0
        self.count_out = 0
        self.object_states = {}  
        self.last_frame = None   
        self.last_detections = []  
        self.last_counts = {}      

    def run(self):
        cap = cv2.VideoCapture(self.video_source)
        if not cap.isOpened():
            print("Error: Cannot open video source:", self.video_source)
            return

        self.running = True
        while self.running:
            ret, frame = cap.read()
            if not ret:
                break

            
            detections = self.detector.detect(frame)
            self.last_detections = detections

            
            person_rects = [(x1, y1, x2, y2) for (x1, y1, x2, y2, cls, conf) in detections if int(cls) == 0]

            
            objects = self.tracker.update(person_rects, self.polygon)

            
            for objectID, (centroid, current_state) in objects.items():
                previous_state = self.object_states.get(objectID, None)
                if previous_state is None:
                    self.object_states[objectID] = current_state
                    if current_state:
                        self.count_in += 1
                else:
                    if previous_state is False and current_state is True:
                        self.count_in += 1
                    elif previous_state is True and current_state is False:
                        self.count_out += 1
                    self.object_states[objectID] = current_state

            
            counts = {}
            for det in detections:
                cls = int(det[4])
                counts[cls] = counts.get(cls, 0) + 1
            self.last_counts = counts

            
            print("last_counts:", self.last_counts)

            
            for (x1, y1, x2, y2, cls, conf) in detections:
                color = (0, 255, 0) if int(cls) == 0 else (255, 0, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                label = f"{int(cls)}: {conf:.2f}"
                cv2.putText(frame, label, (x1, max(y1-10, 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            
            # cv2.polylines(frame, [self.polygon], isClosed=True, color=(0, 255, 255), thickness=2)

            
            self.last_frame = frame

            time.sleep(0.03)

        cap.release()

    def start(self):
        t = threading.Thread(target=self.run, daemon=True)
        t.start()

    def stop(self):
        self.running = False
