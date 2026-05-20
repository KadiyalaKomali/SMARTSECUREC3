# SMARTSECUREC3 - AI-Powered Contextual Warehouse Surveillance

A comprehensive full-stack SaaS application for AI-powered warehouse surveillance with facial recognition, vehicle detection, and natural language querying capabilities.

## Features

### 🔐 Authentication & Authorization
- JWT-based authentication
- Role-based access control (Admin, Security, Manager)
- Multi-tenant architecture

### 📹 Video Management
- Real-time CCTV feed integration
- Camera management and configuration
- Live video streaming with WebSocket support

### 🤖 AI Detection Capabilities
- **Face Recognition**: Real-time facial recognition with ArcFace embeddings
- **Vehicle Detection**: License plate recognition using YOLOv8 and PaddleOCR
- **Object Detection**: Gunny bag counting and general object detection
- **Intrusion Detection**: Unauthorized access detection in restricted zones

### 📊 Dashboard & Analytics
- Real-time statistics and metrics
- Event monitoring and alerts
- Interactive charts and visualizations
- Comprehensive audit logs

### 🔍 Search & Query
- Natural language event querying
- Advanced filtering and search capabilities
- Historical data analysis

### 🛡️ Security & Compliance
- DPDP 2023 compliance features
- Data masking and consent management
- Secure API endpoints with proper validation

## Tech Stack

### Frontend
- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **Zustand** for state management
- **React Router** for navigation
- **Recharts** for data visualization
- **Framer Motion** for animations

### Backend
- **FastAPI** (Python) for REST API
- **PostgreSQL** with pgvector for vector storage
- **Redis** for caching and sessions
- **Celery** for background tasks
- **WebSocket** for real-time updates

### AI & Computer Vision
- **YOLOv8** for object and vehicle detection
- **PaddleOCR** for license plate recognition
- **Face Recognition** library for facial recognition
- **OpenCV** for video processing

### Infrastructure
- **Docker** and **Docker Compose** for containerization
- **Nginx** for reverse proxy (production)
- **PostgreSQL** for primary database
- **Redis** for caching and message queuing

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.9+
- Docker & Docker Compose
- PostgreSQL 15+
- Redis 7+

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd smartsecurec3
   ```

2. **Start with Docker Compose**
   ```bash
   docker-compose up -d
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Demo Credentials
- **Admin**: admin@demo.com / admin123
- **Security**: security@demo.com / security123
- **Manager**: manager@demo.com / manager123

### Manual Setup (Development)

1. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   
   # Set environment variables
   export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/smartsecurec3
   export REDIS_URL=redis://localhost:6379
   
   # Run the server
   uvicorn main:app --reload
   ```

2. **Frontend Setup**
   ```bash
   npm install
   npm run dev
   ```

## API Documentation

The API documentation is automatically generated and available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key API Endpoints

#### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration

#### Camera Management
- `GET /api/v1/cameras` - List all cameras
- `POST /api/v1/cameras` - Create new camera
- `PUT /api/v1/cameras/{id}` - Update camera
- `DELETE /api/v1/cameras/{id}` - Delete camera

#### Person Management
- `GET /api/v1/persons` - List authorized persons
- `POST /api/v1/persons` - Add new person
- `PUT /api/v1/persons/{id}` - Update person
- `DELETE /api/v1/persons/{id}` - Remove person

#### Vehicle Management
- `GET /api/v1/vehicles` - List authorized vehicles
- `POST /api/v1/vehicles` - Add new vehicle
- `PUT /api/v1/vehicles/{id}` - Update vehicle
- `DELETE /api/v1/vehicles/{id}` - Remove vehicle

#### Event Logs
- `GET /api/v1/events` - List surveillance events
- `POST /api/v1/events` - Create new event

## Architecture

### System Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   AI Services   │
│   (React)       │────│   (FastAPI)     │────│   (Computer     │
│                 │    │                 │    │    Vision)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         │              │   Database      │              │
         └──────────────│  (PostgreSQL)   │──────────────┘
                        │  + pgvector     │
                        └─────────────────┘
```

### Database Schema
- **tenants**: Multi-tenant organization data
- **users**: User accounts and authentication
- **cameras**: CCTV camera configurations
- **persons**: Authorized personnel with face encodings
- **vehicles**: Authorized vehicles with license plates
- **events**: Surveillance events and detections
- **video_footage**: Video storage metadata

## Production Deployment

### Environment Variables
Copy `.env.example` to `.env` and configure:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/smartsecurec3

# Redis
REDIS_URL=redis://localhost:6379

# JWT
JWT_SECRET_KEY=your-secure-secret-key
JWT_ALGORITHM=HS256

# AI Configuration
AI_DETECTION_THRESHOLD=0.7
MAX_CONCURRENT_STREAMS=10
```

### Docker Production Build
```bash
# Build and run in production mode
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Security Considerations
- Change default JWT secret key
- Configure proper CORS settings
- Set up SSL/TLS certificates
- Configure firewall rules
- Enable database encryption
- Set up proper backup procedures

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Version 1.0.0
- Initial release
- Core surveillance features
- AI detection capabilities
- Multi-tenant architecture
- Real-time dashboard
- Complete authentication system
