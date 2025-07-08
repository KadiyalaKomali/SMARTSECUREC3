import asyncio
import logging
from typing import Dict, List, Optional, Callable
from .ai_services.video_processor import VideoProcessor

logger = logging.getLogger(__name__)

class VideoManager:
    def __init__(self, event_callback: Optional[Callable] = None):
        self.processors: Dict[str, VideoProcessor] = {}
        self.event_callback = event_callback
        
    def add_camera(self, camera_config: Dict):
        """Add a new camera for processing"""
        camera_id = camera_config['id']
        
        if camera_id in self.processors:
            logger.warning(f"Camera {camera_id} already exists")
            return
        
        processor = VideoProcessor(camera_config, self.event_callback)
        self.processors[camera_id] = processor
        
        if camera_config.get('is_active', False):
            processor.start()
        
        logger.info(f"Added camera: {camera_config['name']}")
    
    def remove_camera(self, camera_id: str):
        """Remove a camera from processing"""
        if camera_id in self.processors:
            self.processors[camera_id].stop()
            del self.processors[camera_id]
            logger.info(f"Removed camera: {camera_id}")
    
    def start_camera(self, camera_id: str):
        """Start processing for a specific camera"""
        if camera_id in self.processors:
            self.processors[camera_id].start()
            logger.info(f"Started camera: {camera_id}")
    
    def stop_camera(self, camera_id: str):
        """Stop processing for a specific camera"""
        if camera_id in self.processors:
            self.processors[camera_id].stop()
            logger.info(f"Stopped camera: {camera_id}")
    
    def update_camera(self, camera_id: str, camera_config: Dict):
        """Update camera configuration"""
        if camera_id in self.processors:
            # Stop current processor
            self.processors[camera_id].stop()
            
            # Create new processor with updated config
            processor = VideoProcessor(camera_config, self.event_callback)
            self.processors[camera_id] = processor
            
            if camera_config.get('is_active', False):
                processor.start()
            
            logger.info(f"Updated camera: {camera_config['name']}")
    
    def load_known_faces(self, persons_data: List[Dict]):
        """Load known faces for all cameras"""
        for processor in self.processors.values():
            processor.load_known_faces(persons_data)
    
    def get_camera_frame(self, camera_id: str):
        """Get latest frame from a specific camera"""
        if camera_id in self.processors:
            return self.processors[camera_id].get_frame()
        return None
    
    def get_active_cameras(self) -> List[str]:
        """Get list of active camera IDs"""
        return [
            camera_id for camera_id, processor in self.processors.items()
            if processor.is_running
        ]
    
    def stop_all(self):
        """Stop all camera processing"""
        for processor in self.processors.values():
            processor.stop()
        self.processors.clear()
        logger.info("Stopped all camera processing")