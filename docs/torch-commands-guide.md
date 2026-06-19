# PyTorch 新手使用指南

> 本指南面向 PyTorch 初学者，涵盖从张量操作到完整训练流程的核心内容。
> PyTorch 是目前最主流的深度学习框架，以动态计算图和 Pythonic 风格著称。

---

## 一、核心概念

| 概念 | 说明 | 类比 |
|------|------|------|
| **Tensor（张量）** | 多维数组，PyTorch 的基本数据结构 | NumPy 的 `ndarray` + GPU 支持 |
| **Autograd** | 自动求导系统，自动计算梯度 | 链式求导法则的自动实现 |
| **nn.Module** | 所有网络层的基类 | 乐高积木的底板 |
| **Dataset / DataLoader** | 数据加载与批处理 | 流水线传送带 |
| **Optimizer** | 优化器，根据梯度更新参数 | 方向盘（SGD） vs 导航仪（Adam） |
| **Loss Function** | 损失函数，衡量预测与真实值的差距 | 考试得分对答案的偏差 |

### PyTorch 与 TensorFlow/Keras 对比

| 特性 | PyTorch | TensorFlow 2.x / Keras |
|------|---------|------------------------|
| 计算图 | **动态图**（Define-by-Run） | 静态图（Graph Mode）为主 |
| 调试体验 | 原生 Python，可用 `pdb` 打断点 | Eager 模式也可调试，但性能模式下受限 |
| 学术社区 | 更主流 | 工业部署更广泛 |
| API 风格 | 灵活，显式控制每一步 | `model.fit()` 高度封装 |
| 部署 | TorchScript、ONNX、TorchServe | TFLite、TF Serving |

---

## 二、Tensor 基础操作

Tensor 是 PyTorch 的基石，所有运算都围绕它展开。

### 创建 Tensor

```python
import torch
import numpy as np

# ---- 从数据创建 ----
torch.tensor([1, 2, 3])                    # 从列表
torch.tensor([[1, 2], [3, 4]])             # 从嵌套列表
torch.tensor(np.array([1, 2, 3]))          # 从 NumPy 数组
torch.from_numpy(np.array([1, 2, 3]))      # 与 NumPy 共享内存（更快）

# ---- 特殊张量 ----
torch.zeros(3, 4)           # 全零 3×4
torch.ones(2, 3, 4)         # 全一 2×3×4
torch.eye(4)                # 4×4 单位矩阵
torch.full((2, 3), 7.0)     # 用 7 填充 2×3
torch.empty(3, 4)           # 未初始化（内容随机）

# ---- 序列张量 ----
torch.arange(0, 10, 2)      # tensor([0, 2, 4, 6, 8])
torch.linspace(0, 1, 5)     # tensor([0.00, 0.25, 0.50, 0.75, 1.00])

# ---- 随机张量 ----
torch.rand(3, 4)            # [0, 1) 均匀分布
torch.randn(3, 4)           # 标准正态分布 N(0, 1)
torch.randint(0, 10, (3, 4)) # [0, 10) 随机整数

# ---- 类似现有张量 ----
x = torch.randn(3, 4)
torch.zeros_like(x)         # 形状与 x 相同的全零张量
torch.randn_like(x)         # 形状与 x 相同的随机张量
```

### Tensor 属性

```python
x = torch.randn(2, 3, 4)

x.shape        # torch.Size([2, 3, 4])
x.size()       # 同 shape
x.size(0)      # 第 0 维大小 → 2
x.dtype        # torch.float32
x.device       # cpu / cuda:0
x.ndim         # 维度数 → 3
x.numel()      # 元素总数 → 2×3×4 = 24

# 常用 dtype
# torch.float32 / torch.float — 默认
# torch.float16               — 半精度（省显存）
# torch.float64 / torch.double — 双精度
# torch.int32 / torch.int64
# torch.bool
```

### 索引与切片（与 NumPy 一致）

