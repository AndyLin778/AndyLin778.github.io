# 我的个人网站

一个纯静态的个人主页，直接用 HTML + CSS + JavaScript 写成，不需要任何后端或构建工具。

## 文件结构

| 文件 | 作用 |
| --- | --- |
| `index.html` | 主页：导航栏、首屏大字、项目 / 文章 / 科研 / 游戏 四个栏目、页脚联系方式 |
| `posts/` | 文章页目录：一篇文章一个 HTML 文件，正文排版统一 |
| `assets/css/style.css` | 样式：中性配色 + 单一强调色、大字号排版、响应式布局、滚动揭示、正文排版 |
| `assets/js/script.js` | 交互：首屏大字轮换、打字机副标题、本地时钟、导航高亮、移动端菜单、欢迎弹窗 |
| `assets/katex/` | 数学公式排版引擎（本地内置，不联网也能渲染） |
| `tools/md2html.py` | 把 Markdown 文章转换成文章页正文的小脚本 |
| `tools/upload.py` | 一键上传到 GitHub：add + commit + push，失败时给出对策 |
| `games/` | 游戏目录页与游戏笔记页（`index.html` 是目录，`_template.html` 是新页面模板） |
| `assets/js/games.js` | 游戏列表数据，加游戏只改这一个文件 |

## 一、本地预览

最简单的方式是直接在文件资源管理器里双击 `index.html`，会用默认浏览器打开。

如果想更接近真实网站的运行方式，在本文件夹打开终端后运行：

```
python -m http.server 8000
```

然后浏览器访问 `http://localhost:8000`。按 `Ctrl + C` 可以停止服务。

## 二、发布到 GitHub Pages（让别人也能访问）

GitHub Pages 可以免费托管这种静态网站。首次发布分三步：

**第 1 步：在 GitHub 网站上新建仓库**

登录 GitHub，点击右上角的 `+` → `New repository`。
仓库名建议填 `你的用户名.github.io`（例如用户名是 `andy`，就填 `andy.github.io`），
可见性选择 `Public`，然后点击 `Create repository`。

**第 2 步：把本地代码推送上去**

在 `D:\mypage` 打开终端（PowerShell），依次运行下面命令，把 `你的用户名` 换成真实的 GitHub 用户名：

```
git remote add origin https://github.com/你的用户名/你的用户名.github.io.git
git push -u origin main
```

第一次推送时 Git 会要求登录 GitHub，按提示在浏览器里完成授权即可。

**第 3 步：开启 Pages 功能**

进入仓库页面 → `Settings` → 左侧 `Pages` →
`Source` 选择 `Deploy from a branch`，分支选 `main`，目录保持 `/ (root)`，点击 `Save`。

等 1～2 分钟，访问 `https://你的用户名.github.io` 就能看到你的网站了，
把链接发给任何人，他们都能打开。

## 三、以后怎么更新网站

改完文件后，在本文件夹执行：

```
git add .
git commit -m "更新说明"
git push
```

更省事的做法是用项目自带的脚本，它会自己找到 git，把上面三步一次做完：

```
python D:\mypage\tools\upload.py "更新说明"
```

推送后 GitHub Pages 会自动重新发布，大约 1 分钟后线上就会更新。

只改文字内容的话，也可以直接在 GitHub 网页上打开对应文件，点铅笔图标编辑，然后 `Commit changes`，效果一样。

## 四、把模板换成你自己的内容

主页分成四个栏目：

- `01 / WORK` 项目 —— 下面分「工具 / 游戏 / 算法」三栏
- `02 / WRITING` 文章 —— 下面分「杂谈 / 诗歌 / 小说」三栏
- `03 / RESEARCH` 科研
- `04 / GAMES` 游戏（之后从 Steam 导入）

要往某一栏里加内容，就照着现成的结构复制一行：

```html
<li>
  <a class="entry" href="链接地址">
    <span class="entry-title">标题</span>
    <span class="entry-date mono">2026.09.16</span>
  </a>
</li>
```

某一栏暂时没有内容时，保留 `<p class="cat-empty mono">待添加</p>` 即可。

还没替换的占位内容：

- 站名与页脚署名已经填成 `Andy.Z`，想换成别的名字，全局替换 `Andy.Z` 即可

## 五、新增一篇文章

