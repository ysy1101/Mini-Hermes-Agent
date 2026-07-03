# Git 版本控制基础

## 什么是 Git

Git 是分布式版本控制系统，由 Linus Torvalds 于 2005 年创建，用于追踪代码变更、协同开发。

## 基本概念

### 工作区、暂存区、仓库
- **工作区**：你正在编辑的文件目录
- **暂存区（Stage）**：`git add` 后暂存变更的地方
- **仓库（Repository）**：`git commit` 后永久保存的地方

### 常用命令

```bash
git init                    # 初始化仓库
git clone <url>             # 克隆远程仓库
git status                  # 查看文件状态
git add <file>              # 添加到暂存区
git commit -m "message"     # 提交变更
git push origin main        # 推送到远程
git pull                    # 拉取远程变更
git log                     # 查看提交历史
```

## 分支管理

```bash
git branch feature          # 创建分支
git checkout feature        # 切换分支
git checkout -b feature     # 创建并切换
git merge feature           # 合并分支
git branch -d feature       # 删除分支
```

### 分支策略
- **Git Flow**：main / develop / feature / release / hotfix
- **GitHub Flow**：main + feature branches，简单直接
- **Trunk-Based**：频繁向主干合并小变更

## 解决冲突

当两个分支修改同一文件的同一位置时产生冲突：
1. `git merge` 或 `git pull` 时触发
2. 手动编辑冲突文件，选择保留的内容
3. `git add` 标记已解决
4. `git commit` 完成合并

## 常用技巧

```bash
git stash                   # 暂存未提交的修改
git stash pop               # 恢复暂存的修改
git reset --soft HEAD~1     # 撤销 commit 但保留修改
git rebase main             # 变基到 main 分支
git cherry-pick <commit>    # 挑选特定提交
```

## 远程仓库

GitHub、GitLab、Gitee 是常见的托管平台。通过 SSH 或 HTTPS 与远程仓库交互。
