import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from prepare_publish import VARIANTS, prepare


class PublishTests(unittest.TestCase):
    def fixtures(self, source, extra=None):
        for variant in VARIANTS:
            with ZipFile(source / f"clover_{variant}.schema-2.zip", "w") as archive:
                archive.writestr(f"clover_{variant}.schema.yaml", "schema: {}")
                archive.writestr("opencc/emoji.json", "{}")
                if extra:
                    archive.writestr(extra, "source")

    def test_stages_only_expected_archives(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp)
            self.fixtures(source)
            (source / "README.md").write_text("source")
            (source / "unexpected.zip").write_text("source")
            output = source / "dist"
            prepare(source, output, "2")
            prepare(source, output, "2")
            self.assertEqual({p.name for p in output.iterdir()},
                             {f"clover_{variant}.schema-2.zip" for variant in VARIANTS})

    def test_rejects_source_and_unsafe_members(self):
        for extra in ("README.md", "src/build.sh", "../escape.yaml"):
            with self.subTest(extra=extra), tempfile.TemporaryDirectory() as tmp:
                source = Path(tmp)
                self.fixtures(source, extra)
                with self.assertRaises(ValueError):
                    prepare(source, source / "dist", "2")
                self.assertFalse((source / "dist").exists())

    def test_rejects_dirty_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp)
            self.fixtures(source)
            output = source / "dist"
            output.mkdir()
            (output / "README.md").write_text("source")
            with self.assertRaises(ValueError):
                prepare(source, output, "2")


if __name__ == "__main__":
    unittest.main()
