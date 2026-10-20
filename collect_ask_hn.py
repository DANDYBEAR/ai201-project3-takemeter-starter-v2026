#!/usr/bin/env python3
"""Collect complete public Ask HN text posts into the course CSV shape."""

import argparse
import csv
import html
import json
import re
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, OSError, ValueError):
    pass


TARGET = 200
OUT = Path(__file__).with_name("labels.csv")
API = "https://hn.algolia.com/api/v1/search_by_date"


class PlainText(HTMLParser):
    """Preserve all visible post text while removing HN's HTML markup."""

    BLOCKS = {"p", "br", "li", "pre", "blockquote"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in self.BLOCKS:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in self.BLOCKS:
            self.parts.append("\n")

    def handle_data(self, data):
        self.parts.append(data)

    def text(self) -> str:
        value = html.unescape("".join(self.parts)).replace("\r\n", "\n")
        value = re.sub(r"[ \t]+", " ", value)
        value = re.sub(r" *\n *", "\n", value)
        value = re.sub(r"\n{3,}", "\n\n", value)
        return value.strip()


def plain_text(markup: str) -> str:
    parser = PlainText()
    parser.feed(markup)
    return parser.text()


def fetch_page(page: int) -> dict:
    query = urllib.parse.urlencode(
        {"tags": "ask_hn", "hitsPerPage": 100, "page": page}
    )
    request = urllib.request.Request(
        f"{API}?{query}", headers={"User-Agent": "TakeMeter course dataset collector"}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def collect(target: int) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    seen_ids: set[str] = set()
    page = 0

    while len(rows) < target:
        payload = fetch_page(page)
        hits = payload.get("hits", [])
        if not hits:
            raise RuntimeError(f"API returned no posts on page {page}")

        for hit in hits:
            object_id = str(hit.get("objectID") or "")
            title = (hit.get("title") or "").strip()
            body_markup = hit.get("story_text") or ""
            body = plain_text(body_markup)
            if not object_id or object_id in seen_ids or not title or not body:
                continue
            seen_ids.add(object_id)
            rows.append({"text": f"{title}\n\n{body}", "label": "", "note": ""})
            if len(rows) == target:
                break
        page += 1

    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--show", type=int, help="print the Nth eligible post without writing")
    parser.add_argument(
        "--show-range", nargs=2, type=int, metavar=("START", "END"),
        help="print an inclusive one-based range without writing",
    )
    args = parser.parse_args()

    if args.show_range:
        start, end = args.show_range
        if start < 1 or end < start:
            parser.error("--show-range requires 1 <= START <= END")
        for number, row in enumerate(collect(end)[start - 1:end], start):
            print(f"===== ELIGIBLE {number} =====")
            print(row["text"])
            print()
        return

    if args.show:
        row = collect(args.show)[-1]
        print(row["text"])
        return

    rows = collect(TARGET)

    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["text", "label", "note"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} complete Ask HN posts to {OUT}")


if __name__ == "__main__":
    main()
