## 概述

该目录下包含 GPT 翻译和翻译润色的工具。除代码文件以外，按章节存放用作对照的英文原文，确保和中文翻译的章节标号一致。

出于作者权益考虑，请确保英文原文 **不** 被 push 到仓库中。该路径下已设置 `.gitignore` ，忽略所有 `.md` 文件。

## 初始化方式（包括添加新章节和卷）

- 从 AO3 [TTS](https://archiveofourown.org/works/777002?view_full_work=true) 下载 EPUB 后[转换](https://www.vertopal.com/en/convert/epub-to-md)为 Markdown ，保存为 `books_en/fulltext_en.md` 。
- 从 `books_en/` 目录下运行 `split_chapters.py` 脚本，生成各卷和各章节的英文原文。

## 翻译和润色

- 从 `books_en/` 目录下运行 `translate_chapter.py` 脚本，跟随提示翻译和润色指定章节。