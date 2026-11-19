"""Check every rendered local link, image and anchor, including Pages subdirectory paths."""

import hashlib
import html
import json
import os
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_book"


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids, self.refs = set(), []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        for key in ("src", "href"):
            if key in attrs:
                self.refs.append(attrs[key])


def main():
    pages = {p.resolve(): Page(p.read_text(encoding="utf-8")) for p in SITE.rglob("*.html")}
    files = {p.resolve() for p in SITE.rglob("*") if p.is_file()}
    errors = []
    references = 0
    if len(pages) < 500:
        errors.append(f"Expected at least 500 HTML pages, found {len(pages)}")
    for path, page in pages.items():
        for ref in page.refs:
            url = urlsplit(ref)
            if url.scheme or url.netloc:
                continue
            references += 1
            target = Path(os.path.abspath(path.parent / unquote(url.path))) if url.path else path
            if url.path.startswith("/"):
                target = Path(os.path.abspath(SITE / unquote(url.path).removeprefix("/csapp-gitbook/").lstrip("/")))
            if target not in files and target / "index.html" in files:
                target /= "index.html"
            if target not in files:
                errors.append(f"{path.relative_to(SITE)}: missing {ref}")
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.append(f"{path.relative_to(SITE)}: missing anchor {ref}")
    manifest = json.loads((ROOT / "book-manifest.json").read_text(encoding="utf-8"))
    for entry in manifest["files"]:
        source = ROOT / "book" / entry["target"]
        if source.suffix == ".md":
            dest = SITE / source.relative_to(ROOT / "book").with_suffix(".html")
            if source.name == "README.md":
                dest = dest.with_name("index.html")
            if not dest.is_file():
                errors.append(f"Missing rendered page: {dest.relative_to(SITE)}")
        else:
            dest = SITE / entry["target"]
            if not dest.is_file() or hashlib.sha256(dest.read_bytes()).hexdigest() != entry["output_sha256"]:
                errors.append(f"Missing or changed asset: {entry['target']}")
    search = json.loads((SITE / "search_plus_index.json").read_text(encoding="utf-8"))
    if len(search) < 450 or not any("补码" in page["body"] for page in search.values()):
        errors.append("Chinese search index is incomplete")
    if any(path.endswith("chapter.html") for path in search):
        errors.append("Whole chapters duplicate sections in the search index")
    overview = next(page for path, page in search.items() if path.endswith("07-本书概述.html"))
    if "(x-y<0)" not in html.unescape(overview["body"]) or "(x-y<0)" in overview["body"]:
        errors.append("Search excerpts lose or misinterpret comparison operators")
    print(f"{len(pages)} HTML pages, {references} local references, {len(search)} indexed pages, {len(errors)} errors")
    for error in errors[:40]:
        print(error)
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
