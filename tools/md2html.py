#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 Markdown 文章转换成 post.html 里的正文 HTML。

用法：
    python tools/md2html.py 你的文章.md posts/2026-09-16-long-text-render-test.html
    python tools/md2html.py 你的文章.md projects/no-ai-memo.html --skip-h1

说明：
    目标页面里必须保留下面这两行占位标记，脚本只替换它们之间的正文：
        <!-- ARTICLE:START -->
        <!-- ARTICLE:END -->

    新增一篇文章时：把 posts/ 下现有的文章页复制一份，
    清空两个标记之间的内容，再运行上面的命令即可。

    --skip-h1：跳过源文件开头的一级标题。页面标题由页头的 <h1> 提供时用它，
    免得正文里再出现一遍同样的标题。

支持的元素：
    # ~ ###### 标题           普通段落
    **粗体**  *斜体*          `行内代码`
    ``` 代码块 ```            | 表格 |（含 :-- / --: / :-: 对齐）
    > 引用                    --- 分隔线
    - 无序列表 / 1. 有序列表
    $$ 独立公式 $$            \\( 行内公式 \\)
    [文字](https://链接)      （只处理 http/https，新窗口打开）
"""

import html
import re
import sys
from pathlib import Path

START = "<!-- ARTICLE:START -->"
END = "<!-- ARTICLE:END -->"


def esc(text):
    """转义 HTML 特殊字符。& 会被 KaTeX 正确还原成数学里的 &。"""
    return html.escape(text, quote=False)


def inline(text):
    """处理行内语法。传入的 text 必须是已经转义过的。"""
    stash = []

    def hold(fragment):
        stash.append(fragment)
        return "\x00%d\x00" % (len(stash) - 1)

    # 行内代码先抽出来，避免里面的符号被当成 Markdown 语法
    text = re.sub(r"`([^`\n]+)`", lambda m: hold("<code>%s</code>" % m.group(1)), text)
    # 粗体
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # 斜体（避开已经处理过的粗体星号）
    text = re.sub(r"(?<![\*\w])\*([^\*\n]+)\*(?!\*)", r"<em>\1</em>", text)
    # 链接：只认 http/https，先抽成占位符，免得方括号、圆括号被后面的规则再碰一次
    text = re.sub(
        r"\[([^\]\n]+)\]\((https?://[^\s)]+)\)",
        lambda m: hold(
            '<a href="%s" target="_blank" rel="noopener">%s</a>'
            % (m.group(2), m.group(1))
        ),
        text,
    )

    return re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], text)


def is_block_start(line):
    t = line.strip()
    return (
        t.startswith("```")
        or t.startswith("$$")
        or t.startswith("|")
        or t.startswith(">")
        or t in ("---", "***", "___")
        or re.match(r"^#{1,6}\s", t) is not None
        or re.match(r"^[-*+]\s+", t) is not None
        or re.match(r"^\d+[.)]\s+", t) is not None
    )


def convert(md_text, skip_first_h1=False):
    lines = md_text.replace("\r\n", "\n").split("\n")

    # --skip-h1：源稿开头的一级标题就是页面标题，页头已经显示过一次了，
    # 这里把它清掉，避免正文重复同样的标题。
    if skip_first_h1:
        for k, line in enumerate(lines):
            if not line.strip():
                continue
            if re.match(r"^#\s+", line.strip()):
                lines[k] = ""
            break

    out = []
    stats = {"h": 0, "math": 0, "table": 0, "code": 0, "quote": 0, "list": 0, "p": 0}
    i, n = 0, len(lines)

    while i < n:
        raw = lines[i]
        s = raw.strip()

        if not s:
            i += 1
            continue

        # ---------- 代码块 ----------
        if s.startswith("```"):
            lang = s[3:].strip()
            i += 1
            buf = []
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1  # 跳过结束的 ```
            attr = ' data-lang="%s"' % esc(lang) if lang else ""
            out.append("<pre%s><code>%s</code></pre>" % (attr, esc("\n".join(buf))))
            stats["code"] += 1
            continue

        # ---------- 独立数学公式 ----------
        if s == "$$":
            i += 1
            buf = []
            while i < n and lines[i].strip() != "$$":
                buf.append(lines[i])
                i += 1
            i += 1
            out.append(
                '<div class="math-block">\n$$%s$$\n</div>' % esc("\n".join(buf))
            )
            stats["math"] += 1
            continue

        # ---------- 分隔线 ----------
        if s in ("---", "***", "___"):
            out.append("<hr>")
            i += 1
            continue

        # ---------- 标题（源码 h1 降为页面 h2） ----------
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            level = min(len(m.group(1)) + 1, 6)
            out.append(
                "<h%d>%s</h%d>" % (level, inline(esc(m.group(2).strip())), level)
            )
            stats["h"] += 1
            i += 1
            continue

        # ---------- 引用 ----------
        if s.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            paras, cur = [], []
            for b in buf:
                if b.strip():
                    cur.append(b.strip())
                elif cur:
                    paras.append(cur)
                    cur = []
            if cur:
                paras.append(cur)
            body = "".join(
                "<p>%s</p>" % inline(esc(" ".join(p))) for p in paras
            )
            out.append("<blockquote>%s</blockquote>" % body)
            stats["quote"] += 1
            continue

        # ---------- 表格 ----------
        if s.startswith("|"):
            buf = []
            while i < n and lines[i].strip().startswith("|"):
                buf.append(lines[i].strip())
                i += 1
            rows = [[c.strip() for c in r.strip("|").split("|")] for r in buf]
            aligns = ["left"] * len(rows[0])
            if len(rows) >= 2 and all(
                re.fullmatch(r":?-+:?", c) for c in rows[1]
            ):
                for k, c in enumerate(rows[1]):
                    if c.startswith(":") and c.endswith(":"):
                        aligns[k] = "center"
                    elif c.endswith(":"):
                        aligns[k] = "right"
                body_rows = rows[2:]
            else:
                body_rows = rows[1:]

            def cell(tag, text, idx):
                align = aligns[idx] if idx < len(aligns) else "left"
                attr = ' align="%s"' % align if align != "left" else ""
                return "<%s%s>%s</%s>" % (tag, attr, inline(esc(text)), tag)

            head = "".join(cell("th", c, k) for k, c in enumerate(rows[0]))
            body = "".join(
                "<tr>%s</tr>" % "".join(cell("td", c, k) for k, c in enumerate(r))
                for r in body_rows
            )
            out.append(
                '<div class="table-wrap"><table><thead><tr>%s</tr></thead>'
                "<tbody>%s</tbody></table></div>" % (head, body)
            )
            stats["table"] += 1
            continue

        # ---------- 列表 ----------
        if re.match(r"^[-*+]\s+", s) or re.match(r"^\d+[.)]\s+", s):
            ordered = re.match(r"^\d+[.)]\s+", s) is not None
            items = []
            while i < n:
                t = lines[i].strip()
                if re.match(r"^[-*+]\s+", t) or re.match(r"^\d+[.)]\s+", t):
                    items.append(re.sub(r"^([-*+]|\d+[.)])\s+", "", t))
                    i += 1
                elif t and items and lines[i][:1] in (" ", "\t") and not is_block_start(lines[i]):
                    items[-1] = items[-1] + " " + t
                    i += 1
                else:
                    break
            tag = "ol" if ordered else "ul"
            out.append(
                "<%s>%s</%s>"
                % (tag, "".join("<li>%s</li>" % inline(esc(x)) for x in items), tag)
            )
            stats["list"] += 1
            continue

        # ---------- 段落 ----------
        buf = []
        while i < n and lines[i].strip() and not is_block_start(lines[i]):
            buf.append(lines[i].strip())
            i += 1
        out.append("<p>%s</p>" % inline(esc("\n".join(buf))))
        stats["p"] += 1

    return "\n\n".join(out), stats


def main():
    args = sys.argv[1:]
    flags = {a for a in args if a.startswith("--")}
    paths = [a for a in args if not a.startswith("--")]

    unknown = flags - {"--skip-h1"}
    if unknown or not paths:
        if unknown:
            print("未知参数：%s" % " ".join(sorted(unknown)))
        print(__doc__)
        sys.exit(1)

    src = Path(paths[0])
    target = Path(paths[1]) if len(paths) > 1 else Path("post.html")

    skip_h1 = "--skip-h1" in flags
    body, stats = convert(src.read_text(encoding="utf-8"), skip_h1)

    page = target.read_text(encoding="utf-8")
    a, b = page.index(START), page.index(END)
    target.write_text(
        page[: a + len(START)] + "\n" + body + "\n" + page[b:], encoding="utf-8"
    )

    if skip_h1:
        print("已跳过源文件开头的一级标题（页面标题由页头提供）")

    print("已生成：%s" % target)
    print("正文 %d 字符" % len(body))
    print(
        "标题 %(h)d · 公式 %(math)d · 表格 %(table)d · 代码块 %(code)d · "
        "引用 %(quote)d · 列表 %(list)d · 段落 %(p)d" % stats
    )


if __name__ == "__main__":
    main()
