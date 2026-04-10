#include "dbus_helpers.h"
#include "p2p_discovery.h"
#include "p2p_connection.h"

#include <iostream>
#include <csignal>
#include <glib.h>

static GMainLoop* g_loop = nullptr;

static void signal_handler(int signum)
{
    std::cout << "\n[*] Exiting..." << std::endl;
    if (g_loop && g_main_loop_is_running(g_loop)) {
        g_main_loop_quit(g_loop);
    }
}

int main(int argc, char* argv[])
{
    const std::string target_peer_address = "62:4B:7C:9E:06:7E";

    // // Create system bus connection
    // std::unique_ptr<sdbus::IConnection> conn;
    // try {
    //     conn = sdbus::createSystemBusConnection();
    // } catch (const sdbus::Error& e) {
    //     std::cerr << "[-] Failed to connect to system D-Bus: " << e.what() << std::endl;
    //     return 1;
    // }

    // // Enter the event loop on a separate thread so signals are processed
    // conn->enterEventLoopAsync();

    // Find P2P device
    auto p2p_dev_path = find_p2p_device();
    if (!p2p_dev_path) {
        std::cerr << "[-] No Wi-Fi P2P device found. "
                  << "Ensure your hardware supports P2P and is enabled." << std::endl;
        return 1;
    }
    std::cout << "[+] Using P2P device at " << *p2p_dev_path << std::endl;

    // Start peer discovery
    P2PDiscovery discovery(*p2p_dev_path, target_peer_address);
    auto peers = discovery.start_discovery();

    if (peers.empty()) {
        std::cerr << "[-] No peers found." << std::endl;
        return 1;
    }

    if (!discovery.is_target_found()) {
        std::cerr << "[-] Target peer " << target_peer_address << " was not found." << std::endl;
        return 1;
    }

    auto target_info = discovery.get_target_info();
    if (target_info) {
        std::cout << "[+] Target peer info:" << std::endl;
        std::cout << "    Name: " << (target_info->name.empty() ? "Unknown" : target_info->name) << std::endl;
        std::cout << "    HwAddress: " << (target_info->hw_address.empty() ? "N/A" : target_info->hw_address) << std::endl;
        std::cout << "    Path: " << target_info->path << std::endl;
        create_p2p_connection(*p2p_dev_path, *target_info);
    }

    // // Keep running until interrupted
    std::signal(SIGINT, signal_handler);
    std::signal(SIGTERM, signal_handler);

    g_loop = g_main_loop_new(nullptr, FALSE);
    std::cout << "[*] Running... Press Ctrl+C to exit." << std::endl;
    g_main_loop_run(g_loop);
    g_main_loop_unref(g_loop);
    g_loop = nullptr;

    return 0;
}
