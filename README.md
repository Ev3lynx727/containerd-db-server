# Database Connector Server

A production-ready, monolithic containerized database connector API with FastAPI, MySQL, Redis, and Nginx.

## Overview

This project provides a complete containerized database server stack in a single monolithic container:
- **MySQL 8.0** database server with custom configuration
- **FastAPI** async web framework with comprehensive validation
- **Redis 7** caching layer with persistence
- **Nginx** reverse proxy with security headers
- **Supervisor** process management for all services

## Quick Start

### Automated Deployment (Recommended)
```bash
# Clone repository
git clone https://github.com/Ev3lynx727/containerd-db-server.git
cd containerd-db-server

# Run automated deployment
chmod +x autorun.sh
./autorun.sh
```

### Manual Deployment
```bash
# Clone repository
git clone https://github.com/Ev3lynx727/containerd-db-server.git
cd containerd-db-server

# Copy environment configuration
cp .env.updated .env

# Pull and run container
docker pull ghcr.io/ev3lynx727/containerd-db-server:latest
docker run -d --name containerd-db-server \
  --env-file .env.updated \
  -p 3307:3306 -p 3003:3000 -p 6380:6380 -p 8083:80 -p 8444:443 \
  -v mysql_data:/var/lib/mysql \
  -v mysql_logs:/var/log/mysql \
  -v redis_data:/data \
  -v redis_logs:/var/log/redis \
  -v nginx_logs:/var/log/nginx \
  -v api_logs:/app/logs \
  -v ./database/init:/docker-entrypoint-initdb.d:ro \
  -v ./database/conf.d:/etc/mysql/mysql.conf.d:ro \
  -v ./redis/redis.conf:/etc/redis/redis.conf:ro \
  -v ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro \
  ghcr.io/ev3lynx727/containerd-db-server:latest
```

## Architecture

```
┌─────────────────┐
│   Nginx (80)    │ ← External Access (8083)
│   Reverse Proxy │
└─────────────────┘
         │
    ┌────▼────┐
    │ FastAPI │ ← API Access (3003)
    │  (3000) │
    └────┬────┘
         │
    ┌────▼────┐
    │ MySQL   │ ← Database Access (3307)
    │  (3306) │
    └────┬────┘
         │
    ┌────▼────┐
    │  Redis  │ ← Cache Access (6380)
    │  (6380) │
    └─────────┘
```

## Access URLs

Once deployed, access your services at:

| Service | URL | Description |
|---------|-----|-------------|
| **Web Interface** | http://localhost:8083 | Nginx reverse proxy |
| **API Health** | http://localhost:3003/health | FastAPI health check |
| **API Docs** | http://localhost:3003/docs | Swagger UI documentation |
| **API ReDoc** | http://localhost:3003/redoc | Alternative API docs |
| **MySQL** | localhost:3307 | Database connection |
| **Redis** | localhost:6380 | Cache connection |

## Features

- ✅ **Async Operations** - FastAPI with SQLAlchemy async support
- ✅ **Type Safety** - SQLModel for database operations
- ✅ **Security** - JWT authentication, CORS, rate limiting
- ✅ **Monitoring** - Health checks and comprehensive logging
- ✅ **Persistence** - Docker named volumes for data
- ✅ **Zero Port Conflicts** - Carefully selected port mappings

## Database

The container includes a fully configured MySQL 8.0 database with:
- Custom performance optimizations
- UTF8MB4 character set
- Automatic schema initialization
- User management and permissions

**Connect**: `mysql -h localhost -P 3307 -u connector_user -p`

## Development

For local development with hot reload:
```bash
# Install dependencies
pip install -r connector-server/requirements.txt

# Run FastAPI locally
cd connector-server
uvicorn main:app --reload --host 0.0.0.0 --port 3000
```

## Documentation

- [Setup Guide](GUIDE.md) - Comprehensive setup instructions
- [Port Conflicts](PORT_CONFLICTS.md) - Port resolution details
- [Workflow Updates](WORKFLOW_UPDATES.md) - CI/CD changes

## License

See LICENSE file for details.