1. 把文章写成 Markdown（`#` 标题、`**粗体**`、表格、代码块、`$$ 公式 $$` 都支持）。
2. 运行下面这条命令，正文会自动填进文章页：

```
python tools/md2html.py 你的文章.md posts/2026-09-16-long-text-render-test.html
```

3. 脚本只替换目标页面里 `<!-- ARTICLE:START -->` 和 `<!-- ARTICLE:END -->` 之间的内容，
   导航、页脚和公式渲染都不受影响。
4. 最后在主页「02 / WRITING」里对应的栏目加一行链接指向这个文件。

## 六、给游戏加笔记

游戏目录在 `games/index.html`，卡片由 `assets/js/games.js` 里的数组生成。

**加一个游戏**：打开 `assets/js/games.js`，照抄一行改成你的内容：

```js
{ title: "游戏名", subtitle: "English Name", tag: "类型", page: "", cover: "" }
```

`page` 留空时卡片显示「待写」；写好笔记页后把文件名填进去
（例如 `"dyson-sphere-program.html"`），卡片就会变成可点击的。

**给一个游戏写笔记**：

1. 复制 `games/_template.html`，改名成英文短名，例如 `games/dyson-sphere-program.html`。
2. 把标题和正文换成你的内容。
3. 图片和视频放进 `games/media/`，页面里用 `media/xxx.jpg` 这样的相对路径引用。
4. 回到 `assets/js/games.js`，把该游戏的 `page` 填上文件名。

模板里已经备好封面图、图集和视频位：

- 图集用 `<div class="gallery">` 包住若干 `<figure>`
- 自己录的视频：`<div class="media-video"><video controls src="media/clip.mp4"></video></div>`
- B 站 / YouTube：把 `<iframe>` 放进 `<div class="media-video">`，模板注释里有现成写法
- 视频建议压到 1080p 以内再传，单个文件不要超过 100 MB

## 七、关于国内访问

- `博客园` 是博客平台，写文章很方便，但不能直接托管这个自定义页面；它更像是内容社区。
- GitHub Pages 在国内部分网络下速度一般，偶尔不稳定。
- 如果主要给国内的朋友看，可以考虑：Gitee Pages（需实名认证）、腾讯云 CloudBase 静态托管、阿里云 OSS 静态网站托管。
- 想用自己的域名（比如 `myname.com`），上面这些平台都支持绑定，但要先买域名；用国内服务器/CDN 通常还需要 ICP 备案。

## 八、GitHub 常用操作速查

> 💡 提示：如果终端提示 `无法将“git”项识别为 cmdlet…`，说明这台电脑还没装 Git，
> 或者安装时没勾选「加入 PATH」。到 <https://git-scm.com/download/win> 下载安装，
> 安装向导里保持默认、确保选中 `Git from the command line and also from 3rd-party software`，
> 装完**关掉并重新打开 VS Code 终端**，再执行下面的命令。

```
git status            查看当前改动状态
git add .             把改动加入暂存区
git commit -m "说明"   把改动保存为一次提交
git push              推送到 GitHub
git pull              拉取 GitHub 上的最新改动
git log --oneline     查看提交历史
```

常用概念：

- **仓库（Repository）**：一个项目的文件夹，包含代码和全部历史记录。
- **提交（Commit）**：一次保存点，记录你改了什么。
- **分支（Branch）**：并行的开发线，主分支一般叫 `main`。
- **远程（Remote）**：GitHub 上的那份仓库，用 `origin` 表示。

## 九、VS Code 工作区配置

本项目已经配好一套 VS Code 设置，换电脑或重新打开时直接生效，不用再手动调。

| 文件 | 作用 |
| --- | --- |
| `mypage.code-workspace` | 工作区文件：双击它就能以工作区方式打开本项目 |
| `.vscode/settings.json` | 编辑器设置：2 空格缩进、UTF-8、保存时去掉行尾空格并自动格式化、隐藏 `.git` 噪音 |
| `.vscode/launch.json` | 调试配置：按 `F5` 用 Chrome 打开页面（可预览本机服务或直接打开文件） |
| `.vscode/tasks.json` | 任务配置：按 `Ctrl + Shift + B` 一键启动 `python -m http.server 8000` |
| `.vscode/extensions.json` | 推荐扩展：打开项目时 VS Code 会提示安装 Live Server、Prettier 等（可选） |
| `.gitignore` | 让系统临时文件和本地配置文件不被提交到 GitHub |

