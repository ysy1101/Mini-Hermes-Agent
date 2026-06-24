# RAG 知识库问答智能体

基于 RAG（检索增强生成）的个人知识库问答系统。将你的文档放入知识库，然后像聊天一样向它提问，它会从文档中检索相关内容并生成准确回答。

## ✨ 特性

- **📚 多格式文档** - 支持 PDF、Markdown、TXT 格式
- **🔍 语义检索** - 基于 ChromaDB 向量检索，不只是关键词匹配
- **🧠 持久化记忆** - 记住你的偏好和问答历史
- **📎 来源标注** - 每个回答都会标注引用了哪个文档
- **💬 交互模式** - 对话式问答，像聊天一样自然

## 📦 安装

```bash
cd RAGagent

# 安装依赖
pip install -r requirements.txt

# 配置 API Key
cp .env.example .env
# 编辑 .env 文件，填入你的 API Key
```

## 🚀 使用

### 1. 添加文档

将你的文档放入 `data/` 目录：

```bash
cp ~/Documents/产品手册.pdf data/
cp ~/Documents/技术笔记.md data/
```

### 2. 构建索引

```bash
python main.py index
```

### 3. 开始问答

**交互模式：**
```bash
python main.py i
```

**单次查询：**
```bash
python main.py query "产品的主要功能有哪些？"
```

## 📁 项目结构

```
mini-hermes-agent/
├── agent/
│   ├── __init__.py      # 模块导出
│   ├── loop.py          # Agent 主循环（RAG 版）
│   ├── memory.py        # 记忆系统
│   ├── skills.py        # 技能系统
│   ├── document.py      # 文档解析（PDF/MD/TXT）
│   ├── retriever.py     # 向量检索（ChromaDB）
│   └── tools.py         # 5 个 RAG 工具
├── data/                # 📁 放文档的地方
├── chroma_db/           # 向量索引（自动生成）
├── memory/              # 记忆文件
├── skills/              # 技能模板
├── main.py              # 主入口
├── requirements.txt     # 依赖
└── .env.example         # 配置模板
```

## 🔧 内置工具

| 工具 | 功能 |
|------|------|
| `search_knowledge` | 语义搜索知识库 |
| `read_document` | 读取文档完整内容 |
| `list_documents` | 列出所有文档 |
| `build_index` | 构建/重建索引 |
| `get_stats` | 查看知识库统计 |

## 🎯 工作流程

```
用户提问 → search_knowledge 检索 → 获取相关片段 → 组织回答 → 标注来源 → 返回
```

## 🛠️ 支持的 API

兼容任何 OpenAI 格式的 API，包括：
- OpenAI / Azure OpenAI
- 通义千问 / 豆包 / DeepSeek / 智谱
- OpenRouter
- 本地 Ollama / vLLM

只需在 `.env` 中配置对应的 `OPENAI_BASE_URL` 和 `MODEL_NAME`。

## 📄 License

MIT