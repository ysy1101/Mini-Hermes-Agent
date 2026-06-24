"""
技能系统模块
管理和加载可复用的工作流技能
"""
import os
import re
from typing import Dict, List, Optional


class SkillManager:
    """技能管理器"""
    
    def __init__(self, skills_dir: str = "skills"):
        self.skills_dir = skills_dir
        self.skills: Dict[str, str] = {}
        self._load_skills()
    
    def _load_skills(self):
        """加载所有技能文件"""
        os.makedirs(self.skills_dir, exist_ok=True)
        for filename in os.listdir(self.skills_dir):
            if filename.endswith('.md'):
                name = filename[:-3]  # 去掉 .md
                filepath = os.path.join(self.skills_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    self.skills[name] = f.read()
    
    def get_skill(self, name: str) -> Optional[str]:
        """获取指定技能"""
        return self.skills.get(name)
    
    def list_skills(self) -> List[str]:
        """列出所有技能名称"""
        return list(self.skills.keys())
    
    def find_relevant_skills(self, task: str) -> List[str]:
        """根据任务描述查找相关技能"""
        relevant = []
        task_lower = task.lower()
        for name, content in self.skills.items():
            # 简单的关键词匹配
            if name.lower() in task_lower:
                relevant.append(name)
                continue
            # 检查内容中的关键词
            keywords = re.findall(r'【(.*?)】', content)
            for kw in keywords:
                if kw.lower() in task_lower:
                    relevant.append(name)
                    break
        return relevant
    
    def get_skills_for_prompt(self, task: str) -> str:
        """获取用于 Prompt 的技能描述"""
        relevant = self.find_relevant_skills(task)
        if not relevant:
            return ""
        
        result = "【可用技能】\n"
        for name in relevant:
            content = self.skills[name]
            # 提取技能描述的前几行
            lines = content.strip().split('\n')
            desc = lines[0] if lines else name
            result += f"- {name}: {desc}\n"
        
        result += "\n如果需要使用某个技能，请在回复中明确说明「使用技能：技能名」"
        return result
    
    def create_skill(self, name: str, description: str, steps: List[str]):
        """创建一个新技能"""
        content = f"# {name}\n\n{description}\n\n## 执行步骤\n"
        for i, step in enumerate(steps, 1):
            content += f"{i}. {step}\n"
        
        filepath = os.path.join(self.skills_dir, f"{name}.md")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.skills[name] = content
        return f"技能 {name} 已创建"
