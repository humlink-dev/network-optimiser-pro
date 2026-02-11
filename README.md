# Network Optimizer Pro - Complete Gaming & Latency Optimization Toolkit

A comprehensive network optimization suite that reduces latency, optimizes routing, and monitors network performance. Think of it as a DIY ExitLag alternative!

## 🚀 Features

### Core Features
- **DNS Optimization** - Automatically finds and switches to the fastest DNS servers
- **TCP/IP Optimization** - Tunes network stack for lower latency
- **Bandwidth Monitoring** - Real-time monitoring of network usage
- **Latency Testing** - Continuous ping monitoring with statistics
- **Network Statistics** - Detailed information about your connection
- **Process Monitoring** - Identifies bandwidth-hungry applications
- **Multi-platform Support** - Works on Windows, Linux, and macOS

### What It Does (Realistically)
1. **Optimizes DNS routing** - Connects you to faster DNS servers (5-50ms improvement)
2. **Reduces TCP overhead** - Disables Nagle's algorithm and optimizes TCP windows
3. **Identifies bottlenecks** - Shows which apps are consuming bandwidth
4. **Monitors connection quality** - Tracks packet loss and latency spikes
5. **System-level optimizations** - Registry and sysctl tweaks for gaming

### What It DOESN'T Do
❌ Cannot increase your ISP bandwidth beyond your plan
❌ Cannot reduce physical distance latency (speed of light limit)
❌ Cannot create VPN-style proxy routes (use actual VPN/ExitLag for that)
❌ Cannot perform miracles - your base connection still matters

## 📦 Installation

### Prerequisites

**For Python version:**
```bash
pip install psutil
```

**For C++ version:**
- Windows: Visual Studio with C++ tools or MinGW
- Linux: g++ compiler
- macOS: Xcode command line tools

### Quick Install

```bash
# Clone or download the files
cd network-optimizer-pro

# Install Python dependencies
pip install -r requirements.txt

# Make scripts executable (Linux/Mac)
chmod +x network_optimizer.py
```

## 🎮 Usage

### Python Version (Recommended for most users)

#### Interactive Menu Mode
```bash
python network_optimizer.py
```

#### Quick Optimization
```bash
# Run with admin/sudo for full functionality
sudo python network_optimizer.py --optimize
```

#### Command Line Options
```bash
python network_optimizer.py --dns          # Test DNS servers only
python network_optimizer.py --monitor      # Monitor bandwidth
python network_optimizer.py --stats        # Show network stats
```

### C++ Version (For performance enthusiasts)

#### Compile
```bash
# Windows (MinGW)
g++ -o network_monitor.exe network_monitor.cpp -lws2_32 -liphlpapi -std=c++11

# Linux
g++ -o network_monitor network_monitor.cpp -std=c++11 -pthread

# macOS
g++ -o network_monitor network_monitor.cpp -std=c++11
```

#### Run
```bash
./network_monitor                    # Interactive menu
./network_monitor --dns              # Test DNS servers
./network_monitor --monitor 8.8.8.8  # Monitor specific host
```

### Windows Batch Scripts

#### Quick Optimization (Easiest)
1. Right-click `windows_optimize.bat`
2. Select "Run as Administrator"
3. Wait for completion
4. Restart computer

#### Advanced Registry Tweaks
1. Right-click `windows_advanced_optimize.bat`
2. Select "Run as Administrator"
3. Creates automatic backup
4. **MUST RESTART** after completion

## 🛠️ Features Breakdown

### 1. DNS Optimization
Tests multiple DNS providers and switches to the fastest:
- Cloudflare (1.1.1.1)
- Google (8.8.8.8)
- Quad9 (9.9.9.9)
- OpenDNS (208.67.222.222)
- AdGuard (94.140.14.14)

**Expected improvement:** 5-50ms faster DNS resolution

### 2. TCP/IP Optimizations

**Windows:**
- Enables TCP window scaling
- Disables Nagle's algorithm
- Enables RSS (Receive Side Scaling)
- Sets CTCP congestion provider
- Optimizes auto-tuning level

**Linux:**
- Enables TCP Fast Open
- Sets BBR congestion control
- Increases network buffers
- Enables SACK and timestamps

**Expected improvement:** 10-30ms lower latency, reduced jitter

### 3. Network Monitoring

**Real-time Bandwidth Monitor:**
- Shows upload/download speeds per second
- Identifies bandwidth spikes
- Tracks network interface statistics

