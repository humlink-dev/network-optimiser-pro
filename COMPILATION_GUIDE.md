# Network Optimizer Pro - Compilation & Setup Guide

## Quick Setup by Platform

### Windows Users

#### Method 1: Batch Scripts (Easiest - No Compilation Needed)
1. Download `windows_optimize.bat` and `windows_advanced_optimize.bat`
2. Right-click → "Run as Administrator"
3. Follow on-screen instructions
4. Restart computer

#### Method 2: Python Script (Recommended)
```batch
# Install Python from python.org (3.7 or higher)
# Open Command Prompt as Administrator

pip install psutil
python network_optimizer.py
```

#### Method 3: C++ Compilation
```batch
# Install MinGW or Visual Studio with C++ tools

# Using MinGW:
g++ -o network_monitor.exe network_monitor.cpp -lws2_32 -liphlpapi -std=c++11

# Using Visual Studio Developer Command Prompt:
cl network_monitor.cpp /Fe:network_monitor.exe ws2_32.lib iphlpapi.lib

# Run:
network_monitor.exe
```

---

### Linux Users

#### Method 1: Shell Script (Easiest)
```bash
chmod +x linux_optimize.sh
sudo ./linux_optimize.sh
```

#### Method 2: Python Script
```bash
# Install Python and pip (usually pre-installed)
pip install psutil

# Or use system package manager:
sudo apt install python3-psutil  # Debian/Ubuntu
sudo dnf install python3-psutil  # Fedora
sudo pacman -S python-psutil     # Arch

# Run:
sudo python3 network_optimizer.py
```

#### Method 3: C++ Compilation
```bash
# Install build tools
sudo apt install build-essential  # Debian/Ubuntu
sudo dnf install gcc-c++          # Fedora
sudo pacman -S base-devel         # Arch

# Compile:
g++ -o network_monitor network_monitor.cpp -std=c++11 -pthread

# Run:
./network_monitor
```

---

### macOS Users

#### Python Method
```bash
# Python usually comes pre-installed
pip3 install psutil

# Run:
sudo python3 network_optimizer.py
```

#### C++ Compilation
```bash
# Install Xcode Command Line Tools
xcode-select --install

# Compile:
g++ -o network_monitor network_monitor.cpp -std=c++11

# Run:
./network_monitor
```

---

## Detailed Compilation Instructions

### C++ Compilation by Compiler

#### GCC/G++ (Linux/macOS/MinGW)
```bash
# Basic compilation
g++ network_monitor.cpp -o network_monitor -std=c++11

# With optimizations
g++ network_monitor.cpp -o network_monitor -std=c++11 -O3

# With threading support (Linux)
g++ network_monitor.cpp -o network_monitor -std=c++11 -pthread

# Windows with MinGW
g++ network_monitor.cpp -o network_monitor.exe -std=c++11 -lws2_32 -liphlpapi
```

#### Visual Studio (Windows)
```batch
# Using Developer Command Prompt
cl /EHsc network_monitor.cpp ws2_32.lib iphlpapi.lib

# With optimizations
cl /O2 /EHsc network_monitor.cpp ws2_32.lib iphlpapi.lib
```

#### Clang (Alternative)
```bash
clang++ network_monitor.cpp -o network_monitor -std=c++11 -pthread
```

---

## Troubleshooting Compilation

### Common Errors and Solutions

#### "psutil not found"
```bash
# Python 3
pip3 install psutil

# Python 2 (not recommended)
pip install psutil

# System package manager (Linux)
sudo apt install python3-psutil
```

#### "Permission denied" when running
```bash
# Linux/Mac
chmod +x filename
sudo ./filename

# Windows
# Right-click → Run as Administrator
```

#### "winsock2.h not found" (Windows C++)
- Install MinGW with MSYS2: https://www.msys2.org/
- Or use Visual Studio with C++ Desktop Development workload

#### "undefined reference to pthread" (Linux C++)
```bash
# Add pthread flag
g++ network_monitor.cpp -o network_monitor -std=c++11 -pthread
```

