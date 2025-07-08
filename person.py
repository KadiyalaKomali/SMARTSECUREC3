from sqlalchemy.orm import Session
from typing import Optional, List
import uuid

from ..models import Person
from ..schemas import PersonCreate, PersonUpdate

def get_person(db: Session, person_id: str) -> Optional[Person]:
    return db.query(Person).filter(Person.id == person_id).first()

def get_persons(db: Session, tenant_id: str, skip: int = 0, limit: int = 100) -> List[Person]:
    return db.query(Person).filter(Person.tenant_id == tenant_id).offset(skip).limit(limit).all()

def get_authorized_persons(db: Session, tenant_id: str) -> List[Person]:
    return db.query(Person).filter(
        Person.tenant_id == tenant_id,
        Person.authorized == True
    ).all()

def get_person_by_employee_id(db: Session, employee_id: str, tenant_id: str) -> Optional[Person]:
    return db.query(Person).filter(
        Person.employee_id == employee_id,
        Person.tenant_id == tenant_id
    ).first()

def create_person(db: Session, person: PersonCreate, tenant_id: str) -> Person:
    db_person = Person(
        id=str(uuid.uuid4()),
        name=person.name,
        employee_id=person.employee_id,
        department=person.department,
        role=person.role,
        authorized=person.authorized,
        tenant_id=tenant_id
    )
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

def update_person(db: Session, person_id: str, person_update: PersonUpdate) -> Optional[Person]:
    db_person = get_person(db, person_id)
    if not db_person:
        return None
    
    update_data = person_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_person, field, value)
    
    db.commit()
    db.refresh(db_person)
    return db_person

def delete_person(db: Session, person_id: str) -> bool:
    db_person = get_person(db, person_id)
    if not db_person:
        return False
    
    db.delete(db_person)
    db.commit()
    return True

def update_face_encodings(db: Session, person_id: str, face_encodings: List[float]) -> Optional[Person]:
    db_person = get_person(db, person_id)
    if not db_person:
        return None
    
    db_person.face_encodings = face_encodings
    db.commit()
    db.refresh(db_person)
    return db_person