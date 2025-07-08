import cv2
import numpy as np
from typing import Dict, List, Optional, Callable
import threading
import time
import logging
from queue import Queue

from .face_recognition import FaceRecognitionService
from .vehicle_detection import VehicleDetectionService
from .object_detection import ObjectDetectionService

logger = logging.getLogger(__name__)

class VideoProcessor:
    def __init__(self, camera_config: Dict, event_callback: Optional[Callable] = None):
        self.camera_config = camera_config
        self.event_callback = event_callback
        self.is_running = False
        self.frame_queue = Queue(maxsize=10)
        
        # Initialize AI services
        self.face_service = FaceRecognitionService()
        self.vehicle_service = VehicleDetectionService()
        self.object_service = ObjectDetectionService()
        
        # Processing thread
        self.processing_thread = None
        self.capture_thread = None
        
        # Video capture
        self.cap = None
        
        # Configuration
        self.detection_interval = 1.0  # Process every second
        self.last_detection_time = 0
    
    def start(self):
        """Start video processing"""
        if self.is_running:
            return
        
        self.is_running = True
        
        # Start capture thread
        self.capture_thread = threading.Thread(target=self._capture_frames)
        self.capture_thread.daemon = True
        self.capture_thread.start()
        
        # Start processing thread
        self.processing_thread = threading.Thread(target=self._process_frames)
        self.processing_thread.daemon = True
        self.processing_thread.start()
        
        logger.info(f"Started video processing for camera: {self.camera_config['name']}")
    
    def stop(self):
        """Stop video processing"""
        self.is_running = False
        
        if self.cap:
            self.cap.release()
        
        if self.capture_thread:
            self.capture_thread.join(timeout=5)
        
        if self.processing_thread:
            self.processing_thread.join(timeout=5)
        
        logger.info(f"Stopped video processing for camera: {self.camera_config['name']}")
    
    def _capture_frames(self):
        """Capture frames from video stream"""
        try:
            self.cap = cv2.VideoCapture(self.camera_config['rtsp_url'])
            
            if not self.cap.isOpened():
                logger.error(f"Could not open camera: {self.camera_config['rtsp_url']}")
                return
            
            while self.is_running:
                ret, frame = self.cap.read()
                if not ret:
                    logger.warning("Failed to read frame")
                    continue
                
                # Add frame to queue (non-blocking)
                if not self.frame_queue.full():
                    self.frame_queue.put(frame)
                
                time.sleep(0.033)  # ~30 FPS
                
        except Exception as e:
            logger.error(f"Error in capture thread: {e}")
        finally:
            if self.cap:
                self.cap.release()
    
    def _process_frames(self):
        """Process frames for AI detection"""
        while self.is_running:
            try:
                if self.frame_queue.empty():
                    time.sleep(0.1)
                    continue
                
                frame = self.frame_queue.get()
                current_time = time.time()
                
                # Process at specified interval
                if current_time - self.last_detection_time >= self.detection_interval:
                    self._process_frame(frame)
                    self.last_detection_time = current_time
                
            except Exception as e:
                logger.error(f"Error in processing thread: {e}")
                time.sleep(1)
    
    def _process_frame(self, frame: np.ndarray):
        """Process a single frame for AI detection"""
        try:
            if not self.camera_config.get('ai_detection_enabled', False):
                return
            
            # Face detection
            face_results = self.face_service.recognize_faces(frame)
            for face_result in face_results:
                if face_result['confidence'] > 0.6:
                    self._trigger_event('face_detection', {
                        'person_id': face_result['person_id'],
                        'name': face_result['name'],
                        'confidence': face_result['confidence']
                    })
            
            # Vehicle detection
            vehicle_detections = self.vehicle_service.detect_vehicles(frame)
            for detection in vehicle_detections:
                license_plate = self.vehicle_service.extract_license_plate(
                    frame, detection['bounding_box']
                )
                
                if license_plate:
                    self._trigger_event('vehicle_detection', {
                        'license_plate': license_plate,
                        'vehicle_type': detection['class'],
                        'confidence': detection['confidence']
                    })
            
            # Object detection (gunny bags)
            gunny_bag_count = self.object_service.count_gunny_bags(frame)
            if gunny_bag_count > 0:
                self._trigger_event('object_detection', {
                    'object_type': 'gunny_bag',
                    'count': gunny_bag_count
                })
            
            # Intrusion detection
            restricted_zones = [
                {
                    'name': 'Restricted Area',
                    'polygon': [(100, 100), (200, 100), (200, 200), (100, 200)]
                }
            ]
            
            intrusions = self.object_service.detect_intrusion(frame, restricted_zones)
            for intrusion in intrusions:
                self._trigger_event('intrusion', {
                    'zone_name': intrusion['zone_name'],
                    'confidence': intrusion['confidence']
                })
            
        except Exception as e:
            logger.error(f"Error processing frame: {e}")
    
    def _trigger_event(self, event_type: str, metadata: Dict):
        """Trigger an event callback"""
        if self.event_callback:
            try:
                event_data = {
                    'event_type': event_type,
                    'camera_id': self.camera_config['id'],
                    'camera_name': self.camera_config['name'],
                    'timestamp': time.time(),
                    'metadata': metadata
                }
                self.event_callback(event_data)
            except Exception as e:
                logger.error(f"Error triggering event: {e}")
    
    def load_known_faces(self, persons_data: List[Dict]):
        """Load known faces for recognition"""
        self.face_service.load_known_faces(persons_data)
    
    def get_frame(self) -> Optional[np.ndarray]:
        """Get the latest frame"""
        if not self.frame_queue.empty():
            return self.frame_queue.get()
        return None