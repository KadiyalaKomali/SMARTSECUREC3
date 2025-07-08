from fastapi import FastAPI, HTTPException, Depends, status
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
import uvicorn
from typing import Optional, List
from datetime import datetime, timedelta
import logging
import json
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Database and models  
from .database import engine, Base, get_db, init_db, check_db_connection
from .models import User, Tenant, Camera, Person, Vehicle, Event
from .auth import (
    create_access_token, get_current_user, get_current_active_user,
    require_admin, require_admin_or_security, require_any_role
)
from .websocket_manager import manager
from .crud import user as crud_user, camera as crud_camera, person as crud_person, vehicle as crud_vehicle, event as crud_event
from schemas import (
    UserCreate, UserResponse, LoginRequest, LoginResponse,
    CameraCreate, CameraResponse, CameraUpdate,
    PersonCreate, PersonResponse, PersonUpdate,
    VehicleCreate, VehicleResponse, VehicleUpdate,
    EventCreate, EventResponse
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database
    try:
        init_db()
        if not check_db_connection():
            raise Exception("Database connection failed")
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    
    yield
    logger.info("Application shutdown")

app = FastAPI(
    title="SMARTSECUREC3 API",
    description="AI-Powered Contextual Warehouse Surveillance System",
    version="1.0.0", 
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5173").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add security middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
)

# Routes
@app.get("/")
async def root():
    return {"message": "SMARTSECUREC3 API is running"}

@app.get("/health")
async def health_check():
    db_status = check_db_connection()
    return {
        "status": "healthy" if db_status else "unhealthy",
        "database": "connected" if db_status else "disconnected",
        "timestamp": datetime.utcnow()
    }

# WebSocket endpoint
@app.websocket("/ws/{tenant_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, tenant_id: str, user_id: str):
    await manager.connect(websocket, tenant_id, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming WebSocket messages
            message_data = json.loads(data)
            
            if message_data.get("type") == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, tenant_id, user_id)

# Authentication endpoints
@app.post("/api/v1/auth/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    # Demo authentication - replace with actual authentication
    demo_users = {
        "admin@demo.com": {
            "id": "1",
            "password": "admin123",
            "full_name": "Admin User",
            "role": "admin",
            "tenant_id": "demo-tenant"
        },
        "security@demo.com": {
            "id": "2", 
            "password": "security123",
            "full_name": "Security Officer",
            "role": "security",
            "tenant_id": "demo-tenant"
        },
        "manager@demo.com": {
            "id": "3",
            "password": "manager123", 
            "full_name": "Manager User",
            "role": "manager",
            "tenant_id": "demo-tenant"
        }
    }
    
    user_data = demo_users.get(request.email)
    if user_data and user_data["password"] == request.password:
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={
                "sub": user_data["id"],
                "email": request.email,
                "role": user_data["role"],
                "tenant_id": user_data["tenant_id"]
            },
            expires_delta=access_token_expires
        )
        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse(
                id=user_data["id"],
                email=request.email,
                full_name=user_data["full_name"],
                role=user_data["role"],
                tenant_id=user_data["tenant_id"]
            )
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

@app.post("/api/v1/auth/register", response_model=UserResponse)
async def register(
    user: UserCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    # Check if user already exists
    existing_user = crud_user.get_user_by_email(db, user.email, current_user.tenant_id)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    db_user = crud_user.create_user(db, user, current_user.tenant_id)
    return UserResponse(
        id=str(db_user.id),
        email=db_user.email,
        full_name=db_user.full_name,
        role=db_user.role,
        tenant_id=str(db_user.tenant_id)
    )

# Camera endpoints
@app.get("/api/v1/cameras", response_model=List[CameraResponse])
async def get_cameras(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_any_role)
):
    cameras = crud_camera.get_cameras(db, current_user.tenant_id, skip, limit)
    return [CameraResponse(
        id=str(camera.id),
        name=camera.name,
        rtsp_url=camera.rtsp_url,
        location=camera.location,
        is_active=camera.is_active,
        ai_detection_enabled=camera.ai_detection_enabled,
        created_at=camera.created_at
    ) for camera in cameras]

@app.post("/api/v1/cameras", response_model=CameraResponse)
async def create_camera(
    camera: CameraCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_security)
):
    db_camera = crud_camera.create_camera(db, camera, current_user.tenant_id)
    
    # Broadcast camera creation
    await manager.broadcast_camera_status({
        "action": "created",
        "camera": {
            "id": str(db_camera.id),
            "name": db_camera.name,
            "location": db_camera.location
        }
    }, current_user.tenant_id)
    
    return CameraResponse(
        id=str(db_camera.id),
        name=db_camera.name,
        rtsp_url=db_camera.rtsp_url,
        location=db_camera.location,
        is_active=db_camera.is_active,
        ai_detection_enabled=db_camera.ai_detection_enabled,
        created_at=db_camera.created_at
    )

@app.put("/api/v1/cameras/{camera_id}", response_model=CameraResponse)
async def update_camera(
    camera_id: str,
    camera_update: CameraUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_security)
):
    db_camera = crud_camera.update_camera(db, camera_id, camera_update)
    if not db_camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found"
        )
    
    # Broadcast camera update
    await manager.broadcast_camera_status({
        "action": "updated",
        "camera": {
            "id": str(db_camera.id),
            "name": db_camera.name,
            "is_active": db_camera.is_active
        }
    }, current_user.tenant_id)
    
    return CameraResponse(
        id=str(db_camera.id),
        name=db_camera.name,
        rtsp_url=db_camera.rtsp_url,
        location=db_camera.location,
        is_active=db_camera.is_active,
        ai_detection_enabled=db_camera.ai_detection_enabled,
        created_at=db_camera.created_at
    )

