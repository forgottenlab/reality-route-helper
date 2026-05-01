# 🧱 架构说明

## 1. 设计原则

Reality Route Helper 的核心原则是：

- **平台隔离**：Windows、Linux、macOS 不混用命令。
- **路线隔离**：VLESS + Reality、Outline、Hysteria2、TUIC、sing-box、面板路线独立扩展。
- **先检测再执行**：不盲目写配置。
- **先备份再修改**：降低误操作风险。
- **沙盒优先**：所有危险操作都尽量支持环境变量重定向。
- **能解释就不黑箱**：让用户知道每个配置在做什么。

---

## 2. 分层结构

```text
CLI 菜单层
  ↓
routes 路线层
  ↓
platforms 平台适配层
  ↓
scanners 扫描层
  ↓
templates 配置模板层
  ↓
core 命令与模型层
```

---

## 3. 目录说明

### `platforms/`

负责判断当前操作系统：

- `linux.py`
- `windows.py`
- `macos.py`

避免出现 Windows 上执行 `systemctl`、Linux 上执行 PowerShell 的问题。

### `routes/`

负责不同方案路线：

- `vless_reality.py`：当前已实现；
- `catalog.py`：路线目录。

后续可以新增：

```text
hysteria2.py
outline.py
tuic.py
sing_box.py
panel.py
```

### `scanners/`

负责扫描当前环境：

- Xray；
- Docker；
- Outline；
- 后续可扩展 Nginx、Caddy、3x-ui、Marzban、Hiddify 等。

### `templates/`

负责生成配置文件，避免配置字符串散落在业务逻辑中。

### `core/`

通用能力：

- 命令执行；
- 数据模型；
- 输入校验；
- 上下文对象。

### `tests/`

测试能力：

- `smoke_test.py`：核心函数烟雾测试；
- `menu_flow_test.py`：菜单流自动化测试。

### `scripts/`

开发、测试、发布辅助脚本：

- `test-local.ps1`：Windows 本地安全测试；
- `test-linux-sandbox.sh`：Linux 沙盒测试；
- `build-release.ps1`：Windows 本地构建；
- `build-release.sh`：Linux/macOS 本地构建；
- `run.ps1` / `run.sh`：未来在线临时运行入口。

---

## 4. 沙盒机制

为了避免误改真实服务器配置，VLESS + Reality 路线支持环境变量：

```text
RRH_CONFIG_PATH
RRH_BACKUP_DIR
RRH_DISABLE_RESTART
```

测试时：

```text
RRH_CONFIG_PATH=/tmp/.../config.json
RRH_BACKUP_DIR=/tmp/.../backups
RRH_DISABLE_RESTART=1
```

这样可以验证配置写入、备份、菜单流程，但不会覆盖：

```text
/usr/local/etc/xray/config.json
```

也不会真实执行：

```text
systemctl restart xray
```

---

## 5. 后续扩展方式

新增一条路线时：

1. 在 `routes/catalog.py` 增加路线说明；
2. 新增 `routes/<route_name>.py`；
3. 如需配置文件，新增 `templates/<route_name>_config.py`；
4. 如需检测环境，新增或扩展 `scanners/`；
5. 在 `cli.py` 中接入菜单；
6. 在 `tests/` 中增加 smoke/menu flow 测试；
7. 在 `docs/ROUTES.zh-CN.md` 中补充路线说明。

---

## 6. 为什么当前不用 Go / Rust？

Go / Rust 更适合最终单文件 CLI，但 Python 更适合当前阶段快速迭代。

当前路线：

```text
v0.x：Python 快速迭代 + PyInstaller 发布单文件
v1.x：功能稳定后，可评估是否迁移 Go
```

### Python 当前优势

- 快速实现 CLI；
- 便于生成 JSON/YAML；
- 易于编写测试；
- 适合早期反复调整交互逻辑。

### Go/Rust 后续优势

- 更适合跨平台单文件分发；
- 不依赖 Python 环境；
- 交叉编译更自然；
- 更适合长期维护的系统工具。

---

## 7. 当前架构状态

当前架构已经支持：

```text
平台检测 ✅
路线目录 ✅
VLESS + Reality 路线 ✅
Outline 检测框架 ✅
沙盒测试 ✅
菜单流测试 ✅
发布脚本框架 ✅
```

下一步重点不是重构，而是补功能：

```text
doctor
remove-user
rotate-key
install-xray
GitHub Actions 测试
```
