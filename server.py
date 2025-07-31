#!/usr/bin/env python3
"""
TCP server that listens on ports 80 and 443 and sends random data to clients.
When a client connects, the server streams non-stop random data from /dev/urandom
until the client disconnects.
"""

import socket
import threading
import sys
import signal
import time
from collections import defaultdict
from threading import Lock

class MetricsCollector:
    """Collects and manages server metrics."""
    
    def __init__(self):
        self.lock = Lock()
        self.total_connections = defaultdict(int)  # per port
        self.active_connections = defaultdict(int)  # per port
        self.bytes_transmitted = defaultdict(int)  # per port
        self.connection_durations = defaultdict(list)  # per port
        self.start_time = time.time()
    
    def connection_started(self, port, _client_address):
        """Record a new connection."""
        with self.lock:
            self.total_connections[port] += 1
            self.active_connections[port] += 1
        print(f"[METRICS] Port {port}: Total connections: {self.total_connections[port]}, Active: {self.active_connections[port]}")
    
    def connection_ended(self, port, _client_address, duration, bytes_sent):
        """Record a connection ending."""
        with self.lock:
            self.active_connections[port] -= 1
            self.bytes_transmitted[port] += bytes_sent
            self.connection_durations[port].append(duration)
        
        print(f"[METRICS] Port {port}: Connection ended - Duration: {duration:.2f}s, Bytes sent: {bytes_sent:,}")
        print(f"[METRICS] Port {port}: Active connections: {self.active_connections[port]}, Total bytes: {self.bytes_transmitted[port]:,}")
    
    def bytes_sent(self, port, bytes_count):
        """Record bytes sent (for real-time tracking)."""
        with self.lock:
            self.bytes_transmitted[port] += bytes_count
    
    def get_summary(self):
        """Get a summary of all metrics."""
        with self.lock:
            uptime = time.time() - self.start_time
            summary = {
                'uptime_seconds': uptime,
                'ports': {}
            }
            
            for port in set(list(self.total_connections.keys()) + list(self.active_connections.keys())):
                avg_duration = 0
                if self.connection_durations[port]:
                    avg_duration = sum(self.connection_durations[port]) / len(self.connection_durations[port])
                
                summary['ports'][port] = {
                    'total_connections': self.total_connections[port],
                    'active_connections': self.active_connections[port],
                    'bytes_transmitted': self.bytes_transmitted[port],
                    'average_connection_duration': avg_duration,
                    'completed_connections': len(self.connection_durations[port])
                }
            
            return summary
    
    def print_summary(self):
        """Print a formatted summary of metrics."""
        summary = self.get_summary()
        print("\n" + "="*50)
        print("SERVER METRICS SUMMARY")
        print("="*50)
        print(f"Uptime: {summary['uptime_seconds']:.2f} seconds")
        
        for port, metrics in summary['ports'].items():
            print(f"\nPort {port}:")
            print(f"  Total Connections: {metrics['total_connections']}")
            print(f"  Active Connections: {metrics['active_connections']}")
            print(f"  Completed Connections: {metrics['completed_connections']}")
            print(f"  Bytes Transmitted: {metrics['bytes_transmitted']:,}")
            print(f"  Average Connection Duration: {metrics['average_connection_duration']:.2f}s")
        print("="*50 + "\n")

# Global metrics collector
metrics = MetricsCollector()