```python
x = torch.arange(12).reshape(3, 4)
# tensor([[ 0,  1,  2,  3],
#         [ 4,  5,  6,  7],
#         [ 8,  9, 10, 11]])

x[0]            # 第一行 → tensor([0, 1, 2, 3])
x[0, 2]         # 第一行第三列 → tensor(2)
x[:, 1]         # 所有行第二列 → tensor([1, 5, 9])
x[:2, 1:]       # 前两行，第二列起
x[x > 5]        # 布尔索引 → tensor([6, 7, 8, 9, 10, 11])
x[[0, 2]]       # 取第 0、2 行
```

### 形状操作

```python
x = torch.randn(2, 3, 4)       # [2, 3, 4]

# 变形（reshape）
x.reshape(6, 4)                # [6, 4]  自动计算
x.reshape(-1, 4)               # -1 表示自动推导
x.view(6, 4)                   # 必须内存连续，否则用 .contiguous().view()

# 增删维度
x.unsqueeze(0)                 # [1, 2, 3, 4]  在第 0 位插入
x.unsqueeze(-1)                # [2, 3, 4, 1]  在最后插入
x.squeeze()                    # 删除所有大小为 1 的维度

# 转置与重排
x.transpose(0, 2)              # 交换第 0 和第 2 维
x.permute(2, 0, 1)             # 按指定顺序重排维度

# 展平
x.flatten()                    # [24]
x.flatten(start_dim=1)         # 从第 1 维开始展平 → [2, 12]

# 拼接与堆叠
torch.cat([a, b], dim=0)       # 沿指定维度拼接（维度数不变）
torch.stack([a, b], dim=0)     # 新维度堆叠（维度数 +1）

# 分割
x.chunk(3, dim=0)              # 均分为 3 块
x.split([2, 1, 1], dim=1)      # 按指定大小分
```

### 运算与广播

```python
a = torch.randn(2, 3)
b = torch.randn(2, 3)

# 逐元素运算
a + b       # 加法
a - b       # 减法
a * b       # 逐元素乘法（不是矩阵乘法！）
a / b       # 除法
a ** 2      # 幂

# 矩阵运算
torch.matmul(a, b.T)           # 矩阵乘法
a @ b.T                        # @ 运算符等价于 matmul
torch.bmm(batch_a, batch_b)    # 批量矩阵乘 [N, M, K] @ [N, K, L]

# 归约运算
x.sum()                        # 全部求和
x.sum(dim=0)                   # 沿第 0 维求和（降维）
x.sum(dim=0, keepdim=True)     # 保留维度
x.mean() / x.max() / x.min() / x.std() / x.var()

# 广播机制
# [3, 1] + [1, 4] → [3, 4]  自动扩展
# 规则：从最后一维往前对齐，维度为 1 或缺失则复制

# 原地操作（以 _ 结尾，节省内存）
x.add_(1)                      # x = x + 1
x.mul_(2)                      # x = x * 2
x.zero_()                      # x 归零
```

### 数据类型与设备转移

```python
x = torch.randn(3, 4)

# 数据类型转换
x.float()                       # → float32（默认）
x.double()                      # → float64
x.half()                        # → float16（节省显存）
x.int() / x.long() / x.bool()
x.to(torch.float16)             # 通用写法

# 设备转移
x.cpu()                         # 移到 CPU
x.cuda()                        # 移到 GPU（默认 cuda:0）
x.to("cuda:0")                  # 移到指定 GPU
x.to("cuda")                    # 同上
x.to(device)                    # device = torch.device("cuda:0")
```

---

## 三、Autograd — 自动求导

这是 PyTorch 最核心的机制：**记录每个操作，构建计算图，自动反向传播求梯度**。

### 基本用法

```python
# 创建一个需要梯度的张量
x = torch.randn(3, requires_grad=True)
# 或
x = torch.randn(3)
x.requires_grad_(True)

# 前向计算
y = x * 3 + 2         # y = 3x + 2
z = y.sum()           # z = sum(3x + 2)

# 反向传播
z.backward()          # 计算 ∂z/∂x
print(x.grad)         # tensor([3., 3., 3.])  ∂z/∂x = 3

# 梯度会累加！每次 backward 前需要清零
x.grad.zero_()
```

