import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE_URL = "https://itnexus.dev/"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class SeoFilesTest(unittest.TestCase):
    def test_required_seo_files_exist(self):
        for path in ("robots.txt", "sitemap.xml", "site.webmanifest"):
            with self.subTest(path=path):
                self.assertTrue((ROOT / path).is_file(), f"{path} is missing")

    def test_robots_points_to_sitemap_and_allows_crawlers(self):
        robots = read("robots.txt")
        self.assertIn("User-agent: *", robots)
        self.assertIn("Allow: /", robots)
        self.assertIn(f"Sitemap: {SITE_URL}sitemap.xml", robots)

    def test_sitemap_contains_canonical_homepage(self):
        sitemap = read("sitemap.xml")
        self.assertIn(f"<loc>{SITE_URL}</loc>", sitemap)
        self.assertIn("<changefreq>monthly</changefreq>", sitemap)
        self.assertIn("<priority>1.0</priority>", sitemap)

    def test_index_contains_social_and_structured_metadata(self):
        html = read("index.html")
        expected = [
            f'<link rel="canonical" href="{SITE_URL}" />',
            '<link rel="manifest" href="/site.webmanifest" />',
            '<meta property="og:type" content="website" />',
            f'<meta property="og:url" content="{SITE_URL}" />',
            '<meta property="og:title" content="IT Nexus — мобильная и продуктовая разработка" />',
            '<meta name="twitter:card" content="summary" />',
            '<script type="application/ld+json">',
            '"@type": "Organization"',
            f'"url": "{SITE_URL}"',
        ]
        for snippet in expected:
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, html)


if __name__ == "__main__":
    unittest.main()
