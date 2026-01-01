# Database Connector Server

A comprehensive server-side database connector stack with MySQL, Redis caching, FastAPI, and Nginx reverse proxy.

## Overview

This project provides a production-ready database connector service with the following components:

- **MySQL Database**: Primary data storage with custom configuration
- **FastAPI Application**: RESTful API for database operations
- **Redis Cache**: Performance caching layer
- **Nginx Proxy**: Load balancing and SSL termination
- **Monitoring**: Netdata integration for observability

## Project Structure

```
database-connector-server/
├── docker-compose.server.yml          # Main server stack configuration
├── docker-compose.override.yml        # Environment-specific overrides
├── docker-compose.dev.yml             # Development configuration
├── docker-compose.prod.yml            # Production configuration
├── docker-compose.test.yml            # Testing configuration
├── docker-compose.yml                 # Base docker-compose configuration
├── .env*                              # Environment configurations
│
├── database/                          # MySQL database layer
│   ├── Dockerfile                     # MySQL container image
│   ├── init/                          # Database initialization scripts
│   │   ├── 01-init-schema.sql         # Schema creation
│   │   ├── 02-init-data.sql           # Initial data
│   │   └── 03-init-permissions.sql    # User permissions
│   ├── conf.d/                        # MySQL configuration files
│   │   ├── mysql.cnf                  # MySQL settings
│   │   └── performance.cnf            # Performance tuning
│   └── scripts/                       # Database management scripts
│       ├── backup.sh                  # Backup script
│       ├── restore.sh                 # Restore script
│       └── healthcheck.sh             # Health check script
│
├── connector-server/                  # FastAPI application layer
│   ├── Dockerfile                     # API container image
│   ├── requirements.txt               # Python dependencies
│   ├── main.py                        # FastAPI application entry point
│   ├── core/                          # Core functionality
│   │   ├── config.py                  # Application configuration
│   │   ├── security.py                # Security utilities
│   │   └── database.py                # Database connection management
│   ├── auth/                          # Authentication system
│   │   ├── jwt.py                     # JWT token handling
│   │   ├── users.py                   # User management
│   │   ├── api_keys.py                # API key management
│   │   └── dependencies.py            # FastAPI dependencies
│   ├── models/                        # Data models
│   │   ├── user.py                    # User models
│   │   ├── api_key.py                 # API key models
│   │   └── query_history.py           # Query history models
│   └── [Additional modules in progress]
│
├── redis/                             # Redis cache layer
│   ├── redis.conf                     # Redis configuration
│   └── scripts/                       # Redis management scripts
│       └── [Scripts to be added]
│
├── nginx/                             # Reverse proxy layer
│   ├── nginx.conf                     # Main nginx configuration
│   └── [SSL and scripts to be added]
│
├── monitoring/                        # Monitoring and observability
│   └── netdata/                       # Netdata configuration
│       └── docker.conf                # Docker monitoring configuration
│
├── scripts/                           # Project management scripts
│   └── [Scripts to be added]
│
├── docs/                              # Documentation
│   └── README.md                      # This file
│
├── docker/                            # Docker-related files
│   └── [Dockerfiles to be added]
│
├── workflows/                         # CI/CD workflows (to be moved to .github/)
│
├── .gitignore                         # Git ignore rules
├── .dockerignore                      # Docker ignore rules
├── Makefile                           # Common tasks
├── pyproject.toml                     # Python project configuration
├── pytest.ini                         # Test configuration
├── mypy.ini                           # Type checking configuration
├── .pre-commit-config.yaml            # Pre-commit hooks
├── LICENSE                            # MIT License
└── README.md                          # Project README
```

## Quick Start

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM minimum

### Development Setup
```bash
# Clone repository
git clone <repository-url>
cd database-connector-server

# Copy environment file
cp .env.development .env

# Start development stack
make up

# Run tests
make test

# Check health
make health
```

### Production Deployment
```bash
# Deploy production stack
make build-prod
make up-prod

# Check status
make status
```

## Configuration

### Environment Variables
- `.env.development`: Development configuration
- `.env.production`: Production configuration
- `.env`: Base environment variables

### Docker Compose Files
- `docker-compose.yml`: Base configuration with networks and volumes
- `docker-compose.server.yml`: Main server services
- `docker-compose.override.yml`: Development overrides
- `docker-compose.prod.yml`: Production-specific settings
- `docker-compose.test.yml`: Testing configuration

## Services

### MySQL Database (Port 3306)
- Custom MySQL 8.0 configuration
- UTF8MB4 character set
- Connection pooling and performance tuning
- Automated backups and health checks

### FastAPI Application (Port 3000)
- RESTful API for database operations
- JWT and API key authentication
- Rate limiting and security middleware
- Comprehensive logging and audit trails

### Redis Cache (Port 6379)
- In-memory caching for performance
- Persistence configuration
- Connection pooling

### Nginx Proxy (Ports 80/443)
- Load balancing and SSL termination
- Security headers and rate limiting
- Health checks and monitoring

## API Documentation

API endpoints and usage documentation will be available at `/docs` when the service is running.

## Development

### Code Quality
```bash
# Run linting
make lint

# Format code
make format

# Type checking
mypy connector-server/
```

### Testing
```bash
# Run tests
make test

# Run with coverage
pytest --cov=connector-server --cov-report=html
```

### Database Operations
```bash
# Create tables
make db-init

# Run migrations
make db-migrate
```

## Security

- API key authentication for all operations
- JWT tokens for session management
- Rate limiting per API key
- Input validation and SQL injection prevention
- Comprehensive audit logging
- SSL/TLS encryption for external access

## Monitoring

- Netdata integration for real-time monitoring
- Docker container metrics
- MySQL performance monitoring
- Redis cache statistics
- Nginx access logs and performance

## Backup and Recovery

### Database Backup
```bash
make backup
```

### Database Recovery
```bash
make restore BACKUP_FILE=path/to/backup.sql
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run linting and tests
6. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Status

This project is currently in development. The following components are implemented:

- ✅ Project structure and configuration files
- ✅ Docker Compose configurations
- ✅ MySQL database setup with initialization scripts
- ✅ Basic FastAPI application structure
- 🔄 API implementation (in progress)
- ⏳ Redis and Nginx configurations
- ⏳ Monitoring setup
- ⏳ Testing framework
- ⏳ Documentation completion

See the [current plan](current_plan_server_side.md) for detailed implementation roadmap.