import cv2
import numpy as np
import face_recognition
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class FaceRecognitionService:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.known_face_ids = []
    
    def load_known_faces(self, persons_data: List[Dict]):
        """Load known faces from database"""
        self.known_face_encodings = []
        self.known_face_names = []
        self.known_face_ids = []
        
        for person in persons_data:
            if person.get('face_encodings'):
                encoding = np.array(person['face_encodings'])
                self.known_face_encodings.append(encoding)
                self.known_face_names.append(person['name'])
                self.known_face_ids.append(person['id'])
    
    def encode_face(self, image_path: str) -> Optional[np.ndarray]:
        """Generate face encoding from image"""
        try:
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)
            
            if len(face_encodings) > 0:
                return face_encodings[0]
            else:
                logger.warning(f"No face found in image: {image_path}")
                return None
        except Exception as e:
            logger.error(f"Error encoding face: {e}")
            return None
    
    def recognize_faces(self, frame: np.ndarray, threshold: float = 0.6) -> List[Dict]:
        """Recognize faces in video frame"""
        try:
            # Find face locations
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)
            
            results = []
            
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(
                    self.known_face_encodings, 
                    face_encoding,
                    tolerance=threshold
                )
                
                name = "Unknown"
                person_id = None
                confidence = 0.0
                
                # Find the best match
                face_distances = face_recognition.face_distance(
                    self.known_face_encodings, 
                    face_encoding
                )
                
                if len(face_distances) > 0:
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        person_id = self.known_face_ids[best_match_index]
                        confidence = 1.0 - face_distances[best_match_index]
                
                results.append({
                    'person_id': person_id,
                    'name': name,
                    'confidence': confidence,
                    'bounding_box': {
                        'top': top,
                        'right': right,
                        'bottom': bottom,
                        'left': left
                    }
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error recognizing faces: {e}")
            return []
    
    def draw_face_boxes(self, frame: np.ndarray, face_results: List[Dict]) -> np.ndarray:
        """Draw bounding boxes around detected faces"""
        for result in face_results:
            bbox = result['bounding_box']
            name = result['name']
            confidence = result['confidence']
            
            # Draw rectangle
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (bbox['left'], bbox['top']), (bbox['right'], bbox['bottom']), color, 2)
            
            # Draw label
            label = f"{name} ({confidence:.2f})"
            cv2.putText(frame, label, (bbox['left'], bbox['top'] - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        return frame