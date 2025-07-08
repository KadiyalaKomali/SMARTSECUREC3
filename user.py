from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List
from passlib.context import CryptContext
import uuid

from ..models import User, Tenant
from ..schemas import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db: Session, user_id: str) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str, tenant_id: str = None) -> Optional[User]:
    query = db.query(User).filter(User.email == email)
    if tenant_id:
        query = query.filter(User.tenant_id == tenant_id)
    return query.first()

def get_users(db: Session, tenant_id: str, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).filter(User.tenant_id == tenant_id).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate, tenant_id: str) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(
        id=str(uuid.uuid4()),
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        role=user.role,
        tenant_id=tenant_id,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str, tenant_id: str = None) -> Optional[User]:
    user = get_user_by_email(db, email, tenant_id)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def update_user(db: Session, user_id: str, user_update: UserUpdate) -> Optional[User]:
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: str) -> bool:
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True