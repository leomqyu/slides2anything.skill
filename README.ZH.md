<div align="center">

# slides2anything.skill

[English](README.md) | 中文

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-blueviolet.svg)](https://openai.com)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

> *"把零碎课件，直接变成能拿来复习、记笔记、备考的最终文件。"*

<br>

还在对着一份满是关键词、公式和提纲的 PPT 发愁？<br>
还在把 PDF 讲义里的碎片内容手动整理成教材语言？<br>
还在重复补写过渡句、定义、例子、小结和习题？<br>

**slides2anything** 是一个把 `.ppt`、`.pptx`、`.pdf` 内容整理成高价值学习材料的 skill，输出形态包括符合真实使用场景的速查表、笔记和教材。  
它不只是提取文字，更重要的是让 Agent 先补问信息、读取原文，再用自己的 LLM 能力把内容写成可直接使用的最终文件，更适合大学生考试突击、平时记笔记、期末复习和课堂教学。

<br>

支持输入课件和 PDF 文档<br>
支持输出 **速查表 / 讲义 / 教材**，格式可为 **Markdown / Word DOCX / LaTeX**<br>
支持让 Agent 先询问路径、格式和模式，再开始生成

[它和普通提取工具有什么不一样](#它和普通提取工具有什么不一样) · [环境要求](#环境要求) · [工作方式](#工作方式) · [自然语言示例](#自然语言示例) · [注意事项](#注意事项)

</div>

---

## 它和普通提取工具有什么不一样

| 普通做法 | slides2anything |
|------|------|
| 只负责提取文字，最后给你一堆碎片 | 先提取，再帮助 Agent 把碎片内容写成可以直接使用的最终学习文件 |
| 默认你第一次提问就把所有参数说全 | Agent 会主动追问路径、格式、模式和结构要求 |
| 把 PPT 和 PDF 当成普通文本文件处理 | 把它们当成有教学结构的课程材料来理解 |
| 容易生成扁平笔记或僵硬模板 | 借助模型写出更贴近真实使用场景的速查表、复习笔记、教师讲义、公式总结和完整教材内容 |
| 只是导出一个文件 | 更强调生成一个可直接拿去学习、复习、备考和整理笔记的最终文件 |

一句话说，这个项目的重点是 **面向教学与考试的改写**，尤其适合 **大学生考试突击和高效整理笔记**，而不只是文本提取。

## 环境要求

建议环境中具备这些工具：

- Python 3，用于提取源文件内容
- LibreOffice，如果你需要处理老式 `.ppt`
- Pandoc，如果你希望最终导出 `.docx`
- 可选的 `pdftotext`，如果有它，PDF 提取通常会更稳

如果你只处理 `.pptx`，可以不安装 LibreOffice。
如果你只输出 Markdown 或 LaTeX，可以不安装 Pandoc。

## 项目结构

- `SKILL.md`：skill 主说明
- `scripts/extract_ppt.py`：PPT 提取脚本
- `scripts/extract_document.py`：统一提取 PPT 和 PDF 内容
- `references/transformation-rubric.md`：教材改写规则
- `agents/openai.yaml`：skill 元数据

## 工作方式

推荐流程是：

1. 使用者用自然语言提出需求。
2. 如果信息不够，Agent 主动追问。
3. 提取脚本读取 PPT 或 PDF。
4. Agent 以提取结果为依据。
5. Agent 使用自己的 LLM 写作能力生成速查表、讲义或教材正文等最终输出。
6. 最终保存为 Markdown、LaTeX，或导出为 DOCX。

这里有一个重要原则：真正的输出内容应该由 Agent 来写，而不是由僵硬的模板脚本直接拼接出来。

如果输出模式是速查表，Agent 还应主动询问大概要压缩到多少页，并通过更紧密的结构、措辞和排版设计，尽量把内容控制在目标页数内。

一个更贴近真实使用场景的例子是：

- Agent 会问：`如果这是速查表，你希望大概控制在几页？`
- 用户回答：`2 页。`
- 预期行为：Agent 接下来应优先采用更紧凑的表格、更短的 bullet、更少的过渡句和更高密度的公式呈现方式，使最终文件尽量能压缩进 2 页。

## 自然语言示例

使用者不需要写命令，直接说自然语言即可。

例如：

- 请使用 `slides2anything` 帮我把 PPT 转成考试速查表。
- 请使用 `slides2anything` 把我的课件直接整理成期末考试速查表。
- 请使用 `slides2anything` 把我的课件整理成 2 页速查表；如果我没说页数，你先主动问我希望控制在几页。
- 请使用 `slides2anything` 把我的 PDF 讲义整理成适合大学生临考复习的笔记。
- 请使用 `slides2anything` 处理我的 PDF 讲义，并先问我缺哪些信息。
- 我想把一个课件转成教师讲义，请使用 `slides2anything`，但开始前先问我希望保留哪些结构。
- 请使用 `slides2anything` 把我的课件转成 DOCX 或者 LaTeX 教材文件，一步步问我需要确认的选项。

正常情况下，Agent 应该继续追问：

- PPT 或 PDF 的路径
- 希望保存到哪里
- 输出为 Markdown、DOCX 还是 LaTeX
- 想要速查表、教师讲义、教材正文还是学生讲义
- 如果是速查表，大概希望控制在多少页
- 是否需要学习目标、术语表、小结和练习题

例如，在速查表场景里，一个合适的补充追问就是：

- `如果这是速查表，你希望大概控制在几页？`

## 注意事项

- 对 `.ppt` 输入，提取器会尝试调用 `libreoffice` 或 `soffice` 进行转换。
- 对 `.pdf` 输入，提取器优先使用系统里的 PDF 文本工具，没有时会使用内置兜底方案。
- 对 `.docx` 输出，`pandoc` 只负责最后的导出；正文内容仍由 Agent 自己生成。
- 如果原始材料里有公式、符号或换算过程，Agent 应直接写进最终内容，而不是写成“课件里给出了……”“PPT 中展示了……”。
