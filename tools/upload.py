#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键把本地改动上传到 GitHub。

用法：
    python tools/upload.py                     # 提交说明自动用当前时间
    python tools/upload.py "改了首页文案"       # 自定义提交说明
    python tools/upload.py "首次对齐" --force   # 用本地覆盖远程（只在新旧历史对不上时用一次）

它依次做三件事：git add -A -> git commit -> git push，
失败时会根据报错给出具体的下一步。
"""

import datetime
import os
import shutil
import subprocess
import sys

BRANCH = "main"
REMOTE = "origin"
PAGES_URL = "https://AndyLin778.github.io"

# 控制台可能是 GBK 编码，遇到无法显示的字符时替换掉，而不是直接报错
try:
    sys.stdout.reconfigure(errors="replace")
except Exception:
    pass

# git 不一定在系统 PATH 里（Codex 自带的便携版就不在），所以按顺序找一遍
GIT_CANDIDATES = [
    r"C:\Program Files\Git\cmd\git.exe",
    r"C:\Program Files (x86)\Git\cmd\git.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Programs\Git\cmd\git.exe"),
    os.path.expandvars(r"%USERPROFILE%\scoop\shims\git.exe"),
    os.path.expandvars(
        r"%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime"
        r"\dependencies\native\git\cmd\git.exe"
    ),
]


def find_git():
    found = shutil.which("git")
    if found:
        return found
    for path in GIT_CANDIDATES:
        if path and os.path.isfile(path):
            return path
    return None


GIT = find_git()

# 仓库根目录 = 本脚本所在目录（tools/）的上一级。
# 所有 git 命令都带 -C，所以在哪个目录运行都不影响。
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 体积护栏：超过 WARN 就提醒，超过 ABORT 直接拦住
# （GitHub 单文件 100 MB 硬上限、50 MB 会警告，仓库建议控制在 1 GB 以内）
SIZE_WARN_MB = 5
SIZE_ABORT_MB = 50


def git(*args):
    return subprocess.run(
        [GIT, "-C", REPO_ROOT, *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def staged_large_files():
    """列出本次暂存里的大文件（已按从大到小排序）。"""
    listing = git("diff", "--cached", "--name-only", "--diff-filter=ACMR").stdout
    found = []
    for rel in listing.splitlines():
        rel = rel.strip()
        if not rel:
            continue
        path = os.path.join(REPO_ROOT, rel.replace("/", os.sep))
        if os.path.isfile(path):
            size = os.path.getsize(path)
            if size >= SIZE_WARN_MB * 1024 * 1024:
                found.append((rel, size))
    return sorted(found, key=lambda item: -item[1])


def main():
    argv = sys.argv[1:]
    force = "--force" in argv
    rest = [a for a in argv if a != "--force"]
    message = rest[0] if rest else "更新网站 " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # 0. 先确认找得到 git
    if not GIT:
        print("[X] 找不到 git。两种办法：")
        print("    1) 安装 Git for Windows：https://git-scm.com/download/win")
        print("       装完重新打开一个 PowerShell 窗口，再运行本脚本。")
        print("    2) 换成 GitHub Desktop 上传，它自带 git，不依赖 PATH。")
        return 1
    print("[..] 使用的 git：" + GIT)

    # 1. 确认当前在 Git 仓库里
    top = git("rev-parse", "--show-toplevel")
    if top.returncode != 0:
        print("[X] " + REPO_ROOT + " 不是一个 Git 仓库。")
        print("    请确认脚本在项目的 tools\\ 目录里。")
        return 1
    print("[..] 仓库目录：" + top.stdout.strip())

    # 2. 暂存所有改动
    add = git("add", "-A")
    if add.returncode != 0:
        print("[X] git add 失败：\n" + add.stderr.strip())
        return 1

    # 2.5 体积护栏
    big = staged_large_files()
    too_big = [item for item in big if item[1] >= SIZE_ABORT_MB * 1024 * 1024]
    if too_big:
        print("[X] 有文件超过 %d MB，先处理掉再传：" % SIZE_ABORT_MB)
        for rel, size in too_big:
            print("      %6.1f MB  %s" % (size / 1024 / 1024, rel))
        print("    图片先压缩（建议单张 300 KB 以内）；视频不要提交到仓库，")
        print("    改成 B 站 / YouTube 外链，或放到 GitHub Releases、对象存储。")
        return 1
    if big:
        print("[!] 这次提交里有偏大的文件（图片建议压到 300 KB 以内）：")
        for rel, size in big:
            print("      %6.1f MB  %s" % (size / 1024 / 1024, rel))

    # 3. 有改动就提交
    if git("status", "--porcelain").stdout.strip():
        commit = git("commit", "-m", message)
        if commit.returncode != 0:
            print("[X] git commit 失败：\n" + (commit.stderr or commit.stdout).strip())
            return 1
        headline = next((l for l in commit.stdout.splitlines() if l.strip()), message)
        print("[OK] 已提交：" + headline)
    else:
        print("[..] 没有新的改动，直接推送已有提交")

    # 4. 推送（没有上游分支时用 -u 建立关联）
    has_upstream = git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}").returncode == 0
    push_args = ["push"] if has_upstream else ["push", "-u", REMOTE, BRANCH]
    if force:
        push_args.insert(1, "--force")

    print("[..] 正在推送……")
    push = git(*push_args)
    out = ((push.stdout or "") + (push.stderr or "")).strip()
    if out:
        print(out)

    if push.returncode == 0:
        print("")
        print("[OK] 推送成功。等 1~2 分钟，网站会自动更新：")
        print("     " + PAGES_URL)
        print("     文章页 " + PAGES_URL + "/posts/2026-09-16-long-text-render-test.html")
        return 0

    # 5. 失败时按原因给办法
    low = out.lower()
    print("")

    if any(k in low for k in ("could not connect", "failed to connect", "connection was reset", "timed out", "operation timed out")):
        print("[X] 连不上 github.com —— 当前网络到不了 GitHub。")
        print("    浏览器插件类的代理只代理浏览器，命令行用不到。两个办法：")
        print("    办法一：打开一个系统级代理（v2rayN / Clash），然后执行")
        print("            git config --global http.proxy  http://127.0.0.1:10809")
        print("            git config --global https.proxy http://127.0.0.1:10809")
        print("            （端口换成你软件里显示的 HTTP 端口，Clash 常见 7890）")
        print("            设完再运行一次本脚本。")
        print("    办法二：直接用 GitHub Desktop 推送，它会跟随 Windows 系统代理。")
        return 2

    if any(k in low for k in ("non-fast-forward", "rejected", "fetch first", "unrelated histories")):
        print("[X] 远程有本地没有的提交，两条历史对不上。")
        print("    如果确认远程那份是旧版、可以被覆盖，加 --force 再跑一次：")
        print('        python tools/upload.py "首次对齐" --force')
        return 3

    if any(k in low for k in ("authentication failed", "permission denied", "could not read username", "invalid username or password")):
        print("[X] 身份验证没通过。")
        print("    弹出的登录窗口里请用 AndyLin778 这个账号登录并授权。")
        print("    如果要求输入密码，需要到 GitHub 生成 Personal Access Token 代替密码。")
        return 4

    print("[X] 推送失败，上面的输出里有具体原因。")
    return 5


if __name__ == "__main__":
    sys.exit(main())
