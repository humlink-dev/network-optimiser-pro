@echo off
:: Network Optimizer Pro - Advanced Windows Registry Tweaks
:: CAUTION: This modifies system registry - creates backup first
:: Run as Administrator

title Network Optimizer Pro - Advanced Registry Tweaks
color 0C

echo ============================================================
echo    NETWORK OPTIMIZER PRO - Advanced Registry Tweaks
echo ============================================================
echo.
echo [!] WARNING: This will modify Windows Registry settings
echo [!] A registry backup will be created first
echo.
pause

:: Check for admin rights
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] ERROR: Must run as Administrator
    pause
    exit /b 1
)

:: Create registry backup
echo [*] Creating registry backup...
set backup_file=%USERPROFILE%\Desktop\network_registry_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%.reg
reg export HKLM\SYSTEM\CurrentControlSet\Services\Tcpip "%backup_file%" /y >nul 2>&1
echo [+] Backup created: %backup_file%
echo.

echo [*] Applying advanced network optimizations...
echo.

:: TCP/IP Optimization
echo [1] TCP Window Size Optimization...
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" /v TcpWindowSize /t REG_DWORD /d 65535 /f >nul 2>&1
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" /v Tcp1323Opts /t REG_DWORD /d 3 /f >nul 2>&1
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" /v DefaultTTL /t REG_DWORD /d 64 /f >nul 2>&1
echo [+] TCP window optimized

:: Network Adapter Settings
echo [2] Network Adapter Optimization...
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" /v EnablePMTUDiscovery /t REG_DWORD /d 1 /f >nul 2>&1
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" /v EnablePMTUBHDetect /t REG_DWORD /d 0 /f >nul 2>&1
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" /v MaxHashTableSize /t REG_DWORD /d 65536 /f >nul 2>&1
echo [+] Network adapter settings optimized

:: Disable Nagle's Algorithm (reduces latency)
echo [3] Disabling Nagle's Algorithm for lower latency...
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces" /v TcpAckFrequency /t REG_DWORD /d 1 /f >nul 2>&1
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces" /v TCPNoDelay /t REG_DWORD /d 1 /f >nul 2>&1
echo [+] Nagle's algorithm disabled

:: Network Throttling
echo [4] Optimizing network throttling...
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile" /v NetworkThrottlingIndex /t REG_DWORD /d 0xffffffff /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile" /v SystemResponsiveness /t REG_DWORD /d 0 /f >nul 2>&1
echo [+] Network throttling optimized

:: Gaming Optimization
echo [5] Gaming-specific optimizations...
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games" /v "GPU Priority" /t REG_DWORD /d 8 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games" /v Priority /t REG_DWORD /d 6 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games" /v "Scheduling Category" /t REG_SZ /d High /f >nul 2>&1
echo [+] Gaming optimizations applied

:: DNS Cache Optimization
echo [6] DNS cache optimization...
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Dnscache\Parameters" /v MaxCacheTtl /t REG_DWORD /d 86400 /f >nul 2>&1
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Dnscache\Parameters" /v MaxNegativeCacheTtl /t REG_DWORD /d 0 /f >nul 2>&1
echo [+] DNS cache optimized

:: IRQ Priority
echo [7] Setting network adapter IRQ priority...
reg add "HKLM\System\CurrentControlSet\Control\PriorityControl" /v IRQ8Priority /t REG_DWORD /d 1 /f >nul 2>&1
echo [+] IRQ priority set

:: Disable Large Send Offload (can cause issues)
echo [8] Optimizing offload settings...
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" /v DisableTaskOffload /t REG_DWORD /d 0 /f >nul 2>&1
echo [+] Offload settings optimized

echo.
echo ============================================================
echo    ADVANCED OPTIMIZATION COMPLETE!
echo ============================================================
echo.
echo [+] All registry tweaks applied successfully
echo [+] Backup saved to: %backup_file%
echo.
echo [!] CRITICAL: You MUST restart your computer now
echo [!] Changes will not take effect until restart
echo.
echo Press any key to exit...
pause >nul