日常最常用的两个快捷键：

- `Ctrl + Shift + B` —— 启动本地预览（等价于手动运行 `python -m http.server 8000`），
  之后在浏览器打开 `http://localhost:8000`；在终端按 `Ctrl + C` 停止。
- `F5` —— 用 Chrome 打开页面进行调试。默认配置是「直接打开 `index.html`」，不依赖服务器；
  如果想在真实服务环境下调试，先按 `Ctrl + Shift + B` 启动预览，再在调试下拉框里选「② 本机服务」。

> 说明：本地预览任务依赖电脑上已安装 Python（本机为 `D:\python\python.exe`）。
> 如果提示找不到 `python`，把 `python` 换成完整路径，或用第一节里说的双击 `index.html` 的方式预览。

## 十、视觉与动效说明（参考 ansyn.me 归纳）

这一版的视觉参考了 <https://ansyn.me/> 的做法：**颜色极少、字号极大、用等宽小字和线条做细节**。

### 1. 配色：中性色 + 一个强调色

所有颜色都定义在 `assets/css/style.css` 顶部的 `:root` 里，改这几个变量就能整站换色：

| 变量 | 值 | 用途 |
| --- | --- | --- |
| `--paper` | `#fdfdfd` | 页面底色（近白） |
| `--ink` | `#0f0f0f` | 正文与大字（近黑） |
| `--muted` | `#666666` | 次要说明文字 |
| `--line` | `#c9c9c9` | 所有 1px 分隔线 |
| `--accent` | `#356bff` | 唯一的强调色：箭头 hover、导航下划线、打字光标、选区内 |

原则是：**除了 hover 状态的蓝色，页面上不再有第二个彩色**，靠黑白对比和大字号来抓眼球。

### 2. 首屏大字

参考 ansyn.me 的「大字号 + 克制配色」，但实现刻意保持简单：**没有 canvas，纯 HTML + CSS + 十几行 JS**。

- 文字肌理：给文字设 `background-clip: text`，背景用 1 像素的细条纹渐变，
  大字看起来就有「印刷/屏幕质感」，不额外加载图片或字体；
- 动态：大字逐字打出 → 停留 1.6 秒 → 逐字退格 → 换下一个词；
- **播完一轮就停住**：4 个词轮流打完后，会稳稳打出第一句 `MY PAGE` 并停下，
  打字光标淡出，不再无限循环（`makeTyper()` 的第 4 个参数就是轮数，传 `1` 表示播 1 轮）。

想改内容只动 `assets/js/script.js` 顶部的两行：

```js
const HERO_WORDS = ["MY PAGE", "HELLO", "2026", "WEB DEV"]; // 首屏依次打出的大字
const TYPED_LINES = ["把想法变成看得见的东西。", "持续学习，保持好奇。", "这里记录我的实验与作品。"];
```

### 3. 其他动效

- **打字机副标题**：和首屏大字共用同一个 `makeTyper()` 函数（参数不同而已），
  同样也是播完一轮就停住；想加第三处打字效果，照着写一行 `makeTyper(...)` 即可。
- **扫描线**：首屏顶部往下扫过一条很淡的蓝色光带（9 秒一轮，对应 ansyn 的 `display-scan`），纯 CSS 动画。
- **滚动揭示**：标题、段落、项目行进入视口时用 `clip-path` 从左往右「刷」出来（对应 ansyn 的 `strip-in`），
  依次有 0.08 秒的错峰。判断「有没有进入视口」用的是滚动事件 + `getBoundingClientRect()`，
  **故意没有用 IntersectionObserver**：被 `clip-path` 裁切的元素可见面积为零，IO 会一直认为它没进视口，
  结果就是下方内容永远不显示。
- **本地时钟**：导航栏、首屏、页脚三处显示本机时间，时区按系统自动计算。

### 4. 无障碍

- 系统开启「减少动效」（`prefers-reduced-motion: reduce`）时：大字和副标题直接显示第一句、
  扫描线隐藏、揭示动画取消（内容直接可见）。
- 首页的大标题在 `index.html` 里用 `.sr-only` 保留了一份真实文本，方便搜索引擎和读屏软件读取。

---

© 2026 Andy.Z
