#include "dbus_helpers.h"
#include <iostream>
#include <vector>

sdbus::Variant get_property(const std::string& obj_path,
                            const std::string& iface,
                            const std::string& prop)
{
    auto proxy = sdbus::createProxy(nm::BUS_NAME, sdbus::ObjectPath{obj_path});
    sdbus::Variant result;
    proxy->callMethod("Get")
         .onInterface(nm::DBUS_PROPS_IFACE)
         .withArguments(iface, prop)
         .storeResultsTo(result);
    return result;
}

VariantMap get_all_properties(const std::string& obj_path,
                              const std::string& iface)
{
    auto proxy = sdbus::createProxy(nm::BUS_NAME, sdbus::ObjectPath{obj_path});
    VariantMap result;
    proxy->callMethod("GetAll")
         .onInterface(nm::DBUS_PROPS_IFACE)
         .withArguments(iface)
         .storeResultsTo(result);
    return result;
}

std::optional<std::string> find_p2p_device() {
    auto nm_proxy = sdbus::createProxy(nm::BUS_NAME, sdbus::ObjectPath{nm::OBJ_PATH});

    std::vector<sdbus::ObjectPath> devices;
    nm_proxy->callMethod("GetDevices")
            .onInterface(nm::IFACE)
            .storeResultsTo(devices);

    for (const auto& dev_path : devices) {
        try {
            auto dev_type_var = get_property(dev_path, nm::DEVICE_IFACE, "DeviceType");
            uint32_t dev_type = dev_type_var.get<uint32_t>();

            if (dev_type == nm::DEVICE_TYPE_WIFI_P2P) {
                auto iface_var = get_property(dev_path, nm::DEVICE_IFACE, "Interface");
                std::string iface_name = iface_var.get<std::string>();
                std::cout << "[+] Found Wi-Fi P2P device: " << iface_name
                          << " (" << dev_path << ")" << std::endl;
                return std::string(dev_path);
            }
        } catch (const sdbus::Error& e) {
            // Skip devices that fail property queries
            continue;
        }
    }

    return std::nullopt;
}