### 计算图控制

```python
# ---- 禁用梯度（推理 / 评估时） ----
with torch.no_grad():
    y = model(x)        # 不记录计算图，节省显存，加速

# 等价写法（装饰器）
@torch.no_grad()
def evaluate(model, data):
    ...

# ---- 冻结参数（迁移学习） ----
for param in model.backbone.parameters():
    param.requires_grad = False

# ---- 只计算局部梯度 ----
x = torch.randn(3, requires_grad=True)
y = x ** 2
y[0].backward()         # 只对 y[0] 反向传播

# ---- 不追踪某段计算 ----
y = x ** 2
y_detached = y.detach() # 从计算图中截断，无梯度
```

### 常见梯度陷阱

```python
# ❌ 错误：Python 标量不能 backward
x = torch.randn(3, requires_grad=True)
y = x.sum().item()      # .item() 返回 Python 数字，脱离计算图
# y.backward()          # 报错！

# ✅ 正确：保持 Tensor 形式
z = x.sum()
z.backward()

# ❌ 错误：原地操作破坏计算图
x = torch.randn(3, requires_grad=True)
y = x * 2
# x += 1                # 原地修改会破坏反向传播所需的计算图

# ✅ 正确：使用非原地版本
x = x + 1               # 创建新张量，保留旧张量在图中
```

---

## 四、nn.Module — 搭建网络

### 基本模式

```python
import torch.nn as nn
import torch.nn.functional as F

class MyNet(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        # 有可学习参数的层：写在 __init__，赋值给 self
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, output_dim)
        self.bn = nn.BatchNorm1d(hidden_dim)
        self.dropout = nn.Dropout(0.3)

    def forward(self, x):
        # 无参数的运算：直接写在 forward
        x = self.fc1(x)
        x = self.bn(x)
        x = F.relu(x)               # 无参数，用 F.relu 或 torch.relu
        x = self.dropout(x)
        x = self.fc2(x)
        return x
```

### 常用层速查

**全连接与卷积**：

| 层 | 用途 | 示例 |
|----|------|------|
| `nn.Linear(in, out)` | 全连接 | `nn.Linear(784, 256)` |
| `nn.Conv2d(in, out, k, stride, padding)` | 2D 卷积 | `nn.Conv2d(3, 64, 3, 1, 1)` |
| `nn.ConvTranspose2d` | 转置卷积（上采样） | `nn.ConvTranspose2d(256, 128, 3, 2, 1)` |
| `nn.MaxPool2d(k)` | 最大池化 | `nn.MaxPool2d(2, 2)` |
| `nn.AvgPool2d(k)` | 平均池化 | `nn.AdaptiveAvgPool2d(1)` |
| `nn.BatchNorm2d(c)` | 2D 批归一化 | `nn.BatchNorm2d(64)` |
| `nn.LayerNorm(d)` | 层归一化（Transformer） | `nn.LayerNorm(512)` |
| `nn.Dropout(p)` | 随机失活 | `nn.Dropout(0.5)` |
| `nn.Flatten()` | 展平 | `nn.Flatten()` |

**激活函数**（无参数，通常用 `F.` 调用）：

| 函数 | 特点 |
|------|------|
| `F.relu(x)` | 最常用，训练快 |
| `F.leaky_relu(x, 0.1)` | YOLO 常用，避免神经元死亡 |
| `F.silu(x)` | 即 Swish，YOLOv4+ 使用 |
| `F.gelu(x)` | Transformer / ViT 使用 |
| `F.sigmoid(x)` | 二分类输出 / 门控 |
| `F.softmax(x, dim=-1)` | 多分类输出 |

### Sequential — 简单网络快捷写法

