# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.0] - HTTP/HTTPS Headers Support

### Added
- Official HTTP response headers for port 80 connections
- HTTPS-style response headers for port 443 connections with security headers
- HTTP chunked transfer encoding for proper streaming protocol compliance
- Server identification header (RandomDataServer/1.3.0)
- Cache control headers to prevent caching of random data streams
- Security headers for HTTPS connections (HSTS, X-Content-Type-Options, X-Frame-Options)

### Enhanced
- More realistic HTTP/HTTPS protocol simulation for testing scenarios
- Proper chunked encoding implementation for continuous data streaming
- Enhanced logging with header transmission notifications
- Better compatibility with HTTP clients and testing tools

### Changed
- Data transmission now follows HTTP chunked encoding format
- Headers are sent before random data stream begins
- Connection handling now includes proper HTTP protocol flow

## [1.2.0] - Docker Compose Migration

### Changed
- **BREAKING**: Replaced native Python startup with Docker Compose deployment
- Updated startup script (start.sh) to use Docker Compose instead of direct Python execution
- Modified installation script to validate Docker and Docker Compose instead of Python
- Completely rewritten README.md to focus on Docker Compose deployment

### Added
- docker-compose.yml with health checks and auto-restart functionality
- Isolated bridge network for container communication
- Automatic container restart policy (unless-stopped)
- Health check monitoring every 30 seconds
- PYTHONUNBUFFERED environment variable for real-time logging

### Removed
- Native Python startup option (now Docker Compose only)
- Root privilege requirements on host system
- Python version validation in installation script
- Direct Docker run commands in favor of Docker Compose

### Enhanced
- No root privileges required on host (handled by Docker)
- Better container lifecycle management
- Improved deployment reliability with health checks
- Simplified management with docker-compose commands

## [1.1.0] - Enhanced Features and Documentation

### Added
- MIT License for open-source distribution
- Comprehensive installation script (install.sh) with environment validation
- Startup script (start.sh) with automatic privilege handling
- Docker startup script (start-docker.sh) for containerized deployment
- Metrics collection system for connection tracking and bandwidth monitoring
- Comprehensive README documentation with usage examples
- CHANGELOG for tracking project changes
- VERSION file for semantic versioning

### Changed
- Enhanced logging with metrics information and periodic reporting
- Improved error handling and connection management
- All scripts made executable automatically
- Added graceful shutdown with final metrics summary

### Enhanced
- Server now displays metrics every 60 seconds
- Real-time connection tracking and bandwidth monitoring
- Automatic Docker detection and setup in installation script

## [1.0.0] - Initial Release

### Added
- TCP server listening on ports 80 and 443
- Multi-threaded client connection handling
- Continuous random data streaming from /dev/urandom
- Docker containerization support
- Graceful shutdown with signal handling
- Basic error handling for network exceptions
- Socket reuse configuration for better resource management

### Features
- 8KB buffer size for optimal performance
- Support for multiple concurrent connections
- Cross-platform compatibility (Unix/Linux systems)
- Clean connection termination handling