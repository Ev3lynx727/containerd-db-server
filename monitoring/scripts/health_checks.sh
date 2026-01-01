#!/bin/bash

echo "Running health checks for database connector stack..."

# Check Netdata
echo "Checking Netdata..."
if curl -s http://localhost:19999/api/v1/info > /dev/null; then
    echo "✓ Netdata is healthy"
else
    echo "✗ Netdata is not responding"
fi

# Check Docker containers (when stack is running)
echo "Checking Docker containers..."
if docker ps | grep -q mysql-db-server; then
    echo "✓ MySQL container is running"
else
    echo "- MySQL container not found (stack may not be running)"
fi

if docker ps | grep -q connector-api-server; then
    echo "✓ API container is running"
else
    echo "- API container not found (stack may not be running)"
fi

if docker ps | grep -q redis-cache-server; then
    echo "✓ Redis container is running"
else
    echo "- Redis container not found (stack may not be running)"
fi

if docker ps | grep -q nginx-proxy-server; then
    echo "✓ Nginx container is running"
else
    echo "- Nginx container not found (stack may not be running)"
fi

echo "Health check complete."
