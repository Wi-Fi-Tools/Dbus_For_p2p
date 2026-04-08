#!/usr/bin/env python3
"""
Wi-Fi P2P (Wi-Fi Direct) Discovery and Group Establishment Demo
using NetworkManager D-Bus API.

Requirements:
    - Python 3.6+
    - dbus-python (system package: python3-dbus)
    - PyGObject (system package: python3-gi)
    - NetworkManager >= 1.16 (with P2P support)

Install dependencies (Debian/Ubuntu):
    sudo apt install python3-dbus python3-gi gir1.2-nm-1.0

Usage:
    sudo python3 p2p_discovery.py              # Discover peers
    sudo python3 p2p_discovery.py --connect     # Discover and connect to first peer
    sudo python3 p2p_discovery.py --timeout 30  # Set discovery timeout (default: 15s)
"""

import sys
import time
import argparse
import signal
from typing import Optional, List, Dict, Any

import dbus
import dbus.mainloop.glib
from gi.repository import GLib


# ============================================================
# Constants
# ============================================================

NM_BUS_NAME = "org.freedesktop.NetworkManager"
NM_OBJ_PATH = "/org/freedesktop/NetworkManager"

NM_IFACE = "org.freedesktop.NetworkManager"
NM_DEVICE_IFACE = "org.freedesktop.NetworkManager.Device"
NM_WIFI_P2P_IFACE = "org.freedesktop.NetworkManager.Device.WifiP2P"
NM_WIFI_P2P_PEER_IFACE = "org.freedesktop.NetworkManager.WifiP2PPeer"
NM_ACTIVE_CONN_IFACE = "org.freedesktop.NetworkManager.Connection.Active"
NM_SETTINGS_IFACE = "org.freedesktop.NetworkManager.Settings"
NM_SETTINGS_CONN_IFACE = "org.freedesktop.NetworkManager.Settings.Connection"

DBUS_PROPS_IFACE = "org.freedesktop.DBus.Properties"

# NM Device Types
NM_DEVICE_TYPE_WIFI_P2P = 30


# ============================================================
# Helper Functions
# ============================================================

def get_system_bus() -> dbus.SystemBus:
    """Get the D-Bus system bus with GLib main loop integration."""
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    return dbus.SystemBus()


def get_nm_proxy(bus: dbus.SystemBus) -> dbus.Interface:
    """Get the NetworkManager D-Bus proxy."""
    proxy = bus.get_object(NM_BUS_NAME, NM_OBJ_PATH)
    return dbus.Interface(proxy, NM_IFACE)


def get_property(bus: dbus.SystemBus, obj_path: str, iface: str, prop: str) -> Any:
    """Get a single D-Bus property from an object."""
    proxy = bus.get_object(NM_BUS_NAME, obj_path)
    props = dbus.Interface(proxy, DBUS_PROPS_IFACE)
    return props.Get(iface, prop)


def get_all_properties(bus: dbus.SystemBus, obj_path: str, iface: str) -> Dict[str, Any]:
    """Get all D-Bus properties from an object."""
    proxy = bus.get_object(NM_BUS_NAME, obj_path)
    props = dbus.Interface(proxy, DBUS_PROPS_IFACE)
    return props.GetAll(iface)


# ============================================================
# P2P Device Discovery
# ============================================================

def find_p2p_device(bus: dbus.SystemBus) -> Optional[str]:
    """
    Find the first Wi-Fi P2P device managed by NetworkManager.

    Returns:
        The D-Bus object path of the P2P device, or None if not found.
    """
    nm = get_nm_proxy(bus)
    devices = nm.GetDevices()

    for dev_path in devices:
        dev_type = get_property(bus, dev_path, NM_DEVICE_IFACE, "DeviceType")
        if dev_type == NM_DEVICE_TYPE_WIFI_P2P:
            iface_name = get_property(bus, dev_path, NM_DEVICE_IFACE, "Interface")
            print(f"[+] Found Wi-Fi P2P device: {iface_name} ({dev_path})")
            return str(dev_path)

    return None


