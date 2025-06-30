# AI Chat Application

A full-stack AI chat application with FastAPI backend and React frontend.

## Docker Setup

### Prerequisites
- Docker
- Docker Compose

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cursortest
   ```

2. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Development Commands

**Start services in detached mode:**
```bash
docker-compose up -d
```

**View logs:**
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend
docker-compose logs frontend
```

**Stop services:**
```bash
docker-compose down
```

**Rebuild and restart:**
```bash
docker-compose down
docker-compose up --build
```

### Individual Service Commands

**Backend only:**
```bash
docker-compose up backend
```

**Frontend only:**
```bash
docker-compose up frontend
```

### Environment Variables

The application uses the following environment variables:

- `VITE_API_URL`: Backend API URL (default: http://localhost:8000)
- `PYTHONPATH`: Python path for the backend (set automatically)

### Project Structure

```
cursortest/
├── backend/           # FastAPI backend
│   ├── app/          # Application code
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/         # React frontend
│   ├── src/          # Source code
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

### Troubleshooting

1. **Port conflicts**: If ports 3000 or 8000 are already in use, modify the ports in `docker-compose.yml`

2. **Build issues**: Clean Docker cache and rebuild
   ```bash
   docker system prune -a
   docker-compose up --build
   ```

3. **Database issues**: The backend uses SQLite by default. For production, consider using a proper database service. 