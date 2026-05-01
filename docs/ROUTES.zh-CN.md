# 🧭 路线对比与技术说明

> 本文用于解释 Reality Route Helper 中涉及或计划支持的几条路线。  
> 主项目第一版只实现 **Xray / VLESS + Reality**，其他路线先作为检测、说明或后续扩展方向。

---

## 1. 总览表

| 路线 | 当前状态 | 主要协议/核心 | 优点 | 风险/复杂点 | 适合人群 |
|---|---|---|---|---|---|
| Xray / VLESS + Reality | ✅ 已实现 | Xray-core、VLESS、Reality、TCP | 可控性强，适合手动理解和维护 | 字段较多，新手容易填错 | 想理解配置、自己维护 VPS 的用户 |
| Outline / Shadowsocks | 🔎 检测中 | Outline Server、Shadowsocks | 最易上手，Outline Manager 体验好 | 灵活性和协议选择不如 Xray 路线 | 只想快速给自己/朋友使用的人 |
| Hysteria2 | 🗓️ 计划中 | QUIC、UDP、Hysteria2 | 在部分高延迟/丢包网络下表现好 | UDP 可用性依赖网络环境 | 网络质量差、想尝试 UDP 路线的人 |
| TUIC | 🗓️ 计划中 | QUIC、TCP/UDP relay | 低握手延迟，UDP 能力强 | 客户端/服务端生态需要确认 | 想尝试现代 QUIC 代理的人 |
| sing-box | 🗓️ 计划中 | Universal proxy platform | 统一客户端/服务端配置能力强 | 配置项多，学习成本较高 | 需要多协议统一管理的人 |
| 3x-ui / Marzban / Hiddify | 🗓️ 计划中 | Xray-core 管理面板、多用户管理 | Web 管理、流量统计、订阅方便 | 增加管理端口和面板安全风险 | 用户较多、需要面板管理的人 |

---

## 2. Xray / VLESS + Reality

### 简介

Xray-core 是 Project X 的核心组件之一，Project X 也包含 REALITY 等网络工具。VLESS 是一种轻量、无状态的传输协议，认证方式使用 UUID。Reality 则是 Xray 生态中常见的安全层方案，通常和 VLESS、TCP、XTLS Vision flow 一起使用。

### 本项目当前实现内容

Reality Route Helper 当前已经支持：

- 检测 Xray 是否安装；
- 生成 UUID 用户；
- 生成 Reality x25519 密钥；
- 生成服务端 `config.json`；
- 写入前备份；
- 测试 Xray 配置；
- 重启 Xray；
- 检查端口监听；
- 生成 v2rayN 导入链接；
- 新增用户 UUID；
- Windows / Linux 沙盒测试。

### 典型配置关键词

```text
VLESS
Reality
xtls-rprx-vision
UUID
PrivateKey / PublicKey
shortIds / shortId
serverNames / SNI
```

### 适合场景

- 想从 Outline 迁移到更可控的配置；
- 想给不同设备/朋友分配不同 UUID；
- 想保留纯配置文件方式，而不是引入面板；
- 想理解每个字段的含义。

### 注意事项

- PrivateKey 不应公开；
- 每个人/设备建议单独 UUID；
- `shortIds` 是服务端数组，客户端通常填写其中一个 `shortId`；
- `443` 不一定在所有网络可用，必要时可测试 `8443` 等端口；
- 配置测试与重启应分开执行，避免写错后服务无法启动。

### 参考链接

- Xray-core: https://github.com/XTLS/Xray-core
- VLESS inbound: https://xtls.github.io/en/config/inbounds/vless.html
- VLESS outbound: https://xtls.github.io/en/config/outbounds/vless.html
- REALITY: https://github.com/XTLS/REALITY

---

## 3. Outline / Shadowsocks

### 简介

Outline Server 是 Outline 体系中的服务端组件，提供 Shadowsocks 服务和服务管理 API；Outline Manager 则用于部署服务器、管理访问密钥和查看资源使用情况。

### 优点

- 上手简单；
- Outline Manager 图形化体验好；
- 适合快速分发 access key；
- 对普通用户友好。

### 局限

- 和 Xray / VLESS + Reality 不是同一套协议体系；
- Outline Manager 不能管理 Xray Reality 节点；
- 进阶配置灵活性不如纯 Xray 配置或面板路线。

### 本项目当前状态

Reality Route Helper 当前只做：

```text
检测 Docker / Outline 相关容器
提示用户 Outline 与 Xray 是不同体系
不默认停止 Outline
不接管 Outline 配置
```

后续可扩展：

- 检测 `shadowbox` / `watchtower` 容器；
- 给出继续使用 Outline 或迁移到 VLESS + Reality 的建议；
- 提供安全暂停 Outline 的提示，但不自动停止。

### 参考链接

- Outline Server: https://github.com/OutlineFoundation/outline-server
- Outline Shadowsocks notes: https://github.com/Jigsaw-Code/outline-server/blob/master/docs/shadowsocks.md

---

## 4. Hysteria2

### 简介

Hysteria2 是基于 QUIC 的 TCP/UDP 代理协议，设计目标包括速度、安全和抗干扰能力。它常被用于高延迟、丢包网络场景，依赖 UDP。

