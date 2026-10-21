#!/usr/bin/env python3
"""Stage only the three validated schema ZIPs for Pages, artifacts and Release."""
import argparse
import shutil
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
VARIANTS = ("hapin_arabic", "hapin_cyrillic", "hapin_mixed_arabic_cyrillic")


def prepare(source, output, version):
    if not version.isascii() or not version.isdigit():
        raise ValueError("规则版本必须是整数")
    names = [f"clover_{variant}.schema-{version}.zip" for variant in VARIANTS]
    if source.resolve() == output.resolve():
        raise ValueError("发布目录必须独立于构建目录")
    if output.exists() and any(p.name not in names or not p.is_file() for p in output.iterdir()):
        raise ValueError(f"{output}: 包含非发布产物，请使用独立的空目录")
    for variant, name in zip(VARIANTS, names):
        with ZipFile(source / name) as archive:
            if archive.testzip() is not None:
                raise ValueError(f"{name}: ZIP 校验失败")
            members = archive.namelist()
            for member in members:
                path = PurePosixPath(member)
                root_yaml = len(path.parts) == 1 and path.suffix == ".yaml"
                opencc = len(path.parts) == 2 and path.parts[0] == "opencc" and path.suffix in {".json", ".txt"}
                if path.is_absolute() or ".." in path.parts or not (root_yaml or opencc):
                    raise ValueError(f"{name}: 含非方案文件 {member}")
            if f"clover_{variant}.schema.yaml" not in members:
                raise ValueError(f"{name}: 缺少对应方案文件")
    output.mkdir(parents=True, exist_ok=True)
    for name in names:
        shutil.copyfile(source / name, output / name)
    print(f"发布目录 {output}: 仅包含 {len(names)} 个方案 ZIP")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "data")
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    prepare(args.source, args.output, (ROOT / "VERSION").read_text().strip())
