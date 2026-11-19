"""Rebuild book/ from pinned upstream snapshots; --update selects newer commits."""

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlsplit, urlunsplit

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book"
LINK = re.compile(r"^- \[([^\]]+)\]\(([^)]+)\)$", re.M)
TABLE_MARKDOWN = MarkdownIt("commonmark", {"html": True}).enable("table")
SUPPLEMENTS = {
    "labs/labs-overview/common-problems.md": "faq.md",
    "labs/data-lab/readme-student.md": "data-lab-student.md",
    "labs/data-lab/readme-instructor.md": "data-lab-instructor.md",
    "labs/bomb-lab/readme-jiang-shi-ban.md": "bomb-lab-instructor.md",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--update", action="store_true")
    args = parser.parse_args()
    sources = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))
    paths = {name: checkout(name, source, args.update) for name, source in sources.items()}
    generate(paths, sources)
    (ROOT / "sources.json").write_text(
        json.dumps(sources, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )


def checkout(name, source, update):
    path = ROOT / ".cache" / name
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "-c", "core.autocrlf=false", "clone", "--no-checkout", "--depth", "1", source["url"], str(path)], check=True)
    ref = source["branch"] if update else source["commit"]
    subprocess.run(["git", "-C", str(path), "fetch", "--depth", "1", "origin", ref], check=True)
    subprocess.run(["git", "-c", "core.autocrlf=false", "-C", str(path), "checkout", "--detach", "--force", "FETCH_HEAD"], check=True)
    source["commit"] = subprocess.check_output(
        ["git", "-C", str(path), "rev-parse", "HEAD"], text=True
    ).strip()
    return path


