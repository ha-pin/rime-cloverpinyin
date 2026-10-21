#!/usr/bin/env python3
"""Check release directories before shipping them to a Rime client."""
import json
import sys
from pathlib import Path

import yaml

RULES_VERSION = (Path(__file__).resolve().parents[1] / "VERSION").read_text(encoding="utf-8").strip()

def dictionary_header(path):
    lines = []
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            lines.append(line)
            if line.strip() == "...":
                return yaml.safe_load("".join(lines))
    raise ValueError(f"{path}: 缺少词典头结束标记 ...")


def validate(package):
    schemas = list(package.glob("*.schema.yaml"))
    if len(schemas) != 1:
        raise ValueError(f"{package}: 应包含一个方案文件")
    schema_path = schemas[0]
    schema = yaml.safe_load(schema_path.read_text(encoding="utf-8"))
    schema_id = schema["schema"]["schema_id"]
    if str(schema["schema"]["version"]) != RULES_VERSION:
        raise ValueError(f"{schema_path}: 方案版本应为 {RULES_VERSION}")
    if schema_path.name != f"{schema_id}.schema.yaml":
        raise ValueError(f"{schema_path}: schema_id 与文件名不一致")
    for dependency in schema["schema"].get("dependencies", []):
        if not (package / f"{dependency}.schema.yaml").is_file():
            raise ValueError(f"{package}: 缺少方案依赖 {dependency}")

    pending = [schema["translator"]["dictionary"]]
    visited = set()
    while pending:
        name = pending.pop()
        if name in visited:
            continue
        visited.add(name)
        path = package / f"{name}.dict.yaml"
        header = dictionary_header(path)
        if header["name"] != name:
            raise ValueError(f"{path}: name 应为 {name}")
        if str(header["version"]) != RULES_VERSION:
            raise ValueError(f"{path}: 词典版本应为 {RULES_VERSION}")
        pending.extend(header.get("import_tables", []))

    def check_opencc(value):
        if isinstance(value, dict):
            if "file" in value and not (package / "opencc" / value["file"]).is_file():
                raise ValueError(f"{package}: 缺少 OpenCC 文件 {value['file']}")
            for child in value.values():
                check_opencc(child)
        elif isinstance(value, list):
            for child in value:
                check_opencc(child)

    for section in ("emoji_suggestion", "symbol_support"):
        path = package / "opencc" / schema[section]["opencc_config"]
        check_opencc(json.loads(path.read_text(encoding="utf-8")))
    if not (package / "clover_hapin.key_bindings.yaml").is_file():
        raise ValueError(f"{package}: 缺少快捷键配置")
    print(f"通过: {schema_id} ({len(visited)} 个词典)")


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "data"
    for variant in ("hapin_arabic", "hapin_cyrillic", "hapin_mixed_arabic_cyrillic"):
        validate(root / variant)


if __name__ == "__main__":
    main()
