#!/usr/bin/env python3

import socket
import sys
from datetime import datetime

def scan_port(target, port):
    """
    Scan a single port on the target host
    Returns True if port is open, False otherwise
    """
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set timeout to 1 second
        sock.settimeout(1)

        # Try to connect to the target and port
        result = sock.connect_ex((target, port))

        # Close the socket
        sock.close()

        # If result is 0, connection was successful (port is open)
        return result == 0

    except socket.gaierror:
        # Could not resolve hostname
        return False
    except Exception:
        # Other errors
        return False

def main():
    # Check if target is provided
    if len(sys.argv) != 2:
        print("Usage: python basic_port_scanner.py <target>")
        print("Example: python basic_port_scanner.py 192.168.1.1")
        sys.exit()

    target = sys.argv[1]

    # Print banner
    print("-" * 50)
    print(f"Starting port scan on: {target}")
    print(f"Time started: {datetime.now()}")
    print("-" * 50)

    # Resolve hostname to IP
    try:
        target_ip = socket.gethostbyname(target)
        print(f"Scanning {target} ({target_ip})")
    except socket.gaierror:
        print(f"Could not resolve hostname: {target}")
        sys.exit()

    print("\nScanning ports 1-1024...")
    print("Open ports:")

    open_ports = []

    # Scan ports 1-1024
    try:
        for port in range(1, 1025):
            if scan_port(target, port):
                print(f"Port {port}: Open")
                open_ports.append(port)

            # Print progress every 100 ports
            if port % 100 == 0:
                print(f"Progress: {port}/1024 ports scanned")

    except KeyboardInterrupt:
        print("\nScan interrupted by user")
        sys.exit()

    # Print summary
    print("\n" + "-" * 50)
    print("SCAN COMPLETE")
    print("-" * 50)
    print(f"Total open ports found: {len(open_ports)}")

    if open_ports:
        print("Open ports:", ", ".join(map(str, open_ports)))
    else:
        print("No open ports found in range 1-1024")

    print(f"Scan finished at: {datetime.now()}")

if __name__ == "__main__":
    main()
