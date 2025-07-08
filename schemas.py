from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    SECURITY = "security"
    MANAGER = "manager"

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role: UserRole

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    tenant_id: str
    
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class CameraCreate(BaseModel):
    name: str
    rtsp_url: str
    location: str
    ai_detection_enabled: bool = True

class CameraUpdate(BaseModel):
    name: Optional[str] = None
    rtsp_url: Optional[str] = None
    location: Optional[str] = None
    is_active: Optional[bool] = None
    ai_detection_enabled: Optional[bool] = None
class CameraResponse(BaseModel):
    id: str
    name: str
    rtsp_url: str
    location: str
    is_active: bool
    ai_detection_enabled: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class PersonCreate(BaseModel):
    name: str
    employee_id: str
    department: str
    role: str
    authorized: bool = True

class PersonUpdate(BaseModel):
    name: Optional[str] = None
    employee_id: Optional[str] = None
    department: Optional[str] = None
    role: Optional[str] = None
    authorized: Optional[bool] = None
class PersonResponse(BaseModel):
    id: str
    name: str
    employee_id: str
    department: str
    role: str
    authorized: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class VehicleCreate(BaseModel):
    license_plate: str
    vehicle_type: str
    owner_name: str
    company: str
    authorized: bool = True

class VehicleUpdate(BaseModel):
    license_plate: Optional[str] = None
    vehicle_type: Optional[str] = None
    owner_name: Optional[str] = None
    company: Optional[str] = None
    authorized: Optional[bool] = None
class VehicleResponse(BaseModel):
    id: str
    license_plate: str
    vehicle_type: str
    owner_name: str
    company: str
    authorized: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class EventCreate(BaseModel):
    event_type: str
    description: str
    camera_id: str
    confidence: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

class EventResponse(BaseModel):
    id: str
    event_type: str
    description: str
    camera_id: str
    confidence: Optional[float]
    metadata: Optional[Dict[str, Any]]
    created_at: datetime
    
    class Config:
        from_attributes = True