# 桌面词表导入

源文件从用户桌面 `Kazakhsha_Kirgizwshi_分类词库` 原样复制，原始提取说明保存在
`extraction_notes.txt`。该说明将来源标注为 Kazakhsha Kirgizwshi Android 3.66.0
内置词库。`manifest.json` 记录原文件名、行数与 SHA-256；转换时会校验。
源文件保留原文字形，不改写桌面文件。

| 文件 | 原始行数 | 处理方式 |
| --- | ---: | --- |
| kazakh_arabic.txt | 58,632 | 与下方柯尔克孜语词表合并，沿用 `u` |
| kyrgyz_arabic.txt | 76,599 | 并入哈萨克语老文字词库，不设独立前缀 |
| kazakh_cyrillic.txt | 8,953 | 西里尔方案用 `u`，双文字方案用 `v` |

阿拉伯文字合并后共有 **123,184 个不同词形**。哈萨克语源文件中只有装饰性
延长线的 `ــ` 不作为词条导入；其余词全部保留。重复的“词形 + 编码”只输出一次，
同一词形可保留不同编码。桌面拉丁文字词表不在此次导入范围内。

`scripts/import_vocabulary.py` 在 `build.sh` 中自动执行，将扩展词典生成到
`cache/`，随后复制到相应的安装包。源词表不提供词频，新增编码统一使用权重 1，
原有基础字母、3000 词和中文词库继续保留。

编码沿用 `src/hapin_*_basic.dict.yaml` 中的按键：例如 `قازاق` → `uqazaq`，
`سالام` → `usalam`。柯尔克孜语专用字母 `ۅ`、`ۉ`、`ئ` 分别映射为
`xo`、`xu`、`xe`，同时接受去掉元音修饰符 `x` 的简写。
哈萨克语弱音标记修饰其后第一个适用元音；末尾独立标记保留为 `x`。
西里尔硬软音符保留原有的 `xx`、`xy` 编码。
本次为词表编码与合并，没有将柯尔克孜语词形翻译或转换成西里尔文字。

专用字母字形参考 [Unicode 的哈萨克语、柯尔克孜语和维吾尔语文字说明](https://www.unicode.org/L2/L2020/20289-kazakh-kyrgyz-uyghur-annot.pdf)。
这些规则定义本项目的输入按键，原始词表的语言、拼写和词频质量仍依赖来源。

可执行：

```shell
python3 scripts/import_vocabulary.py
python3 -m unittest discover -s scripts -p 'test_*.py' -v
```

转换统计位于 `cache/vocabulary-report.json`，包含原始行数、去重词数、
编码覆盖数和排除的非词条。
