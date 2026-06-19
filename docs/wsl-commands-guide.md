# WSL 新手使用指南

> 本指南面向 WSL（Windows Subsystem for Linux）初学者，涵盖安装配置到日常使用的完整流程。
> WSL 让你在 Windows 中**原生运行 Linux**，无需虚拟机，双系统文件互通。

---

## 一、什么是 WSL

### 核心概念

| 概念 | 说明 |
|------|------|
| **WSL 1** | 第一代，通过翻译层将 Linux 系统调用转为 Windows 系统调用，文件读写快但兼容性一般 |
| **WSL 2** | 第二代，运行在轻量级虚拟机中的**完整 Linux 内核**，兼容性接近原生 Linux，磁盘 I/O 大幅提升 |
| **发行版（Distro）** | 具体的 Linux 系统，如 Ubuntu、Debian、Kali 等 |
| **wsl.exe** | Windows 端管理命令 |
| **\\wsl$** | Windows 资源管理器中访问 WSL 文件的网络路径 |

### WSL 2 与虚拟机对比

| 特性 | WSL 2 | 传统虚拟机（VMware/VirtualBox） |
|------|-------|------|
| 启动速度 | **秒级** | 分钟级 |
| 内存占用 | 动态分配，用完释放 | 固定预留 |
| 文件互通 | 原生互通，`/mnt/c` 直接访问 | 需共享文件夹 |
| GPU 支持 | 原生支持 CUDA | 需直通配置 |
| 网络 | 与 Windows 共享 localhost | 独立 IP，需端口转发 |
| 适用场景 | 开发环境、命令行工具 | 完整桌面环境 |

---

## 二、安装 WSL

### 一条命令安装（Windows 10 2004+ / Windows 11）

以**管理员身份**打开 PowerShell 或 CMD：

```powershell
wsl --install
```

这条命令会自动完成四件事：
1. 启用 WSL 功能
2. 启用虚拟机平台
3. 安装 WSL 2 内核
4. 安装默认发行版（Ubuntu）

安装完成后**重启电脑**。首次启动 Ubuntu 会提示创建 Linux 用户名和密码。

### 手动分步安装（旧版 Windows）

```powershell
# 步骤 1：启用 WSL 功能
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# 步骤 2：启用虚拟机平台
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# 步骤 3：重启电脑
# 步骤 4：下载 WSL 2 内核更新包
# https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi

# 步骤 5：设置 WSL 2 为默认版本
wsl --set-default-version 2

# 步骤 6：安装 Linux 发行版
wsl --install -d Ubuntu-22.04
```

### 查看可安装的发行版

```powershell
# 查看所有可安装的发行版
wsl --list --online
wsl -l -o

# 常见选项：
# Ubuntu, Ubuntu-22.04, Ubuntu-24.04
# Debian
# Kali-Linux
# openSUSE-Leap
# Alpine
```

### 安装多个发行版

```powershell
# 安装第二个发行版
wsl --install -d Debian

# 查看已安装的发行版和 WSL 版本
wsl --list --verbose
wsl -l -v
```

---

## 三、WSL 基础命令

### 启动与退出

```powershell
# 启动默认发行版
wsl

# 启动指定发行版
wsl -d Ubuntu-22.04
wsl -d Debian

# 以指定用户启动
wsl -u root
wsl -d Ubuntu-22.04 -u root

# 在 WSL 中执行单条命令（不进入 Shell）
wsl ls -la
wsl python --version
wsl -d Ubuntu-22.04 cat /etc/os-release

# 退出 WSL Shell（在 Linux 终端内）
exit
# 或按 Ctrl+D
```

### 发行版管理

```powershell
# 查看已安装的发行版
wsl -l -v

# 设置默认发行版
wsl --set-default Ubuntu-22.04
wsl -s Ubuntu-22.04

# 设置 WSL 版本（1 → 2 或 2 → 1）
wsl --set-version Ubuntu-22.04 2

# 导出发行版（备份/迁移）
wsl --export Ubuntu-22.04 D:\backup\ubuntu.tar

# 导入发行版（恢复/迁移）
wsl --import Ubuntu-22.04 D:\WSL\Ubuntu D:\backup\ubuntu.tar

# 注销（删除）发行版（⚠ 数据会丢失）
wsl --unregister Ubuntu-22.04

# 终止（关机）发行版
wsl --terminate Ubuntu-22.04
wsl -t Ubuntu-22.04

# 关闭所有 WSL 实例
wsl --shutdown
```

