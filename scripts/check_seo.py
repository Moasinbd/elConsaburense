#!/usr/bin/env python3
"""Validación SEO sin servicios externos; falla CI ante errores básicos."""
from __future__ import annotations

import json
import pathlib
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

ROOT = pathlib.Path(__file__).resolve().parents[1] / "public"
SITE = "https://elconsaburense.moasin.dev"
PAGES = [
    ("/", ROOT / "index.html"),
    ("/carta-para-llevar/", ROOT / "carta-para-llevar" / "index.html"),
    ("/arroces-asados-por-encargo/", ROOT / "arroces-asados-por-encargo" / "index.html"),
    ("/celebraciones/", ROOT / "celebraciones" / "index.html"),
]


class Scan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = False
        self.title_text = []
        self.h1_count = 0
        self.description = None
        self.canonicals = []
        self.refs = []
        self.schemas = []
        self.ld_open = False
        self.ld_data = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self.title = True
        if tag == "h1":
            self.h1_count += 1
        if tag == "meta" and a.get("name") == "description":
            self.description = a.get("content")
        if tag == "link" and a.get("rel") == "canonical":
            self.canonicals.append(a.get("href"))
        if tag in ("a", "img", "script", "link", "source"):
            key = "href" if tag in ("a", "link") else "src"
            if a.get(key):
                self.refs.append((tag, a[key]))
        if tag == "img" and not a.get("alt") and "alt" not in a:
            raise AssertionError("Hay una imagen sin atributo alt")
        if tag == "script" and a.get("type") == "application/ld+json":
            self.ld_open = True
            self.ld_data = []

    def handle_data(self, data):
        if self.title:
            self.title_text.append(data)
        if self.ld_open:
            self.ld_data.append(data)

    def handle_endtag(self, tag):
        if tag == "title":
            self.title = False
        if tag == "script" and self.ld_open:
            self.schemas.append(json.loads("".join(self.ld_data)))
            self.ld_open = False


def check_local(page_path, url):
    if url.startswith(("#", "mailto:", "tel:", "data:", "javascript:")):
        return
    parsed = urlsplit(url)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return
    candidate = (ROOT / unquote(parsed.path).lstrip("/")) if parsed.path.startswith("/") else (page_path.parent / unquote(parsed.path))
    if candidate.is_dir():
        candidate /= "index.html"
    if not candidate.exists():
        raise AssertionError(f"Enlace/recurso local inexistente: {page_path.relative_to(ROOT)}: {url}")


all_canonicals = []
for path, file in PAGES:
    html = file.read_text(encoding="utf-8")
    scanner = Scan()
    scanner.feed(html)
    expected = SITE + path
    assert len(scanner.canonicals) == 1 and scanner.canonicals[0] == expected, f"canonical incorrecto: {path}"
    assert scanner.title_text and 12 <= len("".join(scanner.title_text).strip()) <= 105, f"title: {path}"
    assert scanner.description and len(scanner.description.strip()) >= 70, f"meta description: {path}"
    assert scanner.h1_count == 1, f"H1 no único: {path}"
    assert 'noindex' not in html.lower(), f"Noindex en página SEO: {path}"
    assert scanner.schemas, f"JSON-LD ausente: {path}"
    for tag, ref in scanner.refs:
        check_local(file, ref)
    kinds = {node.get("@type") for node in scanner.schemas if isinstance(node.get("@type"), str)}
    if path == "/":
        assert "Restaurant" in kinds, "Schema Restaurant ausente en la portada"
    else:
        assert "WebPage" in kinds and "BreadcrumbList" in kinds, f"Schema de página incompleto: {path}"
    if path == "/carta-para-llevar/":
        menu = next((x for x in scanner.schemas if x.get("@type") == "Menu"), None)
        assert menu, "No se detecta Menu JSON-LD"
        assert len(menu.get("hasMenuSection", [])) == 6, "Categorías de menú incompletas"
        assert sum(len(g.get("hasMenuItem", [])) for g in menu["hasMenuSection"]) == 31, "Platos de menú incompletos"
    all_canonicals.append(expected)
    print("SEO OK", path, "JSON-LD:", sorted(kinds))

tree = ET.parse(ROOT / "sitemap.xml")
ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
urls = [x.text for x in tree.findall(".//sm:loc", ns)]
assert len(urls) == 4 and sorted(urls) == sorted(all_canonicals), "Sitemap y canonical no coinciden"
robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
assert "Sitemap: " + SITE + "/sitemap.xml" in robots, "Falta declarar sitemap"
print("SEO OK: sitemap, robots, cuatro páginas y enlaces locales coherentes.")
