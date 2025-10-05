import socket
import sys
import threading
from datetime import datetime
import argparse
import time

class PortScanner:
    def __init__(self, target, start_port=1, end_port=1024, timeout=1, threads=100):
        self.target = target
        self.start_port = start_port
        self.end_port = end_port
        self.timeout = timeout
        self.threads = threads
        self.open_ports = []
        self.lock = threading.Lock()

    def scan_port(self, port):
        """Scan a single port"""
        try:
            # Create socket object
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)

            # Attempt to connect
            result = sock.connect_ex((self.target, port))

            if result == 0:
                # Port is open - try banner grabbing
                banner = self.grab_banner(sock, port)

                with self.lock:
                    self.open_ports.append({'port': port, 'banner': banner})
                    print(f"[+] Port {port}: Open {banner}")

            sock.close()

        except socket.gaierror:
            # Hostname could not be resolved
            pass
        except Exception as e:
            # Other socket errors
            pass

    def grab_banner(self, sock, port):
        """Attempt to grab service banner"""
        try:
            # Send HTTP request for web ports
            if port in [80, 443, 8080, 8443]:
                sock.send(b"GET / HTTP/1.1\r\nHost: " + self.target.encode() + b"\r\n\r\n")
            # Send generic probe for other ports
            else:
                sock.send(b"\r\n")

            # Receive response
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            return f"({banner[:50]}...)" if len(banner) > 50 else f"({banner})"

        except:
            return ""

    def run_scan(self):
        """Run the port scan with threading"""
        print("=" * 60)
        print(f"Starting port scan on: {self.target}")
        print(f"Port range: {self.start_port}-{self.end_port}")
        print(f"Started at: {datetime.now()}")
        print("=" * 60)

        # Resolve hostname to IP
        try:
            target_ip = socket.gethostbyname(self.target)
            print(f"Scanning {self.target} ({target_ip})")
        except socket.gaierror:
            print(f"Could not resolve hostname: {self.target}")
            return

        start_time = time.time()

        # Create and start threads
        threads = []
        for port in range(self.start_port, self.end_port + 1):
            thread = threading.Thread(target=self.scan_port, args=(port,))
            threads.append(thread)
            thread.start()

            # Limit concurrent threads
            if len(threads) >= self.threads:
                for t in threads:
                    t.join()
                threads = []

        # Wait for remaining threads
        for thread in threads:
            thread.join()

        end_time = time.time()

        # Display results
        print("\n" + "=" * 60)
        print("SCAN RESULTS")
        print("=" * 60)

        if self.open_ports:
            print(f"Found {len(self.open_ports)} open ports:")
            for port_info in sorted(self.open_ports, key=lambda x: x['port']):
                service = self.get_service_name(port_info['port'])
                print(f"Port {port_info['port']}: {service} {port_info['banner']}")
        else:
            print("No open ports found in the specified range.")

        print(f"\nScan completed in {end_time - start_time:.2f} seconds")

    def get_service_name(self, port):
        """Get common service name for port"""
        services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 993: "IMAPS",
            995: "POP3S", 3389: "RDP", 5432: "PostgreSQL", 3306: "MySQL"
        }
        return services.get(port, "Unknown")

    def save_results(self, filename):
        """Save scan results to file"""
        try:
            with open(filename, 'w') as f:
                f.write(f"Port Scan Results for {self.target}\n")
                f.write(f"Scan Date: {datetime.now()}\n")
                f.write(f"Port Range: {self.start_port}-{self.end_port}\n")
                f.write("=" * 50 + "\n")

                if self.open_ports:
                    for port_info in sorted(self.open_ports, key=lambda x: x['port']):
                        service = self.get_service_name(port_info['port'])
                        f.write(f"Port {port_info['port']}: {service} {port_info['banner']}\n")
                else:
                    f.write("No open ports found.\n")

            print(f"Results saved to {filename}")
        except Exception as e:
            print(f"Error saving results: {e}")

def main():
    parser = argparse.ArgumentParser(description="Simple Port Scanner")
    parser.add_argument("target", help="Target hostname or IP address")
    parser.add_argument("-p", "--ports", default="1-1024", 
                       help="Port range (e.g., 1-1000 or 80,443,22)")
    parser.add_argument("-t", "--timeout", type=float, default=1.0,
                       help="Connection timeout in seconds (default: 1.0)")
    parser.add_argument("--threads", type=int, default=100,
                       help="Number of threads (default: 100)")
    parser.add_argument("-o", "--output", help="Save results to file")

    args = parser.parse_args()

    # Parse port range
    if '-' in args.ports:
        start_port, end_port = map(int, args.ports.split('-'))
    elif ',' in args.ports:
        # Handle comma-separated ports
        ports = list(map(int, args.ports.split(',')))
        start_port, end_port = min(ports), max(ports)
    else:
        start_port = end_port = int(args.ports)

    # Create and run scanner
    scanner = PortScanner(args.target, start_port, end_port, args.timeout, args.threads)

    try:
        scanner.run_scan()

        # Save results if requested
        if args.output:
            scanner.save_results(args.output)

    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user")
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    main()
