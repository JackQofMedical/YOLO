# Docker 新手命令指南

> 本指南面向 Docker 初学者，涵盖从安装到日常使用的完整流程。
> Docker 是一个**容器化平台**，可以将应用及其依赖打包在一起，实现"一次构建，随处运行"。

---

## 一、什么是 Docker

### 核心概念

| 概念 | 说明 | 类比 |
|------|------|------|
| **镜像（Image）** | 应用的只读模板，包含运行环境 + 代码 + 依赖 | 操作系统的 ISO 安装包 |
| **容器（Container）** | 镜像的运行实例，相互隔离 | 安装好的虚拟机 |
| **仓库（Registry）** | 存储和分发镜像的服务 | GitHub / 应用商店 |
| **Dockerfile** | 用于构建镜像的脚本文件 | Makefile / 构建脚本 |
| **Docker Compose** | 管理多容器应用的工具 | 一个项目的启动配置 |

### Docker 与虚拟机的区别

```
┌─────────────────────────────┐  ┌─────────────────────────────┐
│          虚拟机              │  │          Docker              │
│ ┌──────────┐ ┌──────────┐  │  │ ┌──────────┐ ┌──────────┐  │
│ │  App A   │ │  App B   │  │  │ │  App A   │ │  App B   │  │
│ ├──────────┤ ├──────────┤  │  │ ├──────────┤ ├──────────┤  │
│ │ Guest OS │ │ Guest OS │  │  │ │  共用内核  │   │  │
│ ├──────────┤ ├──────────┤  │  │ ├──────────┤ ├──────────┤  │
│ │                    Hypervisor                 │  │
│ ├────────────────────────────────┤  │ │          Host OS              │  │
│ │          Host OS              │  │ ├─────────────────────────────┤  │
│ ├─────────────────────────────┤  │ │         硬件                   │  │
│ │         硬件                   │  │ └─────────────────────────────┘  │
│ └─────────────────────────────┘  │
│ 启动慢（分钟级）                  │  启动快（秒级）                    │
│ 占用资源多（GB 级）               │  占用资源少（MB 级）               │
│ 完全隔离（独立内核）              │  进程级隔离（共用内核）            │
└────────────────────────────────┘
```

---

## 二、安装 Docker

### Windows 安装

**方式一：Docker Desktop（推荐）**