### WSL 1 与 WSL 2 互转

```powershell
# 查看当前版本
wsl -l -v

# 转为 WSL 2
wsl --set-version Ubuntu-22.04 2

# 转为 WSL 1（跨文件系统性能更好）
wsl --set-version Ubuntu-22.04 1
```

---

## 四、文件系统互通

这是 WSL 最实用的特性：**Windows 和 Linux 之间可以直接访问彼此的文件**。

### 从 WSL 访问 Windows 文件

```bash
# Windows 磁盘挂载在 /mnt 下
cd /mnt/c                   # 进入 C 盘
cd /mnt/d/Projects          # 进入 D 盘 Projects 目录
ls /mnt/c/Users/你的用户名   # 查看 Windows 用户目录

# 直接在 Windows 文件目录中工作
cd /mnt/c/Users/admin/Desktop
python script.py
```

### 从 Windows 访问 WSL 文件

```powershell
# 方法一：资源管理器地址栏输入
\\wsl$

# 方法二：在 WSL 终端中输入（从当前目录打开资源管理器）
explorer.exe .

# 方法三：PowerShell 中直接访问
cd \\wsl$\Ubuntu-22.04\home\用户名
```

### 跨系统文件操作注意事项

| 操作 | 建议 |
|------|------|
| 项目代码存放 | 需要高性能时放 WSL 内部（`~/projects`） |
| 跨系统编辑 | 用 `code` 命令（VS Code 的 WSL 远程模式） |
| Windows 文件在 WSL 中访问 | 可以直接用，但 I/O 性能低于 WSL 内部 |
| 不要在 Windows 下直接修改 WSL 内部文件 | 会导致权限问题，应通过 WSL Shell 操作 |

### 性能对比

```
场景：同一个 Python 项目 npm install

代码放在 /mnt/c（Windows 文件系统）
→ 读写速度慢，适合偶尔操作

代码放在 ~/project（WSL 内部 ext4）
→ 读写速度快，适合日常开发 ⭐推荐
```

---

## 五、WSL 配置优化

WSL 的配置文件位于 Windows 用户目录：

```
C:\Users\你的用户名\.wslconfig
```

### 全局配置（.wslconfig）

所有发行版共享的全局设置：

```ini
# C:\Users\你的用户名\.wslconfig
[wsl2]
# 限制内存使用（默认 50% 或 80% 物理内存）
memory=8GB

# 限制 CPU 核心数
processors=4

# 限制 swap 大小（设为 0 禁用 swap）
swap=4GB

# swap 文件位置
swapFile=D:\\WSL\\swap.vhdx

# 启用 localhost 转发
localhostForwarding=true

# 内核命令行参数
kernelCommandLine=

# 网络模式（mirrored 为镜像模式，NAT 为默认）
networkingMode=NAT

# DNS 隧道
dnsTunneling=true

# 防火墙集成
firewall=true

# 自动代理
autoProxy=true
```

### 发行版内配置（/etc/wsl.conf）

在每个发行版内部，编辑 `/etc/wsl.conf` 控制该发行版的特定行为：

```bash
sudo vim /etc/wsl.conf
```

```ini
# /etc/wsl.conf — 发行版级别配置

[boot]
# 启动时执行的命令
command=

# 是否自动挂载 Windows 磁盘
[automount]
enabled=true
# 挂载根目录
root=/mnt/
# 挂载选项
options="metadata,umask=22,fmask=11"

# 网络配置
[network]
# 主机名
hostname=ubuntu-dev
# 是否生成 /etc/resolv.conf
generateResolvConf=true

# 跨系统互操作
[interop]
# 允许从 WSL 调用 Windows .exe
enabled=true
# 将 Windows PATH 追加到 WSL PATH
appendWindowsPath=true

# 用户设置
[user]
# 默认登录用户
default=你的用户名
```

修改后需要重启 WSL 使配置生效：

```powershell
wsl --shutdown
```

---

## 六、与 VS Code 集成（推荐开发方式）

安装 **WSL 扩展** 后，可以在 Windows 的 VS Code 中无缝编辑 WSL 内的代码。

