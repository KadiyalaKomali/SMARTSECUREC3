from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, or_
from typing import Optional, List
from datetime import datetime, timedelta
import uuid

from ..models import Event
from ..schemas import EventCreate

def get_event(db: Session, event_id: str) -> Optional[Event]:
    return db.query(Event).filter(Event.id == event_id).first()

def get_events(
    db: Session, 
    tenant_id: str, 
    skip: int = 0, 
    limit: int = 100,
    event_type: str = None,
    camera_id: str = None,
    start_date: datetime = None,
    end_date: datetime = None
) -> List[Event]:
    query = db.query(Event).filter(Event.tenant_id == tenant_id)
    
    if event_type:
        query = query.filter(Event.event_type == event_type)
    
    if camera_id:
        query = query.filter(Event.camera_id == camera_id)
    
    if start_date:
        query = query.filter(Event.created_at >= start_date)
    
    if end_date:
        query = query.filter(Event.created_at <= end_date)
    
    return query.order_by(desc(Event.created_at)).offset(skip).limit(limit).all()

def get_recent_events(db: Session, tenant_id: str, hours: int = 24, limit: int = 10) -> List[Event]:
    since = datetime.utcnow() - timedelta(hours=hours)
    return db.query(Event).filter(
        Event.tenant_id == tenant_id,
        Event.created_at >= since
    ).order_by(desc(Event.created_at)).limit(limit).all()

def get_events_count_by_type(db: Session, tenant_id: str, hours: int = 24) -> dict:
    since = datetime.utcnow() - timedelta(hours=hours)
    events = db.query(Event).filter(
        Event.tenant_id == tenant_id,
        Event.created_at >= since
    ).all()
    
    counts = {}
    for event in events:
        counts[event.event_type] = counts.get(event.event_type, 0) + 1
    
    return counts

def create_event(db: Session, event: EventCreate, tenant_id: str) -> Event:
    db_event = Event(
        id=str(uuid.uuid4()),
        event_type=event.event_type,
        description=event.description,
        camera_id=event.camera_id,
        confidence=event.confidence,
        metadata=event.metadata,
        tenant_id=tenant_id
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def search_events(db: Session, tenant_id: str, search_query: str, limit: int = 50) -> List[Event]:
    return db.query(Event).filter(
        Event.tenant_id == tenant_id,
        or_(
            Event.description.ilike(f"%{search_query}%"),
            Event.event_type.ilike(f"%{search_query}%")
        )
    ).order_by(desc(Event.created_at)).limit(limit).all()