```python
# 层按顺序连接时可用 Sequential
model = nn.Sequential(
    nn.Conv2d(3, 64, 3, padding=1),
    nn.BatchNorm2d(64),
    nn.ReLU(inplace=True),
    nn.MaxPool2d(2),
    nn.Conv2d(64, 128, 3, padding=1),
    nn.BatchNorm2d(128),
    nn.ReLU(inplace=True),
    nn.AdaptiveAvgPool2d(1),
    nn.Flatten(),
    nn.Linear(128, 10),
)
```

### 权重初始化

```python
def init_weights(m):
    if isinstance(m, nn.Conv2d):
        nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
        if m.bias is not None:
            nn.init.constant_(m.bias, 0)
    elif isinstance(m, nn.BatchNorm2d):
        nn.init.constant_(m.weight, 1)
        nn.init.constant_(m.bias, 0)
    elif isinstance(m, nn.Linear):
        nn.init.normal_(m.weight, 0, 0.01)
        nn.init.constant_(m.bias, 0)

model.apply(init_weights)    # 递归应用到所有子模块
```

### 查看模型结构

```python
print(model)                   # 打印网络结构
print(sum(p.numel() for p in model.parameters()))       # 总参数量
print(sum(p.numel() for p in model.parameters() if p.requires_grad))  # 可训练参数量

# 使用 torchinfo（需要 pip install torchinfo）
from torchinfo import summary
summary(model, input_size=(1, 3, 448, 448))
```

---

## 五、Dataset 与 DataLoader

### 自定义 Dataset

```python
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import json

class VOCDataset(Dataset):
    """Pascal VOC 目标检测数据集"""

    def __init__(self, root, split='train', transform=None):
        self.root = root
        self.transform = transform
        self.samples = self._load_annotations(split)

    def _load_annotations(self, split):
        """读取标注文件，返回样本列表"""
        samples = []
        # 实际解析 VOC 的 XML 标注...
        return samples

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        """返回 (image, target) 元组"""
        img_path, label = self.samples[idx]
        image = Image.open(img_path).convert('RGB')

        if self.transform:
            image = self.transform(image)

        return image, label
```

### DataLoader 关键参数

```python
train_loader = DataLoader(
    dataset,                    # Dataset 实例
    batch_size=32,              # 每批大小
    shuffle=True,               # 每个 epoch 是否打乱
    num_workers=4,              # 子进程数（Windows 下可能需设为 0）
    pin_memory=True,            # 加速 GPU 传输（数据放锁页内存）
    drop_last=True,             # 丢弃最后不完整 batch（BatchNorm 需要）
    collate_fn=None,            # 自定义批处理函数
)

# collate_fn 示例：自动 padding
def collate_fn(batch):
    images = [item[0] for item in batch]
    targets = [item[1] for item in batch]
    images = torch.stack(images)                    # [B, C, H, W]
    return images, targets
```

### Windows 下注意

```python
# Windows 上 num_workers > 0 需要 if __name__ == "__main__" 保护
if __name__ == "__main__":
    train_loader = DataLoader(dataset, batch_size=32, num_workers=4)
```

---

## 六、训练流程（标准模板）

### 完整训练循环

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm

def train_one_epoch(model, loader, criterion, optimizer, device, epoch):
    model.train()                          # ✅ 训练模式
    running_loss = 0.0

    pbar = tqdm(loader, desc=f'Epoch {epoch}')
    for batch_idx, (images, targets) in enumerate(pbar):
        images = images.to(device)
        targets = targets.to(device)

        # ---- 1. 清零梯度 ----
        optimizer.zero_grad()

        # ---- 2. 前向传播 ----
        outputs = model(images)

        # ---- 3. 计算损失 ----
        loss = criterion(outputs, targets)

        # ---- 4. 反向传播 ----
        loss.backward()

        # ---- 5. 更新参数 ----
        optimizer.step()

        # ---- 日志 ----
        running_loss += loss.item()
        pbar.set_postfix({'loss': f'{loss.item():.4f}'})

    return running_loss / len(loader)


def validate(model, loader, criterion, device):
    model.eval()                           # ✅ 评估模式
    total_loss = 0.0

    with torch.no_grad():                  # ✅ 不计算梯度
        for images, targets in loader:
            images = images.to(device)
            targets = targets.to(device)
            outputs = model(images)
            loss = criterion(outputs, targets)
            total_loss += loss.item()

    return total_loss / len(loader)


