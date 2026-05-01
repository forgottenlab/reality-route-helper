# 🧪 测试说明

> Reality Route Helper 涉及配置生成、系统检测、服务重启和网络端口检查。  
> 为了避免误改真实服务器配置，项目内置了沙盒测试机制。

---

## 1. 当前测试状态

当前已经验证：

```text
Windows smoke test ✅
Windows menu flow test ✅
Ubuntu Linux sandbox test ✅
沙盒路径隔离 ✅
禁止真实重启 Xray ✅
不会误改真实配置 ✅
```

测试脚本包括：

```text
tests/smoke_test.py
tests/menu_flow_test.py
scripts/test-local.ps1
scripts/test-linux-sandbox.sh
```

---

## 2. 测试分层

### 2.1 Smoke Test

目标：测试核心函数是否可用。

覆盖内容：

- 平台检测；
- 路线目录；
- v2rayN 链接生成；
- Xray Reality 配置模板生成；
- 沙盒配置写入；
- 沙盒备份；
- 禁止真实重启 Xray。

运行：

```powershell
python .\tests\smoke_test.py
```

Linux：

```bash
python3 tests/smoke_test.py
```

---

### 2.2 Menu Flow Test

目标：模拟用户输入，自动走完主要菜单路径。

覆盖内容：

- 客户端扫描环境；
- 客户端查看路线；
- 客户端生成 v2rayN 链接；
- 客户端测试 TCP 端口；
- 服务器端扫描环境；
- 服务器端查看路线；
- 服务器端进入 VLESS + Reality 菜单；
- 服务器端根据沙盒配置生成链接；
- 服务器端新增用户 UUID。

运行：

```powershell
python .\tests\menu_flow_test.py
```

Linux：

```bash
python3 tests/menu_flow_test.py
```

注意：服务器端菜单流测试会避开必须依赖真实 Xray 的选项，因此即使测试机没有安装 Xray，也能完成非破坏性验证。

---

## 3. Windows 一键安全测试

在项目根目录运行：

```powershell
.\scripts\test-local.ps1
```

它会自动执行：

1. 显示 Python 版本；
2. 编译所有 Python 文件；
3. 运行 smoke tests；
4. 运行 menu flow tests；
5. 设置临时配置路径；
6. 禁止真实重启 Xray；
7. 测试结束后清理临时目录。

成功输出应包含：

```text
All smoke tests passed.
All menu flow tests passed.
Safe test completed successfully.
```

---

## 4. Linux 一键沙盒测试

在 Ubuntu / Debian 服务器或虚拟机中运行：

```bash
bash scripts/test-linux-sandbox.sh
```

它会自动设置：

```text
RRH_CONFIG_PATH=/tmp/.../config.json
RRH_BACKUP_DIR=/tmp/.../backups
RRH_DISABLE_RESTART=1
```

因此不会覆盖真实配置：

```text
/usr/local/etc/xray/config.json
```

也不会真实执行：

```text
systemctl restart xray
```

成功输出应包含：

```text
All smoke tests passed.
All menu flow tests passed.
Linux sandbox test completed successfully.
```

---

## 5. 关键环境变量

### `RRH_CONFIG_PATH`

覆盖 Xray 配置路径。

默认真实路径：

```text
/usr/local/etc/xray/config.json
```

测试时可改成：

```text
/tmp/rrh-test/config.json
```

### `RRH_BACKUP_DIR`

覆盖备份目录。

默认真实路径：

```text
/root/rrh-backups
```

测试时可改成：

```text
/tmp/rrh-test/backups
```

### `RRH_DISABLE_RESTART`

禁止真实执行：

```bash
systemctl restart xray
```

设置：

```text
RRH_DISABLE_RESTART=1
```

后，程序会返回“已跳过重启”，而不会真正重启服务。

---

## 6. 交互式沙盒测试

如果你想手动进入菜单，但不想碰真实配置，可以这样：

### Linux

```bash
mkdir -p /tmp/rrh-test

export RRH_CONFIG_PATH=/tmp/rrh-test/config.json
export RRH_BACKUP_DIR=/tmp/rrh-test/backups
export RRH_DISABLE_RESTART=1

python3 rrh.py
```

### Windows PowerShell

```powershell
$env:RRH_CONFIG_PATH="$env:TEMP\rrh-test\config.json"
$env:RRH_BACKUP_DIR="$env:TEMP\rrh-test\backups"
$env:RRH_DISABLE_RESTART="1"

python rrh.py
```

清理：

```powershell
Remove-Item Env:\RRH_CONFIG_PATH -ErrorAction SilentlyContinue
Remove-Item Env:\RRH_BACKUP_DIR -ErrorAction SilentlyContinue
Remove-Item Env:\RRH_DISABLE_RESTART -ErrorAction SilentlyContinue
```

---

## 7. 真实服务器测试前检查

真实写入前建议：

```bash
sudo cp /usr/local/etc/xray/config.json /root/config-before-rrh-test.json
sudo xray run -test -config /usr/local/etc/xray/config.json
sudo systemctl status xray --no-pager
ss -tlnp | grep ':8443'
```

如果要恢复：

```bash
sudo cp /root/config-before-rrh-test.json /usr/local/etc/xray/config.json
sudo systemctl restart xray
```

---

## 8. 推荐测试流程

```text
Windows 本地 smoke test
  ↓
Windows 菜单流测试
  ↓
Ubuntu / Linux 沙盒测试
  ↓
真实服务器备份
  ↓
真实服务器小范围写入测试
  ↓
发布前构建二进制
```

---

## 9. 当前已知限制

- Linux 沙盒测试不代表真实 Xray 部署成功；
- 没有安装 Xray 的环境下，只能测试非破坏性菜单流程；
- `test_config()` 真实校验仍依赖 `xray run -test`；
- Windows 上不执行 Linux 服务命令；
- 当前测试重点是“不会误伤环境”和“菜单流程不会卡死”。

---

## 10. 后续测试增强计划

- GitHub Actions 自动执行 smoke/menu tests；
- 增加 doctor 命令测试；
- 增加 remove-user 测试；
- 增加 rotate-key 测试；
- 增加 mock xray 测试，以便无 Xray 环境也能测试生成/应用流程；
- 增加真实 Linux VPS 集成测试清单。
