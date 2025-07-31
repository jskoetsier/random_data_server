# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Metrics collection system for connection tracking and bandwidth monitoring
- VERSION file for semantic versioning
- Comprehensive README documentation
- CHANGELOG for tracking project changes

### Changed
- Enhanced logging with metrics information
- Improved error handling and connection management

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