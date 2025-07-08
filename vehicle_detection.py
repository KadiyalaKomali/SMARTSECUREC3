import cv2
import numpy as np
from ultralytics import YOLO
from paddleocr import PaddleOCR
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class VehicleDetectionService:
    def __init__(self):
        # Load YOLO model for vehicle detection
        self.yolo_model = YOLO('yolov8n.pt')
        
        # Initialize PaddleOCR for license plate reading
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')
        
        # Vehicle classes from COCO dataset
        self.vehicle_classes = ['car', 'motorcycle', 'bus', 'truck']
    
    def detect_vehicles(self, frame: np.ndarray, confidence_threshold: float = 0.5) -> List[Dict]:
        """Detect vehicles in video frame"""
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
                        
                        if class_name in self.vehicle_classes and confidence >= confidence_threshold:
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
            logger.error(f"Error detecting vehicles: {e}")
            return []
    
    def extract_license_plate(self, frame: np.ndarray, vehicle_bbox: Dict) -> Optional[str]:
        """Extract license plate text from vehicle region"""
        try:
            # Extract vehicle region
            x1, y1, x2, y2 = vehicle_bbox['x1'], vehicle_bbox['y1'], vehicle_bbox['x2'], vehicle_bbox['y2']
            vehicle_region = frame[y1:y2, x1:x2]
            
            # Use OCR to extract text
            result = self.ocr.ocr(vehicle_region, cls=True)
            
            if result and len(result) > 0:
                # Extract text from OCR result
                texts = []
                for line in result:
                    if line:
                        for word_info in line:
                            if len(word_info) >= 2:
                                texts.append(word_info[1][0])
                
                # Join all text and clean up
                license_plate = ''.join(texts).strip()
                
                # Basic validation for license plate format
                if len(license_plate) >= 3:
                    return license_plate.upper()
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting license plate: {e}")
            return None
    
    def match_authorized_vehicle(self, license_plate: str, authorized_vehicles: List[Dict]) -> Optional[Dict]:
        """Match detected license plate with authorized vehicles"""
        for vehicle in authorized_vehicles:
            if vehicle['license_plate'].upper() == license_plate.upper():
                return vehicle
        return None
    
    def draw_vehicle_boxes(self, frame: np.ndarray, detections: List[Dict]) -> np.ndarray:
        """Draw bounding boxes around detected vehicles"""
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