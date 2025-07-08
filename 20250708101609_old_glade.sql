-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgvector";

-- Create initial tenant
INSERT INTO tenants (id, name, domain, is_active, created_at)
VALUES (
    'demo-tenant',
    'Demo Organization',
    'demo.smartsecurec3.com',
    true,
    NOW()
) ON CONFLICT (id) DO NOTHING;

-- Create initial admin user
INSERT INTO users (id, email, full_name, hashed_password, role, is_active, tenant_id, created_at)
VALUES (
    '1',
    'admin@demo.com',
    'Admin User',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewjGxzHPb/9a8KNy', -- password: admin123
    'admin',
    true,
    'demo-tenant',
    NOW()
) ON CONFLICT (id) DO NOTHING;

-- Create sample cameras
INSERT INTO cameras (id, name, rtsp_url, location, is_active, ai_detection_enabled, tenant_id, created_at)
VALUES 
    ('cam-1', 'Main Gate Camera', 'rtsp://demo:demo@192.168.1.100:554/stream1', 'Main Gate', true, true, 'demo-tenant', NOW()),
    ('cam-2', 'Warehouse A Camera', 'rtsp://demo:demo@192.168.1.101:554/stream1', 'Warehouse A', true, true, 'demo-tenant', NOW()),
    ('cam-3', 'Exit Gate Camera', 'rtsp://demo:demo@192.168.1.102:554/stream1', 'Exit Gate', false, true, 'demo-tenant', NOW())
ON CONFLICT (id) DO NOTHING;

-- Create sample persons
INSERT INTO persons (id, name, employee_id, department, role, authorized, tenant_id, created_at)
VALUES 
    ('person-1', 'John Doe', 'EMP001', 'Security', 'Security Officer', true, 'demo-tenant', NOW()),
    ('person-2', 'Jane Smith', 'EMP002', 'Operations', 'Warehouse Manager', true, 'demo-tenant', NOW()),
    ('person-3', 'Bob Johnson', 'EMP003', 'Logistics', 'Logistics Coordinator', true, 'demo-tenant', NOW())
ON CONFLICT (id) DO NOTHING;

-- Create sample vehicles
INSERT INTO vehicles (id, license_plate, vehicle_type, owner_name, company, authorized, tenant_id, created_at)
VALUES 
    ('vehicle-1', 'ABC-1234', 'truck', 'John Transport', 'ABC Logistics', true, 'demo-tenant', NOW()),
    ('vehicle-2', 'XYZ-5678', 'car', 'Jane Doe', 'Internal Security', true, 'demo-tenant', NOW()),
    ('vehicle-3', 'DEF-9012', 'van', 'Bob Delivery', 'Fast Delivery Co.', false, 'demo-tenant', NOW())
ON CONFLICT (id) DO NOTHING;

-- Create sample events
INSERT INTO events (id, event_type, description, camera_id, confidence, metadata, tenant_id, created_at)
VALUES 
    ('event-1', 'face_detection', 'Face detected: John Doe (Employee ID: EMP001)', 'cam-1', 0.95, '{"person_id": "person-1", "match_score": 0.95}', 'demo-tenant', NOW() - INTERVAL '1 hour'),
    ('event-2', 'vehicle_detection', 'Vehicle detected: ABC-1234 (Authorized)', 'cam-3', 0.88, '{"vehicle_id": "vehicle-1", "license_plate": "ABC-1234"}', 'demo-tenant', NOW() - INTERVAL '2 hours'),
    ('event-3', 'intrusion', 'Unauthorized person detected in restricted area', 'cam-2', 0.92, '{"area": "restricted", "alert_level": "high"}', 'demo-tenant', NOW() - INTERVAL '3 hours')
ON CONFLICT (id) DO NOTHING;