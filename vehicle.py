from sqlalchemy.orm import Session
from typing import Optional, List
import uuid

from ..models import Vehicle
from ..schemas import VehicleCreate, VehicleUpdate

def get_vehicle(db: Session, vehicle_id: str) -> Optional[Vehicle]:
    return db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

def get_vehicles(db: Session, tenant_id: str, skip: int = 0, limit: int = 100) -> List[Vehicle]:
    return db.query(Vehicle).filter(Vehicle.tenant_id == tenant_id).offset(skip).limit(limit).all()

def get_authorized_vehicles(db: Session, tenant_id: str) -> List[Vehicle]:
    return db.query(Vehicle).filter(
        Vehicle.tenant_id == tenant_id,
        Vehicle.authorized == True
    ).all()

def get_vehicle_by_license_plate(db: Session, license_plate: str, tenant_id: str) -> Optional[Vehicle]:
    return db.query(Vehicle).filter(
        Vehicle.license_plate == license_plate.upper(),
        Vehicle.tenant_id == tenant_id
    ).first()

def create_vehicle(db: Session, vehicle: VehicleCreate, tenant_id: str) -> Vehicle:
    db_vehicle = Vehicle(
        id=str(uuid.uuid4()),
        license_plate=vehicle.license_plate.upper(),
        vehicle_type=vehicle.vehicle_type,
        owner_name=vehicle.owner_name,
        company=vehicle.company,
        authorized=vehicle.authorized,
        tenant_id=tenant_id
    )
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def update_vehicle(db: Session, vehicle_id: str, vehicle_update: VehicleUpdate) -> Optional[Vehicle]:
    db_vehicle = get_vehicle(db, vehicle_id)
    if not db_vehicle:
        return None
    
    update_data = vehicle_update.dict(exclude_unset=True)
    if "license_plate" in update_data:
        update_data["license_plate"] = update_data["license_plate"].upper()
    
    for field, value in update_data.items():
        setattr(db_vehicle, field, value)
    
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def delete_vehicle(db: Session, vehicle_id: str) -> bool:
    db_vehicle = get_vehicle(db, vehicle_id)
    if not db_vehicle:
        return False
    
    db.delete(db_vehicle)
    db.commit()
    return True