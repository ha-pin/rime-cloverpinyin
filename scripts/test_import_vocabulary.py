import tempfile
import unittest
from pathlib import Path

from import_vocabulary import ARABIC, CYRILLIC, ROOT, RULES_VERSION, codes, encode, generate


class VocabularyTests(unittest.TestCase):
    def test_existing_basic_keys(self):
        for filename, table in (("hapin_arabic_basic", ARABIC), ("hapin_cyrillic_basic", CYRILLIC)):
            body = (ROOT / "src" / f"{filename}.dict.yaml").read_text(encoding="utf-8").split("...", 1)[1]
            entries = {tuple(line.split("\t")[:2]) for line in body.splitlines() if "\t" in line}
            for letter, key in table.items():
                self.assertIn((letter, "u" + key), entries)

    def test_shared_prefix_and_vowels(self):
        self.assertEqual(codes("قازاق", "kazakh_arabic", "u"), {"uqazaq"})
        self.assertEqual(codes("سالام", "kyrgyz_arabic", "u"), {"usalam"})
        self.assertEqual(codes("ٴسالەم", "kazakh_arabic", "u"), {"usxalyem", "usalyem"})
        self.assertEqual(codes("әөүі", "kazakh_cyrillic", "v"), {"vxaxoxuxe", "vaoue"})
        self.assertEqual(codes("ۅۉئ", "kyrgyz_arabic", "u"), {"uxoxuxe", "uoue"})
        self.assertEqual(codes("ъаьә", "kazakh_cyrillic", "u"), {"uxxaxyxa", "uxxaxya"})
        with self.assertRaises(ValueError):
            encode("abc", "kazakh_arabic")

    def test_full_import_coverage_and_deduplication(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            report = generate(ROOT / "vocabulary", output)
            self.assertEqual(report["hapin_arabic_desktop"]["unique_words"], 123184)
            self.assertEqual(report["hapin_arabic_desktop"]["excluded_nonwords"], ["ــ"])
            for name, item in report.items():
                self.assertEqual(item["unique_words"], item["encoded_words"])
                self.assertEqual(item["rules_version"], RULES_VERSION)
                body = (output / f"{name}.dict.yaml").read_text(encoding="utf-8").split("...\n", 1)[1]
                rows = [line.split("\t") for line in body.splitlines()]
                pairs = {(word, code) for word, code, weight in rows}
                self.assertEqual(len(pairs), len(rows))
                self.assertTrue(all(code.isascii() and code.isalpha() and code.startswith(item["prefix"])
                                    for word, code, weight in rows))
            merged = (output / "hapin_arabic_desktop.dict.yaml").read_text(encoding="utf-8")
            for language in ("kazakh_arabic", "kyrgyz_arabic"):
                words = (ROOT / "vocabulary" / f"{language}.txt").read_text(encoding="utf-8").splitlines()
                outputs = {line.split("\t")[0] for line in merged.splitlines() if "\t" in line}
                self.assertTrue(set(words) - {"ــ"} <= outputs)
            self.assertFalse((output / "kyrgyz_arabic_desktop.dict.yaml").exists())


if __name__ == "__main__":
    unittest.main()
