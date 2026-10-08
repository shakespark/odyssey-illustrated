#!/usr/bin/env python3
"""从本机的 epub 解压目录提取每章文本到 source/text/NN.txt（00 = Preface，01–12 正文）。
每行一段，行首 [段号]（全章连续编号）；`# §k` 是原书用 • • • 隔开的第 k 节，后面是这一节的词数。
{L} 表示这一段是缩进排印的引文（多半是作者当年的信）；{V} 是诗句或歌词。"""
import glob, html, os, re
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
os.makedirs(os.path.join(ROOT, "source/text"), exist_ok=True)
files = sorted(glob.glob(os.path.join(ROOT, "source/epub/text/part*.html")))[6:19]
for k, f in enumerate(files):
    s = open(f, encoding="utf-8").read()
    secs, cur = [], []
    for cls, p in re.findall(r'<p class="(para\d?)"[^>]*>(.*?)</p>', s, flags=re.S):
        t = re.sub(r"\s+", " ", html.unescape(re.sub("<[^>]+>", "", p))).strip()
        if cls == "para" and set(t) <= set("•  "):
            secs.append(cur); cur = []
        elif cls in ("para7", "para8", "para9") and t:
            cur.append(("{V} " if cls == "para7" else "{L} ") + t)
        elif cls in ("para4", "para5", "para") and t:
            cur.append(t)
    secs.append(cur)
    secs = [x for x in secs if x]
    out, i = [], 0
    for j, sec in enumerate(secs):
        out.append(f"# §{j + 1} {sum(len(x.split()) for x in sec)} 词\n")
        for t in sec:
            i += 1; out.append(f"[{i}] {t}\n")
    open(os.path.join(ROOT, f"source/text/{k:02d}.txt"), "w", encoding="utf-8").write("".join(out))
    print(f"{k:02d} {len(secs):2d} 节 {i:3d} 段 {sum(len(x.split()) for x in out if x[0] == '['):5d} 词")
