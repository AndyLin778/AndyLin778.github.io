# 网站变更记录

按时间倒序。每条记：改了什么文件、为什么、还剩什么待办。

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