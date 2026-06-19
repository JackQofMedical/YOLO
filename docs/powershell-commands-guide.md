# PowerShell 新手命令指南

> 本指南面向 PowerShell 初学者，涵盖日常使用中最常用的命令（cmdlet）。
> PowerShell 是 Windows 系统内置的强大命令行工具，比传统 CMD 功能更丰富。

---

## 一、基本概念

### PowerShell 与 CMD 的区别

| 特性 | PowerShell | CMD |
|------|-----------|-----|
| 命令风格 | **动词-名词**（如 `Get-Process`） | 缩写（如 `dir`） |
| 管道传递 | **对象** | 文本 |
| 脚本能力 | 完整编程语言 | 非常有限 |
| 别名支持 | 支持（`ls`、`cat` 等可用） | 原生命令 |

### 命名规则

PowerShell 命令遵循 **"动词-名词"** 格式：

```powershell
Get-Process        # 获取进程
Set-Location       # 设置位置
New-Item           # 创建项目
Remove-Item        # 删除项目
```

常用动词：`Get`（获取）、`Set`（设置）、`New`（新建）、`Remove`（删除）、`Start`（启动）、`Stop`（停止）

---

## 二、文件与目录操作

### 查看目录内容

```powershell
# 查看当前目录内容（类似 ls / dir）
Get-ChildItem
ls                          # 别名
dir                         # 别名

# 查看指定目录
Get-ChildItem C:\Users

# 显示隐藏文件
Get-ChildItem -Force

# 只显示文件（不含目录）
Get-ChildItem -File

# 只显示目录
Get-ChildItem -Directory

# 递归显示所有子目录内容
Get-ChildItem -Recurse

# 按扩展名过滤
Get-ChildItem -Filter *.txt
Get-ChildItem -Filter *.py

# 按名称搜索（支持通配符）
Get-ChildItem -Recurse -Filter "config*"
```

### 切换目录

```powershell
# 切换目录
Set-Location C:\Users
cd C:\Users                 # 别名

# 切换到上级目录
Set-Location ..
cd ..

# 切换到用户主目录
cd ~

# 切换到桌面
cd ~/Desktop
```

### 创建目录和文件

```powershell
# 创建目录
New-Item -ItemType Directory -Name "新文件夹"
mkdir "新文件夹"            # 别名

# 创建空文件
New-Item -ItemType File -Name "test.txt"

# 创建文件并写入内容
New-Item -ItemType File -Name "test.txt" -Value "Hello World"

# 创建多层目录
New-Item -ItemType Directory -Path "a/b/c" -Force
mkdir -p a/b/c              # 别名形式
```

### 复制、移动、删除

```powershell
# 复制文件
Copy-Item 源文件 目标路径
cp file.txt C:\backup\      # 别名

# 复制整个目录
Copy-Item -Recurse 源目录 目标路径

# 移动 / 重命名
Move-Item 旧路径 新路径
mv file.txt newname.txt     # 别名

# 删除文件
Remove-Item 文件名
rm file.txt                 # 别名

# 删除目录
Remove-Item -Recurse 目录名

# 删除前确认
Remove-Item 文件名 -Confirm
```

### 文件内容操作

```powershell
# 查看文件内容
Get-Content 文件名
cat 文件名                  # 别名
type 文件名                 # 别名

# 查看最后 N 行
Get-Content 文件名 -Tail 20

# 实时监控文件变化（类似 Linux tail -f）
Get-Content 文件名 -Wait

# 写入内容（覆盖）
Set-Content 文件名 "新内容"

# 追加内容
Add-Content 文件名 "追加的内容"

# 搜索文件内容（类似 grep）
Select-String -Path *.log -Pattern "Error"
Get-Content app.log | Select-String "Error"
```

---

## 三、系统信息查看

