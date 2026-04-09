import dbus
import dbus.mainloop.glib
import sys
from typing import Any, Dict, Optional
from gi.repository import GLib

# dbus api interfaces and constants
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

# ============================================================
# Peer Discovery
# ============================================================

class P2PDiscovery:
    """Handles Wi-Fi P2P peer discovery using NetworkManager D-Bus API."""

    def __init__(self, bus: dbus.SystemBus, p2p_dev_path: str, target_peer_address: str, timeout: int = 600):
        self.bus = bus
        self.p2p_dev_path = p2p_dev_path
        self.target_peer_address = target_peer_address
        self.target_found = False
        self.target_info: Optional[Dict[str, Any]] = None
        self.timeout = timeout
        self.peers: Dict[str, Dict[str, Any]] = {}
        self.loop: Optional[GLib.MainLoop] = None
        self._signal_match = None

    def _on_peer_added(self, peer_path: str):
        """Signal handler: called when a new P2P peer is discovered."""
        peer_info = self._get_peer_info(peer_path)
        self.peers[str(peer_path)] = peer_info
        print(f"  [FOUND] Peer: {peer_info.get('Name', 'Unknown')}")
        print(f"          HwAddress: {peer_info.get('HwAddress', 'N/A')}")
        print(f"          Path: {peer_path}")
        print()

        if peer_info.get("HwAddress", "").lower() == self.target_peer_address.lower():
            print(f"[*] Target peer {self.target_peer_address} found! Stopping discovery.")
            self.target_found = True
            self.target_info = peer_info
            if self.loop and self.loop.is_running():
                self._stop_loop()

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
                "HwAddress": str(props.get("HwAddress", "")),
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
# Connection Establishment (Placeholder)
# ============================================================
def create_p2p_connection(
    bus: dbus.SystemBus,
    p2p_dev_path: str,
    peer_info: Dict[str, Any],
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
    peer_path = peer_info.get("Path")
    peer_hw = peer_info.get("HwAddress", "Unknown")
    peer_name = peer_info.get("Name", "Unknown")

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
        # _monitor_connection_state(bus, active_conn_path)

        return str(active_conn_path)

    except dbus.exceptions.DBusException as e:
        print(f"[!] Failed to create P2P connection: {e}")
        return None

# ============================================================
# Main Execution
# ============================================================

def main():
    target_peer_address = "62:4B:7C:9E:06:7E"

    bus = get_system_bus()
    p2p_dev_path = find_p2p_device(bus)

    if not p2p_dev_path:
        print("[-] No Wi-Fi P2P device found. Ensure your hardware supports P2P and is enabled.")
        return
    print(f"[+] Using P2P device at {p2p_dev_path}")

    discovery = P2PDiscovery(bus, p2p_dev_path, target_peer_address)
    peers = discovery.start_discovery()

    if not peers:
        print("[-] No peers found.")
        return

    if discovery.target_found is not True:
        print(f"[-] Target peer {target_peer_address} was not found.")
        return
    
    target_info = discovery.target_info
    create_p2p_connection(bus, p2p_dev_path, target_info)

    while True:
        try:
            GLib.MainLoop().run()
        except KeyboardInterrupt:
            print("\n[*] Exiting...")
            break


if __name__ == "__main__":
    main()