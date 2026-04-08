# Linux网络工具杂谈

## 关键概念

- NetworkManager
- wpa_cli
- wpa_supplicant
- dbus
- dbus api
- 无线网卡



## 关系图

- 用户编程应用 → NetworkManager → wpa_supplicant → 网卡
```mermaid
graph TD
    A[用户应用 / 脚本 / nmcli / GUI] -->|D-Bus API| B[NetworkManager]
    A -->|D-Bus API| C[wpa_supplicant]
    B -->|D-Bus API| C[wpa_supplicant]
    B -->|通过 D-Bus 总线通信| D[D-Bus 守护进程]
    C -->|通过 D-Bus 总线通信| D
    A -->|通过 D-Bus 总线通信| D
    C -->|底层驱动调用| E[无线网卡驱动 / 内核]
    B -->|管理| F[网络配置: IP / 路由 / DNS]
```






- wpa_cli与NetworkManager对wpa_supplicant通信机制的区别

```mermaid
graph LR
    A[wpa_cli] -->|Unix Domain Socket| B[wpa_supplicant]
    C[NetworkManager] -->|D-Bus| B
    D[开发者应用] -->|D-Bus| B
    D -->|也可以用 Unix Socket| B
```

## 参考

NetworkManager官方发布页：https://networkmanager.dev/tags/release/(里面下载的是对应版本的程序源码)

wpa_supplicant官方发布页：https://www.linuxfromscratch.org/blfs/view/11.1/basicnet/wpa_supplicant.html(里面下载是源码)

D-bus官网：https://www.freedesktop.org/wiki/Software/dbus/

D-bus api reference：https://people.freedesktop.org/~lkundrak/nm-dbus-api/spec.html