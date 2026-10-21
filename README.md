# :four_leaf_clover:四叶草哈汉混合输入方案

> 本项目基于 四叶草简体拼音输入方案二次开发，支持汉语和哈萨克语混合输入。

## 简介

在linux端，很多拼音输入法有少许 bug 或卡顿，或功能不全，所以接触了 [rime](https://rime.im) ，然而自带的[朙月拼音](https://github.com/rime/rime-luna-pinyin)和[袖珍简化字拼音](https://github.com/rime/rime-pinyin-simp)均不是很不是很理想，但是探索过程中发现很多很好的开源项目提供词库，而 rime 输入法引擎几乎拥有所有的优点（开源、干净无广告、运行流畅、跨平台、...），甚至云同步也能用坚果云之类的服务手动实现，唯一的缺点就是门槛高定制困难，默认配置的不习惯劝退了很多人。

在此方案诞生之前，我没能找到一个比较不错的简体拼音（全拼）的输入方案，多数人用惯了大陆国产的输入法，而以我的动手能力，完全能够按照这些输入法的习惯，自己定制一个方案，共享给更多的人，让更多的人不需要怎么配置也能用上非常类似于搜狗拼音输入法的方案，尽可能开箱即用，降低所有人的使用门槛。所以，为什么不自己做一个呢？

**这个项目我会持续更新，因为我一直在用输入法，我会调教到完全合我的口味习惯为止（我过去一直在用搜狗拼音输入法）。所以如果你觉得哪里不好用，或者哪里想改善，一定要及时在 [issues](https://github.com/fkxxyz/rime-cloverpinyin/issues) 提出，我只要看到就会回复。**

- 博文地址	https://www.fkxxyz.com/d/cloverpinyin

- 项目地址	https://github.com/fkxxyz/rime-cloverpinyin

## 特色

我亲自打造的基于[rime](https://rime.im/)的简体拼音输入方案，有以下几大特点：

1. 完全从零开始制作文字的拼音和基础词库，导入了几个很好用的词库：

   - 用 [pypinyin](https://github.com/mozillazg/python-pinyin) 项目生成所有字词的拼音
   - 合并[结巴中文分词](https://github.com/fxsjy/jieba)项目、[rime八股文](https://github.com/rime/rime-essay)和[袖珍简化字拼音](https://github.com/rime/rime-pinyin-simp)的字的字频
   - 由百度搜索到某个人基于大数据做过的[360万中文词库+词性+词频](https://download.csdn.net/download/xmp3x/8621683)，该词库是用ansj分词对270G新闻语料进行分词统计词频获得
   - [清华大学开源词库](https://github.com/thunlp/THUOCL)，统计来自各大主流网站如CSDN博客、新浪新闻、搜狗语料
   - 搜狗细胞词库 [网络流行新词【官方推荐】](https://pinyin.sogou.com/dict/detail/index/4)
  
2. 词库本身基于简体，并且加入繁简切换，包括自定义词库也能切换繁体（朙月拼音输入简体时的需要经过opencc转换，而且自定义词库也得手动转换成繁体才能繁简切换，而袖珍简化字拼音不支持繁体）

3. 默认加入 emoji 表情输入支持

   ![](https://www.fkxxyz.com/img/cloverpinyin-1.png)

4. 加入拼音输入特殊符号的支持（如输入 pingfang 即可打出 ²）

   ![](https://www.fkxxyz.com/img/cloverpinyin-2.png)

   [rime-symbols](https://github.com/fkxxyz/rime-symbols) 该模块与此项目独立，你也可以把这个模块放到别的方案上用。

5. 修改了几乎所有特殊符号的按键，定制全部快捷键，使之符合搜狗输入法的习惯

不磨蹭了，直接介绍怎么开始使用吧。

## 安装

### 仓输入法（iOS / Hamster）

请导入构建后的 `data/*.zip`，不要直接导入 GitHub 的源码 ZIP 或单独复制 `src/`。
源码不包含生成的中文基础词库和 OpenCC 资源，不能直接部署。

三个安装包分别为：

| 包名前缀 | 方案 | 哈萨克语编码 |
| --- | --- | --- |
| `clover_hapin_arabic.schema-` | 哈汉老文字混合输入 | `u` 前缀 |
| `clover_hapin_cyrillic.schema-` | 哈汉西里尔混合输入 | `u` 前缀 |
| `clover_hapin_mixed_arabic_cyrillic.schema-` | 哈汉双文字混合输入 | 老文字 `u`、西里尔 `v` 前缀 |

1. 将需要的 ZIP 发送到 iPhone，通过分享菜单选择仓输入法导入。
2. 打开仓，重新部署，并在输入方案设置中启用对应的四叶草方案。
3. 测试中文 `nihao` 和哈萨克语 `usalyem`；双文字方案还可以测试 `vsalyem`。

也可以解压后把文件放到仓的 `Rime` 目录：`*.schema.yaml` 和 `*.dict.yaml`
必须直接位于该目录，`opencc/` 保留子目录，不能再套一层项目文件夹。
如果已开启仓的 iCloud 同步，需要同时更新 iCloud 对应的方案目录，
否则重新部署时可能被旧文件覆盖。

如果导入后仍不能使用，请在仓中查看部署日志，搜索 `Error`、`failed`、
`clover_hapin` 或 `dictionary`，记录第一处错误及其前后内容。

参考：[仓官方安装说明](https://github.com/imfuxiao/Hamster/wiki)。
桌面端也可参考上游的 [Windows](https://github.com/fkxxyz/rime-cloverpinyin/wiki/windows)
和 [Linux](https://github.com/fkxxyz/rime-cloverpinyin/wiki/linux) 安装说明。

## 从本仓库源码构建

项目已收录桌面的哈萨克语阿拉伯文字、西里尔文字及柯尔克孜语阿拉伯文字词表。
柯尔克孜语并入老文字哈萨克语词库，沿用 `u` 编码，不增加独立前缀。
词表来源、合并统计及编码规则见 [vocabulary/README.md](vocabulary/README.md)。

本项目生成可由 Rime 客户端部署的词库源码安装包，不包含跨平台通用的预编译二进制词库。

如果你想自己从零开始构建，或者想为别的 linux 发行版打包，那么继续往下看。

该仓库的内容只包含构建四叶草输入法方案的脚本，构建需要以下环境

操作系统：Linux 或 macOS

python版本： 3

Python 依赖统一列在 `requirements.txt` 中，建议使用虚拟环境：

```shell
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

如果是 archlinux 用户，可用下面命令快速安装这些依赖

```shell
pacman -S python-jieba pypinyin opencc python-requests
```

下载工具（三者任意一个均可）： [aria2](http://aria2.sourceforge.net/)、[wget](https://www.gnu.org/software/wget/wget.html)、[curl](https://curl.haxx.se/)

解压工具（三者任意一个均可）： [unzip](https://www.info-zip.org/UnZip.html)、[bsdtar](https://libarchive.org/)、[7z](http://p7zip.sourceforge.net/)

部署编译验证所需的基础库： [librime](https://github.com/rime/librime)（生成源码安装包不需要本机安装）

部署时由输入法提供的基础配置： [librime-prelude](https://github.com/rime/rime-prelude)

克隆此仓库，并下载所有 submodule（360 万词典已随源码提供）

```shell
git clone https://github.com/ha-pin/rime-cloverpinyin.git
cd rime-cloverpinyin
git submodule update --init
```

然后直接执行构建即可

```shell
./build.sh
```

完成后，会生成 cache 目录和 data 目录

- data 是最终生成的目录
- cache 是生成过程中下载和生成的中间文件



其中，执行 build 时，可以有个参数

```shell
./build.sh [minfreq]
```

minfreq 代表360万词里面指定的最小词频，频率低于该值的词语会被筛选掉，达到精简词库的目的，默认是100，该值越小，最终生成的词库越大，为 0 表示不精简词库（会生成大约 100 兆左右的词库）。

构建完成后，可以打包，在 data 目录生成发布用的压缩包

```
./pack.sh [ver]
```

当前规则版本为 `2`，由根目录 `VERSION` 文件记录。打包时使用 `./pack.sh 2`。两个脚本均可从任意工作目录执行。
构建与打包都会自动检查三个方案的词典名称、导入文件及 OpenCC 资源。
也可单独运行 `python3 scripts/validate_packages.py data`。
GitHub Actions 会使用 librime 实际编译三个方案，并上传 ZIP 构建产物。
推送与 `VERSION` 对应的 `v2` 标签，或手动运行 Build and Release Schema workflow，
会将三个 `*.schema-2.zip` 安装包发布到 GitHub Release。普通分支提交与 PR 运行构建校验。
Release 说明来自 `RELEASE_NOTES.md`，发布前请同步更新版本文件、方案及词典版本。

---

## 写在最后

此项目完全开源，你可以随意 fork 或修改和定制，如果你觉得好用，可以来[AUR投票](https://aur.archlinux.org/packages/rime-cloverpinyin/)和在[github上star](https://github.com/fkxxyz/rime-cloverpinyin)，投票和star的人越多越容易被搜索到，以此更好地传播出去。

再次重复开头说的：

**这个项目我会持续更新，因为我一直在用输入法，我会调教到完全合我的口味习惯为止（我过去一直在用搜狗拼音输入法）。所以如果你觉得哪里不好用，或者哪里想改善，一定要及时在 [issues](https://github.com/fkxxyz/rime-cloverpinyin/issues) 提出，我只要看到就会回复。**

当然你也可以直接[联系我](https://www.fkxxyz.com/about/#%E5%85%B3%E4%BA%8E%E6%88%91)本人。