def find_p2p_device_from_wifi(bus: dbus.SystemBus) -> Optional[str]:
    """
    Alternative: Find P2P device by looking at Wi-Fi device's P2PDevice property.
    Some NM versions expose P2P as a companion device of the Wi-Fi adapter.

    Returns:
        The D-Bus object path of the P2P device, or None if not found.
    """
    nm = get_nm_proxy(bus)
    devices = nm.GetDevices()

    NM_DEVICE_TYPE_WIFI = 2
    NM_WIFI_IFACE = "org.freedesktop.NetworkManager.Device.Wireless"

    for dev_path in devices:
        dev_type = get_property(bus, dev_path, NM_DEVICE_IFACE, "DeviceType")
        if dev_type == NM_DEVICE_TYPE_WIFI:
            try:
                # Some NM versions have a P2PDevice property on the Wi-Fi device
                # that points to the companion P2P device
                p2p_path = get_property(bus, dev_path, NM_WIFI_IFACE, "P2PDevice")
                if p2p_path and str(p2p_path) != "/":
                    iface_name = get_property(bus, dev_path, NM_DEVICE_IFACE, "Interface")
                    print(f"[+] Found P2P companion device for Wi-Fi: {iface_name}")
                    return str(p2p_path)
            except dbus.exceptions.DBusException:
                continue

    return None


# ============================================================
# Peer Discovery
# ============================================================

