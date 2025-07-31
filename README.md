# Random Data Server

A lightweight TCP server that streams continuous random data to connected clients on ports 80 and 443.

## Overview

This server is designed for network testing, bandwidth testing, and load testing scenarios. When clients connect, the server immediately begins streaming random data from `/dev/urandom` until the client disconnects.

## Features

- **Multi-port Support**: Listens on both port 80 (HTTP) and 443 (HTTPS)
- **Concurrent Connections**: Multi-threaded architecture supports multiple simultaneous clients
- **Continuous Streaming**: Non-stop random data transmission until client disconnect
- **Metrics Collection**: Built-in connection and bandwidth metrics
- **Docker Support**: Containerized deployment ready
- **Graceful Shutdown**: Proper signal handling for clean termination

## Quick Start

### Local Development

```bash
# Run directly with Python
python3 server.py
```

**Note**: Binding to ports 80 and 443 requires root privileges:
```bash
sudo python3 server.py
```

### Docker Deployment

```bash
# Build the image
docker build -t random-data-server .

# Run the container
docker run -p 80:80 -p 443:443 random-data-server
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

## Requirements

- Python 3.7+
- Unix/Linux system (uses `/dev/urandom`)
- Root privileges for ports 80/443

## Security Considerations

This server is intended for testing purposes. For production use, consider:
- Implementing authentication
- Adding rate limiting
- Using non-privileged ports
- Restricting bind addresses

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