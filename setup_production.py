#!/usr/bin/env python3
"""
Production setup script for SMARTSECUREC3
Run this script to set up initial production data
"""

import os
import sys
from sqlalchemy.orm import Session
from getpass import getpass
import uuid

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, init_db
from models import Tenant, User
from crud.user import create_user, get_user_by_email
from schemas import UserCreate

def setup_production():
    print("🚀 SMARTSECUREC3 Production Setup")
    print("=" * 50)
    
    # Initialize database
    print("Initializing database...")
    init_db()
    
    db = SessionLocal()
    
    try:
        # Create tenant
        print("\n📋 Setting up organization...")
        org_name = input("Organization name: ")
        org_domain = input("Organization domain (e.g., yourcompany.com): ")
        
        tenant_id = str(uuid.uuid4())
        tenant = Tenant(
            id=tenant_id,
            name=org_name,
            domain=org_domain,
            is_active=True
        )
        db.add(tenant)
        db.commit()
        print(f"✅ Organization '{org_name}' created")
        
        # Create admin user
        print("\n👤 Creating admin user...")
        admin_email = input("Admin email: ")
        admin_name = input("Admin full name: ")
        admin_password = getpass("Admin password: ")
        admin_password_confirm = getpass("Confirm password: ")
        
        if admin_password != admin_password_confirm:
            print("❌ Passwords don't match!")
            return
        
        # Check if user already exists
        existing_user = get_user_by_email(db, admin_email, tenant_id)
        if existing_user:
            print("❌ User already exists!")
            return
        
        admin_user = UserCreate(
            email=admin_email,
            full_name=admin_name,
            password=admin_password,
            role="admin"
        )
        
        db_user = create_user(db, admin_user, tenant_id)
        print(f"✅ Admin user '{admin_email}' created")
        
        print("\n🎉 Production setup completed!")
        print(f"Tenant ID: {tenant_id}")
        print(f"Admin User ID: {db_user.id}")
        print("\nYou can now log in with your admin credentials.")
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    setup_production()