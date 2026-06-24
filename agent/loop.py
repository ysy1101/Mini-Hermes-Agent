"""
Agent 主循环模块（RAG 知识库版）
"""
import json
from typing import List, Dict, Any, Optional
from openai import OpenAI

from .memory import MemoryManager
from .skills import SkillManager
from .tools import TOOLS, execute_tool


class RAGAgent:
    """RAG 知识库问答智能体"""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.openai.com/v1",
        model: str = "gpt-4o",
        memory_dir: str = "memory",
        skills_dir: str = "skills",
        data_dir: str = "data",
        max_steps: int = 10,
    ):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.memory = MemoryManager(memory_dir)
        self.skills = SkillManager(skills_dir)
        self.data_dir = data_dir
        self.max_steps = max_steps
        self.messages: List[Dict[str, Any]] = []

    def _build_system_prompt(self) -> str:
        """构建系统提示词"""
        context = self.memory.get_system_context()

        prompt = f"""你是一个专业的个人知识库助手，擅长基于用户的文档进行问答和分析。

{context}

【你的能力】
1. 语义搜索知识库 → 找到与用户问题最相关的文档片段
2. 阅读文档内容 → 了解文档的详细信息
3. 列出文档目录 → 查看知识库中有哪些文档
4. 构建索引 → 添加新文档后更新检索系统

【工作流程】
当用户提问时：
1. 先用 search_knowledge 检索相关文档片段
2. 如果片段不够详细，用 read_document 读取完整文档
3. 基于检索到的内容，组织清晰、准确的回答
4. 回答中标注信息来源（哪个文档）
5. 如果知识库中没有相关内容，诚实告知用户

【回答原则】
- 回答必须基于知识库中的文档内容，不要编造
- 引用文档内容时标注来源
- 如果知识库信息不足以回答，建议用户添加相关文档
- 用简洁清晰的语言组织答案

【知识库位置】{self.data_dir}/ 目录"""

        return prompt

    def run(self, task: str) -> str:
        """运行 Agent 回答问题"""
        system_prompt = self._build_system_prompt()
        self.messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": task}
        ]

        final_answer = ""

        for step in range(self.max_steps):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.messages,
                    tools=TOOLS,
                    tool_choice="auto",
                    temperature=0.3,
                )
            except Exception as e:
                return f"调用模型时出错：{str(e)}"

            msg = response.choices[0].message
            self.messages.append(msg)

            if not msg.tool_calls:
                final_answer = msg.content or "任务完成"
                break

            for tool_call in msg.tool_calls:
                tool_name = tool_call.function.name
                try:
                    tool_args = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    tool_args = {}

                result = execute_tool(tool_name, tool_args)

                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": str(result)
                })
        else:
            final_answer = "已达到最大步骤数，任务未完全完成。"

        return final_answer

    def chat(self, message: str) -> str:
        """多轮对话"""
        if not self.messages:
            return self.run(message)

        self.messages.append({"role": "user", "content": message})
        for step in range(self.max_steps):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.messages,
                    tools=TOOLS,
                    tool_choice="auto",
                    temperature=0.3,
                )
            except Exception as e:
                return f"调用模型时出错：{str(e)}"

            msg = response.choices[0].message
            self.messages.append(msg)

            if not msg.tool_calls:
                return msg.content or "好的"

            for tool_call in msg.tool_calls:
                tool_name = tool_call.function.name
                try:
                    tool_args = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    tool_args = {}

                result = execute_tool(tool_name, tool_args)

                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": str(result)
                })

        return "已达到最大步骤数"