class P2PDiscovery:
    """Handles Wi-Fi P2P peer discovery using NetworkManager D-Bus API."""

    def __init__(self, bus: dbus.SystemBus, p2p_dev_path: str, timeout: int = 15):
        self.bus = bus
        self.p2p_dev_path = p2p_dev_path
        self.timeout = timeout
        self.peers: Dict[str, Dict[str, Any]] = {}
        self.loop: Optional[GLib.MainLoop] = None
        self._signal_match = None

    def _on_peer_added(self, peer_path: str):
        """Signal handler: called when a new P2P peer is discovered."""
        # Defer property retrieval to avoid race condition:
        # When PeerAdded signal fires, the peer object may not have
        # its properties (HWAddress, Name, etc.) fully populated yet.
        GLib.timeout_add(500, self._fetch_and_print_peer, str(peer_path))

    def _fetch_and_print_peer(self, peer_path: str, retry_count: int = 0) -> bool:
        """Fetch peer properties and print them. Retries if HWAddress is empty."""
        MAX_RETRIES = 3
        peer_info = self._get_peer_info(peer_path)

        # If HWAddress is still empty and we haven't exhausted retries, try again
        if not peer_info.get("HWAddress") and retry_count < MAX_RETRIES:
            GLib.timeout_add(500, self._fetch_and_print_peer, peer_path, retry_count + 1)
            return False  # Don't repeat this timeout

        self.peers[str(peer_path)] = peer_info
        print(f"  [FOUND] Peer: {peer_info.get('Name', 'Unknown')}")
        print(f"          HWAddress: {peer_info.get('HWAddress', 'N/A')}")
        print(f"          Manufacturer: {peer_info.get('Manufacturer', 'N/A')}")
        print(f"          Model: {peer_info.get('Model', 'N/A')}")
        print(f"          Path: {peer_path}")
        print()
        return False  # Don't repeat this timeout

    def _on_peer_removed(self, peer_path: str):
        """Signal handler: called when a P2P peer is lost."""
        peer_info = self.peers.pop(str(peer_path), {})
        name = peer_info.get("Name", "Unknown")
        print(f"  [LOST]  Peer: {name} ({peer_path})")

    def _get_peer_info(self, peer_path: str) -> Dict[str, Any]:
        """Retrieve detailed information about a discovered P2P peer."""
        try:
            props = get_all_properties(self.bus, peer_path, NM_WIFI_P2P_PEER_IFACE)
            return {
                "Name": str(props.get("Name", "")),
                "HWAddress": str(props.get("HWAddress", "")),
                "Manufacturer": str(props.get("Manufacturer", "")),
                "Model": str(props.get("Model", "")),
                "ModelNumber": str(props.get("ModelNumber", "")),
                "Serial": str(props.get("Serial", "")),
                "Flags": int(props.get("Flags", 0)),
                "WfdIEs": props.get("WfdIEs", None),
                "Path": str(peer_path),
            }
        except dbus.exceptions.DBusException as e:
            print(f"  [WARN] Failed to get peer info for {peer_path}: {e}")
            return {"Path": str(peer_path)}

    def start_discovery(self) -> Dict[str, Dict[str, Any]]:
        """
        Start P2P peer discovery.

        This method:
        1. Subscribes to PeerAdded/PeerRemoved signals
        2. Calls StartFind() on the P2P device
        3. Runs the GLib main loop for the specified timeout
        4. Calls StopFind() and returns discovered peers

        Returns:
            Dictionary of discovered peers (path -> info).
        """
        print(f"\n[*] Starting P2P peer discovery (timeout: {self.timeout}s)...")
        print("-" * 60)

        # Get the P2P device proxy
        p2p_proxy = self.bus.get_object(NM_BUS_NAME, self.p2p_dev_path)
        p2p_iface = dbus.Interface(p2p_proxy, NM_WIFI_P2P_IFACE)

        # Subscribe to peer discovery signals
        self.bus.add_signal_receiver(
            self._on_peer_added,
            signal_name="PeerAdded",
            dbus_interface=NM_WIFI_P2P_IFACE,
            bus_name=NM_BUS_NAME,
            path=self.p2p_dev_path,
        )
        self.bus.add_signal_receiver(
            self._on_peer_removed,
            signal_name="PeerRemoved",
            dbus_interface=NM_WIFI_P2P_IFACE,
            bus_name=NM_BUS_NAME,
            path=self.p2p_dev_path,
        )

        # Also check already-known peers
        try:
            existing_peers = get_property(
                self.bus, self.p2p_dev_path, NM_WIFI_P2P_IFACE, "Peers"
            )
            for peer_path in existing_peers:
                self._on_peer_added(str(peer_path))
        except dbus.exceptions.DBusException:
            pass

        # Start the P2P find operation
        # StartFind accepts a dictionary of options:
        #   timeout: discovery timeout in seconds (0 = no timeout, NM manages it)
        options = dbus.Dictionary(
            {"timeout": dbus.Int32(self.timeout)},
            signature="sv"
        )

        try:
            p2p_iface.StartFind(options)
            print(f"[*] P2P Find started on {self.p2p_dev_path}")
        except dbus.exceptions.DBusException as e:
            print(f"[!] Failed to start P2P Find: {e}")
            print("[!] Make sure:")
            print("    1. You are running as root (sudo)")
            print("    2. Your Wi-Fi adapter supports P2P")
            print("    3. NetworkManager is running and manages the device")
            return {}

        # Run the main loop with a timeout
        self.loop = GLib.MainLoop()
        GLib.timeout_add_seconds(self.timeout, self._stop_loop)

        try:
            self.loop.run()
        except KeyboardInterrupt:
            print("\n[*] Discovery interrupted by user.")

        # Stop discovery
        try:
            p2p_iface.StopFind()
            print("[*] P2P Find stopped.")
        except dbus.exceptions.DBusException:
            pass

        print("-" * 60)
        print(f"[*] Discovery complete. Found {len(self.peers)} peer(s).\n")
        return self.peers

    def _stop_loop(self) -> bool:
        """GLib timeout callback to stop the main loop."""
        if self.loop and self.loop.is_running():
            self.loop.quit()
        return False  # Don't repeat


# ============================================================
# P2P Connection / Group Establishment
# ============================================================

