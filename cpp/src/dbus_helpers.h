#pragma once

#include <sdbus-c++/sdbus-c++.h>
#include <string>
#include <map>
#include <optional>
#include <variant>
#include <cstdint>

// D-Bus API interfaces and constants
namespace nm {

constexpr const char* BUS_NAME        = "org.freedesktop.NetworkManager";
constexpr const char* OBJ_PATH        = "/org/freedesktop/NetworkManager";

constexpr const char* IFACE           = "org.freedesktop.NetworkManager";
constexpr const char* DEVICE_IFACE    = "org.freedesktop.NetworkManager.Device";
constexpr const char* WIFI_P2P_IFACE  = "org.freedesktop.NetworkManager.Device.WifiP2P";
constexpr const char* WIFI_P2P_PEER_IFACE = "org.freedesktop.NetworkManager.WifiP2PPeer";
constexpr const char* ACTIVE_CONN_IFACE   = "org.freedesktop.NetworkManager.Connection.Active";
constexpr const char* SETTINGS_IFACE      = "org.freedesktop.NetworkManager.Settings";
constexpr const char* SETTINGS_CONN_IFACE = "org.freedesktop.NetworkManager.Settings.Connection";

constexpr const char* DBUS_PROPS_IFACE = "org.freedesktop.DBus.Properties";

// NM Device Types
constexpr uint32_t DEVICE_TYPE_WIFI_P2P = 30;

} // namespace nm

// Type aliases for D-Bus variant maps
using VariantMap = std::map<std::string, sdbus::Variant>;
using ConnectionSettings = std::map<std::string, VariantMap>;

/**
 * Get a single D-Bus property from a NetworkManager object.
 */
sdbus::Variant get_property(const std::string& obj_path,
                            const std::string& iface,
                            const std::string& prop);

/**
 * Get all D-Bus properties from a NetworkManager object.
 */
VariantMap get_all_properties(const std::string& obj_path,
                              const std::string& iface);

/**
 * Find the first Wi-Fi P2P device managed by NetworkManager.
 * Returns the D-Bus object path of the P2P device, or std::nullopt if not found.
 */
std::optional<std::string> find_p2p_device();
