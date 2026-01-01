#!/bin/bash

# Auto-run script for Database Connector Server
# Pulls latest image from GHCR and runs the full stack container

set -e  # Exit on any error

# Configuration
IMAGE_NAME="ghcr.io/ev3lynx727/containerd-db-server:latest"
CONTAINER_NAME="containerd-db-server"
HOST_PORT=80

echo "🚀 Starting Database Connector Server Auto-Run..."
echo "================================================"

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "❌ Error: Docker is not running. Please start Docker first."
    exit 1
fi

# Check if container is already running and stop it
if docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
    echo "🛑 Stopping existing container: $CONTAINER_NAME"
    docker stop "$CONTAINER_NAME" >/dev/null 2>&1
    docker rm "$CONTAINER_NAME" >/dev/null 2>&1
fi

# Pull latest image
echo "📥 Pulling latest image: $IMAGE_NAME"
if ! docker pull "$IMAGE_NAME"; then
    echo "❌ Error: Failed to pull image $IMAGE_NAME"
    echo "   Make sure you're logged in to GHCR:"
    echo "   docker login ghcr.io -u YOUR_USERNAME"
    exit 1
fi

# Run the container
echo "🐳 Starting container: $CONTAINER_NAME"
docker run -d \
    --name "$CONTAINER_NAME" \
    --restart unless-stopped \
    -p "$HOST_PORT":80 \
    --health-cmd "curl -f http://localhost/health || exit 1" \
    --health-interval 30s \
    --health-timeout 10s \
    --health-retries 3 \
    --health-start-period 60s \
    "$IMAGE_NAME"

# Wait for container to be healthy
echo "⏳ Waiting for container to be healthy..."
max_attempts=30
attempt=1

while [ $attempt -le $max_attempts ]; do
    if docker ps -q -f name="$CONTAINER_NAME" | xargs docker inspect -f '{{.State.Health.Status}}' 2>/dev/null | grep -q "healthy"; then
        echo "✅ Container is healthy!"
        break
    fi

    echo "   Attempt $attempt/$max_attempts: Container not yet healthy..."
    sleep 5
    ((attempt++))
done

if [ $attempt -gt $max_attempts ]; then
    echo "⚠️  Warning: Container may not be fully healthy yet, but it's running."
    echo "   Check logs: docker logs $CONTAINER_NAME"
fi

# Get container status
CONTAINER_ID=$(docker ps -q -f name="$CONTAINER_NAME")
if [ -n "$CONTAINER_ID" ]; then
    echo ""
    echo "🎉 Database Connector Server is running!"
    echo "=========================================="
    echo "Container ID: $CONTAINER_ID"
    echo "Container Name: $CONTAINER_NAME"
    echo "Access URLs:"
    echo "  - Web Interface: http://localhost"
    echo "  - Health Check: http://localhost/health"
    echo "  - API Docs: http://localhost/docs (if available)"
    echo ""
    echo "Commands:"
    echo "  - View logs: docker logs $CONTAINER_NAME"
    echo "  - Stop container: docker stop $CONTAINER_NAME"
    echo "  - Shell access: docker exec -it $CONTAINER_NAME bash"
    echo ""
    echo "Container will restart automatically unless stopped."
else
    echo "❌ Error: Failed to start container"
    exit 1
fi