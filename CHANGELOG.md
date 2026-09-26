# 网站变更记录

按时间倒序。每条记：改了什么文件、为什么、还剩什么待办。

---

## 2026-09-26 · 桌宠项目改名：蓝蓝 → deepseek鲸鱼娘

**状态**：本地已改，**尚未上传**。

**改动的文件**

| 文件 | 改动 |
| --- | --- |
| `index.html` | 「设计」分类里的条目名改成 `deepseek鲸鱼娘：双形态桌宠` |
| `projects/lanlan-pet.html` | 页面 `<title>`、`<h1>`、meta description，以及两张预览图的 `aria-label` / `alt` 里的「蓝蓝」改成「鲸鱼娘」 |

文件名保持原样：`projects/lanlan-pet.html` 与两个 ZIP 都还叫 `lanlan-*`。改文件名会让已发布的链接失效，等确实要动的时候再说。

**桌宠仓库（`D:\game\deepseek-pet`）同步改名**——形象是 DeepSeek 鲸鱼的二创，仓库里也必须写清楚

| 文件 | 改动 |
| --- | --- |
| `dual-form-pet/pet.py` | 窗口标题改成 `deepseek鲸鱼娘 · 双形态桌宠` |
| `dual-form-pet/README.md` | 标题改成 `# deepseek鲸鱼娘：双形态像素桌宠` |
| `lanlan-codex/normal/pet.json`、`lanlan-codex/pot/pet.json` | `displayName` 改成 `deepseek鲸鱼娘 · 普通` / `deepseek鲸鱼娘 · 铁锅` |
| `lanlan-codex/build.py` | 重新生成图集时写进 `pet.json` 的 `displayName` 同步改掉，避免下次生成又变回旧名 |
| `USAGE.md` | 「在宠物列表选择…」那句同步改掉 |
| `README.md` | 标题改成 `deepseek鲸鱼娘：双形态桌宠（Codex 版和桌面版）`，正文补一句「角色形象是 DeepSeek 鲸鱼形象的二次创作」 |
| `ASSETS.md` | 开头增加一段：形象是 DeepSeek 鲸鱼形象的二次创作、非官方，形象相关权利归 DeepSeek |

**重新打包的两个下载包**（结构不变，只是里面的文件更新）

| 包 | 大小变化 |
| --- | --- |
| `projects/downloads/lanlan-desktop-pet.zip` | 46365 → 46383 字节 |
| `projects/downloads/lanlan-codex.zip` | 32341 → 32371 字节 |

**待办**

- [ ] 桌宠仓库和网站都还没上传，发布时两边要一起走。
- [ ] `pet.json` 里的 `id` 仍是 `lanlan-normal` / `lanlan-pot`，宠物目录也还叫 `lanlan-*`；id 一改，已经装过的人要重装，所以先不动。

---

## 2026-09-26 · 首屏大字换成 MY PAGE / HELLO / STAY CURIOUS / KEEP EXPLORING

**状态**：本地已改，**尚未上传**。

**改动的文件**

| 文件 | 改动 |
| --- | --- |
| `assets/js/script.js` | `HERO_WORDS` 换成 `MY PAGE` / `HELLO` / `STAY CURIOUS` / `KEEP EXPLORING`（播完一圈后自动回头打 `MY PAGE` 停住）；新增 `fitHeroWord()` 长句自动缩放；`makeTyper()` 增加第 5 个参数 `onDraw` |

**为什么顺手加了自动缩放**：`KEEP EXPLORING` 整句宽 6.99em，而容器在宽屏下的容量是 6.86em——
1440 宽以上字号被 clamp 到上限 172px 时整句 1202px，超出容器 1180px，会被 `.hero` 的 `overflow: hidden` 裁掉右侧；
414 宽的手机上同样超出约 14px。加了缩放后任何长短的句子都能放进来，以后换词不用再算宽度。

**怎么验证的**（无头 Chrome + 临时探针，1440 / 1920 / 1280 / 414 四种宽度）

- 溢出帧数 0；`KEEP EXPLORING` 自动缩到 163.79px（宽屏）、56.91px（414 宽），其余句子保持基准字号。
- 大字块高度、首屏高度、`#work` 位置全程恒定（1440 下分别是 172.0 / 446.4 / 510），没有跳动。
- 收尾停在 `MY PAGE`。探针文件已删除。

**待办**

- [ ] 副标题那三句（`TYPED_LINES`）还没动。
- [ ] 文章摘要、分享预览图（OG 图）等细节还没处理。

---

## 2026-09-26 · 首屏：修掉大字消失时的跳动，移除欢迎弹窗

**状态**：本地已改，**尚未上传**。

**两个问题**

1. 刚进首页时下方栏目会往上跳一下。原因是 `.hero-word` 是 flex 容器，大字 span 被删空时高度变成 0，
   容器只剩 0.68em 高的光标撑着，整块矮了 0.32em；1280 宽下字号约 158px，跳动量正好约 50px。
