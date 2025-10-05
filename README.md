# Port Scanner Project

## Overview
This project is a Python-based network port scanner designed as a beginner-friendly cybersecurity tool. It helps identify open ports on a target host by attempting TCP connections across a range of ports. The project aligns with ethical hacking concepts, particularly footprinting and reconnaissance techniques from the CEH v13 syllabus.

## Features
- Simple and easy-to-understand Python code
- Basic single-threaded port scanner (`basic_port_scanner.py`)
- Advanced multi-threaded port scanner with banner grabbing (`port_scanner.py`)
- Command-line arguments support for target, port range, timeout, and output file
- Results can be saved to a file for further analysis
- Suitable for learning networking fundamentals, socket programming, and reconnaissance

## Project Structure

```
port-scanner-project/
│
├── basic_port_scanner.py         # Beginner version, simple single-thread scanner
├── port_scanner.py               # Advanced version with threading, banner grabbing, CLI
├── README.md                    # This documentation file
└── results/                     # Folder to save scan output files (create if needed)
```

## Prerequisites
- Python 3.x installed on your system
- Basic knowledge of running Python scripts from the command line
- Permission to scan the target hosts

## Usage

### Basic Scanner
```bash
python basic_port_scanner.py <target>
```
Example:
```bash
python basic_port_scanner.py 127.0.0.1
```

### Advanced Scanner
```bash
python port_scanner.py <target> [-p port_range] [-t timeout] [--threads N] [-o output_file]
```

Options:
- `-p`, `--ports`: Port range (e.g., 1-1024, or single port 80)
- `-t`, `--timeout`: Connection timeout in seconds (default: 1.0)
- `--threads`: Number of concurrent threads (default: 100)
- `-o`, `--output`: Save scan results to a specified filename

Example:
```bash
python port_scanner.py example.com -p 1-100 -t 0.5 -o results/scan1.txt
```

## Ethical Considerations
- Only scan systems you own or have explicit permission to test.
- Unauthorized port scanning can be illegal and unethical.
- Use this tool responsibly for educational and defensive security purposes only.

## Future Enhancements
- Service version and OS detection
- Stealth scanning techniques
- Export results in additional formats like JSON or CSV
- Web interface for easier usage

## Resources
- Python socket programming: https://realpython.com/python-sockets/
- Ethical Hacking CEH v13 Footprinting and Reconnaissance modules
- Cybersecurity community and forums for support and collaboration

## License
This project is released under the MIT License.

---

Created by @SachinRajput-SSR
