# 项目概述
这个项目我是想用来学习YOLO的模型怎样构建的，但是在这里我有些不同的。

首先，我应该还是要跟着网络上的视频来先学习好怎样构建YOLO的模型，实现目标检测模型。随后，在Xiaoxin上，我应该做到能够用这台电脑完成各种代码的开发调试，最后构建出一个完整的仓库。在Xiaoxin上，思考完整如何利用容器化技术构建一个可以复用的环境依赖，随后通过远程的仓库来让4060 Laptop完成训练的过程。随后，我要进行对项目代码的一个重构，旨在能够像现有的论文一样，规范地呈现为一个可以利用的仓库。

这些内容我都准备在暑假中完成，并且最好是在国际课程周的第一周就完成，随后衔接我的TLS课题。

# 具体实行计划

## 阶段一：模型学习与本地实现（小新笔记本）

### YOLOv1
- [ ] 对照论文 *You Only Look Once: Unified, Real-Time Object Detection* 逐行理解网络结构
- [ ] 完成 `YOLOv1/YOLOv1_model.py` 的 backbone + detector 实现 ✅ 已初步完成
- [ ] 实现损失函数（bounding box loss + confidence loss + classification loss）
- [ ] 实现数据预处理：VOC 数据集 → 448×448 归一化 + S×S grid 标签生成
- [ ] 实现训练脚本：`YOLOv1/train.py`，含学习率调度与 checkpoint 保存
- [ ] 实现推理脚本：NMS 后处理 + 可视化绘制
- [ ] 在 Pascal VOC 2007/2012 上完成训练验证，输出 mAP 指标

### YOLOv2
- [ ] 对照论文 *YOLO9000: Better, Faster, Stronger* 理解改进点（BatchNorm、Anchor Box、Dimension Clusters、Fine-Grained Features、Multi-Scale Training）
- [ ] 实现 Darknet-19 backbone
- [ ] 实现 passthrough layer（fine-grained features）
- [ ] 实现 Anchor Box 机制与维度先验
- [ ] 完成 `YOLOv2/train.py` 与 `YOLOv2/detect.py`

### YOLOv3
- [ ] 对照论文 *YOLOv3: An Incremental Improvement* 理解多尺度预测与 FPN 结构
- [ ] 实现 Darknet-53 backbone
- [ ] 实现三个尺度检测头（feature pyramid）
- [ ] 完成训练与推理脚本

### YOLOv4 / YOLOv5 / 后续版本（按进度推进）
- [ ] 选择性学习 CSPNet、PANet、Mish 激活、数据增强策略（Mosaic、MixUp）

---

## 阶段二：Docker 容器化与环境固化（小新笔记本）

### 目标
构建一个**可复用的容器化环境**，使训练脚本在任何机器上只需 `docker compose up` 即可运行。

### 具体任务
- [ ] 编写 `Dockerfile`：基于 `pytorch/pytorch:2.x-cuda12.x-runtime`，安装 opencv-python、albumentations、matplotlib 等依赖
- [ ] 编写 `docker-compose.yml`：挂载数据卷与代码目录，配置 GPU 资源
- [ ] 编写 `.dockerignore`：排除 `__pycache__`、`checkpoints/` 等
- [ ] 在本地（小新）验证容器内训练流程可正常运转
- [ ] 编写 `requirements.txt` 或 `environment.yml` 作为备选方案

---

## 阶段三：远程训练（4060 Laptop）

### 目标
利用 4060 笔记本的 GPU 算力执行训练，小新笔记本负责代码开发与任务提交。

### 具体任务
- [ ] 4060 Laptop 环境准备：安装 Docker + NVIDIA Container Toolkit
- [ ] 代码仓库推送至 GitHub（`git push`）
- [ ] 4060 Laptop `git clone` 仓库并执行 `docker compose up` 启动训练
- [ ] 训练产物（checkpoint、日志、TensorBoard）回传或挂载到共享目录
- [ ] 建立标准操作流程：小新 → push 代码 → 4060 pull → 执行训练 → 结果回传