def handle_client(client_socket, client_address, port):
    """Handle a client connection by sending HTTP/HTTPS headers then random data until disconnection."""
    start_time = time.time()
    total_bytes_sent = 0
    
    print(f"[+] Connection established from {client_address[0]}:{client_address[1]} on port {port}")
    metrics.connection_started(port, client_address)
    
    try:
        # Set socket timeout for reading HTTP request
        client_socket.settimeout(5.0)  # 5 second timeout
        
        # Try to read the HTTP request from the client
        request_data = b""
        try:
            while b"\r\n\r\n" not in request_data:
                chunk = client_socket.recv(1024)
                if not chunk:
                    break
                request_data += chunk
                # Prevent infinite reading
                if len(request_data) > 8192:
                    break
            
            # Parse the request line to get method, path, and HTTP version
            request_lines = request_data.decode('utf-8', errors='ignore').split('\r\n')
            if request_lines and request_lines[0]:
                request_line = request_lines[0]
                print(f"[+] Received request: {request_line} from {client_address[0]}:{client_address[1]}")
            else:
                print(f"[+] No HTTP request received from {client_address[0]}:{client_address[1]}, proceeding with data stream")
        except socket.timeout:
            print(f"[+] Request timeout from {client_address[0]}:{client_address[1]}, proceeding with data stream")
        except Exception as e:
            print(f"[+] Error reading request from {client_address[0]}:{client_address[1]}: {e}, proceeding with data stream")
        
        # Remove timeout for data streaming
        client_socket.settimeout(None)
        
        # Send appropriate HTTP/HTTPS headers based on port
        if port == 80:
            # HTTP headers
            http_response = (
                "HTTP/1.1 200 OK\r\n"
                "Server: RandomDataServer/1.3.1\r\n"
                "Content-Type: application/octet-stream\r\n"
                "Transfer-Encoding: chunked\r\n"
                "Cache-Control: no-cache, no-store, must-revalidate\r\n"
                "Pragma: no-cache\r\n"
                "Expires: 0\r\n"
                "Connection: keep-alive\r\n"
                "\r\n"
            )
            print(f"[+] Sending HTTP headers to {client_address[0]}:{client_address[1]}")
        elif port == 443:
            # HTTPS-style headers (note: this is not real HTTPS encryption, just HTTP over port 443)
            http_response = (
                "HTTP/1.1 200 OK\r\n"
                "Server: RandomDataServer/1.3.1\r\n"
                "Content-Type: application/octet-stream\r\n"
                "Transfer-Encoding: chunked\r\n"
                "Cache-Control: no-cache, no-store, must-revalidate\r\n"
                "Pragma: no-cache\r\n"
                "Expires: 0\r\n"
                "Connection: keep-alive\r\n"
                "Strict-Transport-Security: max-age=31536000; includeSubDomains\r\n"
                "X-Content-Type-Options: nosniff\r\n"
                "X-Frame-Options: DENY\r\n"
                "\r\n"
            )
            print(f"[+] Sending HTTPS-style headers to {client_address[0]}:{client_address[1]}")
        else:
            # Default HTTP headers for any other port
            http_response = (
                "HTTP/1.1 200 OK\r\n"
                "Server: RandomDataServer/1.3.1\r\n"
                "Content-Type: application/octet-stream\r\n"
                "Transfer-Encoding: chunked\r\n"
                "Cache-Control: no-cache, no-store, must-revalidate\r\n"
                "Pragma: no-cache\r\n"
                "Expires: 0\r\n"
                "Connection: keep-alive\r\n"
                "\r\n"
            )
            print(f"[+] Sending HTTP headers to {client_address[0]}:{client_address[1]} on port {port}")
        
        # Send the HTTP headers
        header_bytes = client_socket.send(http_response.encode('utf-8'))
        total_bytes_sent += header_bytes
        
        # Open /dev/urandom for reading binary data
        with open("/dev/urandom", "rb") as random_source:
            # Create a buffer for reading random data
            buffer_size = 8192  # 8KB buffer
            
            print(f"[+] Starting random data stream to {client_address[0]}:{client_address[1]}")
            
            # Keep sending random data until the connection is closed
            while True:
                # Read random data
                random_data = random_source.read(buffer_size)
                
                # For HTTP chunked encoding, we need to send chunk size in hex followed by \r\n
                chunk_size = hex(len(random_data))[2:].encode('utf-8')  # Remove '0x' prefix
                chunk_header = chunk_size + b'\r\n'
                chunk_footer = b'\r\n'
                
                # Send chunk header
                bytes_sent = client_socket.send(chunk_header)
                if bytes_sent == 0:
                    break
                total_bytes_sent += bytes_sent
                
                # Send the actual data
                bytes_sent = client_socket.send(random_data)
                if bytes_sent == 0:
                    break
                total_bytes_sent += bytes_sent
                
                # Send chunk footer
                bytes_sent = client_socket.send(chunk_footer)
                if bytes_sent == 0:
                    break
                total_bytes_sent += bytes_sent
                    
    except BrokenPipeError:
        # Client disconnected
        pass
    except ConnectionResetError:
        # Connection reset by peer
        pass
    except Exception as e:
        print(f"[-] Error handling client: {e}")
    finally:
        # Calculate connection duration
        duration = time.time() - start_time
        
        # Record metrics
        metrics.connection_ended(port, client_address, duration, total_bytes_sent)
        
        # Close the client socket
        client_socket.close()
        print(f"[+] Connection closed from {client_address[0]}:{client_address[1]}")

def start_server(port):
    """Start a TCP server on the specified port."""
    try:
        # Create a TCP socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Allow reuse of the address
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind the socket to all interfaces on the specified port
        server.bind(('0.0.0.0', port))
        
        # Listen for incoming connections (queue up to 5 connections)
        server.listen(5)
        
        print(f"[+] Server listening on port {port}")
        
        while True:
            # Accept a client connection
            client_socket, client_address = server.accept()
            
            # Create a new thread to handle the client
            client_handler = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address, port)
            )
            client_handler.daemon = True
            client_handler.start()
            
    except Exception as e:
        print(f"[-] Error starting server on port {port}: {e}")
        return None
    
    return server

def print_periodic_metrics():
    """Print metrics summary every 60 seconds."""
    while True:
        time.sleep(60)  # Wait 60 seconds
        metrics.print_summary()

def signal_handler(_signum, _frame):
    """Handle shutdown signals and print final metrics."""
    print("\n[+] Shutting down servers...")
    print("[+] Final metrics summary:")
    metrics.print_summary()
    sys.exit(0)

def main():
    """Main function to start servers on ports 80 and 443."""
    print("[+] Starting random data servers on ports 80 and 443...")
    print("[+] Metrics will be displayed every 60 seconds")
    print("[+] Press Ctrl+C to stop the server and view final metrics")
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start servers in separate threads
    server_80_thread = threading.Thread(target=start_server, args=(80,))
    server_443_thread = threading.Thread(target=start_server, args=(443,))
    
    server_80_thread.daemon = True
    server_443_thread.daemon = True
    
    server_80_thread.start()
    server_443_thread.start()
    
    # Start periodic metrics reporting
    metrics_thread = threading.Thread(target=print_periodic_metrics)
    metrics_thread.daemon = True
    metrics_thread.start()
    
    # Handle keyboard interrupt gracefully
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    main()
