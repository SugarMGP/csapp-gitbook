"""Validate the actual site configuration and the Markdown consumed by GitBook."""

import json
import re
import unittest
from pathlib import Path

import jsonschema
import yaml
from sync import normalize_headings, rewrite_links

ROOT = Path(__file__).resolve().parents[1]


class GitBookTests(unittest.TestCase):
    def test_moving_openings_rebases_links_and_preserves_code(self):
        source = ROOT / "book/chapter/section/opening.md"
        destination = ROOT / "book/chapter/README.md"
        text = '[Next](next.md)\n![Figure](assets/figure.png)\n```c\nchar *example = "[literal](next.md)";\n```\n'
        moves = {(source.parent / "next.md").resolve(): destination.parent / "other.md"}
        expected = '[Next](other.md)\n![Figure](section/assets/figure.png)\n```c\nchar *example = "[literal](next.md)";\n```\n'
        self.assertEqual(rewrite_links(text, source, destination, moves), expected)

    def test_continuous_chapters_are_removed(self):
        self.assertEqual(list((ROOT / "book").rglob("chapter.md")), [])
        summary = (ROOT / "book/SUMMARY.md").read_text(encoding="utf-8")
        self.assertNotIn("整章", summary)

    def test_opening_content_is_merged_into_chapter_landings(self):
        manifest = json.loads((ROOT / "book-manifest.json").read_text(encoding="utf-8"))
        openings = [entry for entry in manifest["files"]
                    if entry["source"].endswith(("-chapter-opening.md", "A.0-error-handling.md"))]
        self.assertEqual(len(openings), 13)
        for entry in openings:
            self.assertTrue(entry["target"].endswith("/README.md"), entry["source"])
            self.assertFalse((ROOT / "book" / entry["source"]).exists())
        first = next((ROOT / "book").glob("第01章-*/README.md")).read_text(encoding="utf-8")
        self.assertIn("计算机系统是由硬件和系统软件组成的", first)
        second = next((ROOT / "book").glob("第02章-*/README.md")).read_text(encoding="utf-8")
        self.assertIn("2.1/assets/fig-2-1-gcc-c-versions.jpg", second)

    def test_heading_normalization_preserves_code(self):
        source = "### Page\n\nText.\n\n#### Detail\n\n```c\n#define VALUE 1\n```\n"
        self.assertEqual(normalize_headings(source), "# Page\n\nText.\n\n## Detail\n\n```c\n#define VALUE 1\n```\n")

    def test_site_configuration_and_content_mapping(self):
        site = yaml.safe_load((ROOT / "gitbook-docs.yaml").read_text(encoding="utf-8"))
        schema = yaml.safe_load((ROOT / "schemas/gitbook-docs.schema.yaml").read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.Draft202012Validator(schema).validate(site)
        spaces = site["site"]["structure"]
        self.assertEqual(len(spaces), 1)
        self.assertEqual(spaces[0]["type"], "space")
        self.assertIs(spaces[0]["default"], True)
        self.assertEqual(spaces[0]["content"]["language"], "zh")
        directory = ROOT / spaces[0]["content"]["directory"]
        config = yaml.safe_load((directory / ".gitbook.yaml").read_text(encoding="utf-8"))
        content = (directory / config["root"]).resolve()
        self.assertEqual(content, (ROOT / "book").resolve())
        for name in ("readme", "summary"):
            self.assertTrue((content / config["structure"][name]).is_file())

    def test_pages_start_with_a_level_one_title(self):
        wrong = []
        for path in (ROOT / "book").rglob("*.md"):
            heading = re.search(r"^(#{1,6}) ", path.read_text(encoding="utf-8-sig"), re.M)
            if not heading or heading[1] != "#":
                wrong.append(path.relative_to(ROOT).as_posix())
        self.assertFalse(wrong, f"{len(wrong)} pages lack an H1 title: {wrong[:5]}")

    def test_navigation_titles_and_groups(self):
        summary = (ROOT / "book/SUMMARY.md").read_text(encoding="utf-8")
        for label, ref in re.findall(r'^\s*\* \[([^\]]+)\]\(([^)\s]+)(?: "[^"]*")?\)$', summary, re.M):
            title = re.search(r"^# (.+)$", (ROOT / "book" / ref).read_text(encoding="utf-8-sig"), re.M)[1]
            self.assertEqual(label, title, ref)
        self.assertIn("## 附录\n", summary)


if __name__ == "__main__":
    unittest.main()
