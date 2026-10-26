"""Extract the fixed sections in the supplied source; not a Markdown renderer.
Run: python recite/tools/build_content.py
"""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / 'source/essays.md').read_text(encoding='utf-8')
translations = json.loads((ROOT / 'source/translations.json').read_text(encoding='utf-8'))
units = []
for match in re.finditer(r'^## (20\d{2}) · Part ([AB]) ｜(.+?)（约 .*?）\s*\n(.*?)(?=^## 20|^# 附|\Z)', source, re.M | re.S):
    year, part, title, body = match.groups()
    uid = f'{year}-{part}'
    prompt = re.search(r'### 题目\s*```text\s*\n(.*?)```', body, re.S).group(1).strip()
    approach_text = body.split('### 写作思路', 1)[1].split('### 范文', 1)[0]
    approach = []
    for line in approach_text.splitlines():
        if not line.startswith('|') or line.startswith('| 项') or line.startswith('| ---'):
            continue
        cells = line.strip('|').split('|')
        approach.append(re.sub(r'\*\*|`', '', cells[0].strip() + '：' + cells[1].strip()))
    essay = body.split('### 范文', 1)[1].split('\n', 1)[1]
    if '```text' in essay:
        essay = re.search(r'```text\s*\n(.*?)```', essay, re.S).group(1)
    else:
        essay = '\n'.join(line[1:].lstrip() for line in essay.splitlines() if line.startswith('>'))
    chunks = [chunk.strip() for chunk in re.split(r'\n\s*\n', essay.strip()) if chunk.strip()]
    chunks = ['\n'.join(line.strip() for line in chunk.splitlines()) if chunk.strip().startswith(('Yours', 'Li Ming')) else ' '.join(chunk.split()) for chunk in chunks]
    if chunks[0].startswith('Dear '):
        chunks = [chunks[0] + '\n' + chunks[1]] + chunks[2:]
    zh = translations[uid]
    assert len(chunks) == len(zh), (uid, len(chunks), len(zh))
    assert approach and prompt and all(zh), uid
    img = re.search(r'!\[([^\]]+)\]\(([^)]+)\)', body)
    if img:
        assert (ROOT / 'images' / img.group(2)).is_file()
    units.append(dict(id=uid, title=f'{year} · {title}', category=f'{year} / PART {part}',
        source='题目、英文与思路：2021—2026 范文与思路（背诵版）。参考范文，非官方答案；中文为本页补译。',
        note='保留材料中的背诵加长版，篇幅可能超过题目要求。',
        prompt=prompt, approach=approach,
        image=('images/' + img.group(2)) if img else None,
        imageAlt=img.group(1) if img else '',
        paragraphs=[dict(en=en, zh=cn) for en, cn in zip(chunks, zh)]))
assert len(units) == 12 and len({u['id'] for u in units}) == 12
units.sort(key=lambda u: (-int(u['id'][:4]), u['id'][-1]))
for unit in units:
    unit['module'] = 'exams'
    unit['part'] = unit['id'][-1]

# Only the chosen complete versions are imported, not alternate drafts or the full phrase bank.
prediction = (ROOT / 'source/prediction01.md').read_text(encoding='utf-8')
selection = json.loads((ROOT / 'source/prediction-selection.json').read_text(encoding='utf-8'))
for part in ('A', 'B'):
    chosen = selection[part]
    if part == 'A':
        section = prediction.split('## 完整范文（95 词）', 1)[1].split('**四段功能**', 1)[0]
        prompt_section = prediction.split('## 题面原文', 1)[1].split('## 思路五步', 1)[0]
        prompt = '\n'.join(line[1:].strip().replace('**', '') for line in prompt_section.splitlines() if line.startswith('>')).strip()
    else:
        section = prediction.split('> Two woodcutters work in one clearing.', 1)[1].split('## 每段在干什么', 1)[0]
        section = '> Two woodcutters work in one clearing.' + section
        prompt = '题意整理：根据图画描述两名樵夫的行为与结果差异，解读“磨刀不误砍柴工”的寓意，并发表评论。图画见下方。\n原材料没有单列 Part B 的 Directions 原文，此处为题意概括。'
    essay = '\n'.join(line[1:].lstrip() for line in section.splitlines() if line.startswith('>'))
    chunks = [p.strip() for p in re.split(r'\n\s*\n', essay.strip()) if p.strip()]
    assert len(chunks) == len(chosen['translations'])
    units.append(dict(id='prediction01-' + part, module='predictions', part=part,
        title=chosen['title'], category='预测卷一 / PART ' + part,
        source='选自《预测卷01 作文与素材》：' + ('第九节完整范文' if part == 'A' else '第五节打磨版完整范文') + '；英文保留原文，中文为本页补译。',
        note='知经 KNOWECON 预测模拟卷 01 · 本页保留一篇精选范文与六条积累。',
        prompt=prompt, approach=chosen['approach'], materials=chosen['materials'],
        image='images/prediction01-B.jpg' if part == 'B' else None,
        imageAlt='预测卷一：两名樵夫，磨刀与用钝刀砍柴的对比',
        imageCaption='预测卷一配图 · 点击查看大图',
        paragraphs=[dict(en=en, zh=zh) for en, zh in zip(chunks, chosen['translations'])]))

# Fixed context is reviewed per essay: greetings and courtesies stay visible;
# opening/closing paragraphs with actual task details remain recall targets.
fixed = {'2021-A': [0, 2, 3], '2022-A': [3], '2023-A': [0, 5],
         '2024-A': [0, 2, 3], '2025-A': [0, 3], '2026-A': [0, 4],
         'prediction01-A': [0, 4]}
for unit in units:
    for i, paragraph in enumerate(unit['paragraphs']):
        paragraph['core'] = i not in fixed.get(unit['id'], [])
        if unit['part'] == 'A' and paragraph['core'] and paragraph['en'].startswith('Dear '):
            paragraph['prefix'], paragraph['en'] = paragraph['en'].split('\n', 1)
    if unit.get('image'):
        assert (ROOT / unit['image']).is_file()
assert len(units) == 14 and len({u['id'] for u in units}) == 14
(ROOT / 'content.js').write_text('// Generated from source/ by tools/build_content.py. No runtime fetch required.\nwindow.RECITE_UNITS = ' + json.dumps(units, ensure_ascii=False, indent=2) + ';\n', encoding='utf-8')
print(f'Built {len(units)} units, {sum(len(u["paragraphs"]) for u in units)} matched paragraph pairs, 7 local images.')
