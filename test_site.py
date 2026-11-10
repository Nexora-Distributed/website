"""Validate the complete static artifact, including project-URL navigation."""

import json
import unittest
import xml.etree.ElementTree as ET
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse

from build import HERE, PAGES, build

SITE_URL = "https://nexora-distributed.github.io/website"


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        build(SITE_URL)
        cls.dist = HERE / "dist"
        cls.documents = {path: Document(path.read_text()) for path in cls.dist.rglob("*.html")}

    def test_all_routes_and_metadata(self):
        self.assertEqual(len(self.documents), len(PAGES) + 1)
        titles = []
        for path, doc in self.documents.items():
            with self.subTest(page=str(path.relative_to(self.dist))):
                counts = Counter(tag for tag, _ in doc.tags)
                self.assertEqual(counts["h1"], 1)
                self.assertEqual(counts["main"], 1)
                self.assertEqual(counts["title"], 1)
                self.assertTrue(any(tag == "html" and attrs.get("lang") == "en" for tag, attrs in doc.tags))
                ids = [attrs["id"] for _, attrs in doc.tags if "id" in attrs]
                self.assertEqual(len(ids), len(set(ids)), "duplicate HTML id")
                self.assertTrue(any(tag == "meta" and attrs.get("name") == "description" and len(attrs.get("content", "")) > 40 for tag, attrs in doc.tags))
                self.assertTrue(any(tag == "link" and attrs.get("rel") == "canonical" for tag, attrs in doc.tags))
                source = path.read_text()
                self.assertNotIn("@root@", source)
                titles.append(source.split("<title>")[1].split("</title>")[0])
                for tag, attrs in doc.tags:
                    if tag == "img":
                        self.assertIn("alt", attrs)
                        self.assertIn("width", attrs)
                        self.assertIn("height", attrs)
                    if "aria-controls" in attrs:
                        self.assertIn(attrs["aria-controls"], ids)
        self.assertEqual(len(titles), len(set(titles)))

    def test_links_assets_and_fragment_targets(self):
        checked = 0
        for path, doc in self.documents.items():
            relative = path.relative_to(self.dist).as_posix()
            page_url = SITE_URL + "/" + relative
            for tag, attrs in doc.tags:
                value = attrs.get("href") or attrs.get("src")
                if not value:
                    continue
                target = urlparse(urljoin(page_url, value))
                with self.subTest(page=relative, link=value):
                    self.assertNotEqual(target.scheme, "javascript")
                    if target.netloc != urlparse(SITE_URL).netloc:
                        continue
                    prefix = urlparse(SITE_URL).path + "/"
                    self.assertTrue(target.path.startswith(prefix), "link escaped the GitHub project path")
                    local = self.dist / unquote(target.path[len(prefix):])
                    if target.path.endswith("/"):
                        local /= "index.html"
                    self.assertTrue(local.is_file(), f"missing target {local}")
                    if target.fragment:
                        self.assertIn(local, self.documents)
                        self.assertIn(target.fragment, [a.get("id") for _, a in self.documents[local].tags])
                    checked += 1
        self.assertGreater(checked, 400)

    def test_illustrations_and_sitemap(self):
        illustrations = list((self.dist / "assets").glob("*.svg"))
        self.assertGreaterEqual(len(illustrations), 21)
        for path in illustrations:
            tree = ET.parse(path)
            self.assertEqual(tree.getroot().get("viewBox"), "0 0 40 40" if path.name == "logo.svg" else "0 0 960 640")
        sitemap = ET.parse(self.dist / "sitemap.xml")
        urls = [node.text for node in sitemap.findall(".//{*}loc")]
        self.assertEqual(len(urls), len(PAGES))
        self.assertTrue(all(url.startswith(SITE_URL + "/") for url in urls))
        self.assertTrue((self.dist / ".nojekyll").exists())

    def test_public_guide_omits_installation_and_uses_vector_icons(self):
        guide = (self.dist / "get-started/index.html").read_text()
        for withheld in ["git clone", "make full-d", "localhost:8080", "source access", 'id="evaluate"', 'data-copy=']:
            self.assertNotIn(withheld, guide)
        for path, doc in self.documents.items():
            source = path.read_text()
            for glyph in "✓☰◫⌘▥◇⚙▱⌁✳↳↗⌄":
                self.assertNotIn(glyph, source)
            self.assertTrue(any(attrs.get("class") == "icon" and attrs.get("aria-hidden") == "true" for _, attrs in doc.tags))
            self.assertTrue(any(attrs.get("class") == "motion-toggle" and attrs.get("aria-pressed") == "false" for _, attrs in doc.tags))
        for path in (self.dist / "assets").glob("*.svg"):
            if path.name == "logo.svg":
                continue
            source = path.read_text()
            self.assertIn("@keyframes flow", source)
            self.assertIn("prefers-reduced-motion:reduce", source)
            self.assertIn("#still:target", source)

    def test_structured_data_and_accessible_tabs(self):
        for path in self.documents:
            source = path.read_text()
            data = source.split('<script type="application/ld+json">')[1].split('</script>')[0]
            self.assertEqual(json.loads(data)["name"], "Nexora")
        doc = self.documents[self.dist / "index.html"]
        tabs = [attrs for _, attrs in doc.tags if attrs.get("role") == "tab"]
        panels = [attrs for _, attrs in doc.tags if attrs.get("role") == "tabpanel"]
        self.assertEqual(len(tabs), 3)
        self.assertEqual(len(panels), 3)
        self.assertEqual(sum(tab.get("aria-selected") == "true" for tab in tabs), 1)
        self.assertEqual(sum("hidden" not in panel for panel in panels), 1)
        for tab in tabs:
            panel = next(panel for panel in panels if panel["id"] == tab["aria-controls"])
            self.assertEqual(panel["aria-labelledby"], tab["id"])


if __name__ == "__main__":
    unittest.main()
