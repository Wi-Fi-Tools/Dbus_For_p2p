#include "p2p_connection.h"
#include <iostream>

// Type for NM AddAndActivateConnection settings:
// a{sa{sv}} -> map<string, map<string, Variant>>
using NMConnectionSettings = std::map<std::string, std::map<std::string, sdbus::Variant>>;

std::optional<std::string> create_p2p_connection(
    sdbus::IConnection& conn,
    const std::string& p2p_dev_path,
    const PeerInfo& peer_info,
    const std::string& con_name)
{
    const auto& peer_path = peer_info.path;
    const auto& peer_hw = peer_info.hw_address.empty() ? "Unknown" : peer_info.hw_address;
    const auto& peer_name = peer_info.name.empty() ? "Unknown" : peer_info.name;

    std::cout << "[*] Connecting to peer: " << peer_name << " (" << peer_hw << ")" << std::endl;

    // Build the connection settings dictionary
    // Reference: https://networkmanager.dev/docs/api/latest/ref-settings.html
    NMConnectionSettings settings;

    // [connection] section
    settings["connection"]["id"] = sdbus::Variant{con_name};
    settings["connection"]["type"] = sdbus::Variant{std::string("wifi-p2p")};
    settings["connection"]["autoconnect"] = sdbus::Variant{false};

    // [wifi-p2p] section
    settings["wifi-p2p"]["peer"] = sdbus::Variant{peer_hw};

    // [ipv4] section - use automatic (DHCP)
    settings["ipv4"]["method"] = sdbus::Variant{std::string("auto")};

    // [ipv6] section
    settings["ipv6"]["method"] = sdbus::Variant{std::string("auto")};

    // Call AddAndActivateConnection
    // This creates the connection profile AND activates it in one step
    auto nm_proxy = sdbus::createProxy(conn, sdbus::ServiceName{nm::BUS_NAME},
                                       sdbus::ObjectPath{nm::OBJ_PATH});

    try {
        std::cout << "[*] Calling AddAndActivateConnection..." << std::endl;

        sdbus::ObjectPath settings_path;
        sdbus::ObjectPath active_conn_path;

        nm_proxy->callMethod("AddAndActivateConnection")
                .onInterface(nm::IFACE)
                .withArguments(settings,
                               sdbus::ObjectPath{p2p_dev_path},
                               sdbus::ObjectPath{peer_path})
                .storeResultsTo(settings_path, active_conn_path);

        std::cout << "[+] Connection profile created: " << settings_path << std::endl;
        std::cout << "[+] Active connection: " << active_conn_path << std::endl;

        return std::string(active_conn_path);

    } catch (const sdbus::Error& e) {
        std::cerr << "[!] Failed to create P2P connection: " << e.what() << std::endl;
        return std::nullopt;
    }
}