# ===== 主训练逻辑 =====
def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Using device: {device}')

    # 模型 / 损失 / 优化器 / 调度器
    model = MyNet(input_dim=784, hidden_dim=256, output_dim=10).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=100)

    writer = SummaryWriter('logs/')      # TensorBoard

    best_loss = float('inf')
    for epoch in range(1, 101):
        train_loss = train_one_epoch(model, train_loader, criterion, optimizer, device, epoch)
        val_loss = validate(model, val_loader, criterion, device)

        scheduler.step()                 # 更新学习率

        writer.add_scalar('Loss/train', train_loss, epoch)
        writer.add_scalar('Loss/val', val_loss, epoch)
        writer.add_scalar('LR', scheduler.get_last_lr()[0], epoch)

        # 保存最优模型
        if val_loss < best_loss:
            best_loss = val_loss
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': val_loss,
            }, 'best_model.pth')

    writer.close()
```

### optimizer.zero_grad() 为什么必须写

```python
# PyTorch 梯度默认累加
# 不手动清零，前一次 backward 的梯度会和后一次叠加 → 训练出错

# 三种清零方式：
optimizer.zero_grad()               # 常用
model.zero_grad()                   # 直接清模型参数的 .grad
for param in model.parameters():
    param.grad = None               # 最高效（不分配新内存）
```

### model.train() vs model.eval()

| 模式 | Dropout | BatchNorm | 用途 |
|------|---------|-----------|------|
| `model.train()` | 生效（随机丢神经元） | 用当前 batch 统计量 | **训练** |
| `model.eval()` | 不生效（全保留） | 用训练时的滑动均值 | **推理 / 验证** |

---

## 七、优化器与学习率调度

### 常用优化器

```python
# SGD + Momentum（YOLOv1 原论文用这个）
optim.SGD(model.parameters(), lr=0.01, momentum=0.9, weight_decay=5e-4)

# Adam（最通用，收敛快）
optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)

# AdamW（解耦权重衰减，现在推荐）
optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-2)

# RMSprop（RNN / LSTM）
optim.RMSprop(model.parameters(), lr=1e-3)
```

### 常用学习率调度器

```python
# ---- 阶梯式下降 ----
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=30, gamma=0.1)
# 每 30 epoch ×0.1

# ---- 多阶梯（YOLO 常用：在某几个 epoch 下降） ----
scheduler = optim.lr_scheduler.MultiStepLR(optimizer, milestones=[60, 90], gamma=0.1)
# 第 60、90 epoch ×0.1

# ---- 余弦退火（当前主流） ----
scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=100)
# 100 epoch 内从 lr→0 余弦下降

# ---- 余弦退火 + 热重启 ----
scheduler = optim.lr_scheduler.CosineAnnealingWarmRestarts(optimizer, T_0=20, T_mult=2)

# ---- Warmup + 余弦（自定义组合） ----
# 前 5 epoch 线性上升 lr → 随后余弦下降
```

---

## 八、模型的保存与加载

### 保存

```python
# ❌ 只保存权重（推荐）
torch.save(model.state_dict(), 'model_weights.pth')

# ✅ 保存完整 checkpoint（可恢复训练）
checkpoint = {
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'scheduler_state_dict': scheduler.state_dict(),
    'loss': val_loss,
    'config': {'lr': 1e-3, 'batch_size': 32},  # 训练配置
}
torch.save(checkpoint, 'checkpoint_epoch50.pth')

# ⚠ 保存整个模型（不推荐，依赖文件结构）
torch.save(model, 'entire_model.pth')
```

### 加载

```python
# 加载权重
model = MyNet().to(device)
model.load_state_dict(torch.load('model_weights.pth', weights_only=True))

# 加载 checkpoint 并恢复训练
checkpoint = torch.load('checkpoint_epoch50.pth', weights_only=True)
model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
start_epoch = checkpoint['epoch'] + 1