def create_p2p_connection(
    bus: dbus.SystemBus,
    p2p_dev_path: str,
    peer_path: str,
    con_name: str = "wifi-p2p-connection",
    wps_method: str = "pbc",
) -> Optional[str]:
    """
    Create a Wi-Fi P2P connection profile and activate it to form a P2P Group.

    This is the equivalent of:
        nmcli connection add type wifi-p2p con-name <name> wifi-p2p.peer <mac>
        nmcli connection up <name>

    Args:
        bus: D-Bus system bus.
        p2p_dev_path: Object path of the P2P device.
        peer_path: Object path of the target peer.
        con_name: Connection profile name.
        wps_method: WPS method ("pbc" for push-button, "pin" for PIN).

    Returns:
        The object path of the active connection, or None on failure.
    """
    # Get peer's HW address
    peer_hw = get_property(bus, peer_path, NM_WIFI_P2P_PEER_IFACE, "HWAddress")
    peer_name = get_property(bus, peer_path, NM_WIFI_P2P_PEER_IFACE, "Name")

    print(f"[*] Connecting to peer: {peer_name} ({peer_hw})")

    # Build the connection settings dictionary
    # Reference: https://networkmanager.dev/docs/api/latest/ref-settings.html
    connection_settings = dbus.Dictionary({
        # [connection] section
        "connection": dbus.Dictionary({
            "id": con_name,
            "type": "wifi-p2p",
            "autoconnect": False,
        }, signature="sv"),

        # [wifi-p2p] section
        "wifi-p2p": dbus.Dictionary({
            "peer": str(peer_hw),
            # WPS method: 1 = PBC (Push Button), 2 = PIN (Display), 3 = PIN (Keypad)
            # Uncomment below if you need to specify WPS method explicitly:
            # "wps-method": dbus.UInt32(1),  # PBC
        }, signature="sv"),

        # [ipv4] section - use automatic (DHCP) or shared
        "ipv4": dbus.Dictionary({
            "method": "auto",
        }, signature="sv"),

        # [ipv6] section
        "ipv6": dbus.Dictionary({
            "method": "auto",
        }, signature="sv"),
    }, signature="sa{sv}")

    # Method 1: AddAndActivateConnection
    # This creates the connection profile AND activates it in one step
    nm_proxy = bus.get_object(NM_BUS_NAME, NM_OBJ_PATH)
    nm_iface = dbus.Interface(nm_proxy, NM_IFACE)

    try:
        print("[*] Calling AddAndActivateConnection...")
        settings_path, active_conn_path = nm_iface.AddAndActivateConnection(
            connection_settings,   # Connection settings
            dbus.ObjectPath(p2p_dev_path),  # Device
            dbus.ObjectPath(peer_path),     # Specific object (the peer)
        )
        print(f"[+] Connection profile created: {settings_path}")
        print(f"[+] Active connection: {active_conn_path}")

        # Monitor the connection state
        _monitor_connection_state(bus, active_conn_path)

        return str(active_conn_path)

    except dbus.exceptions.DBusException as e:
        print(f"[!] Failed to create P2P connection: {e}")
        return None


def _monitor_connection_state(bus: dbus.SystemBus, active_conn_path: str, timeout: int = 30):
    """
    Monitor the state of an active connection until it's connected or failed.

    Active connection states:
        0 = Unknown
        1 = Activating
        2 = Activated
        3 = Deactivating
        4 = Deactivated
    """
    STATE_NAMES = {
        0: "Unknown",
        1: "Activating",
        2: "Activated",
        3: "Deactivating",
        4: "Deactivated",
    }

    print(f"[*] Monitoring connection state (timeout: {timeout}s)...")

    loop = GLib.MainLoop()
    result = {"connected": False}

    def on_properties_changed(iface, changed_props, invalidated):
        if "State" in changed_props:
            state = int(changed_props["State"])
            state_name = STATE_NAMES.get(state, f"Unknown({state})")
            print(f"  [STATE] Connection state: {state_name}")

            if state == 2:  # Activated
                print("[+] P2P Group established successfully!")
                result["connected"] = True
                # Print connection details
                _print_connection_details(bus, active_conn_path)
                loop.quit()
            elif state == 4:  # Deactivated
                print("[!] Connection deactivated.")
                loop.quit()

    # Subscribe to property changes on the active connection
    proxy = bus.get_object(NM_BUS_NAME, active_conn_path)
    proxy.connect_to_signal(
        "PropertiesChanged",
        on_properties_changed,
        dbus_interface=DBUS_PROPS_IFACE,
    )

    # Check current state
    current_state = int(get_property(
        bus, active_conn_path, NM_ACTIVE_CONN_IFACE, "State"
    ))
    if current_state == 2:
        print("[+] Already connected!")
        _print_connection_details(bus, active_conn_path)
        return

    # Timeout
    GLib.timeout_add_seconds(timeout, lambda: (loop.quit(), False)[1])

    try:
        loop.run()
    except KeyboardInterrupt:
        print("\n[*] Monitoring interrupted.")

    if not result["connected"]:
        print("[!] Connection did not reach Activated state within timeout.")


