# 🧭 Reality Route Helper

[English](README.md) | [简体中文](README.zh-CN.md)

> 一个面向新手的双语网络连接路线助手。  
> 第一版重点实现：**Xray / VLESS + Reality**。  
> 后续可扩展：**Outline、Hysteria2、TUIC、sing-box、3x-ui / Marzban / Hiddify** 等方案。

---

## ✨ 项目愿景

很多教程只告诉你“复制这段命令”，但没有解释：

- 为什么服务端和客户端命令不一样？
- 为什么 Windows 上不能执行 Linux 指令？
- 为什么 `443` 不通但 `8443` 可以？
- UUID、Reality PrivateKey、PublicKey、shortId 分别是什么？
- Outline 和 Xray / VLESS + Reality 是否能用同一个管理器？
- 如何安全地给不同设备或朋友分配独立配置？
- 如何在不破坏真实服务器配置的前提下测试工具？

**Reality Route Helper** 希望做的不是黑箱式一键脚本，而是：

> 帮用户选择路线、理解配置、减少踩坑、保留备份、方便维护。

---

## 🚀 当前功能

### 🌍 通用能力

- 🌐 中文 / English 双语菜单
- 🖥️ 自动检测 Windows / Linux / macOS
- 🧭 支持选择本机角色：服务器端 / 客户端
- 🔎 扫描当前机器环境
- 📦 检测 Xray、Docker、Outline 等常见组件
- 🧩 内置多路线扩展框架
- 🛡️ 写入配置前自动备份
- 🧪 支持 Windows / Linux 沙盒测试
- 🔁 支持菜单流自动化测试，避免人工反复点菜单

### 🛰️ 服务器端能力

- ✅ 检测 Xray 是否安装
- ✅ 生成 Reality x25519 密钥
- ✅ 生成 UUID 用户
- ✅ 生成 VLESS + Reality 服务端配置
- ✅ 测试 Xray 配置文件
- ✅ 重启 Xray 服务
- ✅ 检查端口监听
- ✅ 根据当前配置生成 v2rayN 导入链接
- ✅ 新增 UUID 用户
- ✅ 通过环境变量将配置写入重定向到临时目录，避免误改真实配置

### 💻 客户端能力

- ✅ 生成 v2rayN 一键导入链接
- ✅ 测试服务器 TCP 端口连通性
- ✅ 根据当前系统给出对应操作提示

---

## 🧱 路线概览

| 路线 | 状态 | 难度 | 简要说明 |
|---|---|---:|---|
| Xray / VLESS + Reality | ✅ 已实现 | 中等 | 当前第一版重点路线，适合想理解和掌控配置的个人 VPS 用户 |
| Outline / Shadowsocks | 🔎 检测中 | 简单 | 易用，有 Outline Manager；当前只扫描，不接管 |
| Hysteria2 | 🗓️ 计划中 | 中等 | 基于 QUIC/UDP，适合部分高延迟或丢包网络 |
| TUIC | 🗓️ 计划中 | 中等 | 基于 QUIC 的 TCP/UDP 代理协议，强调低握手延迟和 UDP 能力 |
| sing-box | 🗓️ 计划中 | 中等 | 通用代理平台，适合未来做统一客户端/服务端配置 |
| 3x-ui / Marzban / Hiddify | 🗓️ 计划中 | 简单~中等 | Web 面板管理方便，但会增加管理端口与安全面 |

更详细的路线对比见：

- [路线对比与技术说明](docs/ROUTES.zh-CN.md)
- [架构说明](docs/ARCHITECTURE.zh-CN.md)
- [测试说明](docs/TESTING.zh-CN.md)
- [发布与在线临时运行](docs/DISTRIBUTION.zh-CN.md)
- [Roadmap](docs/ROADMAP.zh-CN.md)

---

## 📁 项目结构

