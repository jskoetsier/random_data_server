# Random Data Server

A lightweight TCP server that streams continuous random data to connected clients on ports 80 and 443.

## Overview

This server is designed for network testing, bandwidth testing, and load testing scenarios. When clients connect, the server immediately begins streaming random data from `/dev/urandom` until the client disconnects.

## Features

- **Multi-port Support**: Listens on both port 80 (HTTP) and 443 (HTTPS)
- **Concurrent Connections**: Multi-threaded architecture supports multiple simultaneous clients
- **Continuous Streaming**: Non-stop random data transmission until client disconnect
- **Metrics Collection**: Built-in connection and bandwidth metrics
- **Docker Compose Support**: Containerized deployment with health checks and auto-restart
- **Graceful Shutdown**: Proper signal handling for clean termination

## Quick Start

### Docker Compose Deployment (Recommended)

```bash
# Install and validate environment
./install.sh

# Start the server
./start.sh
```

### Manual Docker Compose

```bash
# Start with Docker Compose
docker compose up --build

# Or with legacy docker-compose
docker-compose up --build
```

### Management Commands

```bash
# Stop the server
docker compose down

# View logs
docker compose logs -f

# Check status
docker compose ps

# Restart service
docker compose restart
```

## Usage

Once the server is running, clients can connect via TCP to either port:

```bash
# Connect to port 80
telnet localhost 80

# Connect to port 443
telnet localhost 443

# Test with netcat
nc localhost 80
```

The server will immediately begin streaming random data. Disconnect the client to stop the stream.

## Metrics

The server collects the following metrics:
- Total connections per port
- Active connections
- Bytes transmitted per connection
- Connection duration

Metrics are logged to the console and can be accessed programmatically.

## Configuration

Default configuration:
- **Ports**: 80, 443
- **Buffer Size**: 8KB
- **Max Connections**: 5 queued per port
- **Bind Address**: 0.0.0.0 (all interfaces)
- **Health Check**: Every 30 seconds
- **Restart Policy**: Unless stopped

## Requirements

- Docker and Docker Compose
- Unix/Linux/macOS system (Windows supported via Docker)
- No root privileges required (handled by Docker)

## Docker Compose Features

- **Health Checks**: Automatic service health monitoring
- **Auto Restart**: Container restarts on failure
- **Isolated Network**: Dedicated bridge network
- **Environment Variables**: PYTHONUNBUFFERED for real-time logs
- **Graceful Shutdown**: Proper container cleanup

## Security Considerations

This server is intended for testing purposes. For production use, consider:
- Implementing authentication
- Adding rate limiting
- Using non-privileged ports
- Restricting bind addresses
- Network segmentation

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions, please open an issue in the repository.