def _print_connection_details(bus: dbus.SystemBus, active_conn_path: str):
    """Print details about the established P2P connection."""
    try:
        props = get_all_properties(bus, active_conn_path, NM_ACTIVE_CONN_IFACE)
        print("\n  --- P2P Connection Details ---")
        print(f"  Connection ID: {props.get('Id', 'N/A')}")
        print(f"  Connection UUID: {props.get('Uuid', 'N/A')}")
        print(f"  Type: {props.get('Type', 'N/A')}")

        # Get IP configuration
        ip4_config_path = props.get("Ip4Config", "/")
        if ip4_config_path and str(ip4_config_path) != "/":
            ip4_props = get_all_properties(
                bus, str(ip4_config_path),
                "org.freedesktop.NetworkManager.IP4Config"
            )
            addresses = ip4_props.get("AddressData", [])
            for addr in addresses:
                print(f"  IPv4 Address: {addr.get('address', 'N/A')}/{addr.get('prefix', 'N/A')}")
            gateway = ip4_props.get("Gateway", "")
            if gateway:
                print(f"  Gateway: {gateway}")

        # Get the P2P group interface
        devices = props.get("Devices", [])
        for dev_path in devices:
            dev_iface = get_property(bus, str(dev_path), NM_DEVICE_IFACE, "IpInterface")
            print(f"  Interface: {dev_iface}")

        print("  " + "-" * 30)
    except dbus.exceptions.DBusException as e:
        print(f"  [WARN] Could not get connection details: {e}")


# ============================================================
# Disconnect / Cleanup
# ============================================================

def disconnect_p2p(bus: dbus.SystemBus, active_conn_path: str):
    """Deactivate a P2P connection."""
    nm_proxy = bus.get_object(NM_BUS_NAME, NM_OBJ_PATH)
    nm_iface = dbus.Interface(nm_proxy, NM_IFACE)

    try:
        nm_iface.DeactivateConnection(dbus.ObjectPath(active_conn_path))
        print(f"[+] Connection deactivated: {active_conn_path}")
    except dbus.exceptions.DBusException as e:
        print(f"[!] Failed to deactivate: {e}")


