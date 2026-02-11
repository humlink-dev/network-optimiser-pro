#!/usr/bin/env python3
"""
Network Optimizer Pro - Comprehensive Network Optimization Toolkit
Reduces latency, optimizes routing, and monitors network performance
"""

import os
import sys
import platform
import subprocess
import socket
import time
import psutil
import json
from datetime import datetime
from pathlib import Path

class NetworkOptimizer:
    def __init__(self):
        self.os_type = platform.system()
        self.is_admin = self.check_admin()
        self.config_file = Path.home() / '.network_optimizer_config.json'
        self.load_config()
        
    def check_admin(self):
        """Check if running with admin/root privileges"""
        try:
            if self.os_type == 'Windows':
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                return os.geteuid() == 0
        except:
            return False
    
    def load_config(self):
        """Load saved configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                'dns_servers': ['1.1.1.1', '1.0.0.1'],
                'optimized': False,
                'last_run': None
            }
    
    def save_config(self):
        """Save configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def print_banner(self):
        """Print application banner"""
        print("=" * 60)
        print("   NETWORK OPTIMIZER PRO - Gaming & Latency Optimizer")
        print("=" * 60)
        print(f"OS: {self.os_type} | Admin: {'Yes' if self.is_admin else 'No'}")
        print("=" * 60)
        print()
    
    def test_dns_latency(self, dns_server, timeout=2):
        """Test DNS server response time"""
        try:
            start = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((dns_server, 53))
            sock.close()
            latency = (time.time() - start) * 1000
            return latency
        except:
            return 9999
    
    def find_fastest_dns(self):
        """Find the fastest DNS servers"""
        print("[*] Testing DNS servers for lowest latency...")
        
        dns_servers = {
            'Cloudflare': ['1.1.1.1', '1.0.0.1'],
            'Google': ['8.8.8.8', '8.8.4.4'],
            'Quad9': ['9.9.9.9', '149.112.112.112'],
            'OpenDNS': ['208.67.222.222', '208.67.220.220'],
            'AdGuard': ['94.140.14.14', '94.140.15.15'],
        }
        
        results = {}
        for name, servers in dns_servers.items():
            latency = self.test_dns_latency(servers[0])
            results[name] = {'servers': servers, 'latency': latency}
            print(f"    {name}: {latency:.2f}ms")
        
        fastest = min(results.items(), key=lambda x: x[1]['latency'])
        print(f"\n[+] Fastest DNS: {fastest[0]} ({fastest[1]['latency']:.2f}ms)")
        return fastest[1]['servers']
    
    def set_dns_windows(self, dns_servers):
        """Set DNS servers on Windows"""
        try:
            # Get active network interface
            cmd = 'netsh interface show interface'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            # Find connected interface
            lines = result.stdout.split('\n')
            interface = None
            for line in lines:
                if 'Connected' in line and 'Dedicated' in line:
                    parts = line.split()
                    interface = ' '.join(parts[3:])
                    break
            
            if not interface:
                print("[-] Could not find active network interface")
                return False
            
            print(f"[*] Setting DNS on interface: {interface}")
            
            # Set primary DNS
            cmd1 = f'netsh interface ip set dns name="{interface}" static {dns_servers[0]}'
            subprocess.run(cmd1, shell=True, check=True)
            
            # Set secondary DNS
            cmd2 = f'netsh interface ip add dns name="{interface}" {dns_servers[1]} index=2'
            subprocess.run(cmd2, shell=True, check=True)
            
            print(f"[+] DNS set to {dns_servers[0]} and {dns_servers[1]}")
            return True
        except Exception as e:
            print(f"[-] Error setting DNS: {e}")
            return False
    
    def set_dns_linux(self, dns_servers):
        """Set DNS servers on Linux"""
        try:
            with open('/etc/resolv.conf', 'w') as f:
                for dns in dns_servers:
                    f.write(f'nameserver {dns}\n')
            print(f"[+] DNS set to {dns_servers[0]} and {dns_servers[1]}")
            return True
        except Exception as e:
            print(f"[-] Error setting DNS: {e}")
            return False
    
    def optimize_tcp_windows(self):
        """Optimize TCP/IP settings for Windows"""
        print("\n[*] Optimizing TCP/IP settings...")
        
        commands = [
            # Disable Nagle's algorithm for lower latency
            'netsh int tcp set global autotuninglevel=normal',
            # Enable TCP window scaling
            'netsh int tcp set global timestamps=enabled',
            # Optimize for low latency
            'netsh int tcp set global chimney=enabled',
            # Enable RSS (Receive Side Scaling)
            'netsh int tcp set global rss=enabled',
            # Set congestion provider to CTCP
            'netsh int tcp set global congestionprovider=ctcp',
            # Optimize network throttling
            'netsh int tcp set global nonsackrttresiliency=disabled',
            # Set initial RTO to 3000ms
            'netsh int tcp set global initialRto=3000',
        ]
        
        for cmd in commands:
            try:
                subprocess.run(cmd, shell=True, check=True, capture_output=True)
                print(f"    ✓ {cmd.split('=')[0].split()[-1]}")
            except:
                pass
        
        print("[+] TCP/IP optimization complete")
    
    def optimize_tcp_linux(self):
        """Optimize TCP/IP settings for Linux"""
        print("\n[*] Optimizing TCP/IP settings...")
        
        settings = {
            'net.ipv4.tcp_fastopen': '3',
            'net.ipv4.tcp_low_latency': '1',
            'net.ipv4.tcp_timestamps': '1',
            'net.ipv4.tcp_sack': '1',
            'net.core.netdev_max_backlog': '5000',
            'net.ipv4.tcp_congestion_control': 'bbr',
        }
        
        for key, value in settings.items():
            try:
                subprocess.run(f'sysctl -w {key}={value}', shell=True, check=True, capture_output=True)
                print(f"    ✓ {key}")
            except:
                pass
        
        print("[+] TCP/IP optimization complete")
    
    def flush_dns_cache(self):
        """Flush DNS cache"""
        print("\n[*] Flushing DNS cache...")
        try:
            if self.os_type == 'Windows':
                subprocess.run('ipconfig /flushdns', shell=True, check=True, capture_output=True)
            elif self.os_type == 'Linux':
                subprocess.run('systemd-resolve --flush-caches', shell=True, capture_output=True)
            elif self.os_type == 'Darwin':
                subprocess.run('dscacheutil -flushcache', shell=True, capture_output=True)
            print("[+] DNS cache flushed")
        except Exception as e:
            print(f"[-] Could not flush DNS cache: {e}")
    
    def get_network_stats(self):
        """Get current network statistics"""
        print("\n[*] Current Network Statistics:")
        print("-" * 60)
        
        # Get network interfaces
        interfaces = psutil.net_if_stats()
        for iface, stats in interfaces.items():
            if stats.isup:
                print(f"\nInterface: {iface}")
                print(f"  Speed: {stats.speed} Mbps")
                print(f"  MTU: {stats.mtu}")
        
        # Get network IO
        net_io = psutil.net_io_counters()
        print(f"\nNetwork I/O:")
        print(f"  Bytes Sent: {net_io.bytes_sent / 1024 / 1024:.2f} MB")
        print(f"  Bytes Received: {net_io.bytes_recv / 1024 / 1024:.2f} MB")
        print(f"  Packets Sent: {net_io.packets_sent}")
        print(f"  Packets Received: {net_io.packets_recv}")
        
        # Get connections
        connections = psutil.net_connections(kind='inet')
        print(f"\nActive Connections: {len(connections)}")
    
    def monitor_bandwidth(self, duration=10):
        """Monitor bandwidth usage"""
        print(f"\n[*] Monitoring bandwidth for {duration} seconds...")
        print("-" * 60)
        
        old_value = psutil.net_io_counters()
        time.sleep(1)
        
        for i in range(duration):
            new_value = psutil.net_io_counters()
            
            upload_speed = (new_value.bytes_sent - old_value.bytes_sent) / 1024 / 1024
            download_speed = (new_value.bytes_recv - old_value.bytes_recv) / 1024 / 1024
            
            print(f"[{i+1}/{duration}] ↑ {upload_speed:.2f} MB/s | ↓ {download_speed:.2f} MB/s", end='\r')
            
            old_value = new_value
            time.sleep(1)
        
        print("\n[+] Monitoring complete")
    
    def test_latency(self, host='8.8.8.8'):
        """Test latency to a host"""
        print(f"\n[*] Testing latency to {host}...")
        
        if self.os_type == 'Windows':
            cmd = f'ping -n 10 {host}'
        else:
            cmd = f'ping -c 10 {host}'
        
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            print(result.stdout)
        except Exception as e:
            print(f"[-] Error: {e}")
    
    def show_top_bandwidth_consumers(self):
        """Show processes using most bandwidth"""
        print("\n[*] Top Bandwidth Consumers:")
        print("-" * 60)
        
        connections = psutil.net_connections(kind='inet')
        process_bandwidth = {}
        
        for conn in connections:
            if conn.pid:
                try:
                    proc = psutil.Process(conn.pid)
                    name = proc.name()
                    if name not in process_bandwidth:
                        process_bandwidth[name] = {'count': 0, 'pid': conn.pid}
                    process_bandwidth[name]['count'] += 1
                except:
                    pass
        
        sorted_procs = sorted(process_bandwidth.items(), key=lambda x: x[1]['count'], reverse=True)[:10]
        
        for i, (name, info) in enumerate(sorted_procs, 1):
            print(f"{i}. {name} (PID: {info['pid']}) - {info['count']} connections")
    
    def run_full_optimization(self):
        """Run complete optimization suite"""
        if not self.is_admin:
            print("\n[!] WARNING: Running without admin privileges.")
            print("[!] Some optimizations require admin/root access.")
            input("\nPress Enter to continue anyway...")
        
        print("\n" + "=" * 60)
        print("  STARTING FULL NETWORK OPTIMIZATION")
        print("=" * 60)
        
        # Step 1: Find and set fastest DNS
        fastest_dns = self.find_fastest_dns()
        
        if self.is_admin:
            print("\n[*] Applying DNS settings...")
            if self.os_type == 'Windows':
                self.set_dns_windows(fastest_dns)
            elif self.os_type == 'Linux':
                self.set_dns_linux(fastest_dns)
            
            self.config['dns_servers'] = fastest_dns
        
        # Step 2: Flush DNS cache
        self.flush_dns_cache()
        
        # Step 3: Optimize TCP/IP
        if self.is_admin:
            if self.os_type == 'Windows':
                self.optimize_tcp_windows()
            elif self.os_type == 'Linux':
                self.optimize_tcp_linux()
        
        # Step 4: Show network stats
        self.get_network_stats()
        
        # Step 5: Test latency
        self.test_latency()
        
        # Update config
        self.config['optimized'] = True
        self.config['last_run'] = datetime.now().isoformat()
        self.save_config()
        
        print("\n" + "=" * 60)
        print("  OPTIMIZATION COMPLETE!")
        print("=" * 60)
        print("\n[+] Your network has been optimized for gaming and low latency")
        print("[+] You may need to restart your applications for full effect")
    
    def show_menu(self):
        """Show interactive menu"""
        while True:
            print("\n" + "=" * 60)
            print("  NETWORK OPTIMIZER PRO - MENU")
            print("=" * 60)
            print("1. Run Full Optimization")
            print("2. Test & Set Fastest DNS")
            print("3. Flush DNS Cache")
            print("4. Show Network Statistics")
            print("5. Monitor Bandwidth (10s)")
            print("6. Test Latency (Ping)")
            print("7. Show Top Bandwidth Consumers")
            print("8. Exit")
            print("=" * 60)
            
            choice = input("\nSelect option (1-8): ").strip()
            
            if choice == '1':
                self.run_full_optimization()
            elif choice == '2':
                fastest_dns = self.find_fastest_dns()
                if self.is_admin:
                    if self.os_type == 'Windows':
                        self.set_dns_windows(fastest_dns)
                    elif self.os_type == 'Linux':
                        self.set_dns_linux(fastest_dns)
            elif choice == '3':
                self.flush_dns_cache()
            elif choice == '4':
                self.get_network_stats()
            elif choice == '5':
                self.monitor_bandwidth()
            elif choice == '6':
                host = input("Enter host to ping (default: 8.8.8.8): ").strip() or '8.8.8.8'
                self.test_latency(host)
            elif choice == '7':
                self.show_top_bandwidth_consumers()
            elif choice == '8':
                print("\n[+] Thanks for using Network Optimizer Pro!")
                break
            else:
                print("[-] Invalid option")

def main():
    optimizer = NetworkOptimizer()
    optimizer.print_banner()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--optimize' or sys.argv[1] == '-o':
            optimizer.run_full_optimization()
        elif sys.argv[1] == '--dns':
            optimizer.find_fastest_dns()
        elif sys.argv[1] == '--monitor':
            optimizer.monitor_bandwidth()
        elif sys.argv[1] == '--stats':
            optimizer.get_network_stats()
    else:
        optimizer.show_menu()

if __name__ == '__main__':
    main()
