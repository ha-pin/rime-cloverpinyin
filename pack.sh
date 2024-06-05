#!/usr/bin/env bash
set -e

ver="$1"

cd ./rime-cloverpinyin/data
rm -rf clover_hapin_arabic.schema-$ver.zip
rm -rf clover_hapin_arabic.schema-build-$ver.zip
zip -5 clover_hapin_arabic.schema-$ver.zip *.yaml opencc/*
zip -5 clover_hapin_arabic.schema-build-$ver.zip *.yaml opencc/* build/*

