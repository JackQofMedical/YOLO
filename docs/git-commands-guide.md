# Git 新手命令指南

> 本指南面向 Git 初学者，涵盖日常开发中最常用的命令。
> 每个命令附带说明、示例和使用场景。

---

## 一、环境配置

首次使用 Git 前，需要设置用户信息（每次提交都会附带这些信息）。

```bash
# 设置用户名（全局）
git config --global user.name "你的名字"

# 设置邮箱（全局）
git config --global user.email "your@email.com"

# 查看当前配置
git config --list

# 设置默认编辑器（可选）
git config --global core.editor "code --wait"   # VS Code
git config --global core.editor "notepad"        # 记事本
```

| 参数 | 说明 |
|------|------|
| `--global` | 对当前用户所有仓库生效 |
| `--local` | 仅对当前仓库生效（默认） |
| `--system` | 对系统所有用户生效 |

---

## 二、创建仓库

```bash
# 在当前目录初始化一个新的 Git 仓库
git init

# 克隆远程仓库到本地
git clone https://github.com/用户名/仓库名.git

# 克隆到指定目录
git clone https://github.com/用户名/仓库名.git my-folder

# 克隆指定分支
git clone -b dev https://github.com/用户名/仓库名.git
```

---

## 三、日常开发流程（最常用）

这是你每天都会用到的命令组合：

```bash
# 1. 查看文件状态
git status

# 2. 添加文件到暂存区
git add 文件名.py          # 添加单个文件
git add .                  # 添加所有修改
git add *.py               # 添加所有 .py 文件

# 3. 提交到本地仓库
git commit -m "描述你做了什么修改"

# 4. 推送到远程仓库
git push origin 分支名
```

### 工作区域概念

```
工作区 (Working Directory)
    │
    │  git add
    ▼
暂存区 (Staging Area / Index)
    │
    │  git commit
    ▼
本地仓库 (Local Repository)
    │
    │  git push
    ▼
远程仓库 (Remote Repository)
```

---

## 四、查看状态与日志

```bash
# 查看工作区状态（最常用）
git status

# 查看提交历史
git log

# 简洁模式（一行一条）
git log --oneline

# 图形化显示分支结构
git log --oneline --graph --all

# 查看最近 5 条提交
git log -5

# 查看某个文件的修改历史
git log --follow -p 文件名

# 查看某次提交的具体内容
git show 提交哈希

# 查看工作区与暂存区的差异
git diff

# 查看暂存区与上次提交的差异
git diff --staged

# 查看两次提交之间的差异
git diff 提交A..提交B
```

---

## 五、分支管理

分支是 Git 最强大的功能之一，用于并行开发不同功能。

```bash
# 查看所有本地分支
git branch

# 查看所有分支（包括远程）
git branch -a

# 创建新分支
git branch 新分支名

# 切换分支
git checkout 分支名

# 创建并切换到新分支（常用）
git checkout -b 新分支名

# 删除本地分支（已合并的）
git branch -d 分支名

# 强制删除本地分支
git branch -D 分支名

# 重命名当前分支
git branch -m 新名称
```

### 分支工作流示例

```bash
# 从 main 创建功能分支
git checkout -b feature/login

# 开发完成后切回 main 并合并
git checkout main
git merge feature/login

# 删除已合并的功能分支
git branch -d feature/login
```

---

## 六、合并与变基

```bash
# 合并指定分支到当前分支
git merge 分支名

# 合并后删除分支引用（保留提交历史）
git merge --no-ff 分支名

# 变基：将当前分支的提交"移动"到目标分支之上
git rebase 目标分支名

# 变基遇到冲突时中止
git rebase --abort

# 变基遇到冲突时继续（解决冲突后）
git rebase --continue
```

### merge 与 rebase 的区别

| 特性 | `merge` | `rebase` |
|------|---------|----------|
| 历史记录 | 保留分支结构，产生合并提交 | 线性历史，更整洁 |
| 是否改写历史 | 否 | 是 |
| 适用场景 | 公共分支（如 main） | 个人分支整理提交 |
| 冲突处理 | 一次性解决 | 逐个提交解决 |

---

## 七、远程仓库操作

```bash
# 查看远程仓库信息
git remote -v

# 添加远程仓库
git remote add origin https://github.com/用户名/仓库名.git

# 从远程拉取更新（不自动合并）
git fetch origin

# 从远程拉取并合并到当前分支
git pull origin 分支名

# 推送到远程
git push origin 分支名

# 首次推送并设置上游分支
git push -u origin 分支名

# 删除远程分支
git push origin --delete 分支名

# 强制推送（危险！会覆盖远程历史）
git push --force origin 分支名
```

### fetch vs pull

| 命令 | 作用 |
|------|------|
| `git fetch` | 只下载远程更新，**不修改**工作区 |
| `git pull` | 下载 + 自动合并，等于 `fetch` + `merge` |

---

## 八、撤销与回退

