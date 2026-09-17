# 网站变更记录

按时间倒序。每条记：改了什么文件、为什么、还剩什么待办。

---

## 2026-09-18 · 新增「失去 AI 之后」长期项目（项目栏新增「成长」分类）

**背景**：把「失去 AI 后的人工接管备忘录」和「以自己为主导的学习与工作计划」两份文档放到网站上。
确定为**项目**而不是文章：它会有持续的状态和记录，之后形成的感想再单独写成文章放进文章栏。

**改动的文件**

| 文件 | 改动 |
| --- | --- |
| `projects/no-ai.html` | 新页面：项目主页（说明、两条线、两份文档入口、实践记录区、文章出口、维护说明） |
| `projects/no-ai-memo.html` | 新页面：备忘录全文，正文由 Markdown 生成 |
| `projects/no-ai-plan.html` | 新页面：计划全文，正文由 Markdown 生成 |
| `projects/no-ai-memo.md` | 备忘录源稿（从桌面 `关于未来，执行，套利和理想` 文件夹复制） |
| `projects/no-ai-plan.md` | 计划源稿（同上） |
| `index.html` | 「01 / WORK」新增第四栏「成长」，计数 `01`，指向 `projects/no-ai.html` |
| `tools/md2html.py` | 新增 `[文字](链接)` 行内链接支持；新增 `--skip-h1` 参数 |
| `assets/css/style.css` | 追加项目页样式：`.proj-cards / .proj-card / .proj-log / .proj-log-item / .proj-legend` |
| `README.md` | 新增「十一、项目页（projects/）」，说明加记录、改正文与重新生成的命令 |

**为什么这样放**

- 项目页放「正在发生的事」和记录，文章放「想清楚的一个观点」；项目页持续更新，文章是某个时点的定稿。
- 两份文档各有独立页面，项目主页只做导航和记录，避免一个页面越滚越长。
- 网站里的 `projects/no-ai-*.md` 是发布用的快照，桌面上那两份仍是可继续修改的工作稿。

**待办**

- [ ] 运行 `python D:\mypage\tools\upload.py "新增「失去 AI 之后」项目"` 推送到 GitHub Pages。
- [ ] 写第一条实践记录：选一个小程序独立运行并改一个功能，或独立读完一节教材/一篇论文。

---

## 2026-09-17 · 新增「大学生自己的国产 Codex」项目与相关文章

**背景**：把自己的双 Agent 环境（ChatGPT Desktop + DeepSeek）整理成开源项目发布到 GitHub，网站上同步露出。

**改动的文件**

| 文件 | 改动 |
| --- | --- |
| `index.html` | 「01 / WORK → 工具」栏：`00 → 01`，新增条目「大学生自己的国产 Codex」，链接到 GitHub |
| `index.html` | 「02 / WRITING → 杂谈」栏：`01 → 02`，新增条目「从 AI 使用者到 AI 系统构建者」 |
| `posts/2026-09-17-domestic-codex.html` | 新文章页，骨架从 `posts/2026-09-17-qingsuan.html` 复制后改的头部 |
| `posts/2026-09-17-domestic-codex.md` | 文章源稿。改文字只改这个文件，再重新生成 |
| `tools/md2html.py` | 补上列表支持（新增分支，已有行为未改动） |
| `assets/css/style.css` | **未改动**（`.prose ul / ol / li` 的规则原本就存在） |

**关联的外部仓库**：https://github.com/AndyLin778/domestic-codex

**待办**

- [ ] 运行 `python tools/upload.py "新增国产 Codex 项目与项目故事"` 推送到 GitHub Pages。
      这次修改是在一个连不上外网的会话里做的（`github.com:443` 超时），push 需要在你本机正常代理环境下完成。

**怎么改这篇文章**

1. 改 `posts/2026-09-17-domestic-codex.md`；
2. 运行 `python tools/md2html.py posts/2026-09-17-domestic-codex.md posts/2026-09-17-domestic-codex.html`。

脚本只替换 `<!-- ARTICLE:START -->` 和 `<!-- ARTICLE:END -->` 之间的正文，页面头部的标题与页脚不会被覆盖。

**关于 md2html.py 的列表支持**

原脚本支持标题 / 段落 / 粗体 / 斜体 / 行内代码 / 代码块 / 表格 / 引用 / 分隔线 / 公式，**不支持列表**，
所以 `- 条目` 会被当作带「- 」的普通段落。现在补上了无序列表（`-` `*` `+`）和有序列表（`1.` `1)`），
缩进的续行会接到上一条。因为 `style.css` 里 `.prose ul / ol / li` 的样式原本就有，所以没有改样式文件。

**回滚**

改动前的文件备份在 `C:\Users\Andy\Codex-Chat-Archive\_mypage-backup\`：
`index.html.bak`、`post-template.bak.html`、`md2html.py.bak`。