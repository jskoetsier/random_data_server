#!/bin/bash

# Random Data Server Docker Compose Startup Script

set -e

echo "Starting Random Data Server with Docker Compose..."
echo "This will automatically handle privileged ports 80 and 443"
echo "Press Ctrl+C to stop the server"
echo ""

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null && ! command -v docker &> /dev/null; then
    echo "❌ Neither docker-compose nor docker is available."
    echo "Please install Docker and Docker Compose first."
    exit 1
fi

# Use docker compose (newer syntax) if available, fallback to docker-compose
if docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

echo "Using: $COMPOSE_CMD"
echo ""

# Build and start the service
echo "Building and starting Random Data Server..."
$COMPOSE_CMD up --build

# Cleanup function for graceful shutdown
cleanup() {
    echo ""
    echo "Shutting down Random Data Server..."
    $COMPOSE_CMD down
    echo "Server stopped."
}

# Set trap for cleanup on script exit
trap cleanup EXIT INT TERM