# 跨设备加载（CPU 上加载 GPU 保存的模型）
checkpoint = torch.load('model.pth', map_location='cpu')

# 加载到指定 GPU
checkpoint = torch.load('model.pth', map_location='cuda:0')
```

---

## 九、GPU 使用与多卡训练

### 单 GPU

```python
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'GPU: {torch.cuda.get_device_name(0)}')     # 显卡型号
print(f'VRAM: {torch.cuda.get_device_properties(0).total_mem / 1e9:.1f} GB')

model = model.to(device)

# 训练时，数据和模型必须在同一设备
images = images.to(device)
targets = targets.to(device)

# 查看显存占用
print(f'{torch.cuda.memory_allocated() / 1e9:.2f} GB')
print(f'{torch.cuda.max_memory_allocated() / 1e9:.2f} GB')

# 清空缓存（释放碎片显存）
torch.cuda.empty_cache()
```

### 多 GPU — DataParallel（简单，单机多卡）

```python
model = nn.DataParallel(model)
model = model.to('cuda:0')

# 用法完全一样，自动拆分 batch 到多张卡
# 缺点：负载不均衡，主卡压力大
```

### 多 GPU — DistributedDataParallel（推荐）

```python
# 每个 GPU 启动一个独立进程
# torchrun --nproc_per_node=2 train.py

import torch.distributed as dist

def setup():
    dist.init_process_group(backend='nccl')   # NCCL 是 NVIDIA 的通信库

def cleanup():
    dist.destroy_process_group()

# 模型封装
model = nn.parallel.DistributedDataParallel(model, device_ids=[local_rank])

# DataLoader 需要用 DistributedSampler
sampler = DistributedSampler(dataset)
loader = DataLoader(dataset, batch_size=32, sampler=sampler)
```

### 混合精度训练（节省显存，加速）

```python
scaler = torch.amp.GradScaler('cuda')        # PyTorch 2.0+

for images, targets in loader:
    optimizer.zero_grad()

    with torch.amp.autocast('cuda'):          # 自动混合精度
        outputs = model(images)
        loss = criterion(outputs, targets)

    scaler.scale(loss).backward()             # 缩放 loss 防止下溢
    scaler.step(optimizer)
    scaler.update()
```

---

## 十、调试与可视化

### 常用调试技巧

```python
# 1. 检查梯度是否正常
for name, param in model.named_parameters():
    if param.grad is not None:
        grad_norm = param.grad.norm()
        if grad_norm > 100:                  # 梯度爆炸
            print(f'{name}: grad={grad_norm:.2f} ⚠')
        if grad_norm < 1e-7 and param.requires_grad:
            print(f'{name}: grad≈0 ← 可能梯度消失')

# 2. 梯度裁剪（防止梯度爆炸）
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=10.0)

# 3. 检查哪个参数没有梯度
for name, param in model.named_parameters():
    if param.requires_grad and param.grad is None:
        print(f'{name} 未被使用！')

# 4. 检查 NaN
if torch.isnan(loss):
    print(f'NaN at epoch {epoch}, batch {batch_idx}')
    # 可能原因：lr 过大 / 数据有异常值 / 除零
    break

# 5. 用 torch.autograd.detect_anomaly() 定位 NaN 来源
with torch.autograd.detect_anomaly():
    outputs = model(images)
    loss = criterion(outputs, targets)
    loss.backward()
```

### TensorBoard 可视化

```python
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter('logs/experiment1')

# 标量（loss、lr、mAP 等）
writer.add_scalar('Loss/train', loss, epoch)
writer.add_scalar('LR', lr, epoch)

# 图像（检测框、分割 mask）
writer.add_image('train/sample', images[0], epoch)

# 模型图
writer.add_graph(model, torch.randn(1, 3, 448, 448).to(device))

# 直方图（权重分布）
writer.add_histogram('conv1.weight', model.conv1.weight, epoch)

writer.close()

