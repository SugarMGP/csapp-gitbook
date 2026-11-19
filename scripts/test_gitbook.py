"""Validate the actual site configuration and the Markdown consumed by GitBook."""

import json
import re
import unittest
from pathlib import Path

import jsonschema
import yaml
from sync import (disable_processor_table_search, group_answers, native_code_titles,
                  native_figures, native_images, native_math, normalize_headings,
                  outside_fences, rewrite_links)

ROOT = Path(__file__).resolve().parents[1]


class GitBookTests(unittest.TestCase):
    def test_part_introductions_are_not_chapter_subpages(self):
        manifest = json.loads((ROOT / "book-manifest.json").read_text(encoding="utf-8"))
        parts = [entry for entry in manifest["files"] if re.search(r"-part-\d+\.md$", entry["source"])]
        self.assertEqual(len(parts), 3)
        for entry in parts:
            self.assertTrue(entry["target"].endswith("/README.md"), entry["source"])
            self.assertFalse((ROOT / "book" / entry["source"]).exists())
            landing = (ROOT / "book" / entry["target"]).read_text(encoding="utf-8")
            self.assertRegex(landing, r"(?m)^## 第[一二三]+部分")
        summary = (ROOT / "book/SUMMARY.md").read_text(encoding="utf-8")
        self.assertNotRegex(summary, r"(?m)^\s+\* \[第[一二三]+部分")
        tenth = next((ROOT / "book").glob("第10章-*/README.md")).read_text(encoding="utf-8")
        self.assertIn("\n  - [10.5.1 ", tenth)
        self.assertNotIn("10.0-part-3.md", tenth)

    def test_numbered_sections_have_the_correct_parent(self):
        chapter, section = None, None
        summary = (ROOT / "book/SUMMARY.md").read_text(encoding="utf-8")
        for indent, label in re.findall(r"^( *)\* \[([^\]]+)\]", summary, re.M):
            if not indent:
                parent = re.match(r"第 (\d+) 章", label)
                chapter, section = int(parent[1]) if parent else None, None
                continue
            number = re.match(r"(\d+)\.(\d+)(?:\.(\d+))? ", label)
            if number and chapter is not None:
                self.assertEqual(int(number[1]), chapter, label)
                if number[3]:
                    self.assertEqual((number[1], number[2]), section, label)
                    self.assertEqual(len(indent), 4, label)
                else:
                    section = (number[1], number[2])
                    self.assertEqual(len(indent), 2, label)

    def test_chapters_belong_to_the_correct_part(self):
        group = None
        for line in (ROOT / "book/SUMMARY.md").read_text(encoding="utf-8").splitlines():
            if line.startswith("## "):
                group = line[3:]
            chapter = re.match(r"^\* \[第 (\d+) 章", line)
            if chapter:
                number = int(chapter[1])
                if number == 1:
                    expected = None
                elif number <= 6:
                    expected = "第一部分"
                elif number <= 9:
                    expected = "第二部分"
                else:
                    expected = "第三部分"
                self.assertEqual(group.split(" · ")[0] if group else None, expected)

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

    def test_native_figures_keep_only_the_text_caption(self):
        source = "![高速缓存存储器](assets/cache.png)\n\n**图 1-8** 高速缓存存储器\n"
        rendered = native_figures(source)
        self.assertIn('<figure><img src="assets/cache.png" alt="高速缓存存储器">', rendered)
        self.assertIn("</figure>\n\n**图 1-8** 高速缓存存储器", rendered)
        self.assertNotIn("<figcaption>", rendered)
        self.assertNotIn("![", rendered)
        for path in (ROOT / "book").rglob("*.md"):
            text = path.read_text(encoding="utf-8-sig")
            self.assertNotRegex(text, r"(?m)^!\[[^]]+\]\([^)]+\)\n\n\*\*图")

    def test_all_image_captions_are_hidden_but_alt_text_is_preserved(self):
        source = "![向量的抽象数据类型](assets/vector.jpg)\n"
        self.assertEqual(native_images(source),
                         '<figure><img src="assets/vector.jpg" alt="向量的抽象数据类型"></figure>\n')
        for path in (ROOT / "book").rglob("*.md"):
            text = path.read_text(encoding="utf-8-sig")
            self.assertNotIn("<figcaption>", text)
            self.assertNotRegex(text, r"(?m)^!\[[^]]+\]\(")

    def test_file_labels_become_native_code_titles(self):
        source = "`code/intro/hello.c`\n\n```c\nint main(void) {}\n```\n"
        rendered = native_code_titles(source)
        self.assertIn('{% code title="code/intro/hello.c" %}', rendered)
        self.assertIn("```c\nint main(void) {}\n```", rendered)
        self.assertIn("{% endcode %}", rendered)
        chapter = next((ROOT / "book").glob("第01章-*/README.md")).read_text(encoding="utf-8")
        self.assertIn('{% code title="code/intro/hello.c" %}', chapter)

    def test_processor_table_disables_native_search(self):
        source = ("| 阶段 | `OPq rA, rB` | `rrmovq rA, rB` | `irmovq V, rB` |\n"
                  "|---|---|---|---|\n| 取指 | `A` | `B` | `C` |\n")
        rendered = disable_processor_table_search(source)
        self.assertIn('<table data-search="false">', rendered)
        self.assertIn("<th>阶段</th>", rendered)
        self.assertIn("<td><code>A</code></td>", rendered)
        processor = next((ROOT / "book").glob("第04章-*/4.3/4.3.1-*.md")).read_text(encoding="utf-8")
        self.assertIn('<table data-search="false">', processor)

    def test_native_math_replaces_standalone_formula_quotes(self):
        source = "说明。\n\n> S<sub>p</sub> = T<sub>1</sub> / T<sub>p</sub>\n\n下文。\n"
        self.assertIn("$$\nS_{p} = T_{1} / T_{p}\n$$", native_math(source))
        product = "> x *<sup>u</sup><sub>w</sub> y = (x · y) mod 2<sup>w</sup>\n"
        self.assertIn("x *^{u}_{w} y", native_math(product))
        derivation = ("> (x' · y') mod 2<sup>w</sup>\n>\n"
                      "> = (x · y) mod 2<sup>w</sup>　（2.18）\n")
        self.assertIn("\\begin{gathered}", native_math(derivation))
        self.assertIn("\\tag{2.18}", native_math(derivation))
        tagged = "> x = 1　（2.1）\n>\n> y = 2　（2.2）\n"
        self.assertEqual(native_math(tagged).count("$$"), 4)
        note = "> ① 1ns = 10<sup>-9</sup>s。\n"
        self.assertEqual(native_math(note), note)
        parallelism = next((ROOT / "book").glob("第12章-*/12.6/12.6-*.md")).read_text(encoding="utf-8")
        self.assertIn("$$\nS_{p} =", parallelism)

    def test_long_answer_pages_are_grouped(self):
        answers = next((ROOT / "book").glob("第02章-*/练习题答案.md")).read_text(encoding="utf-8")
        self.assertIn("## 练习题 2.1～2.10", answers)
        self.assertIn("**练习题 2.1**", answers)
        self.assertNotRegex(answers, r"(?m)^### 练习题")
        self.assertEqual(group_answers("# 练习题答案\n\n## 练习题 1.1\n"),
                         "# 练习题答案\n\n## 练习题 1.1\n")

    def test_lab_index_uses_native_cards_and_files(self):
        labs = (ROOT / "book/实验/README.md").read_text(encoding="utf-8")
        self.assertIn('<table data-view="cards">', labs)
        self.assertEqual(labs.count("{% file src="), 8)

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
            visible = []
            outside_fences(path.read_text(encoding="utf-8-sig"), lambda line: visible.append(line) or line)
            headings = re.findall(r"^(#{1,6}) ", "".join(visible), re.M)
            if not headings or headings[0] != "#" or headings.count("#") != 1:
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