**Latency Monitor (C++):**
- Continuous ping monitoring
- Min/Max/Average latency tracking
- Packet loss percentage
- High-resolution timing

**Process Monitor:**
- Lists top bandwidth consumers
- Shows connection counts per application
- Helps identify background downloads

### 4. Windows Registry Tweaks

The advanced script optimizes:
- Network adapter IRQ priority
- System responsiveness
- Gaming task priorities
- TCP window sizes
- DNS cache settings
- Network throttling

## ⚠️ Important Notes

### Administrator/Root Required
Most optimizations require elevated privileges:
- **Windows:** Run as Administrator
- **Linux:** Use `sudo`
- **macOS:** Use `sudo`

### Restart Required
After running optimizations, restart your computer for full effect.

### Backup
Windows advanced script automatically creates registry backup on Desktop.

### Compatibility
- **Windows:** 10/11 (7/8 may work)
- **Linux:** Most distributions with systemd
- **macOS:** 10.14+

### Safety
All optimizations are safe and reversible:
- Python script: Changes can be reverted
- Batch scripts: Registry backup created
- No permanent hardware changes

## 📊 Expected Results

### Best Case Scenario
- DNS resolution: 20-50ms faster
- Gaming latency: 10-30ms improvement
- Connection stability: Reduced jitter
- Better routing through optimized TCP

### Realistic Expectations
Your results depend on:
1. **Base connection quality** - Fiber > Cable > DSL
2. **ISP routing** - Some ISPs have better routes
3. **Geographic location** - Closer to servers = lower latency
4. **Network congestion** - Peak hours affect everyone
5. **Game server location** - Physical distance matters most

### What Won't Change
- Your ISP's bandwidth cap
- Physical distance to game servers
- ISP's peering agreements
- Network infrastructure quality

## 🎯 Use Cases

### Gaming
- Reduces input lag in online games
- Stabilizes connection during gameplay
- Identifies background apps affecting performance
- Optimizes for competitive gaming

### Streaming
- Reduces buffering through better DNS
- Optimizes upload for streamers
- Monitors bandwidth usage

### General Use
- Faster web browsing
- More stable video calls
- Better file download speeds
- Network troubleshooting

## 🔧 Troubleshooting

### "Permission Denied"
Run with administrator/sudo privileges

### "Module not found: psutil"
Install requirements: `pip install psutil`

### DNS Changes Don't Apply
- Windows: Use `ipconfig /flushdns`
- Restart network adapter
- Reboot computer

### No Improvement
Some factors are outside software control:
- Physical connection quality
- ISP limitations
- Server-side issues
- Network infrastructure

### Undo Changes

**Windows Quick Reset:**
```batch
netsh int ip reset
netsh winsock reset
ipconfig /flushdns
```

**Linux:**
Edit `/etc/resolv.conf` to restore original DNS

**Registry (if backup exists):**
Double-click the backup `.reg` file on Desktop

## 🤝 Contributing

Found a bug? Have an optimization technique? Contributions welcome!

## 📝 License

Free to use for personal and commercial purposes.

## ⚡ Quick Start Guide

**For Gamers (Windows):**
1. Download `windows_optimize.bat`
2. Right-click → Run as Administrator
3. Restart computer
4. Launch game and enjoy lower latency!

**For Power Users:**
1. Install Python and psutil
2. Run `python network_optimizer.py`
3. Choose option 1 (Full Optimization)
4. Restart computer

**For Developers:**
1. Compile C++ version for maximum performance
2. Integrate into your monitoring tools
3. Customize for specific use cases

## 📧 Support

If you encounter issues:
1. Check your admin/sudo privileges
2. Verify Python/C++ installation
3. Review error messages carefully
4. Try Windows batch scripts for simplest approach

## 🎓 How It Works

Unlike ExitLag which provides VPN routing with optimized paths to game servers, this toolkit optimizes your LOCAL network configuration:

1. **DNS Optimization:** Reduces initial connection time
2. **TCP Tuning:** Reduces per-packet overhead
3. **QoS Settings:** Prioritizes gaming traffic locally
4. **Monitoring:** Identifies and removes bottlenecks

Think of it as tuning your car's engine (local optimizations) vs changing the route you drive (VPN routing). Both help, but work differently!

---

**Made for gamers, by gamers. Game on! 🎮**
