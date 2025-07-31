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