```powershell
# 查看系统信息
Get-ComputerInfo

# 查看操作系统版本
(Get-CimInstance Win32_OperatingSystem).Caption
(Get-CimInstance Win32_OperatingSystem).Version

# 查看 CPU 信息
Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores

# 查看内存信息
Get-CimInstance Win32_PhysicalMemory | Measure-Object -Property Capacity -Sum
# 结果的 Sum 除以 1GB 即为总内存

# 查看磁盘空间
Get-PSDrive -PSProvider FileSystem

# 查看 IP 地址
Get-NetIPAddress | Where-Object AddressFamily -eq "IPv4"

# 查看主机名
$env:COMPUTERNAME

# 查看当前用户名
$env:USERNAME
```

---

## 四、进程管理

```powershell
# 查看所有进程
Get-Process
ps                          # 别名

# 按名称查找进程
Get-Process -Name "chrome"
Get-Process -Name "*code*"

# 按 CPU 使用排序（取前 10）
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10

# 按内存使用排序
Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 10

# 启动程序
Start-Process notepad
Start-Process "C:\Program Files\app.exe"
start notepad               # 别名

# 结束进程（按名称）
Stop-Process -Name "notepad"
kill -name notepad          # 别名

# 结束进程（按 PID）
Stop-Process -Id 1234

# 强制结束进程
Stop-Process -Name "chrome" -Force
```

---

## 五、服务管理

```powershell
# 查看所有服务
Get-Service

# 按名称查找服务
Get-Service -Name "*wuauserv*"
Get-Service -DisplayName "*Windows Update*"

# 查看运行中的服务
Get-Service | Where-Object Status -eq "Running"

# 启动服务
Start-Service -Name "服务名"

# 停止服务
Stop-Service -Name "服务名"

# 重启服务
Restart-Service -Name "服务名"

# 设置服务开机启动类型
Set-Service -Name "服务名" -StartupType Automatic   # 自动
Set-Service -Name "服务名" -StartupType Manual       # 手动
Set-Service -Name "服务名" -StartupType Disabled     # 禁用
```

---

## 六、网络相关

```powershell
# 测试网络连接
Test-Connection baidu.com
Test-NetConnection baidu.com -Port 443    # 测试端口

# 查看网络适配器
Get-NetAdapter

# 查看 DNS 缓存
Get-DnsClientCache

# 清除 DNS 缓存
Clear-DnsClientCache

# 查看当前网络连接（类似 netstat）
Get-NetTCPConnection

# 查看指定端口的连接
Get-NetTCPConnection -LocalPort 80

# 下载文件
Invoke-WebRequest -Uri "https://example.com/file.zip" -OutFile "file.zip"
# 简写
iwr https://example.com/file.zip -OutFile file.zip

# 调用 REST API
Invoke-RestMethod -Uri "https://api.github.com/users/octocat"
```

---

## 七、压缩与解压

```powershell
# 压缩目录为 zip
Compress-Archive -Path 目录名 -DestinationPath 输出.zip

# 示例
Compress-Archive -Path C:\MyProject -DestinationPath C:\backup\myproject.zip

# 解压 zip
Expand-Archive -Path 文件.zip -DestinationPath 目标目录

# 示例
Expand-Archive -Path C:\backup\myproject.zip -DestinationPath C:\Restored

# 追加文件到已有 zip
Compress-Archive -Path 新文件.txt -Update -DestinationPath 已有.zip
```

---

## 八、环境变量

```powershell
# 查看所有环境变量
Get-ChildItem Env:
env                         # 别名

# 查看指定环境变量
$env:PATH
$env:USERNAME
$env:COMPUTERNAME
$env:TEMP

# 临时设置环境变量（当前会话有效）
$env:MY_VAR = "hello"

# 永久设置环境变量（用户级别）
[Environment]::SetEnvironmentVariable("MY_VAR", "hello", "User")

# 永久设置环境变量（系统级别，需管理员权限）
[Environment]::SetEnvironmentVariable("MY_VAR", "hello", "Machine")

# 将目录添加到 PATH（当前会话）
$env:PATH += ";C:\MyTools"

# 将目录永久添加到 PATH
$currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
[Environment]::SetEnvironmentVariable("PATH", "$currentPath;C:\MyTools", "User")
```

