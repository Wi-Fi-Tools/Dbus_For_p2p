#pragma once

#include "dbus_helpers.h"
#include <string>
#include <map>
#include <optional>
#include <functional>
#include <atomic>
#include <memory>
#include <glib.h>

/**
 * Peer information structure.
 */
struct PeerInfo {
    std::string name;
    std::string hw_address;
    std::string path;
};

/**
 * Handles Wi-Fi P2P peer discovery using NetworkManager D-Bus API.
 */
class P2PDiscovery {
public:
    P2PDiscovery(const std::string& p2p_dev_path,
                 const std::string& target_peer_address,
                 int timeout = 15);

    ~P2PDiscovery() = default;

    /**
     * Start P2P peer discovery.
     *
     * This method:
     * 1. Subscribes to PeerAdded/PeerRemoved signals
     * 2. Calls StartFind() on the P2P device
     * 3. Runs the GLib main loop for the specified timeout
     * 4. Calls StopFind() and returns discovered peers
     *
     * Returns: map of discovered peers (path -> PeerInfo).
     */
    std::map<std::string, PeerInfo> start_discovery();

    bool is_target_found() const { return target_found_; }
    std::optional<PeerInfo> get_target_info() const { return target_info_; }

private:
    void on_peer_added(const sdbus::ObjectPath& peer_path);
    void on_peer_removed(const sdbus::ObjectPath& peer_path);
    PeerInfo get_peer_info(const std::string& peer_path);
    
    std::string p2p_dev_path_;
    std::string target_peer_address_;
    int timeout_;

    std::atomic<bool> target_found_{false};
    std::optional<PeerInfo> target_info_;
    std::map<std::string, PeerInfo> peers_;

    GMainLoop* loop_{nullptr};
    std::unique_ptr<sdbus::IProxy> signal_proxy_;
};
