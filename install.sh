#!/bin/bash

# Random Data Server Installation Script
# This script sets up the Random Data Server environment with Docker Compose

set -e  # Exit on any error

echo "=========================================="
echo "Random Data Server Installation Script"
echo "=========================================="

# Check if Docker is installed (required)
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   On macOS: brew install docker or download from https://docs.docker.com/desktop/mac/"
    echo "   On Ubuntu/Debian: sudo apt-get install docker.io"
    echo "   On CentOS/RHEL: sudo yum install docker"
    exit 1
fi

echo "✅ Docker found"

# Check if Docker Compose is available
COMPOSE_AVAILABLE=false
if docker compose version &> /dev/null; then
    echo "✅ Docker Compose (plugin) found"
    COMPOSE_CMD="docker compose"
    COMPOSE_AVAILABLE=true
elif command -v docker-compose &> /dev/null; then
    echo "✅ Docker Compose (standalone) found"
    COMPOSE_CMD="docker-compose"
    COMPOSE_AVAILABLE=true
else
    echo "❌ Docker Compose is not available."
    echo "   Please install Docker Compose:"
    echo "   - For Docker Desktop: Compose is included"
    echo "   - For standalone: https://docs.docker.com/compose/install/"
    exit 1
fi

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo "❌ Docker daemon is not running."
    echo "   Please start Docker first:"
    echo "   - On macOS/Windows: Start Docker Desktop"
    echo "   - On Linux: sudo systemctl start docker"
    exit 1
fi

echo "✅ Docker daemon is running"

# Check if we're on a Unix-like system (required for /dev/urandom in container)
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "⚠️  Windows detected - Docker container will handle Unix compatibility"
else
    echo "✅ Unix-like system detected: $OSTYPE"
fi

# Make scripts executable
echo "📝 Making scripts executable..."
chmod +x server.py
chmod +x install.sh
chmod +x start.sh

# Validate docker-compose.yml exists
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ docker-compose.yml not found!"
    echo "   This file is required for Docker Compose deployment."
    exit 1
fi

echo "✅ docker-compose.yml found"

# Test docker-compose configuration
echo "📝 Validating Docker Compose configuration..."
if ! $COMPOSE_CMD config &> /dev/null; then
    echo "❌ Invalid docker-compose.yml configuration"
    echo "   Please check the docker-compose.yml file for syntax errors"
    exit 1
fi

echo "✅ Docker Compose configuration is valid"

# Display installation summary
echo ""
echo "=========================================="
echo "✅ Installation Complete!"
echo "=========================================="
echo ""
echo "Deployment method:"
echo "  🐳 Docker Compose:      ./start.sh"
echo ""
echo "Server will listen on:"
echo "  - Port 80 (HTTP)"
echo "  - Port 443 (HTTPS)"
echo ""
echo "Test connections with:"
echo "  telnet localhost 80"
echo "  nc localhost 80"
echo ""
echo "Docker Compose features:"
echo "  ✅ Automatic container restart"
echo "  ✅ Health checks every 30 seconds"
echo "  ✅ Isolated network environment"
echo "  ✅ No root privileges required on host"
echo ""
echo "Management commands:"
echo "  Start:    ./start.sh"
echo "  Stop:     $COMPOSE_CMD down"
echo "  Logs:     $COMPOSE_CMD logs -f"
echo "  Status:   $COMPOSE_CMD ps"
echo ""
echo "📊 Metrics will be displayed every 60 seconds"
echo "📋 Press Ctrl+C to stop and view final metrics"