#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include <thread>
#include <cstring>
#include <algorithm>

#ifdef _WIN32
    #include <winsock2.h>
    #include <ws2tcpip.h>
    #include <iphlpapi.h>
    #pragma comment(lib, "ws2_32.lib")
    #pragma comment(lib, "iphlpapi.lib")
#else
    #include <sys/socket.h>
    #include <netinet/in.h>
    #include <arpa/inet.h>
    #include <netdb.h>
    #include <unistd.h>
    #include <ifaddrs.h>
    #include <net/if.h>
#endif

class NetworkMonitor {
private:
    struct PingResult {
        std::string host;
        double latency_ms;
        bool success;
    };
    
    struct DNSServer {
        std::string name;
        std::string ip;
        double latency_ms;
    };

public:
    NetworkMonitor() {
        #ifdef _WIN32
        WSADATA wsaData;
        WSAStartup(MAKEWORD(2, 2), &wsaData);
        #endif
    }
    
    ~NetworkMonitor() {
        #ifdef _WIN32
        WSACleanup();
        #endif
    }
    
    void printBanner() {
        std::cout << "============================================================\n";
        std::cout << "     NETWORK MONITOR PRO - C++ High-Performance Edition\n";
        std::cout << "============================================================\n\n";
    }
    
    double pingHost(const std::string& host, int timeout_ms = 2000) {
        auto start = std::chrono::high_resolution_clock::now();
        
        struct addrinfo hints, *result;
        memset(&hints, 0, sizeof(hints));
        hints.ai_family = AF_INET;
        hints.ai_socktype = SOCK_STREAM;
        
        if (getaddrinfo(host.c_str(), "80", &hints, &result) != 0) {
            return -1.0;
        }
        
        int sock = socket(result->ai_family, result->ai_socktype, result->ai_protocol);
        if (sock < 0) {
            freeaddrinfo(result);
            return -1.0;
        }
        
        // Set timeout
        #ifdef _WIN32
        DWORD timeout = timeout_ms;
        setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, (const char*)&timeout, sizeof(timeout));
        setsockopt(sock, SOL_SOCKET, SO_SNDTIMEO, (const char*)&timeout, sizeof(timeout));
        #else
        struct timeval tv;
        tv.tv_sec = timeout_ms / 1000;
        tv.tv_usec = (timeout_ms % 1000) * 1000;
        setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv));
        setsockopt(sock, SOL_SOCKET, SO_SNDTIMEO, &tv, sizeof(tv));
        #endif
        
        int conn_result = connect(sock, result->ai_addr, result->ai_addrlen);
        
        auto end = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double, std::milli> duration = end - start;
        
        #ifdef _WIN32
        closesocket(sock);
        #else
        close(sock);
        #endif
        freeaddrinfo(result);
        
        if (conn_result < 0) {
            return -1.0;
        }
        
        return duration.count();
    }
    
    std::vector<DNSServer> testDNSServers() {
        std::vector<DNSServer> dns_servers = {
            {"Cloudflare", "1.1.1.1", 0.0},
            {"Google", "8.8.8.8", 0.0},
            {"Quad9", "9.9.9.9", 0.0},
            {"OpenDNS", "208.67.222.222", 0.0},
            {"AdGuard", "94.140.14.14", 0.0}
        };
        
        std::cout << "[*] Testing DNS servers...\n";
        std::cout << "------------------------------------------------------------\n";
        
        for (auto& dns : dns_servers) {
            double latency = pingHost(dns.ip, 2000);
            dns.latency_ms = (latency > 0) ? latency : 9999.0;
            std::cout << "    " << dns.name << " (" << dns.ip << "): " 
                      << dns.latency_ms << " ms\n";
        }
        
        // Sort by latency
        std::sort(dns_servers.begin(), dns_servers.end(), 
                  [](const DNSServer& a, const DNSServer& b) {
                      return a.latency_ms < b.latency_ms;
                  });
        
        std::cout << "\n[+] Fastest DNS: " << dns_servers[0].name 
                  << " (" << dns_servers[0].latency_ms << " ms)\n";
        
        return dns_servers;
    }
    
    void continuousLatencyMonitor(const std::string& host, int duration_seconds = 60) {
        std::cout << "\n[*] Starting continuous latency monitor for " << duration_seconds << "s\n";
        std::cout << "[*] Target: " << host << "\n";
        std::cout << "------------------------------------------------------------\n";
        
        double min_latency = 9999.0;
        double max_latency = 0.0;
        double total_latency = 0.0;
        int successful_pings = 0;
        int failed_pings = 0;
        
        auto start_time = std::chrono::steady_clock::now();
        
        while (true) {
            auto current_time = std::chrono::steady_clock::now();
            auto elapsed = std::chrono::duration_cast<std::chrono::seconds>(
                current_time - start_time).count();
            
            if (elapsed >= duration_seconds) {
                break;
            }
            
            double latency = pingHost(host, 2000);
            
            if (latency > 0) {
                successful_pings++;
                total_latency += latency;
                min_latency = std::min(min_latency, latency);
                max_latency = std::max(max_latency, latency);
                
                std::cout << "[" << elapsed << "s] Latency: " << latency << " ms    \r" << std::flush;
            } else {
                failed_pings++;
                std::cout << "[" << elapsed << "s] TIMEOUT                    \r" << std::flush;
            }
            
            std::this_thread::sleep_for(std::chrono::seconds(1));
        }
        
        std::cout << "\n\n[*] Monitoring Complete\n";
        std::cout << "------------------------------------------------------------\n";
        std::cout << "Total Pings:    " << (successful_pings + failed_pings) << "\n";
        std::cout << "Successful:     " << successful_pings << "\n";
        std::cout << "Failed:         " << failed_pings << "\n";
        
        if (successful_pings > 0) {
            double avg_latency = total_latency / successful_pings;
            std::cout << "Min Latency:    " << min_latency << " ms\n";
            std::cout << "Avg Latency:    " << avg_latency << " ms\n";
            std::cout << "Max Latency:    " << max_latency << " ms\n";
            std::cout << "Packet Loss:    " << (failed_pings * 100.0 / (successful_pings + failed_pings)) << "%\n";
        }
    }
    
    void performanceTest(const std::vector<std::string>& hosts) {
        std::cout << "\n[*] Running performance test to multiple hosts...\n";
        std::cout << "------------------------------------------------------------\n";
        
        for (const auto& host : hosts) {
            std::cout << "\nTesting " << host << "...\n";
            
            double total = 0.0;
            int successful = 0;
            
            for (int i = 0; i < 5; i++) {
                double latency = pingHost(host, 2000);
                if (latency > 0) {
                    total += latency;
                    successful++;
                    std::cout << "  Attempt " << (i+1) << ": " << latency << " ms\n";
                } else {
                    std::cout << "  Attempt " << (i+1) << ": TIMEOUT\n";
                }
                std::this_thread::sleep_for(std::chrono::milliseconds(100));
            }
            
            if (successful > 0) {
                std::cout << "  Average: " << (total / successful) << " ms\n";
            }
        }
    }
    
    void showMenu() {
        while (true) {
            std::cout << "\n============================================================\n";
            std::cout << "  NETWORK MONITOR PRO - MENU\n";
            std::cout << "============================================================\n";
            std::cout << "1. Test DNS Servers\n";
            std::cout << "2. Continuous Latency Monitor (60s)\n";
            std::cout << "3. Multi-Host Performance Test\n";
            std::cout << "4. Quick Ping Test\n";
            std::cout << "5. Exit\n";
            std::cout << "============================================================\n";
            std::cout << "\nSelect option (1-5): ";
            
            int choice;
            std::cin >> choice;
            
            switch (choice) {
                case 1:
                    testDNSServers();
                    break;
                case 2: {
                    std::string host;
                    std::cout << "Enter host (default: 8.8.8.8): ";
                    std::cin.ignore();
                    std::getline(std::cin, host);
                    if (host.empty()) host = "8.8.8.8";
                    continuousLatencyMonitor(host, 60);
                    break;
                }
                case 3: {
                    std::vector<std::string> hosts = {
                        "google.com", "cloudflare.com", "amazon.com", "microsoft.com"
                    };
                    performanceTest(hosts);
                    break;
                }
                case 4: {
                    std::string host;
                    std::cout << "Enter host: ";
                    std::cin.ignore();
                    std::getline(std::cin, host);
                    double latency = pingHost(host, 2000);
                    if (latency > 0) {
                        std::cout << "[+] Latency to " << host << ": " << latency << " ms\n";
                    } else {
                        std::cout << "[-] Failed to reach " << host << "\n";
                    }
                    break;
                }
                case 5:
                    std::cout << "\n[+] Thanks for using Network Monitor Pro!\n";
                    return;
                default:
                    std::cout << "[-] Invalid option\n";
            }
        }
    }
};

int main(int argc, char* argv[]) {
    NetworkMonitor monitor;
    monitor.printBanner();
    
    if (argc > 1) {
        std::string arg = argv[1];
        if (arg == "--dns") {
            monitor.testDNSServers();
        } else if (arg == "--monitor") {
            std::string host = (argc > 2) ? argv[2] : "8.8.8.8";
            monitor.continuousLatencyMonitor(host, 60);
        } else {
            std::cout << "Usage: " << argv[0] << " [--dns|--monitor [host]]\n";
        }
    } else {
        monitor.showMenu();
    }
    
    return 0;
}