---

## 九、查找文件与文本搜索

```powershell
# 按文件名搜索（递归）
Get-ChildItem -Path C:\ -Recurse -Filter "*.log" -ErrorAction SilentlyContinue

# 按文件大小查找（大于 100MB）
Get-ChildItem -Path C:\Users -Recurse -File |
    Where-Object Length -gt 100MB

# 查找最近 7 天修改过的文件
Get-ChildItem -Path C:\MyProject -Recurse -File |
    Where-Object LastWriteTime -gt (Get-Date).AddDays(-7)

# 在文件内容中搜索文本（类似 grep）
Select-String -Path *.py -Pattern "import os"

# 递归搜索所有子目录
Get-ChildItem -Recurse -Include *.py |
    Select-String -Pattern "def main"

# 搜索并排除目录
Get-ChildItem -Recurse -Include *.py -Exclude node_modules |
    Select-String -Pattern "TODO"
```

---

## 十、PowerShell 配置文件

```powershell
# 查看配置文件路径
$PROFILE

# 查看所有配置文件路径
$PROFILE | Select-Object *

# 检查配置文件是否存在
Test-Path $PROFILE

# 创建配置文件
New-Item -ItemType File -Path $PROFILE -Force

# 用记事本打开配置文件
notepad $PROFILE
```

### 配置文件示例（写入 $PROFILE 的内容）

```powershell
# 设置别名
Set-Alias -Name np -Value notepad
Set-Alias -Name py -Value python

# 自定义提示符（显示当前目录名）
function prompt {
    $dir = (Get-Location).Path.Split('\')[-1]
    "PS $dir> "
}

# 常用函数
function mkcd {
    param([string]$dir)
    New-Item -ItemType Directory -Path $dir -Force
    Set-Location $dir
}

function up {
    param([int]$n = 1)
    for ($i = 0; $i -lt $n; $i++) { Set-Location .. }
}
```

---

## 十一、管道与对象操作

PowerShell 管道传递的是**对象**，不是纯文本，这比 Linux shell 更强大。

```powershell
# 排序
Get-Process | Sort-Object CPU -Descending

# 过滤（Where-Object）
Get-Process | Where-Object CPU -gt 100

# 选择属性
Get-Process | Select-Object Name, CPU, WorkingSet

# 重命名属性
Get-Process | Select-Object Name, @{N='MemoryMB';E={[math]::Round($_.WorkingSet/1MB)}}

# 分组
Get-Process | Group-Object Company

# 统计数量
Get-ChildItem | Measure-Object

# 格式化表格输出
Get-Process | Format-Table Name, CPU, WorkingSet -AutoSize

# 格式化列表输出
Get-Process | Format-List Name, CPU, WorkingSet

# 导出为 CSV
Get-Process | Export-Csv -Path processes.csv -NoTypeInformation

# 从 CSV 导入
Import-Csv -Path processes.csv

# 导出为 JSON
Get-Process | ConvertTo-Json | Out-File processes.json

# 从 JSON 导入
Get-Content processes.json | ConvertFrom-Json
```

---

## 十二、脚本与执行策略

### 执行策略

```powershell
# 查看当前执行策略
Get-ExecutionPolicy

# 查看所有作用域的执行策略
Get-ExecutionPolicy -List

# 设置执行策略（以管理员身份运行）
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# 常用策略说明
# Restricted    — 禁止运行任何脚本（默认）
# RemoteSigned  — 本地脚本可运行，远程脚本需签名
# Unrestricted  — 允许所有脚本（有警告）
# Bypass        — 无限制，无警告
```

### 运行脚本

```powershell
# 运行 PowerShell 脚本
.\script.ps1

# 传递参数
.\script.ps1 -Name "test" -Count 5

# 绕过执行策略临时运行
powershell -ExecutionPolicy Bypass -File script.ps1
```

### 简单脚本示例

