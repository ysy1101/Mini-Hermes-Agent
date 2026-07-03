# PyTorch 深度学习框架

## 简介

PyTorch 是 Facebook AI Research 团队开发的开源深度学习框架，以动态计算图和 Pythonic 风格著称，是目前学术界和工业界最流行的深度学习框架之一。

## 核心概念

### Tensor（张量）
Tensor 是 PyTorch 中最基本的数据结构，类似 NumPy 的 ndarray，但支持 GPU 加速。

```python
import torch

# 创建张量
x = torch.tensor([1, 2, 3])
y = torch.zeros(3, 4)           # 3x4 全零矩阵
z = torch.randn(2, 3)           # 2x3 随机正态分布矩阵

# GPU 加速
if torch.cuda.is_available():
    x = x.cuda()
```

### 自动求导（Autograd）
PyTorch 的自动微分引擎，自动计算梯度。

```python
x = torch.tensor(2.0, requires_grad=True)
y = x ** 3 + 2 * x + 1
y.backward()                    # 计算 dy/dx
print(x.grad)                   # 输出 14 (3*2² + 2)
```

## 神经网络构建

### nn.Module
所有神经网络的基类：

```python
class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 256)
        self.fc2 = nn.Linear(256, 10)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        return self.fc2(x)
```

### 常用层
- `nn.Linear(in, out)` — 全连接层
- `nn.Conv2d(in_channels, out_channels, kernel_size)` — 卷积层
- `nn.LSTM` / `nn.GRU` — 循环层
- `nn.BatchNorm2d` — 批归一化
- `nn.Dropout(p)` — 随机丢弃，防过拟合

### 损失函数
- `nn.MSELoss()` — 均方误差（回归）
- `nn.CrossEntropyLoss()` — 交叉熵（分类）
- `nn.BCELoss()` — 二分类交叉熵

### 优化器
```python
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
```

## 训练流程

```python
for epoch in range(num_epochs):
    for batch in dataloader:
        optimizer.zero_grad()           # 清零梯度
        output = model(batch)           # 前向传播
        loss = criterion(output, target)# 计算损失
        loss.backward()                 # 反向传播
        optimizer.step()                # 更新参数
```

## 数据加载

```python
dataset = TensorDataset(X, y)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
```

PyTorch 提供 `torchvision.datasets`（图像）、`torchtext`（文本）等常用数据集。
