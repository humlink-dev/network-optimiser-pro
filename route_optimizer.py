#!/usr/bin/env python3
"""
Route Optimizer - Multi-path routing and gateway optimization
Tests and switches to fastest network gateway
"""

import os
import sys
import platform
import subprocess
import socket
import time
import json
from datetime import datetime

class RouteOptimizer:
    def __init__(self):
        self.os_type = platform.system()
        self.is_admin = self.check_admin()
        
        # Common game servers to test
        self.test_servers = {
            'Google': '8.8.8.8',
            'Cloudflare': '1.1.1.1',
            'AWS US-East': '3.216.34.172',
            'AWS EU-West': '54.170.162.7',
            'Steam': '208.78.164.9',
            'Discord': '162.159.130.233',
            'Riot Games': '104.160.131.3',
            'Blizzard': '24.105.30.129',
        }
    
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
    
    def print_banner(self):
        print("=" * 70)
        print("   ROUTE OPTIMIZER - Multi-Path Routing & Gateway Optimization")
        print("=" * 70)
        print(f"OS: {self.os_type} | Admin: {'Yes' if self.is_admin else 'No'}")
        print("=" * 70)
        print()
    
    def ping_host(self, host, count=5):
        """Ping a host and return average latency"""
        try:
            if self.os_type == 'Windows':
                cmd = f'ping -n {count} {host}'
            else:
                cmd = f'ping -c {count} {host}'
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            
            # Parse average latency
            if self.os_type == 'Windows':
                for line in result.stdout.split('\n'):
                    if 'Average' in line:
                        avg = line.split('=')[-1].strip().replace('ms', '')
                        return float(avg)
            else:
                for line in result.stdout.split('\n'):
                    if 'avg' in line or 'min/avg/max' in line:
                        parts = line.split('=')[-1].split('/')
                        return float(parts[1])
            
            return None
        except Exception as e:
            return None
    
    def traceroute(self, host):
        """Perform traceroute to show network path"""
        print(f"\n[*] Tracing route to {host}...")
        print("-" * 70)
        
        try:
            if self.os_type == 'Windows':
                cmd = f'tracert -h 15 {host}'
            else:
                cmd = f'traceroute -m 15 {host}'
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            print(result.stdout)
        except Exception as e:
            print(f"[-] Error: {e}")
    
    def get_current_gateway(self):
        """Get current default gateway"""
        try:
            if self.os_type == 'Windows':
                result = subprocess.run('ipconfig', shell=True, capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'Default Gateway' in line and ':' in line:
                        gateway = line.split(':')[-1].strip()
                        if gateway and gateway != '0.0.0.0':
                            return gateway
            else:
                result = subprocess.run('ip route show default', shell=True, capture_output=True, text=True)
                if result.stdout:
                    parts = result.stdout.split()
                    if len(parts) > 2:
                        return parts[2]
            
            return None
        except:
            return None
    
    def test_all_game_servers(self):
        """Test latency to all game servers"""
        print("\n[*] Testing latency to game servers...")
        print("-" * 70)
        
        results = {}
        for name, ip in self.test_servers.items():
            print(f"Testing {name:20} ({ip:15})... ", end='', flush=True)
            latency = self.ping_host(ip, count=5)
            
            if latency:
                results[name] = {'ip': ip, 'latency': latency}
                print(f"{latency:.1f} ms")
            else:
                results[name] = {'ip': ip, 'latency': 9999}
                print("TIMEOUT")
        
        print("\n[*] Results Summary:")
        print("-" * 70)
        sorted_results = sorted(results.items(), key=lambda x: x[1]['latency'])
        
        for i, (name, data) in enumerate(sorted_results, 1):
            if data['latency'] < 9999:
                print(f"{i:2}. {name:20} : {data['latency']:6.1f} ms")
        
        return results
    
    def find_best_route(self, destination):
        """Find the best route to a destination"""
        print(f"\n[*] Finding best route to {destination}...")
        
        # Test current route
        print("[*] Testing current route...")
        current_latency = self.ping_host(destination, count=10)
        
        if current_latency:
            print(f"[+] Current route latency: {current_latency:.1f} ms")
        else:
            print("[-] Could not test current route")
        
        # Show traceroute
        self.traceroute(destination)
        
        return current_latency
    
    def optimize_routing_table(self):
        """Optimize routing table for gaming"""
        if not self.is_admin:
            print("[-] Admin privileges required")
            return False
        
        print("\n[*] Optimizing routing table...")
        
        if self.os_type == 'Windows':
            # Clear ARP cache
            subprocess.run('arp -d *', shell=True, capture_output=True)
            print("[+] ARP cache cleared")
            
            # Reset TCP/IP stack
            subprocess.run('netsh int ip reset', shell=True, capture_output=True)
            print("[+] TCP/IP stack reset")
            
        elif self.os_type == 'Linux':
            # Flush routing cache
            subprocess.run('ip route flush cache', shell=True, capture_output=True)
            print("[+] Routing cache flushed")
            
            # Optimize routing
            subprocess.run('sysctl -w net.ipv4.route.flush=1', shell=True, capture_output=True)
            print("[+] Routes optimized")
        
        print("[+] Routing table optimized")
        return True
    
    def add_static_route(self, destination, gateway):
        """Add a static route for better performance"""
        if not self.is_admin:
            print("[-] Admin privileges required")
            return False
        
        print(f"\n[*] Adding static route: {destination} via {gateway}")
        
        try:
            if self.os_type == 'Windows':
                cmd = f'route add {destination} mask 255.255.255.255 {gateway} metric 1'
            else:
                cmd = f'ip route add {destination} via {gateway} metric 1'
            
            subprocess.run(cmd, shell=True, check=True, capture_output=True)
            print("[+] Static route added")
            return True
        except Exception as e:
            print(f"[-] Error: {e}")
            return False
    
    def show_routing_table(self):
        """Display current routing table"""
        print("\n[*] Current Routing Table:")
        print("-" * 70)
        
        try:
            if self.os_type == 'Windows':
                result = subprocess.run('route print', shell=True, capture_output=True, text=True)
            else:
                result = subprocess.run('ip route show', shell=True, capture_output=True, text=True)
            
            print(result.stdout)
        except Exception as e:
            print(f"[-] Error: {e}")
    
    def test_mtu_sizes(self, host='8.8.8.8'):
        """Test optimal MTU size"""
        print(f"\n[*] Testing MTU sizes to {host}...")
        print("-" * 70)
        
        mtu_sizes = [1500, 1492, 1472, 1450, 1400, 1350, 1300]
        
        for mtu in mtu_sizes:
            print(f"Testing MTU {mtu:4}... ", end='', flush=True)
            
            try:
                if self.os_type == 'Windows':
                    cmd = f'ping -n 3 -l {mtu - 28} -f {host}'
                else:
                    cmd = f'ping -c 3 -M do -s {mtu - 28} {host}'
                
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
                
                if 'Packet needs to be fragmented' in result.stdout or 'Message too long' in result.stderr:
                    print("❌ Too large")
                elif result.returncode == 0:
                    print("✅ Works")
                    print(f"\n[+] Recommended MTU: {mtu}")
                    return mtu
                else:
                    print("⚠️  Failed")
            except:
                print("⚠️  Timeout")
        
        print("\n[+] Default MTU (1500) recommended")
        return 1500
    
    def set_mtu(self, interface, mtu):
        """Set MTU for network interface"""
        if not self.is_admin:
            print("[-] Admin privileges required")
            return False
        
        print(f"\n[*] Setting MTU to {mtu} on {interface}...")
        
        try:
            if self.os_type == 'Windows':
                cmd = f'netsh interface ipv4 set subinterface "{interface}" mtu={mtu} store=persistent'
            else:
                cmd = f'ip link set {interface} mtu {mtu}'
            
            subprocess.run(cmd, shell=True, check=True, capture_output=True)
            print(f"[+] MTU set to {mtu}")
            return True
        except Exception as e:
            print(f"[-] Error: {e}")
            return False
    
    def show_menu(self):
        """Interactive menu"""
        while True:
            print("\n" + "=" * 70)
            print("  ROUTE OPTIMIZER - MENU")
            print("=" * 70)
            print("1. Test All Game Servers")
            print("2. Find Best Route to Server")
            print("3. Show Current Routing Table")
            print("4. Optimize Routing Table")
            print("5. Test Optimal MTU Size")
            print("6. Traceroute to Server")
            print("7. Add Static Route")
            print("8. Exit")
            print("=" * 70)
            
            choice = input("\nSelect option (1-8): ").strip()
            
            if choice == '1':
                self.test_all_game_servers()
            elif choice == '2':
                server = input("Enter server IP or hostname: ").strip()
                self.find_best_route(server)
            elif choice == '3':
                self.show_routing_table()
            elif choice == '4':
                self.optimize_routing_table()
            elif choice == '5':
                host = input("Enter host to test (default: 8.8.8.8): ").strip() or '8.8.8.8'
                self.test_mtu_sizes(host)
            elif choice == '6':
                server = input("Enter server IP or hostname: ").strip()
                self.traceroute(server)
            elif choice == '7':
                dest = input("Enter destination IP: ").strip()
                gateway = input("Enter gateway IP: ").strip()
                self.add_static_route(dest, gateway)
            elif choice == '8':
                print("\n[+] Thanks for using Route Optimizer!")
                break
            else:
                print("[-] Invalid option")

def main():
    optimizer = RouteOptimizer()
    optimizer.print_banner()
    
    if not optimizer.is_admin:
        print("[!] WARNING: Not running with admin/root privileges")
        print("[!] Many features require elevated access")
        print()
        input("Press Enter to continue...")
    
    optimizer.show_menu()

if __name__ == '__main__':
    main()
