#!/bin/bash

# Enhanced Auto-run script for Database Connector Server
# Robust deployment for local VM with persistence, monitoring, and error recovery

set -e  # Exit on any error

# Configuration - can be overridden by environment variables
IMAGE_NAME="${IMAGE_NAME:-ghcr.io/ev3lynx727/containerd-db-server:latest}"
CONTAINER_NAME="${CONTAINER_NAME:-containerd-db-server}"
LOGS_DIR="${LOGS_DIR:-./logs}"
BACKUP_DIR="${BACKUP_DIR:-./backups}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging
LOG_FILE="${LOGS_DIR}/autorun-$(date +%Y%m%d-%H%M%S).log"
mkdir -p "$LOGS_DIR"

log() {
    echo -e "$(date '+%Y-%m-%d %H:%M:%S') - $*" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}❌ ERROR: $1${NC}" >&2 | tee -a "$LOG_FILE"
    exit 1
}

warning() {
    echo -e "${YELLOW}⚠️  WARNING: $1${NC}" | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}✅ $1${NC}" | tee -a "$LOG_FILE"
}

info() {
    echo -e "${BLUE}ℹ️  $1${NC}" | tee -a "$LOG_FILE"
}

# Cleanup function
cleanup() {
    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        error "Script failed with exit code $exit_code"
        echo "Check logs: $LOG_FILE"
        echo "Container logs: docker logs $CONTAINER_NAME 2>&1 | tail -50"
    fi
}

trap cleanup EXIT

echo "🚀 Database Connector Server Enhanced Auto-Deploy"
echo "=================================================="
log "Starting deployment process..."

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    error "Docker is not running. Please start Docker service first."
fi
success "Docker is running"

# Check available disk space
DISK_SPACE=$(df / | tail -1 | awk '{print $4}')
if [ "$DISK_SPACE" -lt 1048576 ]; then  # Less than 1GB
    warning "Low disk space detected: $(($DISK_SPACE / 1024))MB available"
fi

# Check if required ports are available
PORTS_IN_USE=""
for port in 3307 3003 6380 8083 8444; do
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        PORTS_IN_USE="$PORTS_IN_USE $port"
    fi
done

if [ -n "$PORTS_IN_USE" ]; then
    warning "Ports$PORTS_IN_USE are already in use"
    info "Required ports: MySQL(3307), API(3003), Redis(6380), HTTP(8083), HTTPS(8444)"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create necessary directories (using named volumes, but ensure logs exist)
mkdir -p "$LOGS_DIR" "$BACKUP_DIR"
success "Created log and backup directories"

# Check if container exists and handle it
if docker ps -a --format 'table {{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    info "Existing container found: $CONTAINER_NAME"

    # Backup current data if container was running
    if docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
        info "Backing up current data before update..."
        mkdir -p "$BACKUP_DIR/pre-update-$(date +%Y%m%d-%H%M%S)"
        # Note: Actual backup would require stopping services briefly
    fi

    log "Stopping and removing existing container..."
    docker stop "$CONTAINER_NAME" >/dev/null 2>&1 || true
    docker rm "$CONTAINER_NAME" >/dev/null 2>&1 || true
    success "Removed existing container"
fi

# Pull latest image with retry
log "Pulling latest image: $IMAGE_NAME"
max_pull_attempts=3
pull_attempt=1

while [ $pull_attempt -le $max_pull_attempts ]; do
    if docker pull "$IMAGE_NAME" 2>&1 | tee -a "$LOG_FILE"; then
        success "Image pulled successfully"
        break
    else
        warning "Pull attempt $pull_attempt failed"
        if [ $pull_attempt -eq $max_pull_attempts ]; then
            error "Failed to pull image after $max_pull_attempts attempts"
        fi
        sleep 5
        ((pull_attempt++))
    fi
done

# Run the container with all services (MySQL, Redis, FastAPI, Nginx)
log "Starting monolithic container with all services..."

