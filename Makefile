# Database Connector Server - Makefile

.PHONY: help build up down logs clean test lint format install deploy backup restore

# Default target
help: ## Show this help message
	@echo "Database Connector Server Makefile"
	@echo ""
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

# Development commands
build: ## Build all services
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml build

up: ## Start all services in development mode
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

down: ## Stop all services
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml down

logs: ## Show logs from all services
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml logs -f

# Production commands
build-prod: ## Build for production
	docker-compose -f docker-compose.yml -f docker-compose.server.yml -f docker-compose.prod.yml build

up-prod: ## Start services in production mode
	docker-compose -f docker-compose.yml -f docker-compose.server.yml -f docker-compose.prod.yml up -d

down-prod: ## Stop production services
	docker-compose -f docker-compose.yml -f docker-compose.server.yml -f docker-compose.prod.yml down

# Testing
test: ## Run tests
	docker-compose -f docker-compose.yml -f docker-compose.test.yml up -d mysql-db redis-cache
	sleep 10
	docker-compose -f docker-compose.yml -f docker-compose.test.yml run --rm connector-api pytest
	docker-compose -f docker-compose.yml -f docker-compose.test.yml down

# Code quality
lint: ## Run linting
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec connector-api flake8
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec connector-api mypy

format: ## Format code
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec connector-api black .
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec connector-api isort .

# Dependencies
install: ## Install Python dependencies
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec connector-api pip install -r requirements.txt

# Operations
deploy: ## Deploy to production
	./scripts/deploy.sh

backup: ## Backup database and Redis
	./scripts/backup.sh

restore: ## Restore from backup
	./scripts/restore.sh $(filter-out $@,$(MAKECMDGOALS))

# Cleanup
clean: ## Remove all containers, volumes, and images
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml down -v --rmi all
	docker-compose -f docker-compose.yml -f docker-compose.test.yml down -v --rmi all

clean-logs: ## Clean log files
	find . -name "*.log" -delete
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec connector-api rm -rf /app/logs/*

# Database operations
db-init: ## Initialize database
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec mysql-db mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS connector_db;"

db-migrate: ## Run database migrations
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec connector-api alembic upgrade head

# Monitoring
status: ## Show service status
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml ps

health: ## Check service health
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec connector-api curl -f http://localhost:3000/health || exit 1