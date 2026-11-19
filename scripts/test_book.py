"""Check the real imported book, rather than a duplicate implementation of the importer."""

import hashlib
import json
import re
import tarfile
import unittest
from pathlib import Path
from urllib.parse import unquote
from check_book import references

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book"


class BookTests(unittest.TestCase):
    def test_lab_packages_match_upstream_checksums(self):
        packages = (BOOK / "实验/PACKAGES.md").read_text(encoding="utf-8")
        hashes = re.findall(r"^([a-f0-9]{64})  (.+)$", packages, re.M)
        self.assertEqual(len(hashes), 8)
        for digest, filename in hashes:
            path = BOOK / "实验" / filename
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), digest)
            with tarfile.open(path) as archive:
                self.assertTrue(archive.getmembers())
                for member in archive:
                    if member.isfile():
                        with archive.extractfile(member) as data:
                            while data.read(1024 * 1024):
                                pass

    def test_imported_files_match_manifest(self):
        manifest = json.loads((ROOT / "book-manifest.json").read_text(encoding="utf-8"))
        paths = [entry["target"] for entry in manifest["files"]]
        self.assertEqual(paths, sorted(paths))
        self.assertEqual(manifest["sources"], json.loads((ROOT / "sources.json").read_text(encoding="utf-8")))
        for entry in manifest["files"]:
            with self.subTest(path=entry["target"]):
                self.assertEqual(hashlib.sha256((BOOK / entry["target"]).read_bytes()).hexdigest(), entry["output_sha256"])
                if not entry["target"].endswith(".md"):
                    self.assertEqual(entry["sha256"], entry["output_sha256"])

    def test_summary_covers_all_sections_answers_and_labs(self):
        summary = (BOOK / "SUMMARY.md").read_text(encoding="utf-8")
        refs = list(references(summary))
        self.assertEqual(len(refs), len(set(refs)))
        for ref in refs:
            self.assertTrue((BOOK / unquote(ref)).is_file(), ref)
        self.assertEqual(len(list(BOOK.glob("第*章-*"))), 12)
        answers = list(BOOK.glob("第*章-*/练习题答案.md"))
        self.assertEqual(len(answers), 12)
        self.assertGreaterEqual(sum(len(re.findall(r"^## 练习题 \d+\.\d+", p.read_text(encoding="utf-8"), re.M)) for p in answers), 238)
        expected = {p.relative_to(BOOK).as_posix() for p in BOOK.rglob("*.md")
                    if p.name not in {"chapter.md", "README.md", "SUMMARY.md", "UPSTREAM.md"}}
        self.assertTrue(expected <= set(refs), f"Not in summary: {expected - set(refs)}")
        self.assertEqual(len(list((BOOK / "实验").rglob("*.tar"))), 8)
        self.assertLess(summary.index("实验/datalab-zh/datalab-zh.md"), summary.index("实验/archlab-zh/archlab-zh.md"))
        self.assertTrue((BOOK / "supplements/assets/perflab-handout.tar").is_file())


if __name__ == "__main__":
    unittest.main()
