# 我的个人网站

一个纯静态的个人主页，直接用 HTML + CSS + JavaScript 写成，不需要任何后端或构建工具。

## 文件结构

| 文件 | 作用 |
| --- | --- |
| `index.html` | 页面结构：导航栏、个人简介、项目展示、联系方式、页脚 |
| `style.css` | 样式：柔和配色、响应式布局、卡片与弹窗外观 |
| `script.js` | 交互：滚动时高亮导航、欢迎弹窗、移动端菜单、年份自动更新 |

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

推送后 GitHub Pages 会自动重新发布，大约 1 分钟后线上就会更新。

只改文字内容的话，也可以直接在 GitHub 网页上打开对应文件，点铅笔图标编辑，然后 `Commit changes`，效果一样。

## 四、把模板换成你自己的内容

在 `index.html` 里搜索并替换这些占位内容：

- `你的名字` —— 换成你的名字
- `<div class="avatar">` 里的 👤 —— 换成你的照片（可改成 `<img src="avatar.jpg" alt="头像">`）
- 三段项目卡片 —— 换成你真实的项目名称和介绍
- `yourname@example.com`、GitHub 链接、微信/微博 —— 换成你的联系方式

## 五、关于国内访问

- `博客园` 是博客平台，写文章很方便，但不能直接托管这个自定义页面；它更像是内容社区。
- GitHub Pages 在国内部分网络下速度一般，偶尔不稳定。
- 如果主要给国内的朋友看，可以考虑：Gitee Pages（需实名认证）、腾讯云 CloudBase 静态托管、阿里云 OSS 静态网站托管。
- 想用自己的域名（比如 `myname.com`），上面这些平台都支持绑定，但要先买域名；用国内服务器/CDN 通常还需要 ICP 备案。

## 六、GitHub 常用操作速查

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

---

© 2026 你的名字
