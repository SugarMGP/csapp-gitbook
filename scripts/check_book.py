"""Check the Markdown pages, images, downloads and anchors consumed by GitBook."""

import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

BOOK = Path(__file__).resolve().parents[1] / "book"


def main():
    root = BOOK.resolve()
    files = list(root.rglob("*.md"))
    errors, targets, anchor_cache = [], set(), {}
    count = 0
    for path in files:
        for ref in references(path.read_text(encoding="utf-8-sig")):
            url = urlsplit(ref)
            if url.scheme or url.netloc:
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            count += 1
            targets.add(target)
            if not target.is_relative_to(root) or not target.is_file():
                errors.append(f"{path.relative_to(root)}: missing file {ref}")
            elif url.fragment and target.suffix == ".md":
                if target not in anchor_cache:
                    anchor_cache[target] = anchors(target.read_text(encoding="utf-8-sig"))
                if unquote(url.fragment) not in anchor_cache[target]:
                    errors.append(f"{path.relative_to(root)}: missing anchor {ref}")
    for path in files:
        if path.name != "SUMMARY.md" and path not in targets:
            errors.append(f"Page is not linked: {path.relative_to(root)}")
    if not files or not (root / "README.md").is_file() or not (root / "SUMMARY.md").is_file():
        errors.append("Missing book homepage or navigation")
    print(f"{len(files)} Markdown files, {count} local references, {len(errors)} errors")
    for error in errors:
        print(error)
    if errors:
        raise SystemExit(1)


def anchors(text):
    text = re.sub(r"^(`{3,}|~{3,}).*?^\1[^\n]*$", "", text, flags=re.M | re.S)
    found = set(re.findall(r'<a\b[^>]*\bid=["\']([^"\']+)', text))
    counts = {}
    for heading in re.findall(r"^#{1,6} (.+)$", text, re.M):
        heading = re.sub(r"<[^>]+>", "", heading)
        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        found.add(f"{slug}-{count}" if count else slug)
    return found


def references(text):
    text = re.sub(r"^(`{3,}|~{3,}).*?^\1[^\n]*$", "", text, flags=re.M | re.S)
    for match in re.finditer(r'!?\[[^\]\n]*\]\((<[^>]+>|[^)\s]+)(?:\s+"(?:\\.|[^"\\])*")?\)', text):
        yield match[1].strip().strip("<>")
    for match in re.finditer(r'^\[(?!\^)[^\]]+\]:\s*(\S+)', text, re.M):
        yield match[1].strip("<>")
    for match in re.finditer(r'<(?:img|a)\b[^>]*?\b(?:src|href)=["\']([^"\']+)', text, re.I):
        yield match[1]


if __name__ == "__main__":
    main()
