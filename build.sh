#!/usr/bin/env bash
set -euo pipefail

SHELLDIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${PYTHON:-python3}"


minfreq="${1:-100}"

for source in rime-symbols/rime-symbols-gen rime-emoji/opencc/emoji.json rime-essay/essay.txt rime-pinyin-simp/pinyin_simp.dict.yaml THUOCL/data libscel/scel.py; do
  if [[ ! -e "$SHELLDIR/$source" ]]; then
    echo "缺少构建依赖 $source，请先运行 git submodule update --init" >&2
    exit 1
  fi
done

mkdir -p "$SHELLDIR/cache"
cd "$SHELLDIR/cache"

# 本地保存的纯词表转换为带编码的 Rime 扩展词典。
"$PYTHON" "$SHELLDIR/scripts/import_vocabulary.py"

# 生成符号列表
mkdir -p opencc
(
  cd opencc
  "$PYTHON" ../../rime-symbols/rime-symbols-gen
)

# 生成符号词汇
cat ../rime-emoji/opencc/*.txt opencc/*.txt | "$PYTHON" -c 'import sys, opencc; sys.stdout.write(opencc.OpenCC("t2s.json").convert(sys.stdin.read()))' | uniq > symbols.txt

# 开始生成词典
ln -sf "../rime-essay/essay.txt" .
ln -sf "../chinese-dictionary-3.6million/词典360万（个人整理）.txt" .
ln -sf "../rime-pinyin-simp/pinyin_simp.dict.yaml" .
"$PYTHON" ../src/clover-dict-gen.py --minfreq="$minfreq"
while read -r file; do
  echo "转换 $file"
  "$PYTHON" ../src/thuocl2rime.py "$file"
done < <(find ../THUOCL/data -type f -name 'THUOCL_*.txt')
cp ../src/sogou_new_words.dict.yaml .
"$PYTHON" ../libscel/scel.py >> sogou_new_words.dict.yaml

# 生成 data 目录
mkdir -p ../data

# 根据不同类型生成不同目录，分开打包
echo "生成 hapin_arabic"
mkdir -p ../data/hapin_arabic
cp ../src/clover_hapin_arabic.*.yaml ../src/clover_hapin.*.yaml ../src/hapin_arabic_*.*.yaml ../src/hapin_emoji.dict.yaml THUOCL_*.yaml ../src/sogou_new_words.dict.yaml ../data/hapin_arabic

echo "生成 hapin_cyrillic"
mkdir -p ../data/hapin_cyrillic
cp ../src/clover_hapin_cyrillic.*.yaml ../src/clover_hapin.*.yaml ../src/hapin_cyrillic_*.*.yaml ../src/hapin_emoji.dict.yaml THUOCL_*.yaml ../src/sogou_new_words.dict.yaml ../data/hapin_cyrillic

echo "生成 hapin_mixed_arabic_cyrillic"
mkdir -p ../data/hapin_mixed_arabic_cyrillic
cp ../src/clover_hapin_mixed_arabic_cyrillic.*.yaml ../src/clover_hapin.*.yaml ../src/hapin_arabic_*.*.yaml ../src/hapin_mixed_cyrillic_*.*.yaml ../src/hapin_emoji.dict.yaml THUOCL_*.yaml ../src/sogou_new_words.dict.yaml ../data/hapin_mixed_arabic_cyrillic

# 三个方案共用生成的中文词库和搜狗新词，不能只复制 src 中的空模板。
for variant in hapin_arabic hapin_cyrillic hapin_mixed_arabic_cyrillic; do
  cp clover_hapin.base.dict.yaml clover_hapin.phrase.dict.yaml sogou_new_words.dict.yaml "../data/$variant/"
done
cp hapin_arabic_desktop.dict.yaml ../data/hapin_arabic/
cp hapin_cyrillic_desktop.dict.yaml ../data/hapin_cyrillic/
cp hapin_arabic_desktop.dict.yaml hapin_mixed_cyrillic_desktop.dict.yaml ../data/hapin_mixed_arabic_cyrillic/

# 生成 opencc 目录
cd ../data
mkdir -p opencc
cp ../rime-emoji/opencc/* opencc
cp ../cache/opencc/* opencc

mkdir -p ../data/hapin_arabic/opencc
mkdir -p ../data/hapin_cyrillic/opencc
mkdir -p ../data/hapin_mixed_arabic_cyrillic/opencc

cp opencc/* ../data/hapin_arabic/opencc
cp opencc/* ../data/hapin_cyrillic/opencc
cp opencc/* ../data/hapin_mixed_arabic_cyrillic/opencc

# echo "开始构建部署二进制"
# rime_deployer --compile clover.schema.yaml . /usr/share/rime-data
"$PYTHON" "$SHELLDIR/scripts/validate_packages.py" "$SHELLDIR/data"
