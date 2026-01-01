# Database Connector Server

A production-ready database connector API stack with MySQL, Redis, and monitoring capabilities.

## Overview

This project provides a complete containerized database connector stack including:
- MySQL database server
- FastAPI-based connector API
- Redis caching layer
- Nginx reverse proxy
- Netdata monitoring integration

## Quick Start

1. Clone the repository
2. Copy environment file: `cp .env.example .env`
3. Configure your environment variables
4. Deploy the stack: `docker-compose -f docker-compose.server.yml up -d`

## Architecture

```
[Nginx Proxy] → [Connector API] ↔ [MySQL DB]
                      ↘
                       [Redis Cache]
```

## Monitoring

The stack integrates with Netdata running on localhost:19999 for comprehensive monitoring of all containers and services.

## Development

For development, use the override file:
```bash
docker-compose -f docker-compose.server.yml -f docker-compose.override.yml up -d
```

## Documentation

- [API Documentation](docs/api.md)
- [Deployment Guide](docs/deployment.md)
- [Security Documentation](docs/security.md)

## License

See LICENSE file for details.