### 连接流程

```bash
# 1. Windows 端安装 VS Code + WSL 扩展
#    VS Code 会自动提示安装，或手动搜索 "WSL"

# 2. 在 WSL 终端中进入项目目录
cd ~/myproject

# 3. 启动 VS Code（自动通过 WSL 远程模式连接）
code .

# 首次运行会自动在 WSL 中安装 VS Code Server
# 之后 VS Code 左下角会显示 "WSL: Ubuntu-22.04"
```

### VS Code WSL 环境下可用的功能

- 终端自动连接到 WSL Shell
- Git 操作在 WSL 内完成
- 调试功能完全可用
- 扩展按需在 WSL 中安装（与 Windows 端分开）

---

## 七、网络与端口

### localhost 自动转发

WSL 2 中，Linux 内启动的服务会**自动映射到 Windows 的 localhost**：

```bash
# 在 WSL 中启动一个 Web 服务
python -m http.server 8000

# Windows 浏览器直接访问
# http://localhost:8000  ✅ 可以直接访问
```

### 查看 WSL IP 地址

```bash
# 查看 WSL 内部 IP
ip addr show eth0

# 查看 Windows 宿主机 IP（从 WSL 内部）
cat /etc/resolv.conf | grep nameserver
```

### Windows 防火墙放行

如果外部设备需要访问 WSL 中的服务，需在 Windows 防火墙中创建入站规则，或将 WSL 网络模式设为 `mirrored`。

### 代理设置

```bash
# WSL 中使用 Windows 端的代理（如 Clash、V2Ray）
# 获取 Windows 宿主机 IP
export HOST_IP=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}')

# 设置代理环境变量
export http_proxy="http://${HOST_IP}:7890"
export https_proxy="http://${HOST_IP}:7890"

# 写入 ~/.bashrc 或 ~/.zshrc 永久生效
echo 'export HOST_IP=$(cat /etc/resolv.conf | grep nameserver | awk "{print \$2}")' >> ~/.bashrc
echo 'export http_proxy="http://${HOST_IP}:7890"' >> ~/.bashrc
echo 'export https_proxy="http://${HOST_IP}:7890"' >> ~/.bashrc
```

---

## 八、GPU 与 CUDA 支持

WSL 2 原生支持 NVIDIA CUDA，可以直接在 Linux 中使用 GPU。

### 安装步骤

```bash
# 步骤 1：Windows 端安装 NVIDIA 驱动（支持 WSL 的版本）
# 下载地址：https://www.nvidia.com/download/index.aspx
# 选择 Game Ready 或 Studio 驱动，安装到 Windows

# 步骤 2：在 WSL 中安装 CUDA Toolkit（无需装驱动）
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-wsl-ubuntu.pin
sudo mv cuda-wsl-ubuntu.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/12.4.0/local_installers/cuda-repo-wsl-ubuntu-12-4-local_12.4.0-1_amd64.deb
sudo dpkg -i cuda-repo-wsl-ubuntu-12-4-local_12.4.0-1_amd64.deb
sudo cp /var/cuda-repo-wsl-ubuntu-12-4-local/cuda-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-4

# 步骤 3：验证 GPU 可用
nvidia-smi
```

### Docker 中使用 GPU

```bash
# 安装 NVIDIA Container Toolkit 后
docker run --gpus all nvidia/cuda:12.0-base nvidia-smi
```

---

## 九、与 Docker Desktop 集成

Docker Desktop 可以直接使用 WSL 2 作为后端引擎：

1. Docker Desktop → Settings → Resources → WSL Integration
2. 勾选要启用 Docker 的发行版
3. 应用后，在 WSL 中可以直接使用 `docker` 命令

这样 Docker 容器运行在 WSL 2 引擎上，与命令行无缝集成。

---

## 十、常用工具安装速查

进入 WSL 后，这是新系统的基础环境搭建：

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 基础工具
sudo apt install -y build-essential curl wget git vim unzip

# Python 开发
sudo apt install -y python3 python3-pip python3-venv

# Node.js（通过 nvm 管理版本）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
nvm install 20
nvm use 20

