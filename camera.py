from sqlalchemy.orm import Session
from typing import Optional, List
import uuid

from ..models import Camera
from ..schemas import CameraCreate, CameraUpdate

def get_camera(db: Session, camera_id: str) -> Optional[Camera]:
    return db.query(Camera).filter(Camera.id == camera_id).first()

def get_cameras(db: Session, tenant_id: str, skip: int = 0, limit: int = 100) -> List[Camera]:
    return db.query(Camera).filter(Camera.tenant_id == tenant_id).offset(skip).limit(limit).all()

def get_active_cameras(db: Session, tenant_id: str) -> List[Camera]:
    return db.query(Camera).filter(
        Camera.tenant_id == tenant_id,
        Camera.is_active == True
    ).all()

def create_camera(db: Session, camera: CameraCreate, tenant_id: str) -> Camera:
    db_camera = Camera(
        id=str(uuid.uuid4()),
        name=camera.name,
        rtsp_url=camera.rtsp_url,
        location=camera.location,
        ai_detection_enabled=camera.ai_detection_enabled,
        tenant_id=tenant_id,
        is_active=True
    )
    db.add(db_camera)
    db.commit()
    db.refresh(db_camera)
    return db_camera

def update_camera(db: Session, camera_id: str, camera_update: CameraUpdate) -> Optional[Camera]:
    db_camera = get_camera(db, camera_id)
    if not db_camera:
        return None
    
    update_data = camera_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_camera, field, value)
    
    db.commit()
    db.refresh(db_camera)
    return db_camera

def delete_camera(db: Session, camera_id: str) -> bool:
    db_camera = get_camera(db, camera_id)
    if not db_camera:
        return False
    
    db.delete(db_camera)
    db.commit()
    return True

def toggle_camera_status(db: Session, camera_id: str) -> Optional[Camera]:
    db_camera = get_camera(db, camera_id)
    if not db_camera:
        return None
    
    db_camera.is_active = not db_camera.is_active
    db.commit()
    db.refresh(db_camera)
    return db_camera