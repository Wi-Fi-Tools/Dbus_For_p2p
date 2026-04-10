#include "p2p_discovery.h"
#include <iostream>
#include <algorithm>
#include <cctype>
#include <glib.h>

// Helper: case-insensitive string comparison
static std::string to_lower(const std::string& s) {
    std::string result = s;
    std::transform(result.begin(), result.end(), result.begin(),
                   [](unsigned char c) { return std::tolower(c); });
    return result;
}

P2PDiscovery::P2PDiscovery(sdbus::IConnection& bus,
                           const std::string& p2p_dev_path,
                           const std::string& target_peer_address,
                           int timeout)
    : bus_(bus)
    , p2p_dev_path_(p2p_dev_path)
    , target_peer_address_(target_peer_address)
    , timeout_(timeout)
{
}

PeerInfo P2PDiscovery::get_peer_info(const std::string& peer_path)
{
    PeerInfo info;
    info.path = peer_path;

    try {
        auto props = get_all_properties(bus_, peer_path, nm::WIFI_P2P_PEER_IFACE);

        if (props.count("Name")) {
            info.name = props["Name"].get<std::string>();
        }
        if (props.count("HwAddress")) {
            info.hw_address = props["HwAddress"].get<std::string>();
        }
    } catch (const sdbus::Error& e) {
        std::cerr << "  [WARN] Failed to get peer info for " << peer_path
                  << ": " << e.what() << std::endl;
    }

    return info;
}

void P2PDiscovery::on_peer_added(const sdbus::ObjectPath& peer_path)
{
    auto info = get_peer_info(std::string(peer_path));
    peers_[std::string(peer_path)] = info;

    std::cout << "  [FOUND] Peer: " << (info.name.empty() ? "Unknown" : info.name) << std::endl;
    std::cout << "          HwAddress: " << (info.hw_address.empty() ? "N/A" : info.hw_address) << std::endl;
    std::cout << "          Path: " << peer_path << std::endl;
    std::cout << std::endl;

    if (to_lower(info.hw_address) == to_lower(target_peer_address_)) {
        std::cout << "[*] Target peer " << target_peer_address_
                  << " found! Stopping discovery." << std::endl;
        target_found_ = true;
        target_info_ = info;
        if (loop_ && g_main_loop_is_running(loop_)) {
            g_main_loop_quit(loop_);
        }
    }
}

void P2PDiscovery::on_peer_removed(const sdbus::ObjectPath& peer_path)
{
    auto it = peers_.find(std::string(peer_path));
    std::string name = "Unknown";
    if (it != peers_.end()) {
        name = it->second.name.empty() ? "Unknown" : it->second.name;
        peers_.erase(it);
    }
    std::cout << "  [LOST]  Peer: " << name << " (" << peer_path << ")" << std::endl;
}

std::map<std::string, PeerInfo> P2PDiscovery::start_discovery()
{
    std::cout << "\n[*] Starting P2P peer discovery (timeout: " << timeout_ << "s)..." << std::endl;
    std::cout << std::string(60, '-') << std::endl;

    // Create proxy for the P2P device to register signals and call methods
    signal_proxy_ = sdbus::createProxy(bus_, sdbus::ServiceName{nm::BUS_NAME},
                                       sdbus::ObjectPath{p2p_dev_path_});

    // Subscribe to PeerAdded signal
    signal_proxy_->registerSignalHandler(
        sdbus::InterfaceName{nm::WIFI_P2P_IFACE},
        sdbus::SignalName{"PeerAdded"},
        [this](sdbus::Signal& signal) {
            sdbus::ObjectPath peer_path;
            signal >> peer_path;
            this->on_peer_added(peer_path);
        }
    );

    // Subscribe to PeerRemoved signal
    signal_proxy_->registerSignalHandler(
        sdbus::InterfaceName{nm::WIFI_P2P_IFACE},
        sdbus::SignalName{"PeerRemoved"},
        [this](sdbus::Signal& signal) {
            sdbus::ObjectPath peer_path;
            signal >> peer_path;
            this->on_peer_removed(peer_path);
        }
    );

    signal_proxy_->finishRegistration();

    // Check already-known peers
    try {
        auto peers_var = get_property(bus_, p2p_dev_path_, nm::WIFI_P2P_IFACE, "Peers");
        auto existing_peers = peers_var.get<std::vector<sdbus::ObjectPath>>();
        for (const auto& peer_path : existing_peers) {
            on_peer_added(peer_path);
        }
    } catch (const sdbus::Error&) {
        // Ignore errors when querying existing peers
    }

    // Start the P2P find operation
    // StartFind accepts a dictionary of options:
    //   timeout: discovery timeout in seconds (0 = no timeout, NM manages it)
    std::map<std::string, sdbus::Variant> options;
    options["timeout"] = sdbus::Variant{static_cast<int32_t>(timeout_)};

    try {
        signal_proxy_->callMethod("StartFind")
                      .onInterface(nm::WIFI_P2P_IFACE)
                      .withArguments(options);
        std::cout << "[*] P2P Find started on " << p2p_dev_path_ << std::endl;
    } catch (const sdbus::Error& e) {
        std::cerr << "[!] Failed to start P2P Find: " << e.what() << std::endl;
        std::cerr << "[!] Make sure:" << std::endl;
        std::cerr << "    1. You are running as root (sudo)" << std::endl;
        std::cerr << "    2. Your Wi-Fi adapter supports P2P" << std::endl;
        std::cerr << "    3. NetworkManager is running and manages the device" << std::endl;
        return {};
    }

    // Run the GLib main loop with a timeout
    loop_ = g_main_loop_new(nullptr, FALSE);

    // Add timeout to stop the loop
    g_timeout_add_seconds(timeout_, [](gpointer data) -> gboolean {
        auto* loop = static_cast<GMainLoop*>(data);
        if (g_main_loop_is_running(loop)) {
            g_main_loop_quit(loop);
        }
        return FALSE; // Don't repeat
    }, loop_);

    // We need to integrate sdbus event loop with GLib.
    // sdbus-c++ processes events on its own connection thread by default,
    // so signals will be delivered. We just need GLib for the timeout.
    g_main_loop_run(loop_);
    g_main_loop_unref(loop_);
    loop_ = nullptr;

    // Stop discovery
    try {
        signal_proxy_->callMethod("StopFind")
                      .onInterface(nm::WIFI_P2P_IFACE);
        std::cout << "[*] P2P Find stopped." << std::endl;
    } catch (const sdbus::Error&) {
        // Ignore
    }

    std::cout << std::string(60, '-') << std::endl;
    std::cout << "[*] Discovery complete. Found " << peers_.size() << " peer(s).\n" << std::endl;
    return peers_;
}