def generate(paths, sources):
    sunny, hans = paths["sunnymaria"], paths["hansimov"]
    directories = [sunny / "前言", *sorted(sunny.glob("第*章-*")), sunny / "附录A-错误处理", sunny / "实验"]
    if len(directories) != 15 or not all((d / "README.md").is_file() for d in directories):
        raise ValueError("Upstream chapter structure changed; review the importer before updating")
    if BOOK.exists():
        shutil.rmtree(BOOK)
    BOOK.mkdir()
    imported = []
    relocations = {}

    def copy(source, target, upstream):
        dest = BOOK / target
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, dest)
        imported.append({"upstream": upstream, "source": source.relative_to(paths[upstream]).as_posix(),
                         "target": target.as_posix(), "sha256": hashlib.sha256(source.read_bytes()).hexdigest()})

    summary = ["# 目录", "", "* [开始阅读](README.md)"]
    for directory in directories:
        if directory.name.startswith("第"):
            part = {"02": "第一部分 · 程序结构和执行", "07": "第二部分 · 在系统上运行程序", "10": "第三部分 · 程序间的交互和通信"}.get(directory.name[1:3])
            if part:
                summary.extend(["", f"## {part}", ""])
        elif directory.name == "实验":
            summary.extend(["", "## 实验与补充资料", ""])
        elif directory.name.startswith("附录"):
            summary.extend(["", "## 附录", ""])
        for path in sorted(directory.rglob("*")):
            if path.is_file() and path.name != "chapter.md":
                copy(path, path.relative_to(sunny), "sunnymaria")
        index = (directory / "README.md").read_text(encoding="utf-8-sig")
        title = re.search(r"^# (.+)$", index, re.M)[1]
        summary.append(f"* [{title}]({directory.name}/README.md)")
        if directory.name == "实验":
            lab_refs = list(dict.fromkeys(re.findall(r"\]\(([^)]+\.md)\)", index)))
            lab_refs.extend(p.relative_to(directory).as_posix()
                            for p in sorted(directory.rglob("*.md"), key=lambda p: p.as_posix())
                            if p.name != "README.md" and p.relative_to(directory).as_posix() not in lab_refs)
            refs = [(re.search(r"^# (.+)$", (directory / ref).read_text(encoding="utf-8-sig"), re.M)[1], ref)
                    for ref in lab_refs]
        else:
            section = index.split("## 小节目录", 1)[1].split("\n## ", 1)[0]
            refs = LINK.findall(section)
            landing = BOOK / directory.name / "README.md"
            chunks = [f"# {title}"]
            part_openings = [ref for label, ref in refs if re.match(r"第[一二三四五六七八九十]+部分", label)]
            openings = [ref for label, ref in refs if label == title] + part_openings
            for ref in openings:
                opening = BOOK / directory.name / ref
                body = normalize_headings(opening.read_text(encoding="utf-8-sig"))
                if ref in part_openings:
                    body = re.sub(r"^# ", "## ", body, count=1)
                else:
                    body = body.split("\n", 1)[1]
                chunks.append(rewrite_links(body.strip(), opening, landing, relocations))
                relocations[opening.resolve()] = landing.resolve()
                original_target = opening.relative_to(BOOK).as_posix()
                for entry in imported:
                    if entry["target"] == original_target:
                        entry["target"] = landing.relative_to(BOOK).as_posix()
                opening.unlink()
            refs = [(label, ref) for label, ref in refs if ref not in openings]
            toc = ["  " * (section_depth(label) - 1) + f"- [{label}]({ref})" for label, ref in refs]
            chunks.extend(["## 小节目录", "\n".join(toc)])
            if (directory / "练习题答案.md").exists():
                chunks.extend(["## 练习题答案", "[查看本章练习题答案](练习题答案.md)"])
            landing.write_text("\n\n".join(chunks) + "\n", encoding="utf-8", newline="\n")
        for label, ref in refs:
            depth = section_depth(label)
            summary.append("  " * depth + f"* [{label}]({directory.name}/{ref})")
        if (directory / "练习题答案.md").exists():
            summary.append(f"  * [练习题答案]({directory.name}/练习题答案.md)")
    for name in ["参考文献.md", "答案编校说明.md"]:
        copy(sunny / name, Path(name), "sunnymaria")
    for original, target in SUPPLEMENTS.items():
        copy(hans / original, Path("supplements") / target, "hansimov")
    for filename in ["code.tar", "code-all.tar"]:
        copy(hans / "_codes" / filename, Path("supplements/assets") / filename, "hansimov")
    for filename in ["perflab-handout.tar", "perflab.pdf", "README-perflab.txt"]:
        copy(hans / "_labs/06 perf lab" / filename, Path("supplements/assets") / filename, "hansimov")
    copy(hans / "labs/perf-lab.md", Path("supplements/performance-lab.md"), "hansimov")
    perf = BOOK / "supplements/performance-lab.md"
    text = perf.read_text(encoding="utf-8-sig")
    for old, new in [("README-perflab", "README-perflab.txt"), ("perflab.pdf", "perflab.pdf"), ("perflab-handout.tar", "perflab-handout.tar")]:
        text = text.replace(f"](http://csapp.cs.cmu.edu/3e/{old})", f"](assets/{new})")
    perf.write_text(text, encoding="utf-8", newline="\n")
    shutil.copyfile(ROOT / "templates/README.md", BOOK / "README.md")
    shutil.copyfile(ROOT / "templates/labs.md", BOOK / "实验/README.md")
    shutil.copyfile(ROOT / "templates/supplements.md", BOOK / "supplements/README.md")
    shutil.copyfile(ROOT / "templates/.gitbook.yaml", BOOK / ".gitbook.yaml")
    summary.extend(["* [补充资料](supplements/README.md)",
                    "  * [Performance Lab](supplements/performance-lab.md)",
                    "  * [实验常见问题](supplements/faq.md)",
                    "  * [Data Lab 学生版](supplements/data-lab-student.md)",
                    "  * [Data Lab 讲师版](supplements/data-lab-instructor.md)",
                    "  * [Bomb Lab 讲师版](supplements/bomb-lab-instructor.md)",
                    "", "## 参考资料", "",
                    "* [参考文献](参考文献.md)", "* [答案编校说明](答案编校说明.md)",
                    "* [资料来源与权利归属](SOURCES.md)"])
    credits = ["# 资料来源与权利归属", "", "本项目整合已有中文资料，通过 Git Sync 导入 GitBook，使用 GitBook 官方默认主题阅读。", ""]
    for name, source in sources.items():
        url = source["url"].removesuffix(".git")
        credits.append(f"- [{name}]({url})：固定版本 [`{source['commit'][:12]}`]({url}/tree/{source['commit']})")
    credits.extend(["", "SunnyMaria 提供第 1—12 章、前言、附录 A、参考文献、原书练习题答案和八个实验资料；其 OCR 基础来自 Hansimov。Hansimov 另提供此站收录的实验 FAQ、Data/Bomb Lab 补充说明、Performance Lab 和示例代码包。", "",
                    "原书作者为 Randal E. Bryant 与 David R. O’Hallaron，原书由 Pearson 出版。中文译者及各资料贡献者保有其相应权利。两上游仓库均未提供 LICENSE；本项目不授予书籍正文、译文、图片或实验材料的额外使用许可。公开可访问不等于获得转载授权。", "",
                    "本项目的“完整”指上述仓库现有的十二章和附属资料均已纳入阅读目录，不代表已经逐字核对正式出版物；不包含自行编写的家庭作业解答、实验解答或讲师专用材料。发现 OCR 或排印疑点请结合正版教材、[官方勘误](https://csapp.cs.cmu.edu/3e/errata.html)及[上游答案编校说明](答案编校说明.md)核对。", "",
                    "自动更新只生成待审查的 Pull Request，不直接把新上游内容合并到主分支。", ""])
    (BOOK / "SOURCES.md").write_text("\n".join(credits), encoding="utf-8", newline="\n")
    for path in BOOK.rglob("*.md"):
        original = path.read_text(encoding="utf-8-sig")
        normalized = normalize_headings(rewrite_links(original, path, path, relocations))
        normalized = native_figures(normalized)
        normalized = native_images(normalized)
        normalized = native_code_titles(normalized)
        normalized = disable_table_search(normalized)
        normalized = native_math(normalized)
        if path.name == "练习题答案.md":
            normalized = group_answers(normalized)
        if normalized != original:
            path.write_text(normalized, encoding="utf-8", newline="\n")
    for i, line in enumerate(summary):
        link = re.match(r"^(\s*)\* \[([^\]]+)\]\(([^)]+)\)$", line)
        if link:
            indent, label, ref = link.groups()
            title = re.search(r"^# (.+)$", (BOOK / ref).read_text(encoding="utf-8-sig"), re.M)[1]
            navigation = " " + json.dumps(label, ensure_ascii=False) if label != title else ""
            summary[i] = f"{indent}* [{title}]({ref}{navigation})"
    (BOOK / "SUMMARY.md").write_text("\n".join(summary) + "\n", encoding="utf-8", newline="\n")
    for entry in imported:
        entry["output_sha256"] = hashlib.sha256((BOOK / entry["target"]).read_bytes()).hexdigest()
    manifest = {"sources": sources, "files": sorted(imported, key=lambda entry: (entry["target"], entry["source"]))}
    (ROOT / "book-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Imported {len(imported)} source files; generated {len(list(BOOK.rglob('*.md')))} Markdown pages")


