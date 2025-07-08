import cv2
import numpy as np
from ultralytics import YOLO
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class ObjectDetectionService:
    def __init__(self):
        # Load YOLO model
        self.yolo_model = YOLO('yolov8n.pt')
        
        # Define object classes we're interested in
        self.target_objects = {
            'gunny_bag': ['backpack', 'handbag', 'suitcase'],  # Approximate classes
            'person': ['person'],
            'box': ['box', 'package'],
            'container': ['container', 'crate']
        }
    
    def detect_objects(self, frame: np.ndarray, confidence_threshold: float = 0.5) -> List[Dict]:
        """Detect objects in video frame"""
        try:
            results = self.yolo_model(frame)
            detections = []
            
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        class_id = int(box.cls[0])
                        class_name = self.yolo_model.names[class_id]
                        confidence = float(box.conf[0])
                        
                        if confidence >= confidence_threshold:
                            x1, y1, x2, y2 = box.xyxy[0].tolist()
                            
                            detections.append({
                                'class': class_name,
                                'confidence': confidence,
                                'bounding_box': {
                                    'x1': int(x1),
                                    'y1': int(y1),
                                    'x2': int(x2),
                                    'y2': int(y2)
                                }
                            })
            
            return detections
            
        except Exception as e:
            logger.error(f"Error detecting objects: {e}")
            return []
    
    def count_gunny_bags(self, frame: np.ndarray) -> int:
        """Count gunny bags (approximated by backpacks/bags) in frame"""
        try:
            detections = self.detect_objects(frame)
            gunny_bag_count = 0
            
            for detection in detections:
                class_name = detection['class']
                if class_name in self.target_objects['gunny_bag']:
                    gunny_bag_count += 1
            
            return gunny_bag_count
            
        except Exception as e:
            logger.error(f"Error counting gunny bags: {e}")
            return 0
    
    def detect_intrusion(self, frame: np.ndarray, restricted_zones: List[Dict]) -> List[Dict]:
        """Detect person intrusion in restricted zones"""
        try:
            person_detections = []
            all_detections = self.detect_objects(frame)
            
            # Filter for person detections
            for detection in all_detections:
                if detection['class'] in self.target_objects['person']:
                    person_detections.append(detection)
            
            intrusions = []
            
            for person in person_detections:
                person_bbox = person['bounding_box']
                person_center = (
                    (person_bbox['x1'] + person_bbox['x2']) // 2,
                    (person_bbox['y1'] + person_bbox['y2']) // 2
                )
                
                # Check if person is in any restricted zone
                for zone in restricted_zones:
                    if self._point_in_polygon(person_center, zone['polygon']):
                        intrusions.append({
                            'person_bbox': person_bbox,
                            'zone_name': zone['name'],
                            'confidence': person['confidence']
                        })
            
            return intrusions
            
        except Exception as e:
            logger.error(f"Error detecting intrusion: {e}")
            return []
    
    def _point_in_polygon(self, point: tuple, polygon: List[tuple]) -> bool:
        """Check if point is inside polygon using ray casting algorithm"""
        x, y = point
        n = len(polygon)
        inside = False
        
        p1x, p1y = polygon[0]
        for i in range(1, n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        
        return inside
    
    def draw_object_boxes(self, frame: np.ndarray, detections: List[Dict]) -> np.ndarray:
        """Draw bounding boxes around detected objects"""
        for detection in detections:
            bbox = detection['bounding_box']
            class_name = detection['class']
            confidence = detection['confidence']
            
            # Draw rectangle
            color = (0, 255, 0)
            cv2.rectangle(frame, (bbox['x1'], bbox['y1']), (bbox['x2'], bbox['y2']), color, 2)
            
            # Draw label
            label = f"{class_name} ({confidence:.2f})"
            cv2.putText(frame, label, (bbox['x1'], bbox['y1'] - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        return frame