@app.delete("/api/v1/cameras/{camera_id}")
async def delete_camera(
    camera_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    success = crud_camera.delete_camera(db, camera_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found"
        )
    
    # Broadcast camera deletion
    await manager.broadcast_camera_status({
        "action": "deleted",
        "camera_id": camera_id
    }, current_user.tenant_id)
    
    return {"message": "Camera deleted successfully"}

# Person endpoints
@app.get("/api/v1/persons", response_model=List[PersonResponse])
async def get_persons(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_any_role)
):
    persons = crud_person.get_persons(db, current_user.tenant_id, skip, limit)
    return [PersonResponse(
        id=str(person.id),
        name=person.name,
        employee_id=person.employee_id,
        department=person.department,
        role=person.role,
        authorized=person.authorized,
        created_at=person.created_at
    ) for person in persons]

@app.post("/api/v1/persons", response_model=PersonResponse)
async def create_person(
    person: PersonCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_security)
):
    # Check if employee ID already exists
    existing_person = crud_person.get_person_by_employee_id(
        db, person.employee_id, current_user.tenant_id
    )
    if existing_person:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID already exists"
        )
    
    db_person = crud_person.create_person(db, person, current_user.tenant_id)
    return PersonResponse(
        id=str(db_person.id),
        name=db_person.name,
        employee_id=db_person.employee_id,
        department=db_person.department,
        role=db_person.role,
        authorized=db_person.authorized,
        created_at=db_person.created_at
    )

@app.put("/api/v1/persons/{person_id}", response_model=PersonResponse)
async def update_person(
    person_id: str,
    person_update: PersonUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_security)
):
    db_person = crud_person.update_person(db, person_id, person_update)
    if not db_person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Person not found"
        )
    
    return PersonResponse(
        id=str(db_person.id),
        name=db_person.name,
        employee_id=db_person.employee_id,
        department=db_person.department,
        role=db_person.role,
        authorized=db_person.authorized,
        created_at=db_person.created_at
    )

@app.delete("/api/v1/persons/{person_id}")
async def delete_person(
    person_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    success = crud_person.delete_person(db, person_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Person not found"
        )
    
    return {"message": "Person deleted successfully"}

# Vehicle endpoints
@app.get("/api/v1/vehicles", response_model=List[VehicleResponse])
async def get_vehicles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_any_role)
):
    vehicles = crud_vehicle.get_vehicles(db, current_user.tenant_id, skip, limit)
    return [VehicleResponse(
        id=str(vehicle.id),
        license_plate=vehicle.license_plate,
        vehicle_type=vehicle.vehicle_type,
        owner_name=vehicle.owner_name,
        company=vehicle.company,
        authorized=vehicle.authorized,
        created_at=vehicle.created_at
    ) for vehicle in vehicles]

@app.post("/api/v1/vehicles", response_model=VehicleResponse)
async def create_vehicle(
    vehicle: VehicleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_security)
):
    # Check if license plate already exists
    existing_vehicle = crud_vehicle.get_vehicle_by_license_plate(
        db, vehicle.license_plate, current_user.tenant_id
    )
    if existing_vehicle:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="License plate already exists"
        )
    
    db_vehicle = crud_vehicle.create_vehicle(db, vehicle, current_user.tenant_id)
    return VehicleResponse(
        id=str(db_vehicle.id),
        license_plate=db_vehicle.license_plate,
        vehicle_type=db_vehicle.vehicle_type,
        owner_name=db_vehicle.owner_name,
        company=db_vehicle.company,
        authorized=db_vehicle.authorized,
        created_at=db_vehicle.created_at
    )

