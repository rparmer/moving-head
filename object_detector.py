import cv2
import logging
from ultralytics import YOLO

GREEN = (0, 255, 0)

class Detection():
    def __init__(self, x1, y1, x2, y2, x_center, y_center, w, h, area, confidence, frame):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x_center = x_center
        self.y_center = y_center
        self.w = w
        self.h = h
        self.area = area
        self.confidence = confidence
        self.frame = frame

    def __repr__(self):
        return f'Detection({self.x1}, {self.y1}, {self.x2}, {self.y2}, {self.x_center}, {self.y_center}, {self.w}, {self.h}, {self.area}, {self.confidence})'

class ObjectDetector():
    def __init__(self, model_file = 'yolo11n.pt', confidence_threshold = 0.25, verbose = False):
        logging.info('Setting up object detector')
        self.confidence_threshold = confidence_threshold
        self.model = YOLO(model_file)
        self.verbose = verbose

    def __del__(self):
        logging.info('Cleaning up object detector')

    def process_frame(self, frame):
        results = []
        # Class '0' filters to only return 'person'
        detections = self.model.predict(source=frame, conf=self.confidence_threshold, classes=[0], verbose=self.verbose)[0]
            
        for data in detections.boxes.data.tolist():
            x1, y1, x2, y2, confidence = int(data[0]), int(data[1]), int(data[2]), int(data[3]), float(data[4])

            x_center = (x1 + x2) / 2
            y_center = (y1 + y2) / 2
            w = x2 - x1
            h = y2 - y1
            area = w * h

            cv2.rectangle(frame, (x1, y1) , (x2, y2), GREEN, 2)

            detection = Detection(
                x1 = x1,
                y1 = y1,
                x2 = x2,
                y2 = y2,
                x_center = x_center,
                y_center = y_center,
                w = w,
                h = h,
                area = area,
                confidence = confidence,
                frame = frame
            )

            results.append(detection)

        return results, frame