def delete_p2p_connection_profile(bus: dbus.SystemBus, con_name: str = "wifi-p2p-connection"):
    """Delete a saved P2P connection profile by name."""
    settings_proxy = bus.get_object(NM_BUS_NAME, "/org/freedesktop/NetworkManager/Settings")
    settings_iface = dbus.Interface(settings_proxy, NM_SETTINGS_IFACE)

    connections = settings_iface.ListConnections()
    for conn_path in connections:
        conn_proxy = bus.get_object(NM_BUS_NAME, conn_path)
        conn_iface = dbus.Interface(conn_proxy, NM_SETTINGS_CONN_IFACE)
        settings = conn_iface.GetSettings()

        conn_id = str(settings.get("connection", {}).get("id", ""))
        conn_type = str(settings.get("connection", {}).get("type", ""))

        if conn_id == con_name and conn_type == "wifi-p2p":
            conn_iface.Delete()
            print(f"[+] Deleted connection profile: {con_name} ({conn_path})")
            return True

    print(f"[!] Connection profile '{con_name}' not found.")
    return False


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Wi-Fi P2P Discovery and Connection using NetworkManager D-Bus API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Discover P2P peers (15 second scan)
  sudo python3 p2p_discovery.py

  # Discover with 30 second timeout
  sudo python3 p2p_discovery.py --timeout 30

  # Discover and connect to the first found peer
  sudo python3 p2p_discovery.py --connect

  # Connect to a specific peer by MAC address
  sudo python3 p2p_discovery.py --connect --peer-mac AA:BB:CC:DD:EE:FF

  # Clean up: delete saved connection profile
  sudo python3 p2p_discovery.py --cleanup
        """,
    )
    parser.add_argument(
        "--timeout", type=int, default=15,
        help="Discovery timeout in seconds (default: 15)"
    )
    parser.add_argument(
        "--connect", action="store_true",
        help="Connect to the first discovered peer (or --peer-mac)"
    )
    parser.add_argument(
        "--peer-mac", type=str, default=None,
        help="MAC address of a specific peer to connect to"
    )
    parser.add_argument(
        "--cleanup", action="store_true",
        help="Delete the saved P2P connection profile and exit"
    )
    parser.add_argument(
        "--con-name", type=str, default="wifi-p2p-connection",
        help="Connection profile name (default: wifi-p2p-connection)"
    )

    args = parser.parse_args()

    # Initialize D-Bus
    bus = get_system_bus()

    # Cleanup mode
    if args.cleanup:
        delete_p2p_connection_profile(bus, args.con_name)
        return

    # Find P2P device
    print("[*] Searching for Wi-Fi P2P device...")
    p2p_dev_path = find_p2p_device(bus)

    if not p2p_dev_path:
        print("[*] No direct P2P device found, checking Wi-Fi companion devices...")
        p2p_dev_path = find_p2p_device_from_wifi(bus)

    if not p2p_dev_path:
        print("[!] No Wi-Fi P2P device found!")
        print("[!] Possible reasons:")
        print("    1. Your Wi-Fi adapter does not support P2P")
        print("    2. NetworkManager is not managing the Wi-Fi device")
        print("    3. P2P support is not enabled in NetworkManager")
        print()
        print("[*] Listing all devices for debugging:")
        nm = get_nm_proxy(bus)
        for dev_path in nm.GetDevices():
            dev_type = int(get_property(bus, dev_path, NM_DEVICE_IFACE, "DeviceType"))
            dev_iface = str(get_property(bus, dev_path, NM_DEVICE_IFACE, "Interface"))
            print(f"    Device: {dev_iface}, Type: {dev_type}, Path: {dev_path}")
        sys.exit(1)

    # Start peer discovery
    discovery = P2PDiscovery(bus, p2p_dev_path, timeout=args.timeout)
    peers = discovery.start_discovery()

    if not peers:
        print("[!] No peers found. Try increasing --timeout or moving closer to P2P devices.")
        sys.exit(0)

    # Print summary
    print("=" * 60)
    print("Discovered Peers Summary:")
    print("=" * 60)
    for i, (path, info) in enumerate(peers.items(), 1):
        print(f"  [{i}] Name: {info.get('Name', 'Unknown')}")
        print(f"      MAC:  {info.get('HWAddress', 'N/A')}")
        print(f"      Model: {info.get('Manufacturer', '')} {info.get('Model', '')}")
        print()

    # Connect if requested
    if args.connect:
        target_peer = None

        if args.peer_mac:
            # Find peer by MAC
            for path, info in peers.items():
                if info.get("HWAddress", "").lower() == args.peer_mac.lower():
                    target_peer = path
                    break
            if not target_peer:
                print(f"[!] Peer with MAC {args.peer_mac} not found in discovered peers.")
                sys.exit(1)
        else:
            # Use the first discovered peer
            target_peer = list(peers.keys())[0]

        print(f"\n[*] Attempting P2P connection to: {peers[target_peer].get('Name', 'Unknown')}")
        active_conn = create_p2p_connection(
            bus, p2p_dev_path, target_peer, con_name=args.con_name
        )

        if active_conn:
            print("\n[*] P2P connection is active.")
            print("[*] Press Ctrl+C to disconnect and exit.")
            try:
                # Keep the script running
                loop = GLib.MainLoop()
                signal.signal(signal.SIGINT, lambda *_: loop.quit())
                loop.run()
            except KeyboardInterrupt:
                pass
            finally:
                print("\n[*] Disconnecting...")
                disconnect_p2p(bus, active_conn)


if __name__ == "__main__":
    main()