1. 前往 [Docker 官网](https://docs.docker.com/desktop/setup/install/windows-install/) 下载 Docker Desktop 安装包
2. 双击安装，需启用 **WSL 2**（Windows Subsystem for Linux）
3. 安装完毕后重启电脑
4. 启动 Docker Desktop，等待鲸鱼图标变为常亮

**前提条件 — 启用 WSL 2（以管理员身份运行 PowerShell）**：

```powershell
# 启用 WSL 功能
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# 启用虚拟机平台
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# 设置 WSL 2 为默认版本
wsl --set-default-version 2

# 安装 Linux 发行版（选一个）
wsl --install -d Ubuntu-22.04
```

**验证安装**：

```bash
docker --version          # 查看版本
docker run hello-world    # 运行测试容器
```

### Linux 安装（Ubuntu）

```bash
# 使用官方脚本一键安装
curl -fsSL https://get.docker.com | bash

# 将当前用户加入 docker 组（免 sudo）
sudo usermod -aG docker $USER

# 退出重新登录后生效
newgrp docker
```

---

## 三、镜像管理

镜像是一切操作的基础，Docker 首先需要"下载镜像"，然后才能"运行容器"。

### 搜索与拉取镜像

```bash
# 搜索镜像
docker search ubuntu
docker search python
docker search nginx

# 拉取镜像（不指定版本则默认 latest）
docker pull 镜像名:标签
docker pull python:3.11
docker pull nginx:latest

# 拉取指定平台的镜像（如 Apple Silicon 上拉 x86 镜像）
docker pull --platform linux/amd64 python:3.11
```

### 查看与删除镜像

```bash
# 查看本地所有镜像
docker images
docker image ls

# 查看镜像详细信息
docker image inspect 镜像名:标签
docker image inspect python:3.11

# 查看镜像历史层
docker image history 镜像名:标签

# 删除镜像
docker rmi 镜像ID
docker rmi python:3.11

# 删除所有未使用的镜像（悬空镜像）
docker image prune

# 强制清理（删除所有未被容器使用的镜像）
docker image prune -a

# 彻底清理（镜像 + 容器 + 网络 + 缓存）
docker system prune -a
```

### 导出与导入镜像

```bash
# 将镜像保存为 tar 文件（用于离线分发）
docker save -o 输出文件.tar 镜像名:标签
docker save -o my-python.tar python:3.11

# 从 tar 文件加载镜像
docker load -i 输入文件.tar
docker load -i my-python.tar

# 保存并压缩（节省空间）
docker save python:3.11 | gzip > python-3.11.tar.gz
gunzip -c python-3.11.tar.gz | docker load
```

### 标记与推送

```bash
# 给镜像打标签
docker tag 源镜像:标签 目标仓库/镜像名:标签
docker tag python:3.11 myrepo/python:latest

# 推送到仓库（需先 docker login）
docker login
docker push myrepo/python:latest
```

---

## 四、容器管理

容器是镜像的运行实例，类比"镜像 = 类，容器 = 对象"。

### 创建与启动容器

```bash
# 创建并启动容器（最常用命令）
docker run [选项] 镜像名:标签 [命令]

# --- 基本示例 ---

# 运行 Ubuntu 并进入交互式 Shell
docker run -it ubuntu:22.04 /bin/bash

# 后台运行 Nginx
docker run -d --name my-nginx nginx

# 运行一个执行完就退出的容器
docker run python:3.11 python -c "print('Hello Docker')"

# 容器退出后自动删除
docker run --rm ubuntu echo "用完即删"
```

### docker run 常用选项速查

| 选项 | 说明 | 示例 |
|------|------|------|
| `-d` | **后台运行**（detached） | `docker run -d nginx` |
| `-it` | **交互模式 + 终端** | `docker run -it ubuntu /bin/bash` |
| `--name` | 指定容器名称 | `docker run --name web nginx` |
| `--rm` | 容器退出后**自动删除** | `docker run --rm ubuntu` |
| `-p` | **端口映射** 主机:容器 | `docker run -p 8080:80 nginx` |
| `-v` | **挂载卷** 主机:容器 | `docker run -v /data:/app/data` |
| `-e` | 设置**环境变量** | `docker run -e MYSQL_ROOT_PASSWORD=123 mysql` |
| `--network` | 指定网络 | `docker run --network my-net nginx` |
| `--restart` | 重启策略 | `docker run --restart=always nginx` |
| `--gpus` | 使用 GPU | `docker run --gpus all nvidia/cuda` |

### 端口映射详解

```bash
# 格式：-p 主机端口:容器端口
docker run -d -p 80:80 nginx           # 访问 localhost:80 → 容器 80 端口
docker run -d -p 8080:80 nginx         # 访问 localhost:8080 → 容器 80 端口
docker run -d -p 127.0.0.1:3000:3000 app   # 仅本地访问

# 同时映射多个端口
docker run -d -p 80:80 -p 443:443 nginx
```

### 挂载卷详解

```bash
# 1. 命名卷（Docker 管理，推荐）
docker volume create mydata
docker run -v mydata:/app/data myapp

# 2. 绑定挂载（直接映射主机目录）
docker run -v /host/path:/container/path:ro myapp   # ro = 只读
docker run -v /host/path:/container/path myapp      # rw = 读写（默认）
docker run -v $(pwd):/app myapp                     # 挂载当前目录

# 3. 挂载单个文件
docker run -v /host/config.json:/app/config.json myapp
```

### 查看容器

```bash
# 查看运行中的容器
docker ps

# 查看所有容器（包括已停止的）
docker ps -a

# 查看最近创建的容器
docker ps -l

# 查看容器大小（含磁盘占用）
docker ps -s

# 查看容器详细信息
docker inspect 容器名/ID

# 查看容器日志
docker logs 容器名
docker logs -f 容器名           # 实时跟踪（类似 tail -f）
docker logs --tail 50 容器名    # 最后 50 行
docker logs --since 1h 容器名   # 最近 1 小时

# 查看容器资源占用
docker stats
docker stats 容器名
```

### 进入正在运行的容器

```bash
# 方式一：启动新的 Shell（最常用）
docker exec -it 容器名 /bin/bash
docker exec -it 容器名 sh         # 精简版（Alpine 等无 bash）

# 方式二：附加到容器主进程
docker attach 容器名              # Ctrl+P Ctrl+Q 可安全退出

# 在容器中执行单条命令
docker exec 容器名 ls -la
docker exec 容器名 cat /etc/os-release
docker exec -e ENV=prod 容器名 python app.py    # 带环境变量
```

### 停止、启动、重启、删除

```bash
# 停止容器
docker stop 容器名
docker stop 容器名1 容器名2          # 同时停多个
docker stop $(docker ps -q)          # 停止所有运行中的容器

# 启动已停止的容器
docker start 容器名

# 重启容器
docker restart 容器名

# 强制停止（直接 kill）
docker kill 容器名

# 暂停 / 恢复（冻结进程，不释放内存）
docker pause 容器名
docker unpause 容器名

# 删除容器
docker rm 容器名
docker rm -f 容器名                   # 强制删除（运行中也行）
docker rm $(docker ps -aq)           # 删除所有容器
docker container prune               # 删除所有已停止的容器
```

### 文件复制

```bash
# 从宿主机复制到容器
docker cp 本地文件 容器名:容器内路径
docker cp ./config.json myapp:/app/config.json

# 从容器复制到宿主机
docker cp 容器名:容器内路径 本地文件
docker cp myapp:/app/logs ./logs
```

---

## 五、Dockerfile 编写

**Dockerfile** 是一个文本文件，用于定义如何构建镜像。

### 基本指令速查

| 指令 | 说明 | 示例 |
|------|------|------|
| `FROM` | 指定**基础镜像** | `FROM python:3.11` |
| `WORKDIR` | 设置**工作目录** | `WORKDIR /app` |
| `COPY` | 从宿主机**复制文件**到镜像 | `COPY . /app` |
| `ADD` | 复制 + 自动解压 tar/URL | `ADD archive.tar.gz /app` |
| `RUN` | **构建时**执行命令 | `RUN pip install -r requirements.txt` |
| `CMD` | 容器**启动时**默认执行的命令 | `CMD ["python", "app.py"]` |
| `ENTRYPOINT` | 容器入口命令（不会被覆盖） | `ENTRYPOINT ["python"]` |
| `ENV` | 设置**环境变量** | `ENV PYTHONUNBUFFERED=1` |
| `EXPOSE` | 声明容器监听端口（文档作用） | `EXPOSE 8000` |
| `VOLUME` | 声明匿名卷 | `VOLUME /data` |
| `ARG` | 构建参数（`--build-arg` 传入） | `ARG VERSION=1.0` |
| `USER` | 切换运行用户 | `USER appuser` |

### CMD 与 ENTRYPOINT 的区别

| 特性 | `CMD` | `ENTRYPOINT` |
|------|-------|-------------|
| 可被 `docker run` 命令覆盖 | 是 | 否（需 `--entrypoint`） |
| 典型用途 | 默认参数 | 固定命令 + 参数 |
| 组合使用 | 作为 `ENTRYPOINT` 的默认参数 | 设置主命令 |

### 常见语言的 Dockerfile 模板

**Python 项目**：

```dockerfile
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖（如需要编译的包）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 先复制依赖文件（利用 Docker 缓存层）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 创建非 root 用户
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
CMD ["python", "app.py"]
```

**Node.js 项目（多阶段构建）**：

```dockerfile
# ===== 构建阶段 =====
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# ===== 运行阶段 =====
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package.json .
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

**静态前端项目（Nginx）**：

```dockerfile
# ===== 构建阶段 =====
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# ===== 运行阶段 =====
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 构建镜像

```bash
# 在当前目录构建（需要 Dockerfile）
docker build -t 镜像名:标签 .
docker build -t myapp:v1.0 .
docker build -t myapp:v1.0 -t myapp:latest .   # 打多个标签

# 指定 Dockerfile 路径
docker build -t myapp -f ./docker/Dockerfile .

# 构建时传入参数
docker build --build-arg VERSION=2.0 -t myapp:v2 .

# 不使用缓存重新构建
docker build --no-cache -t myapp .

# 指定平台（交叉构建）
docker build --platform linux/amd64 -t myapp .
```

### .dockerignore 文件

类似于 `.gitignore`，排除不需要复制到镜像的文件，减小构建上下文体积。

```bash
# 常见的 .dockerignore 内容
__pycache__
*.pyc
*.pyo
.venv
venv
node_modules
.git
.gitignore
.env
*.log
Dockerfile
docker-compose.yml
.vscode
.idea
*.md
dist
build
```

---

## 六、Docker Compose

**Docker Compose** 用于管理**多容器应用**，通过一个 YAML 文件定义所有服务。

### 安装

Docker Desktop（Windows/Mac）自带 Compose。Linux 需单独安装：

```bash
# 安装 Compose 插件（推荐）
sudo apt install docker-compose-plugin

# 或安装独立版
sudo curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### docker-compose.yml 示例

```yaml
version: "3.8"

services:
  # --- Web 服务 ---
  web:
    build: .                           # 从当前目录的 Dockerfile 构建
    # image: myapp:latest              # 或直接使用已有镜像
    container_name: my-web-app
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - DEBUG=false
    volumes:
      - ./app:/app                     # 开发时热重载
      - ./logs:/app/logs
    depends_on:
      db:
        condition: service_healthy     # 等 db 健康后再启动
    restart: unless-stopped

  # --- 数据库服务 ---
  db:
    image: postgres:16-alpine
    container_name: my-db
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:                       # 健康检查
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 10s
      timeout: 5s
      retries: 5

  # --- Redis 缓存 ---
  redis:
    image: redis:7-alpine
    restart: always

volumes:
  postgres_data:                       # 命名卷（数据持久化）
```

### Compose 常用命令

```bash
# 启动所有服务（后台运行）
docker compose up -d

# 启动并重新构建（代码变更后）
docker compose up -d --build

# 查看运行状态
docker compose ps

# 查看服务日志
docker compose logs
docker compose logs -f web            # 实时跟踪
docker compose logs --tail 100 web

# 停止所有服务
docker compose down

# 停止并删除卷（⚠ 数据会丢失！）
docker compose down -v

# 重启单个服务
docker compose restart web

# 在指定服务中执行命令
docker compose exec web /bin/bash
docker compose exec db psql -U user -d mydb

# 扩展服务实例（负载均衡）
docker compose up -d --scale web=3

# 查看资源占用
docker compose stats
```

---

## 七、网络管理

Docker 默认创建三种网络：**bridge**（默认）、**host**、**none**。

### 网络类型

| 类型 | 说明 | 使用场景 |
|------|------|----------|
| **bridge** | 默认桥接网络，容器间通过 IP 互通 | 单机多容器通信 |
| **host** | 容器与宿主机共用网络栈 | 高性能场景 |
| **none** | 完全无网络 | 安全隔离 |
| **overlay** | 跨多台 Docker 主机的网络（Swarm） | 集群部署 |

### 网络命令

```bash
# 查看所有网络
docker network ls

# 创建自定义网络（推荐，支持 DNS 名称解析）
docker network create my-net

# 查看网络详情
docker network inspect my-net

# 将运行中的容器连接到网络
docker network connect my-net 容器名

# 从网络断开容器
docker network disconnect my-net 容器名

# 启动容器时指定网络
docker run -d --network my-net --name web nginx

# 删除网络
docker network rm my-net
docker network prune                     # 删除所有未使用的网络
```

### 容器间通信

```bash
# 同一自定义网络中的容器可以通过**容器名**互相访问
docker network create app-net

# 启动数据库
docker run -d --network app-net --name db -e MYSQL_ROOT_PASSWORD=123 mysql:8

# 启动应用（通过 "db" 这个名字连接数据库）
docker run -d --network app-net --name app -e DB_HOST=db myapp
```

---

## 八、数据管理

Docker 容器是**无状态**的——容器删除后，内部数据默认会丢失。持久化数据需要挂载卷。

### 三种挂载方式

| 方式 | 语法 | 数据位置 | 适用场景 |
|------|------|----------|----------|
| **绑定挂载** | `-v /host/path:/container/path` | 宿主机任意路径 | 开发热重载、配置文件 |
| **命名卷** | `-v volume-name:/container/path` | Docker 管理的目录 | 数据库、持久化数据 |
| **tmpfs** | `--tmpfs /container/path` | 内存 | 临时缓存、敏感数据 |

### 卷管理命令

```bash
# 创建卷
docker volume create mydata

# 查看所有卷
docker volume ls

# 查看卷详情（含宿主机实际路径）
docker volume inspect mydata

# 删除卷
docker volume rm mydata
docker volume prune         # 删除所有未使用的卷

# 备份卷数据
docker run --rm -v mydata:/data -v $(pwd):/backup ubuntu tar czf /backup/mydata.tar.gz /data

# 恢复卷数据
docker run --rm -v mydata:/data -v $(pwd):/backup ubuntu tar xzf /backup/mydata.tar.gz -C /data
```

---

## 九、常用现成镜像速查

Docker Hub 上有大量官方镜像，可以直接使用。

| 镜像 | 用途 | 常用启动命令 |
|------|------|-------------|
| **nginx** | Web 服务器 / 反向代理 | `docker run -d -p 80:80 nginx` |
| **mysql:8** | MySQL 数据库 | `docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123 mysql:8` |
| **postgres:16** | PostgreSQL 数据库 | `docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=123 postgres:16` |
| **redis:7** | 缓存 / 消息队列 | `docker run -d -p 6379:6379 redis:7` |
| **mongo:7** | MongoDB 数据库 | `docker run -d -p 27017:27017 mongo:7` |
| **python:3.11** | Python 运行环境 | `docker run -it python:3.11 /bin/bash` |
| **node:20** | Node.js 运行环境 | `docker run -it node:20 /bin/bash` |
| **alpine** | 超小型 Linux（~5MB） | `docker run -it alpine sh` |
| **ubuntu:22.04** | Ubuntu 系统 | `docker run -it ubuntu:22.04 /bin/bash` |
| **portainer/portainer-ce** | Docker 可视化管理 | 见下方配置 |
| **nvidia/cuda** | CUDA + GPU 支持 | `docker run --gpus all -it nvidia/cuda:12.0-base` |

---

## 十、Docker 可视化管理工具

### Portainer（推荐）

```bash
# 创建 Portainer 数据卷
docker volume create portainer_data

# 启动 Portainer（HTTP）
docker run -d \
  -p 9000:9000 \
  --name portainer \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:latest

# 浏览器访问 http://localhost:9000
# 首次访问需设置管理员密码
```

---

## 十一、实用场景示例

### 场景一：一键启动 MySQL + 持久化数据

```bash
docker run -d \
  --name mysql-local \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=mysecret \
  -e MYSQL_DATABASE=myapp \
  -v mysql_data:/var/lib/mysql \
  --restart=unless-stopped \
  mysql:8
```

### 场景二：开发环境热重载（Python Flask）

**项目结构**：

```
myapp/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── app.py
```

**docker-compose.yml**：

```yaml
services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/app                    # 代码变更实时生效
    environment:
      - FLASK_ENV=development
      - FLASK_DEBUG=1
    command: flask run --host=0.0.0.0
```

### 场景三：使用 GPU 的深度学习环境

```bash
# 需要先安装 NVIDIA Container Toolkit
# https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/

# 启动 PyTorch GPU 容器
docker run -it --gpus all \
  -v $(pwd):/workspace \
  -w /workspace \
  pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime \
  /bin/bash

# 容器内测试 GPU 是否可用
python -c "import torch; print(torch.cuda.is_available())"
```

### 场景四：查看容器内部日志不丢失

```bash
# 错误做法：日志写在容器内部，容器删了就没了
# 正确做法：将日志目录挂载出来
docker run -d --name app \
  -v /host/logs:/app/logs \
  myapp

# 或用 Docker 的日志驱动（json-file 默认）
docker logs --tail 200 app > /host/logs/app.log
```

---

## 十二、常用组合命令

```bash
# 停止并删除所有容器
docker stop $(docker ps -aq) && docker rm $(docker ps -aq)

# 进入任何容器的 Shell（zsh 函数，可加进 ~/.bashrc）
docker-shell() { docker exec -it "$1" "${2:-bash}"; }
# 用法：docker-shell 容器名

# 查看容器 IP 地址
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' 容器名

# 清理所有未使用的资源
docker system prune -a --volumes

# 实时查看所有容器资源占用
watch docker stats --no-stream

# 导出容器为镜像（保存当前状态）
docker commit 容器名 新镜像名:标签
```

---

## 十三、常用场景速查

| 场景 | 命令 |
|------|------|
| 拉取镜像 | `docker pull 镜像名:标签` |
| 后台启动容器 | `docker run -d --name 名称 镜像` |
| 交互式进入容器 | `docker run -it 镜像 /bin/bash` |
| 端口映射 | `docker run -d -p 主机端口:容器端口 镜像` |
| 挂载目录 | `docker run -v /主机路径:/容器路径 镜像` |
| 查看运行中容器 | `docker ps` |
| 查看所有容器 | `docker ps -a` |
| 进入运行中的容器 | `docker exec -it 容器名 /bin/bash` |
| 查看容器日志 | `docker logs -f 容器名` |
| 停止容器 | `docker stop 容器名` |
| 启动已停止容器 | `docker start 容器名` |
| 删除容器 | `docker rm 容器名` |
| 删除镜像 | `docker rmi 镜像名` |
| 构建镜像 | `docker build -t 名称:标签 .` |
| 启动 Compose | `docker compose up -d` |
| 停止 Compose | `docker compose down` |
| 清理未用资源 | `docker system prune -a` |
| 查看磁盘占用 | `docker system df` |

---

## 十四、故障排查思路

```bash
# 1. 容器起不来？先看日志
docker logs 容器名

# 2. 想看容器启动过程的输出
docker logs 容器名 2>&1 | tail -100

# 3. 检查容器内部状态
docker exec 容器名 env              # 查看环境变量
docker exec 容器名 ps aux           # 查看进程
docker exec 容器名 cat /etc/hosts   # 查看 hosts 解析

# 4. 检查端口是否在监听
docker exec 容器名 netstat -tlnp    # 或 ss -tlnp（Alpine）

# 5. 排查网络连通性
docker exec 容器A ping 容器B        # 容器间是否通
docker exec 容器 curl http://db:3306  # 端口是否开放

# 6. 看容器为何退出
docker inspect 容器名 | grep -A 10 State

# 7. 实时监控容器资源
docker stats 容器名

# 8. 磁盘占用过大？
docker system df                    # 按类型显示占用
docker system df -v                 # 详细到每个对象
```

### 常见报错与解决

| 报错 | 可能原因 | 解决 |
|------|----------|------|
| `port is already allocated` | 端口被占用 | 换端口或停掉占用进程 `netstat -ano \| findstr :端口` |
| `No space left on device` | 磁盘满了 | `docker system prune -a` 清理 |
| `Cannot connect to the Docker daemon` | Docker 没启动 | 启动 Docker Desktop 或 `sudo systemctl start docker` |
| `permission denied` (Linux) | 没加入 docker 组 | `sudo usermod -aG docker $USER` |
| `executable file not found` | 镜像无 bash（如 Alpine） | 使用 `sh` 代替 `bash` |
| `image not found` | 镜像未拉取或名称错误 | `docker images` 确认，`docker pull` 拉取 |
| `container name already in use` | 容器名重复 | 换名字或 `docker rm` 删除旧容器 |

---

> **学习路线建议**：
> 1. 先用 `docker run` 跑通几个现成镜像（nginx、mysql、redis）
> 2. 学会写 Dockerfile 打包自己的项目
> 3. 用 docker-compose 管理多服务应用
> 4. 再深入网络、卷、多阶段构建等进阶内容
>
> Docker Hub 地址：[https://hub.docker.com](https://hub.docker.com) — 查找官方和社区镜像的总站。
