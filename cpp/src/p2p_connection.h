#pragma once

#include "dbus_helpers.h"
#include "p2p_discovery.h"
#include <string>
#include <optional>

/**
 * Create a Wi-Fi P2P connection profile and activate it to form a P2P Group.
 *
 * This is the equivalent of:
 *     nmcli connection add type wifi-p2p con-name <name> wifi-p2p.peer <mac>
 *     nmcli connection up <name>
 *
 * @param p2p_dev_path  Object path of the P2P device.
 * @param peer_info  Information about the target peer.
 * @param con_name   Connection profile name.
 * @return The object path of the active connection, or std::nullopt on failure.
 */
std::optional<std::string> create_p2p_connection(
    const std::string& p2p_dev_path,
    const PeerInfo& peer_info,
    const std::string& con_name = "wifi-p2p-connection");
