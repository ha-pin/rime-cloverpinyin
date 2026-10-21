# 🍀 四叶草哈汉混合输入方案

基于 [四叶草简体拼音](https://github.com/fkxxyz/rime-cloverpinyin) 二次开发的
[Rime](https://rime.im/) 输入方案，支持中文拼音、哈萨克语阿拉伯文字和西里尔文字混合输入。
柯尔克孜语阿拉伯文字词条并入哈萨克语老文字词库，沿用原有编码，不增加独立前缀。

当前规则版本：**2**。版本记录在 [VERSION](VERSION)，变更说明见 [RELEASE_NOTES.md](RELEASE_NOTES.md)。

[下载安装包](https://github.com/ha-pin/rime-cloverpinyin/releases) ·
[构建与发布状态](https://github.com/ha-pin/rime-cloverpinyin/actions/workflows/build.yml) ·
[反馈问题](https://github.com/ha-pin/rime-cloverpinyin/issues)

## 下载与方案选择

在 Releases 中选择 `v2`，下载 Assets 下对应的方案 ZIP。
如果发布构建尚未完成，可通过上方 Actions 链接查看进度；检查全部通过后才会生成 Release 附件。

| 方案 | v2 安装包 | 输入前缀 |
| --- | --- | --- |
| 哈汉老文字混合输入 | `clover_hapin_arabic.schema-2.zip` | 阿拉伯文字 `u` |
| 哈汉西里尔混合输入 | `clover_hapin_cyrillic.schema-2.zip` | 西里尔文字 `u` |
| 哈汉双文字混合输入 | `clover_hapin_mixed_arabic_cyrillic.schema-2.zip` | 阿拉伯文字 `u`、西里尔文字 `v` |

三个方案均保留中文拼音输入、Emoji、特殊符号及繁简切换功能。
需要同时使用两种文字时，选择双文字版。

**请下载方案 ZIP。** GitHub 自动生成的 `Source code` 压缩包及仓库中的 `src/`
不含完整生成词库和 OpenCC 资源，不能直接作为安装包导入。

## 仓输入法安装（iOS / Hamster）

1. 将下载的方案 ZIP 保存到 iPhone，通过分享菜单选择仓输入法导入。
2. 在仓中重新部署，等待完成后，在输入方案设置中启用对应的四叶草方案。
3. 切换到仓键盘，测试下方的输入示例。

| 输入 | 老文字版 | 西里尔版 | 双文字版 |
| --- | --- | --- | --- |
| `nihao` | 中文候选 | 中文候选 | 中文候选 |
| `usalyem` | `سالەم` 等候选 | `сәлем` 等候选 | 阿拉伯文字候选 |
| `vsalyem` | — | — | `сәлем` 等西里尔文字候选 |
| `uqazaq` | `قازاق` 等候选 | 西里尔文字候选 | 阿拉伯文字候选 |
| `usalam` | `سالام` 等候选 | — | `سالام` 等候选 |

以上用于检查对应词条能否出现在候选中，候选顺序会受词频和用户词典影响。

也可以解压 ZIP，将方案文件复制到仓的 `Rime` 目录。`*.schema.yaml`、`*.dict.yaml`
和 `clover_hapin.key_bindings.yaml` 应直接位于该目录，`opencc/` 保留子目录，
不要在外面再套一层项目文件夹。

若启用了仓的 iCloud 同步，请同时更新 iCloud 对应的方案目录，避免重新部署时被旧文件覆盖。
安装方式参考 [仓官方说明](https://github.com/imfuxiao/Hamster/wiki)。
桌面端可参考上游的 [Windows](https://github.com/fkxxyz/rime-cloverpinyin/wiki/windows)
和 [Linux](https://github.com/fkxxyz/rime-cloverpinyin/wiki/linux) 说明。

### 无法加载时

- 确认导入的是 Release 中的方案 ZIP，且已重新部署并启用方案。
- 检查文件层级和 iCloud 中是否仍有旧配置。
- 查看部署日志，搜索 `Error`、`failed`、`clover_hapin` 或 `dictionary`。
- 在本项目 Issues 中附上安装包文件名、仓版本，以及第一处报错前后的日志。

## v2 词库与弱音输入

本次新增词表与原有基础字母、3000 词扩展和中文词库一起使用。

| 新增源词表 | 原始词条数 | 合并方式 |
| --- | ---: | --- |
| 哈萨克语阿拉伯文字 | 58,632 | 与柯尔克孜语阿拉伯文字合并 |
| 柯尔克孜语阿拉伯文字 | 76,599 | 并入老文字词库，统一使用 `u` |
| 哈萨克语西里尔文字 | 8,953 | 西里尔版使用 `u`，双文字版使用 `v` |

两份阿拉伯文字词表合并去重后包含 **123,184 个不同词形**。
仅排除一个纯装饰符条目 `ــ`，其余词形保留；同一词形可以对应多个编码。
新增词表没有原始词频，统一使用权重 `1`。
来源、校验值和编码细节见 [词表说明](vocabulary/README.md)。

### 弱音符号可以省略输入吗？

新增词库同时生成完整编码和省略元音修饰符 `x` 的简写。例如：

| 输出词条 | 完整编码 | 简写 |
| --- | --- | --- |
| `ٴسالەم` | `usxalyem` | `usalyem` |

省略 `x` 只改变输入编码，输出仍保留原词的弱音符号。
新增阿拉伯文字哈萨克语词表中，959 个词条含弱音符号，其中 931 个支持两种编码。
另有 28 个词条因符号位于词尾或没有适用元音，仍保留独立 `x`，目前不支持省略。

当前转换规则只修饰弱音符号后的第一个适用元音，没有扩展为整词元音自动匹配。
西里尔元音 `ә/ө/ү/і` 也有省略修饰符 `x` 的简写，硬软音符的 `xx/xy` 编码保留。

## 从源码构建

支持 Linux 和 macOS。需要 Python 3、Git 和 `zip`；CI 使用 Python 3.11。
构建时会在线获取搜狗新词，因此需要网络连接。

```shell
git clone --recurse-submodules https://github.com/ha-pin/rime-cloverpinyin.git
cd rime-cloverpinyin
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
./build.sh
./pack.sh 2
```

已有仓库先运行 `git submodule update --init`。
360 万中文词典及新增的三份词表已随源码保存，不需要从桌面重新复制。

构建后，`cache/` 保存中间文件和 `vocabulary-report.json` 导入统计，
`data/` 保存三个方案目录及打包后的 ZIP。`python3 scripts/prepare_publish.py`
会把本版本的三个方案 ZIP 校验并复制到独立的 `dist/` 发布目录。

`./build.sh [minfreq]` 的参数控制 360 万中文词库的最小词频，默认 `100`；
数值越小，保留词条越多，安装包与部署开销也越大。`0` 表示不按此词频过滤。
两个脚本均可通过完整路径从其他工作目录执行。

### 本地校验

```shell
python3 -m unittest discover -s scripts -p 'test_*.py' -v
python3 scripts/validate_packages.py data
```

构建和打包都会自动检查方案与词典版本、词典名称、导入文件和 OpenCC 资源。
单元测试检查原有字母编码、弱音简写、词表覆盖和去重。
若需要本机编译验证，还需安装 librime 和 Rime 基础配置；生成源码安装包本身不需要 librime。

## 自动构建与 Release

[Build and Release Schema](.github/workflows/build.yml) 会执行词表测试、完整构建、
librime 编译、安装包校验和打包。发布前按固定文件名白名单将三个 ZIP 放入 `dist/`，
Actions 构建产物、GitHub Release 和 gh-pages 均只读取该目录。

- 推送 `master` 或提交到 `master` 的 PR：运行构建检查并上传 Actions 构建产物。
- 非 PR 构建通过后：更新 gh-pages，只保留三个方案 ZIP 和部署标记 `.nojekyll`；不发布源码、子模块、缓存或整个项目目录。
- 推送与 `VERSION` 一致的版本标签（当前为 `v2`）：检查通过后发布 GitHub Release。
- 手动运行 workflow：按当前 `VERSION` 发布；已有 Release 时更新同名 ZIP 附件。

发布新版本时，同步更新 `VERSION`、源方案和词典版本，以及 `RELEASE_NOTES.md`。
标签与版本不一致时构建会失败。Release 附件是供客户端部署的源码词库包，
不包含跨平台通用的预编译二进制词库。GitHub Release 页面自动提供的 `Source code`
是平台的源码下载入口，不属于 workflow 上传的发布附件。

## 来源与致谢

- [四叶草简体拼音](https://github.com/fkxxyz/rime-cloverpinyin)：原方案与中文词库构建脚本。
- [jieba](https://github.com/fxsjy/jieba)、[pypinyin](https://github.com/mozillazg/python-pinyin)：中文词频和拼音生成。
- [Rime 八股文](https://github.com/rime/rime-essay)、[袖珍简化字拼音](https://github.com/rime/rime-pinyin-simp)、[THUOCL](https://github.com/thunlp/THUOCL)：中文基础词库。
- [rime-emoji](https://github.com/rime/rime-emoji)、[rime-symbols](https://github.com/fkxxyz/rime-symbols)、[OpenCC](https://github.com/BYVoid/OpenCC)：表情、符号和文字转换。
- [新增词表来源与提取说明](vocabulary/extraction_notes.txt)。

项目许可证见 [LICENSE](LICENSE)。