@app.put("/api/v1/vehicles/{vehicle_id}", response_model=VehicleResponse)
async def update_vehicle(
    vehicle_id: str,
    vehicle_update: VehicleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_security)
):
    db_vehicle = crud_vehicle.update_vehicle(db, vehicle_id, vehicle_update)
    if not db_vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    
    return VehicleResponse(
        id=str(db_vehicle.id),
        license_plate=db_vehicle.license_plate,
        vehicle_type=db_vehicle.vehicle_type,
        owner_name=db_vehicle.owner_name,
        company=db_vehicle.company,
        authorized=db_vehicle.authorized,
        created_at=db_vehicle.created_at
    )

@app.delete("/api/v1/vehicles/{vehicle_id}")
async def delete_vehicle(
    vehicle_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    success = crud_vehicle.delete_vehicle(db, vehicle_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    
    return {"message": "Vehicle deleted successfully"}

# Event endpoints
@app.get("/api/v1/events", response_model=List[EventResponse])
async def get_events(
    skip: int = 0,
    limit: int = 100,
    event_type: Optional[str] = None,
    camera_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_any_role)
):
    events = crud_event.get_events(
        db, current_user.tenant_id, skip, limit, event_type, camera_id
    )
    return [EventResponse(
        id=str(event.id),
        event_type=event.event_type,
        description=event.description,
        camera_id=str(event.camera_id),
        confidence=event.confidence,
        metadata=event.metadata,
        created_at=event.created_at
    ) for event in events]

@app.post("/api/v1/events", response_model=EventResponse)
async def create_event(
    event: EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_any_role)
):
    db_event = crud_event.create_event(db, event, current_user.tenant_id)
    
    # Broadcast event to connected clients
    await manager.broadcast_event({
        "id": str(db_event.id),
        "event_type": db_event.event_type,
        "description": db_event.description,
        "camera_id": str(db_event.camera_id),
        "confidence": db_event.confidence,
        "created_at": db_event.created_at.isoformat()
    }, current_user.tenant_id)
    
    return EventResponse(
        id=str(db_event.id),
        event_type=db_event.event_type,
        description=db_event.description,
        camera_id=str(db_event.camera_id),
        confidence=db_event.confidence,
        metadata=db_event.metadata,
        created_at=db_event.created_at
    )

@app.get("/api/v1/events/search")
async def search_events(
    q: str,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_any_role)
):
    events = crud_event.search_events(db, current_user.tenant_id, q, limit)
    return [EventResponse(
        id=str(event.id),
        event_type=event.event_type,
        description=event.description,
        camera_id=str(event.camera_id),
        confidence=event.confidence,
        metadata=event.metadata,
        created_at=event.created_at
    ) for event in events]

# Dashboard endpoints
@app.get("/api/v1/dashboard")
async def get_dashboard_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_any_role)
):
    # Get statistics
    cameras = crud_camera.get_cameras(db, current_user.tenant_id)
    active_cameras = crud_camera.get_active_cameras(db, current_user.tenant_id)
    persons = crud_person.get_persons(db, current_user.tenant_id)
    vehicles = crud_vehicle.get_vehicles(db, current_user.tenant_id)
    recent_events = crud_event.get_recent_events(db, current_user.tenant_id, 24, 10)
    event_counts = crud_event.get_events_count_by_type(db, current_user.tenant_id, 24)
    
    # Calculate alerts (high-priority events)
    alerts = len([e for e in recent_events if e.event_type in ['intrusion', 'unauthorized_access']])
    
    return {
        "stats": {
            "totalCameras": len(cameras),
            "activeCameras": len(active_cameras),
            "totalPersons": len(persons),
            "totalVehicles": len(vehicles),
            "todayEvents": len(recent_events),
            "alerts": alerts
        },
        "recentEvents": [
            {
                "id": str(event.id),
                "type": "alert" if event.event_type in ['intrusion', 'unauthorized_access'] else "detection",
                "message": event.description,
                "camera": f"Camera {event.camera_id}",
                "timestamp": event.created_at.isoformat(),
                "status": "pending" if event.event_type in ['intrusion', 'unauthorized_access'] else "resolved"
            }
            for event in recent_events[:5]
        ],
        "chartData": [
            {"date": "2024-01-01", "detections": 45, "events": 23},
            {"date": "2024-01-02", "detections": 52, "events": 28},
            {"date": "2024-01-03", "detections": 38, "events": 19},
            {"date": "2024-01-04", "detections": 67, "events": 34},
            {"date": "2024-01-05", "detections": 71, "events": 41},
            {"date": "2024-01-06", "detections": 58, "events": 29},
            {"date": "2024-01-07", "detections": 63, "events": 32}
        ]
    }

# System status endpoints
@app.get("/api/v1/system/status")
async def get_system_status(current_user: User = Depends(require_admin)):
    return {
        "database": "connected" if check_db_connection() else "disconnected",
        "websocket_connections": manager.get_connection_count(current_user.tenant_id),
        "ai_services": "active",
        "version": "1.0.0",
        "uptime": "24h 15m"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)