```bash
# 撤销工作区的修改（未 add 的文件）
git checkout -- 文件名

# 从暂存区移除文件（取消 add，保留修改）
git reset HEAD 文件名

# 撤销最近一次提交，保留修改在暂存区
git reset --soft HEAD~1

# 撤销最近一次提交，保留修改在工作区
git reset --mixed HEAD~1

# 彻底回退到某次提交（丢弃所有修改，慎用！）
git reset --hard 提交哈希

# 创建一个新的提交来"撤销"某次提交（安全，不改历史）
git revert 提交哈希
```

### reset 三种模式对比

| 模式 | 工作区 | 暂存区 | 提交历史 |
|------|--------|--------|----------|
| `--soft` | 保留 | 保留 | 回退 |
| `--mixed` | 保留 | 清除 | 回退 |
| `--hard` | **清除** | **清除** | 回退 |

---

## 九、暂存工作区（Stash）

临时保存当前修改，切换到其他分支处理紧急事务。

```bash
# 保存当前工作区
git stash

# 保存并添加描述
git stash save "正在开发登录功能"

# 查看所有暂存记录
git stash list

# 恢复最近一次暂存（保留记录）
git stash apply

# 恢复最近一次暂存（并删除记录）
git stash pop

# 恢复指定暂存
git stash apply stash@{2}

# 删除指定暂存
git stash drop stash@{0}

# 清空所有暂存
git stash clear
```

---

## 十、标签管理

用于标记发布版本（如 v1.0、v2.0）。

```bash
# 查看所有标签
git tag

# 创建轻量标签
git tag v1.0

# 创建附注标签（推荐，包含说明信息）
git tag -a v1.0 -m "第一个正式版本"

# 给指定提交打标签
git tag -a v1.0 提交哈希 -m "版本说明"

# 推送标签到远程
git push origin v1.0

# 推送所有标签
git push origin --tags

# 删除本地标签
git tag -d v1.0

# 删除远程标签
git push origin --delete v1.0
```

---

## 十一、解决冲突

当两个分支修改了同一文件的同一位置，合并时会产生冲突。

```bash
# 1. 合并时出现冲突
git merge feature/login
# 输出：CONFLICT (content): Merge conflict in 文件名

# 2. 查看冲突文件
git status

# 3. 手动编辑冲突文件，冲突标记如下：
# <<<<<<< HEAD
# 当前分支的内容
# =======
# 合并分支的内容
# >>>>>>> feature/login

# 4. 删除冲突标记，保留正确的代码

# 5. 标记冲突已解决
git add 文件名

# 6. 完成合并提交
git commit -m "合并 feature/login，解决冲突"
```

---

## 十二、.gitignore 文件

在项目根目录创建 `.gitignore` 文件，指定 Git 应忽略的文件。

```bash
# 常见的 .gitignore 内容

# Python
__pycache__/
*.pyc
*.pyo
.venv/
venv/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp

# 系统文件
.DS_Store
Thumbs.db

# 日志
*.log

# 环境变量
.env
```

---

## 十三、常用场景速查

| 场景 | 命令 |
|------|------|
| 我改了文件，想撤销 | `git checkout -- 文件名` |
| 我 add 了，想撤销 | `git reset HEAD 文件名` |
| 我 commit 了，想修改信息 | `git commit --amend -m "新信息"` |
| 我想查看改了什么 | `git diff` 或 `git diff --staged` |
| 我想切换分支但有未提交修改 | `git stash` → 切换 → `git stash pop` |
| 我想同步远程最新代码 | `git pull origin 分支名` |
| 我想创建功能分支 | `git checkout -b feature/xxx` |
| 我想回退到某个版本 | `git reset --hard 提交哈希` |
| 我想安全地撤销某次提交 | `git revert 提交哈希` |

---

## 十四、救命命令

```bash
# 我不小心删了文件，想恢复
git checkout -- 文件名

# 我搞乱了，想回到上次提交的状态
git reset --hard HEAD

# 我 reset --hard 了，后悔了（在一定时间内）
git reflog            # 找到误操作前的提交哈希
git reset --hard 哈希  # 恢复

# 我想查看谁在什么时候改了这行代码
git blame 文件名

# 我想搜索代码中的关键字
git log -S "搜索内容" --oneline
```

---

## 十五、命令关系图

```
                    ┌─────────┐
                    │ git init │
                    └────┬────┘
                         │
                         ▼
┌──────────┐    add    ┌──────────┐   commit   ┌──────────┐
│  工作区   │─────────▶│  暂存区   │──────────▶│ 本地仓库  │
│Working Dir│         │ Staging   │           │  Local   │
└──────────┘         └──────────┘           └────┬─────┘
     ▲                                           │
     │              checkout/reset               │ push/pull
     └───────────────────────────────────────────┘
                                                 │
                                                 ▼
                                          ┌──────────┐
                                          │ 远程仓库  │
                                          │  Remote  │
                                          └──────────┘
```

---

> **提示**：Git 的学习曲线较陡，建议从日常流程（add → commit → push）开始，逐步掌握分支和合并。
> 遇到问题时，`git status` 是你最好的朋友，它会告诉你当前的状态和下一步该做什么。