# Oh My Zsh（美化终端）
sudo apt install -y zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# 安装 Windows Terminal（Windows 端，强烈推荐）
# Microsoft Store 搜索 "Windows Terminal"
# 支持多标签、分屏、GPU 加速渲染
```

---

## 十一、日常操作速查

| 场景 | 命令（PowerShell） |
|------|-------------------|
| 启动 WSL | `wsl` |
| 启动指定发行版 | `wsl -d Ubuntu-22.04` |
| 执行单条命令 | `wsl 命令` |
| 查看已安装发行版 | `wsl -l -v` |
| 设置默认发行版 | `wsl -s Ubuntu-22.04` |
| 关闭所有 WSL | `wsl --shutdown` |
| 终止指定发行版 | `wsl -t Ubuntu-22.04` |
| 导出备份 | `wsl --export Ubuntu-22.04 backup.tar` |
| 导入恢复 | `wsl --import Ubuntu-22.04 位置 backup.tar` |
| 删除发行版 | `wsl --unregister Ubuntu-22.04` |
| 查看可安装发行版 | `wsl -l -o` |
| 进入 Windows 目录 | `cd /mnt/c` |
| 在资源管理器中打开 | `explorer.exe .` |
| 用 VS Code 打开 | `code .` |

| 场景 | 命令（WSL 内 / bash） |
|------|----------------------|
| 查看 Windows 文件 | `ls /mnt/c/Users/` |
| 查看 WSL 的 IP | `ip addr show eth0` |
| 查看宿主机 IP | `cat /etc/resolv.conf` |
| 测试服务端口 | `curl localhost:8000` |
| 更新系统 | `sudo apt update && sudo apt upgrade -y` |

---

## 十二、常见问题排查

| 问题 | 解决 |
|------|------|
| WSL 启动报错 `0x80370102` | BIOS 未开启虚拟化，重启进 BIOS 启用 Intel VT-x / AMD-V |
| `请启用虚拟机平台` | 管理员 PowerShell 运行：`dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all` |
| WSL 内存占用过高 | 创建 `.wslconfig`，限制 `memory=4GB`，然后 `wsl --shutdown` |
| WSL 磁盘空间越来越大 | `diskpart` 压缩 vhdx，或用 `wsl --shutdown` + `optimize-vhd` 压缩 |
| `wsl` 命令找不到 | 确保已启用 WSL 功能，或使用旧版命令 `bash.exe` |
| localhost 无法访问 WSL 服务 | 检查 `.wslconfig` 中 `localhostForwarding=true`，重启 WSL |
| apt 安装软件特别慢 | 更换为国内镜像源（清华/中科大/阿里云） |
| 挂载 Windows 盘符提示权限错误 | 在 `/etc/wsl.conf` 中 `[automount]` 添加 `options="metadata"` |

### 更换 APT 镜像源加速

```bash
# 备份原始源
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak

# 替换为清华大学镜像源（Ubuntu 22.04）
sudo sed -i 's|http://archive.ubuntu.com|https://mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list
sudo sed -i 's|http://security.ubuntu.com|https://mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list

# 更新
sudo apt update
```

### 回收 WSL 磁盘空间

```powershell
# PowerShell 管理员模式
wsl --shutdown

# 找到 vhdx 文件路径（通常在 %LOCALAPPDATA%\Packages\... 下）
# 压缩虚拟磁盘
optimize-vhd -Path "C:\Users\admin\AppData\Local\Packages\CanonicalGroupLimited.Ubuntu22.04LTS_79rhkp1fndgsc\LocalState\ext4.vhdx" -Mode Full
```

---

## 十三、快捷键

Windows Terminal 中的 WSL 快捷键（建议使用 Windows Terminal）：

| 快捷键 | 操作 |
|--------|------|
| `Ctrl+Shift+T` | 新建标签页 |
| `Alt+Shift+D` | 分屏（左右） |
| `Alt+Shift+-` | 分屏（上下） |
| `Alt+方向键` | 切换窗格 |
| `Ctrl+Shift+W` | 关闭当前窗格 |
| `Ctrl+Shift+P` | 命令面板 |
| `Ctrl+,` | 打开设置 |
| `Shift+PageUp/Down` | 滚动 |

---

> **推荐套装**：WSL 2 + Windows Terminal + VS Code（WSL 扩展）+ Docker Desktop（WSL 后端）
> 这套组合可以让 Windows 获得接近原生 Linux 的开发体验，同时保留 Windows 的日常便利。
