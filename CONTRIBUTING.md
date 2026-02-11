# Contributing to Network Optimizer Pro

First off, thank you for considering contributing to Network Optimizer Pro! 🎉

## 🤝 How Can I Contribute?

### Reporting Bugs 🐛

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the problem
- **Expected behavior** vs actual behavior
- **System information:**
  - OS and version
  - Python version
  - Admin/root privileges (yes/no)
- **Error messages** (full traceback if applicable)
- **Screenshots** (if relevant)

**Example Bug Report:**
```
Title: DNS optimization fails on Ubuntu 22.04

Description: When running dns optimization, script crashes with permission error

Steps to Reproduce:
1. Run: sudo python3 network_optimizer.py
2. Select option 2 (Test & Set Fastest DNS)
3. Error occurs

Expected: DNS servers should be tested and fastest one applied
Actual: Script crashes with "Permission denied" error

System:
- OS: Ubuntu 22.04 LTS
- Python: 3.10.4
- Sudo: Yes

Error Message:
[Full traceback here]
```

### Suggesting Features 💡

Feature suggestions are welcome! Please:

1. Check if the feature already exists or is requested
2. Explain the **use case** and **why** it's needed
3. Describe how it should **work**
4. Consider **platform compatibility**

**Example Feature Request:**
```
Title: Add support for game server region selection

Description: 
Allow users to specify their game server region (NA, EU, Asia, etc.) 
and automatically optimize routing for those specific servers.

Use Case:
Many gamers play on specific regional servers. Optimizing routes to 
the wrong region wastes effort.

Proposed Implementation:
- Add region selection in menu
- Store region-specific server IPs
- Prioritize testing/optimization for selected region

Platform Compatibility:
Should work on Windows, Linux, and macOS
```

### Adding New Games 🎮

To add support for a new game:

1. Find the game's network ports (check game documentation or use Wireshark)
2. Edit `traffic_prioritizer.py`
3. Add to the `gaming_ports` dictionary:

```python
self.gaming_ports = {
    # ... existing games ...
    'Your Game Name': [port1, port2, port3],
}
```

4. Test thoroughly
5. Submit a pull request

### Code Contributions 💻

#### Getting Started

1. **Fork** the repository
2. **Clone** your fork:
   ```bash
   git clone https://github.com/yourusername/network-optimizer-pro.git
   cd network-optimizer-pro
   ```
3. **Create a branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

#### Development Guidelines

**Python Code Style:**
- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions
- Comment complex logic
- Keep functions under 50 lines when possible

**Example:**
```python
def test_dns_latency(self, dns_server, timeout=2):
    """
    Test DNS server response time.
    
    Args:
        dns_server (str): DNS server IP address
        timeout (int): Connection timeout in seconds
    
    Returns:
        float: Latency in milliseconds, or 9999 if failed
    """
    try:
        start = time.time()
        # Test connection logic here
        latency = (time.time() - start) * 1000
        return latency
    except:
        return 9999
```

**Testing:**
- Test on multiple platforms (Windows, Linux, macOS if possible)
- Test with and without admin privileges
- Test edge cases (no internet, wrong input, etc.)
- Document any platform-specific behavior

**Commit Messages:**
```bash
# Good commit messages:
git commit -m "Add support for Apex Legends port optimization"
git commit -m "Fix DNS cache flush on macOS Catalina"
git commit -m "Improve error handling in route_optimizer.py"

# Bad commit messages:
git commit -m "update"
git commit -m "fix bug"
git commit -m "asdf"
```

#### Pull Request Process

1. **Update documentation** if needed
2. **Test thoroughly** on at least one platform
3. **Update CHANGELOG.md** with your changes
4. **Submit PR** with:
   - Clear title
   - Description of changes
   - Testing performed
   - Related issue number (if applicable)

**PR Template:**
```markdown
## Description
Brief description of what this PR does

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Tested on Windows
- [ ] Tested on Linux
- [ ] Tested on macOS
- [ ] Tested with admin privileges
- [ ] Tested without admin privileges

## Checklist
- [ ] Code follows project style guidelines
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] No breaking changes (or documented)
```

### Improving Documentation 📚

Documentation improvements are always welcome:

- Fix typos and grammatical errors
- Clarify confusing sections
- Add examples and use cases
- Translate to other languages
- Create video tutorials