def section_depth(title):
    number = re.match(r"\d+(?:\.\d+)+", title)
    return len(number[0].split(".")) - 1 if number else 1


def normalize_headings(text):
    first = re.search(r"^(#{1,6}) ", text, re.M)
    if not first or len(first[1]) == 1:
        return text
    offset = 1 - len(first[1])
    return outside_fences(text, lambda line: re.sub(
        r"^(#{1,6})(?= )", lambda match: "#" * max(1, len(match[1]) + offset), line))


def native_figures(text):
    pattern = re.compile(r"^!\[([^]\n]*)\]\(([^)\n]+)\)\n\n(\*\*图\s*[^\n]+)$", re.M)

    def replace(match):
        alt, source, caption = match.groups()
        return (f'<figure><img src="{html.escape(source, quote=True)}" '
                f'alt="{html.escape(alt, quote=True)}"></figure>\n\n{caption}')

    return pattern.sub(replace, text)


def native_images(text):
    pattern = re.compile(r"^!\[([^]\n]*)\]\(([^)\n]+)\)$", re.M)
    return pattern.sub(lambda match: (
        f'<figure><img src="{html.escape(match[2], quote=True)}" '
        f'alt="{html.escape(match[1], quote=True)}"></figure>'), text)


def native_code_titles(text):
    pattern = re.compile(
        r"^`([^`\n]+)`\n\n(?P<fence>`{3,}|~{3,})([^\n]*)\n(.*?)^(?P=fence)[ \t]*$",
        re.M | re.S,
    )

    def replace(match):
        title, fence, language, body = match[1], match[2], match[3], match[4]
        block = f"{fence}{language}\n{body}{fence}"
        return f'{{% code title="{html.escape(title, quote=True)}" %}}\n\n{block}\n\n{{% endcode %}}'

    return pattern.sub(replace, text)


def disable_table_search(text):
    lines = text.splitlines()
    result = []
    index = 0
    fence = None
    separator = re.compile(r"^\|(?:\s*:?-{3,}:?\s*\|)+$")
    while index < len(lines):
        line = lines[index]
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            if fence is None:
                fence = marker[1]
            elif marker[1][0] == fence[0] and len(marker[1]) >= len(fence):
                fence = None
            result.append(line)
            index += 1
            continue
        prefix = "> " if line.startswith("> ") else ""
        body = line[len(prefix):]
        next_body = lines[index + 1][len(prefix):] if index + 1 < len(lines) and lines[index + 1].startswith(prefix) else ""
        if (fence is None and body.startswith("|") and body.endswith("|")
                and separator.fullmatch(next_body)):
            end = index + 2
            while end < len(lines) and lines[end].startswith(prefix + "|") and lines[end].endswith("|"):
                end += 1
            if prefix and result and result[-1] == ">":
                result.pop()
            if prefix and result and result[-1] != "":
                result.append("")
            table_lines = [item[len(prefix):] for item in lines[index:end]]
            rendered = TABLE_MARKDOWN.render("\n".join(table_lines) + "\n").strip()
            rendered = rendered.replace("<table>", '<table data-search="false">', 1)
            result.extend(rendered.splitlines())
            if prefix and end < len(lines) and lines[end] == ">":
                end += 1
            if prefix:
                result.append("")
            index = end
            continue
        result.append(line)
        index += 1
    converted = "\n".join(result).rstrip("\n") + ("\n" if text.endswith("\n") else "")
    return outside_fences(converted, lambda line: re.sub(
        r"<table(?![^>]*\bdata-search=)", '<table data-search="false"', line))


