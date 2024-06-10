#!/usr/bin/env bash
set -e

ver="$1"

ls ./rime-cloverpinyin/data

cd ./rime-cloverpinyin/data/hapin_arabic
rm -rf clover_hapin_arabic.schema-$ver.zip
# rm -rf clover_hapin_arabic.schema-build-$ver.zip
zip -5 clover_hapin_arabic.schema-$ver.zip *.yaml ../opencc/*
# zip -5 clover_hapin_arabic.schema-build-$ver.zip *.yaml ../opencc/* ../build/*

cd ./rime-cloverpinyin/data/hapin_cyrillic
rm -rf clover_hapin_cyrillic.schema-$ver.zip
# rm -rf clover_hapin_cyrillic.schema-build-$ver.zip
zip -5 clover_hapin_cyrillic.schema-$ver.zip *.yaml ../opencc/*
# zip -5 clover_hapin_cyrillic.schema-build-$ver.zip *.yaml ../opencc/* ../build/*

cd ./rime-cloverpinyin/data/hapin_mixed_arabic_cyrillic
rm -rf clover_hapin_mixed_arabic_cyrillic.schema-$ver.zip
# rm -rf clover_hapin_mixed_arabic_cyrillic.schema-build-$ver.zip
zip -5 clover_hapin_mixed_arabic_cyrillic.schema-$ver.zip *.yaml ../opencc/*
# zip -5 clover_hapin_mixed_arabic_cyrillic.schema-build-$ver.zip *.yaml ../opencc/* ../build/*
