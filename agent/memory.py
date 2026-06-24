"""
记忆系统模块
负责读取和管理持久化记忆
"""
import os
from datetime import datetime


class MemoryManager:
    """记忆管理器"""
    
    def __init__(self, memory_dir: str = "memory"):
        self.memory_dir = memory_dir
        self.memory_file = os.path.join(memory_dir, "MEMORY.md")
        self.user_file = os.path.join(memory_dir, "USER.md")
        self._ensure_files()
    
    def _ensure_files(self):
        """确保记忆文件存在"""
        os.makedirs(self.memory_dir, exist_ok=True)
        if not os.path.exists(self.memory_file):
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                f.write("# 记忆文件\n\n## 项目信息\n\n## 技术栈偏好\n\n## 已完成的任务\n\n## 学到的经验\n")
        if not os.path.exists(self.user_file):
            with open(self.user_file, 'w', encoding='utf-8') as f:
                f.write("# 用户画像\n\n## 基本信息\n\n## 偏好\n\n## 编码习惯\n")
    
    def get_memory(self) -> str:
        """获取全部记忆内容"""
        with open(self.memory_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def get_user_profile(self) -> str:
        """获取用户画像"""
        with open(self.user_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def get_system_context(self) -> str:
        """获取用于 System Prompt 的上下文"""
        memory = self.get_memory()
        user = self.get_user_profile()
        return f"【用户画像】\n{user}\n\n【记忆】\n{memory}"
    
    def append_memory(self, section: str, content: str):
        """向记忆文件追加内容"""
        with open(self.memory_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # 找到对应的 section 并追加
        section_header = f"## {section}"
        if section_header in text:
            lines = text.split('\n')
            insert_idx = -1
            for i, line in enumerate(lines):
                if line.startswith(section_header):
                    # 找到下一个 ## 或文件末尾
                    for j in range(i + 1, len(lines)):
                        if lines[j].startswith('## '):
                            insert_idx = j
                            break
                    if insert_idx == -1:
                        insert_idx = len(lines)
                    break
            
            if insert_idx > 0:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                lines.insert(insert_idx, f"- [{timestamp}] {content}")
                text = '\n'.join(lines)
                
                with open(self.memory_file, 'w', encoding='utf-8') as f:
                    f.write(text)
    
    def update_user_profile(self, info: str):
        """更新用户画像（追加）"""
        with open(self.user_file, 'a', encoding='utf-8') as f:
            f.write(f"\n- {info}\n")