2. 欢迎弹窗在访问约 5 秒后弹出，容易撞上访客刚开始阅读的时机，按建议直接移除。

**改动的文件**

| 文件 | 改动 |
| --- | --- |
| `assets/css/style.css` | `.hero-word` 加 `min-height: 1em` 钉住行高；删除弹窗相关样式（`.welcome-modal`、`.modal-*`、`@keyframes modal-in`） |
| `assets/js/script.js` | 删除欢迎弹窗的开合逻辑，脚本头部说明同步更新 |
| `index.html` | 删除弹窗 DOM |

**怎么验证的**

- 用临时探针页 + 无头 Chrome 记录前 12 秒内的几何值：`#work.offsetTop` 修复前 `446 ↔ 496`（跳 50px），修复后恒为 `496`；
  大字行高修复前 `157.8 ↔ 107.3`，修复后恒为 `157.8`。探针文件已删除。
- 9 秒时截图确认页面无任何遮挡，`assets/js/script.js` 通过 `node --check` 语法检查。

**待办**

- [x] 首屏大字文案已定（见上一条）；副标题的文案仍待定。
- [ ] 文章摘要、分享预览图（OG 图）等细节还没处理。

---

## 2026-09-26 · 栏目调整：「游戏」改名「设计」，「成长」移入文章栏

**状态**：本地已改，**尚未上传**——等最近这批改动都做完再一起发布。

**背景**：`01 / WORK` 下的「游戏」分类只放了蓝蓝桌宠，和顶部 `04 / GAMES`（真·游戏目录）重名，也不贴切；
「成长」写的是自己的反思和规划，本质是文章，不是做出来的东西。

**改动的文件**

| 文件 | 改动 |
| --- | --- |
| `index.html` | `01 / WORK` 第二个分类「游戏」改名「设计」，桌宠条目与计数 `01` 不变 |
| `index.html` | 「成长」整块从 `01 / WORK` 移到 `02 / WRITING`，排在「杂谈」之后；条目、计数 `01`、两个子条目都不变 |

**之后按这个归类**

- 游戏相关：一律放 `04 / GAMES`，在 `assets/js/games.js` 里加一行卡片数据。
- 有设计成分的小项目：放 `01 / WORK → 设计`。
- 自己的反思与规划：放 `02 / WRITING → 成长`。
- 既不像设计也不像工具的小项目：先留在「设计」里，攒够几个再单独开一栏。

**待办**

- [ ] 这批改动还没上传，发布时 `index.html` 和 `CHANGELOG.md` 一起走。

---

## 2026-09-24 · 游戏栏新增《地球末日生存》，并发布它的游戏分析文章

**背景**：`D:\game` 里有一篇《文章_地球末日生存游戏分析.md》，想把它放进网站的游戏栏。
按网站原有的结构处理：先给游戏栏加一张卡片，再把文章作为这个游戏的笔记页发布。

**改动的文件**

| 文件 | 改动 |
| --- | --- |
| `assets/js/games.js` | 「未分类」组新增一行：`地球末日生存 / Last Day on Earth: Survival / 生存 · 收集`，`page` 指向 `last-day-on-earth.html`，卡片状态从「待写」变成「笔记 ↗」 |
| `games/last-day-on-earth.html` | 新页面：游戏笔记页，页头是游戏名，正文是那篇分析文章（含公式，沿用站点内置的 KaTeX） |
| `games/last-day-on-earth.md` | 文章源稿。从 `D:\game\文章_地球末日生存游戏分析.md` 转来，只做了两件事：公式块 `\[ \]` 改成 `$$ $$`、行尾统一成 LF |
| `games/media/covers/last-day-on-earth.jpg` | 新封面图：游戏里的基地截图，裁成 16:9（去掉底部菜单栏）后压成 1400×786、约 260 KB |
| `index.html` | 「04 / GAMES → 游戏目录」计数 `13 → 14` |

**为什么这样放**

- 卡片数据只改 `assets/js/games.js` 一个文件，和目录页的说明一致。
- 文章正文由 `tools/md2html.py` 生成，页面里保留 `<!-- ARTICLE:START -->` / `<!-- ARTICLE:END -->`，
  以后改文字只改 `.md` 再重新生成，页头和页脚不会被覆盖。
- 源稿里 `# 我重新玩了一遍十年前的那个游戏` 保留着：脚本会把源文件的 h1 降成页面 h2，
  于是「游戏名」在页头、文章标题在正文，两级标题不会打架。

**怎么改这篇文章**

1. 改 `games/last-day-on-earth.md`；
2. 运行 `python tools/md2html.py games/last-day-on-earth.md games/last-day-on-earth.html`。

**待办**

- [ ] 文章目前只在游戏栏里，还没有在「02 / WRITING」列一份；哪天觉得它更像一篇文章，再单独挑一栏放。

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
