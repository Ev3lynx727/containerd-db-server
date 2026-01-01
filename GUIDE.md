# Database Connector Server - Setup Guide

## Overview

The Database Connector Server is a high-performance FastAPI application with MySQL, Redis, and Nginx, built with a 3-tier architecture for enterprise-grade database operations.

## Architecture

- **Frontend Layer**: Nginx reverse proxy with rate limiting and security headers
- **API Layer**: FastAPI with async operations and comprehensive validation
- **Data Layer**: MySQL with SQLModel for type-safe database operations
- **Cache Layer**: Redis for session management and caching
- **Process Management**: Supervisor for reliable service orchestration

## Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Git

## Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd containerd-db-server
```

### 2. Environment Configuration

Copy the updated environment file:

```bash
cp .env.updated .env
```

The environment file includes:
- Database connection settings
- Redis configuration
- Security keys (auto-generated)
- Performance tuning options
- Rate limiting settings

### 3. Install Dependencies

For container deployment (recommended):

```bash
# No action needed - dependencies are installed in Docker
```

For local development:

```bash
cd connector-server
pip install -r requirements.txt
```

### 4. Launch Services

Start all services with Docker Compose:

```bash
docker compose -f docker-compose.server.yml up --build
```

This will:
- Build the monolithic container with all services
- Initialize MySQL database with schema and sample data
- Start Redis on port 6380
- Launch FastAPI on port 3000
- Configure Nginx reverse proxy on port 80

### 5. Verify Installation

Check service health:

```bash
# API Health Check
curl http://localhost/health

# Database Connection Test
curl http://localhost/api/v1/health

# View logs
docker compose -f docker-compose.server.yml logs -f
```

## Configuration Details

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CONNECTOR_SERVER_MODE` | Environment mode | `development` |
| `CONNECTOR_DATABASE_URL` | MySQL connection URL | `mysql://connector_user:password@mysql-db:3306/connector_db` |
| `CONNECTOR_REDIS_URL` | Redis connection URL | `redis://redis-cache:6380/0` |
| `CONNECTOR_SECRET_KEY` | JWT signing key | Auto-generated |
| `CONNECTOR_API_PORT` | FastAPI port | `3000` |
| `CONNECTOR_MAX_CONNECTIONS` | Database pool size | `100` |

### Database Schema

The application uses SQLModel with the following tables:
- `users` - User accounts with authentication
- `api_keys` - API key management
- `query_history` - Query execution tracking
- `user_permissions` - Permission management

### Security Features

- JWT-based authentication
- API key authentication
- bcrypt password hashing
- Rate limiting (100 requests/minute)
- CORS protection
- Security headers (XSS, CSRF, etc.)

## Development Workflow

### Local Development

1. Start only the database services:
```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up mysql-db redis-cache -d
```

2. Run FastAPI locally:
```bash
cd connector-server
export CONNECTOR_DATABASE_URL="mysql://connector_user:connector_user_password_2024@localhost:3306/connector_db"
export CONNECTOR_REDIS_URL="redis://localhost:6380/0"
uvicorn main:app --reload --host 0.0.0.0 --port 3000
```

### Testing

Run the test suite:

```bash
docker-compose -f docker-compose.yml -f docker-compose.test.yml up --build
```

### Code Quality

Format and lint code:

```bash
make format  # Format with black and isort
make lint    # Run flake8 and mypy
```

## API Documentation

Once running, access:
- **API Docs**: `http://localhost/docs` (Swagger UI)
- **ReDoc**: `http://localhost/redoc`
- **Health Check**: `http://localhost/health`

## Troubleshooting

### Common Issues

1. **Port conflicts**: Ensure ports 3306, 6379, 3000, 80 are available
2. **MySQL connection errors**: Check database credentials in `.env`
3. **Redis connection errors**: Verify Redis is running on port 6380
4. **Permission errors**: Ensure Docker has access to project directory

### Logs and Debugging

View service logs:
```bash
# All services
docker compose -f docker-compose.server.yml logs -f

# Specific service
docker compose -f docker-compose.server.yml logs -f connector-api

# Database logs
docker compose -f docker-compose.server.yml logs -f mysql-db
```

### Database Access

Connect to MySQL directly:
```bash
docker-compose -f docker-compose.server.yml exec mysql-db mysql -u connector_user -p connector_db
```

## Deployment

### Production Deployment

1. Update `.env` for production settings:
```bash
CONNECTOR_SERVER_MODE=production
CONNECTOR_DEBUG=false
CONNECTOR_SECRET_KEY=<your-secure-key>
```

2. Use production Docker Compose:
```bash
docker-compose -f docker-compose.server.yml -f docker-compose.prod.yml up -d
```

### Scaling

The architecture supports horizontal scaling:
- Add more API instances behind the load balancer
- Scale database read replicas
- Use Redis cluster for cache scaling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Run `make lint` and `make test`
5. Submit a pull request

## License

MIT License - see LICENSE file for details.</content>
<parameter name="filePath">guide.md