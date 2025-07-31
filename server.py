#!/usr/bin/env python3
"""
TCP server that listens on ports 80 and 443 and sends random data to clients.
When a client connects, the server streams non-stop random data from /dev/urandom
until the client disconnects.
"""

import socket
import threading
import os
import sys
import signal

def handle_client(client_socket, client_address, port):
    """Handle a client connection by sending random data until disconnection."""
    print(f"[+] Connection established from {client_address[0]}:{client_address[1]} on port {port}")
    
    try:
        # Open /dev/urandom for reading binary data
        with open("/dev/urandom", "rb") as random_source:
            # Create a buffer for reading random data
            buffer_size = 8192  # 8KB buffer
            
            # Keep sending random data until the connection is closed
            while True:
                # Read random data
                random_data = random_source.read(buffer_size)
                
                # Send the data to the client
                bytes_sent = client_socket.send(random_data)
                
                # If no bytes were sent, the connection is likely closed
                if bytes_sent == 0:
                    break
                    
    except BrokenPipeError:
        # Client disconnected
        pass
    except ConnectionResetError:
        # Connection reset by peer
        pass
    except Exception as e:
        print(f"[-] Error handling client: {e}")
    finally:
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

def main():
    """Main function to start servers on ports 80 and 443."""
    print("[+] Starting random data servers on ports 80 and 443...")
    
    # Start servers in separate threads
    server_80_thread = threading.Thread(target=start_server, args=(80,))
    server_443_thread = threading.Thread(target=start_server, args=(443,))
    
    server_80_thread.daemon = True
    server_443_thread.daemon = True
    
    server_80_thread.start()
    server_443_thread.start()
    
    # Handle keyboard interrupt gracefully
    try:
        # Keep the main thread alive
        while True:
            signal.pause()
    except KeyboardInterrupt:
        print("\n[+] Shutting down servers...")
        sys.exit(0)

if __name__ == "__main__":
    main()
