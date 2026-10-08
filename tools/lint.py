#!/usr/bin/env python3
"""章节页结构检查：python3 tools/lint.py chapters/NN.html …
查：.en 重复、.loc 不在原文对应段落里、.loc 词数、引用块数量、图片文件是否存在、图的数量、页面里的 <style>/<script>/写死的颜色。"""
import html, os, re, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
norm = lambda s: re.sub(r"\s+", " ", html.unescape(s).replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')).strip()
bad = 0
for path in sys.argv[1:]:
    t = open(path, encoding="utf-8").read(); errs = []
    nn = re.search(r"(\d\d)[a-c]?\.html$", path).group(1)
    src = os.path.join(ROOT, f"source/text/{nn}.txt")
    paras = {int(m.group(1)): norm(m.group(2)) for m in re.finditer(r"^\[(\d+)\] (.*)$", open(src, encoding="utf-8").read(), flags=re.M)} if os.path.exists(src) else {}
    ens = re.findall(r'<div class="en">(.*?)</div>', t)
    for e in sorted({e for e in ens if ens.count(e) > 1}): errs.append(f".en 重复：{e}")
    entries = re.findall(r'<div class="entry( trap)?">(.*?)</div></div>', t, flags=re.S)
    locs = re.findall(r'<div class="loc" data-p="(\d+)">(.*?)</div>', t)
    if len(locs) != len(ens): errs.append(f"词条 {len(ens)} 条，但 .loc 只有 {len(locs)} 个")
    last = 0
    for p, loc in locs:
        s = norm(re.sub(r"<[^>]+>", "", loc)).strip("… ").strip()
        n = len(s.split()); p = int(p)
        if paras and s not in paras.get(p, ""):
            where = [k for k, v in paras.items() if s in v]
            errs.append(f".loc 不在第 {p} 段：{s!r}" + (f"（在第 {where[0]} 段）" if where else "（全章都找不到）"))
        if n > 9: errs.append(f".loc 太长（{n} 词）：{s!r}")
        if p < last: errs.append(f"词条顺序：第 {p} 段的词条排在第 {last} 段之后：{s!r}")
        last = max(last, p)
    q = len(re.findall(r'<blockquote class="quote">', t))
    if q > 2: errs.append(f"引用块 {q} 处，超过 2 处")
    imgs = re.findall(r'<img[^>]+src="([^"]+)"', t)
    for i in imgs:
        if i.startswith("http") or not os.path.exists(os.path.join(os.path.dirname(path), i)): errs.append(f"图片不存在或是外链：{i}")
    svgs = len(re.findall(r"<svg\b", t))
    if nn != "00" and (len(imgs) + svgs < 4 or not imgs or not svgs): errs.append(f"图不够：照片 {len(imgs)}，SVG {svgs}（至少共 4 张，各至少 1 张）")
    if re.search(r"<svg(?![^>]*class=\"diagram\")", t): errs.append("有 SVG 没用 class=\"diagram\"")
    if re.search(r"<style|<script(?![^>]*src=)", t): errs.append("页面里有 <style> 或内联 <script>")
    for m in set(re.findall(r'(?:fill|stroke)="(#[0-9a-fA-F]+|[a-z]+)"', t)) - {"none", "currentColor"}: errs.append(f"SVG 里写死了颜色：{m}")
    if re.search(r'style="', t): errs.append('有内联 style="…"')
    for sec in ["这一章在做什么", "出场的人", "背景：作者默认你知道的事", "留个记号：后面还会回来", "词与短语", "值得停下来的句子", "检查一下理解"]:
        if nn != "00" and f"<h2>{sec}</h2>" not in t: errs.append(f"缺少小节：{sec}")
    traps = len(re.findall(r'class="entry trap"', t))
    print(("✗" if errs else "✓"), path, f"词条 {len(ens)}（trap {traps}） 照片 {len(imgs)} SVG {svgs} 引用 {q} 检查题 {len(re.findall('class=.check.', t))}")
    for e in errs: print("    " + e)
    bad += bool(errs)
sys.exit(1 if bad else 0)
