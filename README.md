# A Personal Odyssey · 英文伴读

陪读者读（听）英文原版 *A Personal Odyssey*（Thomas Sowell, 2000）。每一段人生一页：这一段在讲什么、出场的人、作者默认读者知道的背景、
配图、按出现顺序排的词与短语、几道理解检查题。本站没有译文，不替代原书。

线上地址：https://t.miaowuao.cn/odyssey/

## 目录结构

- `index.html`：首页（怎么用、目录、阅读进度、我的词本）
- `chapters/<id>.html`：`00` 开读之前；正文按章，长章拆成 `02a` `02b` `02c` 这样的上中下，共 23 页
- `assets/`：共享样式 `style.css`、脚本 `po.js`、目录数据 `chapters.js`、图片 `img/`（出处见 `img/CREDITS.md`）
- `tools/`：`extract.py` 提取原书文本、`fetch_img.py` 取图（转调 `~/tutorials-deploy/scripts/fetch_img.py`）、`lint.py` 结构检查、
  `overlap.py` 与原书的重合检查、`check.mjs` 浏览器检查
- `AUTHORING.md`：章节页编写规范
- `source/`：原书材料，只在本机，不入库、不部署

## 版权

原书版权归作者和出版方。本站不翻译、不转述原书，每页直接引用不超过两处、每处不超过 25 个英文单词。
照片来自维基共享资源，授权为公有领域或 CC BY / CC BY-SA，逐张登记在 `assets/img/CREDITS.md`；示意图是本站自己画的。

## 改完之后

```sh
python3 tools/lint.py chapters/*.html
python3 tools/overlap.py chapters/*.html index.html
node tools/check.mjs
```
推送到 `main` 即自动部署（见 `.github/workflows/deploy.yml`，部署方式见 `~/tutorials-deploy`）。