### 优点

- QUIC/UDP 路线；
- 在部分丢包网络中可能有更好表现；
- 支持多种模式，例如 SOCKS5、HTTP Proxy、TCP/UDP Forwarding、TUN 等；
- 配置通常以 YAML 为主，结构相对清晰。

### 风险/限制

- UDP 在部分网络、运营商、机房可能被限制；
- QUIC/UDP 协议特征和 TCP 路线不同，不一定适合所有环境；
- 用户需要理解带宽、拥塞控制、伪装站点等配置。

### 本项目后续可能实现

- 生成 Hysteria2 server/client YAML；
- 检测 UDP 端口连通性；
- 生成常见客户端配置；
- 加入与 VLESS + Reality 的场景对比。

### 参考链接

- Hysteria GitHub: https://github.com/apernet/hysteria
- Hysteria 2 protocol: https://v2.hysteria.network/docs/developers/Protocol/
- Hysteria full server config: https://v2.hysteria.network/docs/advanced/Full-Server-Config/

---

## 5. TUIC

### 简介

TUIC 是一个基于 QUIC 的标准化代理协议，用于转发 TCP 和 UDP 流量，设计目标包括 0-RTT、UDP 代理能力、Full Cone NAT 兼容和利用 QUIC 的连接迁移、多路复用等能力。

### 优点

- QUIC 路线；
- 支持 TCP 和 UDP relay；
- 强调低握手延迟；
- 协议设计较现代。

### 风险/限制

- 生态和客户端支持需要实际验证；
- UDP 可用性依赖网络环境；
- 对普通新手来说概念会比 Outline 更复杂。

### 本项目后续可能实现

- 检测服务器 UDP 可用性；
- 生成 TUIC server/client 配置；
- 与 Hysteria2、VLESS + Reality 进行场景对比。

### 参考链接

- TUIC Protocol: https://github.com/tuic-protocol/tuic

---

## 6. sing-box

### 简介

sing-box 官方定位是 universal proxy platform。它不是单一协议，而是一个统一代理平台，支持多种 inbound/outbound 和代理协议，适合做客户端/服务端统一配置。

### 优点

- 多协议统一配置；
- 客户端和服务端都可使用；
- 适合后续生成 Android / iOS / 桌面端配置；
- 可作为多路线统一出口。

### 风险/限制

- 配置能力强，但配置量也更大；
- 新手理解成本更高；
- 需要明确哪些路线由 sing-box 原生实现，哪些路线由 Xray 实现。

### 本项目后续可能实现

- 生成 sing-box 客户端配置；
- 生成 sing-box outbound；
- 给 Hiddify 等 sing-box 客户端提供配置参考；
- 作为多路线统一配置导出目标。

### 参考链接

- sing-box Home: https://sing-box.sagernet.org/
- sing-box inbound docs: https://sing-box.sagernet.org/configuration/inbound/
- sing-box outbound docs: https://sing-box.sagernet.org/configuration/outbound/
- sing-box GitHub: https://github.com/SagerNet/sing-box

---

## 7. 3x-ui / Marzban / Hiddify

### 简介

这类工具属于 Web 面板或多用户管理平台，通常用于管理 Xray-core 或多协议代理用户。

### 优点

- 图形化；
- 用户管理方便；
- 可查看流量；
- 生成订阅链接方便；
- 适合多人使用场景。

### 风险/限制

- 面板本身也需要安全维护；
- 管理端口暴露会带来额外风险；
- 弱密码、默认端口、HTTP 管理面板都可能造成安全问题；
- 可能接管或覆盖手写配置。

### 本项目态度

Reality Route Helper 第一阶段不默认安装面板。后续更适合做：

```text
检测是否存在面板
提示安全建议
提供迁移建议
提供“纯配置文件 vs 面板”的对比
```

而不是一开始就把用户引向面板。

### 参考链接

- 3x-ui: https://github.com/MHSanaei/3x-ui
- Marzban: https://github.com/Gozargah/Marzban
- Hiddify Manager: https://github.com/hiddify/Hiddify-Manager
- Hiddify Manager guide: https://hiddify.com/manager/

---

## 8. 当前优先级建议

Reality Route Helper 后续路线建议：

```text
v0.1.x：打磨 VLESS + Reality、测试、文档、发布流程
v0.2.x：doctor、remove-user、rotate-key、install-xray
v0.3.x：Outline 检测增强与迁移建议
v0.4.x：sing-box 客户端配置生成
v0.5.x：Hysteria2 / TUIC 路线
v1.0.x：多路线稳定版
```

---

## 9. 选择建议

### 只想快速可用

优先考虑：

```text
Outline / Shadowsocks
```

或未来面板路线。

### 想理解配置、可控性强

优先考虑：

```text
Xray / VLESS + Reality
```

### 网络高延迟、丢包明显

后续可以考虑：

```text
Hysteria2 / TUIC
```

### 想统一客户端配置

后续可以考虑：

```text
sing-box
```

### 管理很多用户

后续可以考虑：

```text
Marzban / Hiddify / 3x-ui
```

但需要格外注意面板安全。
