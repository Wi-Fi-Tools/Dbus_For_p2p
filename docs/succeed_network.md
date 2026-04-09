- 1
  ```shell
  sudo busctl call org.freedesktop.NetworkManager \
  /org/freedesktop/NetworkManager/Devices/3 \
  org.freedesktop.NetworkManager.Device.WifiP2P \
  StartFind \
  "a{sv}" 1 "timeout" i 600 

  ```
- 2
  ```shell
  sudo busctl get-property org.freedesktop.NetworkManager \
  /org/freedesktop/NetworkManager/Devices/3 \
  org.freedesktop.NetworkManager.Device.WifiP2P \
  Peers
  ```

- 3
  ```shell
  sudo busctl introspect org.freedesktop.NetworkManager \
  /org/freedesktop/NetworkManager/WifiP2PPeer/3 
  ```


- 4
  ```shell
  sudo busctl call org.freedesktop.NetworkManager \ 
  /org/freedesktop/NetworkManager \
  org.freedesktop.NetworkManager \
  AddAndActivateConnection \
  "a{sa{sv}}oo" \
  4 \
    "connection" 3 \
      "id" v "s" "wifi-p2p-connection" \
      "type" v "s" "wifi-p2p" \
      "autoconnect" v "b" false \
    "wifi-p2p" 1 \
      "peer" v "s" "62:4B:7C:9E:06:7E" \ # peer的Mac地址
    "ipv4" 1 \
      "method" v "s" "auto" \
    "ipv6" 1 \
      "method" v "s" "auto" \
  "/org/freedesktop/NetworkManager/Devices/3" \
  "/org/freedesktop/NetworkManager/WifiP2PPeer/3"

  ```