#!/bin/bash

# Random Data Server Installation Script
# This script sets up the Random Data Server environment

set -e  # Exit on any error

echo "=========================================="
echo "Random Data Server Installation Script"
echo "=========================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+ first."
    echo "   On macOS: brew install python3"
    echo "   On Ubuntu/Debian: sudo apt-get install python3"
    echo "   On CentOS/RHEL: sudo yum install python3"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.7"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python $PYTHON_VERSION found, but Python $REQUIRED_VERSION+ is required."
    exit 1
fi

echo "✅ Python $PYTHON_VERSION found"

# Check if we're on a Unix-like system (required for /dev/urandom)
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "❌ This server requires a Unix-like system (Linux, macOS, etc.)"
    echo "   Windows is not supported due to /dev/urandom dependency"
    exit 1
fi

echo "✅ Unix-like system detected: $OSTYPE"

# Check if Docker is installed (optional)
if command -v docker &> /dev/null; then
    echo "✅ Docker found - containerized deployment available"
    DOCKER_AVAILABLE=true
else
    echo "⚠️  Docker not found - only local deployment available"
    echo "   Install Docker for containerized deployment: https://docs.docker.com/get-docker/"
    DOCKER_AVAILABLE=false
fi

# Make scripts executable
echo "📝 Making scripts executable..."
chmod +x server.py
chmod +x install.sh

# Create startup script if it doesn't exist
if [ ! -f "start.sh" ]; then
    echo "📝 Creating startup script..."
    cat > start.sh << 'EOF'
#!/bin/bash

# Random Data Server Startup Script

set -e

echo "Starting Random Data Server..."
echo "Note: This server requires root privileges to bind to ports 80 and 443"
echo "Press Ctrl+C to stop the server"
echo ""

# Check if running as root for privileged ports
if [ "$EUID" -ne 0 ]; then
    echo "⚠️  Not running as root. Attempting to start with sudo..."
    echo "You may be prompted for your password."
    exec sudo python3 server.py
else
    exec python3 server.py
fi
EOF
    chmod +x start.sh
fi

# Create Docker startup script if Docker is available
if [ "$DOCKER_AVAILABLE" = true ]; then
    if [ ! -f "start-docker.sh" ]; then
        echo "📝 Creating Docker startup script..."
        cat > start-docker.sh << 'EOF'
#!/bin/bash

# Random Data Server Docker Startup Script

set -e

IMAGE_NAME="random-data-server"
CONTAINER_NAME="random-data-server"

echo "Starting Random Data Server with Docker..."

# Stop and remove existing container if it exists
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "Stopping existing container..."
    docker stop $CONTAINER_NAME >/dev/null 2>&1 || true
    docker rm $CONTAINER_NAME >/dev/null 2>&1 || true
fi

# Build the image if it doesn't exist
if [ ! "$(docker images -q $IMAGE_NAME)" ]; then
    echo "Building Docker image..."
    docker build -t $IMAGE_NAME .
fi

# Run the container
echo "Starting container on ports 80 and 443..."
echo "Press Ctrl+C to stop the server"
docker run --rm -it --name $CONTAINER_NAME -p 80:80 -p 443:443 $IMAGE_NAME
EOF
        chmod +x start-docker.sh
    fi
fi

# Display installation summary
echo ""
echo "=========================================="
echo "✅ Installation Complete!"
echo "=========================================="
echo ""
echo "Available startup options:"
echo "  1. Local deployment:     ./start.sh"
if [ "$DOCKER_AVAILABLE" = true ]; then
echo "  2. Docker deployment:    ./start-docker.sh"
fi
echo ""
echo "Server will listen on:"
echo "  - Port 80 (HTTP)"
echo "  - Port 443 (HTTPS)"
echo ""
echo "Test connections with:"
echo "  telnet localhost 80"
echo "  nc localhost 80"
echo ""
echo "⚠️  Note: Ports 80 and 443 require root privileges"
echo "    The startup script will prompt for sudo if needed"
echo ""
echo "📊 Metrics will be displayed every 60 seconds"
echo "📋 Press Ctrl+C to stop and view final metrics"