# 命令行启动 TensorBoard
# tensorboard --logdir=logs/ --port=6006
# 浏览器访问 http://localhost:6006
```

### 常用性能分析

```python
# 测量每层耗时
import time

start = torch.cuda.Event(enable_timing=True)
end = torch.cuda.Event(enable_timing=True)

start.record()
outputs = model(images)
end.record()
torch.cuda.synchronize()
print(f'Forward: {start.elapsed_time(end):.2f} ms')

# 或使用 PyTorch Profiler
with torch.profiler.profile(
    activities=[torch.profiler.ProfilerActivity.CPU,
                torch.profiler.ProfilerActivity.CUDA],
) as prof:
    outputs = model(images)
print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=10))
```

---

## 十一、torchvision 常用工具

```python
import torchvision
import torchvision.transforms as T
import torchvision.transforms.functional as TF

# ---- 数据集 ----
# ImageNet
train_set = torchvision.datasets.ImageNet('path/', split='train', transform=...)

# CIFAR-10（快速验证）
train_set = torchvision.datasets.CIFAR10('data/', train=True, transform=..., download=True)

# 自定义文件夹
train_set = torchvision.datasets.ImageFolder('data/train/', transform=...)

# ---- 数据增强流程 ----
transform = T.Compose([
    T.Resize((448, 448)),
    T.RandomHorizontalFlip(p=0.5),
    T.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
    T.ToTensor(),                              # [0,255] → [0,1] + CHW
    T.Normalize(mean=[0.485, 0.456, 0.406],   # ImageNet 均值
                std=[0.229, 0.224, 0.225]),    # ImageNet 标准差
])

# ---- 预训练模型 ----
model = torchvision.models.resnet50(pretrained=True)
model = torchvision.models.resnet50(weights=torchvision.models.ResNet50_Weights.DEFAULT)  # 新版 API

# 替换分类头（迁移学习）
model.fc = nn.Linear(model.fc.in_features, num_classes)

# ---- 常用算子 ----
# NMS（非极大值抑制）
torchvision.ops.nms(boxes, scores, iou_threshold=0.5)

# IoU / 边界框
torchvision.ops.box_iou(boxes1, boxes2)
```

---

## 十二、常用训练技巧速查

| 技巧 | 代码 | 说明 |
|------|------|------|
| 梯度裁剪 | `clip_grad_norm_(model.parameters(), 10)` | 防止梯度爆炸 |
| 标签平滑 | `nn.CrossEntropyLoss(label_smoothing=0.1)` | 防止过拟合 |
| EMA（指数滑动平均） | 维护参数的滑动平均作为推理权重 | 提升泛化 |
| 梯度累积 | 每 N 步才 `optimizer.step()` | 模拟大 batch |
| Warmup | 前 K 步 lr 线性增大 | 稳定训练初期 |
| Early Stopping | val_loss 连续 N epoch 不降则停 | 防止过拟合 |
| 权重正则化 | `weight_decay=5e-4` | L2 正则化 |

### 梯度累积示例

```python
accumulation_steps = 4                              # 模拟 batch_size ×4

for i, (images, targets) in enumerate(loader):
    outputs = model(images)
    loss = criterion(outputs, targets) / accumulation_steps
    loss.backward()                                 # 梯度累加

    if (i + 1) % accumulation_steps == 0:
        optimizer.step()                            # 每 4 步更新一次
        optimizer.zero_grad()
```

### EMA 示例

```python
class EMA:
    def __init__(self, model, decay=0.9999):
        self.model = model
        self.decay = decay
        self.shadow = {name: param.data.clone() for name, param in model.named_parameters()}

    def update(self):
        for name, param in self.model.named_parameters():
            self.shadow[name] = self.decay * self.shadow[name] + (1 - self.decay) * param.data

    def apply(self):
        """推理时将 EMA 权重写入模型"""
        for name, param in self.model.named_parameters():
            param.data.copy_(self.shadow[name])

