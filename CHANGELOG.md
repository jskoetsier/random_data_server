# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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