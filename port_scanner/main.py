#!/usr/bin/env python3
"""
Port Scanner - Starter Template for Students
Assignment 2: Network Security

This is a STARTER TEMPLATE to help you get started.
You should expand and improve upon this basic implementation.

TODO for students:
1. Implement multi-threading for faster scans
2. Add banner grabbing to detect services
3. Add support for CIDR notation (e.g., 192.168.1.0/24)
4. Add different scan types (SYN scan, UDP scan, etc.)
5. Add output formatting (JSON, CSV, etc.)
6. Implement timeout and error handling
7. Add progress indicators
8. Add service fingerprinting
"""

import socket
import sys
import queue
import threading
import argparse



def scan_port(target, port, timeout=0.5):
    """
    Scan a single port on the target host

    Args:
        target (str): IP address or hostname to scan
        port (int): Port number to scan
        timeout (float): Connection timeout in seconds

    Returns:
        bool: True if port is open, False otherwise
    """
    try:
        # TODO: Create a socket
        # Af_INET -> IPv4
        # SOCK_STREAM -> TCP
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # TODO: Set timeout
        sk.settimeout(timeout)
        # TODO: Try to connect to target:port
        res = sk.connect((target, port))
        # TODO: Close the socket
        # TODO: Return True if connection successful
        return True
        #pass   Remove this and implement

    except (socket.timeout, ConnectionRefusedError, OSError):
        return False
    finally:
        sk.close()

def threadedScan(target, qPorts,open_ports, timeout):
        while True:
            try:
                p = qPorts.get_nowait()
            except queue.Empty:
                break

            try:
                #print(f"Scanning port {p}-^-^")
                if scan_port(target, p, timeout):
                        open_ports.append(p)
                        print(f"Port {p} opened")

            finally:
                qPorts.task_done()


def scan_range(target, start_port, end_port , numThreads = 300, timeout = 0.5 ):
    """
    Scan a range of ports on the target host

    Args:
        target (str): IP address or hostname to scan
        start_port (int): Starting port number
        end_port (int): Ending port number

    Returns:
        list: List of open ports
    """
    open_ports = []
    print(f"[*] Scanning {target} from port {start_port} to {end_port}")
    print(f"[*] This may take a while...")

    # TODO: Implement the scanning logica
    # Hint: Loop through port range and call scan_port() !done
    # Hint: Consider using threading for better performance !done
    #     # TODO: Scan this port
    #     # TODO: If open, add to open_ports list
    #     # TODO: Print progress (optional)
    qPorts = queue.Queue()
    for port in range(start_port, end_port + 1):
        qPorts.put(port)
    threadList = []
    for i in range(numThreads):
            thread = threading.Thread(target=threadedScan, args=(target, qPorts,open_ports, timeout))
            thread.start()
            threadList.append(thread)
    qPorts.join()
    for thread in threadList:
        thread.join()


    return open_ports


def main():
    """Main function"""
    # TODO: Parse command-line arguments
    # TODO: Validate inputs
    # TODO: Call scan_range()
    # TODO: Display results

    
    #accept iphostname and port range
    argumentParsers = argparse.ArgumentParser(description="Basic Port Scanner", 
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    argumentParsers.add_argument("-target", help="Target IP for scan", required=True)
    argumentParsers.add_argument("-ports", nargs=2, type=int, default=[1, 1024], help="Port range (start end)", metavar=('START', 'END'))
    args = argumentParsers.parse_args()
    target = args.target
    start_port = args.ports[0]
    end_port = args.ports[1]

    print(f"[*] Starting port scan on {target}")

    open_ports = scan_range(target, start_port, end_port)

    print(f"\n[+] Scan complete!")
    print(f"[+] Found {len(open_ports)} open ports:")
    for port in open_ports:
        print(f"    Port {port}: open")


if __name__ == "__main__":
    main()