def native_math(text):
    lines = text.splitlines()
    result = []
    fenced = False
    index = 0
    while index < len(lines):
        line = lines[index]
        if re.match(r"^\s*(`{3,}|~{3,})", line):
            fenced = not fenced
        if fenced or not line.startswith(">"):
            result.append(line)
            index += 1
            continue
        end = index
        while end < len(lines) and lines[end].startswith(">"):
            end += 1
        block = lines[index:end]
        bodies = [item[2:] if item.startswith("> ") else item[1:] for item in block]
        formulas = [item for item in bodies if item.strip()]
        is_formula = (formulas
                      and sum(len(re.findall(r"[\u4e00-\u9fff]", item)) for item in formulas) <= 4
                      and any(re.search(r"[=≈≐Σ∑]|<su[bp]>", item) for item in formulas)
                      and all(not re.search(
                          r"^[①-⑳]|。$|[`{};|]|\b(?:int|long|double|void|printf|for|while|linux>)\b", item)
                          for item in formulas))
        if not is_formula:
            result.extend(block)
            index = end
            continue
        converted = [math_to_tex(item) for item in formulas]
        if sum("\\tag{" in item for item in converted) > 1:
            for formula in converted:
                result.extend(["$$", formula, "$$"])
            index = end
            continue
        formula = converted[0] if len(converted) == 1 else (
            "\\begin{gathered}\n" + r" \\ ".join(converted) + "\n\\end{gathered}")
        result.extend(["$$", formula, "$$"])
        index = end
    return "\n".join(result) + ("\n" if text.endswith("\n") else "")


def math_to_tex(formula):
    formula = re.sub(r"\*([A-Za-z][A-Za-z0-9]*)\*", r"\1", formula)
    formula = re.sub(r"<sub>(.*?)</sub>", r"_{\1}", formula)
    formula = re.sub(r"<sup>(.*?)</sup>", r"^{\1}", formula)
    formula = re.sub(r"[　 ]*（(\d+(?:\.\d+)*)）$", r" \\tag{\1}", formula)
    formula = formula.replace("≐", r"\mathrel{:=}").replace("Σ", r"\sum").replace("∑", r"\sum")
    formula = formula.replace("·", r"\cdot ").replace("×", r"\times ").replace("≈", r"\approx ")
    formula = re.sub(r"\bmod\b", r"\\bmod", formula)
    return formula.replace("…", r"\ldots ").replace("（", "(").replace("）", ")")


def group_answers(text):
    headings = list(re.finditer(r"^## 练习题 (\d+)\.(\d+)$", text, re.M))
    if len(headings) <= 10:
        return text
    chapter = headings[0][1]
    groups = {}
    for match in headings:
        number = int(match[2])
        groups.setdefault((number - 1) // 10 * 10 + 1, []).append(number)
    for start, members in reversed(list(groups.items())):
        marker = f"## 练习题 {chapter}.{start}"
        group = f"## 练习题 {chapter}.{start}～{chapter}.{members[-1]}\n\n"
        text = text.replace(marker, group + marker, 1)
    return re.sub(r"^## (练习题 \d+\.\d+)$", r"**\1**", text, flags=re.M)


def rewrite_links(text, source, destination, relocations):
    def replace(match):
        url = urlsplit(match[2].strip("<>"))
        if url.scheme or url.netloc or not url.path:
            return match[0]
        target = (source.parent / unquote(url.path)).resolve()
        target = relocations.get(target, target)
        relative = Path(os.path.relpath(target, destination.parent)).as_posix()
        return match[1] + urlunsplit(("", "", relative, url.query, url.fragment)) + match[3]
    link = re.compile(r"(!?\[[^\]\n]*\]\()(<[^>]+>|[^)\n]+)(\))")
    return outside_fences(text, lambda line: link.sub(replace, line))


def outside_fences(text, transform):
    lines, fence = [], None
    for line in text.splitlines(keepends=True):
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            if fence is None:
                fence = marker[1]
            elif marker[1][0] == fence[0] and len(marker[1]) >= len(fence):
                fence = None
        elif fence is None:
            line = transform(line)
        lines.append(line)
    return "".join(lines)


if __name__ == "__main__":
    main()
