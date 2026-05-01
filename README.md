# 🧭 Reality Route Helper

> A bilingual, platform-aware helper for choosing, generating, testing, and managing network connection routes.  
> The first implemented route is **Xray / VLESS + Reality**.

---

## ✨ Vision

Many tutorials tell users to copy and run commands, but they often do not explain:

- why server-side and client-side commands differ;
- why Windows and Linux commands cannot be mixed;
- why port `443` may fail while `8443` works;
- what UUID, Reality PrivateKey, PublicKey, and shortId mean;
- how Outline differs from Xray / VLESS + Reality;
- how to safely test configuration flows without touching real server config.

**Reality Route Helper** is not intended to be a black-box one-click script.

It aims to help users:

- choose a route;
- understand the configuration;
- reduce troubleshooting pain;
- keep backups;
- test safely;
- maintain their setup safely.

---

## 🚀 Features

- 🌐 Chinese / English bilingual CLI
- 🖥️ Windows / Linux / macOS platform detection
- 🧭 Server / client role selection
- 🔎 Environment scanning
- 📦 Xray / Docker / Outline detection
- 🧩 Route catalog framework
- 🛡️ Backup-first config writing
- 🧪 Windows and Linux sandbox tests
- 🔁 Automated menu flow tests
- ✅ VLESS + Reality minimal route
- ✅ v2rayN import link generation
- ✅ TCP port testing

---

## 🧱 Route Overview

| Route | Status | Difficulty | Notes |
|---|---|---:|---|
| Xray / VLESS + Reality | ✅ Implemented | Medium | First MVP route for users who want more control over configuration |
| Outline / Shadowsocks | 🔎 Detect-only | Easy | Easy to use with Outline Manager; detected but not managed yet |
| Hysteria2 | 🗓️ Planned | Medium | QUIC/UDP-based route for some high-latency or lossy networks |
| TUIC | 🗓️ Planned | Medium | QUIC-based TCP/UDP proxy protocol |
| sing-box | 🗓️ Planned | Medium | Universal proxy platform; future unified client/server config route |
| 3x-ui / Marzban / Hiddify | 🗓️ Planned | Easy~Medium | Web panels are convenient but increase management-plane risk |

More docs:

- [Route comparison and technical notes](docs/ROUTES.zh-CN.md)
- [Architecture](docs/ARCHITECTURE.zh-CN.md)
- [Testing](docs/TESTING.zh-CN.md)
- [Distribution](docs/DISTRIBUTION.zh-CN.md)
- [Roadmap](docs/ROADMAP.zh-CN.md)

---

## 🐍 Local Development

Recommended Python version:

```powershell
conda create -n rrh python=3.11 -y
conda activate rrh
python -m pip install -U pip setuptools wheel pyinstaller
```

Run:

```bash
python rrh.py
```

or:

```bash
python -m reality_route_helper
```

---

## 🧪 Testing

Windows:

```powershell
.\scripts\test-local.ps1
```

Linux:

```bash
bash scripts/test-linux-sandbox.sh
```

Verified:

```text
Windows smoke test ✅
Windows menu flow test ✅
Ubuntu Linux sandbox test ✅
Sandbox path isolation ✅
Real Xray restart disabled in tests ✅
Real config not modified ✅
```

---

## ⚡ Temporary Online Runner

After GitHub Releases are available:

### Linux / macOS

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/forgottenlab/reality-route-helper/main/scripts/run.sh)
```

### Windows PowerShell

```powershell
irm https://raw.githubusercontent.com/forgottenlab/reality-route-helper/main/scripts/run.ps1 | iex
```

The runner downloads a platform-specific binary into a temporary directory, runs it, and removes it afterwards.

---

## 📦 Planned Release Assets

```text
rrh-linux-amd64
rrh-linux-arm64
rrh-windows-amd64.exe
rrh-windows-arm64.exe
rrh-darwin-amd64
rrh-darwin-arm64
```

For v0.1.0, publishing source code first is acceptable.  
If the online runner is enabled, at least `rrh-linux-amd64` and `rrh-windows-amd64.exe` should be released.

---

## 🔐 Safety Notes

- Never publish your PrivateKey.
- Do not share the same UUID with multiple users.
- Assign one UUID per device or user.
- Rotate keys immediately if the PrivateKey leaks.
- Read remote scripts before running them.
- Follow local laws and your hosting provider’s terms.
- This project is for personal server connectivity, learning, configuration management, and troubleshooting assistance.

---

## 📜 License

MIT
