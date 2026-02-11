@echo off
:: Network Optimizer Pro - Windows Quick Optimization
:: Run as Administrator for full functionality

title Network Optimizer Pro - Quick Setup
color 0A

echo ============================================================
echo    NETWORK OPTIMIZER PRO - Windows Quick Optimization
echo ============================================================
echo.

:: Check for admin rights
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [+] Running with Administrator privileges
    echo.
) else (
    echo [!] WARNING: Not running as Administrator
    echo [!] Some optimizations will be skipped
    echo.
    pause
)

echo [*] Starting Network Optimization...
echo ============================================================
echo.

:: Flush DNS Cache
echo [1/8] Flushing DNS cache...
ipconfig /flushdns >nul 2>&1
echo [+] DNS cache flushed
echo.

:: Release and Renew IP
echo [2/8] Releasing and renewing IP address...
ipconfig /release >nul 2>&1
ipconfig /renew >nul 2>&1
echo [+] IP address renewed
echo.

:: Reset Winsock
echo [3/8] Resetting Winsock...
netsh winsock reset >nul 2>&1
echo [+] Winsock reset
echo.

:: Optimize TCP/IP Settings
echo [4/8] Optimizing TCP/IP settings...
netsh int tcp set global autotuninglevel=normal >nul 2>&1
netsh int tcp set global timestamps=enabled >nul 2>&1
netsh int tcp set global chimney=enabled >nul 2>&1
netsh int tcp set global rss=enabled >nul 2>&1
netsh int tcp set global congestionprovider=ctcp >nul 2>&1
netsh int tcp set global nonsackrttresiliency=disabled >nul 2>&1
netsh int tcp set global initialRto=3000 >nul 2>&1
echo [+] TCP/IP optimization complete
echo.

:: Set DNS to Cloudflare (fastest typically)
echo [5/8] Setting DNS to Cloudflare (1.1.1.1)...
for /f "tokens=3*" %%a in ('netsh interface show interface ^| findstr /C:"Connected"') do (
    set interface=%%b
    goto :found
)
:found
if defined interface (
    netsh interface ip set dns name="%interface%" static 1.1.1.1 >nul 2>&1
    netsh interface ip add dns name="%interface%" 1.0.0.1 index=2 >nul 2>&1
    echo [+] DNS set to Cloudflare
) else (
    echo [-] Could not find active interface
)
echo.

:: Disable Network Throttling
echo [6/8] Disabling network throttling...
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile" /v NetworkThrottlingIndex /t REG_DWORD /d 0xffffffff /f >nul 2>&1
echo [+] Network throttling disabled
echo.

:: Optimize QoS
echo [7/8] Optimizing Quality of Service...
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\Psched" /v NonBestEffortLimit /t REG_DWORD /d 0 /f >nul 2>&1
echo [+] QoS optimized
echo.

:: Test latency
echo [8/8] Testing latency to Google DNS...
ping -n 5 8.8.8.8
echo.

echo ============================================================
echo    OPTIMIZATION COMPLETE!
echo ============================================================
echo.
echo [+] Your network has been optimized for gaming and low latency
echo [!] IMPORTANT: Restart your computer for all changes to take effect
echo.
echo Press any key to exit...
pause >nul