# 每个 step 后调用 ema.update()
# 推理前调用 ema.apply()
```

---

## 十三、常用代码片段速查

| 场景 | 代码 |
|------|------|
| 检查 GPU 是否可用 | `torch.cuda.is_available()` |
| 获取显卡名称 | `torch.cuda.get_device_name(0)` |
| 张量转 NumPy | `x.cpu().numpy()` / `x.detach().cpu().numpy()` |
| NumPy 转张量 | `torch.from_numpy(arr)` |
| 冻结模型参数 | `param.requires_grad = False` |
| 获取当前学习率 | `optimizer.param_groups[0]['lr']` |
| 随机种子固定 | `torch.manual_seed(42)` |
| 完整复现性 | 见下方代码块 |
| 遍历所有参数 | `model.named_parameters()` |
| 只遍历可训练参数 | `filter(lambda p: p.requires_grad, model.parameters())` |
| 获取模型设备 | `next(model.parameters()).device` |
| 查看批次数据形状 | `print(images.shape, targets.shape)` |
| 计算预测准确率 | `(outputs.argmax(1) == targets).float().mean()` |
| 释放 GPU 缓存 | `torch.cuda.empty_cache()` |

### 设置随机种子（完整复现）

```python
import random
import numpy as np

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)             # 多卡
    torch.backends.cudnn.deterministic = True    # 牺牲一点速度
    torch.backends.cudnn.benchmark = False

set_seed(42)
```

---

## 十四、常见报错与解决

| 报错 | 原因 | 解决 |
|------|------|------|
| `RuntimeError: Expected all tensors to be on the same device` | 模型和数据的设备不一致 | 统一 `.to(device)` |
| `RuntimeError: CUDA out of memory` | 显存不够 | 减小 batch_size / 用混合精度 / 梯度累积 |
| `RuntimeError: expected scalar type Float but found Double` | 数据类型不一致 | `x.float()` 统一为 float32 |
| `RuntimeError: shape '[...]' is invalid` | 形状不匹配 | `print(x.shape)` 逐层检查 |
| `UserWarning: volatile was removed` | API 废弃 | 用 `torch.no_grad()` 替代 |
| `IndexError: index out of range in self` | 数据索取出错 | 检查 `__len__` 和 `__getitem__` |
| `AttributeError: 'NoneType' object has no attribute 'data'` | Dataset 返回了 None | 检查 `__getitem__` 返回值 |
| `BrokenPipeError: [Errno 32]` (Windows) | num_workers > 0 问题 | 先设 `num_workers=0` 排查 |
| `UserWarning: The given NumPy array is not writable` | Tensor → NumPy 共享内存 | `.copy()` 创建副本 |
| `NVIDIA driver is too old` | 驱动版本不够 | 更新 NVIDIA 驱动 |

---

## 十五、版本兼容注意

### PyTorch 版本差异

| 特性 | 旧写法 | 新写法（2.0+） |
|------|--------|----------------|
| 编译加速 | — | `model = torch.compile(model)` |
| 混合精度 | `torch.cuda.amp` | `torch.amp` |
| 模型权重 | `pretrained=True` | `weights=Weights.DEFAULT` |
| 设备设置 | `model.cuda()` | `model.to(device)` |
| 保存加载 | `torch.save(obj, f)` | 建议加 `weights_only=True` |

### PyTorch 2.0+ torch.compile 使用

```python
# 一行代码获得免费加速（需 PyTorch 2.0+）
model = torch.compile(model)

# 或选模式
model = torch.compile(model, mode="reduce-overhead")  # 小 batch 时
model = torch.compile(model, mode="max-autotune")      # 最大加速（编译更久）
```

---

> **学习路线建议**：
> 1. 先掌握 Tensor 创建、索引、形状操作（类比 NumPy）
> 2. 理解 Autograd 机制 — `requires_grad` + `backward()` + `no_grad()`
> 3. 学会 `nn.Module` 搭建网络，对照你已有的 `YOLOv1_model.py`
> 4. 背熟训练五步：`zero_grad → forward → loss → backward → step`
> 5. 再逐步深入 GPU 多卡、AMP、TorchScript 部署等进阶内容
