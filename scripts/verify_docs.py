#!/usr/bin/env python3
"""Check the 21-language Lorem Picsum API reference for completeness."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LANGUAGES = [
    ("en", "English", "README.md", None),
    ("ar", "العربية", "docs/ar.md", "ar"),
    ("cs", "Čeština", "docs/cs.md", "cs"),
    ("de", "Deutsch", "docs/de.md", "de"),
    ("es", "Español", "docs/es.md", "es"),
    ("et", "Eesti", "docs/et.md", "et"),
    ("hi", "हिन्दी", "docs/hi.md", "hi"),
    ("id", "Bahasa Indonesia", "docs/id.md", "id"),
    ("ja", "日本語", "docs/ja.md", "ja"),
    ("ko", "한국어", "docs/ko.md", "ko"),
    ("lt", "Lietuvių", "docs/lt.md", "lt"),
    ("nl", "Nederlands", "docs/nl.md", "nl"),
    ("pl", "Polski", "docs/pl.md", "pl"),
    ("pt-PT", "Português (Portugal)", "docs/pt-PT.md", "pt-pt"),
    ("rw", "Ikinyarwanda", "docs/rw.md", "rw"),
    ("sv", "Svenska", "docs/sv.md", "sv"),
    ("tr", "Türkçe", "docs/tr.md", "tr"),
    ("uk", "Українська", "docs/uk.md", "uk"),
    ("ur", "اردو", "docs/ur.md", "ur"),
    ("vi", "Tiếng Việt", "docs/vi.md", "vi"),
    ("zh-TW", "繁體中文", "docs/zh-TW.md", "zh-tw"),
]

ANCHORS = [
    "overview",
    "quick-start",
    "image-urls",
    "dimensions",
    "formats",
    "random-rectangle",
    "random-square",
    "seeded",
    "pinned",
    "query",
    "presets",
    "json",
    "list",
    "info-id",
    "info-seed",
    "fields",
    "examples",
    "categories",
    "headers",
    "errors",
    "code",
    "html",
    "markdown",
    "curl",
    "javascript",
    "python",
    "license",
    "mcp",
]

CATEGORY_IDS = [
    "aerial",
    "agriculture",
    "animals",
    "architecture",
    "birds",
    "city",
    "coasts",
    "deserts",
    "food",
    "freshwater",
    "gardens",
    "industry",
    "insects",
    "interiors",
    "landmarks",
    "landscapes",
    "macro",
    "marine",
    "mountains",
    "music",
    "night",
    "objects",
    "pets",
    "plants",
    "sculpture",
    "skies",
    "snow",
    "sports",
    "technology",
    "textures",
    "transport",
    "woodlands",
    "workspaces",
]

REQUIRED_SNIPPETS = [
    "https://picsum.org/v2/list",
    "https://picsum.org/mcp",
    "photos:read",
    "search_photos",
    "get_photo",
    "list_categories",
    "build_image_url",
    "hello@picsum.org",
    "CC0 1.0",
    "picsum.photos",
    "1000561303",
    "179363399",
    "Syony",
    "Landmannalaugar",
    "Retry-After",
    "Cross-Origin-Resource-Policy",
    "Access-Control-Allow-Origin",
    "Picsum-Total",
    "Picsum-ID",
    "no-store",
    "max-age=3600",
    "max-age=86400",
    "s-maxage=604800",
    "max-age=300",
    "grayscale=1",
    "https://picsum.org/800/600",
    "https://picsum.org/640",
    "https://picsum.org/1200/800",
    "https://picsum.org/600/800",
    "https://picsum.org/1280/720",
    "https://picsum.org/1920/1080",
    '{"error":"Use dimensions from 1 to 2000, JPG or WebP, grayscale, and blur from 1 to 10."}',
    '{"error":"Invalid page or limit."}',
    '{"error":"Unknown image ID."}',
    "/g/{width}/{height}",
]

FENCE_RE = re.compile(r"```[^\n]*\n.*?```", re.DOTALL)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
STUB_MARKERS = ("TODO:", "TRANSLATION NEEDED", "lorem ipsum", "XXX-STUB")


def navigation(current_code: str) -> str:
    parts: list[str] = []
    for code, name, _path, _locale in LANGUAGES:
        if code == current_code:
            parts.append(f"**{name}**")
            continue
        if current_code == "en":
            target = f"docs/{code}.md"
        elif code == "en":
            target = "../README.md"
        else:
            target = f"./{code}.md"
        parts.append(f"[{name}]({target})")
    return " · ".join(parts)


def fences(text: str) -> list[str]:
    return FENCE_RE.findall(text)


def main() -> int:
    errors: list[str] = []
    english_path = ROOT / "README.md"
    if not english_path.is_file():
        print("missing README.md")
        return 1
    english = english_path.read_text(encoding="utf-8")
    english_fences = fences(english)

    if len(LANGUAGES) != 21:
        errors.append(f"language table has {len(LANGUAGES)} rows, expected 21")
    if len(CATEGORY_IDS) != 33:
        errors.append(f"category table has {len(CATEGORY_IDS)} ids, expected 33")

    for code, name, rel, locale in LANGUAGES:
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"{rel}: missing")
            continue
        text = path.read_text(encoding="utf-8")
        if not text.endswith("\n"):
            errors.append(f"{rel}: file does not end with a newline")
        first = text.splitlines()[0] if text else ""
        expected_nav = navigation(code)
        if first != expected_nav:
            errors.append(f"{rel}: language navigation does not match")
            if name not in first:
                errors.append(f"{rel}: navigation is missing {name}")
        if f"**{name}**" not in first:
            errors.append(f"{rel}: current language is not bold")

        for anchor in ANCHORS:
            if f'<a id="{anchor}"></a>' not in text:
                errors.append(f"{rel}: missing anchor {anchor}")

        for snippet in REQUIRED_SNIPPETS:
            if snippet not in text:
                errors.append(f"{rel}: missing required text {snippet!r}")

        for category_id in CATEGORY_IDS:
            if f"`{category_id}`" not in text:
                errors.append(f"{rel}: missing category id `{category_id}`")

        file_fences = fences(text)
        if file_fences != english_fences:
            errors.append(
                f"{rel}: code fences differ from English "
                f"({len(file_fences)} fences, English has {len(english_fences)})"
            )

        for marker in STUB_MARKERS:
            if marker in text:
                errors.append(f"{rel}: stub marker {marker!r}")

        if len(text) < 9000:
            errors.append(f"{rel}: looks short ({len(text)} characters)")

        if locale is None:
            if "https://picsum.org/terms" not in text:
                errors.append(f"{rel}: missing English terms URL")
            if "https://picsum.org/connect" not in text:
                errors.append(f"{rel}: missing English connect URL")
            if "https://picsum.org/en/" in text:
                errors.append(f"{rel}: unexpected /en/ locale prefix")
        else:
            for suffix, label in (("", "homepage"), ("/connect", "connect"), ("/terms", "terms")):
                url = f"https://picsum.org/{locale}{suffix}"
                if url not in text:
                    errors.append(f"{rel}: missing localized {label} URL {url}")

        for match in LINK_RE.finditer(text):
            target = match.group(1)
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            if target.startswith("<"):
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"{rel}: link escapes the repo: {target}")
                continue
            if not resolved.is_file():
                errors.append(f"{rel}: broken relative link {target}")

    if errors:
        print(f"{len(errors)} problem(s):")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"OK: {len(LANGUAGES)} files, navigation, anchors, fences, categories, and links.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