```powershell
# backup.ps1 — 备份指定目录
param(
    [string]$Source = "C:\MyProject",
    [string]$Dest = "D:\Backup"
)

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupPath = Join-Path $Dest "backup_$timestamp"

Write-Host "正在备份 $Source 到 $backupPath ..."
Copy-Item -Path $Source -Destination $backupPath -Recurse
Write-Host "备份完成！"
```

---

## 十三、帮助系统

```powershell
# 查看命令帮助
Get-Help Get-Process
help Get-Process            # 别名

# 查看完整帮助
Get-Help Get-Process -Full

# 查看使用示例
Get-Help Get-Process -Examples

# 在线查看帮助（打开浏览器）
Get-Help Get-Process -Online

# 搜索包含关键字的命令
Get-Help *process*
Get-Command *process*

# 查看命令的所有参数
Get-Command Get-Process -Syntax

# 查看命令的属性和方法
Get-Process | Get-Member

# 更新帮助内容（需管理员权限）
Update-Help
```

---

## 十四、常用场景速查

| 场景 | 命令 |
|------|------|
| 查看目录内容 | `Get-ChildItem` 或 `ls` |
| 切换目录 | `Set-Location 路径` 或 `cd 路径` |
| 创建目录 | `New-Item -ItemType Directory -Name "名"` |
| 复制文件 | `Copy-Item 源 目标` |
| 删除文件 | `Remove-Item 文件名` |
| 查看文件内容 | `Get-Content 文件名` 或 `cat 文件名` |
| 搜索文件内容 | `Select-String -Path 文件 -Pattern "关键词"` |
| 查看进程 | `Get-Process` 或 `ps` |
| 结束进程 | `Stop-Process -Name "进程名"` |
| 查看 IP | `Get-NetIPAddress` |
| 测试连接 | `Test-Connection 目标` |
| 压缩文件 | `Compress-Archive -Path 源 -DestinationPath 目标.zip` |
| 解压文件 | `Expand-Archive -Path 文件.zip -DestinationPath 目标目录` |
| 设置环境变量 | `$env:变量名 = "值"` |
| 查看帮助 | `Get-Help 命令名` 或 `man 命令名` |

---

## 十五、实用别名对照表

PowerShell 为常用命令设置了别名，方便从 Linux / CMD 迁移：

| 别名 | 完整命令 | 来源 |
|------|---------|------|
| `ls` | `Get-ChildItem` | Linux |
| `cd` | `Set-Location` | 通用 |
| `cp` | `Copy-Item` | Linux |
| `mv` | `Move-Item` | Linux |
| `rm` | `Remove-Item` | Linux |
| `cat` | `Get-Content` | Linux |
| `mkdir` | `New-Item -ItemType Directory` | 通用 |
| `clear` | `Clear-Host` | Linux |
| `cls` | `Clear-Host` | CMD |
| `echo` | `Write-Output` | 通用 |
| `ps` | `Get-Process` | Linux |
| `kill` | `Stop-Process` | Linux |
| `man` | `Get-Help` | Linux |
| `curl` | `Invoke-WebRequest` | Linux（别名行为不同） |
| `wget` | `Invoke-WebRequest` | Linux（别名行为不同） |

> **注意**：`curl` 和 `wget` 在 PowerShell 中是 `Invoke-WebRequest` 的别名，但参数格式不同。
> 如果需要真正的 curl，使用 `curl.exe`。

---

## 十六、管理员权限操作

```powershell
# 以管理员身份启动新的 PowerShell 窗口
Start-Process powershell -Verb RunAs

# 检查当前是否为管理员
([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

# 在当前会话中以管理员身份运行命令（会弹出 UAC）
Start-Process powershell -Verb RunAs -ArgumentList "-Command Get-Process"
```

---

> **提示**：PowerShell 最大的优势是**对象管道**——命令之间传递的不是文本，而是结构化对象。
> 善用 `Get-Member` 查看对象的属性和方法，是掌握 PowerShell 的关键。
