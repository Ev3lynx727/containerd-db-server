#!/bin/bash

echo "Setting up Netdata integration for database connector stack..."

# Check if Netdata is running
if curl -s http://localhost:19999/api/v1/info > /dev/null; then
    echo "✓ Netdata is running on localhost:19999"
else
    echo "✗ Netdata is not accessible on localhost:19999"
    echo "Please ensure Netdata container is running with Docker socket access:"
    echo "docker run -d --name netdata -p 19999:19999 -v /var/run/docker.sock:/var/run/docker.sock:ro netdata/netdata"
    exit 1
fi

# Copy configuration files
echo "Copying Netdata configuration files..."
sudo cp ../netdata/*.conf /etc/netdata/go.d/

# Restart Netdata to pick up new configuration
echo "Restarting Netdata..."
sudo systemctl restart netdata

echo "✓ Netdata integration setup complete"
echo "Monitor your containers at: http://localhost:19999"
