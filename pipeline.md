# 流程Demo

- 确认NetworkManager的运行
- 获取Wi-Fi p2p 设备的虚拟接口路径
- 使用p2p接口启动p2p发现
- 匹配Mac地址、DeviceName确定设备
- 发起p2p连接，等待对端设备pbc确认
- 确认连接建立
- 建立Tcp连接
- 数据传输
- 结束，关闭新生成的p2p接口