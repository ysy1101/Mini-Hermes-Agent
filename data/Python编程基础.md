# Python 编程基础

## 变量与数据类型

Python 是动态类型语言，变量无需声明类型。

常见数据类型：
- `int` — 整数，如 `42`
- `float` — 浮点数，如 `3.14`
- `str` — 字符串，如 `"hello"`
- `list` — 列表，如 `[1, 2, 3]`
- `dict` — 字典，如 `{"name": "Alice"}`
- `bool` — 布尔值，`True` / `False`

## 控制流程

### 条件判断
```python
if x > 0:
    print("正数")
elif x < 0:
    print("负数")
else:
    print("零")
```

### 循环
```python
# for 循环遍历可迭代对象
for item in items:
    print(item)

# while 循环
while count > 0:
    count -= 1
```

## 函数

```python
def greet(name, greeting="你好"):
    return f"{greeting}, {name}"

# 调用
result = greet("小明")
```

支持默认参数、关键字参数、可变参数（`*args`, `**kwargs`）。

## 列表推导式

Python 特色语法，简洁创建列表：
```python
squares = [x**2 for x in range(10)]           # [0, 1, 4, 9, 16, ...]
evens = [x for x in range(20) if x % 2 == 0]  # 过滤偶数
```

## 文件操作

```python
# 读取文件
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()

# 写入文件
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello World")
```

使用 `with` 语句自动管理资源，无需手动关闭文件。

## 异常处理

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("不能除以零")
except Exception as e:
    print(f"出错了: {e}")
finally:
    print("清理工作")
```
