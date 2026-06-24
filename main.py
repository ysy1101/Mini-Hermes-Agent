#!/usr/bin/env python3
"""
RAG 知识库问答智能体 - 主入口
"""
import os
import sys
import argparse
from dotenv import load_dotenv

from agent import RAGAgent, build_index


def cmd_index(args):
    """构建索引子命令"""
    print("📚 正在构建知识库索引...")
    result = build_index(args.data_dir, args.index_dir)
    print(result)


def cmd_query(args):
    """单次查询子命令"""
    api_key = _get_api_key()
    if not api_key:
        return

    agent = _create_agent(api_key, args)
    print(f"🤖 问题：{args.question}\n")
    result = agent.run(args.question)
    print(f"\n📋 回答：\n{result}")


def cmd_interactive(args):
    """交互模式子命令"""
    api_key = _get_api_key()
    if not api_key:
        return

    agent = _create_agent(api_key, args)
    print("🤖 RAG 知识库问答 - 交互模式")
    print(f"📚 知识库：{args.data_dir}/")
    print("输入 'exit' 退出，'stats' 查看统计\n")

    while True:
        try:
            question = input("你: ").strip()
            if question.lower() in ("exit", "quit", "退出"):
                print("👋 再见！")
                break
            if question.lower() == "stats":
                from agent.tools import tool_get_stats
                print(f"\n{tool_get_stats()}\n")
                continue
            if not question:
                continue

            print("\n思考中...")
            result = agent.chat(question)
            print(f"\nAgent: {result}\n")
        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 错误：{e}")


def _get_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    if not api_key:
        print("❌ 错误：未设置 API Key")
        print("请设置环境变量 OPENAI_API_KEY 或在 .env 文件中配置")
    return api_key


def _create_agent(api_key: str, args):
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = args.model or os.getenv("MODEL_NAME", "gpt-4o-mini")

    return RAGAgent(
        api_key=api_key,
        base_url=base_url,
        model=model,
        memory_dir=args.memory_dir,
        skills_dir=args.skills_dir,
        data_dir=args.data_dir,
        max_steps=args.max_steps,
    )


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="RAG 知识库问答智能体",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例：
  python main.py index                          # 构建知识库索引
  python main.py query "什么是RAG"              # 单次查询
  python main.py -i                             # 交互模式
        """
    )

    parser.add_argument("--data-dir", default="data", help="文档目录")
    parser.add_argument("--index-dir", default="chroma_db", help="索引存储目录")
    parser.add_argument("--memory-dir", default="memory", help="记忆文件目录")
    parser.add_argument("--skills-dir", default="skills", help="技能文件目录")
    parser.add_argument("--model", default=None, help="使用的模型")
    parser.add_argument("--max-steps", type=int, default=10, help="最大执行步数")

    subparsers = parser.add_subparsers(dest="command", help="子命令")

    parser_index = subparsers.add_parser("index", help="构建知识库索引")
    parser_index.set_defaults(func=cmd_index)

    parser_query = subparsers.add_parser("query", help="单次查询")
    parser_query.add_argument("question", help="要查询的问题")
    parser_query.set_defaults(func=cmd_query)

    parser_interactive = subparsers.add_parser("interactive", aliases=["i"], help="交互模式")
    parser_interactive.set_defaults(func=cmd_interactive)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == "__main__":
    main()