```text
reality-route-helper/
├─ README.md
├─ README.zh-CN.md
├─ LICENSE
├─ pyproject.toml
├─ rrh.py
├─ reality_route_helper/
│  ├─ cli.py
│  ├─ i18n.py
│  ├─ core/
│  ├─ platforms/
│  ├─ routes/
│  ├─ scanners/
│  └─ templates/
├─ scripts/
│  ├─ run.ps1
│  ├─ run.sh
│  ├─ build-release.ps1
│  ├─ build-release.sh
│  └─ test-linux-sandbox.sh
├─ tests/
│  ├─ smoke_test.py
│  └─ menu_flow_test.py
├─ examples/
├─ docs/
└─ .github/
   └─ workflows/
      └─ release.yml
```

---

## 🐍 本地开发环境

推荐使用 Python 3.11：

```powershell
conda create -n rrh python=3.11 -y
conda activate rrh
python -m pip install -U pip setuptools wheel pyinstaller
```

当前项目在 Windows 上也已通过 Python 3.13.9 的本地沙盒测试；但为了打包兼容性，开发环境仍建议优先使用 Python 3.11。

运行项目：

```powershell
python rrh.py
```

Linux / macOS：

```bash
python3 rrh.py
```

模块方式：

```bash
python -m reality_route_helper
```

---

## 🧪 测试

Windows 本地安全测试：

```powershell
.\scripts\test-local.ps1
```

Linux 沙盒测试：

```bash
bash scripts/test-linux-sandbox.sh
```

当前已验证：

```text
Windows smoke test ✅
Windows menu flow test ✅
Ubuntu Linux sandbox test ✅
沙盒路径隔离 ✅
禁止真实重启 Xray ✅
不会误改真实配置 ✅
```

详细说明见：

- [测试说明](docs/TESTING.zh-CN.md)

---

## ⚡ 未来在线临时运行方式

发布 GitHub Releases 后，用户无需安装 Python。

### Linux / macOS

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/forgottenlab/reality-route-helper/main/scripts/run.sh)
```

### Windows PowerShell

```powershell
irm https://raw.githubusercontent.com/forgottenlab/reality-route-helper/main/scripts/run.ps1 | iex
```

运行逻辑：

1. 检测系统和 CPU 架构；
2. 从 GitHub Releases 下载对应单文件程序；
3. 放入临时目录；
4. 运行程序；
5. 程序退出后删除临时文件。

---

## 📦 计划发布文件名

```text
rrh-linux-amd64
rrh-linux-arm64
rrh-windows-amd64.exe
rrh-windows-arm64.exe
rrh-darwin-amd64
rrh-darwin-arm64
```

当前阶段建议：

- v0.1.0 可以先发布源码；
- 如果要启用在线临时运行，至少需要发布：
  - `rrh-linux-amd64`
  - `rrh-windows-amd64.exe`
- `linux-arm64 / windows-arm64 / darwin-*` 可以后续补齐；
- Python + PyInstaller 跨平台交叉构建有限，后续如果迁移 Go，会更容易生成全平台单文件。

---

## 🛠️ 默认推荐配置

```text
端口：8443
协议：VLESS
传输：TCP
安全层：Reality
Flow：xtls-rprx-vision
SNI：www.cloudflare.com
Fingerprint：chrome
Mux：关闭
TUN：默认关闭
```

为什么默认推荐 `8443`？

很多教程默认使用 `443`，但在部分网络环境中可能出现：

```text
PingSucceeded: True
TcpTestSucceeded: False
```

这说明 IP 可达，但 TCP 端口不通。此时可以测试：

```text
8443 / 2053 / 2083 / 2087 / 2096
```

---

## 🔐 安全提醒

- 不要公开 PrivateKey。
- 不要多人共用 UUID。
- 给每个设备或用户分配独立 UUID。
- PrivateKey 泄露后应立即轮换。
- 在线脚本运行前应阅读源码。
- 面板类工具虽然方便，但会增加管理端口和安全风险。
- 请遵守所在地法律法规和服务器服务商条款。
- 本项目仅用于个人服务器连接、学习、配置管理与排障辅助，不鼓励也不支持违法用途。

---

## 📜 License

MIT

