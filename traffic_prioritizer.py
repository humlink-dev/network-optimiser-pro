#!/usr/bin/env python3
"""
Traffic Prioritizer Pro - QoS and Gaming Traffic Optimization
Prioritizes gaming and streaming traffic over background downloads
"""

import os
import sys
import platform
import subprocess
import psutil
import json
from pathlib import Path

class TrafficPrioritizer:
    def __init__(self):
        self.os_type = platform.system()
        self.is_admin = self.check_admin()
        
        # Gaming ports (common games)
        self.gaming_ports = {
            'Valorant': [7000, 8000, 8001],
            'League of Legends': [5000, 5500, 8393, 8394],
            'CS:GO/CS2': [27015, 27016, 27017],
            'Dota 2': [27015, 27016, 27017, 27018],
            'Fortnite': [9000, 9002, 9005],
            'Apex Legends': [37005, 37015, 37017],
            'Call of Duty': [3074, 3478, 27000, 27036],
            'PUBG': [27015, 27016, 27017],
            'Overwatch': [3478, 3479, 6250, 27014, 27015],
            'Minecraft': [25565],
            'Rocket League': [7000, 7001, 7002],
            'Rainbow Six Siege': [3074, 6015],
            'FIFA': [3659, 9960, 9988, 10000],
            'Destiny 2': [3074, 3097, 3478, 7500, 27000],
            'GTA Online': [6672, 61455, 61456, 61457, 61458],
        }
        
        # Streaming ports
        self.streaming_ports = {
            'Twitch': [1935, 3478, 3479, 3480],
            'YouTube Live': [1935, 443],
            'Discord Voice': [50000, 50010, 50020],
            'Zoom': [8801, 8802, 8803, 8804],
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
        print("   TRAFFIC PRIORITIZER PRO - QoS & Gaming Optimization")
        print("=" * 70)
        print(f"OS: {self.os_type} | Admin: {'Yes' if self.is_admin else 'No'}")
        print("=" * 70)
        print()
    
    def list_gaming_ports(self):
        """Display all supported games and their ports"""
        print("\n[*] Supported Games and Ports:")
        print("-" * 70)
        for game, ports in self.gaming_ports.items():
            print(f"  {game:25} : {', '.join(map(str, ports))}")
        print()
    
    def setup_qos_windows(self, game_name=None):
        """Setup QoS on Windows using Group Policy"""
        if not self.is_admin:
            print("[-] Admin privileges required for QoS setup")
            return False
        
        print("\n[*] Setting up Windows QoS policies...")
        
        # Enable QoS on all network adapters
        cmd = 'powershell -Command "Get-NetAdapter | Set-NetAdapterBinding -ComponentID ms_pacer -Enabled $true"'
        subprocess.run(cmd, shell=True, capture_output=True)
        
        # Set gaming traffic to high priority
        if game_name and game_name in self.gaming_ports:
            ports = self.gaming_ports[game_name]
            for port in ports:
                # Create QoS policy for each port
                cmd = f'netsh advfirewall firewall add rule name="QoS_{game_name}_{port}" dir=out action=allow protocol=UDP localport={port} enable=yes'
                subprocess.run(cmd, shell=True, capture_output=True)
                
                cmd = f'netsh advfirewall firewall add rule name="QoS_{game_name}_{port}_TCP" dir=out action=allow protocol=TCP localport={port} enable=yes'
                subprocess.run(cmd, shell=True, capture_output=True)
        
        # Disable bandwidth reservation
        reg_cmd = 'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Psched" /v NonBestEffortLimit /t REG_DWORD /d 0 /f'
        subprocess.run(reg_cmd, shell=True, capture_output=True)
        
        print("[+] Windows QoS configured")
        return True
    
    def setup_tc_linux(self, interface='eth0'):
        """Setup Traffic Control (tc) on Linux"""
        if not self.is_admin:
            print("[-] Root privileges required for Traffic Control setup")
            return False
        
        print(f"\n[*] Setting up Linux Traffic Control on {interface}...")
        
        # Clear existing rules
        subprocess.run(f'tc qdisc del dev {interface} root 2>/dev/null', shell=True)
        
        # Create HTB qdisc (Hierarchical Token Bucket)
        subprocess.run(f'tc qdisc add dev {interface} root handle 1: htb default 30', shell=True)
        
        # Create classes with different priorities
        # Class 1:10 - Gaming (highest priority, 80% bandwidth)
        subprocess.run(f'tc class add dev {interface} parent 1: classid 1:10 htb rate 80mbit ceil 100mbit prio 0', shell=True)
        
        # Class 1:20 - Streaming (medium priority, 60% bandwidth)
        subprocess.run(f'tc class add dev {interface} parent 1: classid 1:20 htb rate 60mbit ceil 90mbit prio 1', shell=True)
        
        # Class 1:30 - Default (low priority, 30% bandwidth)
        subprocess.run(f'tc class add dev {interface} parent 1: classid 1:30 htb rate 30mbit ceil 80mbit prio 2', shell=True)
        
        # Add filters for gaming ports
        for game, ports in self.gaming_ports.items():
            for port in ports:
                # UDP filter
                subprocess.run(f'tc filter add dev {interface} protocol ip parent 1:0 prio 0 u32 match ip dport {port} 0xffff flowid 1:10', shell=True, capture_output=True)
                # TCP filter
                subprocess.run(f'tc filter add dev {interface} protocol ip parent 1:0 prio 0 u32 match ip sport {port} 0xffff flowid 1:10', shell=True, capture_output=True)
        
        print("[+] Linux Traffic Control configured")
        print("[+] Gaming traffic prioritized on", interface)
        return True
    
    def kill_bandwidth_hogs(self):
        """Identify and optionally kill bandwidth-consuming processes"""
        print("\n[*] Scanning for bandwidth-consuming processes...")
        print("-" * 70)
        
        # Get all connections
        connections = psutil.net_connections(kind='inet')
        
        # Count connections per process
        process_connections = {}
        for conn in connections:
            if conn.pid:
                try:
                    proc = psutil.Process(conn.pid)
                    name = proc.name()
                    
                    if name not in process_connections:
                        process_connections[name] = {
                            'pid': conn.pid,
                            'connections': 0,
                            'process': proc
                        }
                    process_connections[name]['connections'] += 1
                except:
                    pass
        
        # Sort by connection count
        sorted_procs = sorted(process_connections.items(), 
                            key=lambda x: x[1]['connections'], 
                            reverse=True)[:15]
        
        # Known bandwidth hogs
        bandwidth_hogs = [
            'chrome', 'firefox', 'edge', 'steam', 'epicgameslauncher',
            'origin', 'battle.net', 'uplay', 'torrent', 'bittorrent',
            'utorrent', 'qbittorrent', 'onedrive', 'dropbox', 'googledrivesync',
            'backup', 'windows update', 'software update'
        ]
        
        print("\nTop Network Consumers:")
        potential_hogs = []
        
        for i, (name, info) in enumerate(sorted_procs, 1):
            is_hog = any(hog in name.lower() for hog in bandwidth_hogs)
            marker = "⚠️  BANDWIDTH HOG" if is_hog else ""
            print(f"{i:2}. {name:30} (PID: {info['pid']:6}) - {info['connections']:3} connections {marker}")
            
            if is_hog:
                potential_hogs.append((name, info))
        
        if potential_hogs:
            print("\n[!] Detected potential bandwidth hogs!")
            print("\nWould you like to suspend these processes? (y/n): ", end='')
            choice = input().strip().lower()
            
            if choice == 'y':
                for name, info in potential_hogs:
                    try:
                        proc = info['process']
                        proc.suspend()
                        print(f"[+] Suspended: {name} (PID: {info['pid']})")
                    except Exception as e:
                        print(f"[-] Could not suspend {name}: {e}")
    
    def optimize_for_game(self, game_name):
        """Optimize network for specific game"""
        if game_name not in self.gaming_ports:
            print(f"[-] Game '{game_name}' not found in database")
            print("[*] Available games:")
            for game in self.gaming_ports.keys():
                print(f"    - {game}")
            return False
        
        print(f"\n[*] Optimizing network for {game_name}...")
        ports = self.gaming_ports[game_name]
        print(f"[*] Game ports: {', '.join(map(str, ports))}")
        
        if self.os_type == 'Windows':
            self.setup_qos_windows(game_name)
        elif self.os_type == 'Linux':
            # Get active network interface
            interfaces = psutil.net_if_stats()
            active_interface = None
            for iface, stats in interfaces.items():
                if stats.isup and iface != 'lo':
                    active_interface = iface
                    break
            
            if active_interface:
                self.setup_tc_linux(active_interface)
        
        print(f"[+] Network optimized for {game_name}")
        return True
    
    def show_active_connections(self):
        """Show active network connections with details"""
        print("\n[*] Active Network Connections:")
        print("-" * 90)
        
        connections = psutil.net_connections(kind='inet')
        
        # Group by process
        process_conns = {}
        for conn in connections:
            if conn.pid and conn.status == 'ESTABLISHED':
                try:
                    proc = psutil.Process(conn.pid)
                    name = proc.name()
                    
                    if name not in process_conns:
                        process_conns[name] = []
                    
                    process_conns[name].append({
                        'local': f"{conn.laddr.ip}:{conn.laddr.port}",
                        'remote': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
                        'type': 'TCP' if conn.type == 1 else 'UDP'
                    })
                except:
                    pass
        
        for name, conns in sorted(process_conns.items()):
            print(f"\n{name} ({len(conns)} connections):")
            for conn in conns[:5]:  # Show first 5
                print(f"  {conn['type']:4} {conn['local']:25} -> {conn['remote']:25}")
            if len(conns) > 5:
                print(f"  ... and {len(conns) - 5} more")
    
    def create_firewall_rules(self, game_name):
        """Create firewall rules to allow game traffic"""
        if not self.is_admin:
            print("[-] Admin privileges required")
            return False
        
        if game_name not in self.gaming_ports:
            print(f"[-] Game '{game_name}' not found")
            return False
        
        print(f"\n[*] Creating firewall rules for {game_name}...")
        ports = self.gaming_ports[game_name]
        
        if self.os_type == 'Windows':
            for port in ports:
                # Inbound rule
                cmd = f'netsh advfirewall firewall add rule name="{game_name}_In_{port}" dir=in action=allow protocol=ANY localport={port}'
                subprocess.run(cmd, shell=True, capture_output=True)
                
                # Outbound rule
                cmd = f'netsh advfirewall firewall add rule name="{game_name}_Out_{port}" dir=out action=allow protocol=ANY localport={port}'
                subprocess.run(cmd, shell=True, capture_output=True)
            
            print(f"[+] Created firewall rules for {game_name}")
        
        elif self.os_type == 'Linux':
            for port in ports:
                # Allow inbound
                subprocess.run(f'iptables -A INPUT -p tcp --dport {port} -j ACCEPT', shell=True, capture_output=True)
                subprocess.run(f'iptables -A INPUT -p udp --dport {port} -j ACCEPT', shell=True, capture_output=True)
                
                # Allow outbound
                subprocess.run(f'iptables -A OUTPUT -p tcp --sport {port} -j ACCEPT', shell=True, capture_output=True)
                subprocess.run(f'iptables -A OUTPUT -p udp --sport {port} -j ACCEPT', shell=True, capture_output=True)
            
            print(f"[+] Created iptables rules for {game_name}")
        
        return True
    
    def show_menu(self):
        """Interactive menu"""
        while True:
            print("\n" + "=" * 70)
            print("  TRAFFIC PRIORITIZER PRO - MENU")
            print("=" * 70)
            print("1. Optimize for Specific Game")
            print("2. List Supported Games")
            print("3. Show Active Connections")
            print("4. Scan for Bandwidth Hogs")
            print("5. Create Firewall Rules for Game")
            print("6. Setup QoS/Traffic Control")
            print("7. Exit")
            print("=" * 70)
            
            choice = input("\nSelect option (1-7): ").strip()
            
            if choice == '1':
                self.list_gaming_ports()
                game = input("Enter game name: ").strip()
                self.optimize_for_game(game)
            elif choice == '2':
                self.list_gaming_ports()
            elif choice == '3':
                self.show_active_connections()
            elif choice == '4':
                self.kill_bandwidth_hogs()
            elif choice == '5':
                self.list_gaming_ports()
                game = input("Enter game name: ").strip()
                self.create_firewall_rules(game)
            elif choice == '6':
                if self.os_type == 'Windows':
                    self.setup_qos_windows()
                elif self.os_type == 'Linux':
                    iface = input("Enter network interface (default: eth0): ").strip() or 'eth0'
                    self.setup_tc_linux(iface)
            elif choice == '7':
                print("\n[+] Thanks for using Traffic Prioritizer Pro!")
                break
            else:
                print("[-] Invalid option")

def main():
    prioritizer = TrafficPrioritizer()
    prioritizer.print_banner()
    
    if not prioritizer.is_admin:
        print("[!] WARNING: Not running with admin/root privileges")
        print("[!] Many features require elevated access")
        print()
        input("Press Enter to continue...")
    
    prioritizer.show_menu()

if __name__ == '__main__':
    main()
