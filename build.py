"""Build the standalone GitHub Pages website with the Python standard library."""

import argparse
import json
import os
import shutil
from html import escape
from pathlib import Path
from urllib.parse import urlparse

from content import PAGES, link
from illustrations import generate

HERE = Path(__file__).parent
NAV = [
    ("platform", "Platform overview", "The whole workspace"),
    ("monitoring", "Observability", "Fleet, queries & host metrics"),
    ("ai", "Intelligence", "AI, advisors & health scans"),
    ("sql-data", "SQL & data", "Query, schedule & validate"),
    ("operations", "Operations", "Backups, deployments & support"),
    ("security", "Security", "Identity, access & audit"),
]


def render(slug, page, site_url, root=None):
    root = root if root is not None else ("../" if slug else "./")
    title = escape(page["title"])
    description = escape(page["description"], quote=True)
    canonical = site_url + ("/404.html" if slug == "404" else f"/{slug}/" if slug else "/")
    product_links = ''
    for path, label, sub in NAV:
        current = 'aria-current="page"' if path == slug else ''
        product_links += f'<a href="@root@{path}/" {current}><strong>{label}</strong><span>{sub}</span></a>'
    top_links = ''
    for path, label in [("integrations", "Integrations"), ("deployment", "Deployment"), ("get-started", "Resources")]:
        current = 'aria-current="page"' if path == slug else ''
        top_links += f'<a href="@root@{path}/" {current}>{label}</a>'
    hero = ''
    if "headline" in page:
        hero = f'''<section class="hero page-hero"><div class="hero-copy"><p class="eyebrow">{page['eyebrow']}</p><h1>{page['headline']}</h1><p class="hero-lede">{page['lede']}</p></div><figure class="page-hero-art"><img src="@root@assets/{page['image']}.svg" alt="{escape(page['caption'])}" width="960" height="640" fetchpriority="high"><figcaption>PRODUCT WORKFLOW / ILLUSTRATION</figcaption></figure></section>'''
    footer_groups = ''.join(f'<div><h3>{name}</h3>' + ''.join(f'<a href="@root@{path}">{label}</a>' for path, label in items) + '</div>' for name, items in [
        ("Product", [("platform/", "Platform"), ("monitoring/", "Observability"), ("ai/", "Intelligence"), ("sql-data/", "SQL & data")]),
        ("Operate", [("operations/", "Operations"), ("security/", "Security"), ("integrations/", "Integrations"), ("deployment/", "Deployment")]),
        ("Start here", [("get-started/", "Getting started"), ("get-started/#mcp", "MCP setup"), ("get-started/#questions", "Common questions")]),
    ])
    schema = json.dumps({"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "Nexora", "applicationCategory": "DeveloperApplication", "operatingSystem": "Docker, Kubernetes", "url": site_url + "/", "description": PAGES[""]["description"]}).replace("<", "\\u003c")
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title><meta name="description" content="{description}"><meta name="theme-color" content="#151b16"><link rel="canonical" href="{canonical}"><link rel="icon" type="image/svg+xml" href="@root@assets/logo.svg"><meta property="og:type" content="website"><meta property="og:site_name" content="Nexora"><meta property="og:title" content="{title}"><meta property="og:description" content="{description}"><meta property="og:url" content="{canonical}"><meta name="twitter:card" content="summary"><link rel="stylesheet" href="@root@assets/site.css"><script src="@root@assets/site.js" defer></script><script type="application/ld+json">{schema}</script></head>
<body><a class="skip-link" href="#main">Skip to content</a><header class="site-header"><div class="header-inner"><a class="brand" href="@root@" aria-label="Nexora home"><img src="@root@assets/logo.svg" alt="" width="36" height="36"><span>nexora<span class="brand-dot">.</span></span></a><button class="menu-toggle" aria-expanded="false" aria-controls="navigation" type="button">Menu <span aria-hidden="true">☰</span></button><nav id="navigation" aria-label="Main navigation"><details class="nav-product"><summary>Product <span aria-hidden="true">⌄</span></summary><div class="product-menu">{product_links}</div></details>{top_links}<a class="nav-cta" href="@root@get-started/">Get started <span aria-hidden="true">↗</span></a></nav></div></header>
<main id="main">{hero}{page['body']}<section class="closing-cta"><div><p class="eyebrow">YOUR NEXT CLEAR STEP</p><h2>Get closer to<br>your ClickHouse.</h2></div><div><p>Bring your fleet, your questions, and your operational work into one place.</p>{link('get-started/', 'Start with Nexora', 'button dark-button')}</div></section></main>
<footer class="site-footer"><div class="footer-main"><div class="footer-brand"><a class="brand" href="@root@"><img src="@root@assets/logo.svg" alt="" width="36" height="36"><span>nexora<span class="brand-dot">.</span></span></a><p>The ops architect<br>beside ClickHouse.</p></div>{footer_groups}</div><div class="footer-bottom"><span>© 2026 Nexora</span><p>Built for the people behind the database.</p><span>ClickHouse is a trademark of ClickHouse, Inc.</span></div></footer></body></html>'''.replace('@root@', root)


def build(site_url):
    parsed = urlparse(site_url)
    if parsed.scheme != "https" or not parsed.netloc or parsed.query or parsed.fragment:
        raise ValueError("SITE_URL must be an HTTPS origin with an optional repository path")
    site_url = site_url.rstrip("/")
    generate()
    dist = HERE / "dist"
    if dist.exists():
        shutil.rmtree(dist)
    (dist / "assets").mkdir(parents=True)
    shutil.copytree(HERE / "assets", dist / "assets", dirs_exist_ok=True)
    for slug, page in PAGES.items():
        directory = dist / slug
        directory.mkdir(exist_ok=True)
        (directory / "index.html").write_text(render(slug, page, site_url), encoding="utf-8")
    not_found = {"title": "Page not found — Nexora", "description": "Find your way back to the Nexora product website.", "body": '<section class="section not-found"><p class="eyebrow">404 / OUT OF RANGE</p><h1>This path needs<br>a new direction.</h1><p>The page may have moved. Start from the platform or return to the homepage.</p><div class="button-row">' + link('', 'Back to home', 'button primary') + link('platform/', 'Explore the platform', 'button secondary') + '</div></section>'}
    (dist / "404.html").write_text(render("404", not_found, site_url, site_url + "/"), encoding="utf-8")
    (dist / ".nojekyll").touch()
    urls = ''.join(f'<url><loc>{escape(site_url + ("/" + slug if slug else "") + "/")}</loc></url>' for slug in PAGES)
    (dist / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>', encoding="utf-8")
    # Project Pages shares its host-level robots.txt with other repositories; no restrictive rules.
    (dist / "robots.txt").write_text(f'User-agent: *\nAllow: /\nSitemap: {site_url}/sitemap.xml\n', encoding="utf-8")
    print(f"Built {len(PAGES)} pages and a 404 page in {dist}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-url", default=os.environ.get("SITE_URL", "https://nexora-distributed.github.io/website"))
    args = parser.parse_args()
    build(args.site_url)
