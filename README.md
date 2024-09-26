
---

# Agent_lite 说明文档

## 概述

该 agent 能够执行多种任务，如与文件进行交互、搜索信息以及生成响应。它设计灵活，可以根据不同的查询执行相应的操作，并实时反思其行为。该 agent 包含一系列可以调用的工具来执行特定任务。
整体逻辑链为：
用户输入 -> 信息提取 -> 生成提示 -> 模型调用 -> 响应解析 -> 决策制定 -> 执行工具 -> 更新状态 -> 反馈与循环

## 功能

- **语言模型交互**：使用 DashScope 的 API，根据提示和用户交互生成响应。
- **文件操作工具**：可以读取、写入和追加内容到文件中，作为处理逻辑的一部分。
- **互联网搜索**：在必要时，agent 可以搜索互联网以获取更多信息。
- **反思与批评**：agent 会对其操作进行批判性反思，以提高效率和性能。

## 环境要求

- Python 3.12

## 安装

提示：记得创建 `.env` 文件来设置环境变量：
   ```
   DASHSCOPE_API_KEY=<your_dashscope_api_key>
   ```

## 使用方法

1. **运行 Agent**：
   你可以通过运行 `main.py` 来启动 agent。agent 会提示你输入目标或查询：
   ```bash
   python main.py
   ```
   - 输入你的目标/查询，agent 将根据提供的工具和模型开始处理。

2. **Agent 执行流程**：
用户输入 -> 信息提取 -> 生成提示 -> 模型调用 -> 响应解析 -> 决策制定 -> 执行工具 -> 更新状态 -> 反馈与循环

3. **支持的工具**：
   agent 可以执行以下操作：
   - `read_file`：从指定目录读取文件。
   - `write_file`：将内容写入文件。
   - `append_to_file`：向现有文件追加内容。
   - `search`：使用外部搜索引擎搜索信息。




---