---

## 阶段四：仓库重构与规范化

### 目标
将项目重构为结构清晰、可复现、符合学术规范的代码仓库。

### 目录结构规划

```
YOLO/
├── README.md                    # 项目说明、安装、使用方法
├── ProjectPlan.md               # 当前文件
├── requirements.txt             # Python 依赖清单
├── environment.yml              # Conda 环境配置文件
├── Dockerfile                   # 容器构建
├── docker-compose.yml           # 一键启动训练
├── .dockerignore
├── .gitignore
├── config/                      # 配置文件
│   ├── default.yaml             # 默认训练参数
│   └── voc.yaml                 # VOC 数据集参数
├── data/                        # 数据集（gitignore）
│   └── VOCdevkit/
├── models/                      # 各版本模型实现
│   ├── __init__.py
│   ├── yolo_v1/
│   │   ├── __init__.py
│   │   ├── model.py             # 从 YOLOv1/ 迁移
│   │   ├── loss.py
│   │   └── utils.py
│   ├── yolo_v2/
│   │   ├── __init__.py
│   │   ├── model.py
│   │   ├── loss.py
│   │   └── utils.py
│   └── yolo_v3/
│       ├── __init__.py
│       ├── model.py
│       ├── loss.py
│       └── utils.py
├── utils/                       # 通用工具
│   ├── __init__.py
│   ├── dataset.py               # 数据加载与预处理
│   ├── transforms.py            # 数据增强
│   ├── metrics.py               # mAP / IoU 计算
│   └── visualize.py             # 检测框绘制
├── scripts/                     # 运行脚本
│   ├── train.py                 # 统一训练入口
│   ├── detect.py                # 统一推理入口
│   └── eval.py                  # 统一评估入口
├── checkpoints/                 # 模型权重（gitignore）
├── logs/                        # 训练日志 + TensorBoard（gitignore）
└── docs/                        # 文档
    ├── git-commands-guide.md
    ├── powershell-commands-guide.md
    ├── docker-commands-guide.md
    └── wsl-commands-guide.md
```

### 重构任务
- [ ] 统一模型接口：所有 YOLO 版本继承同一个 `BaseDetector` 抽象类
- [ ] 统一训练/推理入口：`scripts/train.py` 通过配置文件切换版本
- [ ] 完善文档：每个模块的 docstring + README 使用说明
- [ ] 添加单元测试（pytest）：模型前向、loss 计算、数据加载
- [ ] 添加 GitHub Actions：代码格式检查（ruff）+ 基础测试

---

## 时间线

| 阶段 | 时间节点 | 关键产出 |
|------|----------|----------|
| **阶段一** YOLOv1 完整实现 | 国际课程周内 | 可训练的 YOLOv1，VOC mAP 达标 |
| **阶段一** YOLOv2/YOLOv3 实现 | 国际课程周内至第二周 | Darknet-19/53，多尺度预测 |
| **阶段二** 容器化 | 与阶段一并行 | Dockerfile + docker-compose.yml |
| **阶段三** 远程训练 | 阶段二完成后 1-2 天 | 4060 Laptop 训练流程跑通 |
| **阶段四** 仓库重构 | 暑假剩余时间 | 规范化的 GitHub 仓库 |
| TLS 课题衔接 | 暑假后半段 | 从 YOLO 仓库经验过渡至 TLS 研究 |

---

## 环境与工具汇总

| 机器 | 角色 | 配置 |
|------|------|------|
| **小新笔记本** | 开发、调试、Docker 编排 | 日常开发环境 |
| **4060 Laptop** | 训练、推理 | NVIDIA RTX 4060 8GB |

| 工具 | 用途 |
|------|------|
| VS Code + WSL 扩展 | 代码编写与远程开发 |
| WSL 2 (Ubuntu) | Linux 开发环境 |
| Docker + Docker Compose | 环境容器化与一键部署 |
| Git + GitHub | 版本控制与代码分发 |
| Conda / pip | Python 依赖管理 |
| PyTorch + CUDA | 深度学习框架 |