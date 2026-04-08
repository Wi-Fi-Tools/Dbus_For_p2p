::::::: {#top}
::: {#titlearea}
+-----------------------------------------------------------------------+
| ::: {#projectname}                                                    |
| wpa_supplicant / hostapd  [2.5]{#projectnumber}                       |
| :::                                                                   |
+-----------------------------------------------------------------------+
:::

::: {#navrow1 .tabs}
- [Main Page](index.html)

- [Related Pages](pages.html)

- [Data Structures](annotated.html)

- [Files](files.html)

- ::: {#MSearchBox .MSearchBoxInactive}
  [ ![](search/mag_sel.png){#MSearchSelect
  onmouseover="return searchBox.OnSearchSelectShow()"
  onmouseout="return searchBox.OnSearchSelectHide()"} ]{.left}[
  [![](search/close.png){#MSearchCloseImg
  border="0"}](javascript:searchBox.CloseResultsWindow()){#MSearchClose}
  ]{.right}
  :::
:::

::: {#MSearchSelectWindow onmouseover="return searchBox.OnSearchSelectShow()" onmouseout="return searchBox.OnSearchSelectHide()" onkeydown="return searchBox.OnSearchSelectKey(event)"}
[[ ]{.SelectionMark}All](javascript:void(0)){.SelectItem
onclick="searchBox.OnSelectItem(0)"}[[ ]{.SelectionMark}Data
Structures](javascript:void(0)){.SelectItem
onclick="searchBox.OnSelectItem(1)"}[[ ]{.SelectionMark}Files](javascript:void(0)){.SelectItem
onclick="searchBox.OnSelectItem(2)"}[[ ]{.SelectionMark}Functions](javascript:void(0)){.SelectItem
onclick="searchBox.OnSelectItem(3)"}[[ ]{.SelectionMark}Variables](javascript:void(0)){.SelectItem
onclick="searchBox.OnSelectItem(4)"}[[ ]{.SelectionMark}Typedefs](javascript:void(0)){.SelectItem
onclick="searchBox.OnSelectItem(5)"}[[ ]{.SelectionMark}Enumerations](javascript:void(0)){.SelectItem
onclick="searchBox.OnSelectItem(6)"}[[ ]{.SelectionMark}Enumerator](javascript:void(0)){.SelectItem
onclick="searchBox.OnSelectItem(7)"}[[ ]{.SelectionMark}Macros](javascript:void(0)){.SelectItem
onclick="searchBox.OnSelectItem(8)"}[[ ]{.SelectionMark}Pages](javascript:void(0)){.SelectItem
onclick="searchBox.OnSelectItem(9)"}
:::

::: {#MSearchResultsWindow}
:::
:::::::

::::: header
:::: headertitle
::: title
wpa_supplicant D-Bus API
:::
::::
:::::

:::: contents
::: textblock
This section documents the wpa_supplicant D-Bus API. Every D-Bus
interface implemented by wpa_supplicant is described here including
their methods, signals, and properties with arguments, returned values,
and possible errors.

Interfaces:

- [fi.w1.wpa_supplicant1](dbus.html#dbus_main){.el}
- [fi.w1.wpa_supplicant1.Interface](dbus.html#dbus_interface){.el}
- [fi.w1.wpa_supplicant1.Interface.WPS](dbus.html#dbus_wps){.el}
- [fi.w1.wpa_supplicant1.Interface.P2PDevice](dbus.html#dbus_p2pdevice){.el}
- [fi.w1.wpa_supplicant1.BSS](dbus.html#dbus_bss){.el}
- [fi.w1.wpa_supplicant1.Network](dbus.html#dbus_network){.el}
- [fi.w1.wpa_supplicant1.Peer](dbus.html#dbus_peer){.el}
- [fi.w1.wpa_supplicant1.Group](dbus.html#dbus_group){.el}
- [fi.w1.wpa_supplicant1.PersistentGroup](dbus.html#dbus_persistent_group){.el}

# []{#dbus_main .anchor} fi.w1.wpa_supplicant1

Interface implemented by the main wpa_supplicant D-Bus object registered
in the bus with fi.w1.wpa_supplicant1 name.

## []{#dbus_main_methods .anchor} Methods

- ### CreateInterface ( a{sv} : args ) --\> o : interface

  Registers a wireless interface in wpa_supplicant.

  #### Arguments

  a{sv} : args
  :   A dictionary with arguments used to add the interface to
      wpa_supplicant. The dictionary may contain the following entries:
        Key            Value type   Description                                             Required
        -------------- ------------ ------------------------------------------------------- ----------
        Ifname         s            Name of the network interface to control, e.g., wlan0   Yes
        BridgeIfname   s            Name of the bridge interface to control, e.g., br0      No
        Driver         s            Driver name which the interface uses, e.g., nl80211     No
        ConfigFile     s            Configuration file path                                 No

  #### Returns

  o : interface
  :   A D-Bus path to object representing created interface

  #### Possible errors

  fi.w1.wpa_supplicant1.InterfaceExists
  :   wpa_supplicant already controls this interface.

  fi.w1.wpa_supplicant1.UnknownError
  :   Creating interface failed for an unknown reason.

  fi.w1.wpa_supplicant1.InvalidArgs
  :   Invalid entries were found in the passed argument.

- ### RemoveInterface ( o : interface ) --\> nothing

  Deregisters a wireless interface from wpa_supplicant.

  #### Arguments

  o : interface
  :   A D-Bus path to an object representing an interface to remove
      returned by CreateInterface

  #### Possible errors

  fi.w1.wpa_supplicant1.InterfaceUnknown
  :   Object pointed by the path doesn\'t exist or doesn\'t represent an
      interface.

  fi.w1.wpa_supplicant1.UnknownError
  :   Removing interface failed for an unknown reason.

- ### GetInterface ( s : ifname ) --\> o : interface

  Returns a D-Bus path to an object related to an interface which
  wpa_supplicant already controls.

  #### Arguments

  s : ifname
  :   Name of the network interface, e.g., wlan0

  #### Returns

  o : interface
  :   A D-Bus path to an object representing an interface

  #### Possible errors

  fi.w1.wpa_supplicant1.InterfaceUnknown
  :   An interface with the passed name in not controlled by
      wpa_supplicant.

  fi.w1.wpa_supplicant1.UnknownError
  :   Getting an interface object path failed for an unknown reason.

## []{#dbus_main_properties .anchor} Properties

- ### DebugLevel - s - (read/write)

  Global wpa_supplicant debugging level. Possible values are \"msgdump\"
  (verbose debugging), \"debug\" (debugging), \"info\" (informative),
  \"warning\" (warnings), and \"error\" (errors).

- ### DebugTimestamp - b - (read/write)

  Global wpa_supplicant debugging parameter. Determines if timestamps
  are shown in debug logs.

- ### DebugShowKeys - b - (read/write)

  Global wpa_supplicant debugging parameter. Determines if secrets are
  shown in debug logs.

- ### Interfaces - ao - (read)

  An array with paths to D-Bus objects representing controlled
  interfaces each.

- ### EapMethods - as - (read)

  An array with supported EAP methods names.

- ### Capabilities - as - (read)

  An array with supported capabilities (e.g., \"ap\", \"ibss-rsn\",
  \"p2p\", \"interworking\").

- ### WFDIEs - ay - (read/write)

  Wi-Fi Display subelements.

## []{#dbus_main_signals .anchor} Signals

- ### InterfaceAdded ( o : interface, a{sv} : properties )

  A new interface was added to wpa_supplicant.

  #### Arguments

  o : interface
  :   A D-Bus path to an object representing the added interface

  <!-- -->

  a{sv} : properties
  :   A dictionary containing properties of added interface.

- ### InterfaceRemoved ( o : interface )

  An interface was removed from wpa_supplicant.

  #### Arguments

  o : interface
  :   A D-Bus path to an object representing the removed interface

- ### PropertiesChanged ( a{sv} : properties )

  Some properties have changed.

  #### Arguments

  a{sv} : properties
  :   A dictionary with pairs of properties names which have changed and
      theirs new values. Possible dictionary keys are: \"DebugParams\"

# []{#dbus_interface .anchor} fi.w1.wpa_supplicant1.Interface

Interface implemented by objects related to network interface added to
wpa_supplicant, i.e., returned by fi.w1.wpa_supplicant1.CreateInterface.

## []{#dbus_interface_methods .anchor} Methods

- ### Scan ( a{sv} : args ) --\> nothing

  Triggers a scan.

  #### Arguments

  a{sv} : args
  :   A dictionary with arguments describing scan type:
        Key         Value type   Description                                                                                                            Required
        ----------- ------------ ---------------------------------------------------------------------------------------------------------------------- ----------
        Type        s            Type of the scan. Possible values: \"active\", \"passive\"                                                             Yes
        SSIDs       aay          Array of SSIDs to scan for (applies only if scan type is active)                                                       No
        IEs         aay          Information elements to used in active scan (applies only if scan type is active)                                      No
        Channels    a(uu)        Array of frequencies to scan in form of (center, width) in MHz.                                                        No
        AllowRoam   b            TRUE (or absent) to allow a roaming decision based on the results of this scan, FALSE to prevent a roaming decision.   No

  #### Possible errors

  fi.w1.wpa_supplicant1.InvalidArgs
  :   Invalid entries were found in the passed argument.

- ### Disconnect ( ) --\> nothing

  Disassociates the interface from current network.

  #### Possible errors

  fi.w1.wpa_supplicant1.NotConnected
  :   Interface is not connected to any network.

- ### AddNetwork ( a{sv} : args ) --\> o : network

  Adds a new network to the interface.

  #### Arguments

  a{sv} : args
  :   A dictionary with network configuration. Dictionary entries are
      equivalent to entries in the \"network\" block in wpa_supplicant
      configuration file. Entry values should be appropriate type to the
      entry, e.g., an entry with key \"frequency\" should have value
      type int.

  #### Returns

  o : network
  :   A D-Bus path to an object representing a configured network

  #### Possible errors

  fi.w1.wpa_supplicant1.InvalidArgs
  :   Invalid entries were found in the passed argument.

  fi.w1.wpa_supplicant1.UnknownError
  :   Adding network failed for an unknown reason.

- ### RemoveNetwork ( o : network ) --\> nothing

  Removes a configured network from the interface.

  #### Arguments

  o : network
  :   A D-Bus path to an object representing a configured network
      returned by fi.w1.wpa_supplicant1.Interface.AddNetwork

  #### Possible errors

  fi.w1.wpa_supplicant1.NetworkUnknown
  :   A passed path doesn\'t point to any network object.

  fi.w1.wpa_supplicant1.InvalidArgs
  :   A passed path doesn\'t point to any network object.

  fi.w1.wpa_supplicant1.UnknownError
  :   Removing network failed for an unknown reason.

- ### RemoveAllNetworks ( ) --\> nothing

  Remove all configured networks from the interface.

- ### SelectNetwork ( o : network ) --\> nothing

  Attempt association with a configured network.

  #### Arguments

  o : network
  :   A D-Bus path to an object representing a configured network
      returned by fi.w1.wpa_supplicant1.Interface.AddNetwork

  #### Possible errors

  fi.w1.wpa_supplicant1.NetworkUnknown
  :   A passed path doesn\'t point to any network object.

  fi.w1.wpa_supplicant1.InvalidArgs
  :   A passed path doesn\'t point to any network object.

- ### Reassociate ( ) --\> nothing

  Attempt reassociation.

  #### Possible errors

  fi.w1.wpa_supplicant1.InterfaceDisabled
  :   The interface is disabled.

- ### Reattach ( ) --\> nothing

  Attempt reassociation back to the current BSS.

  #### Possible errors

  fi.w1.wpa_supplicant1.NotConnected
  :   Interface is not connected to any network.

- ### Reconnect ( ) --\> nothing

  Attempt reconnection and connect if in disconnected state.

  #### Possible errors

  fi.w1.wpa_supplicant1.InterfaceDisabled
  :   The interface is disabled.

- ### AddBlob ( s : name, ay : data ) --\> nothing

  Adds a blob to the interface.

  #### Arguments

  s : name
  :   A name of a blob

  ay : data
  :   A blob data

  #### Possible errors

  fi.w1.wpa_supplicant1.BlobExists
  :   A blob with the specified name already exists.

- ### RemoveBlob ( s : name ) --\> nothing

  Removes the blob from the interface.

  #### Arguments

  s : name
  :   A name of the blob to remove

  #### Possible errors

  fi.w1.wpa_supplicant1.BlobUnknown
  :   A blob with the specified name doesn\'t exist.

- ### GetBlob ( s : name ) --\> ay : data

  Returns the blob data of a previously added blob.

  #### Arguments

  s : name
  :   A name of the blob

  #### Returns

  ay : data
  :   A blob data

  #### Possible errors

  fi.w1.wpa_supplicant1.BlobUnknown
  :   A blob with the specified name doesn\'t exist.

- ### AutoScan ( s : arg ) --\> nothing

  Set autoscan parameters for the interface.

  #### Arguments

  s : arg
  :   Autoscan parameter line or empty to unset autoscan.

  #### Possible errors

  fi.w1.wpa_supplicant1.NoMemory
  :   Needed memory was not possible to get allocated.

  fi.w1.wpa_supplicant1.InvalidArgs
  :   Invalid entries were found in the passed argument.

- ### TDLSDiscover ( s : peer_address ) --\> nothing

  Initiate a TDLS discovery for a peer.

  #### Arguments

  s : peer_address
  :   MAC address for the peer to perform TDLS discovery.

  #### Possible errors

  fi.w1.wpa_supplicant1.InvalidArgs
  :   The \"peer_address\" argument is not a properly formatted MAC.

  fi.w1.wpa_supplicant1.UnknownError
  :   Initiating the TDLS operation failed for an unknown reason.

- ### TDLSSetup ( s : peer_address ) --\> nothing

  Setup a TDLS session for a peer.

  #### Arguments

  s : peer_address
  :   MAC address for the peer to perform TDLS setup.

  #### Possible errors

  fi.w1.wpa_supplicant1.InvalidArgs
  :   The \"peer_address\" argument is not a properly formatted MAC.

  fi.w1.wpa_supplicant1.UnknownError
  :   Initiating the TDLS operation failed for an unknown reason.

- ### TDLSStatus ( s : peer_address ) --\> s

  Return TDLS status with respect to a peer.

  #### Arguments

  s : peer_address
  :   MAC address for the peer for which status is requested.

  #### Returns

  s : status
  :   Current status of the TDLS link with the selected peer.

  #### Possible errors

  fi.w1.wpa_supplicant1.InvalidArgs
  :   The \"peer_address\" argument is not a properly formatted MAC.

- ### TDLSTeardown ( s : peer_address ) --\> nothing

  Tear down a TDLS session with a peer.

  #### Arguments

  s : peer_address
  :   MAC address for the peer to tear down TDLS connectivity with.

  #### Possible errors

  fi.w1.wpa_supplicant1.InvalidArgs
  :   The \"peer_address\" argument is not a properly formatted MAC.

  fi.w1.wpa_supplicant1.UnknownError
  :   Initiating the TDLS operation failed for an unknown reason.

- ### EAPLogoff ( ) --\> nothing

  IEEE 802.1X EAPOL state machine logoff.

- ### EAPLogon ( ) --\> nothing

  IEEE 802.1X EAPOL state machine logon.

- ### NetworkReply ( o : network, s : field, s : value ) --\> nothing

  Provide parameter requested by NetworkRequest().

  #### Arguments

  o : network
  :   A D-Bus path to an object representing the network (copied from
      NetworkRequest()).

  s : field
  :   Requested information (copied from NetworkRequest()).

  s : value
  :   The requested information (e.g., password for EAP authentication).

  #### Possible errors

  fi.w1.wpa_supplicant1.NetworkUnknown
  :   A passed path doesn\'t point to any network object.

  fi.w1.wpa_supplicant1.InvalidArgs
  :   A passed path doesn\'t point to any network object.

  fi.w1.wpa_supplicant1.UnknownError
  :   IEEE 802.1X support was not included in the build.

- ### SetPKCS11EngineAndModulePath ( s : pkcs11_engine_path, s : pkcs11_module_path ) --\> nothing

  Set PKCS #11 engine and module path.

  #### Arguments

  s : pkcs11_engine_path
  :   PKCS #11 engine path.

  s : pkcs11_module_path
  :   PKCS #11 module path.

  #### Possible errors

  org.freedesktop.DBus.Error.Failed.InvalidArgs
  :   Invalid PKCS #11 engine or module path.

  org.freedesktop.DBus.Error.Failed
  :   Reinit of the EAPOL state machine with the new PKCS #11 engine and
      module path failed.

- ### SignalPoll ( ) --\> a{sv} : properties

  Fetch signal properties for the current connection.

  #### Returns

  a{sv} : properties

  :   
        Key           Value type   Description                     Required
        ------------- ------------ ------------------------------- ----------
        linkspeed     i            Link speed (Mbps)               No
        noise         i            Noise (dBm)                     No
        width         s            Channel width                   No
        frequency     u            Frequency (MHz)                 No
        rssi          i            RSSI (dBm)                      No
        avg-rssi      i            Average RSSI (dBm)              No
        center-frq1   i            VHT segment 1 frequency (MHz)   No
        center-frq2   i            VHT segment 2 frequency (MHz)   No

- ### FlushBSS ( u : age ) --\> nothing

  Flush BSS entries from the cache.

  #### Arguments

  u : age
  :   Maximum age in seconds for BSS entries to keep in cache (0 =
      remove all entries).

- ### SubscribeProbeReq ( ) --\> nothing

  Subscribe to receive Probe Request events. This is needed in addition
  to registering a signal handler for the ProbeRequest signal to avoid
  flooding D-Bus with all Probe Request indications when no application
  is interested in them.

  #### Possible errors

  fi.w1.wpa_supplicant1.SubscriptionInUse
  :   Another application is already subscribed.

  fi.w1.wpa_supplicant1.NoMemory
  :   Needed memory was not possible to get allocated.

- ### UnsubscribeProbeReq ( ) --\> nothing

  Unsubscribe from receiving Probe Request events.

  #### Possible errors

  fi.w1.wpa_supplicant1.NoSubscription
  :   No subscription in place.

  fi.w1.wpa_supplicant1.SubscriptionNotYou
  :   Subscription in place, but for another process.

## []{#dbus_interface_properties .anchor} Properties

- ### Capabilities - a{sv} - (read)

  Capabilities of the interface. Dictionary contains following entries:

    Key        Value type   Description
    ---------- ------------ ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Pairwise   as           Possible array elements: \"ccmp\", \"tkip\", \"none\"
    Group      as           Possible array elements: \"ccmp\", \"tkip\", \"wep104\", \"wep40\"
    KeyMgmt    as           Possible array elements: \"wpa-psk\", \"wpa-ft-psk\", \"wpa-psk-sha256\", \"wpa-eap\", \"wpa-ft-eap\", \"wpa-eap-sha256\", \"ieee8021x\", \"wpa-none\", \"wps\", \"none\"
    Protocol   as           Possible array elements: \"rsn\", \"wpa\"
    AuthAlg    as           Possible array elements: \"open\", \"shared\", \"leap\"
    Scan       as           Possible array elements: \"active\", \"passive\", \"ssid\"
    Modes      as           Possible array elements: \"infrastructure\", \"ad-hoc\", \"ap\"

- ### State - s - (read)

  A state of the interface. Possible values are: return
  \"disconnected\", \"inactive\", \"scanning\", \"authenticating\",
  \"associating\", \"associated\", \"4way_handshake\",
  \"group_handshake\", \"completed\",\"unknown\".

- ### Scanning - b - (read)

  Determines if the interface is already scanning or not

- ### ApScan - u - (read/write)

  Identical to ap_scan entry in wpa_supplicant configuration file.
  Possible values are 0, 1 or 2.

- ### BSSExpireAge - u - (read/write)

  Identical to bss_expiration_age entry in wpa_supplicant configuration
  file.

- ### BSSExpireCount - u - (read/write)

  Identical to bss_expiration_scan_count entry in wpa_supplicant
  configuration file.

- ### Country - s - (read/write)

  Identical to country entry in wpa_supplicant configuration file.

- ### Ifname - s - (read)

  Name of network interface controlled by the interface, e.g., wlan0.

- ### BridgeIfname - s - (read)

  Name of bridge network interface controlled by the interface, e.g.,
  br0.

- ### Driver - s - (read)

  Name of driver used by the interface, e.g., nl80211.

- ### CurrentBSS - o - (read)

  Path to D-Bus object representing BSS which wpa_supplicant is
  associated with, or \"/\" if is not associated at all.

- ### CurrentNetwork - o - (read)

  Path to D-Bus object representing configured network which
  wpa_supplicant uses at the moment, or \"/\" if doesn\'t use any.

- ### CurrentAuthMode - s - (read)

  Current authentication type.

- ### Blobs - as - (read)

  List of blobs names added to the Interface.

- ### BSSs - ao - (read)

  List of D-Bus objects paths representing BSSs known to the interface,
  i.e., scan results.

- ### Networks - ao - (read)

  List of D-Bus objects paths representing configured networks.

- ### FastReauth - b - (read/write)

  Identical to fast_reauth entry in wpa_supplicant configuration file.

- ### ScanInterval - i - (read/write)

  Time (in seconds) between scans for a suitable AP. Must be \>= 0.

- ### PKCS11EnginePath - s - (read)

  PKCS #11 engine path.

- ### PKCS11ModulePath - s - (read)

  PKCS #11 module path.

- ### DisconnectReason - i - (read)

  The most recent IEEE 802.11 reason code for disconnect. Negative value
  indicates locally generated disconnection.

## []{#dbus_interface_signals .anchor} Signals

- ### ScanDone ( b : success )

  Scanning finished.

  #### Arguments

  s : success
  :   Determines if scanning was successful. If so, results are
      available.

- ### BSSAdded ( o : BSS, a{sv} : properties )

  Interface became aware of a new BSS.

  #### Arguments

  o : BSS
  :   A D-Bus path to an object representing the new BSS.

  <!-- -->

  a{sv} : properties
  :   A dictionary containing properties of added BSS.

- ### BSSRemoved ( o : BSS )

  BSS disappeared.

  #### Arguments

  o : BSS
  :   A D-Bus path to an object representing the BSS.

- ### BlobAdded ( s : blobName )

  A new blob has been added to the interface.

  #### Arguments

  s : blobName
  :   A name of the added blob.

- ### BlobRemoved ( s : blobName )

  A blob has been removed from the interface.

  #### Arguments

  s : blobName
  :   A name of the removed blob.

- ### NetworkAdded ( o : network, a{sv} : properties )

  A new network has been added to the interface.

  #### Arguments

  o : network
  :   A D-Bus path to an object representing the added network.

  <!-- -->

  a{sv} : properties
  :   A dictionary containing properties of added network.

- ### NetworkRemoved ( o : network )

  The network has been removed from the interface.

  #### Arguments

  o : network
  :   A D-Bus path to an object representing the removed network.

- ### NetworkSelected ( o : network )

  The network has been selected.

  #### Arguments

  o : network
  :   A D-Bus path to an object representing the selected network.

- ### StaAuthorized ( s : mac )

  A new station has been authorized to the interface.

  #### Arguments

  s : mac
  :   A mac address which has been authorized.

- ### StaDeauthorized ( s : mac )

  A station has been deauthorized to the interface.

  #### Arguments

  s : mac
  :   A mac address which has been deauthorized.

- ### PropertiesChanged ( a{sv} : properties )

  Some properties have changed.

  #### Arguments

  a{sv} : properties
  :   A dictionary with pairs of properties names which have changed and
      theirs new values. Possible dictionary keys are: \"ApScan\",
      \"Scanning\", \"State\", \"CurrentBSS\", \"CurrentNetwork\"

- ### Certification ( a{sv} : parameters )

  Information about server TLS certificates.

  #### Arguments

  a{sv} : parameters
  :   A dictionary with pairs of field names and their values. Possible
      dictionary keys are: \"depth\", \"subject\", \"altsubject\",
      \"cert_hash\", \"cert\".

- ### EAP ( s : status, s : parameter )

  Information about EAP peer status.

  #### Arguments

  s : status
  :   Operation, e.g., \"started\", \"accept proposed method\", \"remote
      certificate verification\", \"eap parameter needed\",
      \"completion\".

  s : parameter
  :   Information about the operation, e.g., EAP method name,
      \"success\".

- ### NetworkRequest ( o : network, s : field, s : txt )

  Request for network parameter. NetworkResponse() is used to provide
  the requested parameter.

  #### Arguments

  o : network
  :   D-Bus path to an object representing the network.

  s : field
  :   Requested information, e.g., \"PASSWORD\".

  txt : field
  :   Human readable information about the requested information.

- ### ProbeRequest ( a{sv} : args )

  Information about a received Probe Request frame. This signal is
  delivered only to a single application that has subscribed to received
  the events with SubscribeProbeReq().

  #### Arguments

  a{sv} : args
  :   A dictionary with pairs of field names and their values. Possible
      dictionary keys are: \"addr\", \"dst\", \"bssid\", \"ies\",
      \"signal\".

# []{#dbus_wps .anchor} fi.w1.wpa_supplicant1.Interface.WPS

Interface for performing WPS (Wi-Fi Simple Config) operations.

## []{#dbus_wps_methods .anchor} Methods

- ### Start ( a{sv} : args ) --\> a{sv} : output

  Starts WPS configuration. Note: When used with P2P groups, this needs
  to be issued on the GO group interface.

  #### Arguments

  a{sv} : args
  :   A dictionary with arguments used to start WPS configuration. The
      dictionary may contain the following entries:
        Key                Value type   Description                                                                                                Required
        ------------------ ------------ ---------------------------------------------------------------------------------------------------------- ---------------------------------------------
        Role               s            The device\'s role. Possible values are \"enrollee\" and \"registrar\".                                    Yes
        Type               s            WPS authentication type. Applies only for enrollee role. Possible values are \"pin\" and \"pbc\".          Yes, for enrollee role; otherwise no
        Pin                s            WPS Pin.                                                                                                   Yes, for registrar role; otherwise optional
        Bssid              ay           Note: This is used to specify the peer MAC address when authorizing WPS connection in AP or P2P GO role.   No
        P2PDeviceAddress   ay           P2P Device Address of a peer to authorize for PBC connection. Used only in P2P GO role.                    No

  #### Returns

  a{sv} : output

  :   
        Key   Value type   Description                                                                            Required
        ----- ------------ -------------------------------------------------------------------------------------- ----------
        Pin   s            Newly generated PIN, if not specified for enrollee role and pin authentication type.   No

  #### Possible errors

  fi.w1.wpa_supplicant1.UnknownError
  :   Starting WPS configuration failed for an unknown reason.

  fi.w1.wpa_supplicant1.InvalidArgs
  :   Invalid entries were found in the passed argument.

- ### Cancel ( nothing ) --\> nothing

  Cancel ongoing WPS operation.

## []{#dbus_wps_properties .anchor} Properties

- ### ProcessCredentials - b - (read/write)

  Determines if the interface will process the credentials
  (credentials_processed configuration file parameter).

- ### ConfigMethods - s - (read/write)

  The currently advertised WPS configuration methods. Available methods:
  usba ethernet label display ext_nfc_token int_nfc_token nfc_interface
  push_button keypad virtual_display physical_display
  virtual_push_button physical_push_button.

## []{#dbus_wps_signals .anchor} Signals

- ### Event ( s : name, a{sv} : args )

  WPS event occurred.

  #### Arguments

  s : event
  :   Event type. Possible values are: \"success, \"fail\", \"m2d\", and
      \"pbc-overlap\".

  a{sv} : args
  :   Event arguments. Empty for success and pbc-overlap events, error
      information ( \"msg\" : i, \"config_error\" : i,
      \"error_indication\" : i ) for fail event and following entries
      for m2d event:
        config_methods     Value type
        ------------------ ------------
        manufacturer       q
        model_name         ay
        model_number       ay
        serial_number      ay
        dev_name           ay
        primary_dev_type   ay
        config_error       q
        dev_password_id    q

- ### Credentials ( a{sv} : credentials )

  WPS credentials. Dictionary contains:

    Key        Value type   Description
    ---------- ------------ -----------------------------------------------------------------------------------------------------
    BSSID      ay           
    SSID       s            
    AuthType   as           Possible array elements: \"open\", \"shared\", \"wpa-psk\", \"wpa-eap\", \"wpa2-eap\", \"wpa2-psk\"
    EncrType   as           Possible array elements: \"none\", \"wep\", \"tkip\", \"aes\"
    Key        ay           Key data
    KeyIndex   u            Key index

- ### PropertiesChanged ( a{sv} : properties )

  Some properties have changed.

  #### Arguments

  a{sv} : properties
  :   A dictionary with pairs of properties names which have changed and
      theirs new values. Possible dictionary keys are:
      \"ProcessCredentials\"

# []{#dbus_p2pdevice .anchor} fi.w1.wpa_supplicant1.Interface.P2PDevice

Interface for performing P2P (Wi-Fi Peer-to-Peer) P2P Device operations.

## []{#dbus_p2pdevice_methods .anchor} Methods

- ### Find ( a{sv} : args ) --\> nothing

  Start P2P find operation (i.e., alternating P2P Search and Listen
  states to discover peers and be discoverable).

  #### Arguments

  a{sv} : args
  :   A dictionary with parameters for the P2P find operation:
        Key                    Value type   Description                                                                    Required
        ---------------------- ------------ ------------------------------------------------------------------------------ ----------
        Timeout                i            Timeout for operating in seconds                                               no
        RequestedDeviceTypes   aay          WPS Device Types to search for                                                 no
        DiscoveryType          s            \"start_with_full\" (default, if not specified), \"social\", \"progressive\"   no

- ### StopFind ( nothing ) --\> nothing

  Stop P2P find operation.

- ### Listen ( i : timeout ) --\> nothing

  Start P2P listen operation (i.e., be discoverable).

  #### Arguments

  i : timeout
  :   Timeout in seconds for stopping the listen operation.

- ### ExtendedListen ( a{sv} : args ) --\> nothing

  Configure Extended Listen Timing. If the parameters are omitted, this
  feature is disabled. If the parameters are included, Listen State will
  be entered every interval msec for at least period msec. Both values
  have acceptable range of 1-65535 (with interval obviously having to be
  larger than or equal to duration). If the P2P module is not idle at
  the time the Extended Listen Timing timeout occurs, the Listen State
  operation will be skipped.

  #### Arguments

  a{sv} : args
  :   A dictionary with parameters for extended listen. Leave out all
      items to disable extended listen.
        Key        Value type   Description                                          Required
        ---------- ------------ ---------------------------------------------------- ----------
        period     i            Extended listen period in milliseconds; 1-65535.     no
        interval   i            Extended listen interval in milliseconds; 1-65535.   no

- ### PresenceRequest ( a{sv} : args ) --\> nothing

  Request a specific GO presence in a P2P group where the local device
  is a P2P Client. Send a P2P Presence Request to the GO (this is only
  available when acting as a P2P client). If no duration/interval pairs
  are given, the request indicates that this client has no special needs
  for GO presence. The first parameter pair gives the preferred duration
  and interval values in microseconds. If the second pair is included,
  that indicates which value would be acceptable.

  Note
  :   This needs to be issued on a P2P group interface if separate group
      interfaces are used.

  <!-- -->

  **[Bug:](bug.html#_bug000001){.el}**
  :   It would be cleaner to not require .P2PDevice methods to be issued
      on a group interface. In other words, args\[\'group_object\'\]
      could be used to specify the group or this method could be moved
      to be a .Group PresenceRequest() method.

  #### Arguments

  a{sv} : args
  :   A dictionary with parameters for the presence request.
        Key         Value type   Description                 Required
        ----------- ------------ --------------------------- ----------
        duration1   i            Duration in microseconds.   no
        interval1   i            Interval in microseconds.   no
        duration2   i            Duration in microseconds.   no
        interval2   i            Interval in microseconds.   no

- ### ProvisionDiscoveryRequest ( o : peer, s : config_method ) --\> nothing

- ### Connect ( a{sv} : args ) --\> s : generated_pin

  Request a P2P group to be started through GO Negotiation or by joining
  an already operating group.

  #### Arguments

  a{sv} : args
  :   A dictionary with parameters for the requested connection:
        Key              Value type   Description                                                                                 Required
        ---------------- ------------ ------------------------------------------------------------------------------------------- ----------
        peer             o                                                                                                        yes
        persistent       b            Whether to form a persistent group.                                                         no
        join             b            Whether to join an already operating group instead of forming a new group.                  no
        authorize_only   b            Whether to authorize a peer to initiate GO Negotiation instead of initiating immediately.   no
        frequency        i            Operating frequency in MHz                                                                  no
        go_intent        i            GO intent 0-15                                                                              no
        wps_method       s            \"pbc\", \"display\", \"keypad\", \"pin\" (alias for \"display\")                           yes
        pin              s                                                                                                        no

- ### GroupAdd ( a{sv} : args ) --\> nothing

  Request a P2P group to be started without GO Negotiation.

  #### Arguments

  a{sv} : args
  :   A dictionary with parameters for the requested group:
        Key                       Value type   Description                           Required
        ------------------------- ------------ ------------------------------------- ----------
        persistent                b            Whether to form a persistent group.   no
        persistent_group_object   o                                                  no
        frequency                 i            Operating frequency in MHz            no

- ### Cancel ( nothing ) --\> nothing

  Stop ongoing P2P group formation operation.

- ### Invite ( a{sv} : args ) --\> nothing

  Invite a peer to join an already operating group or to re-invoke a
  persistent group.

  #### Arguments

  a{sv} : args
  :   A dictionary with parameters for the invitation:
        Key                       Value type   Description   Required
        ------------------------- ------------ ------------- ----------
        peer                      o                          yes
        persistent_group_object   o                          no

- ### Disconnect ( nothing ) --\> nothing

  Terminate a P2P group.

  Note
  :   This needs to be issued on a P2P group interface if separate group
      interfaces are used.

  <!-- -->

  **[Bug:](bug.html#_bug000002){.el}**
  :   It would be cleaner to not require .P2PDevice methods to be issued
      on a group interface. In other words, this would either need to be
      Disconnect(group_object) or moved to be a .Group Disconnect()
      method.

- ### RejectPeer ( o : peer ) --\> nothing

  Reject connection attempt from a peer (specified with a device
  address). This is a mechanism to reject a pending GO Negotiation with
  a peer and request to automatically block any further connection or
  discovery of the peer.

- ### RemoveClient ( a{sv} : args ) --\> nothing

  Remove the client from all groups (operating and persistent) from the
  local GO.

  #### Arguments

  a{sv} : args
  :   A dictionary with parameters for removing a client:
        Key     Value type   Description                                                                                                        Required
        ------- ------------ ------------------------------------------------------------------------------------------------------------------ ----------
        peer    o            Object path for peer\'s P2P Device Address                                                                         yes
        iface   s            Interface address\[MAC Address format\] of the peer to be disconnected. Required if object path is not provided.   no

- ### Flush ( nothing ) --\> nothing

  Flush P2P peer table and state.

- ### AddService ( a{sv} : args ) --\> nothing

  #### Arguments

  a{sv} : args
  :   A dictionary with parameters for the service:
        Key            Value type   Description                   Required
        -------------- ------------ ----------------------------- ----------
        service_type   s            \"upnp\", \"bonjour\"         yes
        version        u            Required for UPnP services.   no
        service        s                                          
        query          ay                                         
        response       ay                                         

- ### DeleteService ( a{sv} : args ) --\> nothing

  #### Arguments

  a{sv} : args
  :   A dictionary with parameters for the service:
        Key            Value type   Description                   Required
        -------------- ------------ ----------------------------- ----------
        service_type   s            \"upnp\", \"bonjour\"         yes
        version        u            Required for UPnP services.   no
        service        s                                          
        query          ay                                         

- ### FlushService ( nothing ) --\> nothing

- ### ServiceDiscoveryRequest ( a{sv} : args ) --\> t : ref

  #### Arguments

  a{sv} : args
  :   A dictionary with following parameters:
        Key            Value type   Description                   Required
        -------------- ------------ ----------------------------- ----------
        peer_object    o                                          no
        service_type   s            \"upnp\"                      no
        version        u            Required for UPnP services.   no
        service        s                                          
        tlv            ay                                         

- ### ServiceDiscoveryResponse ( a{sv} : args ) --\> nothing : ref

  #### Arguments

  a{sv} : args
  :   A dictionary with following parameters:
        Key            Value type   Description   Required
        -------------- ------------ ------------- ----------
        peer_object    o                          yes
        frequency      i                          yes
        dialog_token   i                          yes
        tlvs           ay                         yes

- ### ServiceDiscoveryCancelRequest ( t : args ) --\> nothing : ref

- ### ServiceUpdate ( nothing ) --\> nothing

- ### ServiceDiscoveryExternal ( i : arg ) --\> nothing

- ### AddPersistentGroup ( a{sv} : args ) --\> o : path

  #### Arguments

  a{sv} : args
  :   A dictionary with following parameters:
        Key     Value type   Description                                                                                              Required
        ------- ------------ -------------------------------------------------------------------------------------------------------- ----------
        bssid   s            P2P Device Address of the GO in the persistent group.                                                    yes
        ssid    s            SSID of the group                                                                                        yes
        psk     s            Passphrase (on the GO and optionally on P2P Client) or PSK (on P2P Client if passphrase ise not known)   yes
        mode    s            \"3\" on GO or \"0\" on P2P Client                                                                       yes

- ### RemovePersistentGroup ( o : path ) --\> nothing

- ### RemoveAllPersistentGroups ( nothing ) --\> nothing

## []{#dbus_p2pdevice_properties .anchor} Properties

- ### P2PDeviceConfig - a{sv} - (read/write)

  Dictionary with following entries. On write, only the included values
  are changed.

    Key                    Value type   Description
    ---------------------- ------------ -------------
    DeviceName             s            
    PrimaryDeviceType      ay           
    SecondaryDeviceTypes   aay          
    VendorExtension        aay          
    GOIntent               u            
    PersistentReconnect    b            
    ListenRegClass         u            
    ListenChannel          u            
    OperRegClass           u            
    OperChannel            u            
    SsidPostfix            s            
    IntraBss               b            
    GroupIdle              u            
    disassoc_low_ack       u            
    NoGroupIface           b            
    p2p_search_delay       u            

- ### Peers - ao - (read)

- ### Role - s - (read)

  **[Bug:](bug.html#_bug000003){.el}**
  :   What is this trying to indicate? It does not make much sense to
      have a P2PDevice property role since there can be multiple
      concurrent groups and the P2P Device role is always active anyway.

- ### Group - o - (read)

  **[Bug:](bug.html#_bug000004){.el}**
  :   What is this trying to indicate? It does not make much sense to
      have a P2PDevice property Group since there can be multiple
      concurrent groups.

- ### PeerGO - o - (read)

  **[Bug:](bug.html#_bug000005){.el}**
  :   What is this trying to indicate? It does not make much sense to
      have a P2PDevice property PeerGO since there can be multiple
      concurrent groups.

- ### PersistentGroups - ao - (read)

## []{#dbus_p2pdevice_signals .anchor} Signals

- ### DeviceFound ( o : path )

- ### DeviceLost ( o : path )

- ### FindStopped ( )

- ### ProvisionDiscoveryRequestDisplayPin ( o : peer_object, s : pin )

- ### ProvisionDiscoveryResponseDisplayPin ( o : peer_object, s : pin )

- ### ProvisionDiscoveryRequestEnterPin ( o : peer_object )

- ### ProvisionDiscoveryResponseEnterPin ( o : peer_object )

- ### ProvisionDiscoveryPBCRequest ( o : peer_object )

- ### ProvisionDiscoveryPBCResponse ( o : peer_object )

- ### ProvisionDiscoveryFailure ( o : peer_object, i : status )

- ### GroupStarted ( a{sv} : properties )

  A new P2P group was started or joined.

  #### Arguments

  a{sv} : properties
  :   A dictionary with following information on the added group:
        Key                Value type   Description
        ------------------ ------------ ----------------------------------------------------------------------------------------------------------------------------------------
        interface_object   o            D-Bus path of the interface on which this group is operating on. See [fi.w1.wpa_supplicant1.Interface](dbus.html#dbus_interface){.el}.
        role               s            The role of the local device in the group: \"GO\" or \"client\".
        group_object       o            D-Bus path of the group. See [fi.w1.wpa_supplicant1.Group](dbus.html#dbus_group){.el}.

- ### GONegotiationSuccess ( a{sv} : properties )

  #### Arguments

  a{sv} : properties
  :   A dictionary with following information:
        Key                   Value type   Description
        --------------------- ------------ -------------------------------------------------------------------------------------
        peer_object           o            D-Bus path of the peer. See [fi.w1.wpa_supplicant1.Peer](dbus.html#dbus_peer){.el}.
        status                i            
        passphrase            s            Passphrase for the group. Included only if this device becomes the GO of the group.
        role_go               s            The role of the local device in the group: \"GO\" or \"client\".
        ssid                  ay           
        peer_device_addr      ay           
        peer_interface_addr   ay           
        wps_method            s            
        frequency_list        ai           
        persistent_group      i            
        peer_config_timeout   u            

- ### GONegotiationFailure ( a{sv} : properties )

  #### Arguments

  a{sv} : properties
  :   A dictionary with following information:
        Key           Value type   Description
        ------------- ------------ -------------------------------------------------------------------------------------
        peer_object   o            D-Bus path of the peer. See [fi.w1.wpa_supplicant1.Peer](dbus.html#dbus_peer){.el}.
        status        i            

- ### GONegotiationRequest ( o : path, q : dev_passwd_id, y : device_go_intent )

- ### InvitationResult ( a{sv} : invite_result )

  #### Arguments

  a{sv} : invite_result
  :   A dictionary with following information:
        Key      Value type   Description
        -------- ------------ --------------------
        status   i            
        BSSID    ay           Optionally present

- ### GroupFinished ( a{sv} : properties )

  A P2P group was removed.

  #### Arguments

  a{sv} : properties
  :   A dictionary with following information of the removed group:
        Key                Value type   Description
        ------------------ ------------ ----------------------------------------------------------------------------------------------------------------------------------------
        interface_object   o            D-Bus path of the interface on which this group is operating on. See [fi.w1.wpa_supplicant1.Interface](dbus.html#dbus_interface){.el}.
        role               s            The role of the local device in the group: \"GO\" or \"client\".
        group_object       o            D-Bus path of the group. See [fi.w1.wpa_supplicant1.Group](dbus.html#dbus_group){.el}.

- ### ServiceDiscoveryRequest ( a{sv} : sd_request )

  #### Arguments

  a{sv} : sd_request
  :   A dictionary with following information:
        ------------------ ---- --
        peer_object        o    
        frequency          i    
        dialog_token       i    
        update_indicator   q    
        tlvs               ay   
        ------------------ ---- --

- ### ServiceDiscoveryResponse ( a{sv} : sd_response )

  #### Arguments

  a{sv} : sd_response
  :   A dictionary with following information:
        ------------------ ---- --
        peer_object        o    
        update_indicator   q    
        tlvs               ay   
        ------------------ ---- --

- ### PersistentGroupAdded ( o : path, a{sv} : properties )

  #### Arguments

  o : path
  :   D-Bus object path for the persistent group. See
      [fi.w1.wpa_supplicant1.PersistentGroup](dbus.html#dbus_persistent_group){.el}.

  a{sv} : properties
  :   A dictionary with following information:
        Key        Value type   Description
        ---------- ------------ --------------------------------------------------------------------------------------------------------
        bssid      s            P2P Device Address of the GO in the persistent group.
        ssid       s            SSID of the group
        psk        s            Passphrase (on the GO and optionally on P2P Client) or PSK (on P2P Client if passphrase ise not known)
        disabled   s            Set to \"2\" to indicate special network block use as a P2P persistent group information
        mode       s            \"3\" on GO or \"0\" on P2P Client

- ### PersistentGroupRemoved ( o : path )

  #### Arguments

  o : path
  :   D-Bus object path for the persistent group. See
      [fi.w1.wpa_supplicant1.PersistentGroup](dbus.html#dbus_persistent_group){.el}.

- ### WpsFailed ( s : name, a{sv} : args )

  #### Arguments

  s : name
  :   \"fail\"

  a{sv} : args
  :   A dictionary with following information:
        Key            Value type   Description
        -------------- ------------ -------------
        msg            i            
        config_error   n            

- ### InvitationReceived ( a{sv} : properties )

  #### Arguments

  a{sv} : properties
  :   A dictionary with following information:
        Key             Value type   Description
        --------------- ------------ --------------------
        sa              ay           Optionally present
        go_dev_addr     ay           Optionally present
        bssid           ay           Optionally present
        persistent_id   i            Optionally present
        op_freq         i            

- ### GroupFormationFailure ( s : reason )

  #### Arguments

  s : reason
  :   Reason for failure or empty string if not known.

# []{#dbus_bss .anchor} fi.w1.wpa_supplicant1.BSS

Interface implemented by objects representing a scanned BSSs, i.e., scan
results.

## []{#dbus_bss_properties .anchor} Properties

- ### BSSID - ay - (read)

  BSSID of the BSS.

- ### SSID - ay - (read)

  SSID of the BSS.

- ### WPA - a{sv} - (read)

  WPA information of the BSS. Empty dictionary indicates no WPA support.
  Dictionary entries are:

    ---------- ---- ---------------------------------------------------------------------------------------
    KeyMgmt    as   Key management suite. Possible array elements: \"wpa-psk\", \"wpa-eap\", \"wpa-none\"
    Pairwise   as   Pairwise cipher suites. Possible array elements: \"ccmp\", \"tkip\"
    Group      s    Group cipher suite. Possible values are: \"ccmp\", \"tkip\", \"wep104\", \"wep40\"
    ---------- ---- ---------------------------------------------------------------------------------------

- ### RSN - a{sv} - (read)

  RSN information of the BSS. Empty dictionary indicates no RSN support.
  Dictionary entries are:

    ----------- ---- --------------------------------------------------------------------------------------------------------------------------------------------------
    KeyMgmt     as   Key management suite. Possible array elements: \"wpa-psk\", \"wpa-eap\", \"wpa-ft-psk\", \"wpa-ft-eap\", \"wpa-psk-sha256\", \"wpa-eap-sha256\",
    Pairwise    as   Pairwise cipher suites. Possible array elements: \"ccmp\", \"tkip\"
    Group       s    Group cipher suite. Possible values are: \"ccmp\", \"tkip\", \"wep104\", \"wep40\"
    MgmtGroup   s    Mangement frames cipher suite. Possible values are: \"aes128cmac\"
    ----------- ---- --------------------------------------------------------------------------------------------------------------------------------------------------

- ### WPS - a{sv} - (read)

  WPS information of the BSS. Empty dictionary indicates no WPS support.
  Dictionary entries are:

    ------ --- ------------------------
    Type   s   \"pbc\", \"pin\", \"\"
    ------ --- ------------------------

- ### IEs - ay - (read)

  All IEs of the BSS as a chain of TLVs

- ### Privacy - b - (read)

  Indicates if BSS supports privacy.

- ### Mode - s - (read)

  Describes mode of the BSS. Possible values are: \"ad-hoc\" and
  \"infrastructure\".

- ### Frequency - q - (read)

  Frequency of the BSS in MHz.

- ### Rates - au - (read)

  Descending ordered array of rates supported by the BSS in bits per
  second.

- ### Signal - n - (read)

  Signal strength of the BSS.

- ### Age - u - (read)

  Number of seconds since the BSS was last seen.

## []{#dbus_bss_signals .anchor} Signals

- ### PropertiesChanged ( a{sv} : properties )

  Some properties have changed.

  #### Arguments

  a{sv} : properties
  :   A dictionary with pairs of properties names which have changed and
      theirs new values.

# []{#dbus_network .anchor} fi.w1.wpa_supplicant1.Network

Interface implemented by objects representing configured networks, i.e.,
returned by fi.w1.wpa_supplicant1.Interface.AddNetwork.

## []{#dbus_network_properties .anchor} Properties

- ### Enabled - b - (read/write)

  Determines if the configured network is enabled or not.

- ### Properties - a{sv} - (read/write)

  Properties of the configured network. Dictionary contains entries from
  \"network\" block of wpa_supplicant configuration file. All values are
  string type, e.g., frequency is \"2437\", not 2437.

## []{#dbus_network_signals .anchor} Signals

- ### PropertiesChanged ( a{sv} : properties )

  Some properties have changed.

  #### Arguments

  a{sv} : properties
  :   A dictionary with pairs of properties names which have changed and
      theirs new values. Possible dictionary keys are: \"Enabled\"

# []{#dbus_peer .anchor} fi.w1.wpa_supplicant1.Peer

Interface implemented by objects representing P2P peer devices.

## []{#dbus_peer_properties .anchor} Properties

- ### DeviceName - s - (read)

- ### Manufacturer - s - (read)

- ### ModelName - s - (read)

- ### ModelNumber - s - (read)

- ### SerialNumber - s - (read)

- ### PrimaryDeviceType - ay - (read)

- ### config_method - q - (read)

- ### level - i - (read)

- ### devicecapability - y - (read)

- ### groupcapability - y - (read)

  Group Capability field from the last frame from which this peer
  information was updated.

  Note
  :   This field is only for debugging purposes and must not be used to
      determine whether the peer happens to be operating a group as a GO
      at the moment.

- ### SecondaryDeviceTypes - aay - (read)

- ### VendorExtension - aay - (read)

- ### IEs - ay - (read)

  This is a confusingly named property that includes Wi-Fi Display
  subelements from the peer.

  **[Bug:](bug.html#_bug000006){.el}**
  :   This should really be renamed since \"IEs\" means something
      completely different..

- ### DeviceAddress - ay - (read)

  The P2P Device Address of the peer.

- ### Groups - ao - (read)

  The current groups in which this peer is connected.

## []{#dbus_peer_signals .anchor} Signals

- ### PropertiesChanged ( a{sv} : properties )

  Some properties have changed.

  **[Deprecated:](deprecated.html#_deprecated000001){.el}**
  :   Use org.freedesktop.DBus.Properties.PropertiesChanged instead.

  <!-- -->

  **[Todo:](todo.html#_todo000001){.el}**
  :   Explain how ProertiesChanged signals are supposed to be of any
      real use with Peer objects (i.e., one signal for multiple peers).

  #### Arguments

  a{sv} : properties
  :   A dictionary with pairs of properties names which have changed and
      their new values.

# []{#dbus_group .anchor} fi.w1.wpa_supplicant1.Group

Interface implemented by objects representing active P2P groups.

## []{#dbus_group_properties .anchor} Properties

- ### Members - ao - (read)

  Array of D-Bus object paths for the peer devices that are currently
  connected to the group. This is valid only on the GO device. An empty
  array is returned in P2P Client role.

- ### Group - o - (read)

  **[Todo:](todo.html#_todo000002){.el}**
  :   Why is this here? This D-Bus object path is to this specific group
      and one needs to know it to fetching this information in the first
      place..

- ### Role - s - (read)

  The role of this device in the group: \"GO\", \"client\".

- ### SSID - ay - (read)

  P2P Group SSID.

- ### BSSID - ay - (read)

  P2P Group BSSID (the P2P Interface Address of the GO).

- ### Frequency - q - (read)

  The frequency (in MHz) of the group operating channel.

- ### Passphrase - s - (read)

  Passphrase used in the group. This is always available on the GO. For
  P2P Client role, this may be available depending on whether the peer
  GO provided the passphrase during the WPS provisioning step. If not
  available, an empty string is returned.

- ### PSK - ay - (read)

  PSK used in the group.

- ### WPSVendorExtensions - aay - (read/write)

  WPS vendor extension attributes used on the GO. This is valid only the
  in the GO role. An empty array is returned in P2P Client role. At
  maximum, 10 separate vendor extension byte arrays can be configured.
  The GO device will include the configured attributes in WPS exchanges.

## []{#dbus_group_signals .anchor} Signals

- ### PeerJoined ( o : peer )

  A peer device has joined the group. This is indicated only on the GO
  device.

  #### Arguments

  o : peer
  :   A D-Bus path to the object representing the peer. See
      [fi.w1.wpa_supplicant1.Peer](dbus.html#dbus_peer){.el}.

- ### PeerDisconnected ( o : peer )

  A peer device has left the group. This is indicated only on the GO
  device.

  #### Arguments

  o : peer
  :   A D-Bus path to the object representing the peer. See
      [fi.w1.wpa_supplicant1.Peer](dbus.html#dbus_peer){.el}.

# []{#dbus_persistent_group .anchor} fi.w1.wpa_supplicant1.PersistentGroup

Interface implemented by objects representing persistent P2P groups.

## []{#dbus_persistent_group_properties .anchor} Properties

- ### Properties - a{sv} - (read/write)

  Properties of the persistent group. These are same properties as in
  the [fi.w1.wpa_supplicant1.Network](dbus.html#dbus_network){.el}. When
  writing this, only the entries to be modified are included, i.e., any
  item that is not included will be left at its existing value. The
  following entries are used for persistent groups:

    Key        Value type   Description
    ---------- ------------ --------------------------------------------------------------------------------------------------------
    bssid      s            P2P Device Address of the GO in the persistent group.
    ssid       s            SSID of the group
    psk        s            Passphrase (on the GO and optionally on P2P Client) or PSK (on P2P Client if passphrase ise not known)
    disabled   s            Set to \"2\" to indicate special network block use as a P2P persistent group information
    mode       s            \"3\" on GO or \"0\" on P2P Client
:::
::::

------------------------------------------------------------------------

[Generated on Sun Sep 27 2015 22:08:09 for wpa_supplicant / hostapd by  
[![doxygen](doxygen.png){.footer}](http://www.doxygen.org/index.html)
1.8.6]{.small}