### Platform-Specific Contributions

**Windows Experts:**
- Improve batch scripts
- Add PowerShell alternatives
- Test on various Windows versions
- Optimize registry tweaks

**Linux Experts:**
- Improve shell scripts
- Add systemd service files
- Test on various distributions
- Optimize kernel parameters

**macOS Experts:**
- Add macOS-specific optimizations
- Test on different macOS versions
- Document macOS-specific issues

**C++ Developers:**
- Optimize network_monitor.cpp
- Add new monitoring features
- Improve cross-platform compatibility
- Reduce compilation dependencies

## 🎨 Style Guidelines

### Python
```python
# Good
def optimize_network(interface: str, mtu_size: int = 1500) -> bool:
    """Optimize network interface settings."""
    if not self.is_admin:
        print("[-] Admin privileges required")
        return False
    
    try:
        # Optimization logic
        return True
    except Exception as e:
        print(f"[-] Error: {e}")
        return False

# Bad
def opt(i,m=1500):
    if not self.is_admin:print("need admin")
    try:
        # stuff
        return True
    except:pass
```

### Shell Scripts
```bash
# Good
optimize_network() {
    local interface=$1
    local mtu_size=${2:-1500}
    
    if [ "$EUID" -ne 0 ]; then
        echo "[-] Root privileges required"
        return 1
    fi
    
    # Optimization logic
    return 0
}

# Bad
opt(){if [ "$EUID" -ne 0 ];then echo "need root";fi;}
```

## 🏗️ Project Structure

```
network-optimizer-pro/
├── network_optimizer.py        # Main optimization tool
├── traffic_prioritizer.py      # QoS and traffic management
├── route_optimizer.py          # Route optimization
├── network_monitor.cpp         # C++ monitoring tool
├── windows_optimize.bat        # Windows quick script
├── windows_advanced_optimize.bat
├── linux_optimize.sh           # Linux shell script
├── requirements.txt            # Python dependencies
├── README.md                   # Main documentation
├── README_GITHUB.md            # GitHub version
├── COMPILATION_GUIDE.md        # Compilation instructions
├── CONTRIBUTING.md             # This file
├── LICENSE                     # MIT License
└── CHANGELOG.md                # Version history
```

## 🧪 Testing Checklist

Before submitting a PR, verify:

**Functionality:**
- [ ] Feature works as intended
- [ ] No regression of existing features
- [ ] Error handling works correctly
- [ ] Admin privilege checks work

**Compatibility:**
- [ ] Works on target platform(s)
- [ ] Backwards compatible with older Python versions (3.7+)
- [ ] No platform-specific bugs

**Code Quality:**
- [ ] Follows style guidelines
- [ ] No unused imports or variables
- [ ] Functions have docstrings
- [ ] Complex logic is commented

**Documentation:**
- [ ] README.md updated (if needed)
- [ ] CHANGELOG.md updated
- [ ] Code comments added
- [ ] Examples provided

## 📝 Changelog Format

When updating CHANGELOG.md:

```markdown
## [2.1.0] - 2026-02-15

### Added
- Support for Call of Duty: Warzone ports
- MTU auto-detection feature
- Real-time bandwidth graph (Linux only)

### Changed
- Improved DNS testing algorithm (30% faster)
- Updated default DNS server list

### Fixed
- Fixed crash on Ubuntu 20.04 when flushing DNS cache
- Corrected Valorant port numbers
- Fixed Windows batch script admin detection

### Security
- Added input validation for user-provided IPs
```

## 🏆 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Credited in release notes
- Thanked in project documentation

## 📞 Questions?

- Open a [Discussion](https://github.com/yourusername/network-optimizer-pro/discussions)
- Check the [Wiki](https://github.com/yourusername/network-optimizer-pro/wiki)
- Ask in existing [Issues](https://github.com/yourusername/network-optimizer-pro/issues)

## Code of Conduct

### Our Pledge

We pledge to make participation in this project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behavior:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards others

**Unacceptable behavior:**
- Trolling, insulting/derogatory comments
- Public or private harassment
- Publishing others' private information
- Other conduct which could reasonably be considered inappropriate

---

Thank you for contributing to Network Optimizer Pro! 🚀
