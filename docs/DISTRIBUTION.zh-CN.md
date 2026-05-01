# 📦 发布与在线临时运行

## 1. 项目名

```text
reality-route-helper
```

## 2. CLI 命令名

```text
rrh
```

不保留 `xrh`，避免与早期讨论稿混淆。

---

## 3. 计划发布文件

```text
rrh-linux-amd64
rrh-linux-arm64
rrh-windows-amd64.exe
rrh-windows-arm64.exe
rrh-darwin-amd64
rrh-darwin-arm64
```

当前 GitHub Actions 默认构建：

```text
rrh-linux-amd64
rrh-windows-amd64.exe
rrh-darwin-amd64
rrh-darwin-arm64
```

Linux arm64 / Windows arm64 后续可通过：

- ARM Runner；
- 自托管 Runner；
- Docker / QEMU；
- 后续迁移 Go 后交叉编译；

进一步完善。

---

## 4. 现在发布前是否必须打全平台包？

不必须。

当前阶段建议分两步：

### v0.1.0：源码优先

适合先发布：

```text
源码
README
docs/
examples/
tests/
scripts/
```

这样可以先让项目公开、积累 issue 和反馈。

### v0.1.x / v0.2.0：启用在线临时运行

如果 README 中正式推荐：

```bash
bash <(curl -fsSL ...)
```

或：

```powershell
irm ... | iex
```

那就至少需要提供：

```text
rrh-linux-amd64
rrh-windows-amd64.exe
```

否则 `run.sh` / `run.ps1` 会找不到 Release assets。

### 全平台包

下面这些可以后续逐步完善：

```text
rrh-linux-arm64
rrh-windows-arm64.exe
rrh-darwin-amd64
rrh-darwin-arm64
```

---

## 5. 在线临时运行

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

## 6. 为什么不直接在线运行 Python？

因为普通用户可能没有 Python 环境。

因此正式入口应该是：

```text
下载对应单文件程序 → 临时目录运行 → 退出后删除
```

而不是要求用户安装 Python。

---

## 7. 本地构建

Windows：

```powershell
.\scripts\build-release.ps1
```

Linux / macOS：

```bash
bash scripts/build-release.sh
```

---

## 8. 发布前测试清单

发布前建议至少运行：

### Windows

```powershell
.\scripts\test-local.ps1
```

### Linux

```bash
bash scripts/test-linux-sandbox.sh
```

### 可选：Windows 本地构建

```powershell
.\scripts\build-release.ps1
.\dist\rrh-windows-amd64.exe
```

### 可选：Linux 本地构建

```bash
bash scripts/build-release.sh
./dist/rrh-linux-amd64
```

---

## 9. 发布流程建议

1. 提交代码到 GitHub：

```bash
git add .
git commit -m "docs: update project documentation"
```

2. 创建 tag：

```bash
git tag v0.1.0
git push origin v0.1.0
```

3. GitHub Actions 自动构建；
4. Release 中生成二进制文件；
5. README 中的在线运行命令即可使用。

---

## 10. 当前建议

当前项目已经通过 Windows 和 Ubuntu 沙盒测试，因此可以：

```text
先发布源码版 v0.1.0
暂时不强制要求所有平台二进制
等准备启用在线临时运行后，再补 Release assets
```

如果你希望一开始 README 里的在线运行命令就可用，建议至少先打：

```text
rrh-linux-amd64
rrh-windows-amd64.exe
```

然后再逐步补齐 arm64 和 darwin。