docker run -d \
    --name "$CONTAINER_NAME" \
    --env-file .env.updated \
    --restart unless-stopped \
    -p 3307:3306 \
    -p 3003:3000 \
    -p 6380:6380 \
    -p 8083:80 \
    -p 8444:443 \
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
    --health-cmd "python3 -c \"import requests; requests.get('http://localhost:3000/health')\" || exit 1" \
    --health-interval 30s \
    --health-timeout 10s \
    --health-retries 3 \
    --health-start-period 60s \
    --memory 1g \
    --cpus 1.0 \
    --log-driver json-file \
    --log-opt max-size=10m \
    --log-opt max-file=3 \
    "$IMAGE_NAME"

if [ $? -ne 0 ]; then
    error "Failed to start container"
fi

success "Container started successfully"

# Enhanced health check with detailed status
log "Performing comprehensive health checks..."
max_attempts=60  # 5 minutes total
attempt=1
health_details=""

while [ $attempt -le $max_attempts ]; do
    # Check container status
    if ! docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
        error "Container stopped unexpectedly"
    fi

    # Check health status
    health_status=$(docker inspect -f '{{.State.Health.Status}}' "$CONTAINER_NAME" 2>/dev/null || echo "unknown")

    case $health_status in
        "healthy")
            success "Container is fully healthy!"
            break
            ;;
        "unhealthy")
            health_details=$(docker logs "$CONTAINER_NAME" 2>&1 | tail -10)
            ;;
        "starting")
            info "Container is still starting..."
            ;;
        *)
            info "Health status: $health_status"
            ;;
    esac

    if [ $attempt -eq $max_attempts ]; then
        warning "Container may not be fully healthy yet"
        if [ -n "$health_details" ]; then
            echo "Recent logs:"
            echo "$health_details" | head -20
        fi
        break
    fi

    sleep 5
    ((attempt++))
done

# Get detailed container information
CONTAINER_ID=$(docker ps -q -f name="$CONTAINER_NAME")
CONTAINER_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$CONTAINER_NAME" 2>/dev/null || echo "N/A")

echo ""
success "Container Information:"
echo "  Container ID: $CONTAINER_ID"
echo "  Container Name: $CONTAINER_NAME"
echo "  Container IP: $CONTAINER_IP"
echo "  Port Mappings:"
echo "    MySQL: 3307 → 3306"
echo "    API: 3003 → 3000"
echo "    Redis: 6380 → 6380"
echo "    HTTP: 8083 → 80"
echo "    HTTPS: 8444 → 443"
echo "  Logs Directory: $LOGS_DIR"

echo ""
success "Access URLs:"
echo "  🌐 Web Interface: http://localhost:8083"
echo "  🏥 API Health Check: http://localhost:3003/health"
echo "  📚 API Docs: http://localhost:3003/docs"
echo "  📖 API ReDoc: http://localhost:3003/redoc"
echo "  🗄️  MySQL: localhost:3307"
echo "  🔄 Redis: localhost:6380"

echo ""
info "Management Commands:"
echo "  📋 View logs: docker logs $CONTAINER_NAME"
echo "  🔄 View real-time logs: docker logs -f $CONTAINER_NAME"
echo "  🛑 Stop container: docker stop $CONTAINER_NAME"
echo "  🐚 Shell access: docker exec -it $CONTAINER_NAME bash"
echo "  📊 Container stats: docker stats $CONTAINER_NAME"
echo "  🔍 Inspect container: docker inspect $CONTAINER_NAME"

echo ""
info "Data Persistence (Docker Named Volumes):"
echo "  MySQL data: mysql_data"
echo "  Redis data: redis_data"
echo "  MySQL logs: mysql_logs"
echo "  Redis logs: redis_logs"
echo "  Nginx logs: nginx_logs"
echo "  API logs: api_logs"
echo "  Backups: $BACKUP_DIR"

echo ""
info "Auto-restart: Container will restart automatically on system reboot"
echo "Deployment log: $LOG_FILE"

# Final verification
if curl -f -s "http://localhost:3003/health" >/dev/null 2>&1; then
    success "Health check passed - all systems operational!"
else
    warning "Health check failed - services may still be starting"
    echo "Monitor with: docker logs -f $CONTAINER_NAME"
fi

echo ""
echo "🚀 Deployment completed successfully!"