#### "command not found: g++"
```bash
# Debian/Ubuntu
sudo apt update
sudo apt install build-essential

# Fedora
sudo dnf install gcc-c++

# macOS
xcode-select --install
```

---

## Performance Tips

### For Best Results:

1. **Run with Admin/Root Privileges**
   - Required for system-level optimizations
   - Enables DNS configuration changes
   - Allows TCP/IP stack modifications

2. **Close Background Applications**
   - Stop automatic updates
   - Close cloud sync services
   - Disable background downloads

3. **Use Wired Connection**
   - Ethernet > WiFi for gaming
   - WiFi adds 1-10ms latency
   - More stable connection

4. **Restart After Optimization**
   - Required for registry changes (Windows)
   - Ensures kernel parameters apply (Linux)
   - Clears network stack state

5. **Run During Off-Peak Hours**
   - Less network congestion
   - Better DNS response times
   - More stable routing

---

## Verification

### Test Your Optimization

After running optimization, test with:

```bash
# Python script
python network_optimizer.py --stats

# Linux shell
./linux_optimize.sh --stats

# Manual ping test
ping -n 50 8.8.8.8  # Windows
ping -c 50 8.8.8.8  # Linux/Mac
```

### What to Look For:
- ✅ Lower average latency
- ✅ More consistent ping times (less jitter)
- ✅ Fewer packet losses
- ✅ Faster DNS resolution
- ✅ Better connection stability

### Benchmarking
Run tests BEFORE and AFTER optimization:
1. Before: `ping -c 100 google.com`
2. Run optimization
3. Restart computer
4. After: `ping -c 100 google.com`
5. Compare average latency and packet loss

---

## Recommended Workflow

### First Time Setup:
1. Test current network performance (baseline)
2. Run optimization with admin privileges
3. Restart computer
4. Test again and compare results
5. Tweak settings if needed

### Regular Maintenance:
- Run DNS optimization weekly
- Monitor bandwidth monthly
- Re-optimize after major system updates

### Before Gaming Session:
1. Run quick optimization: `python network_optimizer.py --optimize`
2. Check for bandwidth consumers: Option 7 in menu
3. Close unnecessary applications
4. Verify latency: `ping game-server.com`

---

## Advanced Usage

### Custom DNS Servers
Edit the DNS server list in the scripts to add your preferred servers.

### Game-Specific Optimization
1. Find game server IPs
2. Test latency to those specific servers
3. Optimize routing for those IPs

### Integration with Other Tools
The Python script can be imported as a module:
```python
from network_optimizer import NetworkOptimizer

optimizer = NetworkOptimizer()
optimizer.run_full_optimization()
```

---

## Support Matrix

| Feature | Windows | Linux | macOS |
|---------|---------|-------|-------|
| DNS Optimization | ✅ | ✅ | ✅ |
| TCP/IP Tuning | ✅ | ✅ | ⚠️ Limited |
| Registry Tweaks | ✅ | N/A | N/A |
| Sysctl Optimization | N/A | ✅ | ✅ |
| Bandwidth Monitor | ✅ | ✅ | ✅ |
| Process Monitor | ✅ | ✅ | ✅ |
| Batch Scripts | ✅ | N/A | N/A |
| Shell Scripts | N/A | ✅ | ✅ |

---

## Getting Help

### If optimization doesn't work:
1. Verify admin/root privileges
2. Check error messages carefully
3. Review README.md for requirements
4. Test individual components separately
5. Ensure all dependencies are installed

### Still having issues?
- Check your antivirus isn't blocking scripts
- Verify Python/C++ version compatibility
- Test with simpler batch/shell scripts first
- Make sure Windows Firewall allows changes

---

## Next Steps

After successful setup:
1. Bookmark your baseline network performance
2. Schedule regular optimization (weekly/monthly)
3. Share with friends who game
4. Customize for your specific needs
5. Contribute improvements back to the project

Happy gaming! 🎮
